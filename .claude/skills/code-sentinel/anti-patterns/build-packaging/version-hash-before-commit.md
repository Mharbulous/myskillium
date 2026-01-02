# Anti-Pattern: Build-Time Version Chicken-and-Egg

## Category
Build/Version

## Issue
Build embeds current commit hash into executable, then user commits the build artifacts, so the executable never reflects its own commit.

## Pattern to Avoid
```python
# generate_version.py runs BEFORE commit
commit_hash = subprocess.check_output(["git", "rev-parse", "--short", "HEAD"])
# Writes hash to __init__.py
# Then user commits
# Executable now has OLD hash!
```

## Correct Approach
```python
# Option 1: Use git tags for releases
version = subprocess.check_output(["git", "describe", "--tags", "--always"])

# Option 2: Use separate gitignored file
# Write to _version.py (gitignored)
# __init__.py imports with fallback:
try:
    from ._version import __version__
except ImportError:
    __version__ = "0.0.0.dev"

# Option 3: Accept and document dev behavior
# Clearly document that dev builds have "previous" commit hash
```

## Why It Fails
The version generation script runs before the commit happens:
1. Script reads current HEAD (commit X)
2. Script writes hash to tracked file
3. User commits the changes (commit Y)
4. Build artifacts now contain hash from commit X, not Y

This creates confusion when debugging production issues.

## Detection
Look for scripts that modify tracked Python files with git commit hashes.

## Test Reference
(No automated test - design pattern issue)

## Related Commits
- From handover 010: Build script version generation fixes
- ab5856b, c28e804: Original flawed implementation
