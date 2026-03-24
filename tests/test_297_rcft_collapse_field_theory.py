"""Tests for RCFT collapse field theory closure.

Validates 12 fundamental collapse field configurations, 8-channel trace
construction, Tier-1 kernel identities, and 6 theorems (T-CFT-1 through T-CFT-6).
"""

from __future__ import annotations

import math

import numpy as np
import pytest

from closures.rcft.collapse_field_theory import (
    CFT_CHANNELS,
    CFT_ENTITIES,
    N_CFT_CHANNELS,
    CFTKernelResult,
    compute_all_entities,
    compute_cft_kernel,
    verify_all_theorems,
    verify_t_cft_1,
    verify_t_cft_2,
    verify_t_cft_3,
    verify_t_cft_4,
    verify_t_cft_5,
    verify_t_cft_6,
)


@pytest.fixture(scope="module")
def all_results() -> list[CFTKernelResult]:
    return compute_all_entities()


class TestEntityCatalog:
    def test_entity_count(self):
        assert len(CFT_ENTITIES) == 12

    def test_channel_count(self):
        assert N_CFT_CHANNELS == 8
        assert len(CFT_CHANNELS) == 8

    def test_all_categories_present(self):
        cats = {e.category for e in CFT_ENTITIES}
        assert cats == {"fixed_point", "phase_boundary", "recursive", "extremal"}

    def test_three_per_category(self):
        from collections import Counter

        counts = Counter(e.category for e in CFT_ENTITIES)
        assert all(v == 3 for v in counts.values())

    @pytest.mark.parametrize("entity", CFT_ENTITIES, ids=lambda e: e.name)
    def test_trace_vector_shape(self, entity):
        assert entity.trace_vector().shape == (8,)

    @pytest.mark.parametrize("entity", CFT_ENTITIES, ids=lambda e: e.name)
    def test_trace_vector_bounds(self, entity):
        c = entity.trace_vector()
        assert np.all(c >= 0.0) and np.all(c <= 1.0)

    @pytest.mark.parametrize("entity", CFT_ENTITIES, ids=lambda e: e.name)
    def test_unique_names(self, entity):
        names = [e.name for e in CFT_ENTITIES]
        assert names.count(entity.name) == 1


class TestTier1Identities:
    @pytest.mark.parametrize("entity", CFT_ENTITIES, ids=lambda e: e.name)
    def test_duality_identity(self, entity):
        r = compute_cft_kernel(entity)
        assert abs(r.F + r.omega - 1.0) < 1e-12

    @pytest.mark.parametrize("entity", CFT_ENTITIES, ids=lambda e: e.name)
    def test_integrity_bound(self, entity):
        r = compute_cft_kernel(entity)
        assert r.IC <= r.F + 1e-12

    @pytest.mark.parametrize("entity", CFT_ENTITIES, ids=lambda e: e.name)
    def test_log_integrity_relation(self, entity):
        r = compute_cft_kernel(entity)
        assert abs(r.IC - math.exp(r.kappa)) < 1e-10

    @pytest.mark.parametrize("entity", CFT_ENTITIES, ids=lambda e: e.name)
    def test_entropy_nonneg(self, entity):
        r = compute_cft_kernel(entity)
        assert r.S >= -1e-12

    @pytest.mark.parametrize("entity", CFT_ENTITIES, ids=lambda e: e.name)
    def test_curvature_nonneg(self, entity):
        r = compute_cft_kernel(entity)
        assert r.C >= -1e-12


class TestTheorems:
    def test_t_cft_1(self, all_results):
        assert verify_t_cft_1(all_results)["passed"]

    def test_t_cft_2(self, all_results):
        assert verify_t_cft_2(all_results)["passed"]

    def test_t_cft_3(self, all_results):
        assert verify_t_cft_3(all_results)["passed"]

    def test_t_cft_4(self, all_results):
        assert verify_t_cft_4(all_results)["passed"]

    def test_t_cft_5(self, all_results):
        assert verify_t_cft_5(all_results)["passed"]

    def test_t_cft_6(self, all_results):
        assert verify_t_cft_6(all_results)["passed"]

    def test_all_theorems_pass(self):
        for t in verify_all_theorems():
            assert t["passed"], f"{t['name']} failed: {t}"


class TestRegimeClassification:
    @pytest.mark.parametrize("entity", CFT_ENTITIES, ids=lambda e: e.name)
    def test_regime_is_valid(self, entity):
        r = compute_cft_kernel(entity)
        assert r.regime in ("Stable", "Watch", "Collapse")

    def test_maximal_coherence_not_collapse(self, all_results):
        mc = next(r for r in all_results if r.name == "maximal_coherence")
        assert mc.regime != "Collapse"

    def test_dissolution_is_collapse(self, all_results):
        df = next(r for r in all_results if r.name == "dissolution_field")
        assert df.regime == "Collapse"


class TestKernelResults:
    def test_to_dict(self, all_results):
        for r in all_results:
            d = r.to_dict()
            assert "F" in d and "omega" in d and "IC" in d
            assert d["name"] == r.name

    def test_compute_all_entities_count(self, all_results):
        assert len(all_results) == 12
