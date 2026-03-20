"""Developmental Neuroscience Closure — Clinical Neuroscience Domain.

Tier-2 closure mapping 12 brain developmental stages through the GCD kernel.
Each stage is characterized by 8 channels drawn from developmental neurobiology
and lifespan neuroscience research.

Channels (8, equal weights w_i = 1/8):
  0  synaptic_density        — synapse count per unit volume (1 = peak density)
  1  myelination             — degree of axonal myelination (1 = fully myelinated)
  2  cortical_thickness      — gray matter volume (1 = maximal)
  3  neurotransmitter_balance— homeostatic balance of NT systems (1 = perfectly balanced)
  4  plasticity              — capacity for structural/functional change (1 = maximally plastic)
  5  connectivity            — inter-regional network integration (1 = fully connected)
  6  metabolic_efficiency    — glucose usage efficiency (1 = maximally efficient)
  7  pruning_completion      — synaptic pruning progress (1 = optimally pruned)

12 entities across 4 categories:
  Prenatal (3): neural_tube_stage, fetal_neurogenesis, third_trimester_wiring
  Childhood (3): infant_synaptogenesis, toddler_myelination, school_age_integration
  Adolescent (3): puberty_pruning, prefrontal_maturation, adolescent_connectivity
  Aging (3): middle_age_maintenance, early_senescence, late_neurodegeneration

6 theorems (T-DN-1 through T-DN-6).
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

DN_CHANNELS = [
    "synaptic_density",
    "myelination",
    "cortical_thickness",
    "neurotransmitter_balance",
    "plasticity",
    "connectivity",
    "metabolic_efficiency",
    "pruning_completion",
]
N_DN_CHANNELS = len(DN_CHANNELS)


@dataclass(frozen=True, slots=True)
class DevelopmentalEntity:
    """A brain developmental stage with 8 measurable channels."""

    name: str
    category: str
    synaptic_density: float
    myelination: float
    cortical_thickness: float
    neurotransmitter_balance: float
    plasticity: float
    connectivity: float
    metabolic_efficiency: float
    pruning_completion: float

    def trace_vector(self) -> np.ndarray:
        return np.array(
            [
                self.synaptic_density,
                self.myelination,
                self.cortical_thickness,
                self.neurotransmitter_balance,
                self.plasticity,
                self.connectivity,
                self.metabolic_efficiency,
                self.pruning_completion,
            ]
        )


DN_ENTITIES: tuple[DevelopmentalEntity, ...] = (
    # Prenatal — high plasticity, minimal myelination and pruning
    DevelopmentalEntity("neural_tube_stage", "prenatal", 0.10, 0.05, 0.15, 0.30, 0.85, 0.10, 0.20, 0.05),
    DevelopmentalEntity("fetal_neurogenesis", "prenatal", 0.55, 0.10, 0.50, 0.40, 0.90, 0.20, 0.35, 0.10),
    DevelopmentalEntity("third_trimester_wiring", "prenatal", 0.70, 0.20, 0.65, 0.50, 0.80, 0.35, 0.45, 0.15),
    # Childhood — peak synaptic density, increasing myelination
    DevelopmentalEntity("infant_synaptogenesis", "childhood", 0.95, 0.30, 0.80, 0.55, 0.95, 0.40, 0.50, 0.20),
    DevelopmentalEntity("toddler_myelination", "childhood", 0.80, 0.55, 0.85, 0.60, 0.75, 0.55, 0.60, 0.35),
    DevelopmentalEntity("school_age_integration", "childhood", 0.70, 0.70, 0.80, 0.75, 0.65, 0.75, 0.75, 0.55),
    # Adolescent — active pruning, maturing prefrontal connectivity
    DevelopmentalEntity("puberty_pruning", "adolescent", 0.55, 0.65, 0.70, 0.50, 0.55, 0.60, 0.55, 0.60),
    DevelopmentalEntity("prefrontal_maturation", "adolescent", 0.45, 0.80, 0.65, 0.65, 0.50, 0.70, 0.65, 0.70),
    DevelopmentalEntity("adolescent_connectivity", "adolescent", 0.50, 0.75, 0.60, 0.60, 0.45, 0.80, 0.60, 0.65),
    # Aging — declining plasticity and density, maintained myelination
    DevelopmentalEntity("middle_age_maintenance", "aging", 0.55, 0.85, 0.55, 0.70, 0.30, 0.85, 0.75, 0.85),
    DevelopmentalEntity("early_senescence", "aging", 0.40, 0.70, 0.45, 0.55, 0.20, 0.70, 0.55, 0.80),
    DevelopmentalEntity("late_neurodegeneration", "aging", 0.20, 0.45, 0.25, 0.30, 0.10, 0.40, 0.30, 0.75),
)


@dataclass(frozen=True, slots=True)
class DNKernelResult:
    """Kernel output for a developmental neuroscience entity."""

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


def compute_dn_kernel(entity: DevelopmentalEntity) -> DNKernelResult:
    """Compute GCD kernel for a developmental neuroscience entity."""
    c = entity.trace_vector()
    c = np.clip(c, EPSILON, 1.0 - EPSILON)
    w = np.ones(N_DN_CHANNELS) / N_DN_CHANNELS
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
    return DNKernelResult(
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


def compute_all_entities() -> list[DNKernelResult]:
    """Compute kernel outputs for all developmental neuroscience entities."""
    return [compute_dn_kernel(e) for e in DN_ENTITIES]


# ── Theorems ──────────────────────────────────────────────────────────


def verify_t_dn_1(results: list[DNKernelResult]) -> dict:
    """T-DN-1: School-age integration has highest F — balanced across all
    channels as myelination advances and connectivity matures while
    synaptic density and plasticity remain high.
    """
    school = next(r for r in results if r.name == "school_age_integration")
    max_F = max(r.F for r in results)
    passed = abs(school.F - max_F) < 0.02
    return {"name": "T-DN-1", "passed": bool(passed), "school_F": school.F, "max_F": float(max_F)}


def verify_t_dn_2(results: list[DNKernelResult]) -> dict:
    """T-DN-2: Prenatal category has lowest mean myelination —
    myelination is primarily a postnatal process.
    """
    cats = {e.category for e in DN_ENTITIES}
    cat_means = {}
    for cat in cats:
        vals = [e.myelination for e in DN_ENTITIES if e.category == cat]
        cat_means[cat] = float(np.mean(vals))
    pre_mean = cat_means["prenatal"]
    passed = all(pre_mean <= v + 1e-9 for v in cat_means.values())
    return {
        "name": "T-DN-2",
        "passed": bool(passed),
        "prenatal_myelination": pre_mean,
        "all_means": cat_means,
    }


def verify_t_dn_3(results: list[DNKernelResult]) -> dict:
    """T-DN-3: Infant synaptogenesis has highest plasticity — the peak
    of experience-dependent synaptic formation.
    """
    infant = next(e for e in DN_ENTITIES if e.name == "infant_synaptogenesis")
    max_plast = max(e.plasticity for e in DN_ENTITIES)
    passed = abs(infant.plasticity - max_plast) < 0.01
    return {
        "name": "T-DN-3",
        "passed": bool(passed),
        "infant_plasticity": infant.plasticity,
        "max_plasticity": float(max_plast),
    }


def verify_t_dn_4(results: list[DNKernelResult]) -> dict:
    """T-DN-4: Late neurodegeneration is in Collapse regime — multiple
    channels simultaneously degraded (density, thickness, plasticity,
    connectivity, metabolic efficiency).
    """
    late = next(r for r in results if r.name == "late_neurodegeneration")
    passed = late.regime == "Collapse"
    return {"name": "T-DN-4", "passed": bool(passed), "late_regime": late.regime, "late_omega": late.omega}


def verify_t_dn_5(results: list[DNKernelResult]) -> dict:
    """T-DN-5: Prenatal category has largest mean heterogeneity gap —
    extreme plasticity paired with minimal myelination and connectivity
    creates maximal channel divergence.
    """
    cats = {r.category for r in results}
    cat_gaps = {}
    for cat in cats:
        gaps = [r.F - r.IC for r in results if r.category == cat]
        cat_gaps[cat] = float(np.mean(gaps))
    pre_gap = cat_gaps["prenatal"]
    passed = all(pre_gap >= v - 1e-9 for v in cat_gaps.values())
    return {
        "name": "T-DN-5",
        "passed": bool(passed),
        "prenatal_gap": pre_gap,
        "all_gaps": cat_gaps,
    }


def verify_t_dn_6(results: list[DNKernelResult]) -> dict:
    """T-DN-6: Adolescent connectivity has highest connectivity among
    developing stages (prenatal + childhood + adolescent) — network
    integration peaks in late adolescence.
    """
    developing = [e for e in DN_ENTITIES if e.category in ("prenatal", "childhood", "adolescent")]
    adol = next(e for e in developing if e.name == "adolescent_connectivity")
    max_conn = max(e.connectivity for e in developing)
    passed = abs(adol.connectivity - max_conn) < 0.01
    return {
        "name": "T-DN-6",
        "passed": bool(passed),
        "adol_connectivity": adol.connectivity,
        "developing_max": float(max_conn),
    }


def verify_all_theorems() -> list[dict]:
    """Run all T-DN theorems."""
    results = compute_all_entities()
    return [
        verify_t_dn_1(results),
        verify_t_dn_2(results),
        verify_t_dn_3(results),
        verify_t_dn_4(results),
        verify_t_dn_5(results),
        verify_t_dn_6(results),
    ]


def main() -> None:
    """Entry point."""
    results = compute_all_entities()
    print("=" * 78)
    print("DEVELOPMENTAL NEUROSCIENCE — GCD KERNEL ANALYSIS")
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
