"""Tests for the Drift Engine — Controlled Collapse-Return Exploration.

Verifies the 6 theorems (T-DE-1 through T-DE-6) and structural properties
of the drift engine closure.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pytest

_WORKSPACE = Path(__file__).resolve().parents[1]
if str(_WORKSPACE / "src") not in sys.path:
    sys.path.insert(0, str(_WORKSPACE / "src"))

from closures.gcd.drift_engine import (
    generate_candidates,
    verify_all_theorems,
    verify_t_de_1,
    verify_t_de_2,
    verify_t_de_3,
    verify_t_de_4,
    verify_t_de_5,
    verify_t_de_6,
)

# ── Fixtures ─────────────────────────────────────────────────────────


@pytest.fixture()
def homogeneous_trace() -> tuple[np.ndarray, np.ndarray]:
    """Homogeneous 8-channel trace at c=0.70 (Watch/Collapse boundary)."""
    c = np.full(8, 0.70)
    w = np.ones(8) / 8
    return c, w


@pytest.fixture()
def heterogeneous_trace() -> tuple[np.ndarray, np.ndarray]:
    """Heterogeneous 8-channel trace (real-world-like)."""
    c = np.array([0.95, 0.80, 0.60, 0.40, 0.85, 0.70, 0.55, 0.30])
    w = np.ones(8) / 8
    return c, w


@pytest.fixture()
def dead_channel_trace() -> tuple[np.ndarray, np.ndarray]:
    """Trace with one near-dead channel (geometric slaughter)."""
    c = np.array([0.95, 0.90, 0.85, 0.80, 0.75, 0.70, 0.65, 0.02])
    w = np.ones(8) / 8
    return c, w


# ── Theorem Tests ────────────────────────────────────────────────────


class TestDriftEngineTheorems:
    """Verify all 6 drift engine theorems."""

    def test_t_de_1_drift_controllability(self) -> None:
        result = verify_t_de_1()
        assert result["PROVEN"], f"T-DE-1 failed: {result}"
        assert result["monotone"]

    def test_t_de_2_gap_amplification(self) -> None:
        result = verify_t_de_2()
        assert result["PROVEN"], f"T-DE-2 failed: {result}"

    def test_t_de_3_return_selectivity(self) -> None:
        result = verify_t_de_3()
        assert result["PROVEN"], f"T-DE-3 failed: {result}"

    def test_t_de_4_budget_ordering(self) -> None:
        result = verify_t_de_4()
        assert result["PROVEN"], f"T-DE-4 failed: {result}"

    def test_t_de_5_regime_diversity(self) -> None:
        result = verify_t_de_5()
        assert result["PROVEN"], f"T-DE-5 failed: {result}"

    def test_t_de_6_generative_yield(self) -> None:
        result = verify_t_de_6()
        assert result["PROVEN"], f"T-DE-6 failed: {result}"

    def test_all_theorems_proven(self) -> None:
        results = verify_all_theorems()
        assert len(results) == 6
        for r in results:
            assert r["PROVEN"], f"{r['theorem']} failed: {r}"


# ── Structural Tests ─────────────────────────────────────────────────


class TestDriftEngineStructure:
    """Verify structural properties of the drift engine."""

    def test_baseline_evaluation(self, homogeneous_trace: tuple[np.ndarray, np.ndarray]) -> None:
        c, w = homogeneous_trace
        result = generate_candidates(c, w, n_candidates=10, perturbation=0.10, seed=42)
        assert abs(result.baseline_F + result.baseline_omega - 1.0) < 1e-12
        assert result.baseline_IC <= result.baseline_F + 1e-12

    def test_duality_all_candidates(self, homogeneous_trace: tuple[np.ndarray, np.ndarray]) -> None:
        c, w = homogeneous_trace
        result = generate_candidates(c, w, n_candidates=50, perturbation=0.20, seed=42)
        for cand in result.candidates:
            assert abs(cand.F + cand.omega - 1.0) < 1e-10, f"Duality violated: F={cand.F}, omega={cand.omega}"

    def test_integrity_bound_all_candidates(self, homogeneous_trace: tuple[np.ndarray, np.ndarray]) -> None:
        c, w = homogeneous_trace
        result = generate_candidates(c, w, n_candidates=50, perturbation=0.20, seed=42)
        for cand in result.candidates:
            assert cand.IC <= cand.F + 1e-10, f"IC > F: IC={cand.IC}, F={cand.F}"

    def test_candidate_count(self, homogeneous_trace: tuple[np.ndarray, np.ndarray]) -> None:
        c, w = homogeneous_trace
        result = generate_candidates(c, w, n_candidates=50, perturbation=0.20, seed=42)
        assert len(result.candidates) == 50

    def test_regime_counts_sum(self, homogeneous_trace: tuple[np.ndarray, np.ndarray]) -> None:
        c, w = homogeneous_trace
        result = generate_candidates(c, w, n_candidates=100, perturbation=0.25, seed=42)
        total = sum(result.regime_counts.values())
        assert total == 100

    def test_seed_reproducibility(self, homogeneous_trace: tuple[np.ndarray, np.ndarray]) -> None:
        c, w = homogeneous_trace
        r1 = generate_candidates(c, w, n_candidates=20, perturbation=0.20, seed=123)
        r2 = generate_candidates(c, w, n_candidates=20, perturbation=0.20, seed=123)
        for c1, c2 in zip(r1.candidates, r2.candidates, strict=True):
            assert c1.F == c2.F
            assert c1.omega == c2.omega
            assert c1.IC == c2.IC

    def test_different_seeds_differ(self, homogeneous_trace: tuple[np.ndarray, np.ndarray]) -> None:
        c, w = homogeneous_trace
        r1 = generate_candidates(c, w, n_candidates=20, perturbation=0.20, seed=1)
        r2 = generate_candidates(c, w, n_candidates=20, perturbation=0.20, seed=2)
        # At least some candidates should differ
        diffs = sum(1 for c1, c2 in zip(r1.candidates, r2.candidates, strict=True) if c1.F != c2.F)
        assert diffs > 0

    def test_passed_candidates_property(self, homogeneous_trace: tuple[np.ndarray, np.ndarray]) -> None:
        c, w = homogeneous_trace
        result = generate_candidates(c, w, n_candidates=50, perturbation=0.25, seed=42)
        passed = result.passed_candidates
        assert len(passed) == result.n_passed
        for p in passed:
            assert p.seam_pass is True


# ── Edge Cases ───────────────────────────────────────────────────────


class TestDriftEngineEdgeCases:
    """Edge cases and boundary conditions."""

    def test_zero_perturbation(self, homogeneous_trace: tuple[np.ndarray, np.ndarray]) -> None:
        c, w = homogeneous_trace
        result = generate_candidates(c, w, n_candidates=10, perturbation=0.0, seed=42)
        # All candidates should match baseline
        for cand in result.candidates:
            assert abs(cand.F - result.baseline_F) < 1e-10

    def test_single_candidate(self, homogeneous_trace: tuple[np.ndarray, np.ndarray]) -> None:
        c, w = homogeneous_trace
        result = generate_candidates(c, w, n_candidates=1, perturbation=0.20, seed=42)
        assert len(result.candidates) == 1

    def test_heterogeneous_baseline_gap(self, heterogeneous_trace: tuple[np.ndarray, np.ndarray]) -> None:
        c, w = heterogeneous_trace
        result = generate_candidates(c, w, n_candidates=50, perturbation=0.20, seed=42)
        # Heterogeneous baseline should have non-trivial gap
        assert result.baseline_gap > 0.01

    def test_dead_channel_low_ic(self, dead_channel_trace: tuple[np.ndarray, np.ndarray]) -> None:
        c, w = dead_channel_trace
        result = generate_candidates(c, w, n_candidates=50, perturbation=0.20, seed=42)
        # Dead channel pulls IC far below F
        assert result.baseline_gap > 0.10

    def test_best_candidate_is_best(self, homogeneous_trace: tuple[np.ndarray, np.ndarray]) -> None:
        c, w = homogeneous_trace
        result = generate_candidates(c, w, n_candidates=100, perturbation=0.25, seed=42)
        if result.best_candidate and result.n_passed > 1:
            passed = result.passed_candidates
            max_score = max(p.return_score for p in passed)
            assert abs(result.best_candidate.return_score - max_score) < 1e-12

    def test_return_score_positive(self, homogeneous_trace: tuple[np.ndarray, np.ndarray]) -> None:
        c, w = homogeneous_trace
        result = generate_candidates(c, w, n_candidates=50, perturbation=0.25, seed=42)
        for cand in result.candidates:
            assert cand.return_score >= 0.0

    def test_high_dimensional_trace(self) -> None:
        """Test with a large number of channels."""
        c = np.full(32, 0.65)
        w = np.ones(32) / 32
        result = generate_candidates(c, w, n_candidates=50, perturbation=0.25, seed=42)
        assert len(result.candidates) == 50
        for cand in result.candidates:
            assert abs(cand.F + cand.omega - 1.0) < 1e-10
