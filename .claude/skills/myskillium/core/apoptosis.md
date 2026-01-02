# Apoptosis

## Definition

In the myskillium context, apoptosis refers to **the controlled, orderly removal of myskillium from a repository**. Just as biological apoptosis is programmed cell death that cleanly removes cells without damaging surrounding tissue, skill apoptosis cleanly removes myskillium without corrupting the host repository.

Key parallels:
- Programmed = deliberate user decision, not accidental deletion
- Orderly = follows specific sequence to avoid orphaned artifacts
- Clean removal = no residual hooks, settings, or broken references
- Non-destructive = host repository continues functioning normally

## Purpose

Provide a safe, complete method to remove myskillium from a repository:

1. **Disable monitoring** - Remove the SessionStart hook first to prevent resurrection
2. **Remove artifacts** - Delete all myskillium files and directories
3. **Preserve integrity** - Leave no orphaned references in settings
4. **Document removal** - Optional: record removal in git history

## Process

### Prerequisites

- Repository has myskillium installed (`.claude/skills/myskillium/` exists)
- User has write access to `.claude/` directory
- User understands removal is permanent (no homeostasis to restore)

### Phase 1: Disable Hook

**Critical**: The hook must be removed FIRST. If the directory is deleted while the hook remains, Claude Code sessions will fail with missing script errors.

Edit `.claude/settings.json` and remove the myskillium SessionStart hook entry:

```json
{
  "hooks": {
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "python .claude/skills/myskillium/scripts/conidium.py"
          }
        ]
      }
    ]
  }
}
```

If this is the only SessionStart hook, the entire `SessionStart` array can be removed.

### Phase 2: Remove Script

Delete the conidium script:

```bash
rm .claude/skills/myskillium/scripts/conidium.py
```

Or on Windows:

```powershell
Remove-Item .claude\skills\myskillium\scripts\conidium.py
```

This prevents any possibility of accidental re-execution.

### Phase 3: Remove Directory

Delete the entire myskillium skill directory:

```bash
rm -rf .claude/skills/myskillium/
```

Or on Windows:

```powershell
Remove-Item -Recurse -Force .claude\skills\myskillium\
```

This removes:
- `SKILL.md` - The skill definition
- `README.md` - Documentation
- `version.yml` - Version tracking
- `processes/` - All process documentation
- `scripts/` - The scripts directory (now empty)

### Phase 4: Commit (Optional)

If tracking the removal in git history:

```bash
git add .claude/
git commit -m "chore: remove myskillium skill"
```

## Apoptosis vs Necrosis

| Aspect | Apoptosis (Controlled) | Necrosis (Uncontrolled) |
|--------|------------------------|------------------------|
| **Hook removal** | First step | Forgotten |
| **Sequence** | Hook → Script → Directory | Random deletion |
| **Result** | Clean removal | Orphaned hooks, errors |
| **Recovery** | Re-germinate if needed | Debug broken settings |

**Warning**: Simply deleting `.claude/skills/myskillium/` without removing the hook causes "necrosis" - the SessionStart hook will attempt to run a non-existent script, producing errors on every Claude Code session.

## Resurrection

Apoptosis is reversible. To restore myskillium after removal:

1. Obtain a fresh `conidium.py` from upstream or another repository
2. Place it anywhere in your repository
3. Run `python conidium.py --germinate`

The germination process will recreate the full skill structure and reinstall the hook.

## Relationship to Other Processes

| Process | Apoptosis Relationship |
|---------|----------------------|
| **Conidiation** | Apoptosis undoes germination |
| **Homeostasis** | Must be disabled (hook removal) before apoptosis succeeds |
| **Fragmentation** | Can extract skills before apoptosis if preservation needed |
| **Plasmogamy** | Can fuse skills before apoptosis if combining with another |

Apoptosis is the **inverse of germination**. Where germination creates and installs, apoptosis removes and uninstalls. The hook removal step is critical because homeostasis would otherwise attempt to restore removed files.

## Quick Reference

```bash
# Complete apoptosis sequence (Unix/Mac)
# 1. Edit .claude/settings.json - remove the SessionStart hook entry
# 2. Then run:
rm .claude/skills/myskillium/scripts/conidium.py
rm -rf .claude/skills/myskillium/
git add .claude/ && git commit -m "chore: remove myskillium"
```

```powershell
# Complete apoptosis sequence (Windows PowerShell)
# 1. Edit .claude/settings.json - remove the SessionStart hook entry
# 2. Then run:
Remove-Item .claude\skills\myskillium\scripts\conidium.py
Remove-Item -Recurse -Force .claude\skills\myskillium\
git add .claude/ ; git commit -m "chore: remove myskillium"
```

## Checklist

- [ ] User confirms intent to remove myskillium
- [ ] SessionStart hook entry removed from `.claude/settings.json`
- [ ] `conidium.py` script deleted
- [ ] `.claude/skills/myskillium/` directory deleted
- [ ] No orphaned references in settings.json
- [ ] Changes committed to git (optional)
- [ ] User informed how to re-germinate if needed
