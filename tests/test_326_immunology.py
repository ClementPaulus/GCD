"""Tests for immunology domain closures.

Validates 52 entities across 4 sub-closures (immune cells, cytokines,
vaccines, autoimmune diseases), Tier-1 kernel identities, and
24 theorems (T-IC-1–6, T-CY-1–6, T-VR-1–6, T-AI-1–6).
"""

from __future__ import annotations

import math

import numpy as np
import pytest

# ── Autoimmune Kernel ──────────────────────────────────────────────────────
from closures.immunology.autoimmune_kernel import (
    AI_ENTITIES,
    N_AI_CHANNELS,
    AIKernelResult,
    compute_ai_kernel,
    verify_t_ai_1,
    verify_t_ai_2,
    verify_t_ai_3,
    verify_t_ai_4,
    verify_t_ai_5,
    verify_t_ai_6,
)
from closures.immunology.autoimmune_kernel import (
    compute_all_entities as compute_all_ai,
)
from closures.immunology.autoimmune_kernel import (
    verify_all_theorems as verify_all_ai,
)

# ── Cytokine Network ───────────────────────────────────────────────────────
from closures.immunology.cytokine_network import (
    CY_ENTITIES,
    N_CY_CHANNELS,
    CYKernelResult,
    compute_cy_kernel,
    verify_t_cy_1,
    verify_t_cy_2,
    verify_t_cy_3,
    verify_t_cy_4,
    verify_t_cy_5,
    verify_t_cy_6,
)
from closures.immunology.cytokine_network import (
    compute_all_entities as compute_all_cy,
)
from closures.immunology.cytokine_network import (
    verify_all_theorems as verify_all_cy,
)

# ── Immune Cell Kernel ──────────────────────────────────────────────────────
from closures.immunology.immune_cell_kernel import (
    IC_ENTITIES,
    N_IC_CHANNELS,
    ICKernelResult,
    compute_ic_kernel,
    verify_t_ic_1,
    verify_t_ic_2,
    verify_t_ic_3,
    verify_t_ic_4,
    verify_t_ic_5,
    verify_t_ic_6,
)
from closures.immunology.immune_cell_kernel import (
    compute_all_entities as compute_all_ic,
)
from closures.immunology.immune_cell_kernel import (
    verify_all_theorems as verify_all_ic,
)

# ── Vaccine Response ───────────────────────────────────────────────────────
from closures.immunology.vaccine_response import (
    N_VR_CHANNELS,
    VR_ENTITIES,
    VRKernelResult,
    compute_vr_kernel,
    verify_t_vr_1,
    verify_t_vr_2,
    verify_t_vr_3,
    verify_t_vr_4,
    verify_t_vr_5,
    verify_t_vr_6,
)
from closures.immunology.vaccine_response import (
    compute_all_entities as compute_all_vr,
)
from closures.immunology.vaccine_response import (
    verify_all_theorems as verify_all_vr,
)

# ── Module-scoped fixtures ─────────────────────────────────────────────────


@pytest.fixture(scope="module")
def ic_results() -> list[ICKernelResult]:
    return compute_all_ic()


@pytest.fixture(scope="module")
def cy_results() -> list[CYKernelResult]:
    return compute_all_cy()


@pytest.fixture(scope="module")
def vr_results() -> list[VRKernelResult]:
    return compute_all_vr()


@pytest.fixture(scope="module")
def ai_results() -> list[AIKernelResult]:
    return compute_all_ai()


# ═══════════════════════════════════════════════════════════════════════════
#  IMMUNE CELL KERNEL — 16 entities, 6 theorems
# ═══════════════════════════════════════════════════════════════════════════


class TestImmuneCellCatalog:
    def test_entity_count(self):
        assert len(IC_ENTITIES) == 16

    def test_channel_count(self):
        assert N_IC_CHANNELS == 8

    def test_all_arms_present(self):
        arms = {e.arm for e in IC_ENTITIES}
        assert arms == {"innate", "adaptive"}

    def test_unique_names(self):
        names = [e.name for e in IC_ENTITIES]
        assert len(names) == len(set(names))

    @pytest.mark.parametrize("entity", IC_ENTITIES, ids=lambda e: e.name)
    def test_trace_vector_shape(self, entity):
        assert entity.trace_vector().shape == (8,)

    @pytest.mark.parametrize("entity", IC_ENTITIES, ids=lambda e: e.name)
    def test_trace_vector_bounds(self, entity):
        c = entity.trace_vector()
        assert np.all(c >= 0.0) and np.all(c <= 1.0)


class TestImmuneCellTier1:
    @pytest.mark.parametrize("entity", IC_ENTITIES, ids=lambda e: e.name)
    def test_duality_identity(self, entity):
        r = compute_ic_kernel(entity)
        assert abs(r.F + r.omega - 1.0) < 1e-12

    @pytest.mark.parametrize("entity", IC_ENTITIES, ids=lambda e: e.name)
    def test_integrity_bound(self, entity):
        r = compute_ic_kernel(entity)
        assert r.IC <= r.F + 1e-12

    @pytest.mark.parametrize("entity", IC_ENTITIES, ids=lambda e: e.name)
    def test_log_integrity_relation(self, entity):
        r = compute_ic_kernel(entity)
        assert abs(r.IC - math.exp(r.kappa)) < 1e-10


class TestImmuneCellTheorems:
    def test_t_ic_1(self, ic_results):
        assert verify_t_ic_1(ic_results)["passed"]

    def test_t_ic_2(self, ic_results):
        assert verify_t_ic_2(ic_results)["passed"]

    def test_t_ic_3(self, ic_results):
        assert verify_t_ic_3(ic_results)["passed"]

    def test_t_ic_4(self, ic_results):
        assert verify_t_ic_4(ic_results)["passed"]

    def test_t_ic_5(self, ic_results):
        assert verify_t_ic_5(ic_results)["passed"]

    def test_t_ic_6(self, ic_results):
        assert verify_t_ic_6(ic_results)["passed"]

    def test_all_ic_theorems_pass(self):
        for t in verify_all_ic():
            assert t["passed"], f"{t['name']} failed: {t}"


class TestImmuneCellRegime:
    @pytest.mark.parametrize("entity", IC_ENTITIES, ids=lambda e: e.name)
    def test_regime_is_valid(self, entity):
        r = compute_ic_kernel(entity)
        assert r.regime in ("Stable", "Watch", "Collapse")

    def test_regime_omega_consistency(self, ic_results):
        for r in ic_results:
            if r.omega >= 0.30:
                assert r.regime == "Collapse", f"{r.name}: ω={r.omega} but regime={r.regime}"


class TestImmuneCellSerialization:
    def test_to_dict_keys(self, ic_results):
        d = ic_results[0].to_dict()
        expected = {"name", "arm", "F", "omega", "S", "C", "kappa", "IC", "regime"}
        assert set(d.keys()) == expected


# ═══════════════════════════════════════════════════════════════════════════
#  CYTOKINE NETWORK — 12 entities, 6 theorems
# ═══════════════════════════════════════════════════════════════════════════


class TestCytokineCatalog:
    def test_entity_count(self):
        assert len(CY_ENTITIES) == 12

    def test_channel_count(self):
        assert N_CY_CHANNELS == 8

    def test_all_classes_present(self):
        classes = {e.functional_class for e in CY_ENTITIES}
        assert classes == {"pro_inflammatory", "th_polarizing", "regulatory"}

    def test_unique_names(self):
        names = [e.name for e in CY_ENTITIES]
        assert len(names) == len(set(names))

    @pytest.mark.parametrize("entity", CY_ENTITIES, ids=lambda e: e.name)
    def test_trace_vector_shape(self, entity):
        assert entity.trace_vector().shape == (8,)

    @pytest.mark.parametrize("entity", CY_ENTITIES, ids=lambda e: e.name)
    def test_trace_vector_bounds(self, entity):
        c = entity.trace_vector()
        assert np.all(c >= 0.0) and np.all(c <= 1.0)


class TestCytokineTier1:
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


class TestCytokineTheorems:
    def test_t_cy_1(self, cy_results):
        assert verify_t_cy_1(cy_results)["passed"]

    def test_t_cy_2(self, cy_results):
        assert verify_t_cy_2(cy_results)["passed"]

    def test_t_cy_3(self, cy_results):
        assert verify_t_cy_3(cy_results)["passed"]

    def test_t_cy_4(self, cy_results):
        assert verify_t_cy_4(cy_results)["passed"]

    def test_t_cy_5(self, cy_results):
        assert verify_t_cy_5(cy_results)["passed"]

    def test_t_cy_6(self, cy_results):
        assert verify_t_cy_6(cy_results)["passed"]

    def test_all_cy_theorems_pass(self):
        for t in verify_all_cy():
            assert t["passed"], f"{t['name']} failed: {t}"


class TestCytokineRegime:
    @pytest.mark.parametrize("entity", CY_ENTITIES, ids=lambda e: e.name)
    def test_regime_is_valid(self, entity):
        r = compute_cy_kernel(entity)
        assert r.regime in ("Stable", "Watch", "Collapse")


class TestCytokineSerialization:
    def test_to_dict_keys(self, cy_results):
        d = cy_results[0].to_dict()
        expected = {"name", "functional_class", "F", "omega", "S", "C", "kappa", "IC", "regime"}
        assert set(d.keys()) == expected


# ═══════════════════════════════════════════════════════════════════════════
#  VACCINE RESPONSE — 12 entities, 6 theorems
# ═══════════════════════════════════════════════════════════════════════════


class TestVaccineCatalog:
    def test_entity_count(self):
        assert len(VR_ENTITIES) == 12

    def test_channel_count(self):
        assert N_VR_CHANNELS == 8

    def test_unique_names(self):
        names = [e.name for e in VR_ENTITIES]
        assert len(names) == len(set(names))

    @pytest.mark.parametrize("entity", VR_ENTITIES, ids=lambda e: e.name)
    def test_trace_vector_shape(self, entity):
        assert entity.trace_vector().shape == (8,)

    @pytest.mark.parametrize("entity", VR_ENTITIES, ids=lambda e: e.name)
    def test_trace_vector_bounds(self, entity):
        c = entity.trace_vector()
        assert np.all(c >= 0.0) and np.all(c <= 1.0)


class TestVaccineTier1:
    @pytest.mark.parametrize("entity", VR_ENTITIES, ids=lambda e: e.name)
    def test_duality_identity(self, entity):
        r = compute_vr_kernel(entity)
        assert abs(r.F + r.omega - 1.0) < 1e-12

    @pytest.mark.parametrize("entity", VR_ENTITIES, ids=lambda e: e.name)
    def test_integrity_bound(self, entity):
        r = compute_vr_kernel(entity)
        assert r.IC <= r.F + 1e-12

    @pytest.mark.parametrize("entity", VR_ENTITIES, ids=lambda e: e.name)
    def test_log_integrity_relation(self, entity):
        r = compute_vr_kernel(entity)
        assert abs(r.IC - math.exp(r.kappa)) < 1e-10


class TestVaccineTheorems:
    def test_t_vr_1(self, vr_results):
        assert verify_t_vr_1(vr_results)["passed"]

    def test_t_vr_2(self, vr_results):
        assert verify_t_vr_2(vr_results)["passed"]

    def test_t_vr_3(self, vr_results):
        assert verify_t_vr_3(vr_results)["passed"]

    def test_t_vr_4(self, vr_results):
        assert verify_t_vr_4(vr_results)["passed"]

    def test_t_vr_5(self, vr_results):
        assert verify_t_vr_5(vr_results)["passed"]

    def test_t_vr_6(self, vr_results):
        assert verify_t_vr_6(vr_results)["passed"]

    def test_all_vr_theorems_pass(self):
        for t in verify_all_vr():
            assert t["passed"], f"{t['name']} failed: {t}"


class TestVaccineRegime:
    @pytest.mark.parametrize("entity", VR_ENTITIES, ids=lambda e: e.name)
    def test_regime_is_valid(self, entity):
        r = compute_vr_kernel(entity)
        assert r.regime in ("Stable", "Watch", "Collapse")


class TestVaccineSerialization:
    def test_to_dict_keys(self, vr_results):
        d = vr_results[0].to_dict()
        expected = {"name", "platform", "F", "omega", "S", "C", "kappa", "IC", "regime"}
        assert set(d.keys()) == expected


# ═══════════════════════════════════════════════════════════════════════════
#  AUTOIMMUNE KERNEL — 12 entities, 6 theorems
# ═══════════════════════════════════════════════════════════════════════════


class TestAutoimmuneCatalog:
    def test_entity_count(self):
        assert len(AI_ENTITIES) == 12

    def test_channel_count(self):
        assert N_AI_CHANNELS == 8

    def test_all_categories_present(self):
        cats = {e.category for e in AI_ENTITIES}
        assert cats == {"organ_specific", "systemic", "overlap"}

    def test_unique_names(self):
        names = [e.name for e in AI_ENTITIES]
        assert len(names) == len(set(names))

    @pytest.mark.parametrize("entity", AI_ENTITIES, ids=lambda e: e.name)
    def test_trace_vector_shape(self, entity):
        assert entity.trace_vector().shape == (8,)

    @pytest.mark.parametrize("entity", AI_ENTITIES, ids=lambda e: e.name)
    def test_trace_vector_bounds(self, entity):
        c = entity.trace_vector()
        assert np.all(c >= 0.0) and np.all(c <= 1.0)


class TestAutoimmuneTier1:
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


class TestAutoimmuneTheorems:
    def test_t_ai_1(self, ai_results):
        assert verify_t_ai_1(ai_results)["passed"]

    def test_t_ai_2(self, ai_results):
        assert verify_t_ai_2(ai_results)["passed"]

    def test_t_ai_3(self, ai_results):
        assert verify_t_ai_3(ai_results)["passed"]

    def test_t_ai_4(self, ai_results):
        assert verify_t_ai_4(ai_results)["passed"]

    def test_t_ai_5(self, ai_results):
        assert verify_t_ai_5(ai_results)["passed"]

    def test_t_ai_6(self, ai_results):
        assert verify_t_ai_6(ai_results)["passed"]

    def test_all_ai_theorems_pass(self):
        for t in verify_all_ai():
            assert t["passed"], f"{t['name']} failed: {t}"


class TestAutoimmuneRegime:
    @pytest.mark.parametrize("entity", AI_ENTITIES, ids=lambda e: e.name)
    def test_regime_is_valid(self, entity):
        r = compute_ai_kernel(entity)
        assert r.regime in ("Stable", "Watch", "Collapse")


class TestAutoimmuneSerialization:
    def test_to_dict_keys(self, ai_results):
        d = ai_results[0].to_dict()
        expected = {"name", "category", "F", "omega", "S", "C", "kappa", "IC", "regime"}
        assert set(d.keys()) == expected


# ═══════════════════════════════════════════════════════════════════════════
#  CROSS-CLOSURE INTEGRATION
# ═══════════════════════════════════════════════════════════════════════════


class TestCrossClosureIntegration:
    """Integration tests across all 4 immunology sub-closures."""

    def test_total_entity_count(self):
        total = len(IC_ENTITIES) + len(CY_ENTITIES) + len(VR_ENTITIES) + len(AI_ENTITIES)
        assert total == 52

    def test_total_theorem_count(self):
        all_thms = verify_all_ic() + verify_all_cy() + verify_all_vr() + verify_all_ai()
        assert len(all_thms) == 24

    def test_all_24_theorems_proven(self):
        all_thms = verify_all_ic() + verify_all_cy() + verify_all_vr() + verify_all_ai()
        for t in all_thms:
            assert t["passed"], f"{t['name']} FAILED: {t}"

    def test_all_entities_satisfy_duality(self):
        """F + ω = 1 for all 52 entities across all sub-closures."""
        for r in compute_all_ic() + compute_all_cy() + compute_all_vr() + compute_all_ai():
            assert abs(r.F + r.omega - 1.0) < 1e-12, f"{r.name}: duality fails"

    def test_all_entities_satisfy_integrity_bound(self):
        """IC ≤ F for all 52 entities."""
        for r in compute_all_ic() + compute_all_cy() + compute_all_vr() + compute_all_ai():
            assert r.IC <= r.F + 1e-12, f"{r.name}: IC > F"

    def test_all_entities_satisfy_log_integrity(self):
        """IC = exp(κ) for all 52 entities."""
        for r in compute_all_ic() + compute_all_cy() + compute_all_vr() + compute_all_ai():
            assert abs(r.IC - math.exp(r.kappa)) < 1e-10, f"{r.name}: IC ≠ exp(κ)"

    def test_immune_cell_innate_adaptive_balance(self, ic_results):
        """Innate and adaptive arms each have 8 entities."""
        innate = [r for r in ic_results if r.arm == "innate"]
        adaptive = [r for r in ic_results if r.arm == "adaptive"]
        assert len(innate) == 8
        assert len(adaptive) == 8

    def test_package_init_imports(self):
        """The immunology __init__.py can import all sub-closures."""
        from closures.immunology import (
            AI_ENTITIES,
            CY_ENTITIES,
            IC_ENTITIES,
            VR_ENTITIES,
        )

        assert len(IC_ENTITIES) == 16
        assert len(CY_ENTITIES) == 12
        assert len(VR_ENTITIES) == 12
        assert len(AI_ENTITIES) == 12
