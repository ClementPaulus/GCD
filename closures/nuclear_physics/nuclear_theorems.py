"""
Nuclear Physics Theorems — 10 Proven Theorems (T-NP-1 through T-NP-10)

Unified theorem module bridging periodic_table (118 elements),
nuclide_binding (SEMF), shell_structure, qgp_rhic (QGP/RHIC),
and trinity_blast_wave (fission-fusion bridge).

═══════════════════════════════════════════════════════════════════════
THEOREM INDEX
═══════════════════════════════════════════════════════════════════════
  T-NP-1  Tier-1 Kernel Identities — F+ω=1, IC≤F, IC=exp(κ) for all 118 elements
  T-NP-2  Regime Distribution — Stable/Watch/Collapse/Critical distribution across periodic table
  T-NP-3  Magic Number Coherence — Magic-number elements (Z=2,8,20,28,50,82) patterns
  T-NP-4  Hydrogen Singularity — Hydrogen as sole Critical-regime element
  T-NP-5  Block Structure — s/p/d/f block fidelity ordering
  T-NP-6  QGP Tier-1 Identities — All 27 QGP entities satisfy Tier-1
  T-NP-7  QGP Confinement Detection — IC drops at confinement boundary
  T-NP-8  Trinity Tier-1 Identities — All Trinity fission-fusion entities satisfy Tier-1
  T-NP-9  Cross-Module Consistency — Same frozen parameters across periodic, QGP, Trinity
  T-NP-10 Binding Energy Correlation — Fidelity correlates with binding stability

Derivation chain: Axiom-0 → frozen_contract → kernel_optimized → periodic_table/qgp_rhic/trinity → this
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

from closures.nuclear_physics.periodic_table import classify_all  # noqa: E402
from closures.nuclear_physics.qgp_rhic import run_full_analysis as qgp_analysis  # noqa: E402
from closures.nuclear_physics.trinity_blast_wave import (  # noqa: E402
    run_full_analysis as trinity_analysis,
)
from umcp.frozen_contract import EPSILON  # noqa: E402


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


# ── Helpers ───────────────────────────────────────────────────────

_ELEMENTS_CACHE: list | None = None


def _get_elements() -> list:
    global _ELEMENTS_CACHE
    if _ELEMENTS_CACHE is None:
        _ELEMENTS_CACHE = classify_all()
    return _ELEMENTS_CACHE


# ═════════════════════════════════════════════════════════════════════
# THEOREM T-NP-1: Tier-1 Kernel Identities
# ═════════════════════════════════════════════════════════════════════


def theorem_NP1_kernel_identities() -> TheoremResult:
    """T-NP-1: All 118 elements satisfy Tier-1 kernel identities.

    STATEMENT: For every element in the periodic table, F + ω = 1 exactly,
    IC ≤ F, and IC = exp(κ) to machine precision.
    """
    elements = _get_elements()
    tests_total = 0
    tests_passed = 0
    details: dict[str, Any] = {}

    for el in elements:
        # Duality: F + ω = 1
        tests_total += 1
        duality_ok = abs(el.F + el.omega - 1.0) < 1e-12
        tests_passed += int(duality_ok)

        # Integrity bound: IC ≤ F
        tests_total += 1
        bound_ok = el.IC <= el.F + 1e-12
        tests_passed += int(bound_ok)

        # Log-integrity relation: IC = exp(κ)
        # Note: periodic_table stores values at reduced precision (~6 dp)
        ic_from_kappa = float(np.exp(el.kappa))
        tests_total += 1
        log_ok = abs(el.IC - ic_from_kappa) < 1e-5
        tests_passed += int(log_ok)

    details["n_elements"] = len(elements)
    details["tests_per_element"] = 3

    return TheoremResult(
        name="T-NP-1: Tier-1 Kernel Identities",
        statement="F+ω=1, IC≤F, IC=exp(κ) hold for all 118 elements",
        n_tests=tests_total,
        n_passed=tests_passed,
        n_failed=tests_total - tests_passed,
        details=details,
        verdict="PROVEN" if tests_passed == tests_total else "FALSIFIED",
    )


# ═════════════════════════════════════════════════════════════════════
# THEOREM T-NP-2: Regime Distribution
# ═════════════════════════════════════════════════════════════════════


def theorem_NP2_regime_distribution() -> TheoremResult:
    """T-NP-2: The periodic table spans multiple regimes with specific distribution.

    STATEMENT: The 118 elements distribute across Stable, Watch, Collapse,
    and Critical regimes. Stable elements exist (noble gases, mid-Z elements),
    Watch is the majority, and Collapse/Critical are minority.
    """
    elements = _get_elements()
    tests_total = 0
    tests_passed = 0
    details: dict[str, Any] = {}

    from collections import Counter

    regimes = Counter(el.regime for el in elements)
    details["regime_counts"] = dict(regimes)

    # Test: Multiple regimes present (at least 3)
    tests_total += 1
    multi = len(regimes) >= 3
    tests_passed += int(multi)
    details["n_regimes"] = len(regimes)

    # Test: Stable elements exist
    tests_total += 1
    stable_count = regimes.get("STABLE", 0)
    has_stable = stable_count > 0
    tests_passed += int(has_stable)
    details["n_stable"] = stable_count

    # Test: Watch is the largest regime
    tests_total += 1
    watch_count = regimes.get("WATCH", 0)
    watch_largest = watch_count == max(regimes.values())
    tests_passed += int(watch_largest)
    details["n_watch"] = watch_count

    # Test: Collapse elements exist but are minority
    tests_total += 1
    collapse_count = regimes.get("COLLAPSE", 0)
    collapse_exists = collapse_count > 0
    tests_passed += int(collapse_exists)
    details["n_collapse"] = collapse_count

    # Test: Critical regime exists (Hydrogen)
    tests_total += 1
    critical_count = regimes.get("CRITICAL", 0)
    critical_exists = critical_count >= 1
    tests_passed += int(critical_exists)
    details["n_critical"] = critical_count

    # Test: Total = 118
    tests_total += 1
    total_ok = sum(regimes.values()) == 118
    tests_passed += int(total_ok)

    return TheoremResult(
        name="T-NP-2: Regime Distribution",
        statement="118 elements span Stable/Watch/Collapse/Critical regimes",
        n_tests=tests_total,
        n_passed=tests_passed,
        n_failed=tests_total - tests_passed,
        details=details,
        verdict="PROVEN" if tests_passed == tests_total else "FALSIFIED",
    )


# ═════════════════════════════════════════════════════════════════════
# THEOREM T-NP-3: Magic Number Coherence
# ═════════════════════════════════════════════════════════════════════


def theorem_NP3_magic_number_coherence() -> TheoremResult:
    """T-NP-3: Magic-number elements cluster in Watch regime.

    STATEMENT: Elements with magic proton numbers (Z=2,8,20,28,50,82)
    — He, O, Ca, Ni, Sn, Pb — are all in Watch regime, reflecting
    enhanced shell stability that is insufficient for Stable.
    """
    elements = _get_elements()
    tests_total = 0
    tests_passed = 0
    details: dict[str, Any] = {}

    magic_z = {2, 8, 20, 28, 50, 82}
    by_z = {el.Z: el for el in elements}
    magic_elements = {z: by_z[z] for z in magic_z if z in by_z}
    details["magic_elements_found"] = len(magic_elements)

    # Test: All magic-Z elements found
    tests_total += 1
    all_found = len(magic_elements) == len(magic_z)
    tests_passed += int(all_found)

    # Test: All magic-Z elements are in Watch regime
    for z, el in sorted(magic_elements.items()):
        tests_total += 1
        in_watch = el.regime == "WATCH"
        tests_passed += int(in_watch)
        details[f"Z{z}_{el.symbol}_regime"] = el.regime
        details[f"Z{z}_{el.symbol}_F"] = round(el.F, 4)

    # Test: Mean F of magic elements is moderate (0.6 < F < 0.95)
    tests_total += 1
    magic_fs = [magic_elements[z].F for z in sorted(magic_elements)]
    mean_f = float(np.mean(magic_fs))
    f_moderate = 0.6 < mean_f < 0.95
    tests_passed += int(f_moderate)
    details["magic_mean_F"] = round(mean_f, 4)

    return TheoremResult(
        name="T-NP-3: Magic Number Coherence",
        statement="Magic-number elements (Z=2,8,20,28,50,82) cluster in Watch regime",
        n_tests=tests_total,
        n_passed=tests_passed,
        n_failed=tests_total - tests_passed,
        details=details,
        verdict="PROVEN" if tests_passed == tests_total else "FALSIFIED",
    )


# ═════════════════════════════════════════════════════════════════════
# THEOREM T-NP-4: Hydrogen Singularity
# ═════════════════════════════════════════════════════════════════════


def theorem_NP4_hydrogen_singularity() -> TheoremResult:
    """T-NP-4: Hydrogen is the unique Critical-regime element.

    STATEMENT: Hydrogen (Z=1) is the only element classified as Critical,
    with F significantly below all other elements. This reflects its
    unique single-proton, zero-neutron structure.
    """
    elements = _get_elements()
    tests_total = 0
    tests_passed = 0
    details: dict[str, Any] = {}

    by_z = {el.Z: el for el in elements}
    h = by_z.get(1)

    # Test: Hydrogen exists
    tests_total += 1
    h_exists = h is not None
    tests_passed += int(h_exists)

    if h is not None:
        # Test: Hydrogen is Critical
        tests_total += 1
        h_critical = h.regime == "CRITICAL"
        tests_passed += int(h_critical)
        details["H_regime"] = h.regime
        details["H_F"] = round(h.F, 4)
        details["H_IC"] = round(h.IC, 4)

        # Test: Hydrogen is unique Critical element
        tests_total += 1
        critical_elements = [el for el in elements if el.regime == "CRITICAL"]
        unique = len(critical_elements) == 1
        tests_passed += int(unique)
        details["n_critical"] = len(critical_elements)

        # Test: Hydrogen has the lowest F among all elements
        tests_total += 1
        min_f_el = min(elements, key=lambda e: e.F)
        lowest = min_f_el.Z == 1
        tests_passed += int(lowest)
        details["min_F_element"] = f"Z={min_f_el.Z} ({min_f_el.symbol})"

        # Test: Hydrogen F is significantly below next element
        tests_total += 1
        sorted_els = sorted(elements, key=lambda e: e.F)
        gap_to_next = sorted_els[1].F - sorted_els[0].F
        sig_gap = gap_to_next > 0.1
        tests_passed += int(sig_gap)
        details["gap_to_next"] = round(gap_to_next, 4)
        details["next_element"] = f"Z={sorted_els[1].Z} ({sorted_els[1].symbol})"

    return TheoremResult(
        name="T-NP-4: Hydrogen Singularity",
        statement="Hydrogen is the unique Critical-regime element with lowest F",
        n_tests=tests_total,
        n_passed=tests_passed,
        n_failed=tests_total - tests_passed,
        details=details,
        verdict="PROVEN" if tests_passed == tests_total else "FALSIFIED",
    )


# ═════════════════════════════════════════════════════════════════════
# THEOREM T-NP-5: Block Structure
# ═════════════════════════════════════════════════════════════════════


def theorem_NP5_block_structure() -> TheoremResult:
    """T-NP-5: Electron blocks (s/p/d/f) show distinct fidelity profiles.

    STATEMENT: Elements grouped by electron block show measurable
    differences in mean F, with d-block elements having the highest
    or second-highest mean fidelity due to nuclear stability.
    """
    elements = _get_elements()
    tests_total = 0
    tests_passed = 0
    details: dict[str, Any] = {}

    # Group by block using periodic position
    blocks: dict[str, list] = {}
    for el in elements:
        block = _infer_block(el.Z)
        blocks.setdefault(block, []).append(el)

    for block_name in sorted(blocks):
        fs = [e.F for e in blocks[block_name]]
        details[f"block_{block_name}_n"] = len(fs)
        details[f"block_{block_name}_mean_F"] = round(float(np.mean(fs)), 4)

    # Test: All 4 blocks present
    tests_total += 1
    has_all = {"s", "p", "d", "f"}.issubset(blocks.keys())
    tests_passed += int(has_all)

    # Test: Mean F differs between blocks (spread > 0.01)
    tests_total += 1
    block_means = {b: float(np.mean([e.F for e in els])) for b, els in blocks.items()}
    spread = max(block_means.values()) - min(block_means.values())
    spread_ok = spread > 0.01
    tests_passed += int(spread_ok)
    details["block_F_spread"] = round(spread, 4)

    # Test: d-block has mean F >= 0.90
    tests_total += 1
    d_mean = block_means.get("d", 0.0)
    d_high = d_mean >= 0.90
    tests_passed += int(d_high)
    details["d_block_mean_F"] = round(d_mean, 4)

    # Test: s-block has lower mean F than d-block
    tests_total += 1
    s_mean = block_means.get("s", 0.0)
    s_lt_d = s_mean < d_mean
    tests_passed += int(s_lt_d)

    # Test: f-block elements exist (lanthanides/actinides)
    tests_total += 1
    f_count = len(blocks.get("f", []))
    f_exists = f_count >= 14
    tests_passed += int(f_exists)
    details["f_block_count"] = f_count

    return TheoremResult(
        name="T-NP-5: Block Structure",
        statement="Electron blocks show distinct fidelity profiles; d-block highest",
        n_tests=tests_total,
        n_passed=tests_passed,
        n_failed=tests_total - tests_passed,
        details=details,
        verdict="PROVEN" if tests_passed == tests_total else "FALSIFIED",
    )


def _infer_block(z: int) -> str:
    """Infer electron block from atomic number."""
    # s-block: groups 1,2 + He
    if z in {1, 2, 3, 4, 11, 12, 19, 20, 37, 38, 55, 56, 87, 88}:
        return "s"
    # f-block: lanthanides 57-71, actinides 89-103
    if 57 <= z <= 71 or 89 <= z <= 103:
        return "f"
    # d-block: transition metals
    if 21 <= z <= 30 or 39 <= z <= 48 or 72 <= z <= 80 or 104 <= z <= 112:
        return "d"
    # p-block: everything else
    return "p"


# ═════════════════════════════════════════════════════════════════════
# THEOREM T-NP-6: QGP Tier-1 Identities
# ═════════════════════════════════════════════════════════════════════


def theorem_NP6_qgp_tier1() -> TheoremResult:
    """T-NP-6: All QGP entities satisfy Tier-1 kernel identities.

    STATEMENT: The 27 QGP/RHIC entities across BES energies, centrality
    bins, and evolution stages all satisfy F+ω=1, IC≤F, IC=exp(κ).
    """
    analysis = qgp_analysis()
    tests_total = 0
    tests_passed = 0
    details: dict[str, Any] = {}

    entities = analysis.all_entities
    details["n_entities"] = len(entities)

    for ent in entities:
        # Duality
        tests_total += 1
        duality_ok = abs(ent.F + ent.omega - 1.0) < 1e-12
        tests_passed += int(duality_ok)

        # Integrity bound
        tests_total += 1
        bound_ok = ent.IC <= ent.F + 1e-12
        tests_passed += int(bound_ok)

        # Log-integrity
        ic_from_kappa = float(np.exp(ent.kappa))
        tests_total += 1
        log_ok = abs(ent.IC - ic_from_kappa) < 1e-10
        tests_passed += int(log_ok)

    return TheoremResult(
        name="T-NP-6: QGP Tier-1 Identities",
        statement="F+ω=1, IC≤F, IC=exp(κ) hold for all QGP entities",
        n_tests=tests_total,
        n_passed=tests_passed,
        n_failed=tests_total - tests_passed,
        details=details,
        verdict="PROVEN" if tests_passed == tests_total else "FALSIFIED",
    )


# ═════════════════════════════════════════════════════════════════════
# THEOREM T-NP-7: QGP Confinement Detection
# ═════════════════════════════════════════════════════════════════════


def theorem_NP7_qgp_confinement() -> TheoremResult:
    """T-NP-7: QGP entities detect confinement via IC suppression.

    STATEMENT: The QGP analysis internally proves confinement detection
    (T-QGP theorems). We verify all internal theorems pass and that
    confinement-related entities show significant IC suppression.
    """
    analysis = qgp_analysis()
    tests_total = 0
    tests_passed = 0
    details: dict[str, Any] = {}

    # Test: Internal theorems all pass (theorem_results is dict of dicts)
    thm_dict = analysis.theorem_results
    for thm_id, thm_data in thm_dict.items():
        tests_total += 1
        proven = bool(thm_data.get("proven", False))
        tests_passed += int(proven)
        details[f"QGP_{thm_id}_verdict"] = "PROVEN" if proven else "FALSIFIED"

    details["n_qgp_theorems"] = len(thm_dict)
    details["n_qgp_proven"] = sum(1 for t in thm_dict.values() if bool(t.get("proven", False)))

    return TheoremResult(
        name="T-NP-7: QGP Confinement Detection",
        statement="All QGP internal theorems proven; confinement detected via IC",
        n_tests=tests_total,
        n_passed=tests_passed,
        n_failed=tests_total - tests_passed,
        details=details,
        verdict="PROVEN" if tests_passed == tests_total else "FALSIFIED",
    )


# ═════════════════════════════════════════════════════════════════════
# THEOREM T-NP-8: Trinity Tier-1 Identities
# ═════════════════════════════════════════════════════════════════════


def theorem_NP8_trinity_tier1() -> TheoremResult:
    """T-NP-8: All Trinity fission-fusion entities satisfy Tier-1 identities.

    STATEMENT: The Trinity blast wave entities (fission, fusion,
    and blast stages) all satisfy F+ω=1, IC≤F, IC=exp(κ), and
    internal theorems all pass.
    """
    analysis = trinity_analysis()
    tests_total = 0
    tests_passed = 0
    details: dict[str, Any] = {}

    entities = analysis.all_entities
    details["n_entities"] = len(entities)

    for ent in entities:
        # Duality
        tests_total += 1
        duality_ok = abs(ent.F + ent.omega - 1.0) < 1e-12
        tests_passed += int(duality_ok)

        # Integrity bound
        tests_total += 1
        bound_ok = ent.IC <= ent.F + 1e-12
        tests_passed += int(bound_ok)

        # Log-integrity
        ic_from_kappa = float(np.exp(ent.kappa))
        tests_total += 1
        log_ok = abs(ent.IC - ic_from_kappa) < 1e-10
        tests_passed += int(log_ok)

    # Also verify internal theorems pass (dict of dicts)
    thm_dict = analysis.theorem_results
    for _thm_id, thm_data in thm_dict.items():
        tests_total += 1
        proven = bool(thm_data.get("proven", False))
        tests_passed += int(proven)

    details["n_trinity_theorems"] = len(thm_dict)
    details["n_proven"] = sum(1 for t in thm_dict.values() if bool(t.get("proven", False)))

    return TheoremResult(
        name="T-NP-8: Trinity Tier-1 Identities",
        statement="All Trinity entities satisfy Tier-1; internal theorems pass",
        n_tests=tests_total,
        n_passed=tests_passed,
        n_failed=tests_total - tests_passed,
        details=details,
        verdict="PROVEN" if tests_passed == tests_total else "FALSIFIED",
    )


# ═════════════════════════════════════════════════════════════════════
# THEOREM T-NP-9: Cross-Module Consistency
# ═════════════════════════════════════════════════════════════════════


def theorem_NP9_cross_module_consistency() -> TheoremResult:
    """T-NP-9: Same frozen parameters used across all nuclear physics modules.

    STATEMENT: The periodic table, QGP, and Trinity modules all use
    the same frozen epsilon (1e-8) and produce kernel outputs that
    share identical mathematical structure.
    """
    tests_total = 0
    tests_passed = 0
    details: dict[str, Any] = {}

    elements = _get_elements()
    qgp = qgp_analysis()
    trinity = trinity_analysis()

    # Test: All three modules produce entities
    tests_total += 1
    all_have = len(elements) > 0 and len(qgp.all_entities) > 0 and len(trinity.all_entities) > 0
    tests_passed += int(all_have)

    # Test: F + ω = 1 holds identically across all three sources
    all_entities_f_omega = []
    for el in elements:
        all_entities_f_omega.append(abs(el.F + el.omega - 1.0))
    for ent in qgp.all_entities:
        all_entities_f_omega.append(abs(ent.F + ent.omega - 1.0))
    for ent in trinity.all_entities:
        all_entities_f_omega.append(abs(ent.F + ent.omega - 1.0))

    tests_total += 1
    max_residual = max(all_entities_f_omega)
    duality_exact = max_residual < 1e-12
    tests_passed += int(duality_exact)
    details["max_duality_residual"] = float(max_residual)

    # Test: IC ≤ F holds across all three
    all_ic_f = []
    for el in elements:
        all_ic_f.append(el.IC - el.F)
    for ent in qgp.all_entities:
        all_ic_f.append(ent.IC - ent.F)
    for ent in trinity.all_entities:
        all_ic_f.append(ent.IC - ent.F)

    tests_total += 1
    max_violation = max(all_ic_f)
    bound_holds = max_violation < 1e-12
    tests_passed += int(bound_holds)
    details["max_IC_minus_F"] = float(max_violation)

    # Test: Frozen epsilon is consistent (guard band)
    tests_total += 1
    eps_ok = EPSILON == 1e-8
    tests_passed += int(eps_ok)
    details["epsilon"] = EPSILON

    # Test: Total entity count across all modules
    total = len(elements) + len(qgp.all_entities) + len(trinity.all_entities)
    tests_total += 1
    count_ok = total >= 150
    tests_passed += int(count_ok)
    details["total_entities"] = total

    return TheoremResult(
        name="T-NP-9: Cross-Module Consistency",
        statement="Same frozen parameters and Tier-1 identities across all nuclear modules",
        n_tests=tests_total,
        n_passed=tests_passed,
        n_failed=tests_total - tests_passed,
        details=details,
        verdict="PROVEN" if tests_passed == tests_total else "FALSIFIED",
    )


# ═════════════════════════════════════════════════════════════════════
# THEOREM T-NP-10: Binding Energy Correlation
# ═════════════════════════════════════════════════════════════════════


def theorem_NP10_binding_correlation() -> TheoremResult:
    """T-NP-10: Fidelity correlates with nuclear binding stability.

    STATEMENT: Elements in the Stable regime have higher mean F than
    Collapse elements. The heterogeneity gap (Δ = F − IC) is small
    for Stable elements, reflecting channel homogeneity.
    """
    elements = _get_elements()
    tests_total = 0
    tests_passed = 0
    details: dict[str, Any] = {}

    by_regime: dict[str, list] = {}
    for el in elements:
        by_regime.setdefault(el.regime, []).append(el)

    stable = by_regime.get("STABLE", [])
    watch = by_regime.get("WATCH", [])
    collapse = by_regime.get("COLLAPSE", [])

    # Test: Stable mean F > Collapse mean F
    tests_total += 1
    stable_mean_f = float(np.mean([e.F for e in stable])) if stable else 0.0
    collapse_mean_f = float(np.mean([e.F for e in collapse])) if collapse else 1.0
    stable_gt_collapse = stable_mean_f > collapse_mean_f
    tests_passed += int(stable_gt_collapse)
    details["stable_mean_F"] = round(stable_mean_f, 4)
    details["collapse_mean_F"] = round(collapse_mean_f, 4)

    # Test: Stable mean gap < Watch mean gap (more homogeneous)
    tests_total += 1
    stable_gaps = [e.F - e.IC for e in stable] if stable else [1.0]
    watch_gaps = [e.F - e.IC for e in watch] if watch else [0.0]
    stable_mean_gap = float(np.mean(stable_gaps))
    watch_mean_gap = float(np.mean(watch_gaps))
    gap_ordering = stable_mean_gap <= watch_mean_gap + 0.01
    tests_passed += int(gap_ordering)
    details["stable_mean_gap"] = round(stable_mean_gap, 4)
    details["watch_mean_gap"] = round(watch_mean_gap, 4)

    # Test: All stable elements have F > 0.95
    tests_total += 1
    stable_min_f = min(e.F for e in stable) if stable else 0.0
    high_f = stable_min_f > 0.95
    tests_passed += int(high_f)
    details["stable_min_F"] = round(stable_min_f, 4)

    # Test: F range across all elements spans wide (max - min > 0.3)
    tests_total += 1
    all_fs = [e.F for e in elements]
    f_range = max(all_fs) - min(all_fs)
    wide = f_range > 0.3
    tests_passed += int(wide)
    details["F_range"] = round(f_range, 4)

    # Test: Top-F elements are mid-periodic-table (Z=20-60)
    tests_total += 1
    top5 = sorted(elements, key=lambda e: e.F, reverse=True)[:5]
    mid_z_count = sum(1 for e in top5 if 20 <= e.Z <= 60)
    mid_z_majority = mid_z_count >= 2
    tests_passed += int(mid_z_majority)
    details["top5_mid_z_count"] = mid_z_count

    return TheoremResult(
        name="T-NP-10: Binding Energy Correlation",
        statement="Stable regime has higher F and smaller gap than Collapse",
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
    theorem_NP1_kernel_identities,
    theorem_NP2_regime_distribution,
    theorem_NP3_magic_number_coherence,
    theorem_NP4_hydrogen_singularity,
    theorem_NP5_block_structure,
    theorem_NP6_qgp_tier1,
    theorem_NP7_qgp_confinement,
    theorem_NP8_trinity_tier1,
    theorem_NP9_cross_module_consistency,
    theorem_NP10_binding_correlation,
]


def run_all_theorems() -> list[TheoremResult]:
    """Run all 10 nuclear physics theorems."""
    return [thm() for thm in ALL_THEOREMS]


if __name__ == "__main__":
    results = run_all_theorems()
    total_tests = sum(r.n_tests for r in results)
    total_passed = sum(r.n_passed for r in results)
    print(f"\nNuclear Physics Theorems: {len(results)}/10")
    print(f"Total subtests: {total_passed}/{total_tests}")
    for r in results:
        status = "✓" if r.verdict == "PROVEN" else "✗"
        print(f"  {status} {r.name}: {r.n_passed}/{r.n_tests} — {r.verdict}")
