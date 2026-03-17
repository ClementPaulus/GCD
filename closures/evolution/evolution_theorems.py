"""
Evolution Theorems — 10 Proven Theorems (T-EV-1 through T-EV-10)

Unified theorem module bridging evolution_kernel (40 organisms),
brain_kernel (19 brains), recursive_evolution scales (5) and extinctions (5).

═══════════════════════════════════════════════════════════════════════
THEOREM INDEX
═══════════════════════════════════════════════════════════════════════
  T-EV-1   Tier-1 Kernel Identities — F+ω=1, IC≤F, IC=exp(κ) for all organisms
  T-EV-2   Organism Universal Collapse — All 40 organisms in Collapse regime
  T-EV-3   Brain Coherence Singularity — Homo sapiens sole Watch brain
  T-EV-4   Extinction Severity Ordering — End-Permian worst F_drop
  T-EV-5   Kingdom Fidelity Ordering — Animalia highest mean organism F
  T-EV-6   Scale Hierarchy — Gene scale sole Watch; all others Collapse
  T-EV-7   Cognitive Fidelity Premium — Sapiens tops organism F ranking
  T-EV-8   Extinction IC Amplification — IC_drop_pct > F_drop_pct in severe events
  T-EV-9   Dodo Vulnerability Floor — Dodo has lowest organism fidelity
  T-EV-10  Cross-Module Consistency — Entity counts consistent across modules

Derivation chain: Axiom-0 → frozen_contract → kernel_optimized → evolution_kernel/brain/recursive → this
"""

from __future__ import annotations

import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np

_WORKSPACE = Path(__file__).resolve().parents[2]
if str(_WORKSPACE / "src") not in sys.path:
    sys.path.insert(0, str(_WORKSPACE / "src"))
if str(_WORKSPACE) not in sys.path:
    sys.path.insert(0, str(_WORKSPACE))

from closures.evolution.brain_kernel import compute_all_brains  # noqa: E402
from closures.evolution.evolution_kernel import compute_all_organisms  # noqa: E402
from closures.evolution.recursive_evolution import (  # noqa: E402
    MASS_EXTINCTIONS,
    compute_all_scales,
    compute_extinction_kernel,
)


@dataclass(frozen=True, slots=True)
class TheoremResult:
    """Result of a theorem proof attempt."""

    name: str
    statement: str
    n_tests: int
    n_passed: int
    n_failed: int
    details: dict[str, Any]
    verdict: str  # "PROVEN" or "FALSIFIED"


# ── Cache ──────────────────────────────────────────────────────────

_CACHE: dict[str, Any] = {}


def _get_organisms() -> list:
    if "organisms" not in _CACHE:
        _CACHE["organisms"] = compute_all_organisms()
    return _CACHE["organisms"]


def _get_brains() -> list:
    if "brains" not in _CACHE:
        _CACHE["brains"] = compute_all_brains()
    return _CACHE["brains"]


def _get_scales() -> list:
    if "scales" not in _CACHE:
        _CACHE["scales"] = compute_all_scales()
    return _CACHE["scales"]


def _get_extinctions() -> list:
    if "extinctions" not in _CACHE:
        _CACHE["extinctions"] = [compute_extinction_kernel(e) for e in MASS_EXTINCTIONS]
    return _CACHE["extinctions"]


# ═════════════════════════════════════════════════════════════════════
# THEOREM T-EV-1: Tier-1 Kernel Identities
# ═════════════════════════════════════════════════════════════════════


def theorem_EV1_kernel_identities() -> TheoremResult:
    """T-EV-1: All evolution organisms satisfy Tier-1 kernel identities."""
    organisms = _get_organisms()
    tests_total = 0
    tests_passed = 0
    details: dict[str, Any] = {}

    for org in organisms:
        # Duality: F + ω = 1
        tests_total += 1
        tests_passed += int(abs(org.F + org.omega - 1.0) < 1e-12)

        # Integrity bound: IC ≤ F
        tests_total += 1
        tests_passed += int(org.IC <= org.F + 1e-12)

        # Log-integrity: IC = exp(κ)
        tests_total += 1
        tests_passed += int(abs(org.IC - float(np.exp(org.kappa))) < 1e-10)

    details["n_organisms"] = len(organisms)
    details["tests_per_organism"] = 3

    return TheoremResult(
        name="T-EV-1: Tier-1 Kernel Identities",
        statement="F+ω=1, IC≤F, IC=exp(κ) hold for all 40 organisms",
        n_tests=tests_total,
        n_passed=tests_passed,
        n_failed=tests_total - tests_passed,
        details=details,
        verdict="PROVEN" if tests_passed == tests_total else "FALSIFIED",
    )


# ═════════════════════════════════════════════════════════════════════
# THEOREM T-EV-2: Organism Universal Collapse
# ═════════════════════════════════════════════════════════════════════


def theorem_EV2_universal_collapse() -> TheoremResult:
    """T-EV-2: All 40 organisms are in Collapse regime."""
    organisms = _get_organisms()
    tests_total = 0
    tests_passed = 0
    details: dict[str, Any] = {}

    collapse_count = sum(1 for o in organisms if o.regime == "Collapse")
    details["collapse_count"] = collapse_count
    details["total_organisms"] = len(organisms)

    # Test: All organisms are Collapse
    tests_total += 1
    tests_passed += int(collapse_count == len(organisms))

    # Test: No Stable organisms
    tests_total += 1
    stable_count = sum(1 for o in organisms if o.regime == "Stable")
    tests_passed += int(stable_count == 0)
    details["stable_count"] = stable_count

    # Test: No Watch organisms
    tests_total += 1
    watch_count = sum(1 for o in organisms if o.regime == "Watch")
    tests_passed += int(watch_count == 0)
    details["watch_count"] = watch_count

    return TheoremResult(
        name="T-EV-2: Organism Universal Collapse",
        statement="All 40 organisms are in Collapse regime",
        n_tests=tests_total,
        n_passed=tests_passed,
        n_failed=tests_total - tests_passed,
        details=details,
        verdict="PROVEN" if tests_passed == tests_total else "FALSIFIED",
    )


# ═════════════════════════════════════════════════════════════════════
# THEOREM T-EV-3: Brain Coherence Singularity
# ═════════════════════════════════════════════════════════════════════


def theorem_EV3_brain_singularity() -> TheoremResult:
    """T-EV-3: Homo sapiens is the sole Watch-regime brain."""
    brains = _get_brains()
    tests_total = 0
    tests_passed = 0
    details: dict[str, Any] = {}

    watch_brains = [b for b in brains if b.regime == "Watch"]
    collapse_brains = [b for b in brains if b.regime == "Collapse"]
    details["n_brains"] = len(brains)
    details["watch_count"] = len(watch_brains)
    details["collapse_count"] = len(collapse_brains)

    # Test: Exactly 1 Watch brain
    tests_total += 1
    tests_passed += int(len(watch_brains) == 1)

    # Test: The Watch brain is Homo sapiens
    tests_total += 1
    is_sapiens = len(watch_brains) == 1 and watch_brains[0].species == "Homo sapiens"
    tests_passed += int(is_sapiens)

    # Test: Homo sapiens brain F > 0.90
    tests_total += 1
    sapiens = [b for b in brains if b.species == "Homo sapiens"]
    high_f = len(sapiens) == 1 and sapiens[0].F > 0.90
    tests_passed += int(high_f)
    if sapiens:
        details["sapiens_F"] = round(sapiens[0].F, 4)

    # Test: All non-sapiens brains are Collapse
    tests_total += 1
    others_collapse = all(b.regime == "Collapse" for b in brains if b.species != "Homo sapiens")
    tests_passed += int(others_collapse)

    return TheoremResult(
        name="T-EV-3: Brain Coherence Singularity",
        statement="Homo sapiens is the sole Watch-regime brain (F > 0.90)",
        n_tests=tests_total,
        n_passed=tests_passed,
        n_failed=tests_total - tests_passed,
        details=details,
        verdict="PROVEN" if tests_passed == tests_total else "FALSIFIED",
    )


# ═════════════════════════════════════════════════════════════════════
# THEOREM T-EV-4: Extinction Severity Ordering
# ═════════════════════════════════════════════════════════════════════


def theorem_EV4_extinction_severity() -> TheoremResult:
    """T-EV-4: End-Permian has the worst F_drop among mass extinctions."""
    extinctions = _get_extinctions()
    tests_total = 0
    tests_passed = 0
    details: dict[str, Any] = {}

    # Sort by F_drop_pct descending
    sorted_ext = sorted(extinctions, key=lambda e: e.F_drop_pct, reverse=True)

    # Test: End-Permian has the highest F_drop_pct
    tests_total += 1
    permian_top = sorted_ext[0].name == "End-Permian"
    tests_passed += int(permian_top)
    details["worst_event"] = sorted_ext[0].name
    details["worst_F_drop_pct"] = round(sorted_ext[0].F_drop_pct, 1)

    # Test: End-Permian F_drop > 70%
    tests_total += 1
    permian = next(e for e in extinctions if e.name == "End-Permian")
    severe = permian.F_drop_pct > 70.0
    tests_passed += int(severe)

    # Test: All extinctions show F_drop > 0
    tests_total += 1
    all_drop = all(e.F_drop_pct > 0.0 for e in extinctions)
    tests_passed += int(all_drop)

    # Test: All post-extinction F values are lower than pre-extinction
    tests_total += 1
    all_lower = all(e.post_F < e.pre_F for e in extinctions)
    tests_passed += int(all_lower)

    for e in extinctions:
        details[f"{e.name}_F_drop"] = round(e.F_drop_pct, 1)

    return TheoremResult(
        name="T-EV-4: Extinction Severity Ordering",
        statement="End-Permian has the highest F_drop (>70%) among mass extinctions",
        n_tests=tests_total,
        n_passed=tests_passed,
        n_failed=tests_total - tests_passed,
        details=details,
        verdict="PROVEN" if tests_passed == tests_total else "FALSIFIED",
    )


# ═════════════════════════════════════════════════════════════════════
# THEOREM T-EV-5: Kingdom Fidelity Ordering
# ═════════════════════════════════════════════════════════════════════


def theorem_EV5_kingdom_ordering() -> TheoremResult:
    """T-EV-5: Animalia has the highest mean organism fidelity."""
    organisms = _get_organisms()
    tests_total = 0
    tests_passed = 0
    details: dict[str, Any] = {}

    by_kingdom: dict[str, list[float]] = {}
    for org in organisms:
        k = org.kingdom
        by_kingdom.setdefault(k, []).append(org.F)

    kingdom_means = {k: float(np.mean(fs)) for k, fs in by_kingdom.items()}
    for k, m in sorted(kingdom_means.items(), key=lambda x: -x[1]):
        details[f"{k}_mean_F"] = round(m, 4)

    # Test: Animalia has the highest mean F
    tests_total += 1
    animalia_top = kingdom_means.get("Animalia", 0) == max(kingdom_means.values())
    tests_passed += int(animalia_top)

    # Test: At least 4 kingdoms present
    tests_total += 1
    enough = len(kingdom_means) >= 4
    tests_passed += int(enough)
    details["n_kingdoms"] = len(kingdom_means)

    # Test: All kingdom means are positive
    tests_total += 1
    all_pos = all(m > 0.0 for m in kingdom_means.values())
    tests_passed += int(all_pos)

    return TheoremResult(
        name="T-EV-5: Kingdom Fidelity Ordering",
        statement="Animalia has the highest mean organism fidelity across kingdoms",
        n_tests=tests_total,
        n_passed=tests_passed,
        n_failed=tests_total - tests_passed,
        details=details,
        verdict="PROVEN" if tests_passed == tests_total else "FALSIFIED",
    )


# ═════════════════════════════════════════════════════════════════════
# THEOREM T-EV-6: Scale Hierarchy
# ═════════════════════════════════════════════════════════════════════


def theorem_EV6_scale_hierarchy() -> TheoremResult:
    """T-EV-6: Gene scale is the sole Watch-regime scale; all others Collapse."""
    scales = _get_scales()
    tests_total = 0
    tests_passed = 0
    details: dict[str, Any] = {}

    watch_scales = [s for s in scales if s.regime == "Watch"]
    collapse_scales = [s for s in scales if s.regime == "Collapse"]
    details["n_scales"] = len(scales)
    details["watch_count"] = len(watch_scales)
    details["collapse_count"] = len(collapse_scales)

    # Test: Exactly 1 Watch scale
    tests_total += 1
    tests_passed += int(len(watch_scales) == 1)

    # Test: The Watch scale is Gene
    tests_total += 1
    gene_watch = len(watch_scales) == 1 and watch_scales[0].scale_name == "Gene"
    tests_passed += int(gene_watch)

    # Test: All non-Gene scales are Collapse
    tests_total += 1
    others_collapse = len(collapse_scales) == len(scales) - 1
    tests_passed += int(others_collapse)

    # Test: Gene has highest F among scales
    tests_total += 1
    gene = [s for s in scales if s.scale_name == "Gene"]
    if gene:
        gene_top = max(s.F for s in scales) == gene[0].F
        tests_passed += int(gene_top)
        details["gene_F"] = round(gene[0].F, 4)
    else:
        details["gene_F"] = "NOT_FOUND"

    return TheoremResult(
        name="T-EV-6: Scale Hierarchy",
        statement="Gene is the sole Watch scale; all others Collapse",
        n_tests=tests_total,
        n_passed=tests_passed,
        n_failed=tests_total - tests_passed,
        details=details,
        verdict="PROVEN" if tests_passed == tests_total else "FALSIFIED",
    )


# ═════════════════════════════════════════════════════════════════════
# THEOREM T-EV-7: Cognitive Fidelity Premium
# ═════════════════════════════════════════════════════════════════════


def theorem_EV7_cognitive_premium() -> TheoremResult:
    """T-EV-7: Homo sapiens has the highest organism fidelity."""
    organisms = _get_organisms()
    tests_total = 0
    tests_passed = 0
    details: dict[str, Any] = {}

    # Sort by F descending
    sorted_orgs = sorted(organisms, key=lambda o: o.F, reverse=True)
    top = sorted_orgs[0]
    details["top_organism"] = top.name
    details["top_F"] = round(top.F, 4)

    # Test: Homo sapiens has the highest F
    tests_total += 1
    sapiens_top = top.name == "Homo sapiens"
    tests_passed += int(sapiens_top)

    # Test: Homo sapiens F > 0.60
    tests_total += 1
    sapiens = [o for o in organisms if o.name == "Homo sapiens"]
    high_f = len(sapiens) == 1 and sapiens[0].F > 0.60
    tests_passed += int(high_f)

    # Test: F spread across organisms > 0.30
    tests_total += 1
    f_range = sorted_orgs[0].F - sorted_orgs[-1].F
    wide = f_range > 0.30
    tests_passed += int(wide)
    details["F_range"] = round(f_range, 4)

    return TheoremResult(
        name="T-EV-7: Cognitive Fidelity Premium",
        statement="Homo sapiens tops the organism fidelity ranking",
        n_tests=tests_total,
        n_passed=tests_passed,
        n_failed=tests_total - tests_passed,
        details=details,
        verdict="PROVEN" if tests_passed == tests_total else "FALSIFIED",
    )


# ═════════════════════════════════════════════════════════════════════
# THEOREM T-EV-8: Extinction IC Amplification
# ═════════════════════════════════════════════════════════════════════


def theorem_EV8_ic_amplification() -> TheoremResult:
    """T-EV-8: IC_drop_pct exceeds F_drop_pct in severe extinctions.

    STATEMENT: For extinctions with F_drop > 50%, IC_drop is even
    more severe, reflecting geometric slaughter of coherence.
    """
    extinctions = _get_extinctions()
    tests_total = 0
    tests_passed = 0
    details: dict[str, Any] = {}

    severe = [e for e in extinctions if e.F_drop_pct > 50.0]
    details["n_severe"] = len(severe)

    # Test: At least 2 severe extinctions (F_drop > 50%)
    tests_total += 1
    enough = len(severe) >= 2
    tests_passed += int(enough)

    # Test: For all severe extinctions, IC_drop_pct >= F_drop_pct
    tests_total += 1
    all_amplified = all(e.IC_drop_pct >= e.F_drop_pct for e in severe) if severe else False
    tests_passed += int(all_amplified)

    # Test: End-Permian IC_drop > 75%
    tests_total += 1
    permian = [e for e in extinctions if e.name == "End-Permian"]
    if permian:
        permian_ic_severe = permian[0].IC_drop_pct > 75.0
        tests_passed += int(permian_ic_severe)
        details["permian_IC_drop"] = round(permian[0].IC_drop_pct, 1)
        details["permian_F_drop"] = round(permian[0].F_drop_pct, 1)

    # Test: All extinctions have IC_drop > 0
    tests_total += 1
    all_ic_drop = all(e.IC_drop_pct > 0.0 for e in extinctions)
    tests_passed += int(all_ic_drop)

    return TheoremResult(
        name="T-EV-8: Extinction IC Amplification",
        statement="IC_drop exceeds F_drop in severe extinctions (geometric slaughter)",
        n_tests=tests_total,
        n_passed=tests_passed,
        n_failed=tests_total - tests_passed,
        details=details,
        verdict="PROVEN" if tests_passed == tests_total else "FALSIFIED",
    )


# ═════════════════════════════════════════════════════════════════════
# THEOREM T-EV-9: Dodo Vulnerability Floor
# ═════════════════════════════════════════════════════════════════════


def theorem_EV9_dodo_floor() -> TheoremResult:
    """T-EV-9: Dodo has the lowest organism fidelity."""
    organisms = _get_organisms()
    tests_total = 0
    tests_passed = 0
    details: dict[str, Any] = {}

    sorted_orgs = sorted(organisms, key=lambda o: o.F)
    bottom = sorted_orgs[0]
    details["bottom_organism"] = bottom.name
    details["bottom_F"] = round(bottom.F, 4)

    # Test: Dodo is at the bottom
    tests_total += 1
    dodo_bottom = "Dodo" in bottom.name
    tests_passed += int(dodo_bottom)

    # Test: Dodo F < 0.25
    tests_total += 1
    dodo = [o for o in organisms if "Dodo" in o.name]
    if dodo:
        low = dodo[0].F < 0.25
        tests_passed += int(low)
        details["dodo_F"] = round(dodo[0].F, 4)

    # Test: Dodo is in Collapse
    tests_total += 1
    if dodo:
        tests_passed += int(dodo[0].regime == "Collapse")

    return TheoremResult(
        name="T-EV-9: Dodo Vulnerability Floor",
        statement="Dodo has the lowest organism fidelity (F < 0.25)",
        n_tests=tests_total,
        n_passed=tests_passed,
        n_failed=tests_total - tests_passed,
        details=details,
        verdict="PROVEN" if tests_passed == tests_total else "FALSIFIED",
    )


# ═════════════════════════════════════════════════════════════════════
# THEOREM T-EV-10: Cross-Module Consistency
# ═════════════════════════════════════════════════════════════════════


def theorem_EV10_cross_module() -> TheoremResult:
    """T-EV-10: Entity counts are consistent across evolution modules."""
    organisms = _get_organisms()
    brains = _get_brains()
    scales = _get_scales()
    extinctions = _get_extinctions()

    tests_total = 0
    tests_passed = 0
    details: dict[str, Any] = {}

    details["n_organisms"] = len(organisms)
    details["n_brains"] = len(brains)
    details["n_scales"] = len(scales)
    details["n_extinctions"] = len(extinctions)

    # Test: 40 organisms
    tests_total += 1
    tests_passed += int(len(organisms) == 40)

    # Test: 19 brains
    tests_total += 1
    tests_passed += int(len(brains) == 19)

    # Test: 5 scales
    tests_total += 1
    tests_passed += int(len(scales) == 5)

    # Test: 5 extinctions
    tests_total += 1
    tests_passed += int(len(extinctions) == 5)

    # Test: Total entities >= 69
    tests_total += 1
    total = len(organisms) + len(brains) + len(scales) + len(extinctions)
    tests_passed += int(total >= 69)
    details["total_entities"] = total

    return TheoremResult(
        name="T-EV-10: Cross-Module Consistency",
        statement="Entity counts consistent: 40+19+5+5 = 69 across modules",
        n_tests=tests_total,
        n_passed=tests_passed,
        n_failed=tests_total - tests_passed,
        details=details,
        verdict="PROVEN" if tests_passed == tests_total else "FALSIFIED",
    )


# ═════════════════════════════════════════════════════════════════════
# Runner
# ═════════════════════════════════════════════════════════════════════

ALL_THEOREMS = [
    theorem_EV1_kernel_identities,
    theorem_EV2_universal_collapse,
    theorem_EV3_brain_singularity,
    theorem_EV4_extinction_severity,
    theorem_EV5_kingdom_ordering,
    theorem_EV6_scale_hierarchy,
    theorem_EV7_cognitive_premium,
    theorem_EV8_ic_amplification,
    theorem_EV9_dodo_floor,
    theorem_EV10_cross_module,
]


def run_all_theorems() -> list[TheoremResult]:
    """Run all 10 evolution theorems."""
    return [thm() for thm in ALL_THEOREMS]


if __name__ == "__main__":
    results = run_all_theorems()
    total_tests = sum(r.n_tests for r in results)
    total_passed = sum(r.n_passed for r in results)
    print(f"\nEvolution Theorems: {len(results)}/10")
    print(f"Total subtests: {total_passed}/{total_tests}")
    for r in results:
        status = "✓" if r.verdict == "PROVEN" else "✗"
        print(f"  {status} {r.name}: {r.n_passed}/{r.n_tests} — {r.verdict}")
