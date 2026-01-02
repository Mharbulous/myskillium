# Anti-Pattern: Missing Workflow Dispatch Permissions

## Category
CI/Workflow

## Issue
`gh workflow run` silently fails because GITHUB_TOKEN lacks `actions: write` permission.

## Pattern to Avoid
```yaml
permissions:
  contents: write
  issues: write
  # Missing actions: write - gh workflow run will fail
```

## Correct Approach
```yaml
permissions:
  contents: write
  issues: write
  actions: write  # Required to trigger other workflows
```

## Why It Fails
When a workflow uses `gh workflow run` to dispatch child workflows, the GITHUB_TOKEN must have `actions: write` permission. Without it, the command fails silently (exit code 0 but no workflow triggered), making debugging difficult.

## Detection
Look for workflows that use `gh workflow run` but don't have `actions: write` in their permissions block.

## Test Reference
`tests/test_code_patterns.py::TestCIWorkflowPatterns::test_workflow_dispatch_has_actions_permission`

## Related Commit
7bc3169 - fix: add actions:write permission to orchestrator workflow
