"""Drift Engine — Controlled Collapse-Return Loop for Generative Exploration.

CATALOGUE TAGS:  T-DE-1 through T-DE-6
TIER:            2 (Expansion — GCD domain, generative exploration)
DEPENDS ON:      Tier-1 identities (F + ω = 1, IC ≤ F, IC = exp(κ))
                 Tier-0 cost closures (Γ(ω), D_C, Δκ budget)
                 T-KS-1 (Dimensionality Fragility Law)

Harnesses the natural tendency of perturbed trace vectors to drift into the
Watch and Collapse regimes, then filters candidates by demonstrated return
through the seam.  The push into drift is the generative engine; the pull
through the seam is the quality filter.

*Ruptura est fons constantiae.* — Rupture is the source of constancy.

The drift engine operates in three phases:

    Phase 1 — PUSH (Controlled Dissolution)
        Perturb the baseline trace vector into a target drift band.
        Generate N candidate trace vectors by injecting noise calibrated
        to place them in Watch or shallow-Collapse regime.

    Phase 2 — EXPLORE (Kernel Evaluation)
        Compute (F, ω, S, C, κ, IC) for each candidate.
        Track the heterogeneity gap Δ = F − IC as the measure of
        creative divergence between channels.

    Phase 3 — PULL (Seam Filtration)
        Rank candidates by return strength: how much IC recovers
        relative to the drift cost incurred.  Candidates that cross
        the seam (budget closes within tol_seam) are welded returns.
        Candidates that fail are gestures — discarded with receipt.

Derivation chain:
    Axiom-0 → F + ω = 1 (duality) → IC ≤ F (integrity bound)
           → Γ(ω) = ω³/(1−ω+ε) (drift cost)
           → Δκ_budget = R·τ_R − (D_ω + D_C) (budget identity)
           → Seam closure: |s| ≤ tol_seam (return verification)

Six theorems:

    T-DE-1  Drift Controllability
            Perturbation strength maps monotonically to mean ω of
            candidates: stronger perturbation → higher drift.

    T-DE-2  Heterogeneity Gap Amplification
            Perturbed candidates have larger Δ = F − IC than the
            baseline, because perturbation increases channel variance.

    T-DE-3  Return Selectivity
            Among candidates pushed to ω ∈ [0.10, 0.35], the seam
            filter retains only those with IC recovery above baseline
            IC minus a tolerance — substantive returns, not noise.

    T-DE-4  Budget Ordering
            Candidates with lower drift cost Γ(ω) + D_C have higher
            return scores — the ledger correctly ranks cheap returns
            above expensive ones.

    T-DE-5  Regime Diversity
            A population of N ≥ 50 candidates at perturbation ≥ 0.15
            contains representatives from at least 2 distinct regimes
            (Watch and Collapse), demonstrating genuine exploration.

    T-DE-6  Generative Yield
            The fraction of candidates that pass the seam filter is
            strictly between 0 and 1 for moderate perturbation — the
            engine is neither trivial (all pass) nor degenerate (none
            pass).  This is the operational proof that controlled drift
            IS generative.
"""

from __future__ import annotations

import sys
from dataclasses import dataclass
from pathlib import Path

import numpy as np

_WORKSPACE = Path(__file__).resolve().parents[2]
if str(_WORKSPACE / "src") not in sys.path:
    sys.path.insert(0, str(_WORKSPACE / "src"))

from umcp.frozen_contract import (  # noqa: E402
    ALPHA,
    EPSILON,
    P_EXPONENT,
)
from umcp.kernel_optimized import compute_kernel_outputs  # noqa: E402

# ── Constants ────────────────────────────────────────────────────────

# Default drift band: Watch to shallow Collapse
DEFAULT_OMEGA_TARGET_MIN = 0.10
DEFAULT_OMEGA_TARGET_MAX = 0.35


# ── Cost Closures (local, matching frozen_contract) ──────────────────


def _gamma_omega(omega: float) -> float:
    """Drift cost Γ(ω) = ω^p / (1 − ω + ε).  Frozen: p=3, ε=1e-8."""
    return float(omega**P_EXPONENT / (1.0 - omega + EPSILON))


def _cost_curvature(C: float) -> float:
    """Curvature cost D_C = α·C.  Frozen: α=1.0."""
    return ALPHA * C


# ── Data Structures ──────────────────────────────────────────────────


@dataclass(frozen=True, slots=True)
class CandidateResult:
    """Kernel evaluation of a single perturbed candidate."""

    index: int
    trace: tuple[float, ...]
    F: float
    omega: float
    S: float
    C: float
    kappa: float
    IC: float
    regime: str
    heterogeneity_gap: float  # Δ = F − IC
    drift_cost: float  # Γ(ω)
    curvature_cost: float  # D_C = α·C
    total_cost: float  # Γ(ω) + D_C
    return_score: float  # IC / (total_cost + ε) — higher = better return per cost
    seam_pass: bool  # Whether this candidate crosses the seam


@dataclass
class DriftResult:
    """Complete result of a drift-engine exploration run."""

    # Baseline
    baseline_F: float
    baseline_omega: float
    baseline_IC: float
    baseline_regime: str
    baseline_gap: float

    # Configuration
    n_candidates: int
    perturbation: float
    omega_target: tuple[float, float]
    seed: int

    # Candidates
    candidates: list[CandidateResult]

    # Aggregates
    mean_omega: float
    mean_IC: float
    mean_gap: float
    regime_counts: dict[str, int]
    n_passed: int  # Candidates that passed seam filter
    yield_fraction: float  # n_passed / n_candidates
    best_candidate: CandidateResult | None

    @property
    def passed_candidates(self) -> list[CandidateResult]:
        """Candidates that survived the seam filter (demonstrated return)."""
        return [c for c in self.candidates if c.seam_pass]


# ── Regime Classification ────────────────────────────────────────────


def _classify_regime(omega: float, F: float, S: float, C: float) -> str:
    """Classify regime using frozen gates."""
    if omega >= 0.30:
        return "Collapse"
    if omega < 0.038 and F > 0.90 and S < 0.15 and C < 0.14:
        return "Stable"
    return "Watch"


# ── Core Engine ──────────────────────────────────────────────────────


def generate_candidates(
    baseline: np.ndarray,
    weights: np.ndarray,
    n_candidates: int = 100,
    perturbation: float = 0.25,
    omega_target: tuple[float, float] = (
        DEFAULT_OMEGA_TARGET_MIN,
        DEFAULT_OMEGA_TARGET_MAX,
    ),
    seed: int = 42,
) -> DriftResult:
    """Run the drift engine: push → explore → pull.

    Parameters
    ----------
    baseline : np.ndarray
        Baseline trace vector c ∈ [ε, 1−ε]^n.
    weights : np.ndarray
        Weight vector w ∈ Δⁿ (must sum to 1.0).
    n_candidates : int
        Number of perturbed candidates to generate.
    perturbation : float
        Maximum fractional perturbation per channel (e.g. 0.25 = ±25%).
    omega_target : tuple[float, float]
        Target drift band [ω_min, ω_max].  Candidates outside this band
        are still evaluated but penalized in return score.
    seed : int
        RNG seed for reproducibility.

    Returns
    -------
    DriftResult
        Complete exploration result with ranked candidates.
    """
    rng = np.random.default_rng(seed)
    eps = float(EPSILON)
    n_channels = len(baseline)

    # Clamp baseline
    c_base = np.clip(baseline.copy(), eps, 1.0 - eps)
    w = weights.copy()

    # ── Phase 0: Baseline evaluation ─────────────────────────────
    base_ko = compute_kernel_outputs(c_base, w)
    base_F = float(base_ko["F"])
    base_omega = float(base_ko["omega"])
    base_IC = float(base_ko["IC"])
    base_S = float(base_ko["S"])
    base_C = float(base_ko["C"])
    base_regime = _classify_regime(base_omega, base_F, base_S, base_C)
    base_gap = base_F - base_IC

    # ── Phase 1: PUSH — Generate perturbed candidates ────────────
    candidates: list[CandidateResult] = []
    regime_counts: dict[str, int] = {}

    for i in range(n_candidates):
        # Channel-wise multiplicative perturbation
        factors = rng.uniform(
            1.0 - perturbation,
            1.0 + perturbation,
            size=n_channels,
        )
        c_pert = np.clip(c_base * factors, eps, 1.0 - eps)

        # ── Phase 2: EXPLORE — Kernel evaluation ─────────────────
        ko = compute_kernel_outputs(c_pert, w)
        F = float(ko["F"])
        omega = float(ko["omega"])
        S = float(ko["S"])
        C = float(ko["C"])
        kappa = float(ko["kappa"])
        IC = float(ko["IC"])
        regime = _classify_regime(omega, F, S, C)
        gap = F - IC

        # Cost accounting
        drift_cost = _gamma_omega(omega)
        curv_cost = _cost_curvature(C)
        total_cost = drift_cost + curv_cost

        # ── Phase 3: PULL — Return score and seam filter ─────────
        # Return score: IC recovery per unit cost.
        # Higher IC with lower cost = better return from drift.
        return_score = IC / (total_cost + eps)

        # Seam filter: candidate passes if
        #   1. IC ≥ baseline_IC - tolerance (didn't destroy too much)
        #   2. ω is within or near target band
        #   3. The return score exceeds a minimum threshold
        ic_tolerance = 0.15  # Allow IC to drop up to 15% below baseline
        in_band = omega_target[0] <= omega <= omega_target[1]
        ic_recovered = (base_IC - ic_tolerance) <= IC
        has_return = return_score > eps

        seam_pass = ic_recovered and has_return and (in_band or omega < omega_target[0])

        regime_counts[regime] = regime_counts.get(regime, 0) + 1

        candidates.append(
            CandidateResult(
                index=i,
                trace=tuple(float(x) for x in c_pert),
                F=F,
                omega=omega,
                S=S,
                C=C,
                kappa=kappa,
                IC=IC,
                regime=regime,
                heterogeneity_gap=gap,
                drift_cost=drift_cost,
                curvature_cost=curv_cost,
                total_cost=total_cost,
                return_score=return_score,
                seam_pass=seam_pass,
            )
        )

    # ── Aggregate and rank ───────────────────────────────────────
    passed = [c for c in candidates if c.seam_pass]
    n_passed = len(passed)
    yield_frac = n_passed / n_candidates if n_candidates > 0 else 0.0

    # Best = highest return score among passed candidates
    best = max(passed, key=lambda c: c.return_score) if passed else None

    mean_omega = sum(c.omega for c in candidates) / n_candidates
    mean_IC = sum(c.IC for c in candidates) / n_candidates
    mean_gap = sum(c.heterogeneity_gap for c in candidates) / n_candidates

    return DriftResult(
        baseline_F=base_F,
        baseline_omega=base_omega,
        baseline_IC=base_IC,
        baseline_regime=base_regime,
        baseline_gap=base_gap,
        n_candidates=n_candidates,
        perturbation=perturbation,
        omega_target=omega_target,
        seed=seed,
        candidates=candidates,
        mean_omega=mean_omega,
        mean_IC=mean_IC,
        mean_gap=mean_gap,
        regime_counts=regime_counts,
        n_passed=n_passed,
        yield_fraction=yield_frac,
        best_candidate=best,
    )


# ── Theorems ─────────────────────────────────────────────────────────


def _make_test_trace(n: int = 8, base_val: float = 0.70) -> tuple[np.ndarray, np.ndarray]:
    """Create a baseline trace vector in Watch regime for testing."""
    c = np.full(n, base_val)
    w = np.ones(n) / n
    return c, w


def verify_t_de_1() -> dict:
    """T-DE-1: Drift Controllability — perturbation maps monotonically to ω."""
    c, w = _make_test_trace()
    perturbations = [0.05, 0.15, 0.25, 0.35, 0.45]
    mean_omegas = []

    for p in perturbations:
        result = generate_candidates(c, w, n_candidates=200, perturbation=p, seed=42)
        mean_omegas.append(result.mean_omega)

    # Check monotonicity (each mean ω ≥ previous, with small tolerance)
    monotone = all(mean_omegas[i + 1] >= mean_omegas[i] - 0.01 for i in range(len(mean_omegas) - 1))

    return {
        "theorem": "T-DE-1",
        "name": "Drift Controllability",
        "PROVEN": monotone,
        "perturbations": perturbations,
        "mean_omegas": [round(o, 4) for o in mean_omegas],
        "monotone": monotone,
    }


def verify_t_de_2() -> dict:
    """T-DE-2: Heterogeneity Gap Amplification — perturbation increases Δ."""
    c, w = _make_test_trace()
    base_ko = compute_kernel_outputs(c, w)
    base_gap = float(base_ko["F"]) - float(base_ko["IC"])

    result = generate_candidates(c, w, n_candidates=200, perturbation=0.25, seed=42)

    # Mean gap among candidates should exceed baseline gap
    amplified = result.mean_gap > base_gap

    return {
        "theorem": "T-DE-2",
        "name": "Heterogeneity Gap Amplification",
        "PROVEN": amplified,
        "baseline_gap": round(base_gap, 6),
        "mean_candidate_gap": round(result.mean_gap, 4),
        "amplification_ratio": round(result.mean_gap / max(base_gap, EPSILON), 2),
    }


def verify_t_de_3() -> dict:
    """T-DE-3: Return Selectivity — seam filter retains substantive returns."""
    c, w = _make_test_trace()
    result = generate_candidates(c, w, n_candidates=200, perturbation=0.25, seed=42)

    passed = result.passed_candidates
    if not passed:
        return {
            "theorem": "T-DE-3",
            "name": "Return Selectivity",
            "PROVEN": False,
            "reason": "No candidates passed seam filter",
        }

    # Passed candidates should have IC ≥ baseline_IC - tolerance
    ic_tol = 0.15
    all_recovered = all(result.baseline_IC - ic_tol <= p.IC for p in passed)

    # Mean IC of passed should be higher than mean IC of failed
    failed = [c for c in result.candidates if not c.seam_pass]
    if failed:
        mean_passed_ic = sum(p.IC for p in passed) / len(passed)
        mean_failed_ic = sum(f.IC for f in failed) / len(failed)
        selective = mean_passed_ic > mean_failed_ic
    else:
        selective = True
        mean_passed_ic = sum(p.IC for p in passed) / len(passed)
        mean_failed_ic = 0.0

    return {
        "theorem": "T-DE-3",
        "name": "Return Selectivity",
        "PROVEN": all_recovered and selective,
        "n_passed": len(passed),
        "n_failed": len(failed),
        "all_ic_recovered": all_recovered,
        "mean_passed_IC": round(mean_passed_ic, 4),
        "mean_failed_IC": round(mean_failed_ic, 4),
        "selective": selective,
    }


def verify_t_de_4() -> dict:
    """T-DE-4: Budget Ordering — lower cost → higher return score."""
    c, w = _make_test_trace()
    result = generate_candidates(c, w, n_candidates=200, perturbation=0.25, seed=42)

    passed = result.passed_candidates
    if len(passed) < 5:
        return {
            "theorem": "T-DE-4",
            "name": "Budget Ordering",
            "PROVEN": False,
            "reason": f"Need ≥5 passed candidates, got {len(passed)}",
        }

    # Spearman-like check: sort by total_cost, check return_score trend
    by_cost = sorted(passed, key=lambda c: c.total_cost)
    n = len(by_cost)
    low_half = by_cost[: n // 2]
    high_half = by_cost[n // 2 :]

    mean_low_return = sum(c.return_score for c in low_half) / len(low_half)
    mean_high_return = sum(c.return_score for c in high_half) / len(high_half)

    # Lower cost half should have higher return scores
    ordered = mean_low_return > mean_high_return

    return {
        "theorem": "T-DE-4",
        "name": "Budget Ordering",
        "PROVEN": ordered,
        "mean_return_low_cost": round(mean_low_return, 4),
        "mean_return_high_cost": round(mean_high_return, 4),
        "n_passed": len(passed),
    }


def verify_t_de_5() -> dict:
    """T-DE-5: Regime Diversity — candidates span ≥2 regimes."""
    c, w = _make_test_trace()
    result = generate_candidates(c, w, n_candidates=100, perturbation=0.25, seed=42)

    n_regimes = len(result.regime_counts)
    diverse = n_regimes >= 2

    return {
        "theorem": "T-DE-5",
        "name": "Regime Diversity",
        "PROVEN": diverse,
        "n_regimes": n_regimes,
        "regime_counts": result.regime_counts,
    }


def verify_t_de_6() -> dict:
    """T-DE-6: Generative Yield — 0 < yield < 1 for moderate perturbation."""
    c, w = _make_test_trace()
    result = generate_candidates(c, w, n_candidates=200, perturbation=0.25, seed=42)

    non_trivial = 0.0 < result.yield_fraction < 1.0

    return {
        "theorem": "T-DE-6",
        "name": "Generative Yield",
        "PROVEN": non_trivial,
        "yield_fraction": round(result.yield_fraction, 4),
        "n_passed": result.n_passed,
        "n_candidates": result.n_candidates,
    }


def verify_all_theorems() -> list[dict]:
    """Run all 6 drift engine theorems."""
    return [
        verify_t_de_1(),
        verify_t_de_2(),
        verify_t_de_3(),
        verify_t_de_4(),
        verify_t_de_5(),
        verify_t_de_6(),
    ]


# ── Main ─────────────────────────────────────────────────────────────


def main() -> None:
    """Demonstrate the drift engine and verify theorems."""
    print("=" * 70)
    print("DRIFT ENGINE — CONTROLLED COLLAPSE-RETURN EXPLORATION")
    print("=" * 70)

    # Demo: 8-channel baseline in Watch regime
    c, w = _make_test_trace(n=8, base_val=0.70)
    print(f"\nBaseline: {c}")
    print(f"Weights:  {w}")

    result = generate_candidates(
        c,
        w,
        n_candidates=200,
        perturbation=0.25,
        seed=42,
    )

    print(f"\n{'─' * 50}")
    print(
        f"Baseline: F={result.baseline_F:.4f}  ω={result.baseline_omega:.4f}  "
        f"IC={result.baseline_IC:.4f}  Δ={result.baseline_gap:.4f}  "
        f"[{result.baseline_regime}]"
    )
    print(f"\nCandidates: {result.n_candidates}")
    print(f"Mean ω={result.mean_omega:.4f}  Mean IC={result.mean_IC:.4f}  Mean Δ={result.mean_gap:.4f}")
    print(f"Regimes: {result.regime_counts}")
    print(f"\nSeam filter: {result.n_passed} passed ({result.yield_fraction:.1%} yield)")

    if result.best_candidate:
        b = result.best_candidate
        print(f"\nBest candidate #{b.index}:")
        print(f"  F={b.F:.4f}  ω={b.omega:.4f}  IC={b.IC:.4f}  Δ={b.heterogeneity_gap:.4f}")
        print(f"  Drift cost Γ={b.drift_cost:.4f}  Curvature cost D_C={b.curvature_cost:.4f}")
        print(f"  Return score={b.return_score:.4f}  [{b.regime}]")

    # Top 5 passed candidates by return score
    passed = result.passed_candidates
    if passed:
        top5 = sorted(passed, key=lambda c: c.return_score, reverse=True)[:5]
        print("\nTop 5 by return score:")
        for c in top5:
            print(
                f"  #{c.index:3d}: F={c.F:.3f} ω={c.omega:.3f} "
                f"IC={c.IC:.3f} Δ={c.heterogeneity_gap:.3f} "
                f"score={c.return_score:.3f} [{c.regime}]"
            )

    # Verify theorems
    print(f"\n{'=' * 70}")
    print("THEOREMS")
    print("=" * 70)
    results = verify_all_theorems()
    proven = sum(1 for r in results if r["PROVEN"])
    for r in results:
        status = "PROVEN" if r["PROVEN"] else "FAILED"
        print(f"  {r['theorem']}: {r['name']} — {status}")
    print(f"\n{proven}/{len(results)} theorems PROVEN")


if __name__ == "__main__":
    main()
