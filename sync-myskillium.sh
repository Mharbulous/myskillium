#!/bin/bash
#
# Sync Myskillium skills to local project.
#
# Fetches the latest Myskillium repository and copies shared skills
# while preserving project-specific files.
#
# Usage:
#     ./sync-myskillium.sh [--dry-run]
#

set -e

# Configuration
MYSKILLIUM_REPO="https://github.com/Mharbulous/Myskillium.git"
MYSKILLIUM_BRANCH="main"

# Parse arguments
DRY_RUN=false
if [[ "$1" == "--dry-run" ]]; then
    DRY_RUN=true
fi

# Check for git
if ! command -v git &> /dev/null; then
    echo "Error: git is not available. Please install git and try again."
    exit 1
fi

# Get project directory
PROJECT_DIR="$(pwd)"

# Read current version
VERSION_FILE="$PROJECT_DIR/.myskillium-version"
if [[ -f "$VERSION_FILE" ]]; then
    OLD_VERSION=$(cat "$VERSION_FILE")
else
    OLD_VERSION=""
fi

# Create temp directory
TEMP_DIR=$(mktemp -d)
trap "rm -rf '$TEMP_DIR'" EXIT

# Clone repository
echo "Fetching Myskillium from $MYSKILLIUM_REPO..."
if ! git clone --depth 1 --branch "$MYSKILLIUM_BRANCH" "$MYSKILLIUM_REPO" "$TEMP_DIR" 2>&1; then
    echo "Error: Failed to fetch Myskillium repository."
    echo "Check your network connection and try again."
    exit 1
fi

# Get new version
NEW_VERSION=$(git -C "$TEMP_DIR" rev-parse HEAD)

# Initialize counters
ADDED=()
UPDATED=()
PRESERVED=()
UNCHANGED=0

# Function to sync a directory
sync_dir() {
    local src="$1"
    local dst="$2"

    if [[ ! -d "$TEMP_DIR/$src" ]]; then
        return
    fi

    # Create destination if needed
    if [[ "$DRY_RUN" == "false" ]]; then
        mkdir -p "$PROJECT_DIR/$dst"
    fi

    # Find all files in source
    while IFS= read -r -d '' src_file; do
        rel_path="${src_file#$TEMP_DIR/$src/}"
        dst_file="$PROJECT_DIR/$dst/$rel_path"

        # Check if file should be preserved
        if [[ "$dst" == ".claude/data" && "$rel_path" == *.db ]]; then
            if [[ -f "$dst_file" ]]; then
                PRESERVED+=("$dst/$rel_path")
                continue
            fi
        fi

        if [[ "$dst/$rel_path" == .claude/local/* ]]; then
            if [[ -f "$dst_file" ]]; then
                PRESERVED+=("$dst/$rel_path")
                continue
            fi
        fi

        if [[ "$dst/$rel_path" == ".claude/settings.local.json" ]]; then
            if [[ -f "$dst_file" ]]; then
                PRESERVED+=("$dst/$rel_path")
                continue
            fi
        fi

        # Compare files
        if [[ -f "$dst_file" ]]; then
            if cmp -s "$src_file" "$dst_file"; then
                ((UNCHANGED++)) || true
                continue
            else
                UPDATED+=("$dst/$rel_path")
            fi
        else
            ADDED+=("$dst/$rel_path")
        fi

        # Copy file
        if [[ "$DRY_RUN" == "false" ]]; then
            mkdir -p "$(dirname "$dst_file")"
            cp "$src_file" "$dst_file"
        fi
    done < <(find "$TEMP_DIR/$src" -type f -print0)
}

# Sync skills directory only
sync_dir ".claude/skills" ".claude/skills"

# Update version file
if [[ "$DRY_RUN" == "false" ]]; then
    echo "$NEW_VERSION" > "$VERSION_FILE"
fi

# Report
echo ""
if [[ "$DRY_RUN" == "true" ]]; then
    echo "=== DRY RUN (no changes made) ==="
    echo ""
fi

OLD_SHORT="${OLD_VERSION:0:7}"
if [[ -z "$OLD_SHORT" ]]; then
    OLD_SHORT="none"
fi
NEW_SHORT="${NEW_VERSION:0:7}"

if [[ "$OLD_VERSION" == "$NEW_VERSION" ]]; then
    echo "Already at version $NEW_SHORT"
else
    echo "Updated from $OLD_SHORT to $NEW_SHORT"
fi

echo ""

if [[ ${#ADDED[@]} -gt 0 ]]; then
    echo "Added (${#ADDED[@]}):"
    for f in "${ADDED[@]}"; do
        echo "  + $f"
    done
    echo ""
fi

if [[ ${#UPDATED[@]} -gt 0 ]]; then
    echo "Updated (${#UPDATED[@]}):"
    for f in "${UPDATED[@]}"; do
        echo "  ~ $f"
    done
    echo ""
fi

if [[ ${#PRESERVED[@]} -gt 0 ]]; then
    echo "Preserved (${#PRESERVED[@]}):"
    for f in "${PRESERVED[@]}"; do
        echo "  * $f"
    done
    echo ""
fi

if [[ $UNCHANGED -gt 0 ]]; then
    echo "Unchanged: $UNCHANGED files"
    echo ""
fi

if [[ "$DRY_RUN" == "false" ]]; then
    echo "Run: git add . && git commit -m 'chore: sync myskillium'"
fi
