# Anti-Pattern: PIL-Saved ICO Files Render Invisible

## Category
Application/Runtime

## Issue
ICO files saved by PIL may render as invisible/blank when loaded by pystray on Windows, even though the file structure appears valid.

## Pattern to Avoid
```python
from PIL import Image

# Create or modify image
img = Image.open("source.png")
img = img.convert("RGBA")

# Save as ICO
img.save("icon.ico", format="ICO")  # May render invisible!
```

## Correct Approach
```python
# Option 1: Use pre-generated ICO from native tools (Inkscape, GIMP)
icon = Image.open("prebuilt-icon.ico")

# Option 2: Use PNG format instead of ICO
icon = Image.open("icon.png")  # PNG works reliably

# Option 3: Load and transform in memory without saving
base_icon = Image.open("working-icon.ico")
# Apply transformations
transformed = recolor_pixels(base_icon)
# Pass directly to pystray without saving to ICO
```

## Why It Fails
The exact root cause is unclear, but PIL-saved ICO files differ from those created by native tools:
1. PIL ICO format may have different internal structure
2. Multi-size ICO handling may differ (9 sizes, 16-256px)
3. ICO metadata may conflict with pystray's serialization
4. PNG compression within ICO may differ

Working icons created by Inkscape rendered correctly, but equivalent PIL-saved versions were invisible.

## Detection
Look for `.save(..., format="ICO")` calls in the codebase.

## Test Reference
(No automated test - requires Windows pystray testing)

## Related Commits
- From handover 058: Tray feedback icon renders invisible
- ai_docs/FailedFixes/icon-usage-analysis.md
- Resolution: Used pre-generated PNG instead of ICO
