"""Tests for closures/rcft/epistemic_agents.py — Three-Agent Epistemic Model.

Tests T-EA-1 through T-EA-6 (6 theorems, 12 entities, 8 channels).
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

from closures.rcft.epistemic_agents import (
    EA_ENTITIES,
    compute_all_entities,
    compute_ea_kernel,
    verify_all_theorems,
    verify_t_ea_1,
    verify_t_ea_2,
    verify_t_ea_3,
    verify_t_ea_4,
    verify_t_ea_5,
    verify_t_ea_6,
)

# ── Fixtures ──


@pytest.fixture(scope="module")
def results():
    return compute_all_entities()


# ── Entity Catalog ──


class TestEntityCatalog:
    def test_entity_count(self):
        assert len(EA_ENTITIES) == 12

    def test_categories(self):
        cats = {e.category for e in EA_ENTITIES}
        assert cats == {"high_coherence", "moderate_coherence", "low_coherence", "degenerate"}

    def test_three_per_category(self):
        for cat in ("high_coherence", "moderate_coherence", "low_coherence", "degenerate"):
            count = sum(1 for e in EA_ENTITIES if e.category == cat)
            assert count == 3, f"{cat} has {count} entities, expected 3"

    def test_trace_shape(self):
        for e in EA_ENTITIES:
            c = e.trace_vector()
            assert c.shape == (8,)

    def test_trace_bounds(self):
        for e in EA_ENTITIES:
            c = e.trace_vector()
            assert np.all(c >= 0.0) and np.all(c <= 1.0), f"{e.name}: out of [0,1]"


# ── Tier-1 Identities ──


class TestTier1Identities:
    @pytest.mark.parametrize("entity", EA_ENTITIES, ids=[e.name for e in EA_ENTITIES])
    def test_duality(self, entity):
        r = compute_ea_kernel(entity)
        assert abs(r.F + r.omega - 1.0) < 1e-12

    @pytest.mark.parametrize("entity", EA_ENTITIES, ids=[e.name for e in EA_ENTITIES])
    def test_integrity_bound(self, entity):
        r = compute_ea_kernel(entity)
        assert r.IC <= r.F + 1e-12

    @pytest.mark.parametrize("entity", EA_ENTITIES, ids=[e.name for e in EA_ENTITIES])
    def test_log_integrity(self, entity):
        r = compute_ea_kernel(entity)
        assert abs(r.IC - math.exp(r.kappa)) < 1e-10


# ── Theorems ──


class TestTheorems:
    def test_t_ea_1(self, results):
        assert verify_t_ea_1(results)["passed"]

    def test_t_ea_2(self, results):
        assert verify_t_ea_2(results)["passed"]

    def test_t_ea_3(self, results):
        assert verify_t_ea_3(results)["passed"]

    def test_t_ea_4(self, results):
        assert verify_t_ea_4(results)["passed"]

    def test_t_ea_5(self, results):
        assert verify_t_ea_5(results)["passed"]

    def test_t_ea_6(self, results):
        assert verify_t_ea_6(results)["passed"]

    def test_all_theorems_pass(self):
        for t in verify_all_theorems():
            assert t["passed"], f"{t['name']} FAILED"


# ── Regime Classification ──


class TestRegimeClassification:
    @pytest.mark.parametrize("entity", EA_ENTITIES, ids=[e.name for e in EA_ENTITIES])
    def test_regime_valid(self, entity):
        r = compute_ea_kernel(entity)
        assert r.regime in {"Stable", "Watch", "Collapse"}
