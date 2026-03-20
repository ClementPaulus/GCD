"""Tests for cosmological memory closure (spacetime-memory domain).

Validates 12 cosmological memory entities, 8-channel trace construction,
Tier-1 kernel identities, and 6 theorems (T-CM-1 through T-CM-6).
"""

from __future__ import annotations

import math

import numpy as np
import pytest

from closures.spacetime_memory.cosmological_memory import (
    CM_CHANNELS,
    CM_ENTITIES,
    N_CM_CHANNELS,
    CMKernelResult,
    compute_all_entities,
    compute_cm_kernel,
    verify_all_theorems,
    verify_t_cm_1,
    verify_t_cm_2,
    verify_t_cm_3,
    verify_t_cm_4,
    verify_t_cm_5,
    verify_t_cm_6,
)


@pytest.fixture(scope="module")
def all_results() -> list[CMKernelResult]:
    return compute_all_entities()


class TestEntityCatalog:
    def test_entity_count(self):
        assert len(CM_ENTITIES) == 12

    def test_channel_count(self):
        assert N_CM_CHANNELS == 8
        assert len(CM_CHANNELS) == 8

    def test_all_categories_present(self):
        cats = {e.category for e in CM_ENTITIES}
        assert cats == {"radiation", "structure", "relic", "dynamic"}

    @pytest.mark.parametrize("entity", CM_ENTITIES, ids=lambda e: e.name)
    def test_trace_vector_shape(self, entity):
        assert entity.trace_vector().shape == (8,)

    @pytest.mark.parametrize("entity", CM_ENTITIES, ids=lambda e: e.name)
    def test_trace_vector_bounds(self, entity):
        c = entity.trace_vector()
        assert np.all(c >= 0.0) and np.all(c <= 1.0)


class TestTier1Identities:
    @pytest.mark.parametrize("entity", CM_ENTITIES, ids=lambda e: e.name)
    def test_duality_identity(self, entity):
        r = compute_cm_kernel(entity)
        assert abs(r.F + r.omega - 1.0) < 1e-12

    @pytest.mark.parametrize("entity", CM_ENTITIES, ids=lambda e: e.name)
    def test_integrity_bound(self, entity):
        r = compute_cm_kernel(entity)
        assert r.IC <= r.F + 1e-12

    @pytest.mark.parametrize("entity", CM_ENTITIES, ids=lambda e: e.name)
    def test_log_integrity_relation(self, entity):
        r = compute_cm_kernel(entity)
        assert abs(r.IC - math.exp(r.kappa)) < 1e-10


class TestTheorems:
    def test_t_cm_1(self, all_results):
        assert verify_t_cm_1(all_results)["passed"]

    def test_t_cm_2(self, all_results):
        assert verify_t_cm_2(all_results)["passed"]

    def test_t_cm_3(self, all_results):
        assert verify_t_cm_3(all_results)["passed"]

    def test_t_cm_4(self, all_results):
        assert verify_t_cm_4(all_results)["passed"]

    def test_t_cm_5(self, all_results):
        assert verify_t_cm_5(all_results)["passed"]

    def test_t_cm_6(self, all_results):
        assert verify_t_cm_6(all_results)["passed"]

    def test_all_theorems_pass(self):
        for t in verify_all_theorems():
            assert t["passed"], f"{t['name']} failed: {t}"


class TestRegimeClassification:
    @pytest.mark.parametrize("entity", CM_ENTITIES, ids=lambda e: e.name)
    def test_regime_is_valid(self, entity):
        r = compute_cm_kernel(entity)
        assert r.regime in ("Stable", "Watch", "Collapse")
