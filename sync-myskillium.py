#!/usr/bin/env python3
"""
Sync Myskillium skills to local project.

Fetches the latest Myskillium repository and copies shared skills
while preserving project-specific files.

Usage:
    python sync-myskillium.py [--dry-run]
"""

import argparse
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

# Configuration
MYSKILLIUM_REPO = "https://github.com/Mharbulous/Myskillium.git"
MYSKILLIUM_BRANCH = "main"

# Directories to sync (source -> destination relative paths)
SYNC_DIRS = [
    (".claude/skills", ".claude/skills"),
]

# Patterns to preserve (never overwrite)
PRESERVE_PATTERNS = [
    ".claude/data/*.db",
    ".claude/local/*",
    ".claude/settings.local.json",
]


def run_command(cmd: list[str], cwd: str | None = None) -> subprocess.CompletedProcess:
    """Run a command and return the result."""
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)


def check_git_available() -> bool:
    """Check if git is available."""
    result = run_command(["git", "--version"])
    return result.returncode == 0


def get_current_version(project_dir: Path) -> str | None:
    """Read the current Myskillium version."""
    version_file = project_dir / ".myskillium-version"
    if version_file.exists():
        return version_file.read_text().strip()
    return None


def clone_myskillium(temp_dir: str) -> str | None:
    """Clone Myskillium repo and return the commit SHA."""
    print(f"Fetching Myskillium from {MYSKILLIUM_REPO}...")
    result = run_command([
        "git", "clone",
        "--depth", "1",
        "--branch", MYSKILLIUM_BRANCH,
        MYSKILLIUM_REPO,
        temp_dir
    ])

    if result.returncode != 0:
        print(f"Error cloning repository: {result.stderr}")
        return None

    # Get commit SHA
    result = run_command(["git", "rev-parse", "HEAD"], cwd=temp_dir)
    if result.returncode != 0:
        print(f"Error getting commit SHA: {result.stderr}")
        return None

    return result.stdout.strip()


def should_preserve(path: Path, project_dir: Path) -> bool:
    """Check if a path should be preserved (not overwritten)."""
    rel_path = path.relative_to(project_dir)
    rel_str = str(rel_path)

    for pattern in PRESERVE_PATTERNS:
        # Simple glob matching
        if pattern.endswith("/*"):
            prefix = pattern[:-2]
            if rel_str.startswith(prefix + "/") or rel_str.startswith(prefix + os.sep):
                return True
        elif pattern.endswith("/*.db"):
            prefix = pattern[:-5]
            if rel_str.startswith(prefix + "/") or rel_str.startswith(prefix + os.sep):
                if rel_str.endswith(".db"):
                    return True
        elif rel_str == pattern:
            return True

    return False


def sync_directory(src_dir: Path, dst_dir: Path, project_dir: Path, dry_run: bool) -> dict:
    """Sync a directory, returning stats about changes."""
    stats = {"added": [], "updated": [], "unchanged": [], "preserved": []}

    if not src_dir.exists():
        return stats

    # Ensure destination exists
    if not dry_run:
        dst_dir.mkdir(parents=True, exist_ok=True)

    # Walk source directory
    for src_path in src_dir.rglob("*"):
        if src_path.is_dir():
            continue

        rel_path = src_path.relative_to(src_dir)
        dst_path = dst_dir / rel_path
        full_dst = project_dir / dst_dir.relative_to(project_dir) / rel_path if dst_dir.is_absolute() else project_dir / dst_dir / rel_path

        # Check if we should preserve this file
        if dst_path.exists() and should_preserve(dst_path, project_dir):
            stats["preserved"].append(str(rel_path))
            continue

        # Check if file exists and compare
        if dst_path.exists():
            src_content = src_path.read_bytes()
            dst_content = dst_path.read_bytes()
            if src_content == dst_content:
                stats["unchanged"].append(str(rel_path))
                continue
            else:
                stats["updated"].append(str(rel_path))
        else:
            stats["added"].append(str(rel_path))

        # Copy file
        if not dry_run:
            dst_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src_path, dst_path)

    return stats


def main():
    parser = argparse.ArgumentParser(description="Sync Myskillium skills to local project")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be done without making changes")
    args = parser.parse_args()

    # Check git
    if not check_git_available():
        print("Error: git is not available. Please install git and try again.")
        sys.exit(1)

    # Get project directory
    project_dir = Path.cwd()

    # Check current version
    old_version = get_current_version(project_dir)

    # Create temp directory and clone
    with tempfile.TemporaryDirectory() as temp_dir:
        new_version = clone_myskillium(temp_dir)
        if not new_version:
            print("Error: Failed to fetch Myskillium repository.")
            print("Check your network connection and try again.")
            sys.exit(1)

        temp_path = Path(temp_dir)

        # Sync directories
        all_stats = {"added": [], "updated": [], "unchanged": [], "preserved": []}

        for src_rel, dst_rel in SYNC_DIRS:
            src_dir = temp_path / src_rel
            dst_dir = project_dir / dst_rel
            stats = sync_directory(src_dir, dst_dir, project_dir, args.dry_run)

            for key in all_stats:
                all_stats[key].extend([f"{dst_rel}/{f}" for f in stats[key]])

        # Update version file
        if not args.dry_run:
            version_file = project_dir / ".myskillium-version"
            version_file.write_text(new_version + "\n")

    # Report
    print()
    if args.dry_run:
        print("=== DRY RUN (no changes made) ===")
        print()

    old_short = old_version[:7] if old_version else "none"
    new_short = new_version[:7]

    if old_version == new_version:
        print(f"Already at version {new_short}")
    else:
        print(f"Updated from {old_short} to {new_short}")

    print()

    if all_stats["added"]:
        print(f"Added ({len(all_stats['added'])}):")
        for f in all_stats["added"]:
            print(f"  + {f}")
        print()

    if all_stats["updated"]:
        print(f"Updated ({len(all_stats['updated'])}):")
        for f in all_stats["updated"]:
            print(f"  ~ {f}")
        print()

    if all_stats["preserved"]:
        print(f"Preserved ({len(all_stats['preserved'])}):")
        for f in all_stats["preserved"]:
            print(f"  * {f}")
        print()

    if all_stats["unchanged"]:
        print(f"Unchanged: {len(all_stats['unchanged'])} files")
        print()

    if not args.dry_run:
        print("Run: git add . && git commit -m 'chore: sync myskillium'")


if __name__ == "__main__":
    main()
