# Tropism

## Definition

In the myskillium context, tropism refers to **the process of discovering and locating skills from external sources**. Just as biological tropism is directional growth toward stimuli (light, nutrients, water), skill tropism is directional search toward valuable skill sources across the ecosystem.

Key parallels:
- Stimulus = need for new capability or improvement
- Directional response = targeted search toward likely sources
- Growth toward = progressive refinement of search results
- Sensitivity = ability to detect skill-like patterns in repositories

## Purpose

Discover and evaluate external skills before acquisition:

1. **Identify sources** - Find repositories likely to contain useful skills
2. **Detect skills** - Recognize Claude Code skill patterns in codebases
3. **Evaluate fitness** - Assess whether a skill meets current needs
4. **Prepare for extraction** - Gather information needed for fragmentation

## Tropism Types

| Type | Stimulus | Response |
|------|----------|----------|
| **Chemotropism** | Keyword/concept need | Search for skills by functionality |
| **Phototropism** | Popular/trending sources | Grow toward well-maintained repositories |
| **Thigmotropism** | Direct reference/link | Follow explicit skill recommendations |
| **Hydrotropism** | Resource availability | Seek skills with good documentation |

## Process

### Prerequisites

- Clear understanding of capability gap or need
- Access to potential source repositories (GitHub, local clones)
- Criteria for evaluating skill fitness

### Phase 1: Stimulus Recognition

Define what capability is needed:

```markdown
## Skill Need Assessment
- What problem does this solve?
- What existing solutions have been tried?
- What would an ideal skill provide?
- What constraints must it satisfy?
```

### Phase 2: Source Discovery

Identify repositories likely to contain relevant skills:

**GitHub Search Patterns:**
```
# Find Claude Code skills by structure
path:.claude/skills filename:SKILL.md

# Find skills by keyword
path:.claude/skills "description:" <keyword>

# Find skills in specific org
org:<organization> path:.claude/skills
```

**Known Skill Sources:**
- `Mharbulous/Myskillium` - Skill management and genealogy
- `anthropics/claude-code` - Official Claude Code examples
- Project-specific repositories with `.claude/skills/` directories

### Phase 3: Skill Detection

Identify skill patterns in discovered repositories:

**Skill Indicators:**
| Pattern | Confidence | Notes |
|---------|------------|-------|
| `.claude/skills/<name>/SKILL.md` | High | Standard skill structure |
| YAML frontmatter with `name:` and `description:` | High | Skill metadata |
| `.claude/commands/<name>.md` | Medium | Slash command (simpler) |
| Process/workflow documentation | Low | May be convertible |

**Scan Command:**
```bash
# Check if repository has skills
ls -la <repo>/.claude/skills/ 2>/dev/null || echo "No skills directory"

# List all skills
find <repo>/.claude/skills -name "SKILL.md" -exec dirname {} \;
```

### Phase 4: Fitness Evaluation

Assess whether discovered skill meets needs:

| Criterion | Question | Weight |
|-----------|----------|--------|
| **Functionality** | Does it solve the problem? | Critical |
| **Compatibility** | Works with current Claude Code version? | Critical |
| **Maintainability** | Is it actively maintained? | High |
| **Documentation** | Is usage well-documented? | Medium |
| **Dependencies** | Does it require external tools? | Medium |
| **Portability** | Can it be adapted to our context? | Medium |

**Fitness Score:**
- 3+ Critical criteria met → Proceed to fragmentation
- 1-2 Critical criteria met → Investigate further
- 0 Critical criteria met → Continue search

### Phase 5: Extraction Preparation

Gather information needed for fragmentation:

```json
{
  "candidate": {
    "sourceURL": "https://github.com/org/repo.git",
    "sourcePath": ".claude/skills/skill-name",
    "sourceCommit": "<current-HEAD>",
    "skillName": "<from-frontmatter>",
    "description": "<from-frontmatter>"
  },
  "evaluation": {
    "fitnessScore": "high|medium|low",
    "adaptationNeeded": ["list", "of", "changes"],
    "dependencies": ["external", "requirements"],
    "risks": ["potential", "issues"]
  },
  "decision": "proceed|defer|reject",
  "rationale": "Why this decision was made"
}
```

## Tropism Signals

### Positive Signals (Grow Toward)
- Active commit history
- Clear skill documentation
- Established pedigree/lineage
- Community adoption
- Test coverage

### Negative Signals (Grow Away)
- Abandoned repository
- Missing or unclear documentation
- Heavy project-specific dependencies
- No visible maintenance
- Incompatible license

## Relationship to Other Processes

| Process | Tropism Relationship |
|---------|---------------------|
| **Fragmentation** | Tropism discovers; fragmentation extracts |
| **Plasmogamy** | Tropism may find multiple skills suitable for fusion |
| **Homeostasis** | Tropism may detect upstream updates for existing skills |
| **Conidiation** | Tropism spreads awareness of available conidia |
| **Apoptosis** | Tropism may find replacement before removal |

Tropism is the **sensory process** that precedes action. It answers "where are useful skills?" before fragmentation answers "how do we acquire them?"

## Autonomous Tropism

In future iterations, tropism could become automated:

```python
# Conceptual: Automated skill discovery
def autonomous_tropism(need: str) -> list[SkillCandidate]:
    """
    Periodically scan known sources for skills matching needs.
    Alert when high-fitness candidates discovered.
    """
    sources = load_known_sources()
    candidates = []
    for source in sources:
        skills = scan_for_skills(source)
        for skill in skills:
            if evaluate_fitness(skill, need) > THRESHOLD:
                candidates.append(skill)
    return candidates
```

This would enable myskillium to proactively suggest skill acquisitions.

## Checklist

- [ ] Capability need clearly defined
- [ ] Source repositories identified
- [ ] Skill detection scan completed
- [ ] Candidate skills evaluated for fitness
- [ ] High-fitness candidates documented
- [ ] Extraction preparation info gathered
- [ ] Decision made: proceed, defer, or reject
- [ ] Rationale documented for future reference
- [ ] Handoff to fragmentation process (if proceeding)
