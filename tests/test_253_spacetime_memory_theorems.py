"""Tests for Spacetime Memory closure — 10 theorems.

Derivation chain: Axiom-0 -> frozen_contract -> kernel_optimized
                   -> spacetime_kernel -> spacetime_theorems -> this test
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pytest

# ── Path setup ────────────────────────────────────────────────────
_WORKSPACE = Path(__file__).resolve().parents[1]
if str(_WORKSPACE / "src") not in sys.path:
    sys.path.insert(0, str(_WORKSPACE / "src"))
if str(_WORKSPACE) not in sys.path:
    sys.path.insert(0, str(_WORKSPACE))

from closures.spacetime_memory.spacetime_kernel import (
    CHANNEL_NAMES,
    SPACETIME_CATALOG,
    SpacetimeEntity,
    SpacetimeKernelResult,
    budget_surface_height,
    classify_lensing_morphology,
    compute_all_spacetime,
    compute_deflection_angle,
    compute_well_depth,
    d2_gamma,
    d_gamma,
    gamma,
)
from closures.spacetime_memory.spacetime_theorems import (
    prove_all_theorems,
    prove_theorem_TST1,
    prove_theorem_TST2,
    prove_theorem_TST3,
    prove_theorem_TST4,
    prove_theorem_TST5,
    prove_theorem_TST6,
    prove_theorem_TST7,
    prove_theorem_TST8,
    prove_theorem_TST9,
    prove_theorem_TST10,
)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# KERNEL SMOKE TESTS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


class TestSpacetimeKernel:
    """Smoke tests for the spacetime kernel module."""

    def test_catalog_count(self) -> None:
        """37 entities in the catalog."""
        assert len(SPACETIME_CATALOG) == 37

    def test_channel_count(self) -> None:
        """All entities have 8 channels."""
        for entity in SPACETIME_CATALOG:
            assert len(entity.channels) == 8, f"{entity.name}: {len(entity.channels)} channels"

    def test_channel_names(self) -> None:
        """8 channel names defined."""
        assert len(CHANNEL_NAMES) == 8

    def test_all_channels_in_range(self) -> None:
        """All channel values in [0, 1]."""
        for entity in SPACETIME_CATALOG:
            for i, c in enumerate(entity.channels):
                assert 0.0 <= c <= 1.0, f"{entity.name}, ch{i}: {c}"

    def test_categories_present(self) -> None:
        """All 8 categories represented."""
        cats = {e.category for e in SPACETIME_CATALOG}
        assert cats == {
            "subatomic",
            "nuclear_atomic",
            "stellar",
            "planetary",
            "diffuse",
            "composite",
            "biological",
            "cognitive",
        }

    @pytest.mark.parametrize(
        "category,expected",
        [
            ("subatomic", 5),
            ("nuclear_atomic", 3),
            ("stellar", 7),
            ("planetary", 5),
            ("diffuse", 4),
            ("composite", 5),
            ("biological", 4),
            ("cognitive", 4),
        ],
    )
    def test_category_counts(self, category: str, expected: int) -> None:
        """Correct count per category."""
        count = sum(1 for e in SPACETIME_CATALOG if e.category == category)
        assert count == expected

    def test_entity_invalid_channels_raises(self) -> None:
        """SpacetimeEntity rejects non-8 channels."""
        with pytest.raises(ValueError, match="expected 8 channels"):
            SpacetimeEntity("bad", "test", (0.5, 0.5))

    def test_compute_all_returns_37(self) -> None:
        """compute_all_spacetime returns 37 results."""
        results = compute_all_spacetime()
        assert len(results) == 37

    def test_kernel_result_types(self) -> None:
        """All kernel results have correct types."""
        results = compute_all_spacetime()
        for r in results:
            assert isinstance(r, SpacetimeKernelResult)
            assert isinstance(r.F, float)
            assert isinstance(r.omega, float)
            assert isinstance(r.IC, float)
            assert isinstance(r.regime, str)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# TIER-1 IDENTITY TESTS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


class TestTier1Identities:
    """Verify Tier-1 identities for all 25 entities."""

    @pytest.fixture(scope="class")
    def all_results(self) -> list[SpacetimeKernelResult]:
        return compute_all_spacetime()

    @pytest.mark.parametrize("idx", range(25))
    def test_duality_identity(self, all_results: list[SpacetimeKernelResult], idx: int) -> None:
        """F + omega = 1 for each entity."""
        r = all_results[idx]
        assert abs(r.F + r.omega - 1.0) < 1e-12, f"{r.name}: F+omega={r.F + r.omega}"

    @pytest.mark.parametrize("idx", range(25))
    def test_integrity_bound(self, all_results: list[SpacetimeKernelResult], idx: int) -> None:
        """IC <= F for each entity."""
        r = all_results[idx]
        assert r.IC <= r.F + 1e-12, f"{r.name}: IC={r.IC} > F={r.F}"

    @pytest.mark.parametrize("idx", range(25))
    def test_log_integrity(self, all_results: list[SpacetimeKernelResult], idx: int) -> None:
        """IC = exp(kappa) for each entity."""
        r = all_results[idx]
        assert abs(r.IC - np.exp(r.kappa)) < 1e-10, f"{r.name}: IC={r.IC}, exp(kappa)={np.exp(r.kappa)}"


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# BUDGET SURFACE FUNCTION TESTS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


class TestBudgetSurface:
    """Tests for the budget surface functions."""

    def test_gamma_zero(self) -> None:
        """Gamma(0) = 0."""
        assert gamma(0.0) == 0.0

    def test_gamma_positive(self) -> None:
        """Gamma is positive for omega > 0."""
        for w in [0.01, 0.1, 0.3, 0.5, 0.8]:
            assert gamma(w) > 0.0

    def test_gamma_diverges_near_one(self) -> None:
        """Gamma grows very large near omega = 1."""
        assert gamma(0.999) > 900

    def test_d_gamma_positive(self) -> None:
        """d_Gamma/d_omega > 0."""
        for w in [0.01, 0.1, 0.3, 0.5, 0.8]:
            assert d_gamma(w) > 0.0

    def test_d2_gamma_positive(self) -> None:
        """d2_Gamma/d_omega2 > 0 (convex)."""
        for w in [0.05, 0.2, 0.5, 0.7, 0.9]:
            assert d2_gamma(w) > 0.0

    def test_surface_linear_in_C(self) -> None:
        """z(omega, C) = Gamma(omega) + alpha * C is linear in C."""
        omega = 0.3
        z1 = budget_surface_height(omega, 0.2)
        z2 = budget_surface_height(omega, 0.4)
        z3 = budget_surface_height(omega, 0.6)
        # Linear: z2 is midpoint of z1 and z3
        assert abs(z2 - (z1 + z3) / 2) < 1e-12


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# MEMORY WELL TESTS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


class TestMemoryWells:
    """Tests for memory well computation."""

    def test_well_depth_zero_cycles(self) -> None:
        """Zero cycles -> zero depth."""
        assert compute_well_depth(-0.5, 0) == 0.0

    def test_well_depth_linearity(self) -> None:
        """Depth is linear in N."""
        d10 = compute_well_depth(-0.5, 10)
        d20 = compute_well_depth(-0.5, 20)
        assert abs(d20 - 2.0 * d10) < 1e-12

    def test_well_depth_positive(self) -> None:
        """Depth is always non-negative."""
        for n in range(50):
            assert compute_well_depth(-0.3, n) >= 0.0


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# LENSING TESTS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


class TestLensing:
    """Tests for lensing functions."""

    def test_deflection_increases_with_kappa(self) -> None:
        """More massive wells deflect more."""
        d1 = compute_deflection_angle(1.0, 1.0)
        d2 = compute_deflection_angle(2.0, 1.0)
        assert d2 > d1

    def test_deflection_decreases_with_distance(self) -> None:
        """Farther trajectories deflect less."""
        d_near = compute_deflection_angle(1.0, 0.5)
        d_far = compute_deflection_angle(1.0, 5.0)
        assert d_near > d_far

    def test_deflection_finite_at_zero(self) -> None:
        """Softening prevents divergence at b = 0."""
        d = compute_deflection_angle(1.0, 0.0)
        assert np.isfinite(d)
        assert d > 0

    @pytest.mark.parametrize(
        "delta,expected",
        [(0.01, "perfect_ring"), (0.05, "thick_arc"), (0.15, "thin_arc"), (0.50, "distorted")],
    )
    def test_lensing_classification(self, delta: float, expected: str) -> None:
        """Lensing morphology classification thresholds."""
        assert classify_lensing_morphology(delta) == expected


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# THEOREM PROOF TESTS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


class TestTheoremTST1:
    """T-ST-1: Gravity Is Budget Gradient."""

    def test_proven(self) -> None:
        result = prove_theorem_TST1()
        assert result.verdict == "PROVEN", f"T-ST-1 failed: {result.n_passed}/{result.n_tests}"

    def test_all_subtests_pass(self) -> None:
        result = prove_theorem_TST1()
        assert result.n_failed == 0


class TestTheoremTST2:
    """T-ST-2: Always Attractive."""

    def test_proven(self) -> None:
        result = prove_theorem_TST2()
        assert result.verdict == "PROVEN", f"T-ST-2 failed: {result.n_passed}/{result.n_tests}"

    def test_all_subtests_pass(self) -> None:
        result = prove_theorem_TST2()
        assert result.n_failed == 0


class TestTheoremTST3:
    """T-ST-3: Cubic Onset (Weakest Force)."""

    def test_proven(self) -> None:
        result = prove_theorem_TST3()
        assert result.verdict == "PROVEN", f"T-ST-3 failed: {result.n_passed}/{result.n_tests}"

    def test_all_subtests_pass(self) -> None:
        result = prove_theorem_TST3()
        assert result.n_failed == 0


class TestTheoremTST4:
    """T-ST-4: Time Dilation Near Wells."""

    def test_proven(self) -> None:
        result = prove_theorem_TST4()
        assert result.verdict == "PROVEN", f"T-ST-4 failed: {result.n_passed}/{result.n_tests}"

    def test_all_subtests_pass(self) -> None:
        result = prove_theorem_TST4()
        assert result.n_failed == 0


class TestTheoremTST5:
    """T-ST-5: Equivalence Principle."""

    def test_proven(self) -> None:
        result = prove_theorem_TST5()
        assert result.verdict == "PROVEN", f"T-ST-5 failed: {result.n_passed}/{result.n_tests}"

    def test_all_subtests_pass(self) -> None:
        result = prove_theorem_TST5()
        assert result.n_failed == 0


class TestTheoremTST6:
    """T-ST-6: Memory Wells From Iteration."""

    def test_proven(self) -> None:
        result = prove_theorem_TST6()
        assert result.verdict == "PROVEN", f"T-ST-6 failed: {result.n_passed}/{result.n_tests}"

    def test_all_subtests_pass(self) -> None:
        result = prove_theorem_TST6()
        assert result.n_failed == 0


class TestTheoremTST7:
    """T-ST-7: Lensing From Heterogeneity."""

    def test_proven(self) -> None:
        result = prove_theorem_TST7()
        assert result.verdict == "PROVEN", f"T-ST-7 failed: {result.n_passed}/{result.n_tests}"

    def test_all_subtests_pass(self) -> None:
        result = prove_theorem_TST7()
        assert result.n_failed == 0


class TestTheoremTST8:
    """T-ST-8: Arrow of Time From Asymmetry."""

    def test_proven(self) -> None:
        result = prove_theorem_TST8()
        assert result.verdict == "PROVEN", f"T-ST-8 failed: {result.n_passed}/{result.n_tests}"

    def test_all_subtests_pass(self) -> None:
        result = prove_theorem_TST8()
        assert result.n_failed == 0


class TestTheoremTST9:
    """T-ST-9: Intrinsic Flatness (K = 0)."""

    def test_proven(self) -> None:
        result = prove_theorem_TST9()
        assert result.verdict == "PROVEN", f"T-ST-9 failed: {result.n_passed}/{result.n_tests}"

    def test_all_subtests_pass(self) -> None:
        result = prove_theorem_TST9()
        assert result.n_failed == 0


class TestTheoremTST10:
    """T-ST-10: Cross-Domain Well Universality."""

    def test_proven(self) -> None:
        result = prove_theorem_TST10()
        assert result.verdict == "PROVEN", f"T-ST-10 failed: {result.n_passed}/{result.n_tests}"

    def test_all_subtests_pass(self) -> None:
        result = prove_theorem_TST10()
        assert result.n_failed == 0


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# ALL THEOREMS INTEGRATION
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


class TestAllTheorems:
    """Integration: all 10 theorems proven."""

    def test_all_10_proven(self) -> None:
        results = prove_all_theorems()
        assert len(results) == 10
        for r in results:
            assert r.verdict == "PROVEN", f"{r.name} failed: {r.n_passed}/{r.n_tests}"

    def test_total_subtests(self) -> None:
        results = prove_all_theorems()
        total = sum(r.n_tests for r in results)
        passed = sum(r.n_passed for r in results)
        assert total >= 30  # At least 30 sub-tests across 10 theorems
        assert passed == total
