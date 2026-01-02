# Myskillium Sync Model

```mermaid
flowchart LR
    SOURCE([Myskillium<br/>Source Repo]) --> SYNC_SCRIPT[sync-myskillium.py<br/>or<br/>sync-myskillium.sh]
    SYNC_SCRIPT --> TARGET([Dependent Project<br/>Target Repo])

    subgraph COPIES[What Gets Copied]
        COPY1[.claude/skills/*]
        COPY2[.claude/commands/*]
        COPY3[.claude/scripts/*]
        COPY4[.github/workflows/*]
        COPY5[.claude/data/schema.sql]
    end

    subgraph PRESERVES[What Gets Preserved]
        PRES1[*.db files]
        PRES2[.claude/local/*]
        PRES3[settings.local.json]
    end

    SYNC_SCRIPT -.-> COPIES
    SYNC_SCRIPT -.-> PRESERVES

    style SOURCE fill:#87CEEB
    style TARGET fill:#90EE90
    style PRES1 fill:#FFD700
    style PRES2 fill:#FFD700
    style PRES3 fill:#FFD700
```

## Overview

Data flow from Myskillium source repository to dependent target repositories via sync scripts. The sync mechanism ensures that core Claude configuration and workflows stay up-to-date while preserving project-specific data.

## Usage Modes

- **Template**: For new projects - complete initial setup
- **Sync**: For existing projects - update shared resources while preserving local state

## Version Tracking

Version is tracked in `.myskillium-version` to detect when updates are needed and prevent unnecessary syncs.

## What Gets Copied

The sync scripts copy these shared resources from Myskillium:

- `.claude/skills/*` - Reusable Claude skills
- `.claude/commands/*` - Custom slash commands
- `.claude/scripts/*` - Helper scripts
- `.github/workflows/*` - GitHub Actions workflows
- `.claude/data/schema.sql` - Database schema

## What Gets Preserved

These project-specific files are never overwritten:

- `*.db files` - Local databases
- `.claude/local/*` - Project-specific configurations
- `settings.local.json` - Local settings
