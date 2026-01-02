# Content Migration Workflow

```mermaid
flowchart TD
    START([Start Migration]) --> INVENTORY[1. INVENTORY<br/>List all files in each<br/>source location]
    INVENTORY --> CATEGORIZE[2. CATEGORIZE<br/>Generic vs StoryTree-specific]
    CATEGORIZE --> DECISION{Is component<br/>generic?}

    DECISION -->|No| LEAVE[Leave in StoryTree]
    DECISION -->|Yes| COPY[3. COPY<br/>Move to Myskillium structure]

    LEAVE -.Next item.-> CATEGORIZE

    COPY --> VERIFY[4. VERIFY<br/>Check for broken references]
    VERIFY --> TEST[5. TEST<br/>Run skills/commands<br/>in Myskillium]
    TEST --> CLEANUP[Post-Migration Cleanup<br/>- Update hardcoded refs<br/>- Simplify SKILL.md files<br/>- Update schema comments]
    CLEANUP --> END([Migration Complete])

    style LEAVE fill:#E0E0E0
    style COPY fill:#90EE90
    style CLEANUP fill:#87CEEB
    style END fill:#90EE90
```

## Source Mappings

| From | To |
|------|-----|
| `StoryTree/distributables/claude/skills/` | `.claude/skills/` |
| `StoryTree/distributables/claude/commands/` | `.claude/commands/` |
| `StoryTree/distributables/claude/scripts/` | `.claude/scripts/` |
| `StoryTree/distributables/claude/data/schema.sql` | `.claude/data/schema.sql` |
| `StoryTree/distributables/github/workflows/` | `.github/workflows/` |
| `StoryTree/gui/` | `gui/` |

## Do Not Migrate

- Submodule infrastructure (setup.py, manifests)
- StoryTree-specific docs (ai_docs/)
- Database files (*.db)
- Symlinks (copy actual content)
