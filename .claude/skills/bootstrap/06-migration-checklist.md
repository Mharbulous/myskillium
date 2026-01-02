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
