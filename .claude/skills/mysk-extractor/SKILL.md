---
name: skill-extractor
description: Use when migrating skills between repositories or extracting skills from a project into a reusable form. Handles copying, cleanup of project-specific references, and genealogy documentation.
---

# Skill Extractor

Migrate skills from one repository to another while cleaning up project-specific references and documenting provenance.

## Quick Start

1. Define migration in config (see `genealogy/templates/migration-config.json`)
2. Run phases: Copy → Cleanup → Genealogy → Commit

## Workflow

### Phase 1: Configure

Create or update migration config with:
- Source/destination paths
- Skills to migrate
- Cleanup replacements (project-specific → generic)

See `genealogy/templates/migration-config.json` for structure.

### Phase 2: Copy

```bash
# For each skill in config
cp -r "<source>/<skill>/" "<destination>/<skill>/"
```

### Phase 3: Cleanup

**Scan** for project-specific references:
```bash
grep -r -i "pattern1\|pattern2\|pattern3" "<destination>/" || echo "Clean"
```

**Replace** according to config:

| Type | Example Find | Example Replace |
|------|--------------|-----------------|
| Project name | `SyncoPaid` | `myapp` |
| Domain term | `story` → `task` | (whole word only) |
| Package name | `syncopaid.module` | `myapp.module` |
| Specific path | `tests/test_project.py` | "your test file" |
| Historical ref | "In the ProjectX case" | "In one case" |

**Verify** - remaining matches should be false positives only:
- "history" matching "story" pattern ✓
- "submodule" as programming term ✓

### Phase 4: Genealogy

Create `<genealogy-path>/<skill-name>.json`:

```json
{
  "name": "<from-frontmatter>",
  "description": "<from-frontmatter>",
  "sourceURL": "<https://github.com/org/repo.git>",
  "date": "<YYYY-MM-DD>"
}
```

### Phase 5: Commit

```
feat: migrate N skills from <source-repo>

Skills: skill-1, skill-2, ...
Project-specific references cleaned up.
```

## Templates

| File | Purpose |
|------|---------|
| `genealogy/templates/migration-config.json` | Example config with replacements |
| `genealogy/templates/pedigree.json` | Genealogy file structure |

## Checklist

- [ ] Skills copied to destination
- [ ] Project names generalized
- [ ] Domain terms universalized
- [ ] Example paths made generic
- [ ] Genealogy file created per skill
- [ ] Final scan shows only false positives
