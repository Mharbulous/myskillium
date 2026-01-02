# Anti-Pattern: Generated Files Still Tracked by Git

## Category
Build/Version

## Issue
Files committed to git before adding them to `.gitignore` remain tracked, causing dirty working trees after builds.

## Pattern to Avoid
```bash
# Commit version_info.txt first
git add version_info.txt
git commit -m "Add version info"

# Later add to .gitignore
echo "version_info.txt" >> .gitignore
# File is still tracked!
```

## Correct Approach
```bash
# 1. Add to .gitignore BEFORE committing
echo "version_info.txt" >> .gitignore
git add .gitignore
git commit -m "Ignore generated version info"

# OR if already tracked, untrack it:
git rm --cached version_info.txt
git commit -m "Untrack generated version info"
```

## Why It Fails
Git's `.gitignore` only affects untracked files. Once a file is committed, it remains tracked regardless of `.gitignore`. This causes:
1. Build scripts modify the file
2. `git status` shows changes
3. CI may fail due to dirty working tree
4. Developers accidentally commit generated content

## Detection
Compare files in `.gitignore` against `git ls-files` to find files that are both ignored AND tracked.

## Test Reference
(No automated test - requires git state inspection)

## Related Commits
- From handover 010: `version_info.txt` was committed before ignore rule
- General pattern from build script version generation fixes
