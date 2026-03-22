"""Tests for Emergent Structural Insight Theorems (T-SI-1 through T-SI-6).

Six theorems formalizing deep structural phenomena discovered through
systematic kernel probing — stateless computation, saddle point geometry,
cascading channel death, number-theoretic bridges, symmetry hierarchy,
and flat-manifold extrinsic complexity.

Cross-references:
    Formalism:       closures/gcd/emergent_structural_insights.py
    Kernel:          src/umcp/kernel_optimized.py
    Frozen contract: src/umcp/frozen_contract.py
    Prior theorems:  closures/gcd/kernel_structural_theorems.py (T-KS-1–7)

All 6 theorems derive from Axiom-0 through the Tier-1 identities:
    F + ω = 1, IC ≤ F, IC = exp(κ)
"""

from __future__ import annotations

import math

import numpy as np
import pytest

from closures.gcd.emergent_structural_insights import (
    TheoremResult,
    run_all_theorems,
    theorem_TSI1_stateless_mirror,
    theorem_TSI2_equator_saddle,
    theorem_TSI3_cascading_channel_death,
    theorem_TSI4_fisher_entropy_zeta_bridge,
    theorem_TSI5_symmetry_hierarchy,
    theorem_TSI6_flat_base_extrinsic,
)
from umcp.frozen_contract import EPSILON
from umcp.kernel_optimized import compute_kernel_outputs

# ═══════════════════════════════════════════════════════════════════
# MODULE-LEVEL: ALL THEOREMS PROVEN
# ═══════════════════════════════════════════════════════════════════


class TestAllEmergentTheoremsProven:
    """Meta-tests: every theorem must pass all its subtests."""

    @pytest.fixture(scope="class")
    def all_results(self) -> list[TheoremResult]:
        return run_all_theorems()

    def test_all_six_proven(self, all_results: list[TheoremResult]) -> None:
        for r in all_results:
            assert r.verdict == "PROVEN", f"{r.name}: {r.n_passed}/{r.n_tests}"

    def test_total_subtests_at_least_100(self, all_results: list[TheoremResult]) -> None:
        total = sum(r.n_tests for r in all_results)
        assert total >= 100, f"Only {total} subtests"

    def test_zero_failures(self, all_results: list[TheoremResult]) -> None:
        total_fail = sum(r.n_failed for r in all_results)
        assert total_fail == 0, f"{total_fail} subtests failed"

    def test_six_theorems(self, all_results: list[TheoremResult]) -> None:
        assert len(all_results) == 6


# ═══════════════════════════════════════════════════════════════════
# T-SI-1: STATELESS MIRROR
# ═══════════════════════════════════════════════════════════════════


class TestTSI1StatelessMirror:
    """T-SI-1: K(c,w) is a pure function — history-independent."""

    def test_theorem_proven(self) -> None:
        r = theorem_TSI1_stateless_mirror()
        assert r.verdict == "PROVEN"
        assert r.n_failed == 0

    def test_same_input_same_output(self) -> None:
        """Identical inputs always produce identical outputs."""
        c = np.array([0.3, 0.5, 0.7, 0.9])
        w = np.ones(4) / 4
        k1 = compute_kernel_outputs(c, w)
        k2 = compute_kernel_outputs(c, w)
        for key in ["F", "omega", "S", "C", "kappa", "IC"]:
            assert k1[key] == k2[key], f"{key} differs between calls"

    def test_order_independent_of_prior_call(self) -> None:
        """Kernel output doesn't depend on what was computed before."""
        c_target = np.array([0.4, 0.6, 0.8])
        w = np.ones(3) / 3

        # Compute target first
        k_first = compute_kernel_outputs(c_target, w)

        # Compute something extreme in between
        compute_kernel_outputs(np.array([EPSILON, EPSILON, 0.999]), w)

        # Recompute target
        k_second = compute_kernel_outputs(c_target, w)

        for key in ["F", "omega", "S", "C", "kappa", "IC"]:
            assert k_first[key] == k_second[key]

    @pytest.mark.parametrize("perm", [[1, 0, 3, 2], [3, 2, 1, 0], [2, 0, 3, 1]])
    def test_permutation_invariance(self, perm: list[int]) -> None:
        """Permuting (c, w) together preserves all outputs."""
        c = np.array([0.2, 0.4, 0.6, 0.8])
        w = np.array([0.1, 0.2, 0.3, 0.4])
        k_orig = compute_kernel_outputs(c, w)
        k_perm = compute_kernel_outputs(c[perm], w[perm])
        for key in ["F", "omega", "S", "C", "kappa", "IC"]:
            assert k_orig[key] == pytest.approx(k_perm[key], abs=1e-14)


# ═══════════════════════════════════════════════════════════════════
# T-SI-2: EQUATOR SADDLE POINT
# ═══════════════════════════════════════════════════════════════════


class TestTSI2EquatorSaddle:
    """T-SI-2: S + κ = 0 at c = 1/2 is a saddle point."""

    def test_theorem_proven(self) -> None:
        r = theorem_TSI2_equator_saddle()
        assert r.verdict == "PROVEN"
        assert r.n_failed == 0

    @pytest.mark.parametrize("n", [2, 4, 8, 16, 32])
    def test_s_plus_kappa_zero_at_equator(self, n: int) -> None:
        """S + κ = 0 exactly when all channels = 1/2."""
        c = np.full(n, 0.5)
        w = np.ones(n) / n
        k = compute_kernel_outputs(c, w)
        assert abs(k["S"] + k["kappa"]) < 1e-14

    def test_away_from_equator_nonzero(self) -> None:
        """S + κ ≠ 0 for c ≠ 1/2 (even homogeneous)."""
        for c0 in [0.1, 0.3, 0.7, 0.9]:
            c = np.full(8, c0)
            w = np.ones(8) / 8
            k = compute_kernel_outputs(c, w)
            assert abs(k["S"] + k["kappa"]) > 1e-10

    def test_heterogeneity_breaks_zero(self) -> None:
        """Perturbation from equator drives S + κ away from zero."""
        w = np.ones(8) / 8
        c_eq = np.full(8, 0.5)
        k_eq = compute_kernel_outputs(c_eq, w)

        c_het = np.full(8, 0.5)
        c_het[:4] = 0.7
        c_het[4:] = 0.3
        k_het = compute_kernel_outputs(c_het, w)

        assert abs(k_eq["S"] + k_eq["kappa"]) < abs(k_het["S"] + k_het["kappa"])


# ═══════════════════════════════════════════════════════════════════
# T-SI-3: CASCADING CHANNEL DEATH
# ═══════════════════════════════════════════════════════════════════


class TestTSI3CascadingChannelDeath:
    """T-SI-3: IC decays exponentially with dead channels."""

    def test_theorem_proven(self) -> None:
        r = theorem_TSI3_cascading_channel_death()
        assert r.verdict == "PROVEN"
        assert r.n_failed == 0

    @pytest.mark.parametrize("n_dead", [1, 2, 3, 4])
    def test_exponential_decay_formula(self, n_dead: int) -> None:
        """ln(IC) = (n_dead/n)·ln(ε) + ((n−n_dead)/n)·ln(c_live)."""
        n = 8
        c_live = 0.999
        c = np.full(n, c_live)
        c[:n_dead] = EPSILON
        w = np.ones(n) / n
        k = compute_kernel_outputs(c, w)
        frac = n_dead / n
        predicted = math.exp(frac * math.log(EPSILON) + (1 - frac) * math.log(c_live))
        assert k["IC"] == pytest.approx(predicted, rel=0.05)

    def test_one_dead_in_32_detectable(self) -> None:
        """Even 1 dead channel in 32 is detectable."""
        n = 32
        c = np.full(n, 0.999)
        w = np.ones(n) / n
        k_clean = compute_kernel_outputs(c, w)
        c[0] = EPSILON
        k_dead = compute_kernel_outputs(c, w)
        assert k_clean["IC"] / k_dead["IC"] > 1.5

    def test_ic_monotone_with_deaths(self) -> None:
        """More dead channels → lower IC."""
        n = 8
        ics = []
        for n_dead in range(n):
            c = np.full(n, 0.999)
            c[:n_dead] = EPSILON
            w = np.ones(n) / n
            k = compute_kernel_outputs(c, w)
            ics.append(k["IC"])
        for i in range(len(ics) - 1):
            assert ics[i] > ics[i + 1]


# ═══════════════════════════════════════════════════════════════════
# T-SI-4: FISHER-ENTROPY-ZETA BRIDGE
# ═══════════════════════════════════════════════════════════════════


class TestTSI4FisherEntropyZetaBridge:
    """T-SI-4: ∫₀¹ g_F(c)·S(c) dc = π²/3 = 2ζ(2)."""

    def test_theorem_proven(self) -> None:
        r = theorem_TSI4_fisher_entropy_zeta_bridge()
        assert r.verdict == "PROVEN"
        assert r.n_failed == 0

    def test_integral_converges_to_pi_squared_over_3(self) -> None:
        """Numerical integral approaches π²/3 with resolution."""
        target = math.pi**2 / 3
        c = np.linspace(1e-10, 1 - 1e-10, 1_000_000)
        g_F = 1.0 / (c * (1.0 - c))
        S = -(c * np.log(c) + (1.0 - c) * np.log(1.0 - c))
        integral = float(np.trapezoid(g_F * S, c))
        assert integral == pytest.approx(target, rel=1e-5)

    def test_symmetry_about_half(self) -> None:
        """Integrand is symmetric about c = 1/2."""
        n = 100_000
        c = np.linspace(1e-10, 0.5, n)
        g_F = 1.0 / (c * (1.0 - c))
        S = -(c * np.log(c) + (1.0 - c) * np.log(1.0 - c))
        half = float(np.trapezoid(g_F * S, c))
        target = math.pi**2 / 3
        assert 2 * half == pytest.approx(target, rel=1e-3)

    def test_two_zeta_two_equals_target(self) -> None:
        """Verify 2·ζ(2) ≈ π²/3 to 4 decimal places."""
        zeta2 = sum(1.0 / k**2 for k in range(1, 100_001))
        assert 2 * zeta2 == pytest.approx(math.pi**2 / 3, abs=1e-4)


# ═══════════════════════════════════════════════════════════════════
# T-SI-5: SYMMETRY BREAKING HIERARCHY
# ═══════════════════════════════════════════════════════════════════


class TestTSI5SymmetryHierarchy:
    """T-SI-5: Only F + ω = 1 is exact; everything else breaks."""

    def test_theorem_proven(self) -> None:
        r = theorem_TSI5_symmetry_hierarchy()
        assert r.verdict == "PROVEN"
        assert r.n_failed == 0

    @pytest.mark.parametrize("seed", [42, 123, 2025, 9999])
    def test_duality_exact_random(self, seed: int) -> None:
        """F + ω = 1 to machine precision for random traces."""
        rng = np.random.default_rng(seed)
        for _ in range(100):
            n = rng.integers(2, 20)
            c = rng.uniform(EPSILON, 1 - EPSILON, n)
            w = rng.dirichlet(np.ones(n))
            k = compute_kernel_outputs(c, w)
            assert abs(k["F"] + k["omega"] - 1.0) < 1e-14

    def test_homogeneous_gap_zero(self) -> None:
        """Δ = F − IC = 0 for homogeneous traces."""
        for c0 in [0.1, 0.3, 0.5, 0.7, 0.9]:
            c = np.full(8, c0)
            w = np.ones(8) / 8
            k = compute_kernel_outputs(c, w)
            assert abs(k["F"] - k["IC"]) < 1e-10

    def test_heterogeneous_gap_positive(self) -> None:
        """Δ = F − IC > 0 for heterogeneous traces."""
        rng = np.random.default_rng(777)
        for _ in range(50):
            c = rng.uniform(0.01, 0.99, 8)
            w = np.ones(8) / 8
            k = compute_kernel_outputs(c, w)
            assert k["F"] - k["IC"] > 1e-10

    def test_gap_monotone_with_spread(self) -> None:
        """Δ increases as channel spread increases."""
        deltas = []
        for sp in np.linspace(0, 0.45, 20):
            c = np.full(8, 0.5)
            c[:4] = np.clip(0.5 + sp, EPSILON, 1 - EPSILON)
            c[4:] = np.clip(0.5 - sp, EPSILON, 1 - EPSILON)
            w = np.ones(8) / 8
            k = compute_kernel_outputs(c, w)
            deltas.append(k["F"] - k["IC"])
        for i in range(1, len(deltas)):
            assert deltas[i] >= deltas[i - 1] - 1e-15


# ═══════════════════════════════════════════════════════════════════
# T-SI-6: FLAT BASE, EXTRINSIC COMPLEXITY
# ═══════════════════════════════════════════════════════════════════


class TestTSI6FlatBaseExtrinsic:
    """T-SI-6: g_F(θ) = 1 — the manifold is flat."""

    def test_theorem_proven(self) -> None:
        r = theorem_TSI6_flat_base_extrinsic()
        assert r.verdict == "PROVEN"
        assert r.n_failed == 0

    @pytest.mark.parametrize(
        "theta",
        [math.pi / 6, math.pi / 4, math.pi / 3, math.pi / 2, 2 * math.pi / 3],
    )
    def test_g_F_equals_one(self, theta: float) -> None:
        """g_F(θ) = sin²θ / (4·sin²(θ/2)·cos²(θ/2)) = 1."""
        c = math.sin(theta / 2) ** 2
        g_F = math.sin(theta) ** 2 / (4 * c * (1 - c))
        assert g_F == pytest.approx(1.0, abs=1e-14)

    def test_curvature_zero_homogeneous(self) -> None:
        """C = 0 for homogeneous traces."""
        for c0 in np.linspace(0.01, 0.99, 20):
            c = np.full(8, c0)
            w = np.ones(8) / 8
            k = compute_kernel_outputs(c, w)
            assert abs(k["C"]) < 1e-14

    def test_curvature_positive_heterogeneous(self) -> None:
        """C > 0 requires heterogeneous channels."""
        c = np.array([0.1, 0.3, 0.5, 0.7, 0.9, 0.2, 0.4, 0.8])
        w = np.ones(8) / 8
        k = compute_kernel_outputs(c, w)
        assert k["C"] > 0.1

    def test_curvature_equals_std_over_half(self) -> None:
        """C = std(c) / 0.5."""
        rng = np.random.default_rng(2025)
        for _ in range(20):
            c = rng.uniform(0.01, 0.99, 8)
            w = np.ones(8) / 8
            k = compute_kernel_outputs(c, w)
            expected = float(np.std(c)) / 0.5
            assert k["C"] == pytest.approx(expected, abs=1e-10)

    def test_fisher_distance_matches_theta_diff(self) -> None:
        """On a flat manifold, Fisher distance = |θ₂ − θ₁|."""
        c1, c2 = 0.2, 0.8
        theta1 = 2 * math.asin(math.sqrt(c1))
        theta2 = 2 * math.asin(math.sqrt(c2))
        expected = abs(theta2 - theta1)

        # Numerical integration of 1/√(c(1−c)) from c1 to c2
        c_arr = np.linspace(c1, c2, 50_000)
        integrand = 1.0 / np.sqrt(c_arr * (1.0 - c_arr))
        numerical = float(np.trapezoid(integrand, c_arr))
        assert numerical == pytest.approx(expected, rel=0.01)
