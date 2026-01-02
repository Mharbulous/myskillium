# Anti-Pattern: Hardcoded Windows Path Separators in Cross-Platform Configs

## Category
Build/Version

## Issue
Using backslash path separators in PyInstaller spec files or other configs breaks Linux/macOS builds.

## Pattern to Avoid
```python
# In .spec file
a = Analysis(
    ['lawtime\\__main__.py'],  # Windows backslash
    ...
)
```

## Correct Approach
```python
# In .spec file
a = Analysis(
    ['lawtime/__main__.py'],  # Forward slash works everywhere
    ...
)
```

Or use pathlib for programmatic path construction:
```python
import pathlib
entry_point = str(pathlib.Path('lawtime') / '__main__.py')
```

## Why It Fails
Forward slashes work as path separators on ALL platforms (Windows, Linux, macOS). Backslashes only work on Windows and are escape characters on Unix systems.

CI workflows typically run on ubuntu-latest (Linux), so Windows-specific paths fail even if the target platform is Windows.

## Detection
Look for `\\` in path strings within `.spec` files or cross-platform configuration files.

## Test Reference
`tests/test_code_patterns.py::TestBuildPatterns::test_spec_uses_forward_slashes`

## Related Commits
- From handover 010: `TimeLogger.spec:5` used `lawtime\\__main__.py`
