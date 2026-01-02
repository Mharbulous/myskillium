# Fragmentation

## Skill Analogy

In the myskillium context, fragmentation refers to **extracting a skill from one repository to another**. The skill is a "fragment" of the source repo's functionality that becomes independent in its new home.

Key parallels:
- The skill (fragment) is viable on its own
- It adapts to the new environment (project-specific references cleaned up)
- It grows independently (maintained separately from source)
- Genetic identity is preserved (pedigree documents lineage)

## Purpose

Migrate a skill from a source repository to Myskillium while:
1. Cleaning up project-specific references
2. Documenting skill pedigree
3. Preserving the skill's core functionality

## Process

### Prerequisites

- Source repository accessible (local clone or remote URL)
- Destination path in Myskillium identified
- Cleanup patterns defined for project-specific references

### Phase 1: Configure

Create or update migration config specifying:
- Source repository URL and skill path
- Destination path
- Cleanup replacements (project names → generic terms)

See `genealogy/templates/migration-config.json` for structure.

### Phase 2: Copy

Transfer skill files from source to destination:

```bash
cp -r "<source-repo>/<skill-path>/" "<dest-repo>/<skill-path>/"
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

**Verify** - remaining matches should be false positives only.

### Phase 4: Genealogy

Create pedigree file at `genealogy/<skill-name>.json`:

```json
{
  "name": "<from-frontmatter>",
  "description": "<from-frontmatter>",
  "pedigree": [
    {
      "date": "YYYY-MM-DD",
      "sourceURL": "https://github.com/org/source-repo.git",
      "sourcePath": ".claude/skills/skill-name",
      "sourceCommitID": "<40-char-hash>",
      "destURL": "https://github.com/org/dest-repo.git",
      "destPath": ".claude/skills/skill-name",
      "destCommitID": "<recorded-after-commit>",
      "destOperator": ".claude/skills/myskillium/SKILL.md",
      "destModel": "<model-id>"
    }
  ]
}
```

### Phase 5: Commit

```
feat: migrate <skill-name> from <source-repo>

Project-specific references cleaned up.
Pedigree documented in genealogy/<skill-name>.json
```

After commit, update the pedigree file with `destCommitID`.

## Experimental Control Requirements

To enable reproducibility research, this process MUST:

1. **Spawn isolated subagent** - Use Task tool, not main conversation
2. **Provide structured data only** - No conversation history passed
3. **Record all variables** - Operator, model, commits in pedigree

This ensures Claude's non-determinism is the only uncontrolled variable.

## Checklist

- [ ] Source skill identified and accessible
- [ ] Cleanup patterns defined
- [ ] Skill files copied to destination
- [ ] Project names generalized
- [ ] Domain terms universalized
- [ ] Example paths made generic
- [ ] Pedigree file created with all fields
- [ ] Commit created with descriptive message
- [ ] destCommitID recorded in pedigree
- [ ] Process used isolated subagent (experimental control)
