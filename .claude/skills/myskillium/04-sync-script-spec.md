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

    # DO NOT copy:
    # - .claude/data/*.db
    # - .claude/local/

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
sync-myskillium.py [--dry-run] [--version]
```
