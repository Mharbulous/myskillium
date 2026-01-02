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
