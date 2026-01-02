# Conidiation

## Biological Definition

**Conidiation** is the asexual reproductive process in fungi where specialized structures called **conidiophores** produce **conidia** (spores). These spores are genetically identical to the parent organism and serve as portable propagules that can germinate in new environments. The process involves:

1. Development of spore-producing structures
2. Mitotic division to create spores
3. Release of spores for dispersal

## Skill Analogy

In the myskillium context, conidiation refers to **creating or updating the portable extraction tool** (`myskillium-spore.py`). Just as fungi produce spores to enable reproduction elsewhere, this process creates the mechanism that enables skill extraction across repositories.

## Purpose

The spore tool is a standalone script that can be copied into any repository to perform skill extraction without requiring the full myskillium skill to be present.

## Process

> **Status**: Not yet implemented

### Planned Workflow

1. **Package extraction logic** into portable Python script
2. **Include pedigree schema** for genealogy documentation
3. **Minimize dependencies** for maximum portability
4. **Version the spore** with its parent myskillium commit

### Output

```
myskillium-spore.py  # Portable extraction tool
```

## Relationship to Other Processes

| Process | Relationship |
|---------|-------------|
| Fragmentation | Uses the spore tool to perform extraction |
| Plasmogamy | Uses the spore tool to perform fusion |

The spore is the **mechanism**; fragmentation and plasmogamy are the **operations** that use it.
