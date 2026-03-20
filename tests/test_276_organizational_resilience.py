"""Tests for organizational resilience closure (continuity-theory domain).

Validates 12 organizational resilience entities, 8-channel trace construction,
Tier-1 kernel identities, and 6 theorems (T-OR-1 through T-OR-6).
"""

from __future__ import annotations

import math

import numpy as np
import pytest

from closures.continuity_theory.organizational_resilience import (
    N_OR_CHANNELS,
    OR_CHANNELS,
    OR_ENTITIES,
    ORKernelResult,
    compute_all_entities,
    compute_or_kernel,
    verify_all_theorems,
    verify_t_or_1,
    verify_t_or_2,
    verify_t_or_3,
    verify_t_or_4,
    verify_t_or_5,
    verify_t_or_6,
)


@pytest.fixture(scope="module")
def all_results() -> list[ORKernelResult]:
    return compute_all_entities()


class TestEntityCatalog:
    def test_entity_count(self):
        assert len(OR_ENTITIES) == 12

    def test_channel_count(self):
        assert N_OR_CHANNELS == 8
        assert len(OR_CHANNELS) == 8

    def test_all_categories_present(self):
        cats = {e.category for e in OR_ENTITIES}
        assert cats == {"agile", "institutional", "distributed", "specialized"}

    @pytest.mark.parametrize("entity", OR_ENTITIES, ids=lambda e: e.name)
    def test_trace_vector_shape(self, entity):
        assert entity.trace_vector().shape == (8,)

    @pytest.mark.parametrize("entity", OR_ENTITIES, ids=lambda e: e.name)
    def test_trace_vector_bounds(self, entity):
        c = entity.trace_vector()
        assert np.all(c >= 0.0) and np.all(c <= 1.0)


class TestTier1Identities:
    @pytest.mark.parametrize("entity", OR_ENTITIES, ids=lambda e: e.name)
    def test_duality_identity(self, entity):
        r = compute_or_kernel(entity)
        assert abs(r.F + r.omega - 1.0) < 1e-12

    @pytest.mark.parametrize("entity", OR_ENTITIES, ids=lambda e: e.name)
    def test_integrity_bound(self, entity):
        r = compute_or_kernel(entity)
        assert r.IC <= r.F + 1e-12

    @pytest.mark.parametrize("entity", OR_ENTITIES, ids=lambda e: e.name)
    def test_log_integrity_relation(self, entity):
        r = compute_or_kernel(entity)
        assert abs(r.IC - math.exp(r.kappa)) < 1e-10


class TestTheorems:
    def test_t_or_1(self, all_results):
        assert verify_t_or_1(all_results)["passed"]

    def test_t_or_2(self, all_results):
        assert verify_t_or_2(all_results)["passed"]

    def test_t_or_3(self, all_results):
        assert verify_t_or_3(all_results)["passed"]

    def test_t_or_4(self, all_results):
        assert verify_t_or_4(all_results)["passed"]

    def test_t_or_5(self, all_results):
        assert verify_t_or_5(all_results)["passed"]

    def test_t_or_6(self, all_results):
        assert verify_t_or_6(all_results)["passed"]

    def test_all_theorems_pass(self):
        for t in verify_all_theorems():
            assert t["passed"], f"{t['name']} failed: {t}"


class TestRegimeClassification:
    @pytest.mark.parametrize("entity", OR_ENTITIES, ids=lambda e: e.name)
    def test_regime_is_valid(self, entity):
        r = compute_or_kernel(entity)
        assert r.regime in ("Stable", "Watch", "Collapse")
