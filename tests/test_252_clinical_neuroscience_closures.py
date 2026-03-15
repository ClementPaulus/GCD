"""Tests for the clinical neuroscience Tier-2 closure.

Tests cover:
    - Entity catalog completeness and channel bounds (35 states, 10 channels)
    - Tier-1 identity verification for all 35 neurocognitive states
    - Structural analysis and category-level statistics
    - 10 theorems (T-CN-1 through T-CN-10)
    - Cross-category comparisons and regime classification
    - Formal bounds to machine precision

Derivation chain: Axiom-0 → frozen_contract → kernel_optimized → neurocognitive_kernel → neurocognitive_theorems
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

from closures.clinical_neuroscience.neurocognitive_kernel import (
    ALL_CHANNELS,
    N_CHANNELS,
    NEUROCOGNITIVE_CATALOG,
    WEIGHTS,
    NeurocognitiveKernelResult,
    NeurocognitiveStructuralAnalysis,
    compute_all_states,
    compute_structural_analysis,
    validate_neurocognitive_kernel,
)
from closures.clinical_neuroscience.neurocognitive_theorems import (
    run_all_theorems,
    theorem_TCN1_consciousness_gradient,
    theorem_TCN2_dmn_collapse_signature,
    theorem_TCN3_entropic_brain,
    theorem_TCN4_anesthesia_collapse,
    theorem_TCN5_formal_compliance,
    theorem_TCN6_sleep_wake_cycle,
    theorem_TCN7_healthy_supremacy,
    theorem_TCN8_psychiatric_dispersion,
    theorem_TCN9_doc_hierarchy,
    theorem_TCN10_developmental_plasticity,
)
from umcp.frozen_contract import EPSILON

# ═══════════════════════════════════════════════════════════════════
# §1 — CATALOG TESTS
# ═══════════════════════════════════════════════════════════════════


class TestCatalog:
    """Verify neurocognitive catalog structure and completeness."""

    def test_catalog_has_35_entities(self) -> None:
        assert len(NEUROCOGNITIVE_CATALOG) == 35

    def test_all_states_have_10_channels(self) -> None:
        for s in NEUROCOGNITIVE_CATALOG:
            assert len(s.channels) == N_CHANNELS, f"{s.name} has {len(s.channels)} channels"

    def test_channel_values_in_01(self) -> None:
        for s in NEUROCOGNITIVE_CATALOG:
            for i, v in enumerate(s.channels):
                assert 0.0 <= v <= 1.0, f"{s.name} ch{i} ({ALL_CHANNELS[i]}) = {v}"

    def test_channel_names_correct_count(self) -> None:
        assert len(ALL_CHANNELS) == 10

    def test_weights_sum_to_one(self) -> None:
        assert abs(float(np.sum(WEIGHTS)) - 1.0) < 1e-15

    def test_trace_clamps_to_epsilon(self) -> None:
        for s in NEUROCOGNITIVE_CATALOG:
            c = s.trace
            assert all(v >= EPSILON for v in c), f"{s.name} has sub-epsilon channel"

    def test_unique_names(self) -> None:
        names = [s.name for s in NEUROCOGNITIVE_CATALOG]
        assert len(names) == len(set(names))

    def test_has_7_categories(self) -> None:
        categories = {s.category for s in NEUROCOGNITIVE_CATALOG}
        expected = {"healthy", "altered", "doc", "neurodegen", "psychiatric", "developmental", "tbi"}
        assert categories == expected

    def test_category_counts(self) -> None:
        from collections import Counter

        counts = Counter(s.category for s in NEUROCOGNITIVE_CATALOG)
        assert counts["healthy"] == 5
        assert counts["altered"] == 6
        assert counts["doc"] == 5
        assert counts["neurodegen"] == 6
        assert counts["psychiatric"] == 6
        assert counts["developmental"] == 4
        assert counts["tbi"] == 3

    def test_has_critical_entities(self) -> None:
        names = {s.name for s in NEUROCOGNITIVE_CATALOG}
        for expected in [
            "Young adult healthy",
            "Coma",
            "Alzheimer severe",
            "Psilocybin state",
            "Expert meditator",
            "Neonatal",
        ]:
            assert expected in names, f"Missing: {expected}"

    def test_subgroup_means_valid(self) -> None:
        for s in NEUROCOGNITIVE_CATALOG:
            assert 0.0 <= s.cortical_mean <= 1.0, f"{s.name} cortical_mean={s.cortical_mean}"
            assert 0.0 <= s.structural_mean <= 1.0, f"{s.name} structural_mean={s.structural_mean}"
            assert 0.0 <= s.metabolic_mean <= 1.0, f"{s.name} metabolic_mean={s.metabolic_mean}"
            assert 0.0 <= s.systemic_mean <= 1.0, f"{s.name} systemic_mean={s.systemic_mean}"


# ═══════════════════════════════════════════════════════════════════
# §2 — TIER-1 IDENTITY TESTS
# ═══════════════════════════════════════════════════════════════════


class TestTier1Identities:
    """Verify Tier-1 identities hold for every neurocognitive state."""

    @pytest.fixture(scope="class")
    def all_results(self) -> list[NeurocognitiveKernelResult]:
        return compute_all_states()

    def test_duality_identity(self, all_results: list[NeurocognitiveKernelResult]) -> None:
        for r in all_results:
            assert abs(r.F + r.omega - 1.0) < 1e-12, f"{r.name}: F+ω={r.F + r.omega}"

    def test_integrity_bound(self, all_results: list[NeurocognitiveKernelResult]) -> None:
        for r in all_results:
            assert r.IC <= r.F + 1e-12, f"{r.name}: IC={r.IC} > F={r.F}"

    def test_log_integrity_relation(self, all_results: list[NeurocognitiveKernelResult]) -> None:
        for r in all_results:
            expected_ic = float(np.exp(r.kappa))
            assert abs(r.IC - expected_ic) < 1e-12, f"{r.name}: IC={r.IC}, exp(κ)={expected_ic}"

    def test_regime_not_empty(self, all_results: list[NeurocognitiveKernelResult]) -> None:
        for r in all_results:
            assert r.regime in ("STABLE", "WATCH", "COLLAPSE", "CRITICAL"), f"{r.name}: {r.regime}"

    def test_heterogeneity_gap_nonnegative(self, all_results: list[NeurocognitiveKernelResult]) -> None:
        for r in all_results:
            assert r.heterogeneity_gap >= -1e-12, f"{r.name}: Δ={r.heterogeneity_gap}"

    def test_IC_F_ratio_leq_one(self, all_results: list[NeurocognitiveKernelResult]) -> None:
        for r in all_results:
            assert r.IC_F_ratio <= 1.0 + 1e-12, f"{r.name}: IC/F={r.IC_F_ratio}"

    def test_omega_in_01(self, all_results: list[NeurocognitiveKernelResult]) -> None:
        for r in all_results:
            assert 0.0 <= r.omega <= 1.0, f"{r.name}: ω={r.omega}"


# ═══════════════════════════════════════════════════════════════════
# §3 — STRUCTURAL ANALYSIS TESTS
# ═══════════════════════════════════════════════════════════════════


class TestStructuralAnalysis:
    """Test the aggregate structural analysis."""

    @pytest.fixture(scope="class")
    def analysis(self) -> NeurocognitiveStructuralAnalysis:
        return compute_structural_analysis()

    def test_entity_count(self, analysis: NeurocognitiveStructuralAnalysis) -> None:
        assert analysis.n_states == 35

    def test_n_categories(self, analysis: NeurocognitiveStructuralAnalysis) -> None:
        assert len(analysis.category_mean_F) == 7

    def test_highest_F_is_meditator(self, analysis: NeurocognitiveStructuralAnalysis) -> None:
        assert analysis.highest_F[0] == "Expert meditator"

    def test_lowest_F_is_ad_severe(self, analysis: NeurocognitiveStructuralAnalysis) -> None:
        assert analysis.lowest_F[0] == "Alzheimer severe"

    def test_category_means_populated(self, analysis: NeurocognitiveStructuralAnalysis) -> None:
        assert len(analysis.category_mean_F) == 7
        assert len(analysis.category_mean_IC_F) == 7

    def test_healthy_leads_F(self, analysis: NeurocognitiveStructuralAnalysis) -> None:
        assert analysis.category_mean_F["healthy"] == max(analysis.category_mean_F.values())

    def test_summary_non_empty(self, analysis: NeurocognitiveStructuralAnalysis) -> None:
        s = analysis.summary()
        assert len(s) > 100


# ═══════════════════════════════════════════════════════════════════
# §4 — VALIDATION TESTS
# ═══════════════════════════════════════════════════════════════════


class TestValidation:
    """Test the validation function."""

    @pytest.fixture(scope="class")
    def checks(self) -> dict[str, object]:
        return validate_neurocognitive_kernel()

    def test_duality_identity_pass(self, checks: dict[str, object]) -> None:
        assert checks["duality_identity_pass"] == 35

    def test_integrity_bound_pass(self, checks: dict[str, object]) -> None:
        assert checks["integrity_bound_pass"] == 35

    def test_log_integrity_pass(self, checks: dict[str, object]) -> None:
        assert checks["log_integrity_pass"] == 35

    def test_all_pass(self, checks: dict[str, object]) -> None:
        assert checks["all_pass"] is True


# ═══════════════════════════════════════════════════════════════════
# §5 — CATEGORY ANALYSIS TESTS
# ═══════════════════════════════════════════════════════════════════


class TestCategoryAnalysis:
    """Test per-category kernel computations."""

    @pytest.fixture(scope="class")
    def categories(self) -> dict[str, list[NeurocognitiveKernelResult]]:
        all_r = compute_all_states()
        cats: dict[str, list[NeurocognitiveKernelResult]] = {}
        for r in all_r:
            cats.setdefault(r.category, []).append(r)
        return cats

    def test_all_7_categories_present(self, categories: dict) -> None:
        assert len(categories) == 7

    def test_healthy_mean_F_above_080(self, categories: dict) -> None:
        mean_F = float(np.mean([r.F for r in categories["healthy"]]))
        assert mean_F > 0.80

    def test_doc_mean_F_below_060(self, categories: dict) -> None:
        mean_F = float(np.mean([r.F for r in categories["doc"]]))
        assert mean_F < 0.60

    def test_healthy_highest_mean_F(self, categories: dict) -> None:
        means = {cat: float(np.mean([r.F for r in rs])) for cat, rs in categories.items()}
        assert max(means, key=means.get) == "healthy"  # type: ignore[arg-type]

    def test_psychiatric_moderate_F(self, categories: dict) -> None:
        mean_F = float(np.mean([r.F for r in categories["psychiatric"]]))
        assert 0.40 < mean_F < 0.80


# ═══════════════════════════════════════════════════════════════════
# §6 — THEOREM TESTS (10 theorems)
# ═══════════════════════════════════════════════════════════════════


_THEOREM_FUNCTIONS = [
    ("T-CN-1", theorem_TCN1_consciousness_gradient),
    ("T-CN-2", theorem_TCN2_dmn_collapse_signature),
    ("T-CN-3", theorem_TCN3_entropic_brain),
    ("T-CN-4", theorem_TCN4_anesthesia_collapse),
    ("T-CN-5", theorem_TCN5_formal_compliance),
    ("T-CN-6", theorem_TCN6_sleep_wake_cycle),
    ("T-CN-7", theorem_TCN7_healthy_supremacy),
    ("T-CN-8", theorem_TCN8_psychiatric_dispersion),
    ("T-CN-9", theorem_TCN9_doc_hierarchy),
    ("T-CN-10", theorem_TCN10_developmental_plasticity),
]


@pytest.mark.parametrize(
    ("theorem_id", "theorem_fn"),
    _THEOREM_FUNCTIONS,
    ids=[t[0] for t in _THEOREM_FUNCTIONS],
)
def test_theorem_proven(theorem_id: str, theorem_fn) -> None:
    result = theorem_fn()
    assert result.verdict == "PROVEN", (
        f"{theorem_id}: {result.n_failed}/{result.n_tests} subtests failed. Details: {result.details}"
    )


def test_all_theorems_proven() -> None:
    results = run_all_theorems()
    assert len(results) == 10
    n_proven = sum(1 for r in results if r.verdict == "PROVEN")
    assert n_proven == 10, f"Only {n_proven}/10 theorems proven"


def test_total_subtests() -> None:
    results = run_all_theorems()
    total = sum(r.n_tests for r in results)
    passed = sum(r.n_passed for r in results)
    assert passed == total, f"{total - passed} subtests failed"


# ═══════════════════════════════════════════════════════════════════
# §7 — FORMAL BOUNDS PRECISION TESTS
# ═══════════════════════════════════════════════════════════════════


class TestFormalBounds:
    """Verify exact analytic bounds to machine precision."""

    @pytest.fixture(scope="class")
    def computer(self):
        from umcp.kernel_optimized import OptimizedKernelComputer

        return OptimizedKernelComputer()

    @pytest.mark.parametrize(
        "channels",
        [
            [0.90] * 10,
            [0.50] * 10,
            [0.30] * 10,
            [0.95] * 10,
        ],
    )
    def test_homogeneous_IC_equals_F(self, computer, channels: list[float]) -> None:
        c = np.array(channels)
        ko = computer.compute(c, WEIGHTS)
        assert abs(ko.F - ko.IC) < 1e-14

    @pytest.mark.parametrize(
        ("high", "low"),
        [(0.95, 0.05), (0.90, 0.10), (0.80, 0.20)],
    )
    def test_heterogeneous_IC_below_F(self, computer, high: float, low: float) -> None:
        c = np.array([high] * 5 + [low] * 5)
        ko = computer.compute(c, WEIGHTS)
        assert ko.IC < ko.F - 1e-10

    def test_max_gap_near_extremes(self, computer) -> None:
        c = np.array([0.99] * 5 + [0.01] * 5)
        ko = computer.compute(c, WEIGHTS)
        assert ko.F - ko.IC > 0.30


# ═══════════════════════════════════════════════════════════════════
# §8 — ENTITY SPOT CHECKS
# ═══════════════════════════════════════════════════════════════════


class TestEntitySpotChecks:
    """Spot-check critical clinical states."""

    @pytest.fixture(scope="class")
    def results(self) -> dict[str, NeurocognitiveKernelResult]:
        return {r.name: r for r in compute_all_states()}

    def test_young_adult_watch_regime(self, results: dict) -> None:
        assert results["Young adult healthy"].regime == "WATCH"

    def test_expert_meditator_highest_F(self, results: dict) -> None:
        highest = max(results.values(), key=lambda r: r.F)
        assert highest.name == "Expert meditator"

    def test_coma_critical_regime(self, results: dict) -> None:
        assert results["Coma"].regime == "CRITICAL"

    def test_alzheimer_severe_lowest_F(self, results: dict) -> None:
        lowest = min(results.values(), key=lambda r: r.F)
        assert lowest.name == "Alzheimer severe"

    def test_psilocybin_high_curvature(self, results: dict) -> None:
        psilo = results["Psilocybin state"]
        young = results["Young adult healthy"]
        assert psilo.C > young.C * 2.0

    def test_locked_in_preserves_cortex(self, results: dict) -> None:
        locked = results["Locked-in syndrome"]
        coma = results["Coma"]
        assert locked.cortical_mean > coma.cortical_mean

    def test_anesthesia_collapse(self, results: dict) -> None:
        assert results["General anesthesia"].regime == "COLLAPSE"

    def test_nrem_collapse(self, results: dict) -> None:
        assert results["NREM deep sleep"].regime == "COLLAPSE"

    def test_flow_state_high_F(self, results: dict) -> None:
        assert results["Flow state"].F > 0.80

    def test_mdd_moderate_F(self, results: dict) -> None:
        mdd = results["Major depression"]
        assert 0.40 < mdd.F < 0.80

    def test_neonatal_lowest_F_in_dev(self, results: dict) -> None:
        dev_states = {
            n: r
            for n, r in results.items()
            if any(s.name == n and s.category == "developmental" for s in NEUROCOGNITIVE_CATALOG)
        }
        lowest = min(dev_states.values(), key=lambda r: r.F)
        assert lowest.name == "Neonatal"

    def test_vegetative_below_coma_or_close(self, results: dict) -> None:
        vs = results["Vegetative state"]
        coma = results["Coma"]
        assert abs(vs.F - coma.F) < 0.10  # close together at bottom


# ═══════════════════════════════════════════════════════════════════
# §9 — CROSS-CATEGORY REGIME TESTS
# ═══════════════════════════════════════════════════════════════════


class TestRegimeDistribution:
    """Test regime distribution across categories."""

    @pytest.fixture(scope="class")
    def all_results(self) -> list[NeurocognitiveKernelResult]:
        return compute_all_states()

    def test_all_healthy_watch(self, all_results: list[NeurocognitiveKernelResult]) -> None:
        healthy = [r for r in all_results if r.category == "healthy"]
        for r in healthy:
            assert r.regime == "WATCH", f"{r.name}: {r.regime}"

    def test_all_doc_collapse_or_critical(self, all_results: list[NeurocognitiveKernelResult]) -> None:
        doc = [r for r in all_results if r.category == "doc"]
        for r in doc:
            assert r.regime in ("COLLAPSE", "CRITICAL"), f"{r.name}: {r.regime}"

    def test_has_critical_regimes(self, all_results: list[NeurocognitiveKernelResult]) -> None:
        n_critical = sum(1 for r in all_results if r.regime == "CRITICAL")
        assert n_critical >= 1

    def test_no_stable_regime(self, all_results: list[NeurocognitiveKernelResult]) -> None:
        n_stable = sum(1 for r in all_results if r.regime == "STABLE")
        assert n_stable == 0
