#!/usr/bin/env python3
"""Claude Code PreToolUse hook (matcher: Bash|PowerShell).

Refuses any regression test run. Full suites run only in nightly CI (in probanda-dev,
the data-mcp-tests and skills-python-tests workflows), because a local run blocks the
session for hours. A test runner may run only test files named by path that are
untracked, uncommitted or changed in a commit of the last 24 hours: the tests of recent
work (TDD). Refused: a folder, a runner with no file, a test file unchanged for 24 hours, unittest, npm test,
node scripts/test.mjs, vitest, jest, mocha, and pytest.main/unittest.main in Python
code. The refusal is a hard deny, not an ask, so it holds in every permission mode.

Do not restrict: a command that only names a runner or a test (grep pytest, git log --
tests/, a commit message), or a non-test script (python scripts/check_plugin.py). Only
the executed command counts. Fails OPEN on any unexpected error, loudly.
"""
import json
import os
import re
import shlex
import subprocess
import sys

HEREDOC_RE = re.compile(r"<<-?\s*(['\"]?)(\w+)\1[^\n]*\n.*?\n\s*\2(?=\s|$)", re.DOTALL)
IN_CODE_RE = re.compile(r"\b(pytest|unittest)\.main\b")
TEST_FILE_RE = re.compile(r"(^|[\\/])(test_[^\\/]*\.py|[^\\/]*_test\.py|[^\\/]*\.test\.[cm]?[jt]s)$")
OPERATORS = {";", "&", "&&", "|", "||", "(", ")"}
PYTHONS = {"python", "python3", "py"}
REASON = (
    "Refused: regression suites run only in the nightly GitHub Actions workflows. Run only "
    "a test file changed in the last 24 hours (committed or not), named by its path. Do "
    "not work around this refusal, for example through a script file or another tool."
)


def segments(command):
    lexer = shlex.shlex(HEREDOC_RE.sub(" ", command), posix=False, punctuation_chars=";&|()")
    lexer.whitespace_split = True
    seg = []
    for tok in lexer:
        if tok in OPERATORS:
            if seg:
                yield seg
            seg = []
        else:
            seg.append(tok.strip("'\""))
    if seg:
        yield seg


def name(tok):
    base = re.split(r"[\\/]", tok)[-1].lower()
    return base[:-4] if base.endswith(".exe") else base


def targets(seg):
    """None when the segment runs no tests, "refuse" for a whole-suite runner, else the
    file-like arguments the runner was given."""
    while seg and re.match(r"^\w+=", seg[0]):  # VAR=value prefix
        seg = seg[1:]
    if not seg:
        return None
    cmd, args = name(seg[0]), seg[1:]
    if cmd in ("uv", "poetry", "pipenv") and args[:1] == ["run"]:
        return targets(args[1:])
    if cmd in ("npx", "pnpm", "yarn", "bunx", "uvx") and args:
        return "refuse" if name(args[0]) in ("vitest", "jest", "mocha", "pytest") else None
    if cmd in ("vitest", "jest", "mocha"):
        return "refuse"
    if cmd == "npm":
        if args[:1] in (["test"], ["t"], ["tst"]) or (args[:1] in (["run"], ["run-script"]) and args[1:2] and args[1].startswith("test")):
            return "refuse"
        return None
    if cmd in ("pytest", "py.test"):
        return args
    if cmd in PYTHONS:
        rest = list(args)
        while rest and rest[0].startswith("-"):
            opt = rest.pop(0)
            if opt == "-m" and rest:
                module = rest.pop(0)
                return rest if module == "pytest" else "refuse" if module == "unittest" else None
            if opt == "-c":
                return None
            if opt in ("-X", "-W") and rest:
                rest.pop(0)
        return rest[:1] if rest and TEST_FILE_RE.search(rest[0]) else None
    if cmd == "node":
        rest = [a for a in args if not a.startswith("-")]
        if any(name(a) == "test.mjs" for a in rest):
            return "refuse"
        if "--test" in args:
            return rest
        return rest[:1] if rest and TEST_FILE_RE.search(rest[0]) else None
    return None


def resolve(arg, cwd):
    """The argument as a local path: $HOME, ~ and other variables expanded as the shell
    would, and Git Bash's /c/... form turned into C:/...."""
    path = re.sub(r"^~(?=[\\/]|$)|\$\{?HOME\}?", lambda m: os.path.expanduser("~").replace("\\", "/"), arg)
    path = os.path.expandvars(path)
    if os.name == "nt":
        path = re.sub(r"^/([a-zA-Z])(?=/)", r"\1:", path)
    return os.path.join(cwd, path)


def recent(path):
    """True for a file that is untracked, ignored or changed, or changed in a commit of the
    last 24 hours, or outside any git repo. Commit dates, not file times: a pull or a
    checkout resets the file times of old tests."""
    git = ["git", "-C", os.path.dirname(path)]
    out = subprocess.run([*git, "status", "--porcelain", "--ignored", "--", path], capture_output=True, text=True)
    if out.returncode != 0 or out.stdout.strip():
        return True
    log = subprocess.run([*git, "log", "-1", "--since=24.hours", "--format=%H", "--", path], capture_output=True, text=True)
    commit = log.stdout.strip()
    if not commit:
        return False
    # A shallow clone's boundary commit looks as if it added every file: it proves nothing.
    shallow = subprocess.run([*git, "rev-parse", "--git-path", "shallow"], capture_output=True, text=True).stdout.strip()
    shallow = os.path.join(os.path.dirname(path), shallow)
    return not (os.path.isfile(shallow) and commit in open(shallow).read().split())


def refusal(command, cwd):
    if IN_CODE_RE.search(command):
        return REASON
    for seg in segments(command):
        found = targets(seg)
        if found is None:
            continue
        if found == "refuse":
            return REASON
        files = []
        for arg in found:
            if arg.startswith("-"):
                continue
            path = resolve(arg.split("::")[0], cwd)
            if os.path.exists(path) or re.search(r"[\\/]|::|\.[cm]?[jt]s$|\.py$", arg):
                files.append(path)
        if not files or not all(os.path.isfile(p) and recent(p) for p in files):
            return REASON
    return None


def main():
    payload = json.load(sys.stdin)
    command = (payload.get("tool_input") or {}).get("command")
    if payload.get("tool_name") not in ("Bash", "PowerShell") or not isinstance(command, str):
        return 0
    reason = refusal(command, payload.get("cwd") or os.getcwd())
    if reason:
        sys.stdout.write(json.dumps({"hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": reason,
        }}) + "\n")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except SystemExit:
        raise
    except Exception as exc:  # fail OPEN, loudly
        sys.stderr.write(f"no-regression-suite hook error (allowing command): {type(exc).__name__}: {exc}\n")
        sys.exit(0)
