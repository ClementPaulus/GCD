#!/usr/bin/env python3
"""
Unified metrics updater — single source of truth for all project counts.

Computes live values from the repository, then sweeps every documentation,
web, paper, and instruction file to replace stale references.

Metrics computed:
  - closure_modules   (find closures/ -name "*.py", excl __init__/conftest)
  - domains           (directories under closures/, excl __pycache__)
  - lemmas            (highest Lemma N in KERNEL_SPECIFICATION.md)
  - identities        (count of identity entries in identity tables)
  - tests             (pytest --collect-only)
  - test_files        (count of test_*.py in tests/)
  - tracked_files     (from integrity/sha256.txt header)
  - bibliography      (count of @-entries in paper/Bibliography.bib)
  - casepacks         (directories under casepacks/)
  - contracts         (*.yaml files in contracts/)
  - schemas           (*.schema.json files in schemas/)
  - canon_files       (*.yaml files in canon/)
  - papers_tex        (*.tex files in paper/)
  - papers_md         (*.md files in paper/)
  - proven_theorems   (count of unique T-XX-N tags across closures/)

Usage:
    python scripts/update_metrics.py           # Compute + update all files
    python scripts/update_metrics.py --check   # Dry-run: report stale refs, exit 1 if any
    python scripts/update_metrics.py --json    # Emit metrics as JSON to stdout
    python scripts/update_metrics.py --skip-pytest  # Skip slow pytest collection
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import NamedTuple

# ── Repository root ──────────────────────────────────────────────
_REPO = Path(__file__).resolve().parent.parent


# ── Metric definition ────────────────────────────────────────────


class Metric(NamedTuple):
    """A single project-wide metric."""

    name: str
    value: int
    label: str  # human-readable label used in patterns


@dataclass
class MetricsSnapshot:
    """All live metrics computed from the repository."""

    closure_modules: int = 0
    domains: int = 0
    lemmas: int = 0
    identities: int = 0
    tests: int = 0
    test_files: int = 0
    test_files_closure: int = 0
    tracked_files: int = 0
    bibliography: int = 0
    casepacks: int = 0
    contracts: int = 0
    schemas: int = 0
    canon_files: int = 0
    papers_tex: int = 0
    papers_md: int = 0
    proven_theorems: int = 0
    c_assertions: int = 326  # stable — only changes with C code edits
    cpp_assertions: int = 434  # stable — only changes with C++ code edits

    def to_dict(self) -> dict[str, int]:
        return {k: v for k, v in self.__dict__.items() if isinstance(v, int)}

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=2)


# ── Metric computation ───────────────────────────────────────────


def _count_closure_modules() -> int:
    """Count Python modules in closures/ (excl __init__, conftest, __pycache__)."""
    return len(
        [
            f
            for f in _REPO.joinpath("closures").rglob("*.py")
            if f.name not in ("__init__.py", "conftest.py") and "__pycache__" not in f.parts
        ]
    )


def _count_domains() -> int:
    """Count domain directories under closures/."""
    return len([d for d in _REPO.joinpath("closures").iterdir() if d.is_dir() and d.name != "__pycache__"])


def _count_lemmas() -> int:
    """Get highest Lemma N from KERNEL_SPECIFICATION.md."""
    ks = _REPO / "KERNEL_SPECIFICATION.md"
    if not ks.exists():
        return 0
    text = ks.read_text(encoding="utf-8")
    nums = [int(m) for m in re.findall(r"Lemma\s+(\d+)", text)]
    return max(nums) if nums else 0


def _count_identities() -> int:
    """Count structural identities — stable at 44, verified by deep_diagnostic."""
    # These are formally proven in the identity verification scripts.
    # Count E-series (8) + B-series (12) + D-series (8) + N-series (16) = 44.
    # Rather than re-derive, read from a stable source.
    ks = _REPO / "KERNEL_SPECIFICATION.md"
    if not ks.exists():
        return 44
    text = ks.read_text(encoding="utf-8")
    # Look for "44 structural identities" or the identity count
    m = re.search(r"(\d+)\s+structural\s+identit", text)
    if m:
        return int(m.group(1))
    return 44


def _count_tests(skip_pytest: bool = False) -> tuple[int, int, int]:
    """Count tests via pytest --collect-only. Returns (total, top_files, closure_files)."""
    test_dir = _REPO / "tests"
    top_files = len(list(test_dir.glob("test_*.py"))) if test_dir.exists() else 0
    closure_dir = test_dir / "closures"
    closure_files = len(list(closure_dir.glob("test_*.py"))) if closure_dir.exists() else 0

    if skip_pytest:
        # Read from canonical count file
        count_file = _REPO / "scripts" / "test_count.txt"
        if count_file.exists():
            text = count_file.read_text(encoding="utf-8").strip()
            if text.isdigit():
                return int(text), top_files, closure_files
        return 0, top_files, closure_files

    try:
        result = subprocess.run(
            [sys.executable, "-m", "pytest", "--collect-only", "-q"],
            capture_output=True,
            text=True,
            timeout=180,
            cwd=str(_REPO),
        )
        for pattern in [r"(\d+)\s+tests?\s+collected", r"(\d+)\s+tests?"]:
            m = re.search(pattern, result.stdout)
            if m:
                count = int(m.group(1))
                # Write canonical count file
                (_REPO / "scripts" / "test_count.txt").write_text(f"{count}\n", encoding="utf-8")
                return count, top_files, closure_files
        # Fallback: count :: lines
        test_lines = [l for l in result.stdout.splitlines() if "::" in l and l.strip().startswith("tests/")]
        if test_lines:
            count = len(test_lines)
            (_REPO / "scripts" / "test_count.txt").write_text(f"{count}\n", encoding="utf-8")
            return count, top_files, closure_files
    except Exception as e:
        print(f"  Warning: pytest collection failed: {e}", file=sys.stderr)

    return 0, top_files, closure_files


def _count_tracked_files() -> int:
    """Read tracked file count from integrity/sha256.txt header."""
    sha = _REPO / "integrity" / "sha256.txt"
    if not sha.exists():
        return 0
    for line in sha.read_text(encoding="utf-8").splitlines()[:5]:
        m = re.search(r"Total files:\s*(\d+)", line)
        if m:
            return int(m.group(1))
    return 0


def _count_bibliography() -> int:
    """Count @-entries in paper/Bibliography.bib."""
    bib = _REPO / "paper" / "Bibliography.bib"
    if not bib.exists():
        return 0
    return len(re.findall(r"^@", bib.read_text(encoding="utf-8"), re.MULTILINE))


def _count_dir_entries(subdir: str, pattern: str) -> int:
    """Count files matching pattern in a subdirectory."""
    d = _REPO / subdir
    if not d.exists():
        return 0
    return len(list(d.glob(pattern)))


def _count_casepacks() -> int:
    """Count casepack directories."""
    d = _REPO / "casepacks"
    if not d.exists():
        return 0
    return len([x for x in d.iterdir() if x.is_dir()])


def _count_proven_theorems() -> int:
    """Count unique proven theorems across all closures.

    A theorem is counted if it appears as a T-XX-N tag in a closure file
    and the file contains 'proven' (case-insensitive) near that tag,
    indicating it has been validated.

    Falls back to counting unique T-XX-N tags in files that contain 'proven'.
    """
    proven_tags: set[str] = set()
    for f in _REPO.joinpath("closures").rglob("*.py"):
        if f.name.startswith("__") or f.name == "conftest.py":
            continue
        if "__pycache__" in f.parts:
            continue
        text = f.read_text(encoding="utf-8", errors="ignore")
        # Only count tags in files that actually prove things
        if re.search(r"proven|PROVEN|status.*proven", text, re.IGNORECASE):
            tags = re.findall(r"T-[A-Z]+-\d+", text)
            proven_tags.update(tags)
    return len(proven_tags)


def compute_metrics(*, skip_pytest: bool = False) -> MetricsSnapshot:
    """Compute all live metrics from the repository."""
    tests, top_files, closure_files = _count_tests(skip_pytest=skip_pytest)
    return MetricsSnapshot(
        closure_modules=_count_closure_modules(),
        domains=_count_domains(),
        lemmas=_count_lemmas(),
        identities=_count_identities(),
        tests=tests,
        test_files=top_files + closure_files,
        test_files_closure=closure_files,
        tracked_files=_count_tracked_files(),
        bibliography=_count_bibliography(),
        casepacks=_count_casepacks(),
        contracts=_count_dir_entries("contracts", "*.yaml"),
        schemas=_count_dir_entries("schemas", "*.schema.json"),
        canon_files=_count_dir_entries("canon", "*.yaml"),
        papers_tex=_count_dir_entries("paper", "*.tex"),
        papers_md=_count_dir_entries("paper", "*.md"),
        proven_theorems=_count_proven_theorems(),
    )


# ── Pattern-based file updater ───────────────────────────────────


@dataclass
class Replacement:
    """A regex pattern + replacement template for a single metric."""

    pattern: re.Pattern[str]
    template: str  # uses {value} placeholder
    metric_name: str


@dataclass
class FileTarget:
    """A file and its applicable replacement patterns."""

    path: Path
    replacements: list[Replacement] = field(default_factory=list)


def _build_replacements(m: MetricsSnapshot) -> list[Replacement]:
    """Build all regex replacement rules from current metrics."""
    rules: list[Replacement] = []

    def _add(name: str, pattern: str, template: str) -> None:
        rules.append(
            Replacement(
                pattern=re.compile(pattern),
                template=template,
                metric_name=name,
            )
        )

    # ── Closure modules ──────────────────────────────────────
    # "NNN closure modules" / "NNN closures" / "NNN closure" / "closures-NNN"
    _add("closure_modules", r"\b\d+(?:\s+closure\s+modules?\b|\s+closures?\b)", f"{m.closure_modules} closure modules")
    # Badge: closures-NNN-informational
    _add("closure_modules", r"closures-\d+-informational", f"closures-{m.closure_modules}-informational")
    # Astro stat: n: 'NNN', label: 'Closures'
    _add(
        "closure_modules",
        r"n:\s*['\"]?\d+['\"]?,\s*label:\s*['\"]Closures['\"]",
        f"n: '{m.closure_modules}', label: 'Closures'",
    )
    # LaTeX: NNN~closure modules / NNN~closures
    _add("closure_modules", r"\d+~closure\s+modules?", f"{m.closure_modules}~closure modules")
    # Table cell: "Closure modules & NNN"
    _add("closure_modules", r"Closure modules\s*&\s*\d+", f"Closure modules & {m.closure_modules}")
    # Bold formatted: text-amber/kernel-200 NNN for closures context
    _add(
        "closure_modules",
        r'(text-amber-\d+">)\d+(</div>\s*\n\s*<div[^>]*>Closure modules)',
        rf"\g<1>{m.closure_modules}\2",
    )

    # ── Domains ──────────────────────────────────────────────
    _add("domains", r"\b\d+\s+domains?\b", f"{m.domains} domains")
    _add("domains", r"n:\s*['\"]?\d+['\"]?,\s*label:\s*['\"]Domains['\"]", f"n: '{m.domains}', label: 'Domains'")
    _add("domains", r"\b\d+\s+scientific\s+domains?\b", f"{m.domains} scientific domains")

    # ── Lemmas ───────────────────────────────────────────────
    _add("lemmas", r"\b\d+\s+lemmas?\b", f"{m.lemmas} lemmas")
    _add("lemmas", r"\b\d+~(?:proven\s+)?lemmas?\b", f"{m.lemmas}~proven lemmas")

    # ── Structural identities ────────────────────────────────
    _add("identities", r"\b\d+\s+structural\s+identit(?:y|ies)\b", f"{m.identities} structural identities")
    _add("identities", r"Structural\s+identities\s*&\s*\d+", f"Structural identities & {m.identities}")

    # ── Tests (total count) ──────────────────────────────────
    if m.tests > 0:
        tc = f"{m.tests:,}"
        tc_url = tc.replace(",", "%2C")
        _add("tests", r"[\d,]+\s+tests\b", f"{tc} tests")
        # Badge: tests-NNN-brightgreen
        _add("tests", r"tests-[\d%2C]+-brightgreen", f"tests-{tc_url}-brightgreen")
        _add("tests", r"n:\s*['\"][\d,]+['\"],\s*label:\s*['\"]Tests['\"]", f"n: '{tc}', label: 'Tests'")
        # pytest comment: "Should show NNN tests"
        _add("tests", r"(Should\s+show\s+)[\d,]+(\s+tests?\b)", rf"\g<1>{tc}\2")
        # "tests: NNNN" in timeline JS data
        _add("tests_timeline", r"tests:\s*\d+,\s*domains:\s*\d+\s*\}", f"tests: {m.tests}, domains: {m.domains} }}")

    # ── Test files ───────────────────────────────────────────
    if m.test_files > 0:
        tf = str(m.test_files)
        _add("test_files", r"\b\d+\s+test\s+files\b", f"{tf} test files")
        _add("test_files", r"(across\s+)\*\*\d+\s+test\s+files\*\*", rf"\1**{tf} test files**")

    # ── Tracked files ────────────────────────────────────────
    _add("tracked_files", r"\b\d+\s+tracked\s+files\b", f"{m.tracked_files} tracked files")
    _add("tracked_files", r"Checksummed\s+\d+\s+files", f"Checksummed {m.tracked_files} files")

    # ── Bibliography ─────────────────────────────────────────
    _add("bibliography", r"\b\d+\s+entries\b", f"{m.bibliography} entries")
    _add("bibliography", r"\b\d+\s+bibliography\s+entries\b", f"{m.bibliography} bibliography entries")

    # ── Casepacks ────────────────────────────────────────────
    _add("casepacks", r"\b\d+\s+casepacks?\b", f"{m.casepacks} casepacks")
    _add("casepacks", r"\b\d+\s+casepack\s+manifests?\b", f"{m.casepacks} casepack manifests")
    _add(
        "casepacks", r"\b\d+\s+reproducible\s+validation\s+bundles?\b", f"{m.casepacks} reproducible validation bundles"
    )

    # ── Contracts ────────────────────────────────────────────
    _add(
        "contracts",
        r"\b\d+\s+versioned\s+mathematical\s+contracts?\b",
        f"{m.contracts} versioned mathematical contracts",
    )
    _add("contracts", r"\b\d+\s+mathematical\s+contracts?\b", f"{m.contracts} mathematical contracts")

    # ── Schemas ──────────────────────────────────────────────
    _add("schemas", r"\b\d+\s+JSON\s+Schema\b", f"{m.schemas} JSON Schema")

    # ── Canon files ──────────────────────────────────────────
    _add("canon_files", r"\b\d+\s+canonical\s+anchor\s+files?\b", f"{m.canon_files} canonical anchor files")

    # ── Papers ───────────────────────────────────────────────
    _add("papers_tex", r"\b\d+\s+LaTeX\s+papers?\b", f"{m.papers_tex} LaTeX papers")

    # ── Proven theorems ──────────────────────────────────────
    _add("proven_theorems", r"\b\d+\s+proven\s+theorems?\b", f"{m.proven_theorems} proven theorems")
    _add("proven_theorems", r"theorems-\d+[\d%2C]*_proven-", f"theorems-{m.proven_theorems}_proven-")

    return rules


# ── Target files ─────────────────────────────────────────────────

# Files excluded from metric updates (historical records, changelogs)
_EXCLUDED_PATTERNS = {
    "CHANGELOG.md",  # Historical — never rewrite past entries
    "archive/",  # Archived content
}


def _should_skip(path: Path) -> bool:
    """Check if a file should be excluded from updates."""
    rel = str(path.relative_to(_REPO))
    return any(exc in rel for exc in _EXCLUDED_PATTERNS)


def _target_files() -> list[Path]:
    """All files that may contain metric references."""
    targets: list[Path] = []

    # Core documentation
    for name in [
        "README.md",
        "README_PYPI.md",
        "CONTRIBUTING.md",
        "COMMIT_PROTOCOL.md",
        "QUICKSTART_TUTORIAL.md",
        "AXIOM.md",
        "pyproject.toml",
    ]:
        p = _REPO / name
        if p.exists():
            targets.append(p)

    # Agent instructions
    for name in [
        ".github/copilot-instructions.md",
        "AGENTS.md",
        "CLAUDE.md",
    ]:
        p = _REPO / name
        if p.exists():
            targets.append(p)

    # Web pages (Astro)
    web_src = _REPO / "web" / "src"
    if web_src.exists():
        for f in web_src.rglob("*.astro"):
            if not _should_skip(f):
                targets.append(f)
        for f in web_src.rglob("*.ts"):
            if not _should_skip(f):
                targets.append(f)

    # Papers (LaTeX)
    paper_dir = _REPO / "paper"
    if paper_dir.exists():
        for f in paper_dir.glob("*.tex"):
            if not _should_skip(f):
                targets.append(f)

    # Scripts that embed metrics in output
    for name in [
        "scripts/generate_diagrams.py",
    ]:
        p = _REPO / name
        if p.exists():
            targets.append(p)

    return sorted(set(targets))


# ── File sweep logic ─────────────────────────────────────────────


@dataclass
class UpdateResult:
    """Result of updating a single file."""

    path: Path
    changed: bool
    replacements_made: int = 0
    details: list[str] = field(default_factory=list)


def _apply_rules_to_file(
    filepath: Path,
    rules: list[Replacement],
    *,
    dry_run: bool = False,
) -> UpdateResult:
    """Apply all replacement rules to a single file."""
    result = UpdateResult(path=filepath, changed=False)

    content = filepath.read_text(encoding="utf-8")
    original = content

    for rule in rules:
        # Find all current matches
        matches = list(rule.pattern.finditer(content))
        if not matches:
            continue

        for match in reversed(matches):
            old_text = match.group(0)
            # Expand template — handle backreferences
            try:
                new_text = rule.pattern.sub(rule.template, old_text)
            except re.error:
                new_text = rule.template

            if old_text != new_text:
                result.replacements_made += 1
                result.details.append(f"  [{rule.metric_name}] {old_text!r} → {new_text!r}")

        # Apply replacement across entire content
        content = rule.pattern.sub(rule.template, content)

    if content != original:
        result.changed = True
        if not dry_run:
            filepath.write_text(content, encoding="utf-8")

    return result


# ── Safeguards ───────────────────────────────────────────────────


def _validate_metrics(m: MetricsSnapshot) -> list[str]:
    """Sanity-check metrics before applying updates."""
    warnings: list[str] = []
    if m.closure_modules < 50:
        warnings.append(f"closure_modules={m.closure_modules} seems too low (expected >50)")
    if m.domains < 10:
        warnings.append(f"domains={m.domains} seems too low (expected >10)")
    if m.lemmas < 40:
        warnings.append(f"lemmas={m.lemmas} seems too low (expected >40)")
    if m.tests > 0 and m.tests < 5000:
        warnings.append(f"tests={m.tests} seems too low (expected >5000)")
    if m.tracked_files < 100:
        warnings.append(f"tracked_files={m.tracked_files} seems too low (expected >100)")
    if m.bibliography < 50:
        warnings.append(f"bibliography={m.bibliography} seems too low (expected >50)")
    return warnings


# ── Main ─────────────────────────────────────────────────────────


def main() -> int:
    """Compute metrics and update all files."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Unified metrics updater — single source of truth for all project counts.",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Dry-run: report stale references without modifying files. Exit 1 if any found.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Emit computed metrics as JSON to stdout.",
    )
    parser.add_argument(
        "--skip-pytest",
        action="store_true",
        help="Skip pytest collection (use cached count from scripts/test_count.txt).",
    )
    args = parser.parse_args()

    print("Computing live metrics...")
    m = compute_metrics(skip_pytest=args.skip_pytest)

    if args.json:
        print(m.to_json())
        return 0

    # Display computed values
    print(f"\n{'─' * 50}")
    print(f"  closure_modules   = {m.closure_modules}")
    print(f"  domains           = {m.domains}")
    print(f"  lemmas            = {m.lemmas}")
    print(f"  identities        = {m.identities}")
    print(f"  tests             = {m.tests:,}")
    print(f"  test_files        = {m.test_files}")
    print(f"  tracked_files     = {m.tracked_files}")
    print(f"  bibliography      = {m.bibliography}")
    print(f"  casepacks         = {m.casepacks}")
    print(f"  contracts         = {m.contracts}")
    print(f"  schemas           = {m.schemas}")
    print(f"  canon_files       = {m.canon_files}")
    print(f"  papers_tex        = {m.papers_tex}")
    print(f"  papers_md         = {m.papers_md}")
    print(f"  proven_theorems   = {m.proven_theorems}")
    print(f"{'─' * 50}\n")

    # Sanity check
    warnings = _validate_metrics(m)
    if warnings:
        for w in warnings:
            print(f"  ⚠ {w}", file=sys.stderr)
        if args.check:
            print("Aborting --check due to metric warnings.", file=sys.stderr)
            return 2

    # Build replacement rules
    rules = _build_replacements(m)

    # Sweep files
    targets = _target_files()
    dry_run = args.check
    total_changes = 0
    changed_files: list[UpdateResult] = []

    mode = "Checking" if dry_run else "Updating"
    print(f"{mode} {len(targets)} files...")

    for filepath in targets:
        result = _apply_rules_to_file(filepath, rules, dry_run=dry_run)
        if result.changed:
            total_changes += result.replacements_made
            changed_files.append(result)
            rel = filepath.relative_to(_REPO)
            icon = "⚠" if dry_run else "✓"
            print(f"  {icon} {rel}  ({result.replacements_made} replacements)")
            for detail in result.details:
                print(detail)

    # Summary
    print()
    if total_changes == 0:
        print("✓ All files already up to date.")
        return 0

    if dry_run:
        print(f"⚠ Found {total_changes} stale references in {len(changed_files)} files.")
        print("  Run without --check to fix them.")
        return 1

    print(f"✓ Updated {total_changes} references in {len(changed_files)} files.")

    # Write metrics snapshot for reference
    snapshot_path = _REPO / "scripts" / "metrics_snapshot.json"
    snapshot_path.write_text(m.to_json() + "\n", encoding="utf-8")
    print("  Snapshot written to scripts/metrics_snapshot.json")

    return 0


if __name__ == "__main__":
    sys.exit(main())
