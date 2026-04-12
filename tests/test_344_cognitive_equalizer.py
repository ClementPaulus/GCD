"""Tests for the Cognitive Equalizer — Aequator Cognitivus.

Non agens mensurat, sed structura.
— Not the agent measures, but the structure.

Six theorems (T-CE-1 through T-CE-6) verify the structural properties
of the Cognitive Equalizer module.
"""

from __future__ import annotations

import pytest

from umcp.cognitive_equalizer import (
    CE_CHANNEL_NAMES,
    CE_SYSTEM_PROMPT,
    AequatorCognitivus,
    CanalesCognitivus,
    CEChannels,
    CELedger,
    CEReport,
    CEVerdict,
    CognitiveEqualizer,
    RatioCognitivus,
    RelatioCognitivus,
    SententiaCognitivus,
)

# ═══════════════════════════════════════════════════════════════════════════
# Fixtures
# ═══════════════════════════════════════════════════════════════════════════


@pytest.fixture
def ce() -> CognitiveEqualizer:
    return CognitiveEqualizer()


@pytest.fixture
def perfect_channels() -> CEChannels:
    """All channels at 1.0 — perfect engagement."""
    return CEChannels(1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0)


@pytest.fixture
def good_channels() -> CEChannels:
    """High-quality but imperfect engagement."""
    return CEChannels(
        relevance=0.95,
        accuracy=0.90,
        completeness=0.85,
        consistency=0.97,
        traceability=0.80,
        groundedness=0.92,
        constraint_respect=0.95,
        return_fidelity=0.88,
    )


@pytest.fixture
def dead_channel() -> CEChannels:
    """One dead traceability channel — geometric slaughter demo."""
    return CEChannels(
        relevance=0.90,
        accuracy=0.85,
        completeness=0.80,
        consistency=0.88,
        traceability=0.001,
        groundedness=0.82,
        constraint_respect=0.88,
        return_fidelity=0.75,
    )


@pytest.fixture
def collapse_channels() -> CEChannels:
    """Severely degraded engagement — Collapse regime."""
    return CEChannels(
        relevance=0.30,
        accuracy=0.25,
        completeness=0.20,
        consistency=0.35,
        traceability=0.10,
        groundedness=0.15,
        constraint_respect=0.28,
        return_fidelity=0.10,
    )


# ═══════════════════════════════════════════════════════════════════════════
# T-CE-1: Duality Identity (F + ω = 1 exactly)
# ═══════════════════════════════════════════════════════════════════════════


class TestTCE1Duality:
    """T-CE-1: The duality identity F + ω = 1 holds exactly for all CE traces."""

    def test_perfect_duality(self, ce: CognitiveEqualizer, perfect_channels: CEChannels) -> None:
        report = ce.engage("test", perfect_channels)
        assert report.F + report.omega == pytest.approx(1.0, abs=0.0)

    def test_good_duality(self, ce: CognitiveEqualizer, good_channels: CEChannels) -> None:
        report = ce.engage("test", good_channels)
        assert report.F + report.omega == pytest.approx(1.0, abs=0.0)

    def test_dead_channel_duality(self, ce: CognitiveEqualizer, dead_channel: CEChannels) -> None:
        report = ce.engage("test", dead_channel)
        assert report.F + report.omega == pytest.approx(1.0, abs=0.0)

    def test_collapse_duality(self, ce: CognitiveEqualizer, collapse_channels: CEChannels) -> None:
        report = ce.engage("test", collapse_channels)
        assert report.F + report.omega == pytest.approx(1.0, abs=0.0)

    @pytest.mark.parametrize("val", [0.0, 0.1, 0.25, 0.5, 0.75, 0.9, 1.0])
    def test_homogeneous_duality(self, ce: CognitiveEqualizer, val: float) -> None:
        ch = CEChannels(val, val, val, val, val, val, val, val)
        report = ce.engage("test", ch)
        assert report.F + report.omega == pytest.approx(1.0, abs=0.0)

    @pytest.mark.parametrize(
        "vals",
        [
            (0.1, 0.9, 0.5, 0.3, 0.8, 0.2, 0.7, 0.4),
            (0.99, 0.01, 0.50, 0.50, 0.99, 0.01, 0.50, 0.50),
            (0.001, 0.001, 0.001, 0.999, 0.999, 0.999, 0.5, 0.5),
        ],
    )
    def test_heterogeneous_duality(self, ce: CognitiveEqualizer, vals: tuple[float, ...]) -> None:
        ch = CEChannels(*vals)
        report = ce.engage("test", ch)
        assert report.F + report.omega == pytest.approx(1.0, abs=0.0)


# ═══════════════════════════════════════════════════════════════════════════
# T-CE-2: Integrity Bound (IC ≤ F)
# ═══════════════════════════════════════════════════════════════════════════


class TestTCE2IntegrityBound:
    """T-CE-2: The integrity bound IC ≤ F holds for all CE traces."""

    def test_perfect_bound(self, ce: CognitiveEqualizer, perfect_channels: CEChannels) -> None:
        report = ce.engage("test", perfect_channels)
        assert report.IC <= report.F + 1e-15

    def test_good_bound(self, ce: CognitiveEqualizer, good_channels: CEChannels) -> None:
        report = ce.engage("test", good_channels)
        assert report.IC <= report.F + 1e-15

    def test_dead_channel_bound(self, ce: CognitiveEqualizer, dead_channel: CEChannels) -> None:
        report = ce.engage("test", dead_channel)
        assert report.IC <= report.F + 1e-15

    def test_collapse_bound(self, ce: CognitiveEqualizer, collapse_channels: CEChannels) -> None:
        report = ce.engage("test", collapse_channels)
        assert report.IC <= report.F + 1e-15

    @pytest.mark.parametrize("val", [0.001, 0.1, 0.25, 0.5, 0.75, 0.9, 1.0])
    def test_homogeneous_bound(self, ce: CognitiveEqualizer, val: float) -> None:
        ch = CEChannels(val, val, val, val, val, val, val, val)
        report = ce.engage("test", ch)
        assert report.IC <= report.F + 1e-15

    def test_all_zero_guard_band(self, ce: CognitiveEqualizer) -> None:
        """At c=0, IC = ε (guard band) and F = 0. Guard band is Tier-1 structure."""
        ch = CEChannels(0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
        report = ce.engage("test", ch)
        assert report.F == 0.0
        assert pytest.approx(1e-8, rel=1e-3) == report.IC  # guard band ε

    @pytest.mark.parametrize(
        "vals",
        [
            (0.1, 0.9, 0.5, 0.3, 0.8, 0.2, 0.7, 0.4),
            (0.99, 0.01, 0.50, 0.50, 0.99, 0.01, 0.50, 0.50),
            (0.001, 0.001, 0.001, 0.999, 0.999, 0.999, 0.5, 0.5),
        ],
    )
    def test_heterogeneous_bound(self, ce: CognitiveEqualizer, vals: tuple[float, ...]) -> None:
        ch = CEChannels(*vals)
        report = ce.engage("test", ch)
        assert report.IC <= report.F + 1e-15

    def test_homogeneous_equality(self, ce: CognitiveEqualizer) -> None:
        """For homogeneous traces, IC = F exactly (AM = GM when all values equal)."""
        ch = CEChannels(0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7)
        report = ce.engage("test", ch)
        assert pytest.approx(report.F, abs=1e-10) == report.IC

    def test_gap_positive(self, ce: CognitiveEqualizer, dead_channel: CEChannels) -> None:
        """Heterogeneity gap Δ = F − IC is non-negative and large for dead channel."""
        report = ce.engage("test", dead_channel)
        assert report.delta >= 0
        assert report.delta > 0.3  # substantial gap due to dead channel


# ═══════════════════════════════════════════════════════════════════════════
# T-CE-3: Geometric Slaughter (one dead channel kills IC)
# ═══════════════════════════════════════════════════════════════════════════


class TestTCE3GeometricSlaughter:
    """T-CE-3: One dead channel obliterates IC while F remains healthy."""

    def test_dead_channel_ic_collapse(self, ce: CognitiveEqualizer) -> None:
        """7 perfect channels + 1 dead → IC ≈ 0.1, F ≈ 0.87."""
        ch = CEChannels(
            relevance=0.999,
            accuracy=0.999,
            completeness=0.999,
            consistency=0.999,
            traceability=1e-8,
            groundedness=0.999,
            constraint_respect=0.999,
            return_fidelity=0.999,
        )
        report = ce.engage("test", ch)
        assert report.F > 0.85
        assert report.IC < 0.15
        assert report.IC / report.F < 0.15  # IC/F ratio < 0.15

    def test_progressive_slaughter(self, ce: CognitiveEqualizer) -> None:
        """As one channel degrades, IC drops faster than F."""
        prev_ic = 1.0
        for dead_val in [0.5, 0.1, 0.01, 0.001, 1e-8]:
            ch = CEChannels(
                relevance=0.999,
                accuracy=0.999,
                completeness=0.999,
                consistency=0.999,
                traceability=dead_val,
                groundedness=0.999,
                constraint_respect=0.999,
                return_fidelity=0.999,
            )
            report = ce.engage("test", ch)
            assert prev_ic > report.IC  # IC monotonically decreases
            prev_ic = report.IC

    def test_ic_f_ratio_progression(self, ce: CognitiveEqualizer) -> None:
        """IC/F ratio drops as dead channel worsens."""
        ratios = []
        for dead_val in [1.0, 0.5, 0.1, 0.01, 0.001, 1e-8]:
            ch = CEChannels(dead_val, 0.999, 0.999, 0.999, 0.999, 0.999, 0.999, 0.999)
            report = ce.engage("test", ch)
            ratios.append(report.IC / max(report.F, 1e-15))
        # Ratios must be monotonically non-increasing
        for i in range(1, len(ratios)):
            assert ratios[i] <= ratios[i - 1] + 1e-10

    def test_all_channels_vulnerable(self, ce: CognitiveEqualizer) -> None:
        """Killing ANY single channel triggers slaughter — all 8 are vulnerable."""
        for i in range(8):
            vals = [0.95] * 8
            vals[i] = 1e-8  # kill this channel
            ch = CEChannels(*vals)
            report = ce.engage("test", ch)
            assert report.IC < 0.15, f"Channel {CE_CHANNEL_NAMES[i]} kill failed"
            assert report.F > 0.80, f"F should stay high for channel {CE_CHANNEL_NAMES[i]}"


# ═══════════════════════════════════════════════════════════════════════════
# T-CE-4: Regime Classification (frozen gates derive verdict)
# ═══════════════════════════════════════════════════════════════════════════


class TestTCE4RegimeClassification:
    """T-CE-4: Regime gates classify correctly into STABLE/WATCH/COLLAPSE."""

    def test_perfect_is_stable(self, ce: CognitiveEqualizer, perfect_channels: CEChannels) -> None:
        report = ce.engage("test", perfect_channels)
        assert report.regime == "STABLE"
        assert report.stance == CEVerdict.CONFORMANT

    def test_good_regime(self, ce: CognitiveEqualizer, good_channels: CEChannels) -> None:
        report = ce.engage("test", good_channels)
        assert report.regime in ("STABLE", "WATCH")

    def test_collapse_classification(self, ce: CognitiveEqualizer, collapse_channels: CEChannels) -> None:
        report = ce.engage("test", collapse_channels)
        assert report.regime == "COLLAPSE"
        assert report.stance == CEVerdict.NONCONFORMANT

    def test_critical_overlay(self, ce: CognitiveEqualizer) -> None:
        """IC < 0.30 triggers critical overlay regardless of regime."""
        ch = CEChannels(0.5, 0.5, 0.5, 0.5, 0.001, 0.5, 0.5, 0.5)
        report = ce.engage("test", ch)
        assert report.is_critical

    def test_stable_requires_all_gates(self, ce: CognitiveEqualizer) -> None:
        """Stable is conjunctive — all four gates must pass."""
        # High F but high curvature — should NOT be Stable
        ch = CEChannels(0.99, 0.99, 0.50, 0.99, 0.99, 0.50, 0.99, 0.99)
        report = ce.engage("test", ch)
        assert report.regime != "STABLE"  # curvature too high

    def test_watch_intermediate(self, ce: CognitiveEqualizer) -> None:
        """Watch regime for intermediate drift."""
        ch = CEChannels(0.85, 0.85, 0.85, 0.85, 0.85, 0.85, 0.85, 0.85)
        report = ce.engage("test", ch)
        assert report.regime == "WATCH"  # drift = 0.15 is in Watch range

    def test_verdict_is_three_valued(self) -> None:
        """CEVerdict has exactly three members."""
        assert len(CEVerdict) == 3
        assert {v.value for v in CEVerdict} == {"CONFORMANT", "NONCONFORMANT", "NON_EVALUABLE"}

    def test_non_evaluable_on_bad_input(self, ce: CognitiveEqualizer) -> None:
        """Out-of-range channel scores produce NON_EVALUABLE."""
        ch = CEChannels(
            relevance=1.5,
            accuracy=0.9,
            completeness=0.8,
            consistency=0.9,
            traceability=0.7,
            groundedness=0.85,
            constraint_respect=0.9,
            return_fidelity=0.8,
        )
        report = ce.engage("test", ch)
        assert report.stance == CEVerdict.NON_EVALUABLE
        assert len(report.errors) > 0


# ═══════════════════════════════════════════════════════════════════════════
# T-CE-5: Cognitive Equalizer Property (same input → same output)
# ═══════════════════════════════════════════════════════════════════════════


class TestTCE5CognitiveEqualizerProperty:
    """T-CE-5: Two independent CE instances produce identical verdicts."""

    def test_two_instances_same_result(self, good_channels: CEChannels) -> None:
        """Two CognitiveEqualizer instances, same channels → identical report."""
        ce1 = CognitiveEqualizer()
        ce2 = CognitiveEqualizer()  # independent instance
        r1 = ce1.engage("same question", good_channels)
        r2 = ce2.engage("same question", good_channels)
        assert r1.F == r2.F
        assert r1.IC == r2.IC
        assert r1.omega == r2.omega
        assert r1.delta == r2.delta
        assert r1.regime == r2.regime
        assert r1.stance == r2.stance
        assert r1.ledger.delta_kappa == r2.ledger.delta_kappa

    def test_question_does_not_change_verdict(self, good_channels: CEChannels) -> None:
        """Different questions, same channels → same verdict (channels drive, not question)."""
        ce = CognitiveEqualizer()
        r1 = ce.engage("Explain quantum mechanics", good_channels)
        r2 = ce.engage("What is 2+2?", good_channels)
        assert r1.F == r2.F
        assert r1.stance == r2.stance
        assert r1.regime == r2.regime

    def test_latin_alias_identity(self, good_channels: CEChannels) -> None:
        """AequatorCognitivus IS CognitiveEqualizer — same class."""
        assert AequatorCognitivus is CognitiveEqualizer
        ac = AequatorCognitivus()
        report = ac.engage("test", good_channels)
        assert report.stance in (CEVerdict.CONFORMANT, CEVerdict.NONCONFORMANT, CEVerdict.NON_EVALUABLE)

    def test_score_shorthand_matches_engage(self) -> None:
        """score() shorthand produces same result as engage()."""
        ce = CognitiveEqualizer()
        kw = {
            "relevance": 0.9,
            "accuracy": 0.85,
            "completeness": 0.8,
            "consistency": 0.95,
            "traceability": 0.7,
            "groundedness": 0.88,
            "constraint_respect": 0.92,
            "return_fidelity": 0.75,
        }
        r1 = ce.score(**kw)
        r2 = ce.engage("x", CEChannels(**kw))
        assert r1.F == r2.F
        assert r1.IC == r2.IC
        assert r1.stance == r2.stance

    def test_frozen_params_not_empty(self) -> None:
        """frozen_params audit surface is populated."""
        ce = CognitiveEqualizer()
        params = ce.frozen_params
        assert "EPSILON" in params
        assert "TOL_SEAM" in params
        assert params["EPSILON"] == pytest.approx(1e-8, rel=1e-6)
        assert params["P_EXPONENT"] == 3


# ═══════════════════════════════════════════════════════════════════════════
# T-CE-6: Spine Completeness (all five stops present in report)
# ═══════════════════════════════════════════════════════════════════════════


class TestTCE6SpineCompleteness:
    """T-CE-6: CEReport contains all five Spine stops and formats correctly."""

    def test_report_has_contract(self, ce: CognitiveEqualizer, good_channels: CEChannels) -> None:
        report = ce.engage("test", good_channels)
        assert report.contract_label == "CE-v1-frozen"

    def test_report_has_narrative(self, ce: CognitiveEqualizer, good_channels: CEChannels) -> None:
        report = ce.engage("test", good_channels)
        assert len(report.narrative) > 0
        # Narrative uses five words
        for word in ["Drift", "Fidelity", "Roughness", "Return", "Integrity"]:
            assert word in report.narrative

    def test_report_has_regime(self, ce: CognitiveEqualizer, good_channels: CEChannels) -> None:
        report = ce.engage("test", good_channels)
        assert report.regime in ("STABLE", "WATCH", "COLLAPSE", "NON_EVALUABLE")

    def test_report_has_ledger(self, ce: CognitiveEqualizer, good_channels: CEChannels) -> None:
        report = ce.engage("test", good_channels)
        assert isinstance(report.ledger, CELedger)
        assert hasattr(report.ledger, "D_drift")
        assert hasattr(report.ledger, "D_roughness")
        assert hasattr(report.ledger, "R_return")
        assert hasattr(report.ledger, "delta_kappa")

    def test_report_has_stance(self, ce: CognitiveEqualizer, good_channels: CEChannels) -> None:
        report = ce.engage("test", good_channels)
        assert isinstance(report.stance, CEVerdict)

    def test_summary_format(self, ce: CognitiveEqualizer, good_channels: CEChannels) -> None:
        report = ce.engage("test", good_channels)
        summary = report.summary()
        assert "[CE]" in summary
        assert "F=" in summary
        assert "IC=" in summary

    def test_full_report_format(self, ce: CognitiveEqualizer, good_channels: CEChannels) -> None:
        report = ce.engage("test", good_channels)
        full = report.full_report()
        assert "COGNITIVE EQUALIZER" in full
        assert "Aequator Cognitivus" in full
        assert "Contract" in full
        assert "Canon" in full
        assert "Integrity Ledger" in full or "Ledger" in full
        assert "Stance" in full

    def test_channel_names_count(self) -> None:
        assert len(CE_CHANNEL_NAMES) == 8

    def test_system_prompt_exists(self) -> None:
        assert len(CE_SYSTEM_PROMPT) > 500
        assert "COGNITIVE EQUALIZER" in CE_SYSTEM_PROMPT
        assert "SPINE" in CE_SYSTEM_PROMPT
        assert "FIVE WORDS" in CE_SYSTEM_PROMPT

    def test_latin_aliases_exist(self) -> None:
        """All Latin aliases are correctly aliased."""
        assert CanalesCognitivus is CEChannels
        assert RelatioCognitivus is CEReport
        assert SententiaCognitivus is CEVerdict
        assert RatioCognitivus is CELedger
