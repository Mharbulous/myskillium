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
- [ ] Sync script works on existing project
- [ ] Works on Windows (if possible to test)

## Post-Migration

- [ ] StoryTree README updated to point to Myskillium
- [ ] StoryTree archived (when confident)
- [ ] Dependent projects migrated to Myskillium
