"""Tests for developmental neuroscience closure (clinical-neuroscience domain).

Validates 12 brain developmental stages, 8-channel trace construction,
Tier-1 kernel identities, and 6 theorems (T-DN-1 through T-DN-6).
"""

from __future__ import annotations

import math

import numpy as np
import pytest

from closures.clinical_neuroscience.developmental_neuroscience import (
    DN_CHANNELS,
    DN_ENTITIES,
    N_DN_CHANNELS,
    DNKernelResult,
    compute_all_entities,
    compute_dn_kernel,
    verify_all_theorems,
    verify_t_dn_1,
    verify_t_dn_2,
    verify_t_dn_3,
    verify_t_dn_4,
    verify_t_dn_5,
    verify_t_dn_6,
)


@pytest.fixture(scope="module")
def all_results() -> list[DNKernelResult]:
    return compute_all_entities()


class TestEntityCatalog:
    def test_entity_count(self):
        assert len(DN_ENTITIES) == 12

    def test_channel_count(self):
        assert N_DN_CHANNELS == 8
        assert len(DN_CHANNELS) == 8

    def test_all_categories_present(self):
        cats = {e.category for e in DN_ENTITIES}
        assert cats == {"prenatal", "childhood", "adolescent", "aging"}

    @pytest.mark.parametrize("entity", DN_ENTITIES, ids=lambda e: e.name)
    def test_trace_vector_shape(self, entity):
        assert entity.trace_vector().shape == (8,)

    @pytest.mark.parametrize("entity", DN_ENTITIES, ids=lambda e: e.name)
    def test_trace_vector_bounds(self, entity):
        c = entity.trace_vector()
        assert np.all(c >= 0.0) and np.all(c <= 1.0)


class TestTier1Identities:
    @pytest.mark.parametrize("entity", DN_ENTITIES, ids=lambda e: e.name)
    def test_duality_identity(self, entity):
        r = compute_dn_kernel(entity)
        assert abs(r.F + r.omega - 1.0) < 1e-12

    @pytest.mark.parametrize("entity", DN_ENTITIES, ids=lambda e: e.name)
    def test_integrity_bound(self, entity):
        r = compute_dn_kernel(entity)
        assert r.IC <= r.F + 1e-12

    @pytest.mark.parametrize("entity", DN_ENTITIES, ids=lambda e: e.name)
    def test_log_integrity_relation(self, entity):
        r = compute_dn_kernel(entity)
        assert abs(r.IC - math.exp(r.kappa)) < 1e-10


class TestTheorems:
    def test_t_dn_1(self, all_results):
        assert verify_t_dn_1(all_results)["passed"]

    def test_t_dn_2(self, all_results):
        assert verify_t_dn_2(all_results)["passed"]

    def test_t_dn_3(self, all_results):
        assert verify_t_dn_3(all_results)["passed"]

    def test_t_dn_4(self, all_results):
        assert verify_t_dn_4(all_results)["passed"]

    def test_t_dn_5(self, all_results):
        assert verify_t_dn_5(all_results)["passed"]

    def test_t_dn_6(self, all_results):
        assert verify_t_dn_6(all_results)["passed"]

    def test_all_theorems_pass(self):
        for t in verify_all_theorems():
            assert t["passed"], f"{t['name']} failed: {t}"


class TestRegimeClassification:
    @pytest.mark.parametrize("entity", DN_ENTITIES, ids=lambda e: e.name)
    def test_regime_is_valid(self, entity):
        r = compute_dn_kernel(entity)
        assert r.regime in ("Stable", "Watch", "Collapse")
