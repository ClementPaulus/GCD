"""Tests for spectral line theorems (T-SP-1 through T-SP-6).

Validates 12 spectral transition entities, 6-channel trace construction,
Tier-1 kernel identities, and 6 theorems.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
import pytest

_WORKSPACE = Path(__file__).resolve().parents[1]
if str(_WORKSPACE) not in sys.path:
    sys.path.insert(0, str(_WORKSPACE))

from closures.atomic_physics.spectral_theorems import (
    N_SP_CHANNELS,
    SP_CHANNELS,
    SP_ENTITIES,
    SPKernelResult,
    compute_all_entities,
    compute_sp_kernel,
    verify_all_theorems,
    verify_t_sp_1,
    verify_t_sp_2,
    verify_t_sp_3,
    verify_t_sp_4,
    verify_t_sp_5,
    verify_t_sp_6,
)


@pytest.fixture(scope="module")
def all_results() -> list[SPKernelResult]:
    return compute_all_entities()


class TestEntityCatalog:
    def test_entity_count(self):
        assert len(SP_ENTITIES) == 12

    def test_channel_count(self):
        assert N_SP_CHANNELS == 6
        assert len(SP_CHANNELS) == 6

    def test_all_categories_present(self):
        cats = {e.category for e in SP_ENTITIES}
        assert "hydrogen_lyman" in cats
        assert "hydrogen_balmer" in cats
        assert "hydrogen_paschen" in cats
        assert "multi_z" in cats

    @pytest.mark.parametrize("entity", SP_ENTITIES, ids=lambda e: e.name)
    def test_trace_vector_shape(self, entity):
        c = entity.trace_vector()
        assert c.shape == (6,)

    @pytest.mark.parametrize("entity", SP_ENTITIES, ids=lambda e: e.name)
    def test_trace_vector_positive(self, entity):
        c = entity.trace_vector()
        assert np.all(c > 0.0)
        # Multi-Z entities may exceed 1.0 before kernel clipping — correct by design


class TestTier1Identities:
    @pytest.mark.parametrize("entity", SP_ENTITIES, ids=lambda e: e.name)
    def test_duality_identity(self, entity):
        r = compute_sp_kernel(entity)
        assert abs(r.F + r.omega - 1.0) < 1e-12

    @pytest.mark.parametrize("entity", SP_ENTITIES, ids=lambda e: e.name)
    def test_integrity_bound(self, entity):
        r = compute_sp_kernel(entity)
        assert r.IC <= r.F + 1e-12

    @pytest.mark.parametrize("entity", SP_ENTITIES, ids=lambda e: e.name)
    def test_log_integrity_relation(self, entity):
        r = compute_sp_kernel(entity)
        assert abs(r.IC - math.exp(r.kappa)) < 1e-10


class TestTheorems:
    def test_t_sp_1(self, all_results):
        assert verify_t_sp_1(all_results)["passed"]

    def test_t_sp_2(self, all_results):
        assert verify_t_sp_2(all_results)["passed"]

    def test_t_sp_3(self, all_results):
        assert verify_t_sp_3(all_results)["passed"]

    def test_t_sp_4(self, all_results):
        assert verify_t_sp_4(all_results)["passed"]

    def test_t_sp_5(self, all_results):
        assert verify_t_sp_5(all_results)["passed"]

    def test_t_sp_6(self, all_results):
        assert verify_t_sp_6(all_results)["passed"]

    def test_all_theorems_pass(self):
        for t in verify_all_theorems():
            assert t["passed"], f"{t['name']} failed: {t}"


class TestRegimeClassification:
    @pytest.mark.parametrize("entity", SP_ENTITIES, ids=lambda e: e.name)
    def test_regime_is_valid(self, entity):
        r = compute_sp_kernel(entity)
        assert r.regime in {"Stable", "Watch", "Collapse"}
