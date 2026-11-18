#!/usr/bin/env python3
"""Claude Code PreToolUse hook (matcher: Bash|PowerShell).

Refuses any regression test run. Full suites run only in each repo's nightly CI workflow
(in probanda-dev, data-mcp-tests and skills-python-tests; in probanda-web, nightly-tests),
because a local run blocks the session for hours. A test runner may run only test files named by path that are
untracked, uncommitted or changed in a commit of the last 24 hours: the tests of recent
work (TDD). Refused: a folder, a runner with no file, a test file unchanged for 24 hours, unittest, npm test,
node scripts/test.mjs, vitest in watch mode or without named test files, jest, mocha,
and pytest.main/unittest.main in Python code. `vitest run <test files>` runs under the
same 24-hour rule as pytest, also as `node .../vitest.mjs run`. `firebase emulators:exec
"<command>"` is judged by its inner command, so a whole emulator suite is refused. A
redirect (2>&1, > out.log) is not an argument. The refusal is a hard deny, not an ask, so it holds in every permission mode.

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
# `firebase emulators:exec` flags that take a value; the script is its first other argument.
EMULATOR_VALUE_FLAGS = {"--only", "--project", "-P", "--import", "--export-on-exit", "--config", "--log-verbosity"}
# A redirect (2>&1, > out.log) is not an argument of the command it follows.
REDIRECT_RE = re.compile(r"(?<=\s)\d*(?:>>?|<)(?:&\d+|\s*[^\s;&|()]+)")
VITEST_VALUE_FLAGS = {"--config", "-c", "--project", "-t", "--testNamePattern", "--root", "-r", "--dir", "--reporter"}
OPERATORS = {";", "&", "&&", "|", "||", "(", ")"}
PYTHONS = {"python", "python3", "py"}
REASON = (
    "Refused: regression suites run only in the nightly GitHub Actions workflows. Run only "
    "a test file changed in the last 24 hours (committed or not), named by its path. Do "
    "not work around this refusal, for example through a script file or another tool."
)


QUOTED_RE = re.compile(r"\"[^\"]*\"|'[^']*'")
MASK = str.maketrans({c: chr(0xE000 + i) for i, c in enumerate(";&|()")})
UNMASK = str.maketrans({chr(0xE000 + i): c for i, c in enumerate(";&|()")})


def segments(command):
    # The lexer (posix=False, kept for Windows backslash paths) sees a quote only at the start of
    # a word, so --flag="a|b" would split on its |. Operators inside quotes are masked first.
    text = QUOTED_RE.sub(lambda m: m.group(0).translate(MASK), HEREDOC_RE.sub(" ", command))
    text = REDIRECT_RE.sub(" ", text)
    lexer = shlex.shlex(text, posix=False, punctuation_chars=";&|()")
    lexer.whitespace_split = True
    seg = []
    for tok in lexer:
        if tok in OPERATORS:
            if seg:
                yield seg
            seg = []
        else:
            seg.append(tok.translate(UNMASK).strip("'\""))
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
    if cmd == "firebase":
        return emulator_script(args)
    if cmd in ("npx", "pnpm", "yarn", "bunx", "uvx") and args:
        if name(args[0]) == "vitest":
            return vitest_files(args[1:])
        if name(args[0]) == "firebase":
            return emulator_script(args[1:])
        return "refuse" if name(args[0]) in ("jest", "mocha", "pytest") else None
    if cmd == "vitest":
        return vitest_files(args)
    if cmd in ("jest", "mocha"):
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
        if rest and name(rest[0]) in ("vitest.mjs", "vitest"):
            return vitest_files(args[args.index(rest[0]) + 1:])
        if any(name(a) == "test.mjs" for a in rest):
            return "refuse"
        if "--test" in args:
            return rest
        return rest[:1] if rest and TEST_FILE_RE.search(rest[0]) else None
    return None


def emulator_script(args):
    """`firebase emulators:exec [flags] "<command>"`: ("script", command), judged as a command of
    its own. No script is refused; any other firebase command runs no tests."""
    if "emulators:exec" not in args:
        return None
    rest = args[args.index("emulators:exec") + 1:]
    while rest:
        arg = rest.pop(0)
        if arg in EMULATOR_VALUE_FLAGS and rest:
            rest.pop(0)
        elif not arg.startswith("-"):
            return ("script", arg)
    return "refuse"


def vitest_files(args):
    """`vitest run <test files>`: the files named. Watch mode (no `run`), a run with no file
    or a filter that is not a test file path would reach past the named tests."""
    if args[:1] != ["run"]:
        return "refuse"
    files, rest = [], args[1:]
    while rest:
        arg = rest.pop(0)
        if arg in VITEST_VALUE_FLAGS and rest:
            rest.pop(0)
        elif not arg.startswith("-"):
            files.append(arg)
    if not files or not all(TEST_FILE_RE.search(f) for f in files):
        return "refuse"
    return files


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
        if isinstance(found, tuple):
            inner = refusal(found[1], cwd)
            if inner:
                return inner
            continue
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
    payload = json.loads(sys.stdin.buffer.read().decode("utf-8"))
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
