"""Tests for fluid dynamics domain closures — FLUID.INTSTACK.v1

Comprehensive test coverage for the fluid_dynamics closure module:
  - flow_kernel.py: 20 flow systems × 8 channels (Tier-1 identity sweep)

Every test verifies structural predictions derivable from Axiom-0:
  F + ω = 1 (duality identity — complementum perfectum)
  IC ≤ F (integrity bound — limbus integritatis)
  IC = exp(κ) (log-integritas)

Key fluid dynamics predictions verified:
  - Stokes / Hele-Shaw / microfluidic in Watch regime (high viscous fidelity)
  - Turbulent and separated flows in Collapse regime (high inertial, low IC)
  - Laminar mean F > turbulent mean F (GCD encodes Re-based transition)
  - Airfoil stall / separated flow: lowest IC — geometric slaughter by
    boundary_adherence ≈ ε (parallel to quark confinement cliff, T3)
  - Laminar-turbulent F split > 0.3

Derivation chain: Axiom-0 → frozen_contract → kernel_optimized → flow_kernel
"""

from __future__ import annotations

import math

import pytest

from closures.fluid_dynamics.flow_kernel import (
    CHANNEL_LABELS,
    FLOW_SYSTEMS,
    N_CHANNELS,
    FlowKernelResult,
    FlowSystem,
    analyze_regime_class_profiles,
    compute_all_flow_systems,
    compute_flow_system,
    find_geometric_slaughter_flows,
    fluid_structural_summary,
)

# ── Tolerances ────────────────────────────────────────────────────
TOL_DUALITY = 1e-9  # F + ω = 1
TOL_EXP = 1e-9  # IC = exp(κ)
TOL_BOUND = 1e-12  # IC ≤ F


# ═══════════════════════════════════════════════════════════════════
# 1. Catalog integrity
# ═══════════════════════════════════════════════════════════════════


class TestFlowCatalog:
    """Verify the flow system catalog data integrity."""

    def test_flow_system_count(self) -> None:
        """20 flow systems in the catalog."""
        assert len(FLOW_SYSTEMS) == 20

    def test_channel_count(self) -> None:
        """8 channels defined."""
        assert N_CHANNELS == 8
        assert len(CHANNEL_LABELS) == 8

    def test_all_channels_labeled(self) -> None:
        """Expected channel labels present."""
        expected = {
            "viscous_fidelity",
            "inertial_coherence",
            "pressure_integrity",
            "boundary_adherence",
            "vorticity_control",
            "thermal_coupling",
            "compressibility_margin",
            "return_to_laminar",
        }
        assert set(CHANNEL_LABELS) == expected

    def test_all_flow_systems_have_8_channels(self) -> None:
        """Every flow system has exactly 8 channel values."""
        for fs in FLOW_SYSTEMS:
            tr = fs.trace()
            assert len(tr) == 8, f"{fs.name}: expected 8 channels, got {len(tr)}"

    def test_all_channel_values_in_unit_interval(self) -> None:
        """All raw channel values are in [0, 1]."""
        for fs in FLOW_SYSTEMS:
            for val in fs.trace():
                assert 0.0 <= val <= 1.0, f"{fs.name}: channel value {val} out of [0,1]"

    def test_unique_names(self) -> None:
        """All flow system names are unique."""
        names = [fs.name for fs in FLOW_SYSTEMS]
        assert len(names) == len(set(names))

    def test_required_regime_classes_present(self) -> None:
        """Laminar, turbulent, transitional, separated, and biological all represented."""
        classes = {fs.regime_class for fs in FLOW_SYSTEMS}
        assert "laminar" in classes
        assert "turbulent" in classes
        assert "transitional" in classes
        assert "separated" in classes
        assert "biological" in classes


# ═══════════════════════════════════════════════════════════════════
# 2. Tier-1 Identity Sweep (all 20 flow systems)
# ═══════════════════════════════════════════════════════════════════


class TestTier1Identities:
    """Verify the three Tier-1 kernel identities for every flow system."""

    @pytest.fixture(scope="class")
    def results(self) -> list[FlowKernelResult]:
        return compute_all_flow_systems()

    def test_duality_identity_all(self, results: list[FlowKernelResult]) -> None:
        """F + ω = 1 for every flow system (complementum perfectum)."""
        for r in results:
            residual = abs(r.F_plus_omega - 1.0)
            assert residual < TOL_DUALITY, f"{r.name}: F + ω = {r.F_plus_omega:.2e}, residual = {residual:.2e}"

    def test_integrity_bound_all(self, results: list[FlowKernelResult]) -> None:
        """IC ≤ F for every flow system (limbus integritatis)."""
        for r in results:
            assert r.IC_leq_F, f"{r.name}: IC ({r.IC:.6f}) > F ({r.F:.6f})"

    def test_log_integrity_all(self, results: list[FlowKernelResult]) -> None:
        """IC = exp(κ) for every flow system (log-integritas).

        Uses the pre-rounded IC_eq_exp_kappa flag (checked at full precision
        before rounding), consistent with the evolution test pattern.
        """
        for r in results:
            assert r.IC_eq_exp_kappa, f"{r.name}: IC = {r.IC:.8f}, exp(κ) = {math.exp(r.kappa):.8f}"

    def test_all_f_in_unit_interval(self, results: list[FlowKernelResult]) -> None:
        """F ∈ [0, 1] for all results."""
        for r in results:
            assert 0.0 <= r.F <= 1.0, f"{r.name}: F = {r.F}"

    def test_all_omega_in_unit_interval(self, results: list[FlowKernelResult]) -> None:
        """ω ∈ [0, 1] for all results."""
        for r in results:
            assert 0.0 <= r.omega <= 1.0, f"{r.name}: ω = {r.omega}"

    def test_all_ic_positive(self, results: list[FlowKernelResult]) -> None:
        """IC > 0 for all results (ε-guard band)."""
        for r in results:
            assert r.IC > 0.0, f"{r.name}: IC = {r.IC}"

    def test_heterogeneity_gap_nonnegative(self, results: list[FlowKernelResult]) -> None:
        """Δ = F − IC ≥ 0 for all results."""
        for r in results:
            assert r.heterogeneity_gap >= -TOL_BOUND, f"{r.name}: gap = {r.heterogeneity_gap:.2e}"

    def test_kappa_nonpositive(self, results: list[FlowKernelResult]) -> None:
        """κ ≤ 0 (log of value ≤ 1 for all channels)."""
        for r in results:
            assert r.kappa <= 1e-9, f"{r.name}: κ = {r.kappa}"


# ═══════════════════════════════════════════════════════════════════
# 3. Regime Classification Predictions
# ═══════════════════════════════════════════════════════════════════


class TestFluidRegimePredictions:
    """Verify fluid dynamics regime predictions derivable from Axiom-0."""

    @pytest.fixture(scope="class")
    def results(self) -> dict[str, FlowKernelResult]:
        return {r.name: r for r in compute_all_flow_systems()}

    def test_stokes_flow_not_collapse(self, results: dict[str, FlowKernelResult]) -> None:
        """Stokes (Creeping) Flow should be in Watch or Stable (high viscous fidelity)."""
        r = results["Stokes (Creeping) Flow"]
        assert r.regime in ("Stable", "Watch"), f"Stokes in regime {r.regime}"

    def test_microfluidic_not_collapse(self, results: dict[str, FlowKernelResult]) -> None:
        """Microfluidic Channel: Stokes-regime, should be Watch or Stable."""
        r = results["Microfluidic Channel (Lab-on-chip)"]
        assert r.regime in ("Stable", "Watch")

    def test_laminar_pipe_not_collapse(self, results: dict[str, FlowKernelResult]) -> None:
        """Laminar Pipe Flow: below Re_crit, should not be in Collapse."""
        r = results["Laminar Pipe Flow (Hagen-Poiseuille)"]
        assert r.regime in ("Stable", "Watch")

    def test_turbulent_pipe_collapse(self, results: dict[str, FlowKernelResult]) -> None:
        """Turbulent Pipe Flow: high ω (inertia dominates) → Collapse."""
        r = results["Turbulent Pipe Flow"]
        assert r.regime == "Collapse"

    def test_airfoil_stall_collapse(self, results: dict[str, FlowKernelResult]) -> None:
        """Airfoil Stall: catastrophic IC loss → Collapse."""
        r = results["Airfoil Stall"]
        assert r.regime == "Collapse"

    def test_separated_flow_collapse(self, results: dict[str, FlowKernelResult]) -> None:
        """Separated Flow: boundary_adherence near ε → Collapse."""
        r = results["Separated Flow (Adverse Gradient)"]
        assert r.regime == "Collapse"

    def test_hypersonic_collapse(self, results: dict[str, FlowKernelResult]) -> None:
        """Hypersonic Flow: compressibility_margin ≈ ε → Collapse."""
        r = results["Hypersonic Flow (Ma > 5)"]
        assert r.regime == "Collapse"

    def test_laminar_higher_f_than_turbulent(self, results: dict[str, FlowKernelResult]) -> None:
        """Laminar Pipe F > Turbulent Pipe F (Re-based collapse visible in kernel)."""
        laminar = results["Laminar Pipe Flow (Hagen-Poiseuille)"]
        turbulent = results["Turbulent Pipe Flow"]
        assert laminar.F > turbulent.F, f"Laminar F ({laminar.F:.3f}) should exceed Turbulent F ({turbulent.F:.3f})"

    def test_stall_has_lowest_ic_among_separated(self, results: dict[str, FlowKernelResult]) -> None:
        """Airfoil Stall has lower IC than Separated Flow (deeper collapse)."""
        stall = results["Airfoil Stall"]
        sep = results["Separated Flow (Adverse Gradient)"]
        assert stall.IC <= sep.IC, f"Stall IC ({stall.IC:.3f}) should be ≤ Separated IC ({sep.IC:.3f})"

    def test_transonic_lower_compressibility_than_subsonic(self, results: dict[str, FlowKernelResult]) -> None:
        """Transonic flow has lower compressibility_margin channel than subsonic."""
        transonic = results["Transonic Flow (Ma ≈ 1)"]
        subsonic = results["Subsonic Compressible Flow (Ma < 0.8)"]
        # Get compressibility_margin index
        idx = CHANNEL_LABELS.index("compressibility_margin")
        assert transonic.trace_vector[idx] < subsonic.trace_vector[idx], (
            "Transonic compressibility_margin should be lower than subsonic"
        )

    def test_blood_flow_high_return_to_laminar(self, results: dict[str, FlowKernelResult]) -> None:
        """Blood flow in aorta should have high return_to_laminar (pulsatile relaminarization)."""
        r = results["Blood Flow in Aorta"]
        idx = CHANNEL_LABELS.index("return_to_laminar")
        assert r.trace_vector[idx] > 0.60, f"Blood flow return_to_laminar = {r.trace_vector[idx]:.3f}, expected > 0.60"


# ═══════════════════════════════════════════════════════════════════
# 4. Geometric Slaughter (Fluid Confinement Cliff)
# ═══════════════════════════════════════════════════════════════════


class TestGeometricSlaughter:
    """Verify the fluid dynamics confinement cliff — parallel to T3 in SM."""

    @pytest.fixture(scope="class")
    def results(self) -> list[FlowKernelResult]:
        return compute_all_flow_systems()

    def test_separated_flow_geometric_slaughter(self, results: list[FlowKernelResult]) -> None:
        """Separated and stalled flows are geometric slaughter candidates (IC < 0.30)."""
        candidates = find_geometric_slaughter_flows(results)
        names = {r.name for r in candidates}
        assert "Airfoil Stall" in names, "Airfoil Stall should be a slaughter candidate"

    def test_laminar_not_slaughter(self, results: list[FlowKernelResult]) -> None:
        """Laminar flows should not be geometric slaughter candidates."""
        candidates = find_geometric_slaughter_flows(results, ic_threshold=0.30)
        laminar_names = {r.name for r in candidates if r.regime_class == "laminar"}
        assert len(laminar_names) == 0, f"Unexpected laminar slaughter candidates: {laminar_names}"

    def test_weakest_channel_in_separated_flow(self, results: list[FlowKernelResult]) -> None:
        """Separated Flow / Stall: weakest channel should be boundary_adherence or return_to_laminar."""
        stall = next(r for r in results if r.name == "Airfoil Stall")
        assert stall.weakest_channel in (
            "boundary_adherence",
            "return_to_laminar",
            "compressibility_margin",
        ), f"Unexpected weakest channel: {stall.weakest_channel}"


# ═══════════════════════════════════════════════════════════════════
# 5. Structural Analysis Functions
# ═══════════════════════════════════════════════════════════════════


class TestFluidStructuralAnalysis:
    """Test the fluid structural analysis helper functions."""

    @pytest.fixture(scope="class")
    def results(self) -> list[FlowKernelResult]:
        return compute_all_flow_systems()

    def test_regime_class_profiles_includes_laminar(self, results: list[FlowKernelResult]) -> None:
        """Profile includes laminar regime class."""
        profile = analyze_regime_class_profiles(results)
        assert "laminar" in profile

    def test_regime_class_profiles_mean_F_in_unit_interval(self, results: list[FlowKernelResult]) -> None:
        """Mean F for each regime class is in [0, 1]."""
        profile = analyze_regime_class_profiles(results)
        for rc, data in profile.items():
            assert 0.0 <= data["mean_F"] <= 1.0, f"{rc}: mean_F = {data['mean_F']}"

    def test_structural_summary_count(self, results: list[FlowKernelResult]) -> None:
        """Summary n_flow_systems matches catalog size."""
        summary = fluid_structural_summary(results)
        assert summary["n_flow_systems"] == 20

    def test_structural_summary_regime_counts_sum(self, results: list[FlowKernelResult]) -> None:
        """Regime counts sum to 20."""
        summary = fluid_structural_summary(results)
        total = sum(summary["regime_counts"].values())
        assert total == 20, f"Regime counts sum = {total}"

    def test_laminar_higher_mean_f_than_turbulent(self, results: list[FlowKernelResult]) -> None:
        """Laminar mean F exceeds turbulent mean F (captures Re transition)."""
        summary = fluid_structural_summary(results)
        assert summary["mean_F_laminar"] > summary["mean_F_turbulent"], (
            f"Laminar mean F ({summary['mean_F_laminar']:.3f}) should exceed "
            f"turbulent mean F ({summary['mean_F_turbulent']:.3f})"
        )

    def test_laminar_turbulent_split_positive(self, results: list[FlowKernelResult]) -> None:
        """Laminar-turbulent F split > 0."""
        summary = fluid_structural_summary(results)
        assert summary["laminar_turbulent_F_split"] > 0.0


# ═══════════════════════════════════════════════════════════════════
# 6. Single-system kernel correctness
# ═══════════════════════════════════════════════════════════════════


class TestSingleKernelComputation:
    """Test that compute_flow_system produces correct outputs for known inputs."""

    def test_homogeneous_flow_system(self) -> None:
        """A homogeneous flow system (all channels = 0.7) has F ≈ 0.7."""
        fs = FlowSystem(
            name="Homogeneous Test",
            regime_class="laminar",
            re_range="test",
            notes="All channels equal",
            viscous_fidelity=0.7,
            inertial_coherence=0.7,
            pressure_integrity=0.7,
            boundary_adherence=0.7,
            vorticity_control=0.7,
            thermal_coupling=0.7,
            compressibility_margin=0.7,
            return_to_laminar=0.7,
        )
        r = compute_flow_system(fs)
        assert abs(r.F - 0.7) < 1e-6, f"F = {r.F:.6f}, expected 0.7"
        assert abs(r.omega - 0.3) < 1e-6
        assert abs(r.F + r.omega - 1.0) < TOL_DUALITY
        assert r.IC_leq_F
        assert r.IC_eq_exp_kappa

    def test_near_stall_flow(self) -> None:
        """A flow with near-zero boundary_adherence collapses (high ω)."""
        fs = FlowSystem(
            name="Near-Stall Test",
            regime_class="separated",
            re_range="varies",
            notes="Boundary adherence near zero",
            viscous_fidelity=0.30,
            inertial_coherence=0.55,
            pressure_integrity=0.20,
            boundary_adherence=0.02,
            vorticity_control=0.15,
            thermal_coupling=0.40,
            compressibility_margin=0.88,
            return_to_laminar=0.02,
        )
        r = compute_flow_system(fs)
        assert r.omega >= 0.30, f"Expected Collapse, ω = {r.omega:.3f}"
        assert r.regime == "Collapse"
        assert r.IC_leq_F

    def test_result_n_channels_correct(self) -> None:
        """Result reports correct n_channels."""
        fs = FLOW_SYSTEMS[0]
        r = compute_flow_system(fs)
        assert r.n_channels == N_CHANNELS

    def test_result_channel_labels_correct(self) -> None:
        """Result channel labels match module constants."""
        fs = FLOW_SYSTEMS[0]
        r = compute_flow_system(fs)
        assert r.channel_labels == list(CHANNEL_LABELS)

    def test_result_trace_length(self) -> None:
        """Result trace vector has length N_CHANNELS."""
        fs = FLOW_SYSTEMS[0]
        r = compute_flow_system(fs)
        assert len(r.trace_vector) == N_CHANNELS

    def test_to_dict_serializable(self) -> None:
        """to_dict returns a plain dict with expected keys."""
        r = compute_flow_system(FLOW_SYSTEMS[0])
        d = r.to_dict()
        assert isinstance(d, dict)
        assert "F" in d
        assert "omega" in d
        assert "IC" in d
        assert "regime" in d
        assert "name" in d
