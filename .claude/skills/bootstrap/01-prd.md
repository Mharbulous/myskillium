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
