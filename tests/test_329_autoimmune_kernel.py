"""Tests for autoimmune kernel closure (immunology domain).

Validates 12 autoimmune disease entities, 8-channel trace construction,
Tier-1 kernel identities, and 6 theorems (T-AI-1 through T-AI-6).
"""

from __future__ import annotations

import math

import numpy as np
import pytest

from closures.immunology.autoimmune_kernel import (
    AI_CHANNELS,
    AI_ENTITIES,
    N_AI_CHANNELS,
    AIKernelResult,
    compute_ai_kernel,
    compute_all_entities,
    verify_all_theorems,
    verify_t_ai_1,
    verify_t_ai_2,
    verify_t_ai_3,
    verify_t_ai_4,
    verify_t_ai_5,
    verify_t_ai_6,
)


@pytest.fixture(scope="module")
def all_results() -> list[AIKernelResult]:
    return compute_all_entities()


# ── Entity Catalog ──


class TestEntityCatalog:
    def test_entity_count(self):
        assert len(AI_ENTITIES) == 12

    def test_channel_count(self):
        assert N_AI_CHANNELS == 8
        assert len(AI_CHANNELS) == 8

    def test_all_categories_present(self):
        cats = {e.category for e in AI_ENTITIES}
        assert cats == {"organ_specific", "systemic", "overlap"}

    def test_category_counts(self):
        organ = [e for e in AI_ENTITIES if e.category == "organ_specific"]
        systemic = [e for e in AI_ENTITIES if e.category == "systemic"]
        overlap = [e for e in AI_ENTITIES if e.category == "overlap"]
        assert len(organ) == 5
        assert len(systemic) == 4
        assert len(overlap) == 3

    def test_unique_names(self):
        names = [e.name for e in AI_ENTITIES]
        assert len(names) == len(set(names))

    @pytest.mark.parametrize("entity", AI_ENTITIES, ids=lambda e: e.name)
    def test_trace_vector_shape(self, entity):
        c = entity.trace_vector()
        assert c.shape == (8,)

    @pytest.mark.parametrize("entity", AI_ENTITIES, ids=lambda e: e.name)
    def test_trace_vector_bounds(self, entity):
        c = entity.trace_vector()
        assert np.all(c >= 0.0) and np.all(c <= 1.0)


# ── Tier-1 Kernel Identities ──


class TestTier1Identities:
    @pytest.mark.parametrize("entity", AI_ENTITIES, ids=lambda e: e.name)
    def test_duality_identity(self, entity):
        r = compute_ai_kernel(entity)
        assert abs(r.F + r.omega - 1.0) < 1e-12

    @pytest.mark.parametrize("entity", AI_ENTITIES, ids=lambda e: e.name)
    def test_integrity_bound(self, entity):
        r = compute_ai_kernel(entity)
        assert r.IC <= r.F + 1e-12

    @pytest.mark.parametrize("entity", AI_ENTITIES, ids=lambda e: e.name)
    def test_log_integrity_relation(self, entity):
        r = compute_ai_kernel(entity)
        assert abs(r.IC - math.exp(r.kappa)) < 1e-10


# ── Theorems ──


class TestTheorems:
    def test_t_ai_1(self, all_results):
        t = verify_t_ai_1(all_results)
        assert t["passed"], t

    def test_t_ai_2(self, all_results):
        t = verify_t_ai_2(all_results)
        assert t["passed"], t

    def test_t_ai_3(self, all_results):
        t = verify_t_ai_3(all_results)
        assert t["passed"], t

    def test_t_ai_4(self, all_results):
        t = verify_t_ai_4(all_results)
        assert t["passed"], t

    def test_t_ai_5(self, all_results):
        t = verify_t_ai_5(all_results)
        assert t["passed"], t

    def test_t_ai_6(self, all_results):
        t = verify_t_ai_6(all_results)
        assert t["passed"], t

    def test_all_theorems_pass(self, all_results):
        results_list = verify_all_theorems()
        for t in results_list:
            assert t["passed"], f"{t['name']} failed: {t}"


# ── Regime Classification ──


class TestRegimeClassification:
    @pytest.mark.parametrize("entity", AI_ENTITIES, ids=lambda e: e.name)
    def test_regime_is_valid(self, entity):
        r = compute_ai_kernel(entity)
        assert r.regime in ("Stable", "Watch", "Collapse")

    def test_regime_consistency_with_omega(self, all_results):
        for r in all_results:
            if r.omega >= 0.30:
                assert r.regime == "Collapse", f"{r.name}: ω={r.omega} but regime={r.regime}"


# ── Serialization ──


class TestSerialization:
    def test_to_dict_keys(self, all_results):
        d = all_results[0].to_dict()
        expected = {"name", "category", "F", "omega", "S", "C", "kappa", "IC", "regime"}
        assert set(d.keys()) == expected
