# Plasmogamy

## Biological Definition

**Plasmogamy** is the first stage of sexual reproduction in fungi, where the **cytoplasm of two parent cells fuses together**. This brings genetic material from both parents into a single cell, though nuclear fusion (karyogamy) occurs later. The process involves:

1. Two compatible hyphae make contact
2. Cell walls dissolve at the contact point
3. Cytoplasm merges, creating a cell with nuclei from both parents
4. The resulting organism carries genetic contributions from both sources

This is distinct from asexual reproduction (fragmentation, conidiation) because it combines traits from multiple parents rather than cloning a single parent.

## Skill Analogy

In the mysk-extractor context, plasmogamy refers to **fusing two or more skills into a single hybrid skill**. Just as fungal plasmogamy combines genetic material from multiple parents, skill plasmogamy combines functionality, patterns, and approaches from multiple source skills.

Key parallels:
- Two (or more) parent skills contribute to the hybrid
- The hybrid has characteristics of both parents
- The combination creates something neither parent had alone
- Lineage from all parents is preserved in pedigree

## Purpose

Create a new skill by combining elements from multiple existing skills:
- Merge complementary functionality
- Combine different approaches to the same problem
- Synthesize best practices from multiple sources
- Create specialized variants by crossing general skills

## Process

> **Status**: Not yet implemented

### Planned Workflow

#### Phase 1: Select Parents

Identify two or more skills to combine:
- Define what each parent contributes
- Identify complementary vs conflicting elements
- Plan how conflicts will be resolved

#### Phase 2: Extract Parent Material

For each parent skill:
- Record source commit and path
- Extract the elements to be combined
- Document what is being taken from each

#### Phase 3: Fusion

Combine parent elements into hybrid:
- Merge non-conflicting sections
- Resolve conflicts according to plan
- Synthesize new sections that bridge parents
- Ensure coherent whole

#### Phase 4: Genealogy

Create pedigree with **multiple entries** in the array:

```json
{
  "name": "hybrid-skill-name",
  "description": "Hybrid combining parent-a and parent-b",
  "pedigree": [
    {
      "date": "YYYY-MM-DD",
      "sourceURL": "https://github.com/org/repo-a.git",
      "sourcePath": ".claude/skills/parent-a",
      "sourceCommitID": "<parent-a-commit>",
      "destURL": "https://github.com/org/myskillium.git",
      "destPath": ".claude/skills/hybrid-skill",
      "destCommitID": "<recorded-after-commit>",
      "destOperator": ".claude/skills/mysk-extractor/SKILL.md",
      "destModel": "<model-id>"
    },
    {
      "date": "YYYY-MM-DD",
      "sourceURL": "https://github.com/org/repo-b.git",
      "sourcePath": ".claude/skills/parent-b",
      "sourceCommitID": "<parent-b-commit>",
      "destURL": "https://github.com/org/myskillium.git",
      "destPath": ".claude/skills/hybrid-skill",
      "destCommitID": "<recorded-after-commit>",
      "destOperator": ".claude/skills/mysk-extractor/SKILL.md",
      "destModel": "<model-id>"
    }
  ]
}
```

#### Phase 5: Commit

```
feat: create <hybrid-name> by fusing <parent-a> and <parent-b>

Combined: [list of elements from each parent]
Pedigree documents both parent lineages.
```

## Experimental Control Requirements

To enable reproducibility research, this process MUST:

1. **Spawn isolated subagent** - Use Task tool, not main conversation
2. **Provide structured data only** - All parent content via parameters
3. **Record all variables** - Operator, model, all parent commits in pedigree

## Variance as the Primary Observable

### Why Plasmogamy Produces Higher Variance

Fragmentation is essentially a **transformation task**: take existing content, clean it up, move it. The input-output relationship is relatively deterministic - given the same source skill and cleanup rules, the output should be similar across runs.

Plasmogamy is fundamentally different. It requires **creative synthesis**:

| Fragmentation (Low Variance) | Plasmogamy (High Variance) |
|------------------------------|---------------------------|
| Copy and transform | Create and synthesize |
| Rules-based cleanup | Judgment-based integration |
| Single source of truth | Multiple sources to reconcile |
| Preserve original structure | Invent new structure |
| Obvious "correct" answer | Multiple valid solutions |

When Claude fuses two skills, it must make decisions that have no objectively correct answer:
- How to order sections from different parents?
- Which parent's phrasing to prefer when both address the same concept?
- How to bridge gaps where parents have different assumptions?
- What new connecting tissue to synthesize?

These decisions exist in a **high-dimensional solution space**. Even with identical inputs, Claude's inherent non-determinism will navigate this space differently each time.

### The Experimental Opportunity

By controlling all external variables (source content, operator, model, human input), we isolate Claude's non-determinism as the **sole source of variance**. This creates a natural experiment:

```
Run plasmogamy N times with identical inputs
    ↓
Measure variance in outputs
    ↓
Compare to fragmentation variance baseline
    ↓
Quantify the "creativity tax" - additional variance introduced by synthesis tasks
```

### What We Can Learn

1. **Variance spectrum**: How does output variance correlate with task type (transformation vs synthesis)?

2. **Consistency boundaries**: At what complexity threshold does Claude's output become unpredictably variable?

3. **Operator design**: Can operator instructions reduce synthesis variance without eliminating beneficial creativity?

4. **Model comparison**: Do different Claude models (Haiku vs Sonnet vs Opus) show different variance profiles on the same fusion task?

5. **Determinism ceiling**: Is there a theoretical minimum variance for synthesis tasks, or does creative work have inherent irreducible variance?

### Pedigree as Experimental Record

The pedigree file isn't just genealogy - it's **experimental documentation**. By recording:

- Exact source commits (inputs)
- Operator version (transformation function)
- Model ID (processing engine)
- Output commit (results)

We create an auditable record that proves: *"All controllable variables were held constant. Any variance observed is attributable to model non-determinism."*

This transforms skill management into **empirical AI research**.

## Checklist

- [ ] Parent skills identified
- [ ] Contribution from each parent defined
- [ ] Conflict resolution planned
- [ ] Parent material extracted
- [ ] Fusion performed by isolated subagent
- [ ] Hybrid skill coherent and functional
- [ ] Pedigree file created with entries for ALL parents
- [ ] Commit created with descriptive message
- [ ] destCommitID recorded in pedigree
