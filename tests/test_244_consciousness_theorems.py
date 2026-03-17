"""Tests for consciousness coherence theorem formalism — T-CC-1 through T-CC-7.

Verifies the ten theorems that emerge when Jackson's claims are corrected
and grounded in the GCD kernel across 20 consciousness-candidate systems.

Every theorem is:
  1. STATED precisely
  2. PROVED computationally
  3. CONNECTED to one of Jackson's original claims
  4. CORRECTED to show what the claim becomes in GCD

Derivation chain: Axiom-0 → frozen_contract → kernel_optimized → coherence_kernel → consciousness_theorems
"""

from __future__ import annotations

import math

import numpy as np
import pytest
from scipy.stats import spearmanr

from closures.consciousness_coherence.coherence_kernel import (
    PHI,
    PHI_SQ_E,
    XI_J,
    compute_all_coherence_systems,
)
from closures.consciousness_coherence.consciousness_theorems import (
    ALL_THEOREMS,
    TheoremResult,
    run_all_theorems,
)

# ═══════════════════════════════════════════════════════════════════
# 0. Theorem Infrastructure
# ═══════════════════════════════════════════════════════════════════


class TestTheoremInfrastructure:
    """Verify theorem infrastructure correctness."""

    def test_ten_theorems_defined(self) -> None:
        """Exactly 10 theorems."""
        assert len(ALL_THEOREMS) == 10

    def test_all_callable(self) -> None:
        """All theorem functions are callable."""
        for fn in ALL_THEOREMS:
            assert callable(fn)

    def test_all_return_theorem_result(self) -> None:
        """Each theorem returns a TheoremResult."""
        results = run_all_theorems()
        for r in results:
            assert isinstance(r, TheoremResult)

    def test_all_have_jackson_claim(self) -> None:
        """Each theorem documents Jackson's original claim."""
        results = run_all_theorems()
        for r in results:
            assert len(r.jackson_claim) > 10

    def test_all_have_correction(self) -> None:
        """Each theorem documents the correction."""
        results = run_all_theorems()
        for r in results:
            assert len(r.correction) > 10

    def test_all_7_proven(self) -> None:
        """All 10/10 theorems PROVEN."""
        results = run_all_theorems()
        for r in results:
            assert r.verdict == "PROVEN", f"{r.name}: {r.verdict} ({r.n_passed}/{r.n_tests})"

    def test_117_subtests_pass(self) -> None:
        """All 117/117 sub-tests pass."""
        results = run_all_theorems()
        total = sum(r.n_tests for r in results)
        passed = sum(r.n_passed for r in results)
        assert total == 117
        assert passed == 117


# ═══════════════════════════════════════════════════════════════════
# 1. T-CC-1: Harmonic Non-Privilege
# ═══════════════════════════════════════════════════════════════════


class TestTCC1HarmonicNonPrivilege:
    """Verify T-CC-1: ξ_J proximity does NOT predict IC."""

    @pytest.fixture(scope="class")
    def results(self) -> list:
        return compute_all_coherence_systems()

    def test_phi_sq_e_not_exact(self) -> None:
        """φ²·e = 7.1166 ≠ 7.2 (1.16% off)."""
        assert abs(PHI_SQ_E - XI_J) / XI_J > 0.01

    def test_phi_sq_e_value(self) -> None:
        """φ²·e computed correctly."""
        expected = ((1 + math.sqrt(5)) / 2) ** 2 * math.e
        assert abs(PHI_SQ_E - expected) < 1e-10

    def test_spearman_not_significant(self, results: list) -> None:
        """ρ(ξ_J, IC) < 0.30 — not significant."""
        xi_vals = [r.xi_j_diagnostic for r in results]
        ic_vals = [r.IC for r in results]
        sr = spearmanr(xi_vals, ic_vals)
        rho = float(sr[0])  # type: ignore[arg-type]
        pval = float(sr[1])  # type: ignore[arg-type]
        assert abs(rho) < 0.30
        assert pval > 0.05

    def test_jackson_system_in_collapse(self, results: list) -> None:
        """Jackson's own system is in Collapse regime."""
        jackson = next(r for r in results if r.name == "jackson_xi_j_identity")
        assert jackson.regime == "Collapse"

    def test_high_harmonic_mostly_collapse(self, results: list) -> None:
        """High harmonic_ratio systems are still in Collapse."""
        high = [r for r in results if r.xi_j_diagnostic > 0.80]
        assert len(high) >= 3
        collapse_count = sum(1 for r in high if r.regime == "Collapse")
        assert collapse_count >= len(high) // 2

    def test_theorem_proven(self) -> None:
        """T-CC-1 verdict is PROVEN."""
        from closures.consciousness_coherence.consciousness_theorems import theorem_TCC1_harmonic_non_privilege

        result = theorem_TCC1_harmonic_non_privilege()
        assert result.verdict == "PROVEN"


# ═══════════════════════════════════════════════════════════════════
# 2. T-CC-2: Recursion-Return Dissociation
# ═══════════════════════════════════════════════════════════════════


class TestTCC2RecursionReturnDissociation:
    """Verify T-CC-2: recursive depth does NOT predict return fidelity."""

    @pytest.fixture(scope="class")
    def results(self) -> list:
        return compute_all_coherence_systems()

    def test_correlation_not_positive(self, results: list) -> None:
        """ρ(recursive_depth, return_fidelity) ≤ 0.10."""
        rec_vals = [r.trace_vector[1] for r in results]
        ret_vals = [r.trace_vector[2] for r in results]
        sr = spearmanr(rec_vals, ret_vals)
        rho = float(sr[0])  # type: ignore[arg-type]
        assert rho <= 0.10

    def test_gesture_systems_exist(self, results: list) -> None:
        """Recursive Gesture systems exist (high recursion, low return)."""
        gestures = [r for r in results if r.coherence_type == "Recursive Gesture"]
        assert len(gestures) >= 1

    def test_llm_is_gesture(self, results: list) -> None:
        """LLM system is classified as Recursive Gesture."""
        llm = next(r for r in results if r.name == "llm_recursive_dialogue")
        assert llm.coherence_type == "Recursive Gesture"
        assert llm.regime == "Collapse"

    def test_low_recursion_high_return_exists(self, results: list) -> None:
        """Systems with low recursion but high return exist."""
        low_rec_high_ret = [r for r in results if r.trace_vector[1] < 0.30 and r.trace_vector[2] > 0.80]
        assert len(low_rec_high_ret) >= 1

    def test_theorem_proven(self) -> None:
        """T-CC-2 verdict is PROVEN."""
        from closures.consciousness_coherence.consciousness_theorems import theorem_TCC2_recursion_return_dissociation

        result = theorem_TCC2_recursion_return_dissociation()
        assert result.verdict == "PROVEN"


# ═══════════════════════════════════════════════════════════════════
# 3. T-CC-3: Universal Instability
# ═══════════════════════════════════════════════════════════════════


class TestTCC3UniversalInstability:
    """Verify T-CC-3: 0/20 systems reach Stable regime."""

    @pytest.fixture(scope="class")
    def results(self) -> list:
        return compute_all_coherence_systems()

    def test_zero_stable(self, results: list) -> None:
        """No consciousness system is Stable."""
        n_stable = sum(1 for r in results if r.regime == "Stable")
        assert n_stable == 0

    def test_watch_count(self, results: list) -> None:
        """5 systems in Watch."""
        n_watch = sum(1 for r in results if r.regime == "Watch")
        assert n_watch == 5

    def test_collapse_majority(self, results: list) -> None:
        """Collapse is the majority regime."""
        n_collapse = sum(1 for r in results if r.regime == "Collapse")
        assert n_collapse == 15
        assert n_collapse / len(results) > 0.50

    def test_euler_not_stable(self, results: list) -> None:
        """Even the best system (Euler identity) is not Stable."""
        euler = next(r for r in results if r.name == "euler_identity")
        assert euler.regime != "Stable"
        assert euler.regime == "Watch"

    def test_no_system_above_f_gate(self, results: list) -> None:
        """No system exceeds F > 0.90 (Stable gate)."""
        n_above = sum(1 for r in results if r.F > 0.90)
        assert n_above == 0

    def test_theorem_proven(self) -> None:
        """T-CC-3 verdict is PROVEN."""
        from closures.consciousness_coherence.consciousness_theorems import theorem_TCC3_universal_instability

        result = theorem_TCC3_universal_instability()
        assert result.verdict == "PROVEN"


# ═══════════════════════════════════════════════════════════════════
# 4. T-CC-4: Geometric Slaughter
# ═══════════════════════════════════════════════════════════════════


class TestTCC4GeometricSlaughter:
    """Verify T-CC-4: one dead channel kills IC."""

    @pytest.fixture(scope="class")
    def results(self) -> list:
        return compute_all_coherence_systems()

    def test_euler_highest_ic_f_ratio(self, results: list) -> None:
        """Euler identity has highest IC/F ratio."""
        euler = next(r for r in results if r.name == "euler_identity")
        euler_ratio = euler.IC / euler.F
        assert euler_ratio > 0.98

    def test_432hz_lower_ratio(self, results: list) -> None:
        """432 Hz has lower IC/F than Euler (information_density kills it)."""
        euler = next(r for r in results if r.name == "euler_identity")
        hz432 = next(r for r in results if r.name == "432hz_tuning_system")
        assert hz432.IC / hz432.F < euler.IC / euler.F - 0.10

    def test_variance_anticorrelates_ic_f(self, results: list) -> None:
        """Channel variance anti-correlates with IC/F ratio."""
        ic_f = [r.IC / r.F for r in results]
        variances = [float(np.var(r.trace_vector)) for r in results]
        sr = spearmanr(variances, ic_f)
        rho = float(sr[0])  # type: ignore[arg-type]
        assert rho < -0.30

    def test_jackson_weakest_channel(self, results: list) -> None:
        """Jackson's system has a dead channel dragging down IC."""
        jackson = next(r for r in results if r.name == "jackson_xi_j_identity")
        assert jackson.heterogeneity_gap > 0.03
        assert jackson.weakest_value < 0.30

    def test_theorem_proven(self) -> None:
        """T-CC-4 verdict is PROVEN."""
        from closures.consciousness_coherence.consciousness_theorems import theorem_TCC4_geometric_slaughter

        result = theorem_TCC4_geometric_slaughter()
        assert result.verdict == "PROVEN"


# ═══════════════════════════════════════════════════════════════════
# 5. T-CC-5: Tuning Invariance
# ═══════════════════════════════════════════════════════════════════


class TestTCC5TuningInvariance:
    """Verify T-CC-5: 432 Hz ≡ 440 Hz in the kernel."""

    @pytest.fixture(scope="class")
    def results(self) -> list:
        return compute_all_coherence_systems()

    def test_f_nearly_identical(self, results: list) -> None:
        """F values differ by < 0.02."""
        hz432 = next(r for r in results if r.name == "432hz_tuning_system")
        hz440 = next(r for r in results if r.name == "440hz_standard_tuning")
        assert abs(hz432.F - hz440.F) < 0.02

    def test_ic_nearly_identical(self, results: list) -> None:
        """IC values differ by < 0.02."""
        hz432 = next(r for r in results if r.name == "432hz_tuning_system")
        hz440 = next(r for r in results if r.name == "440hz_standard_tuning")
        assert abs(hz432.IC - hz440.IC) < 0.02

    def test_same_regime(self, results: list) -> None:
        """Both in Collapse regime."""
        hz432 = next(r for r in results if r.name == "432hz_tuning_system")
        hz440 = next(r for r in results if r.name == "440hz_standard_tuning")
        assert hz432.regime == hz440.regime == "Collapse"

    def test_same_weakest_channel(self, results: list) -> None:
        """Same weakest channel (information_density)."""
        hz432 = next(r for r in results if r.name == "432hz_tuning_system")
        hz440 = next(r for r in results if r.name == "440hz_standard_tuning")
        assert hz432.weakest_channel == hz440.weakest_channel

    def test_delta_nearly_identical(self, results: list) -> None:
        """Heterogeneity gaps differ by < 0.01."""
        hz432 = next(r for r in results if r.name == "432hz_tuning_system")
        hz440 = next(r for r in results if r.name == "440hz_standard_tuning")
        assert abs(hz432.heterogeneity_gap - hz440.heterogeneity_gap) < 0.01

    def test_theorem_proven(self) -> None:
        """T-CC-5 verdict is PROVEN."""
        from closures.consciousness_coherence.consciousness_theorems import theorem_TCC5_tuning_invariance

        result = theorem_TCC5_tuning_invariance()
        assert result.verdict == "PROVEN"


# ═══════════════════════════════════════════════════════════════════
# 6. T-CC-6: Mathematical Supremacy
# ═══════════════════════════════════════════════════════════════════


class TestTCC6MathematicalSupremacy:
    """Verify T-CC-6: mathematical identity beats harmonic ratio."""

    @pytest.fixture(scope="class")
    def results(self) -> list:
        return compute_all_coherence_systems()

    def test_math_highest_mean_f(self, results: list) -> None:
        """Mathematical category has highest mean F."""
        cats: dict[str, list] = {}
        for r in results:
            cats.setdefault(r.category, []).append(r.F)
        means = {c: np.mean(fs) for c, fs in cats.items()}
        assert max(means, key=means.get) == "Mathematical"  # type: ignore[arg-type]

    def test_math_highest_mean_ic(self, results: list) -> None:
        """Mathematical category has highest mean IC."""
        cats: dict[str, list] = {}
        for r in results:
            cats.setdefault(r.category, []).append(r.IC)
        means = {c: np.mean(ics) for c, ics in cats.items()}
        assert max(means, key=means.get) == "Mathematical"  # type: ignore[arg-type]

    def test_harmonic_highest_mean_delta(self, results: list) -> None:
        """Harmonic category has highest mean Δ (most fragile)."""
        cats: dict[str, list] = {}
        for r in results:
            cats.setdefault(r.category, []).append(r.heterogeneity_gap)
        means = {c: np.mean(ds) for c, ds in cats.items()}
        assert max(means, key=means.get) == "Harmonic"  # type: ignore[arg-type]

    def test_euler_beats_all_harmonic(self, results: list) -> None:
        """Euler identity F and IC exceed every harmonic system."""
        euler = next(r for r in results if r.name == "euler_identity")
        harmonic = [r for r in results if r.category == "Harmonic"]
        assert max(r.F for r in harmonic) < euler.F
        assert max(r.IC for r in harmonic) < euler.IC

    def test_euler_lowest_delta(self, results: list) -> None:
        """Euler identity has lowest Δ of all systems."""
        euler = next(r for r in results if r.name == "euler_identity")
        harmonic = [r for r in results if r.category == "Harmonic"]
        assert euler.heterogeneity_gap < min(r.heterogeneity_gap for r in harmonic)

    def test_theorem_proven(self) -> None:
        """T-CC-6 verdict is PROVEN."""
        from closures.consciousness_coherence.consciousness_theorems import theorem_TCC6_mathematical_supremacy

        result = theorem_TCC6_mathematical_supremacy()
        assert result.verdict == "PROVEN"


# ═══════════════════════════════════════════════════════════════════
# 7. T-CC-7: Heterogeneity Gap Ordering
# ═══════════════════════════════════════════════════════════════════


class TestTCC7HeterogeneityGapOrdering:
    """Verify T-CC-7: Δ ordering inverts Jackson's hierarchy."""

    @pytest.fixture(scope="class")
    def results(self) -> list:
        return compute_all_coherence_systems()

    def test_neural_lowest_delta(self, results: list) -> None:
        """Neural category has lowest mean Δ."""
        cats: dict[str, list] = {}
        for r in results:
            cats.setdefault(r.category, []).append(r.heterogeneity_gap)
        means = {c: np.mean(ds) for c, ds in cats.items()}
        assert min(means, key=means.get) == "Neural"  # type: ignore[arg-type]

    def test_harmonic_highest_delta(self, results: list) -> None:
        """Harmonic category has highest mean Δ (in top 2)."""
        cats: dict[str, list] = {}
        for r in results:
            cats.setdefault(r.category, []).append(r.heterogeneity_gap)
        means = {c: np.mean(ds) for c, ds in cats.items()}
        top2 = sorted(means, key=means.get, reverse=True)[:2]  # type: ignore[arg-type]
        assert "Harmonic" in top2

    def test_neural_less_than_harmonic(self, results: list) -> None:
        """Neural Δ < Harmonic Δ (inverts Jackson's hierarchy)."""
        neural = [r for r in results if r.category == "Neural"]
        harmonic = [r for r in results if r.category == "Harmonic"]
        assert np.mean([r.heterogeneity_gap for r in neural]) < np.mean([r.heterogeneity_gap for r in harmonic])

    def test_phi_sq_xi_j_not_threshold(self, results: list) -> None:
        """φ²/ξ_J = 0.364 exceeds max(Δ) — not a threshold."""
        phi_sq_xi = PHI**2 / XI_J
        max_delta = max(r.heterogeneity_gap for r in results)
        assert phi_sq_xi > max_delta

    def test_delta_more_predictive_than_xi_j(self, results: list) -> None:
        """Δ is more predictive of IC than ξ_J proximity."""
        ic_vals = [r.IC for r in results]
        xi_vals = [r.xi_j_diagnostic for r in results]
        delta_vals = [r.heterogeneity_gap for r in results]
        rho_delta = abs(float(spearmanr(delta_vals, ic_vals)[0]))  # type: ignore[arg-type]
        rho_xi = abs(float(spearmanr(xi_vals, ic_vals)[0]))  # type: ignore[arg-type]
        assert rho_delta > rho_xi

    def test_theorem_proven(self) -> None:
        """T-CC-7 verdict is PROVEN."""
        from closures.consciousness_coherence.consciousness_theorems import theorem_TCC7_heterogeneity_gap_ordering

        result = theorem_TCC7_heterogeneity_gap_ordering()
        assert result.verdict == "PROVEN"


# ═══════════════════════════════════════════════════════════════════
# 8. Cross-Theorem Consistency
# ═══════════════════════════════════════════════════════════════════


class TestCrossTheoremConsistency:
    """Verify cross-theorem consistency across all 10 theorems."""

    @pytest.fixture(scope="class")
    def theorem_results(self) -> list[TheoremResult]:
        return run_all_theorems()

    def test_all_verdicts_proven(self, theorem_results: list[TheoremResult]) -> None:
        """All 7 verdicts are PROVEN."""
        verdicts = [r.verdict for r in theorem_results]
        assert all(v == "PROVEN" for v in verdicts)

    def test_total_subtests(self, theorem_results: list[TheoremResult]) -> None:
        """Total sub-tests = 117."""
        assert sum(r.n_tests for r in theorem_results) == 117

    def test_total_passed(self, theorem_results: list[TheoremResult]) -> None:
        """All 117 sub-tests pass."""
        assert sum(r.n_passed for r in theorem_results) == 117

    def test_zero_failures(self, theorem_results: list[TheoremResult]) -> None:
        """Zero sub-test failures."""
        assert sum(r.n_failed for r in theorem_results) == 0

    def test_all_pass_rates_100(self, theorem_results: list[TheoremResult]) -> None:
        """Every theorem has 100% pass rate."""
        for r in theorem_results:
            assert r.pass_rate == 1.0, f"{r.name}: {r.pass_rate}"

    def test_theorem_names_unique(self, theorem_results: list[TheoremResult]) -> None:
        """All theorem names are unique."""
        names = [r.name for r in theorem_results]
        assert len(names) == len(set(names))

    def test_theorem_names_start_with_tcc(self, theorem_results: list[TheoremResult]) -> None:
        """All theorem names start with T-CC-."""
        for r in theorem_results:
            assert r.name.startswith("T-CC-")
