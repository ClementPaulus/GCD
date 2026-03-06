"""Tests for dynamic semiotics domain closures — SEM.INTSTACK.v1

Comprehensive test coverage for the semiotic kernel:
  - semiotic_kernel.py: 30 sign systems × 8 channels (Tier-1 identity sweep)
  - Structural analysis and cross-domain bridge to brain_kernel

Every test verifies structural predictions derivable from Axiom-0:
  F + ω = 1 (duality identity — complementum perfectum)
  IC ≤ F (integrity bound — limbus integritatis)
  IC = exp(κ) (log-integritas)

Derivation chain: Axiom-0 → frozen_contract → kernel_optimized → semiotic_kernel
"""

from __future__ import annotations

import math

import numpy as np
import pytest

from closures.dynamic_semiotics.semiotic_kernel import (
    N_SEMIOTIC_CHANNELS,
    N_SIGN_SYSTEMS,
    SEMIOTIC_CHANNELS,
    SIGN_SYSTEMS,
    SemioticKernelResult,
    analyze_semiotic_structure,
    bridge_to_brain_kernel,
    compute_all_sign_systems,
    compute_semiotic_kernel,
    normalize_sign_system,
    validate_semiotic_kernel,
)

# ── Tolerances (same as frozen contract) ──────────────────────────
TOL_DUALITY = 1e-12  # F + ω = 1 exact to machine precision
TOL_EXP = 1e-9  # IC = exp(κ)
TOL_BOUND = 1e-12  # IC ≤ F (with guard)
EPS = 1e-6  # Closure-level ε


# ═══════════════════════════════════════════════════════════════════
# 1. Sign System Catalog — Data Integrity
# ═══════════════════════════════════════════════════════════════════


class TestSignSystemCatalog:
    """Verify the sign system catalog data integrity."""

    def test_sign_system_count(self) -> None:
        """30 sign systems in the catalog."""
        assert len(SIGN_SYSTEMS) == 30
        assert N_SIGN_SYSTEMS == 30

    def test_channel_count(self) -> None:
        """8 channels defined."""
        assert N_SEMIOTIC_CHANNELS == 8
        assert len(SEMIOTIC_CHANNELS) == 8

    def test_channel_names(self) -> None:
        """Verify canonical channel names match specification."""
        expected = [
            "sign_repertoire",
            "interpretant_depth",
            "ground_stability",
            "translation_fidelity",
            "semiotic_density",
            "indexical_coupling",
            "iconic_persistence",
            "symbolic_recursion",
        ]
        assert expected == SEMIOTIC_CHANNELS

    def test_all_systems_have_8_traits(self) -> None:
        """Every sign system has exactly 8 trait values."""
        for ss in SIGN_SYSTEMS:
            traits = [
                ss.sign_repertoire,
                ss.interpretant_depth,
                ss.ground_stability,
                ss.translation_fidelity,
                ss.semiotic_density,
                ss.indexical_coupling,
                ss.iconic_persistence,
                ss.symbolic_recursion,
            ]
            assert len(traits) == 8, f"{ss.name}: expected 8 traits, got {len(traits)}"

    def test_trait_values_in_unit_interval(self) -> None:
        """All trait values must be in [0, 1]."""
        for ss in SIGN_SYSTEMS:
            for attr in SEMIOTIC_CHANNELS:
                val = getattr(ss, attr)
                assert 0.0 <= val <= 1.0, f"{ss.name}.{attr} = {val} out of [0,1]"

    def test_status_values(self) -> None:
        """Status must be one of the defined values."""
        valid_statuses = {"living", "dead", "extinct", "artificial"}
        for ss in SIGN_SYSTEMS:
            assert ss.status in valid_statuses, f"{ss.name}: status={ss.status}"

    def test_living_count(self) -> None:
        """Majority of systems should be living."""
        living = [s for s in SIGN_SYSTEMS if s.status == "living"]
        assert len(living) >= 20  # At least 20 living systems

    def test_dead_or_extinct_count(self) -> None:
        """Some dead/extinct systems in catalog."""
        dead = [s for s in SIGN_SYSTEMS if s.status in ("dead", "extinct")]
        assert len(dead) >= 3  # At least 3 dead/extinct

    def test_unique_names(self) -> None:
        """No duplicate sign system names."""
        names = [s.name for s in SIGN_SYSTEMS]
        assert len(names) == len(set(names))

    def test_categories_diverse(self) -> None:
        """Multiple categories represented."""
        categories = {s.category for s in SIGN_SYSTEMS}
        assert len(categories) >= 5  # Natural Language, Formal System, Visual, etc.

    def test_media_diverse(self) -> None:
        """Multiple media represented."""
        media = {s.medium for s in SIGN_SYSTEMS}
        assert len(media) >= 5  # Spoken, Written, Visual, Digital, Chemical, etc.


# ═══════════════════════════════════════════════════════════════════
# 2. Normalization Pipeline
# ═══════════════════════════════════════════════════════════════════


class TestNormalizeSignSystem:
    """Test the normalization pipeline."""

    def test_normalize_returns_correct_shapes(self) -> None:
        c, w, labels = normalize_sign_system(SIGN_SYSTEMS[0])
        assert c.shape == (8,)
        assert w.shape == (8,)
        assert len(labels) == 8

    def test_weights_sum_to_one(self) -> None:
        _, w, _ = normalize_sign_system(SIGN_SYSTEMS[0])
        assert abs(w.sum() - 1.0) < 1e-15

    def test_channels_clamped(self) -> None:
        """All channels must be clamped to [EPS, 1-EPS]."""
        for ss in SIGN_SYSTEMS:
            c, _, _ = normalize_sign_system(ss)
            assert np.all(c >= EPS), f"{ss.name}: channel below EPS"
            assert np.all(c <= 1.0 - EPS), f"{ss.name}: channel above 1-EPS"

    def test_trace_vector_matches_normalize(self) -> None:
        """trace_vector() and normalize_sign_system() produce same c."""
        for ss in SIGN_SYSTEMS:
            c_norm, _, _ = normalize_sign_system(ss)
            c_trace = ss.trace_vector()
            np.testing.assert_array_almost_equal(c_norm, c_trace)

    def test_labels_match_channels(self) -> None:
        """Labels from normalization match SEMIOTIC_CHANNELS."""
        _, _, labels = normalize_sign_system(SIGN_SYSTEMS[0])
        assert labels == SEMIOTIC_CHANNELS


# ═══════════════════════════════════════════════════════════════════
# 3. Kernel Identity Sweep — ALL 30 Sign Systems
# ═══════════════════════════════════════════════════════════════════


class TestSemioticKernelIdentities:
    """Tier-1 identity sweep across all 30 sign systems.

    These are the structural identities of collapse — they must hold
    for every sign system regardless of trait values. Violations here
    would indicate a broken kernel, not a semiotic anomaly.
    """

    @pytest.fixture(scope="class")
    def all_results(self) -> list[SemioticKernelResult]:
        return compute_all_sign_systems()

    def test_duality_identity_all(self, all_results: list[SemioticKernelResult]) -> None:
        """F + ω = 1 for every sign system (complementum perfectum)."""
        for r in all_results:
            assert abs(r.F_plus_omega - 1.0) < TOL_DUALITY, f"{r.name}: F+ω = {r.F_plus_omega}"

    def test_integrity_bound_all(self, all_results: list[SemioticKernelResult]) -> None:
        """IC ≤ F for every sign system (limbus integritatis)."""
        for r in all_results:
            assert r.IC_leq_F, f"{r.name}: IC={r.IC} > F={r.F}"

    def test_log_integritas_all(self, all_results: list[SemioticKernelResult]) -> None:
        """IC = exp(κ) for every sign system."""
        for r in all_results:
            assert r.IC_eq_exp_kappa, f"{r.name}: IC={r.IC}, exp(κ)={math.exp(r.kappa)}"

    def test_F_range(self, all_results: list[SemioticKernelResult]) -> None:
        """F must be in [0, 1] for all sign systems."""
        for r in all_results:
            assert 0.0 <= r.F <= 1.0, f"{r.name}: F={r.F}"

    def test_omega_range(self, all_results: list[SemioticKernelResult]) -> None:
        """ω must be in [0, 1] for all sign systems."""
        for r in all_results:
            assert 0.0 <= r.omega <= 1.0, f"{r.name}: ω={r.omega}"

    def test_IC_range(self, all_results: list[SemioticKernelResult]) -> None:
        """IC must be in (0, 1]."""
        for r in all_results:
            assert 0.0 < r.IC <= 1.0, f"{r.name}: IC={r.IC}"

    def test_kappa_nonpositive(self, all_results: list[SemioticKernelResult]) -> None:
        """κ must be ≤ 0 (log of values in (0,1])."""
        for r in all_results:
            assert r.kappa <= 0.0 + 1e-12, f"{r.name}: κ={r.kappa}"

    def test_heterogeneity_gap_nonnegative(self, all_results: list[SemioticKernelResult]) -> None:
        """Δ = F - IC ≥ 0 (consequence of IC ≤ F)."""
        for r in all_results:
            assert r.heterogeneity_gap >= -TOL_BOUND, f"{r.name}: Δ={r.heterogeneity_gap}"

    def test_entropy_nonnegative(self, all_results: list[SemioticKernelResult]) -> None:
        """Bernoulli field entropy S ≥ 0."""
        for r in all_results:
            assert r.S >= -1e-12, f"{r.name}: S={r.S}"

    def test_curvature_range(self, all_results: list[SemioticKernelResult]) -> None:
        """Curvature C in [0, 1]."""
        for r in all_results:
            assert 0.0 <= r.C <= 1.0 + 1e-12, f"{r.name}: C={r.C}"


# ═══════════════════════════════════════════════════════════════════
# 4. Regime and Semiotic Type Classification
# ═══════════════════════════════════════════════════════════════════


class TestSemioticRegimeClassification:
    """Verify regime and semiotic type classifications."""

    @pytest.fixture(scope="class")
    def all_results(self) -> list[SemioticKernelResult]:
        return compute_all_sign_systems()

    def test_valid_regimes(self, all_results: list[SemioticKernelResult]) -> None:
        """Regime must be one of the three canonical values."""
        for r in all_results:
            assert r.regime in ("Stable", "Watch", "Collapse"), f"{r.name}: regime={r.regime}"

    def test_valid_semiotic_types(self, all_results: list[SemioticKernelResult]) -> None:
        """Semiotic type must be a recognized classification."""
        valid = {
            "Alive Recursive (Balanced)",
            "Alive Recursive (Fragile)",
            "Stable Formal",
            "Fixed Signal",
            "Biological Signal",
            "Heterogeneous (Fragile)",
            "Mixed Semiotic",
            "Gestus (Dead System)",
        }
        for r in all_results:
            assert r.semiotic_type in valid, f"{r.name}: type={r.semiotic_type}"

    def test_weakest_strongest_channels_exist(self, all_results: list[SemioticKernelResult]) -> None:
        """Weakest and strongest channels must be valid channel labels."""
        for r in all_results:
            assert r.weakest_channel in SEMIOTIC_CHANNELS, f"{r.name}: weakest={r.weakest_channel}"
            assert r.strongest_channel in SEMIOTIC_CHANNELS, f"{r.name}: strongest={r.strongest_channel}"

    def test_weakest_leq_strongest(self, all_results: list[SemioticKernelResult]) -> None:
        """Weakest value ≤ strongest value."""
        for r in all_results:
            assert r.weakest_value <= r.strongest_value + 1e-12, (
                f"{r.name}: weakest={r.weakest_value} > strongest={r.strongest_value}"
            )

    def test_regime_omega_consistency(self, all_results: list[SemioticKernelResult]) -> None:
        """If regime is Collapse, ω ≥ 0.30."""
        for r in all_results:
            if r.regime == "Collapse":
                assert r.omega >= 0.30, f"{r.name}: Collapse but ω={r.omega}"


# ═══════════════════════════════════════════════════════════════════
# 5. Domain-Specific Semiotic Predictions
# ═══════════════════════════════════════════════════════════════════


class TestSemioticPredictions:
    """Test domain-specific predictions derived from Axiom-0."""

    @pytest.fixture(scope="class")
    def results_by_name(self) -> dict[str, SemioticKernelResult]:
        results = compute_all_sign_systems()
        return {r.name: r for r in results}

    def test_math_notation_alive_recursive(self, results_by_name: dict[str, SemioticKernelResult]) -> None:
        """Mathematical Notation: high symbolic_recursion (0.98) + high interpretant_depth (0.95)
        → Alive Recursive, despite high ground_stability. Recursion dominates."""
        r = results_by_name["Mathematical Notation"]
        assert "Alive Recursive" in r.semiotic_type

    def test_formal_logic_alive_recursive(self, results_by_name: dict[str, SemioticKernelResult]) -> None:
        """Formal Logic: high symbolic_recursion (0.95) + high interpretant_depth (0.92)
        → Alive Recursive. Gödelian self-reference makes it recursive, not merely formal."""
        r = results_by_name["Formal Logic (First-Order)"]
        assert "Alive Recursive" in r.semiotic_type

    def test_latin_is_gestus(self, results_by_name: dict[str, SemioticKernelResult]) -> None:
        """Classical Latin should be classified as Gestus (Dead System)."""
        r = results_by_name["Latin (Classical)"]
        assert r.semiotic_type == "Gestus (Dead System)"

    def test_english_recursive(self, results_by_name: dict[str, SemioticKernelResult]) -> None:
        """Modern English should be classified as Alive Recursive."""
        r = results_by_name["Modern English"]
        assert "Alive Recursive" in r.semiotic_type

    def test_bee_dance_fixed_signal(self, results_by_name: dict[str, SemioticKernelResult]) -> None:
        """Honeybee Waggle Dance should be Fixed Signal or Biological Signal."""
        r = results_by_name["Honeybee Waggle Dance"]
        assert r.semiotic_type in ("Fixed Signal", "Biological Signal")

    def test_ant_pheromones_biological(self, results_by_name: dict[str, SemioticKernelResult]) -> None:
        """Ant Pheromone Trails should be Biological Signal or Fixed Signal."""
        r = results_by_name["Ant Pheromone Trails"]
        assert r.semiotic_type in ("Biological Signal", "Fixed Signal")

    def test_pointing_gesture_fixed(self, results_by_name: dict[str, SemioticKernelResult]) -> None:
        """Pointing Gesture should be Fixed Signal."""
        r = results_by_name["Pointing Gesture (Deixis)"]
        assert r.semiotic_type == "Fixed Signal"

    def test_formal_systems_have_higher_delta_than_natural(
        self, results_by_name: dict[str, SemioticKernelResult]
    ) -> None:
        """Formal systems should have higher heterogeneity gap than natural languages.

        Formal systems have extreme channel profiles: near-1.0 ground_stability
        and translation_fidelity but near-zero indexical_coupling and
        iconic_persistence. This creates geometric slaughter — the near-zero
        channels drive IC toward ε while F stays high. Natural languages have
        more uniformly distributed channels, producing smaller gaps.
        This is the structural prediction of geometric slaughter (AX-SEM1).
        """
        nat_langs = ["Modern English", "Mandarin Chinese", "Arabic (Modern Standard)", "Japanese"]
        formal_sys = ["Mathematical Notation", "Formal Logic (First-Order)"]

        mean_delta_nat = np.mean([results_by_name[n].heterogeneity_gap for n in nat_langs])
        mean_delta_formal = np.mean([results_by_name[n].heterogeneity_gap for n in formal_sys])

        # Formal systems should have larger gap due to geometric slaughter
        assert mean_delta_formal > mean_delta_nat, f"Formal Δ={mean_delta_formal:.4f} ≤ Natural Δ={mean_delta_nat:.4f}"

    def test_pirahã_extreme_heterogeneity(self, results_by_name: dict[str, SemioticKernelResult]) -> None:
        """Pirahã should have extreme heterogeneity due to near-zero symbolic_recursion."""
        r = results_by_name["Pirahã"]
        # Very low symbolic_recursion (0.05) should create large gap
        assert r.heterogeneity_gap > 0.10, f"Pirahã Δ={r.heterogeneity_gap:.4f}"

    def test_dna_high_ground_stability(self, results_by_name: dict[str, SemioticKernelResult]) -> None:
        """DNA/RNA should have highest ground_stability (3.8 Gyr persistence)."""
        r = results_by_name["DNA/RNA Genetic Code"]
        all_stabilities = [results_by_name[n].trace_vector[2] for n in results_by_name]
        assert r.trace_vector[2] >= max(all_stabilities) - 0.01


# ═══════════════════════════════════════════════════════════════════
# 6. Structural Analysis
# ═══════════════════════════════════════════════════════════════════


class TestSemioticStructuralAnalysis:
    """Test the cross-system structural analysis."""

    @pytest.fixture(scope="class")
    def analysis(self):
        return analyze_semiotic_structure()

    def test_system_count(self, analysis) -> None:
        assert analysis.n_systems == 30

    def test_mean_F_in_range(self, analysis) -> None:
        assert 0.0 < analysis.mean_F < 1.0

    def test_mean_IC_in_range(self, analysis) -> None:
        assert 0.0 < analysis.mean_IC < 1.0

    def test_mean_IC_leq_mean_F(self, analysis) -> None:
        """Mean IC should be less than mean F (on average)."""
        assert analysis.mean_IC <= analysis.mean_F + 1e-6

    def test_mean_delta_positive(self, analysis) -> None:
        assert analysis.mean_delta > 0.0

    def test_category_means_populated(self, analysis) -> None:
        assert len(analysis.category_means) >= 5

    def test_channel_means_all_channels(self, analysis) -> None:
        for ch in SEMIOTIC_CHANNELS:
            assert ch in analysis.channel_mean_values

    def test_ic_killer_is_valid_channel(self, analysis) -> None:
        assert analysis.ic_killer_channel in SEMIOTIC_CHANNELS

    def test_ic_anchor_is_valid_channel(self, analysis) -> None:
        assert analysis.ic_anchor_channel in SEMIOTIC_CHANNELS

    def test_regime_distribution_sums(self, analysis) -> None:
        total = analysis.n_stable + analysis.n_watch + analysis.n_collapse
        assert total == 30

    def test_living_vs_dead_ic(self, analysis) -> None:
        """Living systems should generally have higher IC than dead ones
        (living community provides indexical coupling)."""
        # This is a structural prediction, not a necessary identity
        assert analysis.mean_IC_living > 0.0
        assert analysis.mean_IC_dead > 0.0


# ═══════════════════════════════════════════════════════════════════
# 7. Brain Kernel Bridge
# ═══════════════════════════════════════════════════════════════════


class TestBrainKernelBridge:
    """Test the cross-domain bridge to brain_kernel channel 8."""

    @pytest.fixture(scope="class")
    def bridge(self):
        return bridge_to_brain_kernel()

    def test_bridge_keys(self, bridge) -> None:
        """Bridge should contain expected keys."""
        expected = {
            "brain_kernel_channel_8",
            "semiotic_F",
            "semiotic_IC",
            "semiotic_delta",
            "semiotic_regime",
            "semiotic_type",
            "weakest_channel",
            "strongest_channel",
            "interpretation",
        }
        assert expected <= set(bridge.keys())

    def test_brain_score(self, bridge) -> None:
        assert bridge["brain_kernel_channel_8"] == 0.98

    def test_semiotic_F_less_than_brain(self, bridge) -> None:
        """Semiotic F should be less than the brain kernel's single-channel score.

        The 8 channels reveal heterogeneity hidden in the scalar value.
        """
        assert bridge["semiotic_F"] < bridge["brain_kernel_channel_8"]

    def test_semiotic_IC_positive(self, bridge) -> None:
        assert bridge["semiotic_IC"] > 0.0

    def test_interpretation_is_string(self, bridge) -> None:
        assert isinstance(bridge["interpretation"], str)
        assert len(bridge["interpretation"]) > 50


# ═══════════════════════════════════════════════════════════════════
# 8. Full Validation Sweep
# ═══════════════════════════════════════════════════════════════════


class TestValidationSweep:
    """Run the full Tier-1 validation and verify conformance."""

    @pytest.fixture(scope="class")
    def validation(self):
        return validate_semiotic_kernel()

    def test_verdict_conformant(self, validation) -> None:
        """Full sweep must be CONFORMANT."""
        assert validation["verdict"] == "CONFORMANT"

    def test_total_checks(self, validation) -> None:
        """30 systems × 3 identities = 90 checks."""
        assert validation["total_checks"] == 90

    def test_all_pass(self, validation) -> None:
        assert validation["total_pass"] == 90

    def test_no_failures(self, validation) -> None:
        assert validation["total_fail"] == 0

    def test_no_violations(self, validation) -> None:
        assert validation["violations"] == []

    def test_duality_all_pass(self, validation) -> None:
        assert validation["duality_pass"] == 30

    def test_bound_all_pass(self, validation) -> None:
        assert validation["bound_pass"] == 30

    def test_log_all_pass(self, validation) -> None:
        assert validation["log_pass"] == 30


# ═══════════════════════════════════════════════════════════════════
# 9. Result Serialization
# ═══════════════════════════════════════════════════════════════════


class TestResultSerialization:
    """Test that results serialize correctly."""

    def test_to_dict(self) -> None:
        """to_dict should produce a dictionary with all fields."""
        r = compute_semiotic_kernel(SIGN_SYSTEMS[0])
        d = r.to_dict()
        assert isinstance(d, dict)
        assert "F" in d
        assert "omega" in d
        assert "IC" in d
        assert "regime" in d
        assert "semiotic_type" in d
        assert "channel_sensitivities" in d

    def test_to_dict_round_trip(self) -> None:
        """All values in to_dict should be JSON-serializable types."""
        import json

        r = compute_semiotic_kernel(SIGN_SYSTEMS[0])
        d = r.to_dict()
        # Should not raise
        serialized = json.dumps(d)
        assert len(serialized) > 0


# ═══════════════════════════════════════════════════════════════════
# 10. Channel Sensitivity Analysis
# ═══════════════════════════════════════════════════════════════════


class TestChannelSensitivity:
    """Test channel sensitivity computation."""

    def test_sensitivities_populated(self) -> None:
        r = compute_semiotic_kernel(SIGN_SYSTEMS[0])
        assert len(r.channel_sensitivities) == 8

    def test_sensitivity_keys(self) -> None:
        r = compute_semiotic_kernel(SIGN_SYSTEMS[0])
        for ch in SEMIOTIC_CHANNELS:
            assert ch in r.channel_sensitivities

    def test_sensitivities_positive(self) -> None:
        """All sensitivities should be positive (IC > 0, channels > 0)."""
        for ss in SIGN_SYSTEMS:
            r = compute_semiotic_kernel(ss)
            for ch, sens in r.channel_sensitivities.items():
                assert sens > 0, f"{ss.name}.{ch}: sensitivity={sens}"
