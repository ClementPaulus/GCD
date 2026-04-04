"""Tests for Fermion Quantum Criticality closure.

Validates the 6 theorems from the GCD kernel analysis of
Mittal, Zander, Lang, and Diehl (2026), "Fermion quantum criticality
far from equilibrium," Phys. Rev. X 16, 011069.  arXiv: 2507.14318.

Test coverage:
  - Entity catalog integrity (12 entities, 4 categories, frozen dataclass)
  - 8-channel trace construction (bounds, weights, dtype)
  - Tier-1 kernel identities for all entities (duality, integrity bound,
    log-integrity relation, entropy non-negativity, gap non-negativity)
  - All 6 theorems (T-FQC-1 through T-FQC-6)
  - Regime classification consistency
  - Channel autopsy (geometric slaughter detection)
  - Serialization round-trip (to_dict)
"""

from __future__ import annotations

import math

import numpy as np
import pytest

from closures.quantum_mechanics.fermion_criticality import (
    FQC_CHANNELS,
    FQC_ENTITIES,
    FQC_WEIGHTS,
    N_FQC_CHANNELS,
    FermionCriticalityEntity,
    FQCKernelResult,
    compute_all_entities,
    compute_fqc_kernel,
    verify_all_theorems,
    verify_t_fqc_1,
    verify_t_fqc_2,
    verify_t_fqc_3,
    verify_t_fqc_4,
    verify_t_fqc_5,
    verify_t_fqc_6,
)

EPSILON = 1e-8


# ═══════════════════════════════════════════════════════════════════════════
# Fixtures
# ═══════════════════════════════════════════════════════════════════════════


@pytest.fixture(scope="module")
def all_results() -> list[FQCKernelResult]:
    """Compute kernel invariants for all 12 entities."""
    return compute_all_entities()


@pytest.fixture(scope="module")
def results_by_name(all_results: list[FQCKernelResult]) -> dict[str, FQCKernelResult]:
    """Index results by entity name."""
    return {r.name: r for r in all_results}


@pytest.fixture(scope="module")
def dark_results(all_results: list[FQCKernelResult]) -> list[FQCKernelResult]:
    """Dark-state category results."""
    return [r for r in all_results if r.category == "dark_state"]


@pytest.fixture(scope="module")
def broken_results(all_results: list[FQCKernelResult]) -> list[FQCKernelResult]:
    """Symmetry-broken category results."""
    return [r for r in all_results if r.category == "symmetry_broken"]


# ═══════════════════════════════════════════════════════════════════════════
# SECTION 1: ENTITY CATALOG INTEGRITY
# ═══════════════════════════════════════════════════════════════════════════


class TestEntityCatalog:
    """Verify the fermion criticality entity catalog structure."""

    def test_entity_count(self) -> None:
        assert len(FQC_ENTITIES) == 12

    def test_unique_names(self) -> None:
        names = [e.name for e in FQC_ENTITIES]
        assert len(names) == len(set(names))

    def test_all_categories_present(self) -> None:
        categories = {e.category for e in FQC_ENTITIES}
        assert categories == {"dark_state", "critical", "symmetry_broken", "comparison"}

    def test_category_counts(self) -> None:
        cats = {}
        for e in FQC_ENTITIES:
            cats[e.category] = cats.get(e.category, 0) + 1
        assert cats == {
            "dark_state": 3,
            "critical": 3,
            "symmetry_broken": 3,
            "comparison": 3,
        }

    @pytest.mark.parametrize("entity", FQC_ENTITIES, ids=lambda e: e.name)
    def test_entity_has_description(self, entity: FermionCriticalityEntity) -> None:
        assert len(entity.description) > 20

    @pytest.mark.parametrize("entity", FQC_ENTITIES, ids=lambda e: e.name)
    def test_entity_is_frozen(self, entity: FermionCriticalityEntity) -> None:
        with pytest.raises(AttributeError):
            entity.name = "mutated"  # type: ignore[misc]


# ═══════════════════════════════════════════════════════════════════════════
# SECTION 2: TRACE VECTOR CONSTRUCTION
# ═══════════════════════════════════════════════════════════════════════════


class TestTraceVector:
    """Verify trace vector construction and bounds."""

    def test_channel_count(self) -> None:
        assert N_FQC_CHANNELS == 8
        assert len(FQC_CHANNELS) == 8

    def test_weights_uniform(self) -> None:
        assert len(FQC_WEIGHTS) == N_FQC_CHANNELS
        np.testing.assert_allclose(FQC_WEIGHTS.sum(), 1.0, atol=1e-15)
        np.testing.assert_allclose(FQC_WEIGHTS, 1.0 / N_FQC_CHANNELS)

    @pytest.mark.parametrize("entity", FQC_ENTITIES, ids=lambda e: e.name)
    def test_trace_vector_length(self, entity: FermionCriticalityEntity) -> None:
        c = entity.trace_vector()
        assert len(c) == N_FQC_CHANNELS

    @pytest.mark.parametrize("entity", FQC_ENTITIES, ids=lambda e: e.name)
    def test_trace_vector_bounds(self, entity: FermionCriticalityEntity) -> None:
        c = entity.trace_vector()
        assert np.all(c >= 0.0), f"{entity.name}: channel negative"
        assert np.all(c <= 1.0), f"{entity.name}: channel above 1.0"

    @pytest.mark.parametrize("entity", FQC_ENTITIES, ids=lambda e: e.name)
    def test_trace_vector_dtype(self, entity: FermionCriticalityEntity) -> None:
        c = entity.trace_vector()
        assert c.dtype == np.float64


# ═══════════════════════════════════════════════════════════════════════════
# SECTION 3: TIER-1 KERNEL IDENTITIES
# ═══════════════════════════════════════════════════════════════════════════


class TestTier1Identities:
    """Verify Tier-1 identities hold for every entity."""

    @pytest.mark.parametrize("entity", FQC_ENTITIES, ids=lambda e: e.name)
    def test_duality_identity(self, entity: FermionCriticalityEntity) -> None:
        """F + omega = 1 — exact to machine precision."""
        r = compute_fqc_kernel(entity)
        assert abs(r.F + r.omega - 1.0) < 1e-12, f"{entity.name}: F+ω={r.F + r.omega}"

    @pytest.mark.parametrize("entity", FQC_ENTITIES, ids=lambda e: e.name)
    def test_integrity_bound(self, entity: FermionCriticalityEntity) -> None:
        """IC <= F — the integrity bound."""
        r = compute_fqc_kernel(entity)
        assert r.IC <= r.F + 1e-12, f"{entity.name}: IC={r.IC:.6f} > F={r.F:.6f}"

    @pytest.mark.parametrize("entity", FQC_ENTITIES, ids=lambda e: e.name)
    def test_log_integrity_relation(self, entity: FermionCriticalityEntity) -> None:
        """IC = exp(kappa) — log-integrity relation."""
        r = compute_fqc_kernel(entity)
        assert abs(r.IC - math.exp(r.kappa)) < 1e-10, f"{entity.name}: IC={r.IC:.6e}, exp(κ)={math.exp(r.kappa):.6e}"

    @pytest.mark.parametrize("entity", FQC_ENTITIES, ids=lambda e: e.name)
    def test_positive_entropy(self, entity: FermionCriticalityEntity) -> None:
        """Bernoulli field entropy S >= 0."""
        r = compute_fqc_kernel(entity)
        assert r.S >= -1e-15, f"{entity.name}: S={r.S}"

    @pytest.mark.parametrize("entity", FQC_ENTITIES, ids=lambda e: e.name)
    def test_heterogeneity_gap_non_negative(self, entity: FermionCriticalityEntity) -> None:
        """Delta = F - IC >= 0 (consequence of IC <= F)."""
        r = compute_fqc_kernel(entity)
        gap = r.F - r.IC
        assert gap >= -1e-12, f"{entity.name}: Δ={gap}"


# ═══════════════════════════════════════════════════════════════════════════
# SECTION 4: THEOREM VERIFICATION
# ═══════════════════════════════════════════════════════════════════════════


class TestTheorems:
    """Verify all 6 fermion criticality theorems."""

    def test_t_fqc_1_dark_state_fidelity(self, all_results: list[FQCKernelResult]) -> None:
        """T-FQC-1: Dark states have highest mean F across categories."""
        result = verify_t_fqc_1(all_results)
        assert result["passed"], f"dark F={result['dark_state_mean_F']:.4f}"

    def test_t_fqc_2_geometric_slaughter(self, all_results: list[FQCKernelResult]) -> None:
        """T-FQC-2: Broken-symmetry entities show IC/F collapse < 0.35."""
        result = verify_t_fqc_2(all_results)
        assert result["passed"], (
            f"broken IC/F={result['broken_mean_IC_F']:.4f}, dark IC/F={result['dark_state_mean_IC_F']:.4f}"
        )

    def test_t_fqc_3_purity_ic_correspondence(self, all_results: list[FQCKernelResult]) -> None:
        """T-FQC-3: Purity tracks IC (Spearman rho > 0.85)."""
        result = verify_t_fqc_3(all_results)
        assert result["passed"], f"Spearman rho={result['spearman_rho']:.4f}"

    def test_t_fqc_4_regime_separation(self, all_results: list[FQCKernelResult]) -> None:
        """T-FQC-4: Dark states NOT Collapse; symmetry-broken ARE Collapse."""
        result = verify_t_fqc_4(all_results)
        assert result["passed"], (
            f"dark_not_collapse={result['dark_not_collapse']}, broken_all_collapse={result['broken_all_collapse']}"
        )
        assert result["omega_separation"] > 0.20

    def test_t_fqc_5_bosonic_slaughter(self, all_results: list[FQCKernelResult]) -> None:
        """T-FQC-5: Bosonic KPZ entity has IC/F < 0.40 from dead antiunitary."""
        result = verify_t_fqc_5(all_results)
        assert result["passed"], f"bosonic IC/F={result['bosonic_IC_F']:.4f}"

    def test_t_fqc_6_fdss_completeness(self, all_results: list[FQCKernelResult]) -> None:
        """T-FQC-6: Complete FDSS has higher mean IC than broken FDSS."""
        result = verify_t_fqc_6(all_results)
        assert result["passed"], (
            f"complete IC={result['complete_fdss_mean_IC']:.4f}, broken IC={result['broken_fdss_mean_IC']:.4f}"
        )
        assert result["IC_ratio"] > 5.0  # at least 5x difference

    def test_all_theorems_pass(self, all_results: list[FQCKernelResult]) -> None:
        """Verify all theorems pass via the aggregate function."""
        results = verify_all_theorems()
        for t in results:
            assert t["passed"], f"{t['name']} FAILED: {t}"


# ═══════════════════════════════════════════════════════════════════════════
# SECTION 5: REGIME CLASSIFICATION
# ═══════════════════════════════════════════════════════════════════════════


class TestRegimeClassification:
    """Verify regime classification consistency."""

    def test_valid_regimes(self, all_results: list[FQCKernelResult]) -> None:
        for r in all_results:
            assert r.regime in {"Stable", "Watch", "Collapse"}, f"{r.name}: invalid regime '{r.regime}'"

    def test_collapse_has_high_omega(self, all_results: list[FQCKernelResult]) -> None:
        for r in all_results:
            if r.regime == "Collapse":
                assert r.omega >= 0.30, f"{r.name}: Collapse but ω={r.omega:.4f}"

    def test_equilibrium_is_watch(self, results_by_name: dict[str, FQCKernelResult]) -> None:
        """Equilibrium QCP has near-unit purity and Watch regime."""
        eq = results_by_name["Equilibrium_QCP"]
        assert eq.regime == "Watch"
        assert eq.F > 0.85


# ═══════════════════════════════════════════════════════════════════════════
# SECTION 6: CHANNEL AUTOPSY
# ═══════════════════════════════════════════════════════════════════════════


class TestChannelAutopsy:
    """Identify which channels drive geometric slaughter."""

    def test_broken_antiunitary_weakest_channel(self) -> None:
        """Broken_antiunitary entity: fdss_antiunitary is the dead channel."""
        entity = next(e for e in FQC_ENTITIES if e.name == "Broken_antiunitary")
        c = entity.trace_vector()
        weakest_idx = int(np.argmin(c))
        assert FQC_CHANNELS[weakest_idx] == "fdss_antiunitary"

    def test_broken_global_weakest_channel(self) -> None:
        """Broken_global entity: fdss_global is the dead channel."""
        entity = next(e for e in FQC_ENTITIES if e.name == "Broken_global")
        c = entity.trace_vector()
        weakest_idx = int(np.argmin(c))
        assert FQC_CHANNELS[weakest_idx] == "fdss_global"

    def test_fully_broken_two_dead_channels(self) -> None:
        """Fully_broken has both FDSS channels dead."""
        entity = next(e for e in FQC_ENTITIES if e.name == "Fully_broken_classical")
        c = entity.trace_vector()
        dead = np.where(c < 1e-4)[0]
        dead_names = {FQC_CHANNELS[i] for i in dead}
        assert "fdss_global" in dead_names
        assert "fdss_antiunitary" in dead_names

    def test_dark_state_no_dead_channels(self) -> None:
        """Deep dark states have no channels below 0.01."""
        for entity in FQC_ENTITIES:
            if entity.category == "dark_state":
                c = entity.trace_vector()
                assert np.all(c > 0.01), f"{entity.name}: channel below 0.01 at {np.argmin(c)}"


# ═══════════════════════════════════════════════════════════════════════════
# SECTION 7: SERIALIZATION
# ═══════════════════════════════════════════════════════════════════════════


class TestSerialization:
    """Verify to_dict round-trip."""

    @pytest.mark.parametrize("entity", FQC_ENTITIES, ids=lambda e: e.name)
    def test_to_dict_keys(self, entity: FermionCriticalityEntity) -> None:
        r = compute_fqc_kernel(entity)
        d = r.to_dict()
        assert set(d.keys()) == {"name", "category", "F", "omega", "S", "C", "kappa", "IC", "regime"}

    @pytest.mark.parametrize("entity", FQC_ENTITIES, ids=lambda e: e.name)
    def test_to_dict_values_match(self, entity: FermionCriticalityEntity) -> None:
        r = compute_fqc_kernel(entity)
        d = r.to_dict()
        assert d["F"] == r.F
        assert d["omega"] == r.omega
        assert d["regime"] == r.regime
