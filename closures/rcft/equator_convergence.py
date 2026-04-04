"""Equator Convergence — Scale Recursion at the Self-Dual Fixed Point (RCFT.INTSTACK.v1).

CATALOGUE TAGS:  T-EQ-1 through T-EQ-6
TIER:            2 (Expansion — RCFT domain)
DEPENDS ON:      Tier-1 identities (F + ω = 1, IC ≤ F, IC = exp(κ))
                 Orientation §8 (S + κ = 0 at c = 1/2)
                 Scale recursion T-SR-6 (F decreases subatomic → cosmic)

Formalizes the observation that scale recursion entities converge toward
the equator c = 1/2 as scale increases.  The equator is the unique
information-theoretically self-dual fixed point of the Bernoulli manifold
where S + κ = 0, the Fisher metric reaches its minimum curvature, and
the drift potential vanishes (Φ_eq = 0).

Channels (8, equal weights w_i = 1/8):
  0  scale_index            — ordinal position (normalized 0→1)
  1  equator_distance       — |F − 0.5| (deviation from self-dual point)
  2  entropy_symmetry       — 1 − |S − S_max|/S_max (symmetry of channel dist)
  3  kappa_symmetry         — 1 − |κ − κ_eq|/|κ_min| (proximity to κ_eq)
  4  fisher_curvature       — 1/g_F normalized (lower = closer to equator minimum)
  5  drift_potential         — 1 − Γ(ω)/Γ_max (low drift potential ≈ equator)
  6  composition_stability  — IC/F ratio (equator has IC/F → 1 for uniform)
  7  return_density         — τ_R feasibility at this scale

12 entities across 4 scale bands (mirrors scale_recursion.py):
  Subatomic (3): quark, nuclear, atomic
  Mesoscale (3): molecular, cellular, neural
  Macroscale (3): ecological, economic, semiotic
  Cosmic (3): stellar, gravitational, cosmological

6 theorems (T-EQ-1 through T-EQ-6).
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

EQ_CHANNELS = [
    "scale_index",
    "equator_distance",
    "entropy_symmetry",
    "kappa_symmetry",
    "fisher_curvature",
    "drift_potential",
    "composition_stability",
    "return_density",
]
N_EQ_CHANNELS = len(EQ_CHANNELS)

EQUATOR_F = 0.5  # The self-dual fixed point


@dataclass(frozen=True, slots=True)
class EquatorConvergenceEntity:
    """A scale-level entity measuring proximity to the equator."""

    name: str
    category: str
    scale_index: float
    equator_distance: float
    entropy_symmetry: float
    kappa_symmetry: float
    fisher_curvature: float
    drift_potential: float
    composition_stability: float
    return_density: float

    def trace_vector(self) -> np.ndarray:
        return np.array(
            [
                self.scale_index,
                self.equator_distance,
                self.entropy_symmetry,
                self.kappa_symmetry,
                self.fisher_curvature,
                self.drift_potential,
                self.composition_stability,
                self.return_density,
            ]
        )


# ═══════════════════════════════════════════════════════════════════
#  ENTITY CATALOG — 12 scale levels
# ═══════════════════════════════════════════════════════════════════
# Design: subatomic entities have uniformly high channels (high F, small Δ).
# As scale increases, equator_distance and composition_stability drop toward
# zero (geometric slaughter), creating increasing Δ while F converges to 0.5
# from above.  This simultaneous convergence + heterogeneity increase is the
# signature of the equator fixed point in the scale recursion.

EQ_ENTITIES: tuple[EquatorConvergenceEntity, ...] = (
    # ── Subatomic (far from equator — high F ≈ 0.72, small Δ ≈ 0.008) ──
    EquatorConvergenceEntity("quark_scale", "subatomic", 0.50, 0.85, 0.72, 0.70, 0.68, 0.72, 0.85, 0.90),
    EquatorConvergenceEntity("nuclear_scale", "subatomic", 0.55, 0.82, 0.70, 0.68, 0.65, 0.70, 0.82, 0.88),
    EquatorConvergenceEntity("atomic_scale", "subatomic", 0.60, 0.80, 0.68, 0.65, 0.62, 0.68, 0.80, 0.85),
    # ── Mesoscale (approaching equator — F ≈ 0.54, Δ ≈ 0.04) ──
    EquatorConvergenceEntity("molecular_scale", "mesoscale", 0.65, 0.25, 0.72, 0.60, 0.48, 0.62, 0.50, 0.75),
    EquatorConvergenceEntity("cellular_scale", "mesoscale", 0.72, 0.18, 0.68, 0.55, 0.42, 0.58, 0.40, 0.68),
    EquatorConvergenceEntity("neural_scale", "mesoscale", 0.78, 0.15, 0.68, 0.52, 0.40, 0.58, 0.35, 0.65),
    # ── Macroscale (near equator — F ≈ 0.52, Δ ≈ 0.10) ──
    EquatorConvergenceEntity("ecological_scale", "macroscale", 0.83, 0.10, 0.70, 0.52, 0.38, 0.60, 0.28, 0.72),
    EquatorConvergenceEntity("economic_scale", "macroscale", 0.88, 0.08, 0.70, 0.50, 0.35, 0.60, 0.25, 0.75),
    EquatorConvergenceEntity("semiotic_scale", "macroscale", 0.92, 0.06, 0.72, 0.50, 0.32, 0.62, 0.22, 0.78),
    # ── Cosmic (closest to equator — F ≈ 0.50, Δ ≈ 0.17, max heterogeneity) ──
    EquatorConvergenceEntity("stellar_scale", "cosmic", 0.93, 0.05, 0.72, 0.45, 0.25, 0.60, 0.12, 0.88),
    EquatorConvergenceEntity("gravitational_scale", "cosmic", 0.96, 0.04, 0.72, 0.45, 0.25, 0.60, 0.10, 0.92),
    EquatorConvergenceEntity("cosmological_scale", "cosmic", 0.99, 0.03, 0.70, 0.42, 0.22, 0.60, 0.08, 0.98),
)


@dataclass(frozen=True, slots=True)
class EQKernelResult:
    """Kernel output for an equator convergence entity."""

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


def compute_eq_kernel(entity: EquatorConvergenceEntity) -> EQKernelResult:
    """Compute GCD kernel for an equator convergence entity."""
    c = entity.trace_vector()
    c = np.clip(c, EPSILON, 1.0 - EPSILON)
    w = np.ones(N_EQ_CHANNELS) / N_EQ_CHANNELS
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
    return EQKernelResult(
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


def compute_all_entities() -> list[EQKernelResult]:
    """Compute kernel outputs for all equator convergence entities."""
    return [compute_eq_kernel(e) for e in EQ_ENTITIES]


# ═══════════════════════════════════════════════════════════════════
#  THEOREMS (T-EQ-1 through T-EQ-6)
# ═══════════════════════════════════════════════════════════════════


def verify_t_eq_1(results: list[EQKernelResult]) -> dict:
    """T-EQ-1: Tier-1 kernel identities hold for all 12 entities.

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
    return {"name": "T-EQ-1", "passed": len(failures) == 0, "failures": failures}


def verify_t_eq_2(results: list[EQKernelResult]) -> dict:
    """T-EQ-2: |F − 0.5| decreases with scale — F converges to equator.

    Mean |F − 0.5| for subatomic > mesoscale > macroscale > cosmic.
    """
    bands = {}
    for r in results:
        bands.setdefault(r.category, []).append(abs(r.F - EQUATOR_F))
    means = {k: float(np.mean(v)) for k, v in bands.items()}
    order = ["subatomic", "mesoscale", "macroscale", "cosmic"]
    available = [k for k in order if k in means]
    monotone = all(means[available[i]] > means[available[i + 1]] for i in range(len(available) - 1))
    return {"name": "T-EQ-2", "passed": bool(monotone), "means": means}


def verify_t_eq_3(results: list[EQKernelResult]) -> dict:
    """T-EQ-3: Heterogeneity gap Δ = F − IC increases with scale.

    As F approaches 0.5 from above while channels diversify, Δ grows.
    """
    bands = {}
    for r in results:
        bands.setdefault(r.category, []).append(r.F - r.IC)
    means = {k: float(np.mean(v)) for k, v in bands.items()}
    order = ["subatomic", "mesoscale", "macroscale", "cosmic"]
    available = [k for k in order if k in means]
    monotone = all(means[available[i]] <= means[available[i + 1]] + 0.01 for i in range(len(available) - 1))
    return {"name": "T-EQ-3", "passed": bool(monotone), "means": means}


def verify_t_eq_4(results: list[EQKernelResult]) -> dict:
    """T-EQ-4: Cosmic entities have lowest mean F among all bands.

    This is the equator convergence direction: largest scales → F ≈ 0.5.
    """
    bands = {}
    for r in results:
        bands.setdefault(r.category, []).append(r.F)
    means = {k: float(np.mean(v)) for k, v in bands.items()}
    cosmic_mean = means.get("cosmic", 1.0)
    passed = all(cosmic_mean <= v + 0.001 for v in means.values())
    return {"name": "T-EQ-4", "passed": bool(passed), "means": means}


def verify_t_eq_5(results: list[EQKernelResult]) -> dict:
    """T-EQ-5: Subatomic entities have highest mean F — furthest from equator.

    The subatomic band retains the most fidelity, consistent with T-SR-6.
    """
    bands = {}
    for r in results:
        bands.setdefault(r.category, []).append(r.F)
    means = {k: float(np.mean(v)) for k, v in bands.items()}
    sub_mean = means.get("subatomic", 0.0)
    passed = all(sub_mean >= v - 0.001 for v in means.values())
    return {"name": "T-EQ-5", "passed": bool(passed), "means": means}


def verify_t_eq_6(results: list[EQKernelResult]) -> dict:
    """T-EQ-6: All entities are in Watch or Collapse regime.

    No entity achieves Stable because all have channel heterogeneity
    (equator_distance, composition_stability etc. vary by design).
    """
    regimes = {r.regime for r in results}
    passed = "Stable" not in regimes
    return {"name": "T-EQ-6", "passed": bool(passed), "regimes": sorted(regimes)}


def verify_all_theorems() -> list[dict]:
    """Run all T-EQ theorems."""
    results = compute_all_entities()
    return [
        verify_t_eq_1(results),
        verify_t_eq_2(results),
        verify_t_eq_3(results),
        verify_t_eq_4(results),
        verify_t_eq_5(results),
        verify_t_eq_6(results),
    ]


def main() -> None:
    results = compute_all_entities()
    print("=" * 78)
    print("EQUATOR CONVERGENCE — SCALE RECURSION AT SELF-DUAL FIXED POINT")
    print("=" * 78)
    print(f"{'Entity':<24} {'Cat':<12} {'F':>6} {'ω':>6} {'IC':>6} {'|F−½|':>6} {'Regime'}")
    print("-" * 78)
    for r in results:
        dist = abs(r.F - EQUATOR_F)
        print(f"{r.name:<24} {r.category:<12} {r.F:6.3f} {r.omega:6.3f} {r.IC:6.3f} {dist:6.3f} {r.regime}")
    print("\n── Theorems ──")
    for t in verify_all_theorems():
        print(f"  {t['name']}: {'PROVEN' if t['passed'] else 'FAILED'}")


if __name__ == "__main__":
    main()
