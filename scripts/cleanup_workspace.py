"""Cleanup utility for generated local artifacts.

Usage:
  python scripts/cleanup_workspace.py --apply
  python scripts/cleanup_workspace.py --dry-run
"""

from __future__ import annotations

import argparse
import fnmatch
import os
import shutil
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]

FILE_PATTERNS = [
    "financial_summary_*.xlsx",
    "students_by_class_*.xlsx",
    "student_database_*.xlsx",
    "student_profile_*.xlsx",
    "teachers_directory_*.xlsx",
]

DB_BACKUP_PATTERNS = [
    "*_integration-test.db",
    "*_test-integration.db",
    "*_automated.db",
]

DIR_PATTERNS = [
    "__pycache__",
]


def iter_matching_files(base: Path, patterns: list[str]):
    for path in base.rglob("*"):
        if not path.is_file():
            continue
        for pattern in patterns:
            if fnmatch.fnmatch(path.name, pattern):
                yield path
                break


def iter_matching_dirs(base: Path, dir_names: list[str]):
    for path in base.rglob("*"):
        if path.is_dir() and path.name in dir_names:
            yield path


def collect_targets() -> list[Path]:
    targets: list[Path] = []

    # Root export files
    targets.extend(iter_matching_files(PROJECT_ROOT, FILE_PATTERNS))

    # Database backup test artifacts
    db_backups = PROJECT_ROOT / "database_backups"
    if db_backups.exists():
        targets.extend(iter_matching_files(db_backups, DB_BACKUP_PATTERNS))

    # Python cache folders
    targets.extend(iter_matching_dirs(PROJECT_ROOT, DIR_PATTERNS))

    # Deduplicate while preserving order
    seen = set()
    unique_targets = []
    for t in targets:
        key = str(t)
        if key not in seen:
            seen.add(key)
            unique_targets.append(t)
    return unique_targets


def remove_target(path: Path):
    if path.is_dir():
        shutil.rmtree(path, ignore_errors=True)
    elif path.exists():
        path.unlink(missing_ok=True)


def main():
    parser = argparse.ArgumentParser(description="Clean generated workspace artifacts")
    parser.add_argument("--apply", action="store_true", help="Apply cleanup changes")
    parser.add_argument("--dry-run", action="store_true", help="Show cleanup targets only")
    args = parser.parse_args()

    apply = args.apply
    if args.dry_run:
        apply = False

    targets = collect_targets()

    print("=" * 72)
    print("Workspace Cleanup")
    print("=" * 72)
    if not targets:
        print("No generated artifacts found.")
        return

    print(f"Found {len(targets)} artifact(s):")
    for target in targets:
        print(f" - {target.relative_to(PROJECT_ROOT)}")

    if not apply:
        print("\nDry-run only. Use --apply to remove listed artifacts.")
        return

    for target in targets:
        remove_target(target)

    print("\nCleanup complete.")


if __name__ == "__main__":
    main()
