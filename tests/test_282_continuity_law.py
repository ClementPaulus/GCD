"""Tests for umcp.continuity_law — budget identity & continuity verification.

Covers:
  - verify_continuity_law() with valid transitions (passing)
  - verify_continuity_law() with infinite τ_R (∞_rec)
  - verify_continuity_law() with I_pre = 0 edge case
  - verify_continuity_law() with large residual (failing)
  - verify_continuity_law() with explicit delta_kappa_ledger
  - verify_continuity_chain() across multiple transitions
  - ContinuityLawSpec defaults match frozen contract
  - ContinuityVerdict fields
"""

from __future__ import annotations

import math

import pytest

from umcp.continuity_law import (
    DEFAULT_CONTINUITY_SPEC,
    ContinuityLawSpec,
    ContinuityVerdict,
    verify_continuity_chain,
    verify_continuity_law,
)
from umcp.frozen_contract import ALPHA, EPSILON, LAMBDA, P_EXPONENT, TOL_SEAM


class TestContinuityLawSpec:
    """ContinuityLawSpec defaults match frozen contract."""

    def test_defaults_match_frozen_contract(self) -> None:
        spec = ContinuityLawSpec()
        assert spec.tol_seam == TOL_SEAM
        assert spec.p == P_EXPONENT
        assert spec.alpha == ALPHA
        assert spec.lambda_drift == LAMBDA
        assert spec.epsilon == EPSILON

    def test_default_singleton(self) -> None:
        assert DEFAULT_CONTINUITY_SPEC.tol_seam == TOL_SEAM

    def test_custom_spec(self) -> None:
        spec = ContinuityLawSpec(tol_seam=0.01, p=5)
        assert spec.tol_seam == 0.01
        assert spec.p == 5


class TestVerifyContinuityLaw:
    """Test verify_continuity_law() in all code paths."""

    def test_passing_transition(self) -> None:
        """Low drift, finite τ_R, matching budget → passes."""
        I_pre = 0.8
        I_post = 0.75
        omega = 0.05
        C = 0.1
        tau_R = 1.0
        v = verify_continuity_law(I_pre=I_pre, I_post=I_post, tau_R=tau_R, omega=omega, C=C)
        assert isinstance(v, ContinuityVerdict)
        assert isinstance(v.delta_kappa, float)
        assert isinstance(v.ir, float)
        assert math.isfinite(v.ir)
        assert math.isfinite(v.identity_error)
        assert isinstance(v.failures, tuple)

    def test_infinite_tau_R_fails(self) -> None:
        """τ_R = ∞_rec → zero credit, should fail."""
        v = verify_continuity_law(I_pre=0.8, I_post=0.75, tau_R=float("inf"), omega=0.05, C=0.1)
        assert not v.passes
        assert any("not finite" in f for f in v.failures)

    def test_I_pre_zero_fails(self) -> None:
        """I_pre = 0 → cannot compute ratio."""
        v = verify_continuity_law(I_pre=0.0, I_post=0.5, tau_R=1.0, omega=0.05, C=0.1)
        assert not v.passes
        assert v.ir == 0.0
        assert any("I_pre = 0" in f for f in v.failures)

    def test_I_post_zero_with_I_pre_zero(self) -> None:
        """Both I_pre and I_post zero → multiple failures."""
        v = verify_continuity_law(I_pre=0.0, I_post=0.0, tau_R=1.0, omega=0.05, C=0.1)
        assert not v.passes
        assert any("I_pre = 0" in f for f in v.failures)

    def test_large_residual_fails(self) -> None:
        """Explicit delta_kappa_ledger with large mismatch → residual fails."""
        v = verify_continuity_law(I_pre=0.8, I_post=0.75, tau_R=1.0, omega=0.05, C=0.1, delta_kappa_ledger=100.0)
        assert not v.passes
        assert any("tol_seam" in f for f in v.failures)

    def test_explicit_delta_kappa_ledger_passing(self) -> None:
        """When delta_kappa_ledger is provided and matches budget → residual OK."""
        from umcp.frozen_contract import gamma_omega

        omega = 0.05
        C = 0.1
        tau_R = 1.0
        R = 1.0
        spec = ContinuityLawSpec()
        D_omega = gamma_omega(omega, p=spec.p, epsilon=spec.epsilon)
        D_C = spec.alpha * C
        budget = R * tau_R - (D_omega + D_C)
        v = verify_continuity_law(
            I_pre=0.8,
            I_post=0.8 * math.exp(budget),
            tau_R=tau_R,
            omega=omega,
            C=C,
            delta_kappa_ledger=budget,
        )
        assert abs(v.residual) < spec.tol_seam

    def test_identity_error_field(self) -> None:
        """identity_error = |ir - exp(Δκ)|."""
        v = verify_continuity_law(I_pre=0.9, I_post=0.85, tau_R=1.0, omega=0.02, C=0.05)
        assert v.identity_error == pytest.approx(abs(v.ir - v.ir_expected), abs=1e-12)

    def test_custom_spec_tolerance(self) -> None:
        """Custom spec with large tolerance → passes even with mismatch."""
        spec = ContinuityLawSpec(tol_seam=1000.0, tol_identity=1000.0)
        v = verify_continuity_law(I_pre=0.8, I_post=0.1, tau_R=1.0, omega=0.5, C=0.5, spec=spec)
        # With very large tolerances, residual and identity checks don't fail
        failures_without_inf = [f for f in v.failures if "not finite" not in f]
        assert len(failures_without_inf) == 0

    def test_R_zero_no_credit(self) -> None:
        """R=0 means no return credit."""
        v = verify_continuity_law(I_pre=0.8, I_post=0.75, tau_R=1.0, omega=0.05, C=0.1, R=0.0)
        # Budget = 0*1 - costs = negative
        assert v.delta_kappa < 0

    def test_verdict_is_namedtuple(self) -> None:
        """ContinuityVerdict is a NamedTuple with correct fields."""
        v = verify_continuity_law(I_pre=0.8, I_post=0.75, tau_R=1.0, omega=0.05, C=0.1)
        assert hasattr(v, "passes")
        assert hasattr(v, "delta_kappa")
        assert hasattr(v, "ir")
        assert hasattr(v, "ir_expected")
        assert hasattr(v, "identity_error")
        assert hasattr(v, "residual")
        assert hasattr(v, "failures")


class TestVerifyContinuityChain:
    """Test verify_continuity_chain() function."""

    def test_empty_chain(self) -> None:
        result = verify_continuity_chain([])
        assert result == []

    def test_single_transition_chain(self) -> None:
        transitions = [
            {
                "I_pre": 0.8,
                "I_post": 0.75,
                "tau_R": 1.0,
                "omega": 0.05,
                "C": 0.1,
            }
        ]
        verdicts = verify_continuity_chain(transitions)
        assert len(verdicts) == 1
        assert isinstance(verdicts[0], ContinuityVerdict)

    def test_multi_transition_chain(self) -> None:
        transitions = [
            {"I_pre": 0.9, "I_post": 0.85, "tau_R": 1.0, "omega": 0.02, "C": 0.05, "R": 1.0},
            {"I_pre": 0.85, "I_post": 0.80, "tau_R": 2.0, "omega": 0.03, "C": 0.08, "R": 0.5},
            {"I_pre": 0.80, "I_post": 0.75, "tau_R": float("inf"), "omega": 0.1, "C": 0.2},
        ]
        verdicts = verify_continuity_chain(transitions)
        assert len(verdicts) == 3
        # Third has infinite τ_R → should fail
        assert not verdicts[2].passes

    def test_chain_with_custom_spec(self) -> None:
        spec = ContinuityLawSpec(tol_seam=100.0, tol_identity=100.0)
        transitions = [
            {"I_pre": 0.9, "I_post": 0.1, "tau_R": 1.0, "omega": 0.5, "C": 0.5},
        ]
        verdicts = verify_continuity_chain(transitions, spec=spec)
        assert len(verdicts) == 1

    def test_chain_with_delta_kappa_ledger(self) -> None:
        transitions = [
            {"I_pre": 0.9, "I_post": 0.85, "tau_R": 1.0, "omega": 0.02, "C": 0.05, "delta_kappa_ledger": 0.0},
        ]
        verdicts = verify_continuity_chain(transitions)
        assert len(verdicts) == 1
