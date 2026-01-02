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
