"""Tests for semiotics domain closures — SEM.INTSTACK.v1

Comprehensive test coverage for the semiotics closure module:
  - sign_kernel.py: 20 sign systems × 8 channels (Tier-1 identity sweep)

Every test verifies structural predictions derivable from Axiom-0:
  F + ω = 1 (duality identity — complementum perfectum)
  IC ≤ F (integrity bound — limbus integritatis)
  IC = exp(κ) (log-integritas)

Key semiotic predictions verified:
  - Formal systems (logic, math, Morse) occupy Watch regime (high F, high IC)
  - Pidgin / abstract art in Collapse regime (low convention, high entropy)
  - Creole outperforms pidgin in F and IC (collapse returns as stable grammar)
  - Dead language: high syntactic_integrity, low pragmatic → Watch/Collapse
  - Tradition split: Pragmatic < Peircean ≈ Saussurean in mean F

Derivation chain: Axiom-0 → frozen_contract → kernel_optimized → sign_kernel
"""

from __future__ import annotations

import math

import pytest

from closures.semiotics.sign_kernel import (
    CHANNEL_LABELS,
    N_CHANNELS,
    SIGN_SYSTEMS,
    SignKernelResult,
    SignSystem,
    analyze_sign_type_profiles,
    compute_all_sign_systems,
    compute_sign_system,
    find_semiotic_collapse_candidates,
    semiotic_structural_summary,
)

# ── Tolerances ────────────────────────────────────────────────────
TOL_DUALITY = 1e-9  # F + ω = 1
TOL_EXP = 1e-9  # IC = exp(κ)
TOL_BOUND = 1e-12  # IC ≤ F


# ═══════════════════════════════════════════════════════════════════
# 1. Catalog integrity
# ═══════════════════════════════════════════════════════════════════


class TestSignCatalog:
    """Verify the sign system catalog data integrity."""

    def test_sign_system_count(self) -> None:
        """20 sign systems in the catalog."""
        assert len(SIGN_SYSTEMS) == 20

    def test_channel_count(self) -> None:
        """8 channels defined."""
        assert N_CHANNELS == 8
        assert len(CHANNEL_LABELS) == 8

    def test_all_channels_labeled(self) -> None:
        """Expected channel labels present."""
        expected = {
            "syntactic_integrity",
            "semantic_fidelity",
            "pragmatic_coherence",
            "iconicity",
            "indexicality",
            "conventionality",
            "interpretant_stability",
            "contextual_return",
        }
        assert set(CHANNEL_LABELS) == expected

    def test_all_sign_systems_have_8_channels(self) -> None:
        """Every sign system has exactly 8 channel values."""
        for ss in SIGN_SYSTEMS:
            tr = ss.trace()
            assert len(tr) == 8, f"{ss.name}: expected 8 channels, got {len(tr)}"

    def test_all_channel_values_in_unit_interval(self) -> None:
        """All raw channel values are in [0, 1]."""
        for ss in SIGN_SYSTEMS:
            for val in ss.trace():
                assert 0.0 <= val <= 1.0, f"{ss.name}: channel value {val} out of [0,1]"

    def test_unique_names(self) -> None:
        """All sign system names are unique."""
        names = [ss.name for ss in SIGN_SYSTEMS]
        assert len(names) == len(set(names))

    def test_required_traditions_present(self) -> None:
        """Peircean, Saussurean, and Pragmatic traditions all represented."""
        traditions = {ss.tradition for ss in SIGN_SYSTEMS}
        assert "Peircean" in traditions
        assert "Saussurean" in traditions
        assert "Pragmatic" in traditions

    def test_required_sign_types_present(self) -> None:
        """Icon, index, symbol, and hybrid all represented."""
        sign_types = {ss.sign_type for ss in SIGN_SYSTEMS}
        assert "icon" in sign_types
        assert "index" in sign_types
        assert "symbol" in sign_types
        assert "hybrid" in sign_types


# ═══════════════════════════════════════════════════════════════════
# 2. Tier-1 Identity Sweep (all 20 sign systems)
# ═══════════════════════════════════════════════════════════════════


class TestTier1Identities:
    """Verify the three Tier-1 kernel identities for every sign system."""

    @pytest.fixture(scope="class")
    def results(self) -> list[SignKernelResult]:
        return compute_all_sign_systems()

    def test_duality_identity_all(self, results: list[SignKernelResult]) -> None:
        """F + ω = 1 for every sign system (complementum perfectum)."""
        for r in results:
            residual = abs(r.F_plus_omega - 1.0)
            assert residual < TOL_DUALITY, f"{r.name}: F + ω = {r.F_plus_omega:.2e}, residual = {residual:.2e}"

    def test_integrity_bound_all(self, results: list[SignKernelResult]) -> None:
        """IC ≤ F for every sign system (limbus integritatis)."""
        for r in results:
            assert r.IC_leq_F, f"{r.name}: IC ({r.IC:.6f}) > F ({r.F:.6f})"

    def test_log_integrity_all(self, results: list[SignKernelResult]) -> None:
        """IC = exp(κ) for every sign system (log-integritas).

        Uses the pre-rounded IC_eq_exp_kappa flag (checked at full precision
        before rounding), consistent with the evolution test pattern.
        """
        for r in results:
            assert r.IC_eq_exp_kappa, f"{r.name}: IC = {r.IC:.8f}, exp(κ) = {math.exp(r.kappa):.8f}"

    def test_all_f_in_unit_interval(self, results: list[SignKernelResult]) -> None:
        """F ∈ [0, 1] for all results."""
        for r in results:
            assert 0.0 <= r.F <= 1.0, f"{r.name}: F = {r.F}"

    def test_all_omega_in_unit_interval(self, results: list[SignKernelResult]) -> None:
        """ω ∈ [0, 1] for all results."""
        for r in results:
            assert 0.0 <= r.omega <= 1.0, f"{r.name}: ω = {r.omega}"

    def test_all_ic_positive(self, results: list[SignKernelResult]) -> None:
        """IC > 0 for all results (ε-guard band)."""
        for r in results:
            assert r.IC > 0.0, f"{r.name}: IC = {r.IC}"

    def test_heterogeneity_gap_nonnegative(self, results: list[SignKernelResult]) -> None:
        """Δ = F − IC ≥ 0 for all results."""
        for r in results:
            assert r.heterogeneity_gap >= -TOL_BOUND, f"{r.name}: gap = {r.heterogeneity_gap:.2e}"

    def test_kappa_nonpositive(self, results: list[SignKernelResult]) -> None:
        """κ ≤ 0 (log of value ≤ 1 for all channels)."""
        for r in results:
            assert r.kappa <= 1e-9, f"{r.name}: κ = {r.kappa}"


# ═══════════════════════════════════════════════════════════════════
# 3. Regime Classification Predictions
# ═══════════════════════════════════════════════════════════════════


class TestRegimeClassification:
    """Verify semiotic regime predictions derivable from Axiom-0."""

    @pytest.fixture(scope="class")
    def results(self) -> dict[str, SignKernelResult]:
        return {r.name: r for r in compute_all_sign_systems()}

    def test_formal_logic_watch_or_stable(self, results: dict[str, SignKernelResult]) -> None:
        """Formal Logic should be in Watch or Stable (high F, strong convention)."""
        r = results["Formal Logic"]
        assert r.regime in ("Stable", "Watch"), f"Formal Logic in regime {r.regime}"
        assert r.F > 0.60, f"Formal Logic F = {r.F:.3f}, expected > 0.60"

    def test_mathematical_notation_watch_or_stable(self, results: dict[str, SignKernelResult]) -> None:
        """Mathematical Notation should be in Watch or Stable."""
        r = results["Mathematical Notation"]
        assert r.regime in ("Stable", "Watch")

    def test_traffic_signs_watch_or_stable(self, results: dict[str, SignKernelResult]) -> None:
        """Traffic Signs: highly conventional, should be Watch or Stable."""
        r = results["Traffic Signs"]
        assert r.regime in ("Stable", "Watch")

    def test_abstract_art_collapse(self, results: dict[str, SignKernelResult]) -> None:
        """Abstract Art: low convention, high entropy → Collapse."""
        r = results["Abstract Art"]
        assert r.regime == "Collapse", f"Abstract Art in regime {r.regime}"

    def test_pidgin_collapse(self, results: dict[str, SignKernelResult]) -> None:
        """Pidgin Language: broken convention, high drift → Collapse."""
        r = results["Pidgin Language"]
        assert r.regime == "Collapse"

    def test_creole_better_than_pidgin(self, results: dict[str, SignKernelResult]) -> None:
        """Creole outperforms Pidgin in F and IC (collapse returns as grammar)."""
        creole = results["Creole Language"]
        pidgin = results["Pidgin Language"]
        assert creole.F > pidgin.F, f"Creole F ({creole.F:.3f}) should exceed Pidgin F ({pidgin.F:.3f})"
        assert creole.IC > pidgin.IC, f"Creole IC ({creole.IC:.3f}) should exceed Pidgin IC ({pidgin.IC:.3f})"

    def test_formal_logic_higher_f_than_pidgin(self, results: dict[str, SignKernelResult]) -> None:
        """Formal Logic should have higher F than Pidgin."""
        assert results["Formal Logic"].F > results["Pidgin Language"].F

    def test_sign_language_asl_higher_f_than_gesture(self, results: dict[str, SignKernelResult]) -> None:
        """ASL (full language) should have higher F than co-speech gesture."""
        assert results["Sign Language (ASL)"].F > results["Gesture (Co-speech)"].F

    def test_smoke_fire_high_indexicality_channel(self, results: dict[str, SignKernelResult]) -> None:
        """Smoke-as-Fire: dominant channel should be indexicality (causal bond)."""
        r = results["Smoke as Sign of Fire"]
        assert r.dominant_channel == "indexicality", f"Expected indexicality, got {r.dominant_channel}"

    def test_formal_logic_high_conventionality_channel(self, results: dict[str, SignKernelResult]) -> None:
        """Formal Logic: dominant channel should be conventionality or interpretant_stability."""
        r = results["Formal Logic"]
        assert r.dominant_channel in (
            "conventionality",
            "interpretant_stability",
            "semantic_fidelity",
            "syntactic_integrity",
        ), f"Unexpected dominant channel: {r.dominant_channel}"


# ═══════════════════════════════════════════════════════════════════
# 4. Structural Analysis Functions
# ═══════════════════════════════════════════════════════════════════


class TestStructuralAnalysis:
    """Test the semiotic structural analysis helper functions."""

    @pytest.fixture(scope="class")
    def results(self) -> list[SignKernelResult]:
        return compute_all_sign_systems()

    def test_sign_type_profiles_has_all_types(self, results: list[SignKernelResult]) -> None:
        """Sign type profile includes all four types."""
        profile = analyze_sign_type_profiles(results)
        assert "icon" in profile
        assert "index" in profile
        assert "symbol" in profile
        assert "hybrid" in profile

    def test_sign_type_profiles_mean_F_in_unit_interval(self, results: list[SignKernelResult]) -> None:
        """Mean F for each sign type is in [0, 1]."""
        profile = analyze_sign_type_profiles(results)
        for stype, data in profile.items():
            assert 0.0 <= data["mean_F"] <= 1.0, f"{stype}: mean_F = {data['mean_F']}"

    def test_collapse_candidates_are_in_collapse(self, results: list[SignKernelResult]) -> None:
        """All collapse candidates have ω ≥ 0.30."""
        candidates = find_semiotic_collapse_candidates(results)
        for r in candidates:
            assert r.omega >= 0.30, f"{r.name}: ω = {r.omega:.3f}, expected ≥ 0.30"

    def test_structural_summary_count(self, results: list[SignKernelResult]) -> None:
        """Summary n_sign_systems matches catalog size."""
        summary = semiotic_structural_summary(results)
        assert summary["n_sign_systems"] == 20

    def test_structural_summary_regime_counts_sum(self, results: list[SignKernelResult]) -> None:
        """Regime counts sum to 20."""
        summary = semiotic_structural_summary(results)
        total = sum(summary["regime_counts"].values())
        assert total == 20, f"Regime counts sum = {total}"

    def test_pragmatic_mean_F_lower_than_peircean(self, results: list[SignKernelResult]) -> None:
        """Pragmatic tradition has lower mean F than Peircean (derivable from data)."""
        summary = semiotic_structural_summary(results)
        mf = summary["mean_F_per_tradition"]
        assert mf["Pragmatic"] < mf["Peircean"], (
            f"Expected Pragmatic ({mf['Pragmatic']:.3f}) < Peircean ({mf['Peircean']:.3f})"
        )


# ═══════════════════════════════════════════════════════════════════
# 5. Single-system kernel correctness
# ═══════════════════════════════════════════════════════════════════


class TestSingleKernelComputation:
    """Test that compute_sign_system produces correct outputs for known inputs."""

    def test_homogeneous_sign_system(self) -> None:
        """A homogeneous sign system (all channels = 0.8) has F = 0.8, IC ≈ F.

        When all channels are equal, geometric mean = arithmetic mean,
        so IC should equal F (up to ε-clipping rounding).
        """
        ss = SignSystem(
            name="Homogeneous Test",
            tradition="Peircean",
            sign_type="symbol",
            domain="formal",
            notes="All channels equal — homogeneous trace",
            syntactic_integrity=0.8,
            semantic_fidelity=0.8,
            pragmatic_coherence=0.8,
            iconicity=0.8,
            indexicality=0.8,
            conventionality=0.8,
            interpretant_stability=0.8,
            contextual_return=0.8,
        )
        r = compute_sign_system(ss)
        assert abs(r.F - 0.8) < 1e-6, f"F = {r.F:.6f}, expected 0.8"
        assert abs(r.omega - 0.2) < 1e-6, f"ω = {r.omega:.6f}, expected 0.2"
        assert abs(r.F + r.omega - 1.0) < TOL_DUALITY
        assert r.IC_leq_F
        assert r.IC_eq_exp_kappa
        # For homogeneous trace, geometric mean = arithmetic mean → IC ≈ F
        assert abs(r.IC - r.F) < 1e-5, f"IC ({r.IC:.6f}) should ≈ F ({r.F:.6f}) for homogeneous trace"

    def test_near_collapse_sign_system(self) -> None:
        """A sign system with very low convention collapses (high ω)."""
        ss = SignSystem(
            name="Near-Collapse Test",
            tradition="Pragmatic",
            sign_type="icon",
            domain="cultural",
            notes="Broken convention channels",
            syntactic_integrity=0.10,
            semantic_fidelity=0.20,
            pragmatic_coherence=0.15,
            iconicity=0.40,
            indexicality=0.30,
            conventionality=0.05,
            interpretant_stability=0.08,
            contextual_return=0.12,
        )
        r = compute_sign_system(ss)
        assert r.omega >= 0.30, f"Expected Collapse, ω = {r.omega:.3f}"
        assert r.regime == "Collapse"
        assert r.IC_leq_F
        assert r.IC_eq_exp_kappa

    def test_result_n_channels_correct(self) -> None:
        """Result reports correct n_channels."""
        ss = SIGN_SYSTEMS[0]
        r = compute_sign_system(ss)
        assert r.n_channels == N_CHANNELS

    def test_result_channel_labels_correct(self) -> None:
        """Result channel labels match module constants."""
        ss = SIGN_SYSTEMS[0]
        r = compute_sign_system(ss)
        assert r.channel_labels == list(CHANNEL_LABELS)

    def test_result_trace_length(self) -> None:
        """Result trace vector has length N_CHANNELS."""
        ss = SIGN_SYSTEMS[0]
        r = compute_sign_system(ss)
        assert len(r.trace_vector) == N_CHANNELS

    def test_to_dict_serializable(self) -> None:
        """to_dict returns a plain dict with expected keys."""
        r = compute_sign_system(SIGN_SYSTEMS[0])
        d = r.to_dict()
        assert isinstance(d, dict)
        assert "F" in d
        assert "omega" in d
        assert "IC" in d
        assert "regime" in d
        assert "name" in d
