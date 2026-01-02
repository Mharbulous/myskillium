# Myskillium Architecture

## Core Principle

**What you see is what you get.** No indirection layers, no symlinks, no submodules.

## Directory Structure

```
Myskillium/
├── .claude/                    # Claude Code components (direct, not symlinked)
│   ├── skills/
│   │   ├── story-tree/
│   │   ├── story-execution/
│   │   └── streamline/
│   ├── commands/
│   │   ├── ci-create-plan.md
│   │   ├── ci-implement-plan.md
│   │   └── design-story.md
│   ├── scripts/
│   │   └── *.py
│   └── data/
│       └── schema.sql          # Database schema (synced)
├── .github/
│   └── workflows/
│       └── *.yml
├── gui/                        # Xstory GUI application
│   ├── xstory.py
│   ├── requirements.txt
│   └── ...
├── sync-myskillium.sh          # Bash sync script
├── sync-myskillium.py          # Python sync script
├── .myskillium-version         # Version tracking
├── CLAUDE.md                   # Claude Code instructions
└── README.md
```

## Key Differences from StoryTree

| StoryTree | Myskillium |
|-----------|------------|
| `distributables/claude/` → symlink → `.claude/` | `.claude/` directly |
| `distributables/github/` → copy → `.github/` | `.github/` directly |
| Submodule in dependent repos | Template or sync script |
| Complex component-ownership-manifest | Simple: everything in repo is shared |

## Sync Model

```
Myskillium (source)              Dependent (target)
      │                                │
      │   sync-myskillium.py           │
      └──────────────────────────────► │
          copies .claude/*             │
          copies .github/workflows/*   │
          preserves *.db files         │
          updates .myskillium-version  │
```

## Project-Specific Files (Never Synced)

These paths are preserved during sync:
- `.claude/data/*.db` - Database files
- `.claude/local/*` - Repo-specific skill data
- `.claude/settings.local.json` - Local settings

## Template vs Sync

Two ways to use Myskillium:

1. **Template** (new projects): Click "Use this template" on GitHub
2. **Sync** (existing projects): Run `python sync-myskillium.py`

Both result in the same file structure.
