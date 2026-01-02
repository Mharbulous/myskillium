# AI Code Review Checklist

Use this checklist during code review. Check each applicable item.

---

## Security

### Input Validation
- [ ] User input validated before use
- [ ] Input sanitized for expected type/format
- [ ] Length limits enforced where applicable
- [ ] Reject unexpected input rather than try to clean it

### Authentication & Authorization
- [ ] Auth checks present on protected resources
- [ ] Authorization verified (not just authentication)
- [ ] Session handling is secure
- [ ] No hardcoded credentials or secrets
- [ ] API keys not exposed in client code

### Injection Prevention
- [ ] SQL queries use parameterized statements
- [ ] No string concatenation for queries
- [ ] Command execution escapes/sanitizes input
- [ ] Path traversal prevented (no `../` exploitation)
- [ ] XSS prevented (output properly escaped)

### Data Protection
- [ ] Sensitive data not logged
- [ ] Error messages don't reveal internals
- [ ] PII handled according to policy
- [ ] Secrets not committed to repo

---

## AI-Generated Code Specific

### Hallucination Checks
- [ ] All imported modules/packages exist
- [ ] All called methods/functions exist in the API
- [ ] API usage matches current documentation
- [ ] No made-up library features

### Outdated Patterns
- [ ] No deprecated APIs used
- [ ] Follows current framework conventions
- [ ] No security patterns that were patched years ago
- [ ] Using modern language features appropriately

### Over-Engineering
- [ ] Abstraction level appropriate for use case
- [ ] No unnecessary design patterns
- [ ] Not over-generalized for hypothetical futures
- [ ] Complexity justified by requirements

### Context Alignment
- [ ] Follows project's existing patterns
- [ ] Consistent with codebase naming conventions
- [ ] Matches architectural decisions
- [ ] Aligns with business logic requirements

---

## Logic & Correctness

### Edge Cases
- [ ] Null/None checks where needed
- [ ] Empty collection handling
- [ ] Boundary conditions (0, 1, max)
- [ ] Array bounds checked before access
- [ ] Division by zero prevented

### Error Handling
- [ ] Errors caught at appropriate level
- [ ] Error messages are useful (not too verbose, not too vague)
- [ ] Failed operations don't leave bad state
- [ ] Resources cleaned up on error (finally/with/using)

### Control Flow
- [ ] No infinite loops without exit conditions
- [ ] Recursion has base case
- [ ] Async/await used correctly
- [ ] Race conditions considered
- [ ] State mutations are intentional

### Data Integrity
- [ ] Type conversions are safe
- [ ] Floating point comparisons done correctly
- [ ] String encoding handled properly
- [ ] Timezone handling correct for dates

---

## Architecture & Design

### Project Conventions
- [ ] Follows project file/folder structure
- [ ] Uses established patterns from codebase
- [ ] Naming matches project conventions
- [ ] Import style matches project

### Dependencies
- [ ] No circular dependencies introduced
- [ ] Dependencies flow in correct direction
- [ ] New dependencies justified
- [ ] Version constraints appropriate

### Modularity
- [ ] Single responsibility per function/class
- [ ] Appropriate encapsulation
- [ ] Public interface is minimal
- [ ] Changes are cohesive (one concern)

### Coupling
- [ ] Low coupling between modules
- [ ] No god classes/functions
- [ ] Dependencies are injectable/mockable

---

## Maintainability

### Readability
- [ ] Code is self-documenting where possible
- [ ] Complex logic has explanatory comments
- [ ] No magic numbers/strings (use constants)
- [ ] Variable names are descriptive

### Simplicity
- [ ] No dead code
- [ ] No duplicated code (DRY)
- [ ] No unnecessarily complex constructs
- [ ] Could a junior understand this?

### Testability
- [ ] New code has tests
- [ ] Tests are meaningful (not just coverage)
- [ ] Tests cover edge cases
- [ ] Tests don't test implementation details
- [ ] No tests deleted or skipped to make code pass

---

## Performance

### Efficiency
- [ ] No N+1 queries
- [ ] Appropriate data structures used
- [ ] No unnecessary iterations
- [ ] Memory allocations reasonable

### Scalability
- [ ] Will this work with 10x data?
- [ ] Database queries are indexed
- [ ] Pagination used for large collections

### Resource Management
- [ ] Files/connections closed properly
- [ ] No memory leaks (event listeners, etc.)
- [ ] Caching used appropriately

---

## Quick Reference by Review Stage

### Concept Stage
Focus: Clarity, scope, testable acceptance criteria
- [ ] Concept is clearly defined
- [ ] Scope is bounded and reasonable
- [ ] Acceptance criteria are verifiable

### Planning Stage
Focus: Design quality, pattern adherence
- [ ] Design follows established patterns
- [ ] Avoids known anti-patterns
- [ ] Plan is implementable with available resources

### Executing Stage
Focus: Full code review
- [ ] All sections above checked
- [ ] Tests adequate for changes
- [ ] Code matches the plan

### Testing Stage
Focus: Integration, coverage
- [ ] Integration interfaces properly defined
- [ ] Test coverage is adequate
- [ ] Regression test coverage exists

### Releasing Stage
Focus: Final inspection
- [ ] All previous findings addressed
- [ ] Documentation complete
- [ ] Release checklist items documented
