"""Tests for neuroimmune bridge closure (immunology domain).

Validates 12 neuroimmune interface states, 8-channel trace construction,
Tier-1 kernel identities, and 6 theorems (T-NI-1 through T-NI-6).
"""

from __future__ import annotations

import math

import numpy as np
import pytest

from closures.immunology.neuroimmune_bridge import (
    N_NI_CHANNELS,
    NI_CHANNELS,
    NI_ENTITIES,
    NIKernelResult,
    compute_all_entities,
    compute_ni_kernel,
    verify_all_theorems,
    verify_t_ni_1,
    verify_t_ni_2,
    verify_t_ni_3,
    verify_t_ni_4,
    verify_t_ni_5,
    verify_t_ni_6,
)


@pytest.fixture(scope="module")
def all_results() -> list[NIKernelResult]:
    return compute_all_entities()


# ── Entity Catalog ──


class TestEntityCatalog:
    def test_entity_count(self):
        assert len(NI_ENTITIES) == 12

    def test_channel_count(self):
        assert N_NI_CHANNELS == 8
        assert len(NI_CHANNELS) == 8

    def test_all_clinical_classes_present(self):
        classes = {e.clinical_class for e in NI_ENTITIES}
        assert classes == {"healthy", "acute", "chronic", "intermediate"}

    def test_unique_names(self):
        names = [e.name for e in NI_ENTITIES]
        assert len(names) == len(set(names))

    def test_class_distribution(self):
        from collections import Counter

        counts = Counter(e.clinical_class for e in NI_ENTITIES)
        assert counts["healthy"] == 3
        assert counts["acute"] == 3
        assert counts["chronic"] == 3
        assert counts["intermediate"] == 3

    @pytest.mark.parametrize("entity", NI_ENTITIES, ids=lambda e: e.name)
    def test_trace_vector_shape(self, entity):
        c = entity.trace_vector()
        assert c.shape == (8,)

    @pytest.mark.parametrize("entity", NI_ENTITIES, ids=lambda e: e.name)
    def test_trace_vector_bounds(self, entity):
        c = entity.trace_vector()
        assert np.all(c >= 0.0) and np.all(c <= 1.0)


# ── Tier-1 Kernel Identities ──


class TestTier1Identities:
    @pytest.mark.parametrize("entity", NI_ENTITIES, ids=lambda e: e.name)
    def test_duality_identity(self, entity):
        r = compute_ni_kernel(entity)
        assert abs(r.F + r.omega - 1.0) < 1e-12

    @pytest.mark.parametrize("entity", NI_ENTITIES, ids=lambda e: e.name)
    def test_integrity_bound(self, entity):
        r = compute_ni_kernel(entity)
        assert r.IC <= r.F + 1e-12

    @pytest.mark.parametrize("entity", NI_ENTITIES, ids=lambda e: e.name)
    def test_log_integrity_relation(self, entity):
        r = compute_ni_kernel(entity)
        assert abs(r.IC - math.exp(r.kappa)) < 1e-10


# ── Theorems ──


class TestTheorems:
    def test_t_ni_1(self, all_results):
        t = verify_t_ni_1(all_results)
        assert t["proven"], t

    def test_t_ni_2(self, all_results):
        t = verify_t_ni_2(all_results)
        assert t["proven"], t

    def test_t_ni_3(self, all_results):
        t = verify_t_ni_3(all_results)
        assert t["proven"], t

    def test_t_ni_4(self, all_results):
        t = verify_t_ni_4(all_results)
        assert t["proven"], t

    def test_t_ni_5(self, all_results):
        t = verify_t_ni_5(all_results)
        assert t["proven"], t

    def test_t_ni_6(self, all_results):
        t = verify_t_ni_6(all_results)
        assert t["proven"], t

    def test_all_theorems_pass(self):
        results_list = verify_all_theorems()
        for t in results_list:
            assert t["proven"], f"{t['theorem']} failed: {t}"


# ── Regime Classification ──


class TestRegimeClassification:
    def test_healthy_not_collapse(self, all_results):
        healthy = [r for r in all_results if r.clinical_class == "healthy"]
        for r in healthy:
            assert r.regime != "Collapse", f"{r.name} should not be Collapse"

    def test_acute_in_collapse(self, all_results):
        acute = [r for r in all_results if r.clinical_class == "acute"]
        for r in acute:
            assert r.regime == "Collapse", f"{r.name} should be Collapse"

    def test_regime_values_valid(self, all_results):
        for r in all_results:
            assert r.regime in ("Stable", "Watch", "Collapse")


# ── Kernel Result Structure ──


class TestKernelResultStructure:
    @pytest.mark.parametrize("entity", NI_ENTITIES, ids=lambda e: e.name)
    def test_result_fields(self, entity):
        r = compute_ni_kernel(entity)
        assert isinstance(r.name, str)
        assert isinstance(r.clinical_class, str)
        assert isinstance(r.F, float)
        assert isinstance(r.omega, float)
        assert isinstance(r.S, float)
        assert isinstance(r.C, float)
        assert isinstance(r.kappa, float)
        assert isinstance(r.IC, float)
        assert isinstance(r.regime, str)

    @pytest.mark.parametrize("entity", NI_ENTITIES, ids=lambda e: e.name)
    def test_to_dict(self, entity):
        r = compute_ni_kernel(entity)
        d = r.to_dict()
        assert "name" in d
        assert "F" in d
        assert "IC" in d
        assert d["name"] == entity.name

    @pytest.mark.parametrize("entity", NI_ENTITIES, ids=lambda e: e.name)
    def test_f_in_unit_interval(self, entity):
        r = compute_ni_kernel(entity)
        assert 0.0 <= r.F <= 1.0

    @pytest.mark.parametrize("entity", NI_ENTITIES, ids=lambda e: e.name)
    def test_omega_in_unit_interval(self, entity):
        r = compute_ni_kernel(entity)
        assert 0.0 <= r.omega <= 1.0

    @pytest.mark.parametrize("entity", NI_ENTITIES, ids=lambda e: e.name)
    def test_ic_positive(self, entity):
        r = compute_ni_kernel(entity)
        assert r.IC > 0.0

    @pytest.mark.parametrize("entity", NI_ENTITIES, ids=lambda e: e.name)
    def test_entropy_non_negative(self, entity):
        r = compute_ni_kernel(entity)
        assert r.S >= 0.0
