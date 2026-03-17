"""
Astronomy Theorems — 10 Proven Theorems (T-AS-1 through T-AS-10)

Theorem module for the astronomy domain, built on cosmological epochs
(6 entities) from the cosmology closure.

═══════════════════════════════════════════════════════════════════════
THEOREM INDEX
═══════════════════════════════════════════════════════════════════════
  T-AS-1   Tier-1 Kernel Identities — F+ω=1, IC≤F, IC=exp(κ) for all epochs
  T-AS-2   Epoch Universal Collapse — All 6 cosmological epochs in Collapse
  T-AS-3   Present Epoch Fidelity Peak — Present (ΛCDM) has highest F
  T-AS-4   Inflation Exit IC Floor — Inflation exit has lowest IC
  T-AS-5   Curvature Dominance — All epochs show high curvature (C > 0.75)
  T-AS-6   Gap-IC Anticorrelation — Higher IC correlates with smaller gap
  T-AS-7   Entropy-Curvature Coupling — Negative C-S correlation across epochs
  T-AS-8   Duality Exactness — F+ω=1 to machine precision for all epochs
  T-AS-9   Kappa Ordering — All κ<0; Inflation exit most negative
  T-AS-10  Epoch Count and Coverage — 6 epochs span cosmic history

Derivation chain: Axiom-0 → frozen_contract → kernel_optimized → cosmology → this
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

from closures.astronomy.cosmology import compute_all_cosmological_epochs  # noqa: E402


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


def _get_epochs() -> list:
    if "epochs" not in _CACHE:
        _CACHE["epochs"] = compute_all_cosmological_epochs()
    return _CACHE["epochs"]


# ═════════════════════════════════════════════════════════════════════
# THEOREM T-AS-1: Tier-1 Kernel Identities
# ═════════════════════════════════════════════════════════════════════


def theorem_AS1_kernel_identities() -> TheoremResult:
    """T-AS-1: All cosmological epochs satisfy Tier-1 kernel identities."""
    epochs = _get_epochs()
    tests_total = 0
    tests_passed = 0
    details: dict[str, Any] = {}

    for ep in epochs:
        # Duality: F + ω = 1
        tests_total += 1
        tests_passed += int(abs(ep.F + ep.omega - 1.0) < 1e-12)

        # Integrity bound: IC ≤ F
        tests_total += 1
        tests_passed += int(ep.IC <= ep.F + 1e-12)

        # Log-integrity: IC = exp(κ)
        tests_total += 1
        tests_passed += int(abs(ep.IC - float(np.exp(ep.kappa))) < 1e-5)

    details["n_epochs"] = len(epochs)

    return TheoremResult(
        name="T-AS-1: Tier-1 Kernel Identities",
        statement="F+ω=1, IC≤F, IC=exp(κ) hold for all 6 cosmological epochs",
        n_tests=tests_total,
        n_passed=tests_passed,
        n_failed=tests_total - tests_passed,
        details=details,
        verdict="PROVEN" if tests_passed == tests_total else "FALSIFIED",
    )


# ═════════════════════════════════════════════════════════════════════
# THEOREM T-AS-2: Epoch Universal Collapse
# ═════════════════════════════════════════════════════════════════════


def theorem_AS2_universal_collapse() -> TheoremResult:
    """T-AS-2: All 6 cosmological epochs are in Collapse regime."""
    epochs = _get_epochs()
    tests_total = 0
    tests_passed = 0
    details: dict[str, Any] = {}

    collapse_count = sum(1 for e in epochs if e.regime == "Collapse")
    details["collapse_count"] = collapse_count
    details["total_epochs"] = len(epochs)

    # Test: All epochs are Collapse
    tests_total += 1
    tests_passed += int(collapse_count == len(epochs))

    # Test: All ω > 0.30 (Collapse threshold)
    tests_total += 1
    all_high_omega = all(e.omega > 0.30 for e in epochs)
    tests_passed += int(all_high_omega)

    return TheoremResult(
        name="T-AS-2: Epoch Universal Collapse",
        statement="All 6 cosmological epochs are in Collapse regime (ω > 0.30)",
        n_tests=tests_total,
        n_passed=tests_passed,
        n_failed=tests_total - tests_passed,
        details=details,
        verdict="PROVEN" if tests_passed == tests_total else "FALSIFIED",
    )


# ═════════════════════════════════════════════════════════════════════
# THEOREM T-AS-3: Present Epoch Fidelity Peak
# ═════════════════════════════════════════════════════════════════════


def theorem_AS3_present_fidelity_peak() -> TheoremResult:
    """T-AS-3: Present (ΛCDM) epoch has the highest fidelity."""
    epochs = _get_epochs()
    tests_total = 0
    tests_passed = 0
    details: dict[str, Any] = {}

    sorted_eps = sorted(epochs, key=lambda e: e.F, reverse=True)
    top = sorted_eps[0]
    details["top_epoch"] = top.epoch
    details["top_F"] = round(top.F, 4)

    # Test: Present (ΛCDM) is at the top
    tests_total += 1
    present_top = "Present" in top.epoch or "CDM" in top.epoch
    tests_passed += int(present_top)

    # Test: Present F > 0.64
    tests_total += 1
    present = [e for e in epochs if "Present" in e.epoch or "CDM" in e.epoch]
    if present:
        high = present[0].F > 0.64
        tests_passed += int(high)
        details["present_F"] = round(present[0].F, 4)

    # Test: Present has highest gap
    tests_total += 1
    max_gap = max(e.gap for e in epochs)
    present_highest_gap = present and abs(present[0].gap - max_gap) < 1e-10
    tests_passed += int(present_highest_gap)

    return TheoremResult(
        name="T-AS-3: Present Epoch Fidelity Peak",
        statement="Present (ΛCDM) has the highest F and gap among epochs",
        n_tests=tests_total,
        n_passed=tests_passed,
        n_failed=tests_total - tests_passed,
        details=details,
        verdict="PROVEN" if tests_passed == tests_total else "FALSIFIED",
    )


# ═════════════════════════════════════════════════════════════════════
# THEOREM T-AS-4: Inflation Exit IC Floor
# ═════════════════════════════════════════════════════════════════════


def theorem_AS4_inflation_ic_floor() -> TheoremResult:
    """T-AS-4: Inflation exit has the lowest IC among epochs."""
    epochs = _get_epochs()
    tests_total = 0
    tests_passed = 0
    details: dict[str, Any] = {}

    sorted_by_ic = sorted(epochs, key=lambda e: e.IC)
    bottom = sorted_by_ic[0]
    details["lowest_IC_epoch"] = bottom.epoch
    details["lowest_IC"] = round(bottom.IC, 6)

    # Test: Inflation exit is at the bottom
    tests_total += 1
    inflation_bottom = "Inflation" in bottom.epoch
    tests_passed += int(inflation_bottom)

    # Test: Inflation exit IC < 0.005
    tests_total += 1
    inflation = [e for e in epochs if "Inflation" in e.epoch]
    if inflation:
        low_ic = inflation[0].IC < 0.005
        tests_passed += int(low_ic)

    # Test: Inflation exit has highest curvature
    tests_total += 1
    max_c = max(e.C for e in epochs)
    inflation_highest_c = inflation and abs(inflation[0].C - max_c) < 0.01
    tests_passed += int(inflation_highest_c)

    return TheoremResult(
        name="T-AS-4: Inflation Exit IC Floor",
        statement="Inflation exit has lowest IC (<0.005) and highest curvature",
        n_tests=tests_total,
        n_passed=tests_passed,
        n_failed=tests_total - tests_passed,
        details=details,
        verdict="PROVEN" if tests_passed == tests_total else "FALSIFIED",
    )


# ═════════════════════════════════════════════════════════════════════
# THEOREM T-AS-5: Curvature Dominance
# ═════════════════════════════════════════════════════════════════════


def theorem_AS5_curvature_dominance() -> TheoremResult:
    """T-AS-5: All epochs show high curvature (C > 0.75)."""
    epochs = _get_epochs()
    tests_total = 0
    tests_passed = 0
    details: dict[str, Any] = {}

    curvatures = [e.C for e in epochs]
    details["min_C"] = round(min(curvatures), 4)
    details["max_C"] = round(max(curvatures), 4)
    details["mean_C"] = round(float(np.mean(curvatures)), 4)

    # Test: All C > 0.75
    tests_total += 1
    all_high = all(c > 0.75 for c in curvatures)
    tests_passed += int(all_high)

    # Test: Mean C > 0.80
    tests_total += 1
    mean_high = float(np.mean(curvatures)) > 0.80
    tests_passed += int(mean_high)

    # Test: C range is measurable (spread > 0.05)
    tests_total += 1
    c_range = max(curvatures) - min(curvatures)
    spread = c_range > 0.05
    tests_passed += int(spread)

    return TheoremResult(
        name="T-AS-5: Curvature Dominance",
        statement="All cosmological epochs have C > 0.75",
        n_tests=tests_total,
        n_passed=tests_passed,
        n_failed=tests_total - tests_passed,
        details=details,
        verdict="PROVEN" if tests_passed == tests_total else "FALSIFIED",
    )


# ═════════════════════════════════════════════════════════════════════
# THEOREM T-AS-6: Gap-IC Anticorrelation
# ═════════════════════════════════════════════════════════════════════


def theorem_AS6_gap_ic_anticorrelation() -> TheoremResult:
    """T-AS-6: Higher IC correlates with smaller heterogeneity gap."""
    epochs = _get_epochs()
    tests_total = 0
    tests_passed = 0
    details: dict[str, Any] = {}

    ics = np.array([e.IC for e in epochs])
    gaps = np.array([e.gap for e in epochs])

    # Spearman rank correlation
    from scipy.stats import spearmanr

    corr, _ = spearmanr(ics, gaps)
    details["spearman_rho"] = round(float(corr), 4)

    # Test: Negative correlation (IC up → gap down)
    tests_total += 1
    tests_passed += int(corr < 0)

    # Test: Correlation is strong (|ρ| > 0.5)
    tests_total += 1
    tests_passed += int(abs(corr) > 0.5)

    # Test: Epoch with max IC has smaller gap than epoch with min IC
    tests_total += 1
    max_ic_epoch = max(epochs, key=lambda e: e.IC)
    min_ic_epoch = min(epochs, key=lambda e: e.IC)
    tests_passed += int(max_ic_epoch.gap < min_ic_epoch.gap)

    return TheoremResult(
        name="T-AS-6: Gap-IC Anticorrelation",
        statement="Higher IC correlates with smaller gap (negative Spearman ρ)",
        n_tests=tests_total,
        n_passed=tests_passed,
        n_failed=tests_total - tests_passed,
        details=details,
        verdict="PROVEN" if tests_passed == tests_total else "FALSIFIED",
    )


# ═════════════════════════════════════════════════════════════════════
# THEOREM T-AS-7: Entropy-Curvature Coupling
# ═════════════════════════════════════════════════════════════════════


def theorem_AS7_entropy_curvature() -> TheoremResult:
    """T-AS-7: Epochs with higher curvature have lower entropy.

    STATEMENT: There is a negative correlation between C and S across
    cosmological epochs, consistent with the Tier-1 constraint S ≈ f(F,C).
    """
    epochs = _get_epochs()
    tests_total = 0
    tests_passed = 0
    details: dict[str, Any] = {}

    cs = [e.C for e in epochs]
    ss = [e.S for e in epochs]

    from scipy.stats import spearmanr

    corr, _ = spearmanr(cs, ss)
    details["spearman_C_S"] = round(float(corr), 4)

    # Test: Negative correlation between C and S
    tests_total += 1
    tests_passed += int(corr < 0)

    # Test: Epoch with highest C has lowest S
    tests_total += 1
    max_c_ep = max(epochs, key=lambda e: e.C)
    min_s_ep = min(epochs, key=lambda e: e.S)
    tests_passed += int(max_c_ep.epoch == min_s_ep.epoch)

    # Test: All S values are positive
    tests_total += 1
    tests_passed += int(all(s > 0 for s in ss))

    return TheoremResult(
        name="T-AS-7: Entropy-Curvature Coupling",
        statement="Negative correlation between C and S across epochs",
        n_tests=tests_total,
        n_passed=tests_passed,
        n_failed=tests_total - tests_passed,
        details=details,
        verdict="PROVEN" if tests_passed == tests_total else "FALSIFIED",
    )


# ═════════════════════════════════════════════════════════════════════
# THEOREM T-AS-8: Duality Exactness
# ═════════════════════════════════════════════════════════════════════


def theorem_AS8_duality_exactness() -> TheoremResult:
    """T-AS-8: F + ω = 1 holds to machine precision for all epochs."""
    epochs = _get_epochs()
    tests_total = 0
    tests_passed = 0
    details: dict[str, Any] = {}

    residuals = [abs(e.F + e.omega - 1.0) for e in epochs]
    max_r = max(residuals)
    details["max_residual"] = float(max_r)

    # Test: Max residual < 1e-14
    tests_total += 1
    tests_passed += int(max_r < 1e-14)

    # Test: All residuals < 1e-12
    tests_total += 1
    tests_passed += int(all(r < 1e-12 for r in residuals))

    # Test: All F in [0,1] and all ω in [0,1]
    tests_total += 1
    valid = all(0 <= e.F <= 1 and 0 <= e.omega <= 1 for e in epochs)
    tests_passed += int(valid)

    return TheoremResult(
        name="T-AS-8: Duality Exactness",
        statement="F+ω=1 to machine precision for all cosmological epochs",
        n_tests=tests_total,
        n_passed=tests_passed,
        n_failed=tests_total - tests_passed,
        details=details,
        verdict="PROVEN" if tests_passed == tests_total else "FALSIFIED",
    )


# ═════════════════════════════════════════════════════════════════════
# THEOREM T-AS-9: Kappa Ordering
# ═════════════════════════════════════════════════════════════════════


def theorem_AS9_kappa_ordering() -> TheoremResult:
    """T-AS-9: All epochs have negative κ, Inflation exit most negative.

    STATEMENT: κ < 0 for all epochs (IC < 1), and Inflation exit
    has the most negative κ, reflecting maximum incoherence.
    """
    epochs = _get_epochs()
    tests_total = 0
    tests_passed = 0
    details: dict[str, Any] = {}

    kappas = [(e.epoch, e.kappa) for e in epochs]
    details["kappas"] = {e: round(k, 4) for e, k in kappas}

    # Test: All κ < 0
    tests_total += 1
    all_neg = all(e.kappa < 0 for e in epochs)
    tests_passed += int(all_neg)

    # Test: Inflation exit has the most negative κ
    tests_total += 1
    most_neg = min(epochs, key=lambda e: e.kappa)
    tests_passed += int("Inflation" in most_neg.epoch)
    details["most_negative_kappa"] = most_neg.epoch

    # Test: κ range spans > 3.0
    tests_total += 1
    k_range = max(e.kappa for e in epochs) - min(e.kappa for e in epochs)
    tests_passed += int(k_range > 3.0)
    details["kappa_range"] = round(k_range, 4)

    return TheoremResult(
        name="T-AS-9: Kappa Ordering",
        statement="All κ<0; Inflation exit most negative (max incoherence)",
        n_tests=tests_total,
        n_passed=tests_passed,
        n_failed=tests_total - tests_passed,
        details=details,
        verdict="PROVEN" if tests_passed == tests_total else "FALSIFIED",
    )


# ═════════════════════════════════════════════════════════════════════
# THEOREM T-AS-10: Epoch Count and Coverage
# ═════════════════════════════════════════════════════════════════════


def theorem_AS10_coverage() -> TheoremResult:
    """T-AS-10: 6 epochs span cosmic history from inflation to present."""
    epochs = _get_epochs()
    tests_total = 0
    tests_passed = 0
    details: dict[str, Any] = {}

    details["n_epochs"] = len(epochs)
    epoch_names = [e.epoch for e in epochs]
    details["epochs"] = epoch_names

    # Test: Exactly 6 epochs
    tests_total += 1
    tests_passed += int(len(epochs) == 6)

    # Test: Contains inflation-related epoch
    tests_total += 1
    has_inflation = any("Inflation" in e.epoch for e in epochs)
    tests_passed += int(has_inflation)

    # Test: Contains present-related epoch
    tests_total += 1
    has_present = any("Present" in e.epoch or "CDM" in e.epoch for e in epochs)
    tests_passed += int(has_present)

    # Test: Contains CMB/recombination epoch
    tests_total += 1
    has_cmb = any("CMB" in e.epoch or "Recombination" in e.epoch for e in epochs)
    tests_passed += int(has_cmb)

    # Test: All epochs have valid kernel output (F in [0,1])
    tests_total += 1
    all_valid = all(0 <= e.F <= 1 for e in epochs)
    tests_passed += int(all_valid)

    return TheoremResult(
        name="T-AS-10: Epoch Count and Coverage",
        statement="6 epochs span cosmic history from inflation to present",
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
    theorem_AS1_kernel_identities,
    theorem_AS2_universal_collapse,
    theorem_AS3_present_fidelity_peak,
    theorem_AS4_inflation_ic_floor,
    theorem_AS5_curvature_dominance,
    theorem_AS6_gap_ic_anticorrelation,
    theorem_AS7_entropy_curvature,
    theorem_AS8_duality_exactness,
    theorem_AS9_kappa_ordering,
    theorem_AS10_coverage,
]


def run_all_theorems() -> list[TheoremResult]:
    """Run all 10 astronomy theorems."""
    return [thm() for thm in ALL_THEOREMS]


if __name__ == "__main__":
    results = run_all_theorems()
    total_tests = sum(r.n_tests for r in results)
    total_passed = sum(r.n_passed for r in results)
    print(f"\nAstronomy Theorems: {len(results)}/10")
    print(f"Total subtests: {total_passed}/{total_tests}")
    for r in results:
        status = "✓" if r.verdict == "PROVEN" else "✗"
        print(f"  {status} {r.name}: {r.n_passed}/{r.n_tests} — {r.verdict}")
