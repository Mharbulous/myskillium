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
- All `.claude/skills/` files present
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

### T3: Sync Script (Bash)

**Steps:**
1. Create a project (not from template)
2. Run `./sync-myskillium.sh`

**Expected:**
- Script clones Myskillium
- Skills copied to `.claude/skills/`
- `.myskillium-version` created
- No errors

### T4: Sync Script (Python)

**Steps:**
1. Create a project (not from template)
2. Run `python sync-myskillium.py`

**Expected:**
- Same as T3
- Works on Windows

### T5: Sync Preserves Project Files

**Steps:**
1. Create project from template
2. Create `.claude/data/test.db`
3. Create `.claude/local/mydata.json`
4. Run sync script

**Expected:**
- `test.db` still exists
- `mydata.json` still exists
- Skills updated

### T6: Sync Updates Version

**Steps:**
1. Note current `.myskillium-version`
2. Make a commit in Myskillium
3. Run sync in dependent

**Expected:**
- `.myskillium-version` has new SHA

### T7: Web Compatibility

**Steps:**
1. Push project to GitHub
2. Open in Claude Code web
3. Reference skills

**Expected:**
- Skills work (files are committed, not symlinked)

### T8: Windows Compatibility

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
- [ ] T3/T4: Sync scripts still work
- [ ] T5: Project files still preserved

## Known Limitations to Document

- Sync is manual (not automatic)
