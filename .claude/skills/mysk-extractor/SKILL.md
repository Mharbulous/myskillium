---
name: mysk-extractor
description: Use when migrating skills between repositories or extracting skills from a project into a reusable form. Handles copying, cleanup of project-specific references, and genealogy documentation.
---

# Mysk Extractor

Migrate and crossbreed skills between repositories while documenting provenance for reproducibility research.

## Processes

This skill supports three operations, named after mycological reproductive processes:

| Process | File | Description |
|---------|------|-------------|
| **Conidiation** | `processes/conidiation.md` | Spore production - create/update the portable extraction tool |
| **Fragmentation** | `processes/fragmentation.md` | Asexual reproduction - extract a skill from a single source repo |
| **Plasmogamy** | `processes/plasmogamy.md` | Sexual reproduction - fuse two skills into a hybrid |

## Pedigree Schema

Every extracted skill gets a genealogy file documenting its lineage.

### Schema Structure

```json
{
  "name": "skill-name",
  "description": "Skill description from frontmatter",
  "pedigree": [
    {
      "date": "YYYY-MM-DD",
      "sourceURL": "https://github.com/org/source-repo.git",
      "sourcePath": ".claude/skills/original-skill",
      "sourceCommitID": "abcdef1234567890abcdef1234567890abcdef12",
      "destURL": "https://github.com/org/dest-repo.git",
      "destPath": ".claude/skills/extracted-skill",
      "destCommitID": "1234567890abcdef1234567890abcdef12345678",
      "destOperator": ".claude/skills/mysk-extractor/SKILL.md",
      "destModel": "claude-opus-4-5-20251101"
    }
  ]
}
```

### Field Reference

| Field | Purpose |
|-------|---------|
| `date` | When the extraction occurred |
| `sourceURL` | Git URL of the source repository |
| `sourcePath` | Path to skill within source repo |
| `sourceCommitID` | Exact commit hash at extraction time |
| `destURL` | Git URL of the destination repository |
| `destPath` | Path to skill within destination repo |
| `destCommitID` | Commit hash after extraction was committed |
| `destOperator` | The skill file that performed the extraction |
| `destModel` | Claude model ID that executed the operator |

### Crossbreeding Support

The `pedigree` array supports multiple entries for hybrid skills:
- Single entry = conidiation (one parent)
- Multiple entries = plasmogamy (multiple parents fused)

## Experimental Design: Isolated Agents

### Why Exclude Human Input

The pedigree schema captures all variables needed to theoretically reproduce a skill extraction:
- Source content (via `sourceCommitID`)
- Transformation logic (via `destOperator` at `destCommitID`)
- Model version (via `destModel`)

However, if human prompts influence the extraction, they become an uncontrolled variable that breaks reproducibility.

### Isolating Claude's Non-Determinism

By designing extraction processes to:
1. **Spawn subagents** rather than work in the main conversation
2. **Feed structured data** rather than conversation history
3. **Exclude human prompt context** from the transformation

We control for all external variables, leaving **Claude's inherent non-determinism as the only remaining variable**.

This enables experiments like:
- Run identical extractions N times → measure output variance
- Compare variance across different operator designs
- Correlate variance with task complexity

The pedigree file serves dual purposes:
1. **Genealogy record** - trace skill ancestry
2. **Experimental control log** - prove all controllable variables were fixed

### Implications for Process Design

Both `fragmentation.md` and `plasmogamy.md` processes MUST:
- Use the Task tool to spawn isolated subagents
- Provide all context via structured parameters, not conversation history
- Record the exact operator and model in the pedigree

## Templates

| File | Purpose |
|------|---------|
| `genealogy/templates/migration-config.json` | Migration configuration structure |
| `genealogy/templates/pedigree.json` | Pedigree file template |

## Workflow (Fragmentation)

See `processes/fragmentation.md` for the full single-source extraction workflow.

High-level phases:
1. **Configure** - Define source/destination and cleanup rules
2. **Copy** - Transfer skill files
3. **Cleanup** - Generalize project-specific references
4. **Genealogy** - Create pedigree record
5. **Commit** - Finalize with descriptive message

## Checklist

- [ ] Process spawns isolated subagent (no conversation context)
- [ ] Subagent receives structured data only
- [ ] Skills copied to destination
- [ ] Project names generalized
- [ ] Domain terms universalized
- [ ] Pedigree file created with all fields populated
- [ ] destCommitID recorded after commit
