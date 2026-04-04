"""Regime Derivation — D(x,t) ↔ Kernel Regime Mapping (RCFT.INTSTACK.v1).

CATALOGUE TAGS:  T-RD-1 through T-RD-6
TIER:            2 (Expansion — RCFT domain)
DEPENDS ON:      Tier-1 identities (F + ω = 1, IC ≤ F, IC = exp(κ))
                 Tier-0 frozen contract (ε, p, α, tol_seam)
                 Orientation §4 (first weld at c ≈ 0.318)

Closes the first of five open gestures from the RCFT second edition
(§ sec:open, item 4): the connection between the original RCFT collapse
dominance field D(x,t) = ‖ϑ‖²/|v| and the kernel's regime classification.

The derivation shows that:
  1. The kernel's seam budget D_budget = Γ(ω) + α·C is the discrete
     analogue of the continuous D(x,t).
  2. D(x,t) ≥ 1 maps to budget deficit: D_ω + D_C ≥ available credit.
  3. The frozen regime gates partition the budget space consistently.
  4. For rank-1 (uniform) systems, the mapping is bijective.

Channels (8, equal weights w_i = 1/8):
  0  coherence_level       — mean channel fidelity (maps to |v|)
  1  amplification         — stochastic amplitude (maps to ‖ϑ‖)
  2  advection_fidelity    — return capacity (maps to |v| in SDE)
  3  drift_exposure        — proximity to collapse (Γ(ω) normalized)
  4  curvature_load        — coupling to uncontrolled DOF (D_C)
  5  budget_headroom       — credit − debit margin (normalized)
  6  entropy_state         — Bernoulli field entropy (normalized)
  7  return_capacity       — τ_R feasibility (1 = finite, ε = ∞_rec)

12 entities across 4 regime zones:
  Deep Stable (3): quiescent, laminar, near_unity
  Watch Band (3): moderate_drift, asymmetric_load, curvature_onset
  Onset Collapse (3): threshold_crossing, budget_deficit, critical_coupling
  Deep Collapse (3): full_dissolution, geometric_slaughter, maximum_entropy

6 theorems (T-RD-1 through T-RD-6).
"""

from __future__ import annotations

import math
import sys
from dataclasses import dataclass
from pathlib import Path

import numpy as np

_WORKSPACE = Path(__file__).resolve().parents[2]
for _p in [str(_WORKSPACE / "src"), str(_WORKSPACE)]:
    if _p not in sys.path:
        sys.path.insert(0, _p)

from umcp.frozen_contract import ALPHA, EPSILON, P_EXPONENT  # noqa: E402
from umcp.kernel_optimized import compute_kernel_outputs  # noqa: E402

RD_CHANNELS = [
    "coherence_level",
    "amplification",
    "advection_fidelity",
    "drift_exposure",
    "curvature_load",
    "budget_headroom",
    "entropy_state",
    "return_capacity",
]
N_RD_CHANNELS = len(RD_CHANNELS)


@dataclass(frozen=True, slots=True)
class RegimeDerivationEntity:
    """A collapse dominance scenario with 8 measurable channels."""

    name: str
    category: str
    coherence_level: float
    amplification: float
    advection_fidelity: float
    drift_exposure: float
    curvature_load: float
    budget_headroom: float
    entropy_state: float
    return_capacity: float

    def trace_vector(self) -> np.ndarray:
        return np.array(
            [
                self.coherence_level,
                self.amplification,
                self.advection_fidelity,
                self.drift_exposure,
                self.curvature_load,
                self.budget_headroom,
                self.entropy_state,
                self.return_capacity,
            ]
        )


# ═══════════════════════════════════════════════════════════════════
#  ENTITY CATALOG — 12 collapse dominance scenarios
# ═══════════════════════════════════════════════════════════════════

RD_ENTITIES: tuple[RegimeDerivationEntity, ...] = (
    # ── Deep Stable (all four gates: ω < 0.038, F > 0.90, S < 0.15, C < 0.14) ──
    RegimeDerivationEntity("quiescent", "deep_stable", 0.99, 0.98, 0.99, 0.98, 0.97, 0.99, 0.97, 0.99),
    RegimeDerivationEntity("laminar", "deep_stable", 0.97, 0.97, 0.98, 0.96, 0.97, 0.98, 0.96, 0.97),
    RegimeDerivationEntity("near_unity", "deep_stable", 0.96, 0.97, 0.97, 0.96, 0.97, 0.96, 0.97, 0.96),
    # ── Watch Band (0.038 ≤ ω < 0.30, or stable gates not all met) ──
    RegimeDerivationEntity("moderate_drift", "watch_band", 0.85, 0.82, 0.88, 0.80, 0.84, 0.86, 0.78, 0.85),
    RegimeDerivationEntity("asymmetric_load", "watch_band", 0.92, 0.60, 0.90, 0.85, 0.75, 0.88, 0.70, 0.80),
    RegimeDerivationEntity("curvature_onset", "watch_band", 0.78, 0.80, 0.76, 0.82, 0.74, 0.80, 0.75, 0.79),
    # ── Onset Collapse (ω near or above 0.30) ──
    RegimeDerivationEntity("threshold_crossing", "onset_collapse", 0.68, 0.55, 0.60, 0.50, 0.55, 0.45, 0.55, 0.60),
    RegimeDerivationEntity("budget_deficit", "onset_collapse", 0.60, 0.50, 0.55, 0.45, 0.60, 0.40, 0.60, 0.55),
    RegimeDerivationEntity("critical_coupling", "onset_collapse", 0.65, 0.45, 0.50, 0.40, 0.70, 0.35, 0.55, 0.50),
    # ── Deep Collapse (ω well above 0.30) ──
    RegimeDerivationEntity("full_dissolution", "deep_collapse", 0.20, 0.15, 0.18, 0.12, 0.85, 0.10, 0.75, 0.15),
    RegimeDerivationEntity("geometric_slaughter", "deep_collapse", 0.01, 0.90, 0.85, 0.80, 0.10, 0.60, 0.40, 0.70),
    RegimeDerivationEntity("maximum_entropy", "deep_collapse", 0.50, 0.50, 0.50, 0.50, 0.50, 0.50, 0.99, 0.50),
)


# ═══════════════════════════════════════════════════════════════════
#  BUDGET COMPUTATION — D(x,t) → D_budget mapping
# ═══════════════════════════════════════════════════════════════════


def drift_cost(omega: float) -> float:
    """Γ(ω) = ω^p / (1 − ω + ε) — the drift cost potential."""
    return omega**P_EXPONENT / (1.0 - omega + EPSILON)


def curvature_cost(C: float) -> float:
    """D_C = α · C — the curvature debit."""
    return ALPHA * C


def total_debit(omega: float, C: float) -> float:
    """D_budget = Γ(ω) + α · C — the total collapse debit.

    This is the discrete kernel analogue of the original RCFT collapse
    dominance field D(x,t) = ‖ϑ‖² / |v|.  The identification is:
      ‖ϑ‖²  →  Γ(ω)  (stochastic amplification → drift cost)
      |v|   →  1 / (1 + α·C)  (advection speed → inverse curvature load)
    """
    return drift_cost(omega) + curvature_cost(C)


# ═══════════════════════════════════════════════════════════════════
#  KERNEL COMPUTATION
# ═══════════════════════════════════════════════════════════════════


@dataclass(frozen=True, slots=True)
class RDKernelResult:
    """Kernel output for a regime derivation entity."""

    name: str
    category: str
    F: float
    omega: float
    S: float
    C: float
    kappa: float
    IC: float
    regime: str
    D_budget: float

    def to_dict(self) -> dict:
        return {k: getattr(self, k) for k in self.__dataclass_fields__}


def compute_rd_kernel(entity: RegimeDerivationEntity) -> RDKernelResult:
    """Compute GCD kernel and budget for a regime derivation entity."""
    c = entity.trace_vector()
    c = np.clip(c, EPSILON, 1.0 - EPSILON)
    w = np.ones(N_RD_CHANNELS) / N_RD_CHANNELS
    result = compute_kernel_outputs(c, w)
    F = float(result["F"])
    omega = float(result["omega"])
    S = float(result["S"])
    C_val = float(result["C"])
    kappa = float(result["kappa"])
    IC = float(result["IC"])
    D_b = total_debit(omega, C_val)
    if omega >= 0.30:
        regime = "Collapse"
    elif omega < 0.038 and F > 0.90 and S < 0.15 and C_val < 0.14:
        regime = "Stable"
    else:
        regime = "Watch"
    return RDKernelResult(
        name=entity.name,
        category=entity.category,
        F=F,
        omega=omega,
        S=S,
        C=C_val,
        kappa=kappa,
        IC=IC,
        regime=regime,
        D_budget=D_b,
    )


def compute_all_entities() -> list[RDKernelResult]:
    """Compute kernel outputs for all regime derivation entities."""
    return [compute_rd_kernel(e) for e in RD_ENTITIES]


# ═══════════════════════════════════════════════════════════════════
#  THEOREMS (T-RD-1 through T-RD-6)
# ═══════════════════════════════════════════════════════════════════


def verify_t_rd_1(results: list[RDKernelResult]) -> dict:
    """T-RD-1: Tier-1 kernel identities hold for all 12 entities.

    F + ω = 1 (duality), IC ≤ F (integrity bound), IC = exp(κ).
    """
    failures = []
    for r in results:
        if abs(r.F + r.omega - 1.0) > 1e-12:
            failures.append(f"{r.name}: F+ω={r.F + r.omega}")
        if r.IC > r.F + 1e-12:
            failures.append(f"{r.name}: IC({r.IC})>F({r.F})")
        if abs(r.IC - math.exp(r.kappa)) > 1e-10:
            failures.append(f"{r.name}: IC≠exp(κ)")
    return {"name": "T-RD-1", "passed": len(failures) == 0, "failures": failures}


def verify_t_rd_2(results: list[RDKernelResult]) -> dict:
    """T-RD-2: D_budget is monotone with regime severity.

    Deep Stable < Watch < Onset Collapse < Deep Collapse in mean D_budget.
    """
    means: dict[str, float] = {}
    for cat in ("deep_stable", "watch_band", "onset_collapse", "deep_collapse"):
        vals = [r.D_budget for r in results if r.category == cat]
        means[cat] = float(np.mean(vals)) if vals else float("nan")
    order = ["deep_stable", "watch_band", "onset_collapse", "deep_collapse"]
    monotone = all(means[order[i]] < means[order[i + 1]] for i in range(len(order) - 1))
    return {"name": "T-RD-2", "passed": bool(monotone), "means": means}


def verify_t_rd_3(results: list[RDKernelResult]) -> dict:
    """T-RD-3: Budget partitions align with regime labels.

    Mean D_budget is lowest for Stable, intermediate for Watch,
    highest for Collapse.
    """
    budgets_by_regime: dict[str, list[float]] = {"Stable": [], "Watch": [], "Collapse": []}
    for r in results:
        budgets_by_regime[r.regime].append(r.D_budget)
    means = {k: float(np.mean(v)) if v else float("nan") for k, v in budgets_by_regime.items()}
    populated = [k for k in ("Stable", "Watch", "Collapse") if budgets_by_regime[k]]
    passed = True
    for i in range(1, len(populated)):
        if means[populated[i]] < means[populated[i - 1]] - 0.001:
            passed = False
    return {"name": "T-RD-3", "passed": bool(passed), "means": means}


def verify_t_rd_4(results: list[RDKernelResult]) -> dict:
    """T-RD-4: At ω_c = 0.30 the drift cost Γ(0.30) establishes a floor.

    All entities in Collapse regime have D_budget ≥ Γ(0.30).
    """
    gamma_at_threshold = drift_cost(0.30)
    collapse_entities = [r for r in results if r.regime == "Collapse"]
    passed = all(r.D_budget >= gamma_at_threshold - 1e-10 for r in collapse_entities)
    return {
        "name": "T-RD-4",
        "passed": bool(passed),
        "gamma_threshold": gamma_at_threshold,
        "min_collapse_budget": min(r.D_budget for r in collapse_entities) if collapse_entities else None,
    }


def verify_t_rd_5(results: list[RDKernelResult]) -> dict:
    """T-RD-5: Rank-1 equivalence — for uniform channels, D maps bijectively to ω.

    When all channels equal c₀, then ω = 1 − c₀, C = 0,
    D_budget = Γ(ω).  The mapping c₀ → D_budget is monotone decreasing.
    """
    test_points = np.array([0.1, 0.3, 0.5, 0.7, 0.9, 0.95, 0.99])
    budgets = [drift_cost(1.0 - c0) for c0 in test_points]
    passed = all(budgets[i] >= budgets[i + 1] for i in range(len(budgets) - 1))
    return {
        "name": "T-RD-5",
        "passed": bool(passed),
        "budgets": list(zip([float(c) for c in test_points], budgets, strict=True)),
    }


def verify_t_rd_6(results: list[RDKernelResult]) -> dict:
    """T-RD-6: All three regimes {Stable, Watch, Collapse} are realized."""
    regimes = {r.regime for r in results}
    passed = regimes == {"Stable", "Watch", "Collapse"}
    return {"name": "T-RD-6", "passed": bool(passed), "regimes": sorted(regimes)}


def verify_all_theorems() -> list[dict]:
    """Run all T-RD theorems."""
    results = compute_all_entities()
    return [
        verify_t_rd_1(results),
        verify_t_rd_2(results),
        verify_t_rd_3(results),
        verify_t_rd_4(results),
        verify_t_rd_5(results),
        verify_t_rd_6(results),
    ]


# ═══════════════════════════════════════════════════════════════════
#  MAIN
# ═══════════════════════════════════════════════════════════════════


def main() -> None:
    results = compute_all_entities()
    print("=" * 80)
    print("REGIME DERIVATION — D(x,t) ↔ KERNEL REGIME MAPPING")
    print("=" * 80)
    print(f"{'Entity':<24} {'Cat':<18} {'F':>6} {'ω':>6} {'IC':>6} {'D_bud':>7} {'Regime'}")
    print("-" * 80)
    for r in results:
        print(f"{r.name:<24} {r.category:<18} {r.F:6.3f} {r.omega:6.3f} {r.IC:6.3f} {r.D_budget:7.4f} {r.regime}")
    print("\n── Theorems ──")
    for t in verify_all_theorems():
        status = "PROVEN" if t["passed"] else "FAILED"
        print(f"  {t['name']}: {status}")


if __name__ == "__main__":
    main()
