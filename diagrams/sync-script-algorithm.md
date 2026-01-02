# Sync Script Algorithm

```mermaid
flowchart TD
    START([Start Sync]) --> CHECK_GIT{Git available?}

    CHECK_GIT -->|No| ERROR_GIT[Exit: Install git]
    CHECK_GIT -->|Yes| CREATE_TEMP[Create temp directory]

    CREATE_TEMP --> GIT_CLONE[git clone shallow, depth=1<br/>from Myskillium repo]

    GIT_CLONE --> CHECK_NETWORK{Network OK?}
    CHECK_NETWORK -->|No| ERROR_NETWORK[Exit: Retry later]
    CHECK_NETWORK -->|Yes| GET_VERSION[Get new version HEAD SHA<br/>Read old version .myskillium-version]

    GET_VERSION --> COPY_SKILLS[Copy .claude/skills/*]
    COPY_SKILLS --> COPY_COMMANDS[Copy .claude/commands/*]
    COPY_COMMANDS --> COPY_SCRIPTS[Copy .claude/scripts/*]
    COPY_SCRIPTS --> COPY_SCHEMA[Copy .claude/data/schema.sql]
    COPY_SCHEMA --> COPY_WORKFLOWS[Copy .github/workflows/*]

    COPY_WORKFLOWS -.-> SKIP_NOTE[SKIP: *.db, .claude/local/,<br/>settings.local.json]
    COPY_WORKFLOWS --> UPDATE_VERSION[Write new SHA to<br/>.myskillium-version]

    UPDATE_VERSION --> CLEANUP[Remove temp directory]
    CLEANUP --> REPORT[Print: Updated from X to Y<br/>Print: Run git add/commit]
    REPORT --> END([Done])

    style ERROR_GIT fill:#FF6B6B
    style ERROR_NETWORK fill:#FF6B6B
    style SKIP_NOTE fill:#FFD700
    style REPORT fill:#90EE90
    style END fill:#90EE90
```

## Error Handling Notes

| Error Condition | Exit Point | User Action Required |
|-----------------|------------|---------------------|
| Git not installed | ERROR_GIT | Install git and retry |
| Network failure (clone) | ERROR_NETWORK | Check connection and retry later |
| Temp directory creation fails | CREATE_TEMP | Check disk space and permissions |

## File Preservation

The sync script **preserves** local files that should not be overwritten:

- **Database files**: `*.db` (local skill data)
- **Local directory**: `.claude/local/` (user-specific configs)
- **Local settings**: `settings.local.json` (user overrides)

These files are intentionally skipped during the copy process to prevent data loss.

## Script Variants

- **Python**: `sync-myskillium.py` - Cross-platform, requires Python 3.6+
- **Shell**: `sync-myskillium.sh` - Unix/Linux/macOS native, requires bash

Both scripts implement the same algorithm and produce identical results.

## Source Repository

- **URL**: https://github.com/Mharbulous/Myskillium.git
- **Branch**: main
- **Clone method**: Shallow clone (depth=1) for minimal bandwidth
