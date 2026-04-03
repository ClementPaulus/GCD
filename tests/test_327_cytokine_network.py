"""Tests for cytokine network closure (immunology domain).

Validates 12 cytokine entities, 8-channel trace construction,
Tier-1 kernel identities, and 6 theorems (T-CY-1 through T-CY-6).
"""

from __future__ import annotations

import math

import numpy as np
import pytest

from closures.immunology.cytokine_network import (
    CY_CHANNELS,
    CY_ENTITIES,
    N_CY_CHANNELS,
    CYKernelResult,
    compute_all_entities,
    compute_cy_kernel,
    verify_all_theorems,
    verify_t_cy_1,
    verify_t_cy_2,
    verify_t_cy_3,
    verify_t_cy_4,
    verify_t_cy_5,
    verify_t_cy_6,
)


@pytest.fixture(scope="module")
def all_results() -> list[CYKernelResult]:
    return compute_all_entities()


# ── Entity Catalog ──


class TestEntityCatalog:
    def test_entity_count(self):
        assert len(CY_ENTITIES) == 12

    def test_channel_count(self):
        assert N_CY_CHANNELS == 8
        assert len(CY_CHANNELS) == 8

    def test_all_functional_classes_present(self):
        classes = {e.functional_class for e in CY_ENTITIES}
        assert classes == {"pro_inflammatory", "th_polarizing", "regulatory"}

    def test_unique_names(self):
        names = [e.name for e in CY_ENTITIES]
        assert len(names) == len(set(names))

    @pytest.mark.parametrize("entity", CY_ENTITIES, ids=lambda e: e.name)
    def test_trace_vector_shape(self, entity):
        c = entity.trace_vector()
        assert c.shape == (8,)

    @pytest.mark.parametrize("entity", CY_ENTITIES, ids=lambda e: e.name)
    def test_trace_vector_bounds(self, entity):
        c = entity.trace_vector()
        assert np.all(c >= 0.0) and np.all(c <= 1.0)


# ── Tier-1 Kernel Identities ──


class TestTier1Identities:
    @pytest.mark.parametrize("entity", CY_ENTITIES, ids=lambda e: e.name)
    def test_duality_identity(self, entity):
        r = compute_cy_kernel(entity)
        assert abs(r.F + r.omega - 1.0) < 1e-12

    @pytest.mark.parametrize("entity", CY_ENTITIES, ids=lambda e: e.name)
    def test_integrity_bound(self, entity):
        r = compute_cy_kernel(entity)
        assert r.IC <= r.F + 1e-12

    @pytest.mark.parametrize("entity", CY_ENTITIES, ids=lambda e: e.name)
    def test_log_integrity_relation(self, entity):
        r = compute_cy_kernel(entity)
        assert abs(r.IC - math.exp(r.kappa)) < 1e-10


# ── Theorems ──


class TestTheorems:
    def test_t_cy_1(self, all_results):
        t = verify_t_cy_1(all_results)
        assert t["passed"], t

    def test_t_cy_2(self, all_results):
        t = verify_t_cy_2(all_results)
        assert t["passed"], t

    def test_t_cy_3(self, all_results):
        t = verify_t_cy_3(all_results)
        assert t["passed"], t

    def test_t_cy_4(self, all_results):
        t = verify_t_cy_4(all_results)
        assert t["passed"], t

    def test_t_cy_5(self, all_results):
        t = verify_t_cy_5(all_results)
        assert t["passed"], t

    def test_t_cy_6(self, all_results):
        t = verify_t_cy_6(all_results)
        assert t["passed"], t

    def test_all_theorems_pass(self, all_results):
        results_list = verify_all_theorems()
        for t in results_list:
            assert t["passed"], f"{t['name']} failed: {t}"


# ── Regime Classification ──


class TestRegimeClassification:
    @pytest.mark.parametrize("entity", CY_ENTITIES, ids=lambda e: e.name)
    def test_regime_is_valid(self, entity):
        r = compute_cy_kernel(entity)
        assert r.regime in ("Stable", "Watch", "Collapse")

    def test_regime_consistency_with_omega(self, all_results):
        for r in all_results:
            if r.omega >= 0.30:
                assert r.regime == "Collapse", f"{r.name}: ω={r.omega} but regime={r.regime}"


# ── Serialization ──


class TestSerialization:
    def test_to_dict_keys(self, all_results):
        d = all_results[0].to_dict()
        expected = {"name", "functional_class", "F", "omega", "S", "C", "kappa", "IC", "regime"}
        assert set(d.keys()) == expected
