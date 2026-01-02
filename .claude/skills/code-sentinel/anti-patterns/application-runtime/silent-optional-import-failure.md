# Anti-Pattern: Silent Dependency Failures

## Category
Application/Runtime

## Issue
Missing optional dependencies cause features to fail silently instead of producing clear error messages.

## Pattern to Avoid
```python
try:
    import pynput
    PYNPUT_AVAILABLE = True
except ImportError:
    PYNPUT_AVAILABLE = False

# Later, feature just doesn't work:
if PYNPUT_AVAILABLE:
    register_click_handler()
# No log, no warning - feature silently missing
```

## Correct Approach
```python
try:
    import pynput
    PYNPUT_AVAILABLE = True
except ImportError:
    PYNPUT_AVAILABLE = False
    logging.warning("pynput not installed - action screenshots disabled")

# At feature initialization
if not PYNPUT_AVAILABLE:
    logging.warning(
        "Action screenshot feature unavailable. "
        "Install with: pip install pynput"
    )
```

## Why It Fails
When optional dependencies fail silently:
1. Users don't know features are missing
2. Developers spend time debugging "working" code
3. The actual issue (missing package) is never surfaced
4. Hours can be wasted before checking requirements

In one case, `pynput` wasn't installed, causing action screenshots to silently not work. The root cause was only discovered after extensive debugging.

## Detection
Look for `try/except ImportError` blocks that only set a boolean flag without any logging.

## Test Reference
(No automated test - requires runtime analysis)

## Related Commits
- From handover 011: Action screenshots not working - root cause was `pynput` not installed
