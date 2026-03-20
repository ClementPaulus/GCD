"""Organizational Resilience Closure — Continuity Theory Domain.

Tier-2 closure mapping 12 organizational systems through the GCD kernel.
Each system is characterized by 8 channels drawn from resilience engineering
and organizational continuity research.

Channels (8, equal weights w_i = 1/8):
  0  adaptive_capacity       — ability to restructure under stress (1 = fully adaptive)
  1  redundancy              — backup systems and pathways (1 = fully redundant)
  2  resource_reserve        — buffer against disruption (1 = unlimited reserves)
  3  communication_integrity — information flow reliability (1 = perfect)
  4  leadership_continuity   — succession and decision persistence (1 = seamless)
  5  knowledge_retention     — institutional memory preservation (1 = perfect)
  6  response_speed          — time to react to disruption (1 = instant)
  7  external_independence   — independence from external systems (1 = fully independent)

12 entities across 4 categories:
  Agile (3): tech_startup, emergency_response, special_operations
  Institutional (3): central_bank, university, healthcare_system
  Distributed (3): open_source_project, cooperative_network, supply_chain
  Specialized (3): nuclear_plant, space_mission, submarine_crew

6 theorems (T-OR-1 through T-OR-6).
"""

from __future__ import annotations

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

OR_CHANNELS = [
    "adaptive_capacity",
    "redundancy",
    "resource_reserve",
    "communication_integrity",
    "leadership_continuity",
    "knowledge_retention",
    "response_speed",
    "external_independence",
]
N_OR_CHANNELS = len(OR_CHANNELS)


@dataclass(frozen=True, slots=True)
class OrganizationalEntity:
    """An organizational system with 8 measurable resilience channels."""

    name: str
    category: str
    adaptive_capacity: float
    redundancy: float
    resource_reserve: float
    communication_integrity: float
    leadership_continuity: float
    knowledge_retention: float
    response_speed: float
    external_independence: float

    def trace_vector(self) -> np.ndarray:
        return np.array(
            [
                self.adaptive_capacity,
                self.redundancy,
                self.resource_reserve,
                self.communication_integrity,
                self.leadership_continuity,
                self.knowledge_retention,
                self.response_speed,
                self.external_independence,
            ]
        )


OR_ENTITIES: tuple[OrganizationalEntity, ...] = (
    # Agile — high adaptivity and response speed, variable reserves
    OrganizationalEntity("tech_startup", "agile", 0.90, 0.15, 0.10, 0.65, 0.20, 0.25, 0.95, 0.60),
    OrganizationalEntity("emergency_response", "agile", 0.85, 0.70, 0.45, 0.90, 0.60, 0.55, 0.90, 0.75),
    OrganizationalEntity("special_operations", "agile", 0.80, 0.55, 0.35, 0.85, 0.65, 0.50, 0.85, 0.70),
    # Institutional — high knowledge retention, deep reserves, slow adaptation
    OrganizationalEntity("central_bank", "institutional", 0.30, 0.75, 0.90, 0.70, 0.85, 0.90, 0.25, 0.55),
    OrganizationalEntity("university", "institutional", 0.45, 0.50, 0.60, 0.55, 0.70, 0.95, 0.20, 0.40),
    OrganizationalEntity("healthcare_system", "institutional", 0.40, 0.80, 0.70, 0.75, 0.65, 0.80, 0.50, 0.35),
    # Distributed — low leadership continuity, high external independence
    OrganizationalEntity("open_source_project", "distributed", 0.75, 0.60, 0.30, 0.80, 0.15, 0.70, 0.60, 0.85),
    OrganizationalEntity("cooperative_network", "distributed", 0.65, 0.55, 0.40, 0.70, 0.25, 0.60, 0.50, 0.80),
    OrganizationalEntity("supply_chain", "distributed", 0.55, 0.65, 0.50, 0.85, 0.30, 0.45, 0.70, 0.40),
    # Specialized — high redundancy, safety-critical, low adaptivity
    OrganizationalEntity("nuclear_plant", "specialized", 0.20, 0.95, 0.85, 0.80, 0.75, 0.70, 0.30, 0.65),
    OrganizationalEntity("space_mission", "specialized", 0.25, 0.90, 0.70, 0.75, 0.80, 0.75, 0.40, 0.55),
    OrganizationalEntity("submarine_crew", "specialized", 0.35, 0.85, 0.55, 0.90, 0.70, 0.65, 0.50, 0.50),
)


@dataclass(frozen=True, slots=True)
class ORKernelResult:
    """Kernel output for an organizational entity."""

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
        return {
            "name": self.name,
            "category": self.category,
            "F": self.F,
            "omega": self.omega,
            "S": self.S,
            "C": self.C,
            "kappa": self.kappa,
            "IC": self.IC,
            "regime": self.regime,
        }


def compute_or_kernel(entity: OrganizationalEntity) -> ORKernelResult:
    """Compute GCD kernel for an organizational entity."""
    c = entity.trace_vector()
    c = np.clip(c, EPSILON, 1.0 - EPSILON)
    w = np.ones(N_OR_CHANNELS) / N_OR_CHANNELS
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
    return ORKernelResult(
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


def compute_all_entities() -> list[ORKernelResult]:
    """Compute kernel outputs for all organizational entities."""
    return [compute_or_kernel(e) for e in OR_ENTITIES]


# ── Theorems ──────────────────────────────────────────────────────────


def verify_t_or_1(results: list[ORKernelResult]) -> dict:
    """T-OR-1: Emergency response has highest F — optimized for rapid
    adaptation with moderate redundancy and strong communication.
    """
    er = next(r for r in results if r.name == "emergency_response")
    max_F = max(r.F for r in results)
    passed = abs(er.F - max_F) < 0.02
    return {"name": "T-OR-1", "passed": bool(passed), "er_F": er.F, "max_F": float(max_F)}


def verify_t_or_2(results: list[ORKernelResult]) -> dict:
    """T-OR-2: Specialized category has highest mean redundancy —
    safety-critical systems require extensive backup pathways.
    """
    cats = {e.category for e in OR_ENTITIES}
    cat_means = {}
    for cat in cats:
        vals = [e.redundancy for e in OR_ENTITIES if e.category == cat]
        cat_means[cat] = float(np.mean(vals))
    spec_mean = cat_means["specialized"]
    passed = all(spec_mean >= v - 1e-9 for v in cat_means.values())
    return {
        "name": "T-OR-2",
        "passed": bool(passed),
        "specialized_redundancy": spec_mean,
        "all_means": cat_means,
    }


def verify_t_or_3(results: list[ORKernelResult]) -> dict:
    """T-OR-3: Tech startup is in Collapse regime — high adaptivity/speed
    but near-zero reserves and redundancy push ω above threshold.
    """
    ts = next(r for r in results if r.name == "tech_startup")
    passed = ts.regime == "Collapse"
    return {"name": "T-OR-3", "passed": bool(passed), "startup_regime": ts.regime, "startup_omega": ts.omega}


def verify_t_or_4(results: list[ORKernelResult]) -> dict:
    """T-OR-4: Nuclear plant has largest heterogeneity gap among specialized —
    extreme redundancy paired with minimal adaptive capacity.
    """
    spec = [r for r in results if r.category == "specialized"]
    gaps = {r.name: r.F - r.IC for r in spec}
    nuc_gap = gaps["nuclear_plant"]
    passed = all(nuc_gap >= v - 1e-9 for v in gaps.values())
    return {
        "name": "T-OR-4",
        "passed": bool(passed),
        "nuclear_gap": float(nuc_gap),
        "specialized_gaps": {k: float(v) for k, v in gaps.items()},
    }


def verify_t_or_5(results: list[ORKernelResult]) -> dict:
    """T-OR-5: Institutional category has highest mean knowledge retention —
    universities, banks, and healthcare systems preserve institutional memory.
    """
    cats = {e.category for e in OR_ENTITIES}
    cat_means = {}
    for cat in cats:
        vals = [e.knowledge_retention for e in OR_ENTITIES if e.category == cat]
        cat_means[cat] = float(np.mean(vals))
    inst_mean = cat_means["institutional"]
    passed = all(inst_mean >= v - 1e-9 for v in cat_means.values())
    return {
        "name": "T-OR-5",
        "passed": bool(passed),
        "institutional_retention": inst_mean,
        "all_means": cat_means,
    }


def verify_t_or_6(results: list[ORKernelResult]) -> dict:
    """T-OR-6: Distributed category has lowest mean leadership continuity —
    open-source projects, cooperatives, and supply chains lack centralized
    succession mechanisms.
    """
    cats = {e.category for e in OR_ENTITIES}
    cat_means = {}
    for cat in cats:
        vals = [e.leadership_continuity for e in OR_ENTITIES if e.category == cat]
        cat_means[cat] = float(np.mean(vals))
    dist_mean = cat_means["distributed"]
    passed = all(dist_mean <= v + 1e-9 for v in cat_means.values())
    return {
        "name": "T-OR-6",
        "passed": bool(passed),
        "distributed_leadership": dist_mean,
        "all_means": cat_means,
    }


def verify_all_theorems() -> list[dict]:
    """Run all T-OR theorems."""
    results = compute_all_entities()
    return [
        verify_t_or_1(results),
        verify_t_or_2(results),
        verify_t_or_3(results),
        verify_t_or_4(results),
        verify_t_or_5(results),
        verify_t_or_6(results),
    ]


def main() -> None:
    """Entry point."""
    results = compute_all_entities()
    print("=" * 78)
    print("ORGANIZATIONAL RESILIENCE — GCD KERNEL ANALYSIS")
    print("=" * 78)
    print(f"{'Entity':<28} {'Cat':<14} {'F':>6} {'ω':>6} {'IC':>6} {'Δ':>6} {'Regime'}")
    print("-" * 78)
    for r in results:
        gap = r.F - r.IC
        print(f"{r.name:<28} {r.category:<14} {r.F:6.3f} {r.omega:6.3f} {r.IC:6.3f} {gap:6.3f} {r.regime}")

    print("\n── Theorems ──")
    for t in verify_all_theorems():
        print(f"  {t['name']}: {'PROVEN' if t['passed'] else 'FAILED'}")


if __name__ == "__main__":
    main()
