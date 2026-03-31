"""Tests for spliceosome dynamics closure (quantum mechanics domain).

Validates 12 spliceosome entities, 8-channel trace construction,
Tier-1 kernel identities, and 6 theorems (T-SD-1 through T-SD-6).

Sources:
    Martino et al. 2026, PNAS, DOI: 10.1073/pnas.2522293123
    CRG Barcelona 2024, Science, DOI: 10.1126/science.adn8105
"""

from __future__ import annotations

import math

import numpy as np
import pytest

from closures.quantum_mechanics.spliceosome_dynamics import (
    N_SD_CHANNELS,
    SD_CHANNELS,
    SD_ENTITIES,
    SDKernelResult,
    compute_all_entities,
    compute_sd_kernel,
    verify_all_theorems,
    verify_t_sd_1,
    verify_t_sd_2,
    verify_t_sd_3,
    verify_t_sd_4,
    verify_t_sd_5,
    verify_t_sd_6,
)


@pytest.fixture(scope="module")
def all_results() -> list[SDKernelResult]:
    return compute_all_entities()


class TestEntityCatalog:
    def test_entity_count(self):
        assert len(SD_ENTITIES) == 12

    def test_channel_count(self):
        assert N_SD_CHANNELS == 8
        assert len(SD_CHANNELS) == 8

    def test_all_categories_present(self):
        cats = {e.category for e in SD_ENTITIES}
        assert cats == {"catalytic_state", "rna_component", "splicing_factor", "md_simulation"}

    def test_three_per_category(self):
        for cat in ("catalytic_state", "rna_component", "splicing_factor", "md_simulation"):
            count = sum(1 for e in SD_ENTITIES if e.category == cat)
            assert count == 3, f"{cat} has {count} entities, expected 3"

    @pytest.mark.parametrize("entity", SD_ENTITIES, ids=lambda e: e.name)
    def test_trace_vector_shape(self, entity):
        assert entity.trace_vector().shape == (8,)

    @pytest.mark.parametrize("entity", SD_ENTITIES, ids=lambda e: e.name)
    def test_trace_vector_bounds(self, entity):
        c = entity.trace_vector()
        assert np.all(c >= 0.0) and np.all(c <= 1.0)


class TestTier1Identities:
    @pytest.mark.parametrize("entity", SD_ENTITIES, ids=lambda e: e.name)
    def test_duality_identity(self, entity):
        r = compute_sd_kernel(entity)
        assert abs(r.F + r.omega - 1.0) < 1e-12

    @pytest.mark.parametrize("entity", SD_ENTITIES, ids=lambda e: e.name)
    def test_integrity_bound(self, entity):
        r = compute_sd_kernel(entity)
        assert r.IC <= r.F + 1e-12

    @pytest.mark.parametrize("entity", SD_ENTITIES, ids=lambda e: e.name)
    def test_log_integrity_relation(self, entity):
        r = compute_sd_kernel(entity)
        assert abs(r.IC - math.exp(r.kappa)) < 1e-10


class TestTheorems:
    def test_t_sd_1(self, all_results):
        assert verify_t_sd_1(all_results)["passed"]

    def test_t_sd_2(self, all_results):
        assert verify_t_sd_2(all_results)["passed"]

    def test_t_sd_3(self, all_results):
        assert verify_t_sd_3(all_results)["passed"]

    def test_t_sd_4(self, all_results):
        assert verify_t_sd_4(all_results)["passed"]

    def test_t_sd_5(self, all_results):
        assert verify_t_sd_5(all_results)["passed"]

    def test_t_sd_6(self, all_results):
        assert verify_t_sd_6(all_results)["passed"]

    def test_all_theorems_pass(self):
        for t in verify_all_theorems():
            assert t["passed"], f"{t['name']} failed: {t}"


class TestRegimeClassification:
    @pytest.mark.parametrize("entity", SD_ENTITIES, ids=lambda e: e.name)
    def test_regime_is_valid(self, entity):
        r = compute_sd_kernel(entity)
        assert r.regime in ("Stable", "Watch", "Collapse")


class TestCollapseReturnStructure:
    """Validate the collapse-return mapping specific to this closure."""

    def test_cryoem_has_dead_channels(self):
        cryo = next(e for e in SD_ENTITIES if e.name == "cryoem_static_reference")
        assert cryo.transition_resolution < 0.10
        assert cryo.simulation_convergence < 0.10

    def test_franklin_has_live_channels(self):
        franklin = next(e for e in SD_ENTITIES if e.name == "franklin_allosteric_path")
        assert franklin.transition_resolution > 0.80
        assert franklin.simulation_convergence > 0.80

    def test_geometric_slaughter_visible(self, all_results):
        cryo = next(r for r in all_results if r.name == "cryoem_static_reference")
        gap = cryo.F - cryo.IC
        assert gap > 0.20, f"Expected large gap for cryo-EM, got {gap:.4f}"
