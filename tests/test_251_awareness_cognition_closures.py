"""Tests for the awareness-cognition Tier-2 closure.

Tests cover:
    - Entity catalog completeness and channel bounds
    - Tier-1 identity verification for all 36 organisms
    - Structural analysis correlations
    - 10 theorems (T-AW-1 through T-AW-10)
    - Human developmental trajectory
    - Cross-domain bridge validation
    - Formal bounds to machine precision

Derivation chain: Axiom-0 → frozen_contract → kernel_optimized → awareness_kernel → awareness_theorems
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

from closures.awareness_cognition.awareness_kernel import (
    ALL_CHANNELS,
    APTITUDE_CHANNELS,
    AWARENESS_CHANNELS,
    N_CHANNELS,
    ORGANISM_CATALOG,
    WEIGHTS,
    AwarenessKernelResult,
    AwarenessStructuralAnalysis,
    analyze_awareness_structure,
    compute_all_organisms,
    compute_human_trajectory,
    validate_awareness_kernel,
)
from closures.awareness_cognition.awareness_theorems import (
    run_all_theorems,
    theorem_TAW1_awareness_aptitude_inversion,
    theorem_TAW2_universal_instability,
    theorem_TAW3_geometric_slaughter,
    theorem_TAW4_sensitivity_formula,
    theorem_TAW5_cross_domain_isomorphism,
    theorem_TAW6_cost_of_awareness,
    theorem_TAW7_human_development,
    theorem_TAW8_binding_gate_transition,
    theorem_TAW9_cross_domain_bridge,
    theorem_TAW10_formal_bounds,
)
from umcp.frozen_contract import EPSILON

# ═══════════════════════════════════════════════════════════════════
# §1 — CATALOG TESTS
# ═══════════════════════════════════════════════════════════════════


class TestCatalog:
    """Verify organism catalog structure and completeness."""

    def test_catalog_has_36_entities(self) -> None:
        assert len(ORGANISM_CATALOG) == 36

    def test_all_organisms_have_10_channels(self) -> None:
        for org in ORGANISM_CATALOG:
            assert len(org.channels) == N_CHANNELS, f"{org.name} has {len(org.channels)} channels"

    def test_channel_values_in_01(self) -> None:
        for org in ORGANISM_CATALOG:
            for i, v in enumerate(org.channels):
                assert 0.0 <= v <= 1.0, f"{org.name} ch{i} ({ALL_CHANNELS[i]}) = {v}"

    def test_channel_names_correct_count(self) -> None:
        assert len(ALL_CHANNELS) == 10
        assert len(AWARENESS_CHANNELS) == 5
        assert len(APTITUDE_CHANNELS) == 5

    def test_weights_sum_to_one(self) -> None:
        assert abs(float(np.sum(WEIGHTS)) - 1.0) < 1e-15

    def test_trace_clamps_to_epsilon(self) -> None:
        ecoli = ORGANISM_CATALOG[0]
        c = ecoli.trace
        assert all(v >= EPSILON for v in c)

    def test_unique_names(self) -> None:
        names = [org.name for org in ORGANISM_CATALOG]
        assert len(names) == len(set(names))

    def test_has_human_stages(self) -> None:
        human_names = {org.name for org in ORGANISM_CATALOG if org.clade == "Homo sapiens"}
        assert "Human infant" in human_names
        assert "Human adult" in human_names
        assert "Human elderly 85" in human_names

    def test_has_great_apes(self) -> None:
        primate_names = {org.name for org in ORGANISM_CATALOG if org.clade == "Primates"}
        assert "Chimpanzee" in primate_names
        assert "Gorilla" in primate_names
        assert "Bonobo" in primate_names

    def test_organism_awareness_aptitude_means(self) -> None:
        for org in ORGANISM_CATALOG:
            aw = org.awareness_mean
            ap = org.aptitude_mean
            assert 0.0 <= aw <= 1.0, f"{org.name} aw={aw}"
            assert 0.0 <= ap <= 1.0, f"{org.name} ap={ap}"


# ═══════════════════════════════════════════════════════════════════
# §2 — TIER-1 IDENTITY TESTS
# ═══════════════════════════════════════════════════════════════════


class TestTier1Identities:
    """Verify Tier-1 identities hold for every organism."""

    @pytest.fixture(scope="class")
    def all_results(self) -> list[AwarenessKernelResult]:
        return compute_all_organisms()

    def test_duality_identity(self, all_results: list[AwarenessKernelResult]) -> None:
        for r in all_results:
            assert abs(r.F + r.omega - 1.0) < 1e-12, f"{r.name}: F+ω={r.F + r.omega}"

    def test_integrity_bound(self, all_results: list[AwarenessKernelResult]) -> None:
        for r in all_results:
            assert r.IC <= r.F + 1e-12, f"{r.name}: IC={r.IC} > F={r.F}"

    def test_log_integrity_relation(self, all_results: list[AwarenessKernelResult]) -> None:
        for r in all_results:
            expected_ic = float(np.exp(r.kappa))
            assert abs(r.IC - expected_ic) < 1e-12, f"{r.name}: IC={r.IC}, exp(κ)={expected_ic}"

    def test_regime_not_empty(self, all_results: list[AwarenessKernelResult]) -> None:
        for r in all_results:
            assert r.regime in ("STABLE", "WATCH", "COLLAPSE", "CRITICAL"), f"{r.name}: {r.regime}"

    def test_delta_nonnegative(self, all_results: list[AwarenessKernelResult]) -> None:
        for r in all_results:
            assert r.delta >= -1e-12, f"{r.name}: Δ={r.delta}"

    def test_coupling_efficiency_leq_one(self, all_results: list[AwarenessKernelResult]) -> None:
        for r in all_results:
            assert r.coupling_efficiency <= 1.0 + 1e-12, f"{r.name}: IC/F={r.coupling_efficiency}"


# ═══════════════════════════════════════════════════════════════════
# §3 — STRUCTURAL ANALYSIS TESTS
# ═══════════════════════════════════════════════════════════════════


class TestStructuralAnalysis:
    """Test the aggregate structural analysis."""

    @pytest.fixture(scope="class")
    def analysis(self) -> AwarenessStructuralAnalysis:
        return analyze_awareness_structure()

    def test_entity_count(self, analysis: AwarenessStructuralAnalysis) -> None:
        assert analysis.n_entities == 36

    def test_zero_stable(self, analysis: AwarenessStructuralAnalysis) -> None:
        assert analysis.n_stable == 0

    def test_awareness_dominates_F(self, analysis: AwarenessStructuralAnalysis) -> None:
        assert analysis.awareness_F_rho > 0.80

    def test_awareness_aptitude_anti_correlated(self, analysis: AwarenessStructuralAnalysis) -> None:
        assert analysis.awareness_aptitude_rho < -0.50

    def test_polarization_drives_gap(self, analysis: AwarenessStructuralAnalysis) -> None:
        assert analysis.polarization_gap_rho > 0.70


# ═══════════════════════════════════════════════════════════════════
# §4 — VALIDATION TESTS
# ═══════════════════════════════════════════════════════════════════


class TestValidation:
    """Test the validation function."""

    @pytest.fixture(scope="class")
    def checks(self) -> dict[str, bool]:
        return validate_awareness_kernel()

    def test_all_checks_pass(self, checks: dict[str, bool]) -> None:
        for name, passed in checks.items():
            assert passed, f"Validation check failed: {name}"

    def test_at_least_6_checks(self, checks: dict[str, bool]) -> None:
        assert len(checks) >= 6


# ═══════════════════════════════════════════════════════════════════
# §5 — HUMAN TRAJECTORY TESTS
# ═══════════════════════════════════════════════════════════════════


class TestHumanTrajectory:
    """Test human developmental trajectory."""

    @pytest.fixture(scope="class")
    def trajectory(self) -> list[AwarenessKernelResult]:
        return compute_human_trajectory()

    def test_has_all_stages(self, trajectory: list[AwarenessKernelResult]) -> None:
        names = {r.name for r in trajectory}
        assert "Human infant" in names
        assert "Human child 5" in names
        assert "Human adult" in names

    def test_adult_has_max_F(self, trajectory: list[AwarenessKernelResult]) -> None:
        adult = next(r for r in trajectory if r.name == "Human adult")
        assert max(r.F for r in trajectory) == adult.F

    def test_all_collapse_or_critical(self, trajectory: list[AwarenessKernelResult]) -> None:
        for r in trajectory:
            assert r.regime in ("COLLAPSE", "CRITICAL"), f"{r.name}: {r.regime}"


# ═══════════════════════════════════════════════════════════════════
# §6 — THEOREM TESTS (10 theorems)
# ═══════════════════════════════════════════════════════════════════


_THEOREM_FUNCTIONS = [
    ("T-AW-1", theorem_TAW1_awareness_aptitude_inversion),
    ("T-AW-2", theorem_TAW2_universal_instability),
    ("T-AW-3", theorem_TAW3_geometric_slaughter),
    ("T-AW-4", theorem_TAW4_sensitivity_formula),
    ("T-AW-5", theorem_TAW5_cross_domain_isomorphism),
    ("T-AW-6", theorem_TAW6_cost_of_awareness),
    ("T-AW-7", theorem_TAW7_human_development),
    ("T-AW-8", theorem_TAW8_binding_gate_transition),
    ("T-AW-9", theorem_TAW9_cross_domain_bridge),
    ("T-AW-10", theorem_TAW10_formal_bounds),
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
        ("aw", "ap"),
        [
            (0.10, 0.80),
            (0.30, 0.60),
            (0.50, 0.50),
            (0.70, 0.40),
            (0.90, 0.30),
            (0.95, 0.12),
            (0.99, 0.05),
            (0.01, 0.99),
        ],
    )
    def test_F_equals_mean_of_subgroups(self, computer, aw: float, ap: float) -> None:
        c = np.array([aw] * 5 + [ap] * 5)
        ko = computer.compute(c, WEIGHTS)
        assert abs(ko.F - (aw + ap) / 2) < 1e-14

    @pytest.mark.parametrize(
        ("aw", "ap"),
        [
            (0.10, 0.80),
            (0.30, 0.60),
            (0.50, 0.50),
            (0.70, 0.40),
            (0.90, 0.30),
            (0.95, 0.12),
            (0.99, 0.05),
            (0.01, 0.99),
        ],
    )
    def test_IC_equals_geometric_mean(self, computer, aw: float, ap: float) -> None:
        c = np.array([aw] * 5 + [ap] * 5)
        ko = computer.compute(c, WEIGHTS)
        assert abs(ko.IC - np.sqrt(aw * ap)) < 1e-14

    def test_delta_zero_when_equal(self, computer) -> None:
        c = np.array([0.60] * 10)
        ko = computer.compute(c, WEIGHTS)
        assert abs(ko.F - ko.IC) < 1e-15

    @pytest.mark.parametrize(
        ("aw", "ap"),
        [(0.90, 0.30), (0.95, 0.12), (0.70, 0.40)],
    )
    def test_coupling_efficiency_formula(self, computer, aw: float, ap: float) -> None:
        c = np.array([aw] * 5 + [ap] * 5)
        ko = computer.compute(c, WEIGHTS)
        predicted = 2 * np.sqrt(aw * ap) / (aw + ap)
        actual = ko.IC / ko.F
        assert abs(actual - predicted) < 1e-13


# ═══════════════════════════════════════════════════════════════════
# §8 — INDIVIDUAL ENTITY SPOT CHECKS
# ═══════════════════════════════════════════════════════════════════


class TestEntitySpotChecks:
    """Spot-check critical entities."""

    @pytest.fixture(scope="class")
    def results(self) -> dict[str, AwarenessKernelResult]:
        all_r = compute_all_organisms()
        return {r.name: r for r in all_r}

    def test_ecoli_awareness_near_zero(self, results: dict) -> None:
        assert results["E. coli"].awareness_mean < 0.05

    def test_ecoli_high_aptitude(self, results: dict) -> None:
        assert results["E. coli"].aptitude_mean > 0.50

    def test_human_adult_highest_awareness(self, results: dict) -> None:
        max_aw = max(results.values(), key=lambda r: r.awareness_mean)
        # Human adult or meditator should be at top
        assert max_aw.name in ("Human adult", "Human meditator")

    def test_human_adult_binding_gate_C(self, results: dict) -> None:
        assert results["Human adult"].binding_gate == "C"

    def test_chimp_weakest_is_aptitude(self, results: dict) -> None:
        assert results["Chimpanzee"].weakest_channel in APTITUDE_CHANNELS

    def test_human_adult_F_above_06(self, results: dict) -> None:
        assert results["Human adult"].F > 0.60

    def test_ecoli_regime_critical(self, results: dict) -> None:
        assert results["E. coli"].regime == "CRITICAL"

    def test_savant_low_social_cognition(self, results: dict) -> None:
        savant = next(o for o in ORGANISM_CATALOG if o.name == "Human savant")
        assert savant.channels[4] < 0.30  # social_cognition

    def test_minimally_conscious_lowest_F(self, results: dict) -> None:
        mc = results["Human minimally conscious"]
        # Should have very low F
        assert mc.F < 0.15
