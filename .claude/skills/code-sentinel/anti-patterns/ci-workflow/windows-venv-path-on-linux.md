# Anti-Pattern: Windows venv Activation Path on Linux

## Category
CI/Workflow

## Issue
Using Windows-style virtual environment activation path (`venv\Scripts\activate`) in GitHub Actions (which runs on Linux).

## Pattern to Avoid
```yaml
- name: Run in venv
  run: |
    venv\Scripts\activate
    python script.py
```

## Correct Approach
```yaml
- name: Run in venv
  run: |
    source venv/bin/activate
    python script.py
```

Or use platform detection:
```yaml
- name: Activate venv
  run: |
    if [[ "$RUNNER_OS" == "Windows" ]]; then
      source venv/Scripts/activate
    else
      source venv/bin/activate
    fi
```

## Why It Fails
GitHub Actions ubuntu runners use Linux, which:
1. Uses forward slashes for paths
2. Has venv activation script at `venv/bin/activate`, not `venv/Scripts/activate`
3. Uses `source` or `.` to activate, not just the path

The Windows path structure doesn't exist on Linux, causing the workflow to fail with "file not found."

## Detection
Look for `venv\\Scripts\\activate` or `venv\Scripts\activate` in `.github/workflows/*.yml` files.

## Test Reference
`tests/test_code_patterns.py::TestCIWorkflowPatterns::test_venv_activation_uses_linux_path`

## Related Commits
- From handover 051: CI workflow using Windows paths on Linux runners
