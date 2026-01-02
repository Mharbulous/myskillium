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
