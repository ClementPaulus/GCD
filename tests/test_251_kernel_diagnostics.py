"""
Tests for KernelDiagnostics: coupling structure, gate margins,
cost decomposition, and per-channel sensitivity.

Tier-0 Protocol: Tests that the diagnose() function correctly reveals
the coupling structure hidden in flat kernel outputs.

Test Range: 251
Domain: Kernel diagnostics (Tier-0 interpretive layer over Tier-1 outputs)
"""

from __future__ import annotations

import numpy as np
import pytest

from umcp.frozen_contract import (
    ALPHA,
    EPSILON,
    P_EXPONENT,
)
from umcp.kernel_optimized import (
    OptimizedKernelComputer,
    diagnose,
)


@pytest.fixture()
def computer() -> OptimizedKernelComputer:
    return OptimizedKernelComputer()


# ---- Helpers ----


def _compute_and_diagnose(
    c: np.ndarray,
    w: np.ndarray | None = None,
    computer: OptimizedKernelComputer | None = None,
) -> tuple:
    """Compute kernel outputs and diagnostics in one call."""
    if w is None:
        w = np.ones(len(c)) / len(c)
    if computer is None:
        computer = OptimizedKernelComputer()
    outputs = computer.compute(c, w)
    diag = diagnose(outputs, c, w)
    return outputs, diag


# ===========================================================================
# §1 — IC/F Ratio
# ===========================================================================


class TestICFRatio:
    """IC/F ratio reveals multiplicative coherence fraction."""

    def test_homogeneous_channels_ratio_near_one(self, computer: OptimizedKernelComputer) -> None:
        """Uniform channels → IC ≈ F → IC/F ≈ 1."""
        c = np.full(8, 0.75)
        w = np.ones(8) / 8
        outputs = computer.compute(c, w)
        diag = diagnose(outputs, c, w)
        assert abs(diag.ic_f_ratio - 1.0) < 1e-10

    def test_one_weak_channel_depresses_ratio(self, computer: OptimizedKernelComputer) -> None:
        """One weak channel kills IC more than F → IC/F drops."""
        c_uniform = np.full(8, 0.80)
        c_slaughtered = np.array([0.80, 0.80, 0.05, 0.80, 0.80, 0.80, 0.80, 0.80])
        w = np.ones(8) / 8

        _, diag_uniform = _compute_and_diagnose(c_uniform, w, computer)
        _, diag_slaughter = _compute_and_diagnose(c_slaughtered, w, computer)

        assert diag_uniform.ic_f_ratio > 0.99
        assert diag_slaughter.ic_f_ratio < 0.85
        # Geometric slaughter: IC/F drops with one weak channel
        assert diag_slaughter.ic_f_ratio < diag_uniform.ic_f_ratio

    def test_ratio_bounded_by_integrity_bound(self, computer: OptimizedKernelComputer) -> None:
        """IC ≤ F → IC/F ≤ 1 always."""
        rng = np.random.default_rng(42)
        for _ in range(100):
            c = rng.uniform(0.01, 0.99, size=8)
            w = rng.dirichlet(np.ones(8))
            _, diag = _compute_and_diagnose(c, w, computer)
            assert diag.ic_f_ratio <= 1.0 + 1e-12


# ===========================================================================
# §2 — Canonical Regime Classification
# ===========================================================================


class TestCanonicalRegime:
    """Canonical 4-gate regime matches frozen_contract.classify_regime."""

    def test_stable_regime(self, computer: OptimizedKernelComputer) -> None:
        """High fidelity, low drift, low entropy, low curvature → STABLE."""
        c = np.full(8, 0.97)
        w = np.ones(8) / 8
        _, diag = _compute_and_diagnose(c, w, computer)
        assert diag.regime == "STABLE"
        assert not diag.critical

    def test_collapse_regime(self, computer: OptimizedKernelComputer) -> None:
        """High drift → COLLAPSE."""
        c = np.full(8, 0.40)
        w = np.ones(8) / 8
        _, diag = _compute_and_diagnose(c, w, computer)
        assert diag.regime == "COLLAPSE"

    def test_watch_regime(self, computer: OptimizedKernelComputer) -> None:
        """Intermediate drift → WATCH."""
        c = np.full(8, 0.92)
        w = np.ones(8) / 8
        _, diag = _compute_and_diagnose(c, w, computer)
        assert diag.regime == "WATCH"

    def test_critical_overlay(self, computer: OptimizedKernelComputer) -> None:
        """IC < 0.30 → critical flag set."""
        # Need enough near-zero channels to drag IC below 0.30
        c = np.array([0.90, 0.01, 0.01, 0.01, 0.90, 0.90, 0.90, 0.90])
        w = np.ones(8) / 8
        _, diag = _compute_and_diagnose(c, w, computer)
        assert diag.critical

    def test_regime_differs_from_legacy(self, computer: OptimizedKernelComputer) -> None:
        """The canonical regime can differ from the legacy heterogeneity classification."""
        # This channel config gives heterogeneity_gap > 0.05 ("fragmented" in legacy)
        # but ω < 0.30 because F is high enough → Watch regime canonically
        c = np.array([0.95, 0.95, 0.10, 0.95, 0.95, 0.95, 0.95, 0.95])
        w = np.ones(8) / 8
        outputs, diag = _compute_and_diagnose(c, w, computer)
        # Legacy says one thing, canonical says another
        assert outputs.regime in ("heterogeneous", "fragmented")
        assert diag.regime in ("WATCH", "COLLAPSE", "CRITICAL")


# ===========================================================================
# §3 — Gate Margins
# ===========================================================================


class TestGateMargins:
    """Gate margins reveal WHICH gate binds and by how much."""

    def test_stable_all_positive(self, computer: OptimizedKernelComputer) -> None:
        """In Stable regime, all margins are positive."""
        c = np.full(8, 0.97)
        w = np.ones(8) / 8
        _, diag = _compute_and_diagnose(c, w, computer)
        assert diag.gates.omega > 0
        assert diag.gates.F > 0
        assert diag.gates.S > 0
        assert diag.gates.C > 0

    def test_collapse_omega_negative(self, computer: OptimizedKernelComputer) -> None:
        """In Collapse, ω margin is deeply negative."""
        c = np.full(8, 0.30)
        w = np.ones(8) / 8
        _, diag = _compute_and_diagnose(c, w, computer)
        assert diag.gates.omega < -0.3

    def test_binding_gate_is_smallest(self, computer: OptimizedKernelComputer) -> None:
        """Binding gate is the one with the smallest margin."""
        rng = np.random.default_rng(123)
        for _ in range(50):
            c = rng.uniform(0.05, 0.99, size=8)
            w = rng.dirichlet(np.ones(8))
            _, diag = _compute_and_diagnose(c, w, computer)
            margins = {
                "omega": diag.gates.omega,
                "F": diag.gates.F,
                "S": diag.gates.S,
                "C": diag.gates.C,
            }
            actual_binding = min(margins, key=margins.get)  # type: ignore[arg-type]
            assert diag.gates.binding == actual_binding

    def test_min_margin_property(self, computer: OptimizedKernelComputer) -> None:
        """GateMargins.min_margin returns the smallest value."""
        c = np.array([0.80, 0.80, 0.20, 0.80, 0.80, 0.80, 0.80, 0.80])
        w = np.ones(8) / 8
        _, diag = _compute_and_diagnose(c, w, computer)
        expected = min(diag.gates.omega, diag.gates.F, diag.gates.S, diag.gates.C)
        assert abs(diag.gates.min_margin - expected) < 1e-15


# ===========================================================================
# §4 — Cost Decomposition
# ===========================================================================


class TestCostDecomposition:
    """Cost decomposition reveals whether drift or curvature dominates."""

    def test_gamma_formula(self, computer: OptimizedKernelComputer) -> None:
        """Γ(ω) = ω^p / (1 - ω + ε) matches hand computation."""
        c = np.full(8, 0.60)
        w = np.ones(8) / 8
        outputs, diag = _compute_and_diagnose(c, w, computer)
        omega = outputs.omega
        expected_gamma = omega**P_EXPONENT / (1 - omega + EPSILON)
        assert abs(diag.costs.gamma - expected_gamma) < 1e-12

    def test_d_c_formula(self, computer: OptimizedKernelComputer) -> None:
        """D_C = α·C matches hand computation."""
        c = np.array([0.90, 0.20, 0.70, 0.50, 0.80, 0.30, 0.60, 0.40])
        w = np.ones(8) / 8
        outputs, diag = _compute_and_diagnose(c, w, computer)
        expected_d_c = ALPHA * outputs.C
        assert abs(diag.costs.d_c - expected_d_c) < 1e-12

    def test_total_is_sum(self, computer: OptimizedKernelComputer) -> None:
        """Total debit = Γ + D_C."""
        rng = np.random.default_rng(77)
        for _ in range(50):
            c = rng.uniform(0.05, 0.99, size=8)
            w = rng.dirichlet(np.ones(8))
            _, diag = _compute_and_diagnose(c, w, computer)
            assert abs(diag.costs.total_debit - (diag.costs.gamma + diag.costs.d_c)) < 1e-12

    def test_low_drift_curvature_dominates(self, computer: OptimizedKernelComputer) -> None:
        """When ω is small but C is large, curvature dominates."""
        # High F but dispersed channels
        c = np.array([0.99, 0.99, 0.50, 0.99, 0.99, 0.99, 0.99, 0.99])
        w = np.ones(8) / 8
        _, diag = _compute_and_diagnose(c, w, computer)
        assert diag.costs.dominant == "curvature"
        assert diag.costs.d_c > diag.costs.gamma

    def test_high_drift_gamma_dominates(self, computer: OptimizedKernelComputer) -> None:
        """When ω is large, drift cost dominates."""
        c = np.full(8, 0.30)  # uniform → C ≈ 0, ω = 0.70
        w = np.ones(8) / 8
        _, diag = _compute_and_diagnose(c, w, computer)
        assert diag.costs.dominant == "drift"
        assert diag.costs.gamma > diag.costs.d_c


# ===========================================================================
# §5 — Channel Sensitivity
# ===========================================================================


class TestChannelSensitivity:
    """Sensitivity ∂IC/∂cₖ = IC·wₖ/cₖ reveals coupling structure."""

    def test_sensitivity_formula(self, computer: OptimizedKernelComputer) -> None:
        """Check sensitivity matches IC·w/c for each channel."""
        c = np.array([0.60, 0.80, 0.10, 0.50, 0.70, 0.40, 0.55, 0.30])
        w = np.ones(8) / 8
        outputs, diag = _compute_and_diagnose(c, w, computer)
        c_clamped = np.clip(c, EPSILON, 1.0 - EPSILON)
        expected = outputs.IC * w / c_clamped
        np.testing.assert_allclose(diag.sensitivity, expected, rtol=1e-10)

    def test_weak_channel_highest_sensitivity(self, computer: OptimizedKernelComputer) -> None:
        """Weakest channel has highest sensitivity (low c → high ∂IC/∂c)."""
        c = np.array([0.80, 0.80, 0.05, 0.80, 0.80, 0.80, 0.80, 0.80])
        w = np.ones(8) / 8
        _, diag = _compute_and_diagnose(c, w, computer)
        assert int(np.argmax(diag.sensitivity)) == 2  # weakest channel
        assert diag.c_min_idx == 2

    def test_uniform_channels_flat_sensitivity(self, computer: OptimizedKernelComputer) -> None:
        """Uniform channels → flat sensitivity → ratio ≈ 1."""
        c = np.full(8, 0.70)
        w = np.ones(8) / 8
        _, diag = _compute_and_diagnose(c, w, computer)
        assert abs(diag.sensitivity_ratio - 1.0) < 1e-10

    def test_heterogeneous_channels_high_ratio(self, computer: OptimizedKernelComputer) -> None:
        """Heterogeneous channels → high sensitivity ratio."""
        c = np.array([0.95, 0.95, 0.05, 0.95, 0.95, 0.95, 0.95, 0.95])
        w = np.ones(8) / 8
        _, diag = _compute_and_diagnose(c, w, computer)
        assert diag.sensitivity_ratio > 10.0  # At least 10x spread

    def test_f_sensitivity_is_flat(self, computer: OptimizedKernelComputer) -> None:
        """∂F/∂cₖ = wₖ is FLAT — contrast with ∂IC/∂cₖ which varies."""
        c = np.array([0.90, 0.90, 0.10, 0.90, 0.90, 0.90, 0.90, 0.90])
        w = np.ones(8) / 8
        _, diag = _compute_and_diagnose(c, w, computer)
        # F's sensitivity is constant: ∂F/∂cₖ = wₖ = 1/8 for all k
        # IC's sensitivity varies: ∂IC/∂cₖ = IC·wₖ/cₖ
        ic_sens_range = float(np.max(diag.sensitivity) / np.min(diag.sensitivity))
        assert ic_sens_range > 5.0  # IC sensitivity varies >5x while F is flat


# ===========================================================================
# §6 — Weakest Channel Identification
# ===========================================================================


class TestWeakestChannel:
    """Weakest channel (c_min) is identified correctly."""

    def test_c_min_and_index(self, computer: OptimizedKernelComputer) -> None:
        c = np.array([0.70, 0.80, 0.15, 0.60, 0.90, 0.50, 0.75, 0.85])
        w = np.ones(8) / 8
        _, diag = _compute_and_diagnose(c, w, computer)
        assert diag.c_min_idx == 2
        assert abs(diag.c_min - 0.15) < 1e-10

    def test_c_max(self, computer: OptimizedKernelComputer) -> None:
        c = np.array([0.70, 0.80, 0.15, 0.60, 0.90, 0.50, 0.75, 0.85])
        w = np.ones(8) / 8
        _, diag = _compute_and_diagnose(c, w, computer)
        assert abs(diag.c_max - 0.90) < 1e-10


# ===========================================================================
# §7 — repr Readability
# ===========================================================================


class TestRepr:
    """The repr makes coupling visible at a glance."""

    def test_repr_contains_key_info(self, computer: OptimizedKernelComputer) -> None:
        c = np.array([0.62, 0.78, 0.15, 0.55, 0.68, 0.45, 0.50, 0.35])
        w = np.ones(8) / 8
        _, diag = _compute_and_diagnose(c, w, computer)
        r = repr(diag)
        assert "regime=" in r
        assert "IC/F=" in r
        assert "binding=" in r
        assert "cost=" in r
        assert "c_min[" in r
        assert "sens=[" in r


# ===========================================================================
# §8 — Stress and Edge Cases
# ===========================================================================


class TestEdgeCases:
    """Boundary conditions and stress tests."""

    def test_all_channels_near_one(self, computer: OptimizedKernelComputer) -> None:
        """c ≈ 1 → everything healthy."""
        c = np.full(8, 0.999)
        w = np.ones(8) / 8
        _, diag = _compute_and_diagnose(c, w, computer)
        assert diag.ic_f_ratio > 0.999
        assert diag.regime == "STABLE"
        assert diag.sensitivity_ratio < 1.01

    def test_all_channels_near_epsilon(self, computer: OptimizedKernelComputer) -> None:
        """c ≈ ε → deep collapse."""
        c = np.full(8, 0.01)
        w = np.ones(8) / 8
        _, diag = _compute_and_diagnose(c, w, computer)
        assert diag.regime in ("COLLAPSE", "CRITICAL")
        assert diag.ic_f_ratio > 0.99  # still ≈1 because uniform

    def test_two_channels(self, computer: OptimizedKernelComputer) -> None:
        """Works with minimal channel count n=2."""
        c = np.array([0.90, 0.10])
        w = np.array([0.5, 0.5])
        _, diag = _compute_and_diagnose(c, w, computer)
        assert diag.c_min_idx == 1
        assert diag.sensitivity_ratio > 5.0

    def test_many_channels(self, computer: OptimizedKernelComputer) -> None:
        """Works with large channel count."""
        rng = np.random.default_rng(999)
        c = rng.uniform(0.01, 0.99, size=100)
        w = np.ones(100) / 100
        _, diag = _compute_and_diagnose(c, w, computer)
        assert 0.0 < diag.ic_f_ratio <= 1.0
        assert diag.sensitivity.shape == (100,)

    @pytest.mark.parametrize("seed", range(20))
    def test_random_invariants_hold(self, computer: OptimizedKernelComputer, seed: int) -> None:
        """Tier-1 identities hold in diagnostics for random inputs."""
        rng = np.random.default_rng(seed)
        c = rng.uniform(0.01, 0.99, size=8)
        w = rng.dirichlet(np.ones(8))
        _outputs, diag = _compute_and_diagnose(c, w, computer)

        # IC/F ≤ 1 (integrity bound)
        assert diag.ic_f_ratio <= 1.0 + 1e-12

        # Total debit = Γ + D_C
        assert abs(diag.costs.total_debit - (diag.costs.gamma + diag.costs.d_c)) < 1e-12

        # Sensitivity ≥ 0
        assert np.all(diag.sensitivity >= 0)

        # Binding gate is the min
        margins = {"omega": diag.gates.omega, "F": diag.gates.F, "S": diag.gates.S, "C": diag.gates.C}
        assert diag.gates.binding == min(margins, key=margins.get)  # type: ignore[arg-type]
