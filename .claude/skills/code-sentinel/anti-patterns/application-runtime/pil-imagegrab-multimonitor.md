# Anti-Pattern: PIL ImageGrab Multi-Monitor Failure

## Category
Application/Runtime

## Issue
`PIL.ImageGrab.grab(bbox=...)` can produce black screenshots when capturing windows on secondary monitors.

## Pattern to Avoid
```python
from PIL import ImageGrab

# Direct bbox capture may fail on secondary monitor
img = ImageGrab.grab(bbox=(x1, y1, x2, y2))
```

## Correct Approach
```python
# Option 1: Use mss library (better multi-monitor support)
import mss
with mss.mss() as sct:
    monitor = {"left": x1, "top": y1, "width": width, "height": height}
    img = sct.grab(monitor)

# Option 2: Use Windows Graphics Capture API (Windows 10 1803+)
# Requires pywinrt

# Option 3: Use Win32 BitBlt API
import win32ui, win32gui
# Use BitBlt with proper device contexts
```

## Why It Fails
`PIL.ImageGrab` has known issues with multi-monitor setups:
1. DPI scaling differences between monitors
2. Coordinate system mismatches with virtual screen bounds
3. DirectX/GPU-accelerated content on secondary monitors
4. Different color depths between monitors

The `all_screens=True` approach with cropping also fails due to similar coordinate translation issues.

## Detection
Look for `ImageGrab.grab()` calls in screenshot capture code, especially without DPI awareness handling.

## Test Reference
(No automated test - requires multi-monitor hardware)

## Related Commits
- From failed fix docs: bc46d54 attempted multi-monitor fix but still failed
- ai_docs/FailedFixes/2025-12-10-Secondary-Monitor-Black-Screenshots.md
