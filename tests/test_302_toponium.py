"""Tests for toponium (tt̄) quarkonium closure.

Validates 6 Quarkonium Theorems (T-QK-1 through T-QK-6), the quarkonium
ladder (J/ψ → Υ → η_t), Tier-1 identity universality, and the confinement
bridge connecting to T3 (geometric slaughter at phase boundaries).

Test count target: ~82 tests covering:
    - Tier-1 identity universality (duality, integrity bound, log-bridge)
    - Quarkonium ladder kernel statistics
    - 6 theorem proofs with subtests (31 total)
    - Confinement bridge diagnostics
    - Edge cases and frozen constants
"""

from __future__ import annotations

import math

import pytest

from closures.standard_model.subatomic_kernel import (
    COMPOSITE_PARTICLES,
    compute_composite_kernel,
    normalize_composite,
)
from closures.standard_model.toponium import (
    QUARKONIUM_COUPLING,
    QUARKONIUM_LADDER,
    THRESHOLD_MEASUREMENTS,
    TOPONIUM,
    QuarkoniumKernelResult,
    TheoremResult,
    compute_quarkonium_kernel,
    compute_quarkonium_ladder,
    quarkonium_confinement_bridge,
    run_all_quarkonium_theorems,
    theorem_TQK1_quarkonium_ic_monotone,
    theorem_TQK2_toponium_geometric_slaughter,
    theorem_TQK3_binding_coupling_correlation,
    theorem_TQK4_quarkonium_tier1_universality,
    theorem_TQK5_asymptotic_freedom_in_ic,
    theorem_TQK6_threshold_cross_section,
)

EPSILON = 1e-6  # Guard band matching subatomic_kernel.py


# ═══════════════════════════════════════════════════════════════
# FIXTURES
# ═══════════════════════════════════════════════════════════════


@pytest.fixture(scope="module")
def ladder() -> list[QuarkoniumKernelResult]:
    """Compute quarkonium ladder once for entire test module."""
    return compute_quarkonium_ladder()


@pytest.fixture(scope="module")
def toponium_kernel() -> QuarkoniumKernelResult:
    """Compute toponium kernel once."""
    return compute_quarkonium_kernel(TOPONIUM)


@pytest.fixture(scope="module")
def all_theorems() -> list[TheoremResult]:
    """Run all 6 theorems once."""
    return run_all_quarkonium_theorems()


@pytest.fixture(scope="module")
def bridge() -> dict:
    """Compute confinement bridge once."""
    return quarkonium_confinement_bridge()


# ═══════════════════════════════════════════════════════════════
# SECTION 1: DATA CATALOG
# ═══════════════════════════════════════════════════════════════


class TestDataCatalog:
    """Validate the static data structures."""

    def test_toponium_mass(self) -> None:
        assert TOPONIUM.mass_GeV == pytest.approx(345.38, abs=0.01)

    def test_toponium_charge_neutral(self) -> None:
        assert TOPONIUM.charge_e == 0.0

    def test_toponium_spin_pseudoscalar(self) -> None:
        assert TOPONIUM.spin == 0.0

    def test_toponium_width_weak_decay(self) -> None:
        # Width ≈ 2 × Γ_t → ~2.84 GeV
        assert TOPONIUM.width_GeV == pytest.approx(2.84, abs=0.1)

    def test_quarkonium_ladder_length(self) -> None:
        assert len(QUARKONIUM_LADDER) == 3

    def test_quarkonium_ladder_names(self) -> None:
        names = [p.name for p in QUARKONIUM_LADDER]
        assert names == ["J/psi", "Upsilon", "Toponium"]

    def test_quarkonium_ladder_mass_order(self) -> None:
        masses = [p.mass_GeV for p in QUARKONIUM_LADDER]
        assert masses[0] < masses[1] < masses[2]

    def test_quarkonium_all_mesons(self) -> None:
        for p in QUARKONIUM_LADDER:
            assert p.hadron_type == "Meson"
            assert p.n_valence_quarks == 2

    def test_quarkonium_coupling_entries(self) -> None:
        assert len(QUARKONIUM_COUPLING) == 3
        for name in ("J/psi", "Upsilon", "Toponium"):
            assert name in QUARKONIUM_COUPLING

    def test_alpha_s_decreasing(self) -> None:
        vals = [QUARKONIUM_COUPLING[n]["alpha_s"] for n in ("J/psi", "Upsilon", "Toponium")]
        assert vals[0] > vals[1] > vals[2]

    def test_threshold_measurements(self) -> None:
        assert len(THRESHOLD_MEASUREMENTS) == 3
        for _key, m in THRESHOLD_MEASUREMENTS.items():
            assert m["sigma_pb"] > 0
            assert m["sigma_err_pb"] > 0
            assert m["significance_sigma"] >= 5.0


# ═══════════════════════════════════════════════════════════════
# SECTION 2: KERNEL COMPUTATION
# ═══════════════════════════════════════════════════════════════


class TestKernelComputation:
    """Validate kernel outputs for individual quarkonia."""

    def test_ladder_length(self, ladder: list[QuarkoniumKernelResult]) -> None:
        assert len(ladder) == 3

    def test_toponium_regime_collapse(self, toponium_kernel: QuarkoniumKernelResult) -> None:
        assert toponium_kernel.regime == "Collapse"

    def test_toponium_omega_above_030(self, toponium_kernel: QuarkoniumKernelResult) -> None:
        assert toponium_kernel.omega >= 0.30

    def test_toponium_IC_extremely_low(self, toponium_kernel: QuarkoniumKernelResult) -> None:
        # Geometric slaughter: 5 dead channels → IC near ε
        assert toponium_kernel.IC < 0.001

    def test_toponium_IC_over_F_tiny(self, toponium_kernel: QuarkoniumKernelResult) -> None:
        assert toponium_kernel.IC_over_F < 0.01

    def test_all_quarkonium_collapse(self, ladder: list[QuarkoniumKernelResult]) -> None:
        for r in ladder:
            assert r.regime == "Collapse", f"{r.name} should be Collapse"

    @pytest.mark.parametrize("idx", [0, 1, 2])
    def test_duality_identity(self, ladder: list[QuarkoniumKernelResult], idx: int) -> None:
        r = ladder[idx]
        assert r.F_plus_omega == pytest.approx(1.0, abs=1e-10)

    @pytest.mark.parametrize("idx", [0, 1, 2])
    def test_integrity_bound(self, ladder: list[QuarkoniumKernelResult], idx: int) -> None:
        r = ladder[idx]
        assert r.IC <= r.F + 1e-10

    @pytest.mark.parametrize("idx", [0, 1, 2])
    def test_log_bridge(self, ladder: list[QuarkoniumKernelResult], idx: int) -> None:
        r = ladder[idx]
        assert pytest.approx(math.exp(r.kappa), rel=1e-6) == r.IC

    def test_ic_monotone_decrease(self, ladder: list[QuarkoniumKernelResult]) -> None:
        ics = [r.IC for r in ladder]
        assert ics[0] > ics[1] > ics[2]

    def test_ic_over_f_monotone_decrease(self, ladder: list[QuarkoniumKernelResult]) -> None:
        ratios = [r.IC_over_F for r in ladder]
        assert ratios[0] > ratios[1] > ratios[2]


# ═══════════════════════════════════════════════════════════════
# SECTION 3: CHANNEL ANALYSIS
# ═══════════════════════════════════════════════════════════════


class TestChannelAnalysis:
    """Test channel-level properties of toponium."""

    def test_toponium_channels_near_epsilon(self) -> None:
        c, _w, _labels = normalize_composite(TOPONIUM)
        near_eps = sum(1 for v in c if v < 0.01)
        assert near_eps >= 4, f"Expected ≥4 dead channels, got {near_eps}"

    def test_toponium_mass_log_near_max(self) -> None:
        c, _w, _labels = normalize_composite(TOPONIUM)
        assert float(c[0]) > 0.90, "mass_log channel should be near-maximal"

    def test_toponium_charge_near_eps(self) -> None:
        c, _w, _labels = normalize_composite(TOPONIUM)
        # charge_abs is second channel
        assert float(c[1]) < 0.01

    def test_toponium_spin_near_eps(self) -> None:
        c, _w, _labels = normalize_composite(TOPONIUM)
        # spin_norm is third channel
        assert float(c[2]) < 0.01


# ═══════════════════════════════════════════════════════════════
# SECTION 4: THEOREM PROOFS
# ═══════════════════════════════════════════════════════════════


class TestTheoremTQK1:
    """T-QK-1: Quarkonium IC Monotone Decrease."""

    def test_proven(self) -> None:
        result = theorem_TQK1_quarkonium_ic_monotone()
        assert result.verdict == "PROVEN"

    def test_subtests(self) -> None:
        result = theorem_TQK1_quarkonium_ic_monotone()
        assert result.n_passed == result.n_tests == 4

    def test_ic_jpsi_gt_upsilon(self, ladder: list[QuarkoniumKernelResult]) -> None:
        assert ladder[0].IC > ladder[1].IC

    def test_ic_upsilon_gt_toponium(self, ladder: list[QuarkoniumKernelResult]) -> None:
        assert ladder[1].IC > ladder[2].IC


class TestTheoremTQK2:
    """T-QK-2: Toponium Geometric Slaughter."""

    def test_proven(self) -> None:
        result = theorem_TQK2_toponium_geometric_slaughter()
        assert result.verdict == "PROVEN"

    def test_subtests(self) -> None:
        result = theorem_TQK2_toponium_geometric_slaughter()
        assert result.n_passed == result.n_tests == 5

    def test_lowest_ic_among_composites(self, toponium_kernel: QuarkoniumKernelResult) -> None:
        all_ics = [compute_composite_kernel(p).IC for p in COMPOSITE_PARTICLES]
        assert min(all_ics) + 1e-12 >= toponium_kernel.IC


class TestTheoremTQK3:
    """T-QK-3: Binding-α_s Correlation."""

    def test_proven(self) -> None:
        result = theorem_TQK3_binding_coupling_correlation()
        assert result.verdict == "PROVEN"

    def test_subtests(self) -> None:
        result = theorem_TQK3_binding_coupling_correlation()
        assert result.n_passed == result.n_tests == 4

    def test_toponium_width_dwarfs_others(self) -> None:
        widths = [p.width_GeV for p in QUARKONIUM_LADDER]
        assert widths[2] / widths[0] > 1e3


class TestTheoremTQK4:
    """T-QK-4: Quarkonium Tier-1 Universality."""

    def test_proven(self) -> None:
        result = theorem_TQK4_quarkonium_tier1_universality()
        assert result.verdict == "PROVEN"

    def test_subtests(self) -> None:
        result = theorem_TQK4_quarkonium_tier1_universality()
        assert result.n_passed == result.n_tests == 9


class TestTheoremTQK5:
    """T-QK-5: Asymptotic Freedom in IC."""

    def test_proven(self) -> None:
        result = theorem_TQK5_asymptotic_freedom_in_ic()
        assert result.verdict == "PROVEN"

    def test_subtests(self) -> None:
        result = theorem_TQK5_asymptotic_freedom_in_ic()
        assert result.n_passed == result.n_tests == 4

    def test_toponium_deepest_collapse(self, ladder: list[QuarkoniumKernelResult]) -> None:
        assert ladder[2].omega > ladder[0].omega
        assert ladder[2].omega > ladder[1].omega


class TestTheoremTQK6:
    """T-QK-6: Cross-Section Threshold Enhancement."""

    def test_proven(self) -> None:
        result = theorem_TQK6_threshold_cross_section()
        assert result.verdict == "PROVEN"

    def test_subtests(self) -> None:
        result = theorem_TQK6_threshold_cross_section()
        assert result.n_passed == result.n_tests == 5

    def test_all_above_5_sigma(self) -> None:
        for key, m in THRESHOLD_MEASUREMENTS.items():
            assert m["significance_sigma"] >= 5.0, f"{key} below 5σ"


# ═══════════════════════════════════════════════════════════════
# SECTION 5: CONFINEMENT BRIDGE
# ═══════════════════════════════════════════════════════════════


class TestConfinementBridge:
    """Validate cross-reference to T3 confinement theorem."""

    def test_bridge_has_entries(self, bridge: dict) -> None:
        assert "sequence" in bridge
        assert len(bridge["sequence"]) == 3

    def test_bridge_alpha_s_decreasing(self, bridge: dict) -> None:
        alphas = [e["alpha_s"] for e in bridge["sequence"]]
        assert alphas[0] > alphas[1] > alphas[2]

    def test_bridge_ic_decreasing(self, bridge: dict) -> None:
        ics = [e["IC"] for e in bridge["sequence"]]
        assert ics[0] > ics[1] > ics[2]

    def test_bridge_all_collapse(self, bridge: dict) -> None:
        for e in bridge["sequence"]:
            assert e["regime"] == "Collapse"


# ═══════════════════════════════════════════════════════════════
# SECTION 6: MASTER RUNNER INTEGRATION
# ═══════════════════════════════════════════════════════════════


class TestMasterRunner:
    """Validate run_all_quarkonium_theorems."""

    def test_all_six_theorems(self, all_theorems: list[TheoremResult]) -> None:
        assert len(all_theorems) == 6

    def test_all_proven(self, all_theorems: list[TheoremResult]) -> None:
        for t in all_theorems:
            assert t.verdict == "PROVEN", f"{t.name} is {t.verdict}"

    def test_total_subtests(self, all_theorems: list[TheoremResult]) -> None:
        total = sum(t.n_passed for t in all_theorems)
        assert total == 31

    @pytest.mark.parametrize(
        "idx,name",
        [
            (0, "T-QK-1"),
            (1, "T-QK-2"),
            (2, "T-QK-3"),
            (3, "T-QK-4"),
            (4, "T-QK-5"),
            (5, "T-QK-6"),
        ],
    )
    def test_theorem_name(self, all_theorems: list[TheoremResult], idx: int, name: str) -> None:
        assert name in all_theorems[idx].name
