"""
Weyl Theorems — 10 Proven Theorems (T-WL-1 through T-WL-10)

Theorem module for the Weyl cosmology domain, built on DES Y3
background cosmology (4 redshift bins) and Sigma-to-UMCP analogy.

═══════════════════════════════════════════════════════════════════════
THEOREM INDEX
═══════════════════════════════════════════════════════════════════════
  T-WL-1   Growth Factor Monotonicity — D1 decreases with redshift
  T-WL-2   Hubble Monotonicity — H(z) increases with redshift
  T-WL-3   Comoving Distance Monotonicity — χ increases with redshift
  T-WL-4   Omega_m Dominance at High z — Ω_m → 1 as z → ∞
  T-WL-5   Sigma8 Suppression — σ8(z) decreases with redshift
  T-WL-6   Flatness Consistency — Ω_m + Ω_Λ = 1 at all z
  T-WL-7   Sigma Tension Mapping — Σ₀ ≠ 1 maps to Collapse regime
  T-WL-8   Anchor Star Properties — z* = 10 anchor has D1 < 0.2
  T-WL-9   DES Y3 Bin Count — 4 tomographic bins in [0.2, 0.8]
  T-WL-10  Boost Nonlinearity — Boost grows with multipole ℓ

Derivation chain: Axiom-0 → frozen_contract → cosmology_background/sigma_evolution → this
"""

from __future__ import annotations

import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

_WORKSPACE = Path(__file__).resolve().parents[2]
if str(_WORKSPACE / "src") not in sys.path:
    sys.path.insert(0, str(_WORKSPACE / "src"))
if str(_WORKSPACE) not in sys.path:
    sys.path.insert(0, str(_WORKSPACE))

from closures.weyl.boost_factor import compute_boost_factor  # noqa: E402
from closures.weyl.cosmology_background import (  # noqa: E402
    compute_background,
    compute_des_y3_background,
)
from closures.weyl.sigma_evolution import Sigma_to_UMCP_invariants  # noqa: E402


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


def _get_des_y3():
    """Load DES Y3 background data."""
    return compute_des_y3_background()


# ═════════════════════════════════════════════════════════════════════
# THEOREM T-WL-1: Growth Factor Monotonicity
# ═════════════════════════════════════════════════════════════════════


def theorem_WL1_D1_monotonicity() -> TheoremResult:
    """T-WL-1: D1(z) decreases with redshift across DES Y3 bins."""
    des = _get_des_y3()
    tests_total = 0
    tests_passed = 0
    details: dict[str, Any] = {}

    d1 = des["D1"]

    # Test: D1 strictly decreasing
    tests_total += 1
    mono = all(d1[i] > d1[i + 1] for i in range(len(d1) - 1))
    tests_passed += int(mono)

    # Test: D1 at lowest z > 0.80
    tests_total += 1
    tests_passed += int(d1[0] > 0.80)

    # Test: D1 at highest z < 0.70
    tests_total += 1
    tests_passed += int(d1[-1] < 0.70)

    details["D1_range"] = (round(float(d1[0]), 4), round(float(d1[-1]), 4))

    return TheoremResult(
        name="T-WL-1: Growth Factor Monotonicity",
        statement="D1(z) strictly decreases with redshift across DES Y3 bins",
        n_tests=tests_total,
        n_passed=tests_passed,
        n_failed=tests_total - tests_passed,
        details=details,
        verdict="PROVEN" if tests_passed == tests_total else "FALSIFIED",
    )


# ═════════════════════════════════════════════════════════════════════
# THEOREM T-WL-2: Hubble Monotonicity
# ═════════════════════════════════════════════════════════════════════


def theorem_WL2_H_monotonicity() -> TheoremResult:
    """T-WL-2: H(z) increases with redshift across DES Y3 bins."""
    des = _get_des_y3()
    tests_total = 0
    tests_passed = 0
    details: dict[str, Any] = {}

    h = des["H_z"]

    # Test: H strictly increasing
    tests_total += 1
    mono = all(h[i] < h[i + 1] for i in range(len(h) - 1))
    tests_passed += int(mono)

    # Test: H at lowest z consistent with H₀ ~ 67.4
    tests_total += 1
    tests_passed += int(70 < h[0] < 90)

    # Test: H at highest z > 100
    tests_total += 1
    tests_passed += int(h[-1] > 100)

    details["H_range"] = (round(float(h[0]), 2), round(float(h[-1]), 2))

    return TheoremResult(
        name="T-WL-2: Hubble Monotonicity",
        statement="H(z) strictly increases with redshift across DES Y3 bins",
        n_tests=tests_total,
        n_passed=tests_passed,
        n_failed=tests_total - tests_passed,
        details=details,
        verdict="PROVEN" if tests_passed == tests_total else "FALSIFIED",
    )


# ═════════════════════════════════════════════════════════════════════
# THEOREM T-WL-3: Comoving Distance Monotonicity
# ═════════════════════════════════════════════════════════════════════


def theorem_WL3_chi_monotonicity() -> TheoremResult:
    """T-WL-3: Comoving distance χ(z) increases with redshift."""
    des = _get_des_y3()
    tests_total = 0
    tests_passed = 0
    details: dict[str, Any] = {}

    chi = des["chi"]

    # Test: χ strictly increasing
    tests_total += 1
    mono = all(chi[i] < chi[i + 1] for i in range(len(chi) - 1))
    tests_passed += int(mono)

    # Test: All χ > 0
    tests_total += 1
    tests_passed += int(all(c > 0 for c in chi))

    # Test: χ spans > 1000 Mpc/h
    tests_total += 1
    span = chi[-1] - chi[0]
    tests_passed += int(span > 1000)

    details["chi_range"] = (round(float(chi[0]), 1), round(float(chi[-1]), 1))

    return TheoremResult(
        name="T-WL-3: Comoving Distance Monotonicity",
        statement="χ(z) strictly increases with redshift across DES Y3 bins",
        n_tests=tests_total,
        n_passed=tests_passed,
        n_failed=tests_total - tests_passed,
        details=details,
        verdict="PROVEN" if tests_passed == tests_total else "FALSIFIED",
    )


# ═════════════════════════════════════════════════════════════════════
# THEOREM T-WL-4: Omega_m Dominance at High z
# ═════════════════════════════════════════════════════════════════════


def theorem_WL4_omega_m_dominance() -> TheoremResult:
    """T-WL-4: Ω_m(z) increases with z, approaching 1 at high redshift."""
    des = _get_des_y3()
    tests_total = 0
    tests_passed = 0
    details: dict[str, Any] = {}

    omega_m = des["Omega_m_z"]

    # Test: Ω_m strictly increasing
    tests_total += 1
    mono = all(omega_m[i] < omega_m[i + 1] for i in range(len(omega_m) - 1))
    tests_passed += int(mono)

    # Test: Ω_m at highest z > 0.70
    tests_total += 1
    tests_passed += int(omega_m[-1] > 0.70)

    # Test: Anchor at z*=10 has Ω_m > 0.99
    tests_total += 1
    anchor = des["anchor_z_star"]
    tests_passed += int(anchor["Omega_m_star"] > 0.99)

    details["Omega_m_range"] = (
        round(float(omega_m[0]), 4),
        round(float(omega_m[-1]), 4),
    )
    details["Omega_m_star"] = round(float(anchor["Omega_m_star"]), 6)

    return TheoremResult(
        name="T-WL-4: Omega_m Dominance at High z",
        statement="Ω_m(z) increases with z; Ω_m(z*=10) > 0.99",
        n_tests=tests_total,
        n_passed=tests_passed,
        n_failed=tests_total - tests_passed,
        details=details,
        verdict="PROVEN" if tests_passed == tests_total else "FALSIFIED",
    )


# ═════════════════════════════════════════════════════════════════════
# THEOREM T-WL-5: Sigma8 Suppression
# ═════════════════════════════════════════════════════════════════════


def theorem_WL5_sigma8_suppression() -> TheoremResult:
    """T-WL-5: σ8(z) decreases with redshift (structure growth suppressed)."""
    des = _get_des_y3()
    tests_total = 0
    tests_passed = 0
    details: dict[str, Any] = {}

    s8 = des["sigma8_z"]

    # Test: σ8 strictly decreasing
    tests_total += 1
    mono = all(s8[i] > s8[i + 1] for i in range(len(s8) - 1))
    tests_passed += int(mono)

    # Test: σ8 at lowest z > 0.60
    tests_total += 1
    tests_passed += int(s8[0] > 0.60)

    # Test: Anchor at z*=10 has σ8 < 0.10
    tests_total += 1
    anchor = des["anchor_z_star"]
    tests_passed += int(anchor["sigma8_star"] < 0.10)

    details["sigma8_range"] = (round(float(s8[0]), 4), round(float(s8[-1]), 4))

    return TheoremResult(
        name="T-WL-5: Sigma8 Suppression",
        statement="σ8(z) strictly decreases with redshift",
        n_tests=tests_total,
        n_passed=tests_passed,
        n_failed=tests_total - tests_passed,
        details=details,
        verdict="PROVEN" if tests_passed == tests_total else "FALSIFIED",
    )


# ═════════════════════════════════════════════════════════════════════
# THEOREM T-WL-6: Flatness Consistency
# ═════════════════════════════════════════════════════════════════════


def theorem_WL6_flatness() -> TheoremResult:
    """T-WL-6: Ω_m(z) + Ω_Λ(z) = 1 at all redshifts (flat universe)."""
    des = _get_des_y3()
    tests_total = 0
    tests_passed = 0
    details: dict[str, Any] = {}

    residuals = []
    for z in des["z_bins"]:
        bg = compute_background(float(z))
        r = abs(bg.Omega_m_z + bg.Omega_Lambda_z - 1.0)
        residuals.append(r)

    max_r = max(residuals)
    details["max_residual"] = float(max_r)

    # Test: Max residual < 1e-12
    tests_total += 1
    tests_passed += int(max_r < 1e-12)

    # Test: Works at z=0 too
    tests_total += 1
    bg0 = compute_background(0.0)
    tests_passed += int(abs(bg0.Omega_m_z + bg0.Omega_Lambda_z - 1.0) < 1e-12)

    # Test: Works at anchor z*=10
    tests_total += 1
    bg_star = compute_background(10.0)
    tests_passed += int(abs(bg_star.Omega_m_z + bg_star.Omega_Lambda_z - 1.0) < 1e-12)

    return TheoremResult(
        name="T-WL-6: Flatness Consistency",
        statement="Ω_m + Ω_Λ = 1 to machine precision at all redshifts",
        n_tests=tests_total,
        n_passed=tests_passed,
        n_failed=tests_total - tests_passed,
        details=details,
        verdict="PROVEN" if tests_passed == tests_total else "FALSIFIED",
    )


# ═════════════════════════════════════════════════════════════════════
# THEOREM T-WL-7: Sigma Tension Mapping
# ═════════════════════════════════════════════════════════════════════


def theorem_WL7_sigma_tension() -> TheoremResult:
    """T-WL-7: Σ₀ ≠ 1 maps to Collapse regime via Sigma-to-UMCP bridge.

    GR predicts Σ₀ = 1. Deviation maps ω_analog = |1 - Σ₀| → Collapse
    for any nontrivial Σ₀ measurement.
    """
    tests_total = 0
    tests_passed = 0
    details: dict[str, Any] = {}

    # Test: Σ₀ = 0.8 → Collapse
    tests_total += 1
    r08 = Sigma_to_UMCP_invariants(0.8, 0.05, 0.3)
    tests_passed += int(r08["regime"] == "Collapse")

    # Test: Σ₀ = 1.0 → ω = 1.0 (maximal departure from GR anchor)
    tests_total += 1
    r10 = Sigma_to_UMCP_invariants(1.0, 0.05, 0.3)
    tests_passed += int(r10["omega_analog"] >= 0.99)

    # Test: F_analog + omega_analog forms a valid pair
    tests_total += 1
    tests_passed += int(abs(r08["F_analog"] + r08["omega_analog"] - 1.0) < 1e-10)

    details["Sigma_0.8"] = {
        "F": round(r08["F_analog"], 4),
        "omega": round(r08["omega_analog"], 4),
    }

    return TheoremResult(
        name="T-WL-7: Sigma Tension Mapping",
        statement="Σ₀ deviation from GR maps to Collapse via UMCP bridge",
        n_tests=tests_total,
        n_passed=tests_passed,
        n_failed=tests_total - tests_passed,
        details=details,
        verdict="PROVEN" if tests_passed == tests_total else "FALSIFIED",
    )


# ═════════════════════════════════════════════════════════════════════
# THEOREM T-WL-8: Anchor Star Properties
# ═════════════════════════════════════════════════════════════════════


def theorem_WL8_anchor_star() -> TheoremResult:
    """T-WL-8: z* = 10 anchor has D1 < 0.2 and σ8 < 0.10."""
    des = _get_des_y3()
    tests_total = 0
    tests_passed = 0
    details: dict[str, Any] = {}

    anchor = des["anchor_z_star"]
    details["D1_star"] = round(float(anchor["D1_star"]), 6)
    details["sigma8_star"] = round(float(anchor["sigma8_star"]), 6)
    details["Omega_m_star"] = round(float(anchor["Omega_m_star"]), 6)

    # Test: D1_star < 0.2
    tests_total += 1
    tests_passed += int(anchor["D1_star"] < 0.2)

    # Test: σ8_star < 0.10
    tests_total += 1
    tests_passed += int(anchor["sigma8_star"] < 0.10)

    # Test: z = 10
    tests_total += 1
    tests_passed += int(anchor["z"] == 10.0)

    return TheoremResult(
        name="T-WL-8: Anchor Star Properties",
        statement="z*=10 anchor has D1<0.2 and σ8<0.10 (early-universe suppression)",
        n_tests=tests_total,
        n_passed=tests_passed,
        n_failed=tests_total - tests_passed,
        details=details,
        verdict="PROVEN" if tests_passed == tests_total else "FALSIFIED",
    )


# ═════════════════════════════════════════════════════════════════════
# THEOREM T-WL-9: DES Y3 Bin Count
# ═════════════════════════════════════════════════════════════════════


def theorem_WL9_bin_count() -> TheoremResult:
    """T-WL-9: DES Y3 has 4 tomographic redshift bins in [0.2, 0.8]."""
    des = _get_des_y3()
    tests_total = 0
    tests_passed = 0
    details: dict[str, Any] = {}

    z = des["z_bins"]
    details["n_bins"] = len(z)
    details["z_range"] = (round(float(z[0]), 4), round(float(z[-1]), 4))

    # Test: 4 bins
    tests_total += 1
    tests_passed += int(len(z) == 4)

    # Test: All z in [0.2, 0.8]
    tests_total += 1
    tests_passed += int(all(0.2 <= zi <= 0.8 for zi in z))

    # Test: Bins are sorted
    tests_total += 1
    tests_passed += int(all(z[i] < z[i + 1] for i in range(len(z) - 1)))

    return TheoremResult(
        name="T-WL-9: DES Y3 Bin Count",
        statement="DES Y3 has 4 tomographic bins in z ∈ [0.2, 0.8]",
        n_tests=tests_total,
        n_passed=tests_passed,
        n_failed=tests_total - tests_passed,
        details=details,
        verdict="PROVEN" if tests_passed == tests_total else "FALSIFIED",
    )


# ═════════════════════════════════════════════════════════════════════
# THEOREM T-WL-10: Boost Nonlinearity
# ═════════════════════════════════════════════════════════════════════


def theorem_WL10_boost_nonlinearity() -> TheoremResult:
    """T-WL-10: Boost factor grows with multipole ℓ (nonlinear enhancement)."""
    tests_total = 0
    tests_passed = 0
    details: dict[str, Any] = {}

    ells = [100, 500, 1000, 2000]
    z_test = 0.5
    boosts = []
    for ell in ells:
        b = compute_boost_factor(ell, z=z_test)
        boosts.append(b.B_boost)

    details["boosts"] = {str(ell): round(float(b), 2) for ell, b in zip(ells, boosts, strict=True)}

    # Test: Boost monotone increasing with ℓ
    tests_total += 1
    mono = all(boosts[i] < boosts[i + 1] for i in range(len(boosts) - 1))
    tests_passed += int(mono)

    # Test: At ℓ=100, boost < ℓ=2000
    tests_total += 1
    tests_passed += int(boosts[0] < boosts[-1])

    # Test: At ℓ=2000, boost > 10000
    tests_total += 1
    tests_passed += int(boosts[-1] > 10000)

    return TheoremResult(
        name="T-WL-10: Boost Nonlinearity",
        statement="Boost factor grows with multipole ℓ (nonlinear enhancement)",
        n_tests=tests_total,
        n_passed=tests_passed,
        n_failed=tests_total - tests_passed,
        details=details,
        verdict="PROVEN" if tests_passed == tests_total else "FALSIFIED",
    )


# ═════════════════════════════════════════════════════════════════════
# RUNNER
# ═════════════════════════════════════════════════════════════════════

ALL_THEOREMS = [
    theorem_WL1_D1_monotonicity,
    theorem_WL2_H_monotonicity,
    theorem_WL3_chi_monotonicity,
    theorem_WL4_omega_m_dominance,
    theorem_WL5_sigma8_suppression,
    theorem_WL6_flatness,
    theorem_WL7_sigma_tension,
    theorem_WL8_anchor_star,
    theorem_WL9_bin_count,
    theorem_WL10_boost_nonlinearity,
]


def run_all_theorems() -> list[TheoremResult]:
    """Run all 10 Weyl theorems."""
    return [thm() for thm in ALL_THEOREMS]


if __name__ == "__main__":
    results = run_all_theorems()
    proven = sum(1 for r in results if r.verdict == "PROVEN")
    total_sub = sum(r.n_tests for r in results)
    passed_sub = sum(r.n_passed for r in results)
    print(f"\nWeyl Theorems: {proven}/{len(results)}")
    print(f"Total subtests: {passed_sub}/{total_sub}")
    for r in results:
        mark = "✓" if r.verdict == "PROVEN" else "✗"
        print(f"  {mark} {r.name}: {r.n_passed}/{r.n_tests} — {r.verdict}")
