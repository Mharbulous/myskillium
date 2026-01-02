---
name: code-reviewing
description: Use when completing implementation, before escalating to human review, or when human checkpoint is reached - performs AI-assisted code review covering security, AI-specific issues, logic errors, and architecture to ensure humans see fresh analysis
---

# Code Reviewing

Perform AI-assisted code review immediately before escalating to human review. Ensures humans always see fresh, relevant code analysis when making decisions.

## When to Use

- After completing implementation work (executing stage)
- Before any human checkpoint/escalation
- When `/AI-review` is invoked
- Before creating PRs or requesting human review

## Quick Reference

| Stage | Focus Areas |
|-------|-------------|
| **concept** | Clarity, scope, testable criteria |
| **planning** | Design quality, pattern adherence |
| **executing** | Security, logic, architecture, tests |
| **testing** | Integration, coverage, regressions |
| **releasing** | All findings addressed, docs complete |

---

## Review Process

### Phase 1: Gather Context

1. **Identify changed files** - `git diff` or compare to last review
2. **Load task context** - Read task description, acceptance criteria
3. **Check stage** - Adjust review focus based on current stage

### Phase 2: Run Automated Checks

```bash
# Python projects
python -m flake8 src/ || echo "No flake8"
python -m mypy src/ || echo "No mypy"

# JavaScript/TypeScript projects
npm run lint || echo "No linter"
npm run typecheck || echo "No type checker"
```

### Phase 3: AI Analysis

**See `references/review-checklist.md` for complete checklist.**

Key areas:

| Category | Critical Checks |
|----------|-----------------|
| **Security** | Input validation, no hardcoded secrets, parameterized queries |
| **AI-specific** | No hallucinated APIs, follows project patterns, appropriate abstraction |
| **Logic** | Edge cases (null, empty, boundary), error handling, no infinite loops |
| **Architecture** | Follows conventions, correct dependency flow, no circular deps |

### Phase 4: Generate Report

```markdown
## AI Code Review Report

**Task:** [ID] - [Title]
**Stage:** [current_stage]
**Files reviewed:** [count]
**Review date:** [timestamp]

### Summary
[1-2 sentence overall assessment]

### Findings

#### Critical (must fix)
- [ ] [Finding with file:line reference]

#### Warnings (should fix)
- [ ] [Finding with file:line reference]

#### Suggestions (consider)
- [ ] [Finding with file:line reference]

### Automated Check Results
- Linting: [pass/fail/skipped]
- Type check: [pass/fail/skipped]

### Recommended Actions
1. [Specific action item]
```

### Phase 5: Save Review

1. **Update task notes** - Append review summary
2. **Create artifact** - Save to `.claude/data/reviews/{task_id}_{timestamp}.md`

---

## Stage-Specific Focus

### Concept Stage
- Concept clearly defined?
- Scope bounded and reasonable?
- Acceptance criteria verifiable?

### Planning Stage
- Design follows established patterns?
- Avoids known anti-patterns?
- Plan is implementable?

### Executing Stage (Full Review)
- All security checks
- All AI-specific checks
- All logic checks
- All architecture checks
- Tests adequate for changes?
- Code matches the plan?

### Testing Stage
- Integration interfaces properly defined?
- Test coverage adequate?
- Regression test coverage exists?

### Releasing Stage
- All previous findings addressed?
- Documentation complete?
- Release checklist items documented?

---

## Common AI Code Mistakes

**See `references/common-ai-mistakes.md` for complete patterns.**

| Issue | Detection |
|-------|-----------|
| Hallucinated APIs | Verify imports/methods exist |
| Outdated patterns | Check for deprecation warnings |
| Missing edge cases | Test null, empty, boundaries |
| Security blind spots | Check input validation, query building |
| Over-abstraction | Is complexity justified? |
| Silent failures | Look for bare `except: pass` |

---

## Reference Files

| File | Purpose |
|------|---------|
| `references/best-practices-research.md` | Industry research on AI code review |
| `references/tool-capabilities.md` | What CodeRabbit, Copilot, Semgrep, SonarQube check |
| `references/review-checklist.md` | Complete checklist by category |
| `references/common-ai-mistakes.md` | Patterns specific to AI-generated code |

---

## Invocation

```
/AI-review --task-id=[ID] --stage=[current_stage]
```

Or simply `/AI-review` when context is clear from current work.
