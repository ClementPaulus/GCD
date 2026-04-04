"""Three-Agent Epistemic Model — RCFT Information Geometry (RCFT.INTSTACK.v1).

CATALOGUE TAGS:  T-EA-1 through T-EA-6
TIER:            2 (Expansion — RCFT domain)
DEPENDS ON:      Tier-1 identities (F + ω = 1, IC ≤ F, IC = exp(κ))
                 Information geometry T17-T19 (Fisher geodesic, Fano-Fisher)
                 Epistemic coherence (T-EC-1..7)
                 DOI: 10.5281/zenodo.16526052 (Three-Agent Model)

Formalizes the Three-Agent epistemic model from information_geometry.py:
  Agent 1 (Present/Measuring) → ω = drift (the act of observation)
  Agent 2 (Retained/Archive)  → F = fidelity (what survives)
  Agent 3 (Unknown/Horizon)   → Γ(ω) = cost of crossing into the unknown

Each entity represents a knowledge-state scenario where the three agents
have different relative strengths, and the kernel evaluates the resulting
epistemic coherence.

Channels (8, equal weights w_i = 1/8):
  0  measurement_fidelity   — Agent 1: precision of present observation
  1  archive_integrity      — Agent 2: reliability of retained knowledge
  2  horizon_accessibility  — Agent 3: how reachable the unknown is
  3  inter_agent_coherence  — agreement between agents
  4  geodesic_efficiency    — η: how close to optimal the transition is
  5  epistemic_return       — demonstrated return from unknown to measured
  6  derivation_depth       — length of traceable derivation chain
  7  falsifiability         — capacity for empirical refutation

12 entities across 4 epistemic categories:
  High coherence (3): proven_theorem, empirical_law, calibrated_model
  Moderate coherence (3): working_hypothesis, expert_judgment, historical_pattern
  Low coherence (3): ungrounded_assertion, folk_wisdom, ideological_claim
  Degenerate (3): pure_dogma, pure_measurement, pure_speculation

6 theorems (T-EA-1 through T-EA-6).
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

from umcp.frozen_contract import EPSILON  # noqa: E402
from umcp.kernel_optimized import compute_kernel_outputs  # noqa: E402

EA_CHANNELS = [
    "measurement_fidelity",
    "archive_integrity",
    "horizon_accessibility",
    "inter_agent_coherence",
    "geodesic_efficiency",
    "epistemic_return",
    "derivation_depth",
    "falsifiability",
]
N_EA_CHANNELS = len(EA_CHANNELS)


@dataclass(frozen=True, slots=True)
class EpistemicAgentEntity:
    """A knowledge-state scenario with 8 epistemic channels."""

    name: str
    category: str
    measurement_fidelity: float
    archive_integrity: float
    horizon_accessibility: float
    inter_agent_coherence: float
    geodesic_efficiency: float
    epistemic_return: float
    derivation_depth: float
    falsifiability: float

    def trace_vector(self) -> np.ndarray:
        return np.array(
            [
                self.measurement_fidelity,
                self.archive_integrity,
                self.horizon_accessibility,
                self.inter_agent_coherence,
                self.geodesic_efficiency,
                self.epistemic_return,
                self.derivation_depth,
                self.falsifiability,
            ]
        )


# ═══════════════════════════════════════════════════════════════════
#  ENTITY CATALOG — 12 epistemic scenarios
# ═══════════════════════════════════════════════════════════════════

EA_ENTITIES: tuple[EpistemicAgentEntity, ...] = (
    # ── High coherence (all three agents strong) ──
    EpistemicAgentEntity("proven_theorem", "high_coherence", 0.95, 0.98, 0.85, 0.92, 0.90, 0.95, 0.98, 0.70),
    EpistemicAgentEntity("empirical_law", "high_coherence", 0.92, 0.90, 0.80, 0.88, 0.85, 0.90, 0.80, 0.95),
    EpistemicAgentEntity("calibrated_model", "high_coherence", 0.88, 0.85, 0.82, 0.85, 0.82, 0.88, 0.85, 0.85),
    # ── Moderate coherence (agents partly aligned) ──
    EpistemicAgentEntity("working_hypothesis", "moderate_coherence", 0.75, 0.70, 0.65, 0.60, 0.55, 0.72, 0.60, 0.80),
    EpistemicAgentEntity("expert_judgment", "moderate_coherence", 0.80, 0.75, 0.50, 0.65, 0.60, 0.70, 0.55, 0.60),
    EpistemicAgentEntity("historical_pattern", "moderate_coherence", 0.60, 0.82, 0.55, 0.58, 0.50, 0.65, 0.70, 0.55),
    # ── Low coherence (agents poorly aligned) ──
    EpistemicAgentEntity("ungrounded_assertion", "low_coherence", 0.40, 0.30, 0.35, 0.25, 0.20, 0.15, 0.10, 0.50),
    EpistemicAgentEntity("folk_wisdom", "low_coherence", 0.50, 0.60, 0.20, 0.35, 0.15, 0.30, 0.05, 0.15),
    EpistemicAgentEntity("ideological_claim", "low_coherence", 0.55, 0.65, 0.10, 0.30, 0.10, 0.20, 0.08, 0.05),
    # ── Degenerate (one agent dominates, others near ε — geometric slaughter) ──
    EpistemicAgentEntity("pure_dogma", "degenerate", 0.10, 0.95, 0.05, 0.15, 0.05, 0.08, 0.02, 0.01),
    EpistemicAgentEntity("pure_measurement", "degenerate", 0.99, 0.10, 0.08, 0.12, 0.05, 0.10, 0.05, 0.03),
    EpistemicAgentEntity("pure_speculation", "degenerate", 0.05, 0.05, 0.95, 0.10, 0.08, 0.05, 0.03, 0.02),
)


@dataclass(frozen=True, slots=True)
class EAKernelResult:
    """Kernel output for an epistemic agent entity."""

    name: str
    category: str
    F: float
    omega: float
    S: float
    C: float
    kappa: float
    IC: float
    regime: str

    def to_dict(self) -> dict:
        return {k: getattr(self, k) for k in self.__dataclass_fields__}


def compute_ea_kernel(entity: EpistemicAgentEntity) -> EAKernelResult:
    """Compute GCD kernel for an epistemic agent entity."""
    c = entity.trace_vector()
    c = np.clip(c, EPSILON, 1.0 - EPSILON)
    w = np.ones(N_EA_CHANNELS) / N_EA_CHANNELS
    result = compute_kernel_outputs(c, w)
    F = float(result["F"])
    omega = float(result["omega"])
    S = float(result["S"])
    C_val = float(result["C"])
    kappa = float(result["kappa"])
    IC = float(result["IC"])
    if omega >= 0.30:
        regime = "Collapse"
    elif omega < 0.038 and F > 0.90 and S < 0.15 and C_val < 0.14:
        regime = "Stable"
    else:
        regime = "Watch"
    return EAKernelResult(
        name=entity.name,
        category=entity.category,
        F=F,
        omega=omega,
        S=S,
        C=C_val,
        kappa=kappa,
        IC=IC,
        regime=regime,
    )


def compute_all_entities() -> list[EAKernelResult]:
    """Compute kernel outputs for all epistemic agent entities."""
    return [compute_ea_kernel(e) for e in EA_ENTITIES]


# ═══════════════════════════════════════════════════════════════════
#  THEOREMS (T-EA-1 through T-EA-6)
# ═══════════════════════════════════════════════════════════════════


def verify_t_ea_1(results: list[EAKernelResult]) -> dict:
    """T-EA-1: Tier-1 kernel identities hold for all 12 entities.

    F + ω = 1, IC ≤ F, IC = exp(κ).
    """
    failures = []
    for r in results:
        if abs(r.F + r.omega - 1.0) > 1e-12:
            failures.append(f"{r.name}: F+ω={r.F + r.omega}")
        if r.IC > r.F + 1e-12:
            failures.append(f"{r.name}: IC>F")
        if abs(r.IC - math.exp(r.kappa)) > 1e-10:
            failures.append(f"{r.name}: IC≠exp(κ)")
    return {"name": "T-EA-1", "passed": len(failures) == 0, "failures": failures}


def verify_t_ea_2(results: list[EAKernelResult]) -> dict:
    """T-EA-2: High-coherence entities have highest mean F.

    When all three agents are strong, fidelity is maximized.
    """
    cats = {}
    for r in results:
        cats.setdefault(r.category, []).append(r.F)
    means = {k: float(np.mean(v)) for k, v in cats.items()}
    high_mean = means.get("high_coherence", 0.0)
    passed = all(high_mean >= v - 0.001 for v in means.values())
    return {"name": "T-EA-2", "passed": bool(passed), "means": means}


def verify_t_ea_3(results: list[EAKernelResult]) -> dict:
    """T-EA-3: Degenerate entities have largest heterogeneity gap.

    When one agent dominates and others are near ε, geometric slaughter
    destroys IC while F remains moderate → large Δ = F − IC.
    """
    cats = {}
    for r in results:
        cats.setdefault(r.category, []).append(r.F - r.IC)
    means = {k: float(np.mean(v)) for k, v in cats.items()}
    degen_gap = means.get("degenerate", 0.0)
    passed = all(degen_gap >= v - 0.01 for v in means.values())
    return {"name": "T-EA-3", "passed": bool(passed), "means": means}


def verify_t_ea_4(results: list[EAKernelResult]) -> dict:
    """T-EA-4: proven_theorem achieves highest IC among all entities.

    Balanced high channels yield strong multiplicative coherence.
    """
    pt = next(r for r in results if r.name == "proven_theorem")
    max_IC = max(r.IC for r in results)
    passed = abs(pt.IC - max_IC) < 0.02
    return {"name": "T-EA-4", "passed": bool(passed), "proven_IC": pt.IC, "max_IC": float(max_IC)}


def verify_t_ea_5(results: list[EAKernelResult]) -> dict:
    """T-EA-5: pure_dogma has lowest IC — dead falsifiability channel.

    A knowledge system with zero falsifiability has IC near ε regardless
    of archive strength, demonstrating geometric slaughter of epistemic
    coherence.
    """
    pd = next(r for r in results if r.name == "pure_dogma")
    min_IC = min(r.IC for r in results)
    passed = abs(pd.IC - min_IC) < 0.02
    return {"name": "T-EA-5", "passed": bool(passed), "dogma_IC": pd.IC, "min_IC": float(min_IC)}


def verify_t_ea_6(results: list[EAKernelResult]) -> dict:
    """T-EA-6: High-coherence entities are Watch, degenerate are Collapse.

    The regime classification structurally separates well-formed
    knowledge (Watch — not Stable because 12.5% rarity) from
    degenerate knowledge (Collapse — one dead channel kills coherence).
    """
    high = [r for r in results if r.category == "high_coherence"]
    degen = [r for r in results if r.category == "degenerate"]
    high_watch = all(r.regime == "Watch" for r in high)
    degen_collapse = all(r.regime == "Collapse" for r in degen)
    passed = high_watch and degen_collapse
    return {
        "name": "T-EA-6",
        "passed": bool(passed),
        "high_regimes": [r.regime for r in high],
        "degen_regimes": [r.regime for r in degen],
    }


def verify_all_theorems() -> list[dict]:
    """Run all T-EA theorems."""
    results = compute_all_entities()
    return [
        verify_t_ea_1(results),
        verify_t_ea_2(results),
        verify_t_ea_3(results),
        verify_t_ea_4(results),
        verify_t_ea_5(results),
        verify_t_ea_6(results),
    ]


def main() -> None:
    results = compute_all_entities()
    print("=" * 78)
    print("THREE-AGENT EPISTEMIC MODEL — KNOWLEDGE STATE KERNEL ANALYSIS")
    print("=" * 78)
    print(f"{'Entity':<24} {'Cat':<20} {'F':>6} {'ω':>6} {'IC':>6} {'Δ':>6} {'Regime'}")
    print("-" * 78)
    for r in results:
        gap = r.F - r.IC
        print(f"{r.name:<24} {r.category:<20} {r.F:6.3f} {r.omega:6.3f} {r.IC:6.3f} {gap:6.3f} {r.regime}")
    print("\n── Theorems ──")
    for t in verify_all_theorems():
        print(f"  {t['name']}: {'PROVEN' if t['passed'] else 'FAILED'}")


if __name__ == "__main__":
    main()
