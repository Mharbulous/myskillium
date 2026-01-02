# Anti-Pattern: Duplicate Module-Level Constants

## Category
Application/Runtime

## Issue
Different modules independently define the same constant (e.g., `WINDOWS_APIS_AVAILABLE`), leading to inconsistent behavior when they check different dependencies.

## Pattern to Avoid
```python
# tracker.py
try:
    import win32gui, win32process, psutil
    WINDOWS_APIS_AVAILABLE = True
except ImportError:
    WINDOWS_APIS_AVAILABLE = False

# screenshot.py (different file!)
try:
    import win32gui, ImageGrab, imagehash
    WINDOWS_APIS_AVAILABLE = True  # Same name, different check!
except ImportError:
    WINDOWS_APIS_AVAILABLE = False
```

## Correct Approach
```python
# platform_checks.py (single source of truth)
def check_windows_apis():
    """Check if Windows APIs are available."""
    try:
        import win32gui, win32process
        return True
    except ImportError:
        return False

WINDOWS_APIS_AVAILABLE = check_windows_apis()

# Other modules import from here
from .platform_checks import WINDOWS_APIS_AVAILABLE
```

## Why It Fails
When each module independently defines `WINDOWS_APIS_AVAILABLE`:
1. One module may pass (has all its imports)
2. Another module may fail (missing one of its imports)
3. Features silently don't work because checks pass in one place but not another
4. Debugging is confusing because the "same" constant has different values

In one case, tracker.py's check passed but screenshot.py's check (which included imagehash) failed silently.

## Detection
Search for multiple definitions of the same constant name across different files.

## Test Reference
(No automated test - requires cross-file analysis)

## Related Commits
- From handover 008: Two different WINDOWS_APIS_AVAILABLE variables causing silent screenshot failure
