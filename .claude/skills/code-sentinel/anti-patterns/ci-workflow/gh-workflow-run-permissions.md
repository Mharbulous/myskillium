# Anti-Pattern: Missing Workflow Dispatch Permissions

## Category
CI/Workflow

## Issue
`gh workflow run` silently fails without `actions: write` permission in the workflow's permissions block.

## Pattern to Avoid
```yaml
permissions:
  contents: write
  # Missing actions: write

jobs:
  dispatch-job:
    runs-on: ubuntu-latest
    steps:
      - run: gh workflow run other-workflow.yml
```

## Correct Approach
```yaml
permissions:
  contents: write
  actions: write  # Required for gh workflow run

jobs:
  dispatch-job:
    runs-on: ubuntu-latest
    steps:
      - run: gh workflow run other-workflow.yml
```

## Why It Fails
When a workflow uses `gh workflow run` to trigger another workflow, it needs `actions: write` permission. Without this permission, the dispatch call completes without error but the target workflow never starts. This is particularly insidious because there's no error message - the call simply does nothing.

## Detection
Look for `gh workflow run` or `gh workflow dispatch` in GitHub Actions workflows, then verify `actions: write` is in the `permissions:` block.

## Test Reference
`tests/test_code_patterns.py::TestCIWorkflowPatterns::test_workflow_dispatch_has_actions_permission`

## Related Commits
- 7bc3169 - fix: add actions:write permission to orchestrator workflow
- 57080d9 - fix: add actions:write permission to orchestrator
