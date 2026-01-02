# Bootstrap Hook Workflow

```mermaid
flowchart TD
    START([SessionStart Hook]) --> READ_VERSION[Read version.yml]
    READ_VERSION --> CHECK_24H{< 24h since<br/>last check?}

    CHECK_24H -->|Yes| EXIT_FAST([Silent Exit<br/>FAST PATH ~99%])
    CHECK_24H -->|No / Never| CHECK_SOURCE[Check git remote]

    CHECK_SOURCE --> IS_SOURCE{Remote contains<br/>Mharbulous/Myskillium?}
    IS_SOURCE -->|Yes| EXIT_SOURCE([Silent Exit<br/>Source Template])
    IS_SOURCE -->|No| CALC_HASH[Calculate hashes]

    CALC_HASH --> COMPARE{Local hash ==<br/>Embedded hash?}

    COMPARE -->|No| SYNC[Write docs + version.yml]
    SYNC --> MSG_SYNC[/"## Bootstrap Skill Synced"/]
    MSG_SYNC --> EXIT_SYNC([Exit])

    COMPARE -->|Yes| FETCH_REMOTE[Fetch remote version.yml<br/>from GitHub<br/>5s timeout]

    FETCH_REMOTE --> NETWORK{Network<br/>success?}
    NETWORK -->|No| WRITE_VERSION_NET[Write version.yml<br/>★ resets 24h timer]
    WRITE_VERSION_NET --> EXIT_NET([Silent Exit<br/>Retry in 24h])

    NETWORK -->|Yes| REMOTE_MATCH{Remote hash ==<br/>Embedded hash?}
    REMOTE_MATCH -->|No| MSG_UPDATE[/"## Update Available"/]
    MSG_UPDATE --> EXIT_UPDATE([Exit<br/>Timer NOT reset])

    REMOTE_MATCH -->|Yes| WRITE_VERSION[Write version.yml<br/>★ resets 24h timer]
    WRITE_VERSION --> EXIT_OK([Silent Exit<br/>Up to Date])

    style EXIT_FAST fill:#90EE90
    style EXIT_SOURCE fill:#E0E0E0
    style MSG_SYNC fill:#87CEEB
    style MSG_UPDATE fill:#FFA500
    style EXIT_OK fill:#90EE90
    style WRITE_VERSION_NET fill:#90EE90
    style WRITE_VERSION fill:#90EE90
    style EXIT_NET fill:#90EE90
```

## 24h Cooldown Behavior

| Outcome | Writes version.yml? | Next session behavior |
|---------|---------------------|----------------------|
| Fast path (<24h) | No | Fast exit again |
| Source template | No | Fast exit (no version.yml needed) |
| Sync | **Yes** | Fast exit for 24h |
| Network error | **Yes** | Fast exit for 24h |
| Update available | No | Check again (intentional reminder) |
| Up to date | **Yes** | Fast exit for 24h |

**Key insight**: Network failures write `version.yml`, so the hook won't retry until 24h later. This prevents exacerbating network outages.

## Performance Notes

- **Fast path** (~99%): Only loads `os`, `sys`, `datetime`, `pathlib` (~1ms file read)
- **Steps 2-4**: Lazy-load `subprocess`, `hashlib`, `urllib` only when needed
- **Max overhead**: One 5-second network attempt per 24h, regardless of success/failure

## Why version.yml Everywhere

Both local and remote use the same `version.yml` format:

```yaml
# .claude/skills/bootstrap/version.yml
last_check: "2025-01-15T12:00:00"
hash: "abc123..."
```

- **Same format** - simpler mental model, no separate `.hash` file
- **Human-readable** - can inspect deployed version at a glance
- **Trivial parsing** - just find the `hash:` line
