#!/usr/bin/env python3
"""
Myskillium Spore - Bootstrap Hook

A self-bootstrapping SessionStart hook that syncs and checks for updates to
the Myskillium bootstrap skill docs. Embeds all 7 planning docs and writes
them to .claude/skills/bootstrap/ when needed.

Workflow (optimized for minimal intrusion - fastest checks first):
1. 24h fast path → silent exit if <24h since last check (most common)
2. Source template check → silent exit if git remote is Mharbulous/Myskillium
3. Hash comparison → sync docs if any difference (missing, added, or modified)
4. Remote check → notify if upstream update available

Performance: Lazy imports keep the fast path (~99% of invocations) minimal -
only os, sys, datetime, pathlib loaded. Heavy modules (hashlib, subprocess,
urllib) are imported only when needed (once per 24h at most).
"""

# Minimal imports for fast path - only what's needed to check version.yml
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

# Lazy imports - these are only loaded when actually needed (once per 24h)
# This keeps the fast path (~99% of invocations) as light as possible
hashlib = None
subprocess = None
urllib_request = None
urllib_error = None


def _import_hashlib():
    global hashlib
    if hashlib is None:
        import hashlib as _hashlib
        hashlib = _hashlib
    return hashlib


def _import_subprocess():
    global subprocess
    if subprocess is None:
        import subprocess as _subprocess
        subprocess = _subprocess
    return subprocess


def _import_urllib():
    global urllib_request, urllib_error
    if urllib_request is None:
        import urllib.request as _urllib_request
        import urllib.error as _urllib_error
        urllib_request = _urllib_request
        urllib_error = _urllib_error
    return urllib_request, urllib_error

# Source template identifier - split to resist simple text searches
# Assembled at runtime: "Mharbulous/Myskillium"
_SOURCE_OWNER = "Mharbulous"
_SOURCE_REPO = "Myskillium"

# Remote version.yml for update checks (same format as local, just need the hash)
REMOTE_VERSION_URL = f"https://raw.githubusercontent.com/{_SOURCE_OWNER}/{_SOURCE_REPO}/main/.claude/skills/bootstrap/version.yml"

# Target directory for bootstrap skill docs
BOOTSTRAP_SKILL_DIR = ".claude/skills/bootstrap"

# Version file for tracking last check (replaces self-modifying timestamp)
VERSION_FILE = ".claude/skills/bootstrap/version.yml"

# All 7 planning docs embedded as strings
EMBEDDED_DOCS = {
    "01-prd.md": """\
# Myskillium PRD (Product Requirements Document)

## Vision

A GitHub template repository for sharing Claude Code skills, commands, and agents across multiple projects. Works on CLI and web, no submodules, no symlinks.

## Problem Statement

StoryTree's submodule + symlink architecture failed:
- Symlinks fragile on Windows
- Claude Code web can't follow symlinks
- Files get overwritten during sync
- Too complex to maintain

## Goals

1. Share skills/commands across multiple GitHub repos
2. Work on VS Code Claude Code CLI (Windows/Mac/Linux)
3. Work on Claude Code web
4. Edit in Myskillium, sync to dependents
5. Simple enough that anyone can understand it

## Non-Goals

- Real-time sync (manual sync is acceptable)
- Bidirectional sync (one-way from Myskillium to dependents)
- Package manager distribution (npm/pip) - future consideration

## User Stories

1. As a developer, I want to create a new project from Myskillium template so I get all skills/commands immediately
2. As a developer, I want to run a sync script to get the latest skills/commands from Myskillium
3. As a maintainer, I want to edit skills in Myskillium and have dependents pull updates
4. As a web user, I want skills to work in Claude Code web (files committed to repo)

## Success Metrics

- New project setup: < 5 minutes
- Sync operation: < 30 seconds
- Zero symlinks in any repo
- Works on Windows without Developer Mode

## Components to Include

- Claude Code skills (story-tree, story-execution, streamline, etc.)
- Custom slash commands (ci-*, design-story, etc.)
- Helper scripts
- GitHub workflows
- Database schema (story-tree)
- Xstory GUI

## Out of Scope (v1)

- Automated PR-based sync (future: handover 016)
- Plugin marketplace distribution
- MCP server approach
""",

    "02-architecture.md": """\
# Myskillium Architecture

## Core Principle

**What you see is what you get.** No indirection layers, no symlinks, no submodules.

## Directory Structure

```
Myskillium/
├── .claude/                    # Claude Code components (direct, not symlinked)
│   ├── skills/
│   │   ├── story-tree/
│   │   ├── story-execution/
│   │   └── streamline/
│   ├── commands/
│   │   ├── ci-create-plan.md
│   │   ├── ci-implement-plan.md
│   │   └── design-story.md
│   ├── scripts/
│   │   └── *.py
│   └── data/
│       └── schema.sql          # Database schema (synced)
├── .github/
│   └── workflows/
│       └── *.yml
├── gui/                        # Xstory GUI application
│   ├── xstory.py
│   ├── requirements.txt
│   └── ...
├── sync-myskillium.sh          # Bash sync script
├── sync-myskillium.py          # Python sync script
├── .myskillium-version         # Version tracking
├── CLAUDE.md                   # Claude Code instructions
└── README.md
```

## Key Differences from StoryTree

| StoryTree | Myskillium |
|-----------|------------|
| `distributables/claude/` → symlink → `.claude/` | `.claude/` directly |
| `distributables/github/` → copy → `.github/` | `.github/` directly |
| Submodule in dependent repos | Template or sync script |
| Complex component-ownership-manifest | Simple: everything in repo is shared |

## Sync Model

```
Myskillium (source)              Dependent (target)
      │                                │
      │   sync-myskillium.py           │
      └──────────────────────────────► │
          copies .claude/*             │
          copies .github/workflows/*   │
          preserves *.db files         │
          updates .myskillium-version  │
```

## Project-Specific Files (Never Synced)

These paths are preserved during sync:
- `.claude/data/*.db` - Database files
- `.claude/local/*` - Repo-specific skill data
- `.claude/settings.local.json` - Local settings

## Template vs Sync

Two ways to use Myskillium:

1. **Template** (new projects): Click "Use this template" on GitHub
2. **Sync** (existing projects): Run `python sync-myskillium.py`

Both result in the same file structure.
""",

    "03-bootstrap-plan.md": """\
# Myskillium Bootstrap Plan

## Overview

Steps to create the Myskillium repository from scratch.

## Phase 1: Create Repository

1. Create new GitHub repo: `Mharbulous/Myskillium`
2. Initialize with README.md
3. Clone locally

## Phase 2: Create Directory Structure

```bash
mkdir -p .claude/skills
mkdir -p .claude/commands
mkdir -p .claude/scripts
mkdir -p .claude/data
mkdir -p .github/workflows
mkdir -p gui
```

## Phase 3: Create Core Files

1. **CLAUDE.md** - Instructions for Claude Code
   - Overview of Myskillium
   - How to use skills/commands
   - How to sync updates

2. **README.md** - User-facing documentation
   - What is Myskillium
   - Quick start (template vs sync)
   - List of included skills/commands

3. **.myskillium-version** - Version tracking
   - Initial: `v0.1.0` or commit SHA

4. **.gitignore** - Ignore patterns
   - `*.db` (database files)
   - `__pycache__/`
   - `.claude/local/`

## Phase 4: Create Sync Scripts

1. **sync-myskillium.sh** (Bash)
2. **sync-myskillium.py** (Python)

See `04-sync-script-spec.md` for requirements.

## Phase 5: Migrate Content

Run the scrape plan (`05-scrape-plan.md`) to extract content from StoryTree.

## Phase 6: Enable Template

1. GitHub Settings > General
2. Check "Template repository"
3. Test with "Use this template" button

## Phase 7: Validate

Run the testing plan (`07-testing-plan.md`).

## Deliverables

- [ ] Empty repo with directory structure
- [ ] CLAUDE.md
- [ ] README.md
- [ ] Sync scripts (sh + py)
- [ ] .gitignore
- [ ] Template enabled
""",

    "04-sync-script-spec.md": """\
# Sync Script Specification

## Overview

Two sync scripts that fetch latest Myskillium and update local project:
- `sync-myskillium.sh` - Bash (Linux/Mac)
- `sync-myskillium.py` - Python (Windows/cross-platform)

## Requirements

### Functional

1. **Fetch source**: Clone Myskillium repo (shallow, to temp directory)
2. **Copy components**:
   - `.claude/skills/*` → local `.claude/skills/`
   - `.claude/commands/*` → local `.claude/commands/`
   - `.claude/scripts/*` → local `.claude/scripts/`
   - `.claude/data/schema.sql` → local `.claude/data/schema.sql`
   - `.github/workflows/*` → local `.github/workflows/`
3. **Preserve project-specific files**:
   - `.claude/data/*.db` (never overwrite)
   - `.claude/local/*` (never touch)
   - `.claude/settings.local.json` (never overwrite)
4. **Update version**: Write commit SHA to `.myskillium-version`
5. **Report changes**: List what was added/updated/unchanged
6. **Remind user**: Print "Run: git add . && git commit -m 'sync myskillium'"

### Non-Functional

1. **No dependencies** (Bash script) - just git, cp, rm
2. **Minimal dependencies** (Python) - standard library only
3. **Cross-platform** (Python) - Windows path handling
4. **Idempotent** - safe to run multiple times
5. **Fast** - shallow clone, no full history

## Configuration

```python
MYSKILLIUM_REPO = "https://github.com/Mharbulous/Myskillium.git"
MYSKILLIUM_BRANCH = "main"
```

## Algorithm (Pseudocode)

```python
def sync():
    temp_dir = create_temp_directory()

    # Fetch
    git_clone(MYSKILLIUM_REPO, temp_dir, depth=1, branch=MYSKILLIUM_BRANCH)

    # Get version
    new_version = git_rev_parse(temp_dir, "HEAD")
    old_version = read_file(".myskillium-version") or "none"

    # Copy (with exclusions)
    copy_tree(f"{temp_dir}/.claude/skills", ".claude/skills")
    copy_tree(f"{temp_dir}/.claude/commands", ".claude/commands")
    copy_tree(f"{temp_dir}/.claude/scripts", ".claude/scripts")
    copy_file(f"{temp_dir}/.claude/data/schema.sql", ".claude/data/schema.sql")
    copy_tree(f"{temp_dir}/.github/workflows", ".github/workflows")

    # DO NOT copy:
    # - .claude/data/*.db
    # - .claude/local/
    # - gui/ (optional - user decides)

    # Update version
    write_file(".myskillium-version", new_version)

    # Cleanup
    remove_directory(temp_dir)

    # Report
    print(f"Updated from {old_version[:7]} to {new_version[:7]}")
    print("Run: git add . && git commit -m 'chore: sync myskillium'")
```

## Error Handling

1. **No git**: Exit with helpful message
2. **Network error**: Exit with retry suggestion
3. **No .claude/ directory**: Create it
4. **Permission error**: Exit with explanation

## CLI Options (Future)

```bash
sync-myskillium.py [--dry-run] [--include-gui] [--version]
```
""",

    "05-scrape-plan.md": """\
# Scrape Plan: Extract Components from StoryTree

## Overview

Extract valuable components from StoryTree into Myskillium's new structure.

## Source Locations (StoryTree)

```
StoryTree/
├── distributables/
│   ├── claude/
│   │   ├── skills/          → .claude/skills/
│   │   ├── commands/        → .claude/commands/
│   │   ├── scripts/         → .claude/scripts/
│   │   └── data/
│   │       └── schema.sql   → .claude/data/schema.sql
│   └── github/
│       └── workflows/       → .github/workflows/
└── gui/                     → gui/
```

## Component Inventory

### Skills to Migrate

| Skill | Purpose | Migrate? |
|-------|---------|----------|
| story-tree | Story management database operations | Yes |
| story-execution | Story workflow execution | Yes |
| streamline | Code streamlining utilities | Yes |
| [others] | Review and decide | TBD |

### Commands to Migrate

| Command | Purpose | Migrate? |
|---------|---------|----------|
| ci-create-plan.md | CI planning | Yes |
| ci-implement-plan.md | CI implementation | Yes |
| design-story.md | Story design | Yes |
| [others] | Review and decide | TBD |

### Scripts to Migrate

Review `.claude/scripts/` and `distributables/claude/scripts/`:
- Identify which are generic (migrate)
- Identify which are StoryTree-specific (leave)

### Workflows to Migrate

Review `.github/workflows/` and `distributables/github/workflows/`:
- Orchestrator workflow
- CI workflows
- [others]

### GUI to Migrate

The entire `gui/` directory (Xstory):
- xstory.py
- requirements.txt
- Supporting files
- Tests

## What NOT to Migrate

1. **Submodule infrastructure**
   - `src/setup.py` (symlink/submodule logic)
   - `component-ownership-manifest.json`
   - Dependent registration system

2. **StoryTree-specific docs**
   - `ai_docs/` (handovers, etc.)
   - Architecture decision records about submodules

3. **Database files**
   - `*.db` files (project-specific)
   - `templates/story-tree.db.empty` (recreate from schema)

4. **Symlinks**
   - Any symlinked directories
   - Copy the actual content instead

## Migration Steps

1. **Inventory**: List all files in each source location
2. **Categorize**: Generic vs StoryTree-specific
3. **Copy**: Move generic files to Myskillium structure
4. **Verify**: Ensure no broken references
5. **Test**: Run skills/commands in Myskillium

## Post-Migration Cleanup

In Myskillium:
1. Update any hardcoded "StoryTree" references
2. Simplify SKILL.md files (remove submodule context)
3. Update schema.sql comments if needed

## Deliverables

- [ ] Complete inventory of StoryTree components
- [ ] Migration decisions for each component
- [ ] Migrated files in Myskillium structure
- [ ] Updated references (no "StoryTree" mentions)
""",

    "06-migration-checklist.md": """\
# Migration Checklist

## Pre-Migration

- [ ] Myskillium repo created on GitHub
- [ ] Directory structure established
- [ ] Sync scripts written and tested
- [ ] StoryTree accessible for reference

## Skills Migration

- [ ] `story-tree/` skill copied
- [ ] `story-execution/` skill copied
- [ ] `streamline/` skill copied
- [ ] Other skills reviewed and copied as needed
- [ ] SKILL.md files updated (remove submodule references)
- [ ] No broken file references

## Commands Migration

- [ ] `ci-create-plan.md` copied
- [ ] `ci-implement-plan.md` copied
- [ ] `design-story.md` copied
- [ ] Other commands reviewed and copied as needed
- [ ] No broken references to StoryTree paths

## Scripts Migration

- [ ] Generic scripts identified and copied
- [ ] StoryTree-specific scripts left behind
- [ ] Scripts work without submodule context

## Workflows Migration

- [ ] Orchestrator workflow copied
- [ ] CI workflows copied
- [ ] Workflow triggers updated if needed
- [ ] No references to `.StoryTree/` paths

## Schema Migration

- [ ] `schema.sql` copied to `.claude/data/`
- [ ] Schema creates valid database
- [ ] No StoryTree-specific comments needing update

## GUI Migration

- [ ] `gui/` directory copied
- [ ] `requirements.txt` present
- [ ] `xstory.py` runs standalone
- [ ] Tests pass

## Documentation

- [ ] `CLAUDE.md` written
- [ ] `README.md` written
- [ ] No "StoryTree" references (except historical context)

## Configuration

- [ ] `.gitignore` configured
- [ ] `.myskillium-version` initialized
- [ ] Template repository enabled on GitHub

## Validation

- [ ] Create test project from template
- [ ] All skills load in Claude Code
- [ ] All commands accessible
- [ ] Workflows run (or are valid YAML)
- [ ] Sync script works on existing project
- [ ] Works on Windows (if possible to test)

## Post-Migration

- [ ] StoryTree README updated to point to Myskillium
- [ ] StoryTree archived (when confident)
- [ ] Dependent projects migrated to Myskillium
""",

    "07-testing-plan.md": """\
# Testing Plan

## Overview

Validate that Myskillium works correctly as a template and via sync.

## Test Environments

1. **Local CLI** - VS Code with Claude Code extension
2. **Claude Code Web** - claude.ai/code (if accessible)
3. **Windows** - Verify no symlink dependencies
4. **Linux/Mac** - Verify bash script works

## Test Cases

### T1: Template Creation

**Steps:**
1. Go to Myskillium on GitHub
2. Click "Use this template"
3. Create new repo
4. Clone locally

**Expected:**
- All `.claude/` files present
- All `.github/workflows/` files present
- No symlinks in the repo
- `.myskillium-version` present

### T2: Skills Load

**Steps:**
1. Open project in VS Code with Claude Code
2. Start a conversation
3. Reference a skill (e.g., ask about story management)

**Expected:**
- Skills are discovered
- SKILL.md content is accessible
- No errors about missing files

### T3: Commands Available

**Steps:**
1. Type `/` in Claude Code
2. Look for custom commands

**Expected:**
- `ci-create-plan` appears
- `design-story` appears
- Commands execute without error

### T4: Sync Script (Bash)

**Steps:**
1. Create a project (not from template)
2. Run `./sync-myskillium.sh`

**Expected:**
- Script clones Myskillium
- Files copied to `.claude/` and `.github/`
- `.myskillium-version` created
- No errors

### T5: Sync Script (Python)

**Steps:**
1. Create a project (not from template)
2. Run `python sync-myskillium.py`

**Expected:**
- Same as T4
- Works on Windows

### T6: Sync Preserves Project Files

**Steps:**
1. Create project from template
2. Create `.claude/data/test.db`
3. Create `.claude/local/mydata.json`
4. Run sync script

**Expected:**
- `test.db` still exists
- `mydata.json` still exists
- Other files updated

### T7: Sync Updates Version

**Steps:**
1. Note current `.myskillium-version`
2. Make a commit in Myskillium
3. Run sync in dependent

**Expected:**
- `.myskillium-version` has new SHA

### T8: GUI Runs Standalone

**Steps:**
1. `cd gui/`
2. `pip install -r requirements.txt`
3. `python xstory.py --help` (or similar)

**Expected:**
- No import errors
- Help text displays (or GUI launches)

### T9: Web Compatibility

**Steps:**
1. Push project to GitHub
2. Open in Claude Code web
3. Reference skills/commands

**Expected:**
- Skills work (files are committed, not symlinked)
- Commands work

### T10: Windows Compatibility

**Steps:**
1. Clone Myskillium on Windows
2. Run `python sync-myskillium.py`
3. Verify no symlink errors

**Expected:**
- No errors about symlinks or Developer Mode
- Files copied correctly

## Regression Tests

After any change to Myskillium:
- [ ] T1: Template creation still works
- [ ] T4/T5: Sync scripts still work
- [ ] T6: Project files still preserved

## Known Limitations to Document

- Sync is manual (not automatic)
- GUI requires Python + PySide6
- Large files may slow clone
""",
}


# Embedded hash - computed lazily on first use (not at import time)
# This keeps the fast path lightweight while still providing hardening
_EMBEDDED_HASH = None


def _extract_hash_from_yml(content: str) -> str | None:
    """Extract hash value from version.yml content. Returns None if not found."""
    for line in content.splitlines():
        line = line.strip()
        if line.startswith("hash:"):
            return line.split(":", 1)[1].strip().strip('"\'')
    return None


def calculate_embedded_hash() -> str:
    """
    Return the embedded hash (computed lazily on first call, then cached).

    This is the combined SHA-256 hash of all embedded docs, used to detect
    when local files differ from what's embedded in this hook.
    """
    global _EMBEDDED_HASH
    if _EMBEDDED_HASH is not None:
        return _EMBEDDED_HASH

    _hashlib = _import_hashlib()

    def _hash(s: str) -> str:
        return _hashlib.sha256(s.encode("utf-8")).hexdigest()

    combined = "".join(
        f"{name}:{_hash(content)}"
        for name, content in sorted(EMBEDDED_DOCS.items())
    )
    _EMBEDDED_HASH = _hash(combined)
    return _EMBEDDED_HASH


def get_project_root() -> Path:
    """Get the project root directory from environment or fallback to cwd."""
    project_dir = os.environ.get("CLAUDE_PROJECT_DIR")
    if project_dir:
        return Path(project_dir)
    return Path.cwd()


def get_skill_dir(project_root: Path) -> Path:
    """Get the bootstrap skill directory path."""
    return project_root / BOOTSTRAP_SKILL_DIR


def write_embedded_docs(skill_dir: Path) -> None:
    """Write all embedded docs to the skill directory."""
    skill_dir.mkdir(parents=True, exist_ok=True)
    for filename, content in EMBEDDED_DOCS.items():
        (skill_dir / filename).write_text(content, encoding="utf-8")


def calculate_hash(content: str) -> str:
    """Calculate SHA-256 hash of content."""
    _hashlib = _import_hashlib()
    return _hashlib.sha256(content.encode("utf-8")).hexdigest()


def calculate_local_hash(skill_dir: Path) -> str:
    """Calculate combined hash of all local docs."""
    combined_parts = []
    for name in sorted(EMBEDDED_DOCS.keys()):
        filepath = skill_dir / name
        if filepath.exists():
            content = filepath.read_text(encoding="utf-8")
            combined_parts.append(f"{name}:{calculate_hash(content)}")
        else:
            # File missing - use empty hash
            combined_parts.append(f"{name}:{calculate_hash('')}")
    return calculate_hash("".join(combined_parts))


def is_source_template(project_root: Path) -> bool:
    """
    Check if this is the Myskillium source template by examining git remotes.

    Returns True if any remote URL contains the source template identifier.
    This prevents the source template from trying to update from itself.
    """
    _subprocess = _import_subprocess()
    source_pattern = f"{_SOURCE_OWNER}/{_SOURCE_REPO}"
    try:
        result = _subprocess.run(
            ["git", "remote", "-v"],
            cwd=project_root,
            capture_output=True,
            text=True,
            timeout=2.0,  # Fast timeout for responsiveness
        )
        if result.returncode == 0:
            return source_pattern in result.stdout
    except (_subprocess.TimeoutExpired, FileNotFoundError, OSError):
        pass
    return False


def read_version_yml(project_root: Path) -> dict:
    """
    Read version.yml file and return parsed data.

    Returns dict with:
    - 'last_check': datetime, "germinating", or None
    - 'hash': str or None
    - 'version': float or None
    """
    version_path = project_root / VERSION_FILE
    result = {"last_check": None, "hash": None, "version": None}

    if not version_path.exists():
        return result

    try:
        content = version_path.read_text(encoding="utf-8")
        # Extract hash using shared helper
        result["hash"] = _extract_hash_from_yml(content)
        # Parse each line
        for line in content.splitlines():
            line = line.strip()
            if line.startswith("last_check:"):
                ts_str = line.split(":", 1)[1].strip().strip('"\'')
                # Check for special "germinating" status
                if ts_str == "germinating":
                    result["last_check"] = "germinating"
                else:
                    try:
                        dt = datetime.fromisoformat(ts_str.replace("Z", "+00:00"))
                        if dt.tzinfo is None:
                            dt = dt.replace(tzinfo=timezone.utc)
                        result["last_check"] = dt
                    except ValueError:
                        pass
            elif line.startswith("version:"):
                try:
                    result["version"] = float(line.split(":", 1)[1].strip())
                except ValueError:
                    pass
    except (OSError, IOError):
        pass

    return result


def write_version_yml(project_root: Path, embedded_hash: str) -> None:
    """Write version.yml with current timestamp and hash."""
    version_path = project_root / VERSION_FILE
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S")
    content = f"""# Myskillium Bootstrap Version Tracking
# Auto-generated - do not edit manually
last_check: "{timestamp}"
hash: "{embedded_hash}"
version: 0.1
"""
    try:
        version_path.parent.mkdir(parents=True, exist_ok=True)
        version_path.write_text(content, encoding="utf-8")
    except (OSError, IOError):
        pass  # Non-fatal - will just recheck next time


def write_germinating_version_yml(project_root: Path, embedded_hash: str) -> None:
    """
    Write version.yml with germinating status.

    This special status keeps the bootstrap hook triggering until the process
    reaches a step where it checks the root template repo's version.yml.
    """
    version_path = project_root / VERSION_FILE
    content = f"""# Myskillium Bootstrap Version Tracking
# Auto-generated - do not edit manually
last_check: "germinating"
hash: "{embedded_hash}"
version: 0.1
"""
    try:
        version_path.parent.mkdir(parents=True, exist_ok=True)
        version_path.write_text(content, encoding="utf-8")
    except (OSError, IOError):
        pass  # Non-fatal - will just recheck next time


def hours_since_last_check(project_root: Path) -> float:
    """
    Calculate hours since the last hash check from version.yml.

    Returns infinity if:
    - No version.yml exists
    - last_check is "germinating" (keeps triggering bootstrap)
    - last_check couldn't be parsed
    """
    version_data = read_version_yml(project_root)
    last_check = version_data.get("last_check")

    # If germinating or missing, always trigger full check
    if last_check is None or last_check == "germinating":
        return float("inf")

    now = datetime.now(timezone.utc)
    delta = now - last_check
    return delta.total_seconds() / 3600


def fetch_remote_hash(timeout: float = 5.0) -> str | None:
    """Fetch the remote hash from version.yml on GitHub. Returns None on any error."""
    _urllib_request, _urllib_error = _import_urllib()
    try:
        req = _urllib_request.Request(
            REMOTE_VERSION_URL,
            headers={"User-Agent": "Myskillium-Bootstrap/1.0"}
        )
        with _urllib_request.urlopen(req, timeout=timeout) as response:
            content = response.read().decode("utf-8")
            return _extract_hash_from_yml(content)
    except (_urllib_error.URLError, _urllib_error.HTTPError, TimeoutError, OSError):
        return None


def germinate(project_root: Path, skill_dir: Path) -> None:
    """
    Germination mode: Force-write all embedded docs with germinating status.

    This is used for initial setup. The "germinating" status in version.yml
    keeps the bootstrap hook triggering until the process advances to a step
    where it checks the root template repo's version.yml.
    """
    embedded_hash = calculate_embedded_hash()
    write_embedded_docs(skill_dir)
    write_germinating_version_yml(project_root, embedded_hash)

    print("## Bootstrap Skill Synced")
    print()
    print(f"Bootstrap docs written to `{BOOTSTRAP_SKILL_DIR}/`")
    print()
    print("This skill contains 7 planning documents for setting up Myskillium.")
    print("Read `03-bootstrap-plan.md` to begin the bootstrap process.")


def main():
    """
    Main entry point for the bootstrap check hook.

    Modes:
    - --germinate: Force write all docs with germinating status
    - (default): Run the optimized check workflow

    Optimized workflow (fastest checks first):
    1. 24h fast path → silent exit if recently checked (most common case)
    2. Source template check → silent exit if source (never syncs)
    3. Hash comparison → sync docs if mismatch
    4. Remote update check → notify if available

    The 24h check comes first because:
    - It's just a file read (~1ms) vs git subprocess (~2ms)
    - Dependents are the common case (many repos vs one source)
    - If version.yml exists with <24h, files must exist and it's not source
    """
    project_root = get_project_root()
    skill_dir = get_skill_dir(project_root)

    # ==== Handle --germinate flag ====
    if "--germinate" in sys.argv:
        germinate(project_root, skill_dir)
        sys.exit(0)

    # ==== STEP 1: 24-Hour Fast Path (most common case for dependents) ====
    # If version.yml exists and <24h elapsed, exit immediately.
    # This is the hot path - just a file read, no subprocess, no network.
    # If this passes, we know: files exist, not source template, recently checked.
    if hours_since_last_check(project_root) < 24:
        sys.exit(0)

    # ==== STEP 2: Source Template Detection ====
    # Only reached if >24h or no version.yml (first run / source template).
    # Source template never syncs or checks for updates.
    if is_source_template(project_root):
        sys.exit(0)

    # ==== STEP 3: Hash Comparison (sync if any difference) ====
    embedded_hash = calculate_embedded_hash()
    local_hash = calculate_local_hash(skill_dir)

    if local_hash != embedded_hash:
        write_embedded_docs(skill_dir)
        write_version_yml(project_root, embedded_hash)

        print("## Bootstrap Skill Synced")
        print()
        print(f"Bootstrap docs written to `{BOOTSTRAP_SKILL_DIR}/`")
        print()
        print("This skill contains 7 planning documents for setting up Myskillium.")
        print("Read `03-bootstrap-plan.md` to begin the bootstrap process.")
        sys.exit(0)

    # ==== STEP 4: Remote Update Check (once/day) ====
    remote_hash = fetch_remote_hash()

    if remote_hash is None:
        # Network error - update timestamp anyway to avoid retry storm
        write_version_yml(project_root, embedded_hash)
        sys.exit(0)

    if remote_hash != embedded_hash:
        # Update available - don't update timestamp so we remind again
        print("## Myskillium Update Available")
        print()
        print("A new version of Myskillium is available upstream.")
        print()
        print("To update, run:")
        print("```")
        print("python sync-myskillium.py")
        print("```")
        print()
        print("This will fetch the latest skills, commands, and docs from Myskillium.")
        sys.exit(0)

    # ==== Everything up to date ====
    write_version_yml(project_root, embedded_hash)
    sys.exit(0)


if __name__ == "__main__":
    main()
