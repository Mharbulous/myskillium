# Scrape Plan: Extract Skills from StoryTree

## Overview

Extract valuable skills from StoryTree into Myskillium's new structure.

## Source Locations (StoryTree)

```
StoryTree/
└── distributables/
    └── claude/
        └── skills/          → .claude/skills/
```

## Skills Inventory

### Skills to Migrate

| Skill | Purpose | Migrate? |
|-------|---------|----------|
| story-tree | Story management database operations | Yes |
| story-execution | Story workflow execution | Yes |
| streamline | Code streamlining utilities | Yes |
| [others] | Review and decide | TBD |

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

1. **Inventory**: List all skills in source location
2. **Categorize**: Generic vs StoryTree-specific
3. **Copy**: Move generic skills to Myskillium structure
4. **Verify**: Ensure no broken references
5. **Test**: Run skills in Myskillium

## Post-Migration Cleanup

In Myskillium:
1. Update any hardcoded "StoryTree" references
2. Simplify SKILL.md files (remove submodule context)

## Deliverables

- [ ] Complete inventory of StoryTree skills
- [ ] Migration decisions for each skill
- [ ] Migrated skills in Myskillium structure
- [ ] Updated references (no "StoryTree" mentions)
