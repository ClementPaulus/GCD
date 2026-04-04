"""Tests for closures/rcft/regime_derivation.py — D(x,t) ↔ Kernel Regime Mapping.

Tests T-RD-1 through T-RD-6 (6 theorems, 12 entities, 8 channels).
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
import pytest

_WORKSPACE = Path(__file__).resolve().parents[1]
for _p in [str(_WORKSPACE / "src"), str(_WORKSPACE)]:
    if _p not in sys.path:
        sys.path.insert(0, _p)

from closures.rcft.regime_derivation import (
    RD_ENTITIES,
    compute_all_entities,
    compute_rd_kernel,
    curvature_cost,
    drift_cost,
    total_debit,
    verify_all_theorems,
    verify_t_rd_1,
    verify_t_rd_2,
    verify_t_rd_3,
    verify_t_rd_4,
    verify_t_rd_5,
    verify_t_rd_6,
)

# ── Fixtures ──


@pytest.fixture(scope="module")
def results():
    return compute_all_entities()


# ── Entity Catalog ──


class TestEntityCatalog:
    def test_entity_count(self):
        assert len(RD_ENTITIES) == 12

    def test_categories(self):
        cats = {e.category for e in RD_ENTITIES}
        assert cats == {"deep_stable", "watch_band", "onset_collapse", "deep_collapse"}

    def test_three_per_category(self):
        for cat in ("deep_stable", "watch_band", "onset_collapse", "deep_collapse"):
            count = sum(1 for e in RD_ENTITIES if e.category == cat)
            assert count == 3, f"{cat} has {count} entities, expected 3"

    def test_trace_shape(self):
        for e in RD_ENTITIES:
            c = e.trace_vector()
            assert c.shape == (8,)

    def test_trace_bounds(self):
        for e in RD_ENTITIES:
            c = e.trace_vector()
            assert np.all(c >= 0.0) and np.all(c <= 1.0), f"{e.name}: out of [0,1]"


# ── Tier-1 Identities ──


class TestTier1Identities:
    @pytest.mark.parametrize("entity", RD_ENTITIES, ids=[e.name for e in RD_ENTITIES])
    def test_duality(self, entity):
        r = compute_rd_kernel(entity)
        assert abs(r.F + r.omega - 1.0) < 1e-12

    @pytest.mark.parametrize("entity", RD_ENTITIES, ids=[e.name for e in RD_ENTITIES])
    def test_integrity_bound(self, entity):
        r = compute_rd_kernel(entity)
        assert r.IC <= r.F + 1e-12

    @pytest.mark.parametrize("entity", RD_ENTITIES, ids=[e.name for e in RD_ENTITIES])
    def test_log_integrity(self, entity):
        r = compute_rd_kernel(entity)
        assert abs(r.IC - math.exp(r.kappa)) < 1e-10


# ── Budget Functions ──


class TestBudgetFunctions:
    def test_drift_cost_monotone(self):
        omegas = [0.01, 0.05, 0.10, 0.20, 0.30, 0.50]
        costs = [drift_cost(w) for w in omegas]
        for i in range(len(costs) - 1):
            assert costs[i] < costs[i + 1]

    def test_curvature_cost_positive(self):
        assert curvature_cost(0.5) > 0

    def test_total_debit_sum(self):
        omega, C = 0.25, 0.40
        assert abs(total_debit(omega, C) - (drift_cost(omega) + curvature_cost(C))) < 1e-12


# ── Theorems ──


class TestTheorems:
    def test_t_rd_1(self, results):
        assert verify_t_rd_1(results)["passed"]

    def test_t_rd_2(self, results):
        assert verify_t_rd_2(results)["passed"]

    def test_t_rd_3(self, results):
        assert verify_t_rd_3(results)["passed"]

    def test_t_rd_4(self, results):
        assert verify_t_rd_4(results)["passed"]

    def test_t_rd_5(self, results):
        assert verify_t_rd_5(results)["passed"]

    def test_t_rd_6(self, results):
        assert verify_t_rd_6(results)["passed"]

    def test_all_theorems_pass(self):
        for t in verify_all_theorems():
            assert t["passed"], f"{t['name']} FAILED"


# ── Regime Classification ──


class TestRegimeClassification:
    @pytest.mark.parametrize("entity", RD_ENTITIES, ids=[e.name for e in RD_ENTITIES])
    def test_regime_valid(self, entity):
        r = compute_rd_kernel(entity)
        assert r.regime in {"Stable", "Watch", "Collapse"}
