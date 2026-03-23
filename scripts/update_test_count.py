#!/usr/bin/env python3
"""
Update test count across the entire repository from a single source of truth.

Workflow:
  1. Run ``pytest --collect-only`` to get the actual test count.
  2. Write the canonical count to ``scripts/test_count.txt``.
  3. Sweep every documentation, web, and instruction file that references
     the test count and update it in-place.

The single source of truth is ``scripts/test_count.txt`` — a one-line file
containing just the integer.  All references across the repository are
derived from this file so they stay in sync automatically.
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

# ── Canonical source of truth ────────────────────────────────────
_REPO_ROOT = Path(__file__).resolve().parent.parent
_COUNT_FILE = _REPO_ROOT / "scripts" / "test_count.txt"


def get_test_count() -> int:
    """Get the total number of tests by running pytest --collect-only."""
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pytest", "--collect-only"],
            capture_output=True,
            text=True,
            timeout=120,
            cwd=str(_REPO_ROOT),
        )
        # Primary: "N tests collected" summary line
        for pattern in [r"(\d+) tests? collected", r"(\d+) passed"]:
            match = re.search(pattern, result.stdout)
            if match:
                return int(match.group(1))
        # Fallback: count test-item lines
        test_lines = [line for line in result.stdout.splitlines() if line.strip().startswith("tests/") and "::" in line]
        if test_lines:
            return len(test_lines)
        print("Warning: Could not parse test count from pytest output", file=sys.stderr)
        return 0
    except Exception as e:
        print(f"Error running pytest: {e}", file=sys.stderr)
        return 0


def read_canonical_count() -> int:
    """Read the last-known count from the source-of-truth file."""
    if _COUNT_FILE.exists():
        text = _COUNT_FILE.read_text(encoding="utf-8").strip()
        if text.isdigit():
            return int(text)
    return 0


def write_canonical_count(count: int) -> None:
    """Persist the canonical count."""
    _COUNT_FILE.write_text(f"{count}\n", encoding="utf-8")


def count_test_files() -> int:
    """Count test files in tests/ directory (top-level test_*.py)."""
    test_dir = _REPO_ROOT / "tests"
    if not test_dir.exists():
        return 0
    return len(list(test_dir.glob("test_*.py")))


def count_closure_test_files() -> int:
    """Count test files in tests/closures/ directory."""
    closure_dir = _REPO_ROOT / "tests" / "closures"
    if not closure_dir.exists():
        return 0
    return len(list(closure_dir.glob("test_*.py")))


# ── File update logic ────────────────────────────────────────────
# Each target file gets a list of (compiled_regex, replacement_template)
# pairs.  Templates use {count}, {count_comma}, {count_url}, {files},
# {files_total}, {files_top}, {files_closure} placeholders.


def _build_replacements(
    test_count: int,
    test_files_top: int,
    test_files_closure: int,
) -> dict[str, str]:
    """Build the placeholder dict used in replacement templates."""
    total_files = test_files_top + test_files_closure
    return {
        "count": str(test_count),
        "count_comma": f"{test_count:,}",
        "count_url": f"{test_count:,}".replace(",", "%2C"),
        "files_top": str(test_files_top),
        "files_closure": str(test_files_closure),
        "files_total": str(total_files),
        # total including conftest.py
        "files_total_plus": str(total_files + 1),
    }


def _update_generic(
    content: str,
    old_count_comma: str,
    old_count_url: str,
    vals: dict[str, str],
) -> str:
    """Replace all occurrences of the old count with the new one.

    This is the primary sweep — it replaces the comma-formatted count
    and the URL-encoded count everywhere they appear, but is careful
    to avoid partial matches on unrelated numbers.
    """
    # Direct comma-formatted count replacement
    content = content.replace(old_count_comma, vals["count_comma"])
    # URL-encoded count: "11%2C489" → "11%2C676"
    content = content.replace(old_count_url, vals["count_url"])
    return content


def _update_test_file_counts(content: str, vals: dict[str, str]) -> str:
    """Update test file count references (e.g., '168 test files')."""
    # "NNN test files" pattern
    content = re.sub(
        r"\b\d+ test files\b",
        f"{vals['files_total']} test files",
        content,
    )
    # "NNN test file" (singular, in tree diagrams)
    content = re.sub(
        r"\b(\d+) test file,",
        f"{vals['files_total']} test file,",
        content,
    )
    # "(NNN top-level test_*.py + N in tests/closures/ + conftest.py)"
    content = re.sub(
        r"\d+ top-level `test_\*\.py` \+ \d+ in `tests/closures/`",
        f"{vals['files_top']} top-level `test_*.py` + {vals['files_closure']} in `tests/closures/`",
        content,
    )
    # "across NNN files" (e.g., README_PYPI table)
    content = re.sub(
        r"(across\s+)\d+(\s+files\b)",
        rf"\g<1>{vals['files_total']}\2",
        content,
    )
    return content


def update_file(
    filepath: Path,
    old_count_comma: str,
    old_count_url: str,
    vals: dict[str, str],
) -> bool:
    """Update all test count references in a single file."""
    if not filepath.exists():
        return False

    content = filepath.read_text(encoding="utf-8")
    original = content

    # 1) Generic count replacement (comma + URL-encoded)
    content = _update_generic(content, old_count_comma, old_count_url, vals)

    # 2) Test file count updates
    content = _update_test_file_counts(content, vals)

    # 3) Targeted patterns for specific file formats
    # Badge: tests-NNN-brightgreen
    content = re.sub(
        r"tests-[\d%2C]+-brightgreen",
        f"tests-{vals['count_url']}-brightgreen",
        content,
    )

    # "Should show NNNN tests"
    content = re.sub(
        r"(Should show\s+)[\d,]+(\s+tests?\b)",
        rf"\g<1>{vals['count_comma']}\2",
        content,
    )

    # "suite (NNNN tests)"
    content = re.sub(
        r"(suite\s*\()[\d,]+(\s+tests?\))",
        rf"\g<1>{vals['count_comma']}\2",
        content,
    )

    # "update test count to NNNN"
    content = re.sub(
        r"(update test count to\s+)[\d,]+",
        rf"\g<1>{vals['count_comma']}",
        content,
    )

    # "tests/ for NNNN examples"
    content = re.sub(
        r"(tests/[`'\"]?\s+for\s+)[\d,]+(\s+examples?\b)",
        rf"\g<1>{vals['count_comma']}\2",
        content,
    )

    # "# NNNN tests" in pytest comments
    content = re.sub(
        r"(#\s+)[\d,]+(\s+tests\b(?:\s*\(|\s*$))",
        rf"\g<1>{vals['count_comma']}\2",
        content,
    )

    if content != original:
        filepath.write_text(content, encoding="utf-8")
        print(f"  ✓ Updated {filepath.relative_to(_REPO_ROOT)}")
        return True
    return False


# ── Master file list ─────────────────────────────────────────────


def _files_to_update() -> list[Path]:
    """All files that may contain test count references."""
    return [
        # Core documentation
        _REPO_ROOT / "README.md",
        _REPO_ROOT / "README_PYPI.md",
        _REPO_ROOT / "CONTRIBUTING.md",
        _REPO_ROOT / "COMMIT_PROTOCOL.md",
        _REPO_ROOT / "QUICKSTART_TUTORIAL.md",
        # Agent instructions
        _REPO_ROOT / ".github" / "copilot-instructions.md",
        _REPO_ROOT / "AGENTS.md",
        _REPO_ROOT / "CLAUDE.md",
        # Web
        _REPO_ROOT / "web" / "src" / "pages" / "about.astro",
        _REPO_ROOT / "web" / "src" / "layouts" / "IndexLayout.astro",
    ]


def main() -> int:
    """Update test counts across the entire repository."""
    # 1) Collect actual count
    print("Collecting tests via pytest...")
    test_count = get_test_count()
    test_files_top = count_test_files()
    test_files_closure = count_closure_test_files()

    if test_count == 0:
        print("Error: No tests collected. Is pytest installed?", file=sys.stderr)
        return 1

    # 2) Read previous canonical count for pattern matching
    old_count = read_canonical_count()
    old_count_comma = f"{old_count:,}" if old_count > 0 else ""
    old_count_url = old_count_comma.replace(",", "%2C") if old_count_comma else ""

    # 3) Write new canonical count
    write_canonical_count(test_count)
    print(f"Canonical count: {test_count:,} tests ({test_files_top} top-level + {test_files_closure} closure files)")

    if old_count == test_count:
        print("Count unchanged — scanning for any stale references anyway.")

    # 4) Build replacement values
    vals = _build_replacements(test_count, test_files_top, test_files_closure)

    # 5) Sweep all target files
    updated_any = False
    for filepath in _files_to_update():
        if old_count_comma:
            if update_file(filepath, old_count_comma, old_count_url, vals):
                updated_any = True
        else:
            # No previous count — still try targeted patterns
            if update_file(filepath, "NEVER_MATCH_SENTINEL", "NEVER_MATCH_SENTINEL", vals):
                updated_any = True

    if updated_any:
        print(f"\n✓ Test count synced to {test_count:,} across all files")
    else:
        print("\nAll files already up to date")

    print(f"Found {test_count} tests")
    return 0


if __name__ == "__main__":
    sys.exit(main())
