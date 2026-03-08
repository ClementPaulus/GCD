"""Tests for RHIC Quark-Gluon Plasma closure — qgp_rhic.py.

Validates 10 QGP theorems (T-QGP-1 through T-QGP-10), 27 entity
constructions across 4 categories (BES, centrality, evolution, reference),
Tier-1 identity universality, trace vector construction, and narrative
generation.

Test count target: ~170 tests covering:
    - Frozen QCD constants (T_c, T_H, KSS bound, etc.)
    - BES entity construction (8 energy scan points)
    - Centrality entity construction (9 bins at 200 GeV)
    - Evolution entity construction (8 time stages)
    - Reference entity construction (2 baselines)
    - Trace vector channel normalization
    - 10 theorem proofs with subtests
    - Tier-1 identity universality (F+ω=1, IC≤F, IC=exp(κ))
    - Regime classification
    - Narrative generation
    - Full analysis integration
    - Edge cases
"""

from __future__ import annotations

import math

import numpy as np
import pytest

from closures.nuclear_physics.qgp_rhic import (
    AU_A,
    AU_Z,
    BES_DATA,
    CENTRALITY_DATA,
    CHANNEL_NAMES,
    CS2_CONFORMAL,
    EPSILON_0_GEV_FM3,
    EPSILON_C_GEV_FM3,
    ETA_OVER_S_KSS,
    EVOLUTION_DATA,
    MU_B_SCALE_MEV,
    REFERENCE_DATA,
    RHO_0_FM3,
    SIGMA_NN_MB,
    SQRT_S_MAX_GEV,
    T_C_MEV,
    T_HAGEDORN_MEV,
    V2_SCALE,
    QGPAnalysisResult,
    QGPObservables,
    build_all_entities,
    build_bes_entities,
    build_centrality_entities,
    build_evolution_entities,
    build_reference_entities,
    build_trace,
    run_full_analysis,
)
from umcp.frozen_contract import EPSILON

# ═══════════════════════════════════════════════════════════════
# FIXTURES
# ═══════════════════════════════════════════════════════════════


@pytest.fixture(scope="module")
def full_analysis():
    """Run full analysis once for the entire test module."""
    return run_full_analysis()


@pytest.fixture(scope="module")
def bes_entities():
    """Build BES entities once."""
    return build_bes_entities()


@pytest.fixture(scope="module")
def centrality_entities():
    """Build centrality entities once."""
    return build_centrality_entities()


@pytest.fixture(scope="module")
def evolution_entities():
    """Build evolution entities once."""
    return build_evolution_entities()


@pytest.fixture(scope="module")
def reference_entities():
    """Build reference entities once."""
    return build_reference_entities()


@pytest.fixture(scope="module")
def all_entities():
    """Build all entities once."""
    return build_all_entities()


# ═══════════════════════════════════════════════════════════════
# FROZEN CONSTANTS
# ═══════════════════════════════════════════════════════════════


class TestFrozenConstants:
    """Verify frozen QCD / RHIC constants."""

    def test_critical_temperature(self):
        assert T_C_MEV == 155.0

    def test_hagedorn_temperature(self):
        assert T_HAGEDORN_MEV == 176.0

    def test_critical_energy_density(self):
        assert EPSILON_C_GEV_FM3 == 0.5

    def test_kss_bound(self):
        assert abs(ETA_OVER_S_KSS - 1.0 / (4.0 * math.pi)) < 1e-12

    def test_rho_0(self):
        assert RHO_0_FM3 == 0.16

    def test_epsilon_0(self):
        assert EPSILON_0_GEV_FM3 == 0.15

    def test_sigma_nn(self):
        assert SIGMA_NN_MB == 42.0

    def test_sqrt_s_max(self):
        assert SQRT_S_MAX_GEV == 200.0

    def test_gold_mass_number(self):
        assert AU_A == 197

    def test_gold_atomic_number(self):
        assert AU_Z == 79

    def test_mu_b_scale(self):
        assert MU_B_SCALE_MEV == 550.0

    def test_v2_scale(self):
        assert V2_SCALE == 0.08

    def test_cs2_conformal(self):
        assert abs(CS2_CONFORMAL - 1.0 / 3.0) < 1e-12

    def test_channel_count(self):
        assert len(CHANNEL_NAMES) == 8


# ═══════════════════════════════════════════════════════════════
# DATA TABLE INTEGRITY
# ═══════════════════════════════════════════════════════════════


class TestDataTables:
    """Verify data table structure and consistency."""

    def test_bes_count(self):
        assert len(BES_DATA) == 8

    def test_centrality_count(self):
        assert len(CENTRALITY_DATA) == 9

    def test_evolution_count(self):
        assert len(EVOLUTION_DATA) == 8

    def test_reference_count(self):
        assert len(REFERENCE_DATA) == 2

    @pytest.mark.parametrize("idx", range(8))
    def test_bes_energy_ordering(self, idx):
        if idx < 7:
            assert BES_DATA[idx]["sqrt_s"] < BES_DATA[idx + 1]["sqrt_s"]

    @pytest.mark.parametrize("idx", range(9))
    def test_centrality_npart_ordering(self, idx):
        if idx < 8:
            assert CENTRALITY_DATA[idx]["N_part"] > CENTRALITY_DATA[idx + 1]["N_part"]

    @pytest.mark.parametrize("idx", range(8))
    def test_evolution_tau_ordering(self, idx):
        if idx < 7:
            assert EVOLUTION_DATA[idx]["tau_fm_c"] < EVOLUTION_DATA[idx + 1]["tau_fm_c"]

    def test_bes_temperature_trend(self):
        """T_ch should generally increase with √s."""
        T_vals = [d["T_MeV"] for d in BES_DATA]
        assert T_vals[-1] > T_vals[0]

    def test_bes_mu_b_trend(self):
        """μ_B should decrease with √s."""
        mu_vals = [d["mu_B_MeV"] for d in BES_DATA]
        assert mu_vals[0] > mu_vals[-1]

    def test_bes_gamma_s_range(self):
        """All γ_s in (0, 1]."""
        for d in BES_DATA:
            assert 0 < d["gamma_s"] <= 1.0

    def test_centrality_dNch_range(self):
        """Multiplicity should decrease with centrality."""
        mults = [d["dNch_deta"] for d in CENTRALITY_DATA]
        assert mults[0] > mults[-1]


# ═══════════════════════════════════════════════════════════════
# TRACE VECTOR CONSTRUCTION
# ═══════════════════════════════════════════════════════════════


class TestTraceVector:
    """Test trace vector construction and normalization."""

    def test_trace_shape(self):
        obs = QGPObservables(200, 100, 5.0, 0.06, 0.3, 0.9, 500, 0.8)
        c, w = build_trace(obs)
        assert c.shape == (8,)
        assert w.shape == (8,)

    def test_weights_sum(self):
        obs = QGPObservables(200, 100, 5.0, 0.06, 0.3, 0.9, 500, 0.8)
        _, w = build_trace(obs)
        assert abs(w.sum() - 1.0) < 1e-12

    def test_trace_bounds(self):
        obs = QGPObservables(200, 100, 5.0, 0.06, 0.3, 0.9, 500, 0.8)
        c, _ = build_trace(obs)
        for val in c:
            assert EPSILON <= val <= 1.0 - EPSILON

    def test_extreme_low(self):
        """Near-zero inputs should clip to ε."""
        obs = QGPObservables(0.001, 0.001, 0.001, 0.0, 1.0, 0.0, 0, 0.0)
        c, _ = build_trace(obs)
        for val in c:
            assert val >= EPSILON

    def test_extreme_high(self):
        """Maximum inputs should clip to 1-ε."""
        obs = QGPObservables(500, 550, 100, 0.1, 0.0, 1.0, 2000, 1.0)
        c, _ = build_trace(obs)
        for val in c:
            assert val <= 1.0 - EPSILON

    def test_channel_names(self):
        assert CHANNEL_NAMES[0] == "temperature_frac"
        assert CHANNEL_NAMES[4] == "opacity"
        assert CHANNEL_NAMES[7] == "deconfinement"


# ═══════════════════════════════════════════════════════════════
# ENTITY CONSTRUCTION
# ═══════════════════════════════════════════════════════════════


class TestBESEntities:
    """Test BES entity construction."""

    def test_count(self, bes_entities):
        assert len(bes_entities) == 8

    def test_category(self, bes_entities):
        for e in bes_entities:
            assert e.category == "bes"

    @pytest.mark.parametrize("idx", range(8))
    def test_has_kernel_outputs(self, bes_entities, idx):
        e = bes_entities[idx]
        assert 0 < e.F <= 1
        assert 0 <= e.omega < 1
        assert e.IC > 0
        assert e.kappa <= 0

    @pytest.mark.parametrize("idx", range(8))
    def test_trace_length(self, bes_entities, idx):
        assert len(bes_entities[idx].trace) == 8

    @pytest.mark.parametrize("idx", range(8))
    def test_channels_list(self, bes_entities, idx):
        assert bes_entities[idx].channels == CHANNEL_NAMES


class TestCentralityEntities:
    """Test centrality entity construction."""

    def test_count(self, centrality_entities):
        assert len(centrality_entities) == 9

    def test_category(self, centrality_entities):
        for e in centrality_entities:
            assert e.category == "centrality"

    def test_all_200gev(self, centrality_entities):
        for e in centrality_entities:
            assert e.sqrt_s_GeV == 200.0

    @pytest.mark.parametrize("idx", range(9))
    def test_has_kernel_outputs(self, centrality_entities, idx):
        e = centrality_entities[idx]
        assert 0 < e.F <= 1
        assert e.IC > 0

    def test_metadata_has_npart(self, centrality_entities):
        for e in centrality_entities:
            assert "N_part" in e.metadata


class TestEvolutionEntities:
    """Test evolution entity construction."""

    def test_count(self, evolution_entities):
        assert len(evolution_entities) == 8

    def test_category(self, evolution_entities):
        for e in evolution_entities:
            assert e.category == "evolution"

    def test_metadata_has_tau(self, evolution_entities):
        for e in evolution_entities:
            assert "tau_fm_c" in e.metadata

    def test_pre_collision_low_f(self, evolution_entities):
        pre = evolution_entities[0]
        assert pre.F < 0.05

    def test_qgp_stages_high_f(self, evolution_entities):
        """Fully thermalized QGP should have high F."""
        for e in evolution_entities:
            if "QGP" in e.name and "Pre" not in e.name:
                assert e.F > 0.5


class TestReferenceEntities:
    """Test reference entity construction."""

    def test_count(self, reference_entities):
        assert len(reference_entities) == 2

    def test_category(self, reference_entities):
        for e in reference_entities:
            assert e.category == "reference"

    def test_pp_no_deconfinement(self, reference_entities):
        pp = reference_entities[0]
        assert pp.observables.deconfinement_frac == 0.0

    def test_dau_no_deconfinement(self, reference_entities):
        dau = reference_entities[1]
        assert dau.observables.deconfinement_frac == 0.0


class TestAllEntities:
    """Test combined entity set."""

    def test_total_count(self, all_entities):
        assert len(all_entities) == 27

    def test_category_breakdown(self, all_entities):
        cats = [e.category for e in all_entities]
        assert cats.count("bes") == 8
        assert cats.count("centrality") == 9
        assert cats.count("evolution") == 8
        assert cats.count("reference") == 2


# ═══════════════════════════════════════════════════════════════
# TIER-1 IDENTITY UNIVERSALITY
# ═══════════════════════════════════════════════════════════════


class TestTier1:
    """Universal Tier-1 identity checks across all entities."""

    @pytest.mark.parametrize("idx", range(27))
    def test_duality(self, all_entities, idx):
        """F + ω = 1 (duality identity)."""
        e = all_entities[idx]
        assert abs(e.F + e.omega - 1.0) < 1e-12

    @pytest.mark.parametrize("idx", range(27))
    def test_integrity_bound(self, all_entities, idx):
        """IC ≤ F (integrity bound)."""
        e = all_entities[idx]
        assert e.IC <= e.F + 1e-12

    @pytest.mark.parametrize("idx", range(27))
    def test_log_integrity(self, all_entities, idx):
        """IC = exp(κ) (log-integrity relation)."""
        e = all_entities[idx]
        assert abs(e.IC - math.exp(e.kappa)) < 1e-10

    @pytest.mark.parametrize("idx", range(27))
    def test_gap_nonneg(self, all_entities, idx):
        """Δ = F − IC ≥ 0."""
        e = all_entities[idx]
        assert e.gap >= -1e-12


# ═══════════════════════════════════════════════════════════════
# REGIME CLASSIFICATION
# ═══════════════════════════════════════════════════════════════


class TestRegime:
    """Test regime classification."""

    def test_pp_is_collapse(self, reference_entities):
        """p+p at 200 GeV → Collapse (ω > 0.3)."""
        pp = reference_entities[0]
        assert pp.regime == "Collapse"

    def test_pre_collision_is_collapse(self, evolution_entities):
        pre = evolution_entities[0]
        assert pre.regime == "Collapse"

    def test_valid_regimes(self, all_entities):
        for e in all_entities:
            assert e.regime in {"Stable", "Watch", "Collapse"}

    def test_some_watch(self, all_entities):
        """At least some entities should be in Watch regime."""
        watch = [e for e in all_entities if e.regime == "Watch"]
        assert len(watch) > 0

    def test_some_collapse(self, all_entities):
        """At least some entities should be in Collapse regime."""
        collapse = [e for e in all_entities if e.regime == "Collapse"]
        assert len(collapse) > 0


# ═══════════════════════════════════════════════════════════════
# THEOREM PROOFS
# ═══════════════════════════════════════════════════════════════


class TestTheoremQGP1:
    """T-QGP-1: Perfect Liquid Diagnostic."""

    def test_proven(self, full_analysis):
        t = full_analysis.theorem_results["T-QGP-1"]
        assert t["proven"]

    def test_peak_is_interior(self, full_analysis):
        t = full_analysis.theorem_results["T-QGP-1"]
        assert "0-5%" not in t["peak_centrality"]
        assert "70-80%" not in t["peak_centrality"]

    def test_peripheral_lowest(self, centrality_entities):
        ics = [e.IC for e in centrality_entities]
        assert ics[-1] == min(ics)


class TestTheoremQGP2:
    """T-QGP-2: Centrality Ordering."""

    def test_proven(self, full_analysis):
        t = full_analysis.theorem_results["T-QGP-2"]
        assert t["proven"]

    def test_central_vs_peripheral(self, full_analysis):
        t = full_analysis.theorem_results["T-QGP-2"]
        assert t["F_central"] > t["F_peripheral"]


class TestTheoremQGP3:
    """T-QGP-3: BES Energy Ordering."""

    def test_proven(self, full_analysis):
        t = full_analysis.theorem_results["T-QGP-3"]
        assert t["proven"]

    def test_f_increases(self, bes_entities):
        F_vals = [e.F for e in bes_entities]
        assert F_vals[-1] > F_vals[0]

    def test_delta_f_positive(self, full_analysis):
        t = full_analysis.theorem_results["T-QGP-3"]
        assert t["delta_F"] > 0


class TestTheoremQGP4:
    """T-QGP-4: Strangeness Equilibration."""

    def test_proven(self, full_analysis):
        t = full_analysis.theorem_results["T-QGP-4"]
        assert t["proven"]

    def test_positive_correlation(self, full_analysis):
        t = full_analysis.theorem_results["T-QGP-4"]
        assert t["spearman_rho"] > 0.5


class TestTheoremQGP5:
    """T-QGP-5: Reconfinement Gap Jump."""

    def test_proven(self, full_analysis):
        t = full_analysis.theorem_results["T-QGP-5"]
        assert t["proven"]

    def test_jump_substantial(self, full_analysis):
        t = full_analysis.theorem_results["T-QGP-5"]
        assert t["reconfinement_jump"] > 0.1


class TestTheoremQGP6:
    """T-QGP-6: Flow-Opacity Structure."""

    def test_proven(self, full_analysis):
        t = full_analysis.theorem_results["T-QGP-6"]
        assert t["proven"]

    def test_different_peaks(self, full_analysis):
        t = full_analysis.theorem_results["T-QGP-6"]
        assert t["v2_peak_centrality"] != t["opacity_peak_centrality"]


class TestTheoremQGP7:
    """T-QGP-7: Chemical Freeze-out Curve."""

    def test_proven(self, full_analysis):
        t = full_analysis.theorem_results["T-QGP-7"]
        assert t["proven"]

    def test_strong_anticorrelation(self, full_analysis):
        t = full_analysis.theorem_results["T-QGP-7"]
        assert t["spearman_rho"] < -0.9

    def test_near_tc(self, full_analysis):
        t = full_analysis.theorem_results["T-QGP-7"]
        assert abs(t["T_at_200GeV"] - T_C_MEV) < 15


class TestTheoremQGP8:
    """T-QGP-8: Reconfinement Cliff."""

    def test_proven(self, full_analysis):
        t = full_analysis.theorem_results["T-QGP-8"]
        assert t["proven"]

    def test_ic_drop(self, full_analysis):
        t = full_analysis.theorem_results["T-QGP-8"]
        assert t["IC_drop_frac"] > 0.30


class TestTheoremQGP9:
    """T-QGP-9: Reference Discrimination."""

    def test_proven(self, full_analysis):
        t = full_analysis.theorem_results["T-QGP-9"]
        assert t["proven"]

    def test_auau_higher_ic(self, full_analysis):
        t = full_analysis.theorem_results["T-QGP-9"]
        assert t["central_AuAu_IC"] > t["pp_IC"]


class TestTheoremQGP10:
    """T-QGP-10: Universal Tier-1."""

    def test_proven(self, full_analysis):
        t = full_analysis.theorem_results["T-QGP-10"]
        assert t["proven"]

    def test_all_subtests(self, full_analysis):
        t = full_analysis.theorem_results["T-QGP-10"]
        assert t["passed"] == t["tests"]

    def test_27_entities(self, full_analysis):
        t = full_analysis.theorem_results["T-QGP-10"]
        assert t["n_entities"] == 27


# ═══════════════════════════════════════════════════════════════
# FULL ANALYSIS
# ═══════════════════════════════════════════════════════════════


class TestFullAnalysis:
    """Integration tests for run_full_analysis()."""

    def test_result_type(self, full_analysis):
        assert isinstance(full_analysis, QGPAnalysisResult)

    def test_entity_counts(self, full_analysis):
        assert len(full_analysis.bes_entities) == 8
        assert len(full_analysis.centrality_entities) == 9
        assert len(full_analysis.evolution_entities) == 8
        assert len(full_analysis.reference_entities) == 2
        assert len(full_analysis.all_entities) == 27

    def test_zero_tier1_violations(self, full_analysis):
        assert full_analysis.tier1_violations == 0

    def test_theorems_count(self, full_analysis):
        assert len(full_analysis.theorem_results) == 10

    def test_all_proven(self, full_analysis):
        for tid, t in full_analysis.theorem_results.items():
            assert t["proven"], f"{tid} NOT PROVEN"

    def test_summary_keys(self, full_analysis):
        s = full_analysis.summary
        required = {
            "n_entities",
            "n_bes",
            "n_centrality",
            "n_evolution",
            "n_reference",
            "n_theorems_proven",
            "n_theorems_total",
            "mean_F",
            "mean_IC",
            "mean_gap",
            "F_range",
            "IC_range",
            "tier1_violations",
        }
        assert required.issubset(set(s.keys()))

    def test_summary_counts(self, full_analysis):
        s = full_analysis.summary
        assert s["n_entities"] == 27
        assert s["n_theorems_total"] == 10
        assert s["n_theorems_proven"] == 10

    def test_mean_f_in_range(self, full_analysis):
        s = full_analysis.summary
        assert 0.3 < s["mean_F"] < 0.8

    def test_mean_ic_in_range(self, full_analysis):
        s = full_analysis.summary
        assert 0.1 < s["mean_IC"] < 0.8

    def test_positive_gap(self, full_analysis):
        assert full_analysis.summary["mean_gap"] > 0


# ═══════════════════════════════════════════════════════════════
# NARRATIVE
# ═══════════════════════════════════════════════════════════════


class TestNarrative:
    """Test narrative generation."""

    def test_narrative_nonempty(self, full_analysis):
        assert len(full_analysis.narrative) > 100

    def test_has_prologue(self, full_analysis):
        assert "PROLOGUE" in full_analysis.narrative

    def test_has_acts(self, full_analysis):
        assert "ACT I" in full_analysis.narrative
        assert "ACT II" in full_analysis.narrative
        assert "ACT III" in full_analysis.narrative
        assert "ACT IV" in full_analysis.narrative

    def test_has_epilogue(self, full_analysis):
        assert "EPILOGUE" in full_analysis.narrative

    def test_has_theorem_scorecard(self, full_analysis):
        assert "THEOREM SCORECARD" in full_analysis.narrative

    def test_has_axiom(self, full_analysis):
        assert "Solum quod redit, reale est" in full_analysis.narrative


# ═══════════════════════════════════════════════════════════════
# KERNEL STATISTICS
# ═══════════════════════════════════════════════════════════════


class TestKernelStats:
    """Statistical properties of the QGP kernel analysis."""

    def test_bes_f_range(self, bes_entities):
        """BES F range spans at least 0.2."""
        Fs = [e.F for e in bes_entities]
        assert max(Fs) - min(Fs) > 0.2

    def test_centrality_f_range(self, centrality_entities):
        """Centrality F range spans at least 0.3."""
        Fs = [e.F for e in centrality_entities]
        assert max(Fs) - min(Fs) > 0.3

    def test_evolution_f_range(self, evolution_entities):
        """Evolution F range spans from near-zero to >0.5."""
        Fs = [e.F for e in evolution_entities]
        assert min(Fs) < 0.1
        assert max(Fs) > 0.5

    def test_reference_lower_ic(self, reference_entities, centrality_entities):
        """References have lower IC than central Au+Au."""
        ref_max_ic = max(e.IC for e in reference_entities)
        central_ic = centrality_entities[0].IC
        assert ref_max_ic < central_ic

    def test_watch_regime_in_bes(self, bes_entities):
        """Highest BES energy should be Watch (ω < 0.3)."""
        highest = bes_entities[-1]
        assert highest.regime == "Watch"

    def test_evolution_entropy(self, evolution_entities):
        """Entropy should be defined for all stages."""
        for e in evolution_entities:
            assert e.S >= 0

    def test_curvature_defined(self, all_entities):
        """Curvature should be >= 0 for all entities."""
        for e in all_entities:
            assert e.C >= 0


# ═══════════════════════════════════════════════════════════════
# EDGE CASES
# ═══════════════════════════════════════════════════════════════


class TestEdgeCases:
    """Edge case tests."""

    def test_zero_temperature_obs(self):
        """Pre-collision observable with T=0 should still produce valid trace."""
        obs = QGPObservables(0, 0, 0.15, 0.0, 1.0, 0.0, 0, 0.0)
        c, _w = build_trace(obs)
        assert all(c >= EPSILON)

    def test_max_temperature_obs(self):
        """Extremely high temperature should be clipped."""
        obs = QGPObservables(1000, 0, 100, 0.1, 0.0, 1.0, 5000, 1.0)
        c, _w = build_trace(obs)
        assert all(c <= 1.0 - EPSILON)

    def test_entity_has_correct_fields(self, all_entities):
        """All entities should have all required fields."""
        for e in all_entities:
            assert isinstance(e.name, str)
            assert isinstance(e.category, str)
            assert isinstance(e.trace, np.ndarray)
            assert isinstance(e.F, float)
            assert isinstance(e.omega, float)
            assert isinstance(e.regime, str)
