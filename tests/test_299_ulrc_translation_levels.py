"""Tests for ULRC translation levels closure (dynamic-semiotics domain).

Validates 12 translation-level entities (6 linguistic + 6 mathematical),
8-channel trace construction, Tier-1 kernel identities, 6 theorems
(T-TL-1 through T-TL-6), and cross-level structural analysis.

The ULRC establishes that the kernel IS a grammar (Kernel-Grammar
Isomorphism). Translation levels are the strata at which meaning
transforms — both in natural language and in formal mathematics. This
test suite verifies that the Rosetta invariance property holds: same
kernel, different domains, comparable verdicts.
"""

from __future__ import annotations

import math

import numpy as np
import pytest

from closures.dynamic_semiotics.translation_levels import (
    N_TL_CHANNELS,
    TL_CHANNELS,
    TL_ENTITIES,
    TLKernelResult,
    analyze_translation_structure,
    compute_all_entities,
    compute_tl_kernel,
    verify_all_theorems,
    verify_t_tl_1,
    verify_t_tl_2,
    verify_t_tl_3,
    verify_t_tl_4,
    verify_t_tl_5,
    verify_t_tl_6,
)


@pytest.fixture(scope="module")
def all_results() -> list[TLKernelResult]:
    return compute_all_entities()


# ── Entity Catalog ────────────────────────────────────────────────────


class TestEntityCatalog:
    def test_entity_count(self):
        assert len(TL_ENTITIES) == 12

    def test_channel_count(self):
        assert N_TL_CHANNELS == 8
        assert len(TL_CHANNELS) == 8

    def test_both_domains_present(self):
        domains = {e.domain for e in TL_ENTITIES}
        assert domains == {"linguistic", "mathematical"}

    def test_six_linguistic(self):
        ling = [e for e in TL_ENTITIES if e.domain == "linguistic"]
        assert len(ling) == 6

    def test_six_mathematical(self):
        math_ents = [e for e in TL_ENTITIES if e.domain == "mathematical"]
        assert len(math_ents) == 6

    def test_unique_names(self):
        names = [e.name for e in TL_ENTITIES]
        assert len(names) == len(set(names))

    def test_linguistic_names(self):
        ling = {e.name for e in TL_ENTITIES if e.domain == "linguistic"}
        expected = {
            "phonological",
            "morphological",
            "syntactic",
            "semantic",
            "pragmatic",
            "discourse",
        }
        assert ling == expected

    def test_mathematical_names(self):
        math_names = {e.name for e in TL_ENTITIES if e.domain == "mathematical"}
        expected = {
            "symbolic",
            "algebraic",
            "topological",
            "measure_theoretic",
            "categorical",
            "type_theoretic",
        }
        assert math_names == expected

    @pytest.mark.parametrize("entity", TL_ENTITIES, ids=lambda e: e.name)
    def test_trace_vector_shape(self, entity):
        assert entity.trace_vector().shape == (8,)

    @pytest.mark.parametrize("entity", TL_ENTITIES, ids=lambda e: e.name)
    def test_trace_vector_bounds(self, entity):
        c = entity.trace_vector()
        assert np.all(c >= 0.0) and np.all(c <= 1.0)

    @pytest.mark.parametrize("entity", TL_ENTITIES, ids=lambda e: e.name)
    def test_no_zero_channels(self, entity):
        """All channels should be > 0 (no dead channels by construction)."""
        c = entity.trace_vector()
        assert np.all(c > 0.0)


# ── Tier-1 Identities ────────────────────────────────────────────────


class TestTier1Identities:
    @pytest.mark.parametrize("entity", TL_ENTITIES, ids=lambda e: e.name)
    def test_duality_identity(self, entity):
        """F + ω = 1 — duality identity (complementum perfectum)."""
        r = compute_tl_kernel(entity)
        assert abs(r.F + r.omega - 1.0) < 1e-12

    @pytest.mark.parametrize("entity", TL_ENTITIES, ids=lambda e: e.name)
    def test_integrity_bound(self, entity):
        """IC ≤ F — integrity bound (limbus integritatis)."""
        r = compute_tl_kernel(entity)
        assert r.IC <= r.F + 1e-12

    @pytest.mark.parametrize("entity", TL_ENTITIES, ids=lambda e: e.name)
    def test_log_integrity_relation(self, entity):
        """IC = exp(κ) — log-integrity relation."""
        r = compute_tl_kernel(entity)
        assert abs(r.IC - math.exp(r.kappa)) < 1e-10

    @pytest.mark.parametrize("entity", TL_ENTITIES, ids=lambda e: e.name)
    def test_F_in_unit_interval(self, entity):
        r = compute_tl_kernel(entity)
        assert 0.0 <= r.F <= 1.0

    @pytest.mark.parametrize("entity", TL_ENTITIES, ids=lambda e: e.name)
    def test_omega_in_unit_interval(self, entity):
        r = compute_tl_kernel(entity)
        assert 0.0 <= r.omega <= 1.0

    @pytest.mark.parametrize("entity", TL_ENTITIES, ids=lambda e: e.name)
    def test_entropy_non_negative(self, entity):
        r = compute_tl_kernel(entity)
        assert r.S >= -1e-12

    @pytest.mark.parametrize("entity", TL_ENTITIES, ids=lambda e: e.name)
    def test_IC_positive(self, entity):
        r = compute_tl_kernel(entity)
        assert r.IC > 0.0


# ── Theorems ──────────────────────────────────────────────────────────


class TestTheorems:
    def test_t_tl_1(self, all_results):
        """T-TL-1: Syntactic has highest structural fidelity (linguistic)."""
        result = verify_t_tl_1(all_results)
        assert result["passed"], f"T-TL-1 failed: {result}"

    def test_t_tl_2(self, all_results):
        """T-TL-2: Pragmatic has lowest invertibility (linguistic)."""
        result = verify_t_tl_2(all_results)
        assert result["passed"], f"T-TL-2 failed: {result}"

    def test_t_tl_3(self, all_results):
        """T-TL-3: Categorical has highest cross-level coherence (mathematical)."""
        result = verify_t_tl_3(all_results)
        assert result["passed"], f"T-TL-3 failed: {result}"

    def test_t_tl_4(self, all_results):
        """T-TL-4: Math levels have higher mean invertibility than linguistic."""
        result = verify_t_tl_4(all_results)
        assert result["passed"], f"T-TL-4 failed: {result}"

    def test_t_tl_5(self, all_results):
        """T-TL-5: Discourse and categorical top generative productivity."""
        result = verify_t_tl_5(all_results)
        assert result["passed"], f"T-TL-5 failed: {result}"

    def test_t_tl_6(self, all_results):
        """T-TL-6: Linguistic gap > mathematical gap (more channel divergence)."""
        result = verify_t_tl_6(all_results)
        assert result["passed"], f"T-TL-6 failed: {result}"

    def test_all_theorems_pass(self):
        for t in verify_all_theorems():
            assert t["passed"], f"{t['name']} failed: {t}"


# ── Regime Classification ─────────────────────────────────────────────


class TestRegimeClassification:
    @pytest.mark.parametrize("entity", TL_ENTITIES, ids=lambda e: e.name)
    def test_regime_is_valid(self, entity):
        r = compute_tl_kernel(entity)
        assert r.regime in ("Stable", "Watch", "Collapse")

    def test_phonological_in_collapse(self, all_results):
        """Phonological level is in Collapse — low semantic preservation
        and referential grounding produce high drift (ω > 0.30). Sound
        patterns carry minimal meaning; the translation from phoneme to
        morpheme boundary is where the most meaning is lost."""
        phon = next(r for r in all_results if r.name == "phonological")
        assert phon.regime == "Collapse"
        assert phon.omega >= 0.30

    def test_mathematical_never_collapse(self, all_results):
        """Higher mathematical levels (algebraic and above) should not be
        in Collapse — they preserve enough structure. Symbolic level may
        enter Collapse due to low semantic preservation and referential
        grounding (pure token manipulation is semantics-free)."""
        for r in all_results:
            if r.domain == "mathematical" and r.name != "symbolic":
                assert r.regime != "Collapse", f"{r.name} unexpectedly in Collapse"

    def test_symbolic_high_drift(self, all_results):
        """Symbolic level has high drift — token manipulation without
        semantic grounding produces ω > 0.30. This parallels phonological
        in the linguistic domain: both are surface-level operations with
        minimal meaning preservation."""
        sym = next(r for r in all_results if r.name == "symbolic")
        assert sym.omega > 0.30


# ── Cross-Level Structural Analysis ──────────────────────────────────


class TestStructuralAnalysis:
    def test_analysis_has_both_domains(self):
        analysis = analyze_translation_structure()
        assert "linguistic" in analysis["per_domain"]
        assert "mathematical" in analysis["per_domain"]

    def test_analysis_result_count(self):
        analysis = analyze_translation_structure()
        assert len(analysis["all_results"]) == 12

    def test_rosetta_invariance_duality(self):
        analysis = analyze_translation_structure()
        assert analysis["rosetta_invariance"]["duality_all_hold"]

    def test_rosetta_invariance_bound(self):
        analysis = analyze_translation_structure()
        assert analysis["rosetta_invariance"]["integrity_bound_all_hold"]

    def test_mathematical_higher_mean_F(self, all_results):
        """Mathematical levels should have higher mean F than linguistic —
        formal systems preserve more structure on average."""
        ling_F = np.mean([r.F for r in all_results if r.domain == "linguistic"])
        math_F = np.mean([r.F for r in all_results if r.domain == "mathematical"])
        assert math_F > ling_F

    def test_mathematical_higher_mean_IC(self, all_results):
        """Mathematical levels should have higher mean IC — more uniform
        channel profiles yield stronger geometric mean coherence."""
        ling_IC = np.mean([r.IC for r in all_results if r.domain == "linguistic"])
        math_IC = np.mean([r.IC for r in all_results if r.domain == "mathematical"])
        assert math_IC > ling_IC


# ── Serialization ─────────────────────────────────────────────────────


class TestSerialization:
    def test_to_dict_has_all_keys(self, all_results):
        for r in all_results:
            d = r.to_dict()
            assert set(d.keys()) == {
                "name",
                "domain",
                "F",
                "omega",
                "S",
                "C",
                "kappa",
                "IC",
                "regime",
            }

    def test_to_dict_types(self, all_results):
        for r in all_results:
            d = r.to_dict()
            assert isinstance(d["name"], str)
            assert isinstance(d["domain"], str)
            assert isinstance(d["F"], float)
            assert isinstance(d["regime"], str)
