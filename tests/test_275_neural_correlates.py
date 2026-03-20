"""Tests for neural correlates closure (consciousness-coherence domain).

Validates 12 neural correlate of consciousness entities, 8-channel trace
construction, Tier-1 kernel identities, and 6 theorems (T-NC-1 through T-NC-6).
"""

from __future__ import annotations

import math

import numpy as np
import pytest

from closures.consciousness_coherence.neural_correlates import (
    N_NC_CHANNELS,
    NC_CHANNELS,
    NC_ENTITIES,
    NCKernelResult,
    compute_all_entities,
    compute_nc_kernel,
    verify_all_theorems,
    verify_t_nc_1,
    verify_t_nc_2,
    verify_t_nc_3,
    verify_t_nc_4,
    verify_t_nc_5,
    verify_t_nc_6,
)


@pytest.fixture(scope="module")
def all_results() -> list[NCKernelResult]:
    return compute_all_entities()


class TestEntityCatalog:
    def test_entity_count(self):
        assert len(NC_ENTITIES) == 12

    def test_channel_count(self):
        assert N_NC_CHANNELS == 8
        assert len(NC_CHANNELS) == 8

    def test_all_categories_present(self):
        cats = {e.category for e in NC_ENTITIES}
        assert cats == {"binding", "network", "gating", "modulation"}

    @pytest.mark.parametrize("entity", NC_ENTITIES, ids=lambda e: e.name)
    def test_trace_vector_shape(self, entity):
        assert entity.trace_vector().shape == (8,)

    @pytest.mark.parametrize("entity", NC_ENTITIES, ids=lambda e: e.name)
    def test_trace_vector_bounds(self, entity):
        c = entity.trace_vector()
        assert np.all(c >= 0.0) and np.all(c <= 1.0)


class TestTier1Identities:
    @pytest.mark.parametrize("entity", NC_ENTITIES, ids=lambda e: e.name)
    def test_duality_identity(self, entity):
        r = compute_nc_kernel(entity)
        assert abs(r.F + r.omega - 1.0) < 1e-12

    @pytest.mark.parametrize("entity", NC_ENTITIES, ids=lambda e: e.name)
    def test_integrity_bound(self, entity):
        r = compute_nc_kernel(entity)
        assert r.IC <= r.F + 1e-12

    @pytest.mark.parametrize("entity", NC_ENTITIES, ids=lambda e: e.name)
    def test_log_integrity_relation(self, entity):
        r = compute_nc_kernel(entity)
        assert abs(r.IC - math.exp(r.kappa)) < 1e-10


class TestTheorems:
    def test_t_nc_1(self, all_results):
        assert verify_t_nc_1(all_results)["passed"]

    def test_t_nc_2(self, all_results):
        assert verify_t_nc_2(all_results)["passed"]

    def test_t_nc_3(self, all_results):
        assert verify_t_nc_3(all_results)["passed"]

    def test_t_nc_4(self, all_results):
        assert verify_t_nc_4(all_results)["passed"]

    def test_t_nc_5(self, all_results):
        assert verify_t_nc_5(all_results)["passed"]

    def test_t_nc_6(self, all_results):
        assert verify_t_nc_6(all_results)["passed"]

    def test_all_theorems_pass(self):
        for t in verify_all_theorems():
            assert t["passed"], f"{t['name']} failed: {t}"


class TestRegimeClassification:
    @pytest.mark.parametrize("entity", NC_ENTITIES, ids=lambda e: e.name)
    def test_regime_is_valid(self, entity):
        r = compute_nc_kernel(entity)
        assert r.regime in ("Stable", "Watch", "Collapse")
