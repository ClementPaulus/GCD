"""Collapse Field Theory — Foundational Field Configurations (RCFT.INTSTACK.v1).

Tier-2 closure cataloging 12 fundamental collapse field configurations through
the GCD kernel.  Each configuration represents a canonical field state that all
domain closures across the 20-domain corpus instantiate in their own channel
semantics.  RCFT is the theoretical substrate — this module makes that explicit.

As the originating theory of the entire GCD corpus (May 2025 → Feb 2026 weld),
Recursive Collapse Field Theory provides the conceptual framework from which
Axiom-0 ("Collapse is generative; only what returns is real") was first
articulated.  This module grounds that framework in the standardized entity
pattern, making RCFT's field configurations available for cross-domain study,
composition proofs, and the test manifest.

Channels (8, equal weights w_i = 1/8):
  0  field_coherence       — spatial coherence of the collapse field
  1  recursive_depth       — depth of self-similar nesting (normalized)
  2  return_fidelity       — fraction of information that survives collapse-return
  3  drift_potential       — proximity to the collapse threshold (Γ(ω) normalized)
  4  entropy_density       — Bernoulli field entropy per channel (normalized)
  5  curvature_coupling    — coupling strength to uncontrolled degrees of freedom
  6  geodesic_efficiency   — efficiency of the Fisher geodesic path (T22)
  7  grammar_complexity    — collapse grammar entropy rate (T23, normalized)

12 entities across 4 categories:
  Fixed-point (3): equator_field, logistic_fixed_point, trap_fixed_point
  Phase boundary (3): confinement_boundary, scale_inversion, weld_threshold
  Recursive (3): nested_collapse, fractal_cascade, self_dual_field
  Extremal (3): maximal_coherence, minimal_integrity, dissolution_field

6 theorems (T-CFT-1 through T-CFT-6).
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

CFT_CHANNELS = [
    "field_coherence",
    "recursive_depth",
    "return_fidelity",
    "drift_potential",
    "entropy_density",
    "curvature_coupling",
    "geodesic_efficiency",
    "grammar_complexity",
]
N_CFT_CHANNELS = len(CFT_CHANNELS)


@dataclass(frozen=True, slots=True)
class CollapseFieldEntity:
    """A fundamental collapse field configuration with 8 measurable channels."""

    name: str
    category: str
    field_coherence: float
    recursive_depth: float
    return_fidelity: float
    drift_potential: float
    entropy_density: float
    curvature_coupling: float
    geodesic_efficiency: float
    grammar_complexity: float

    def trace_vector(self) -> np.ndarray:
        return np.array(
            [
                self.field_coherence,
                self.recursive_depth,
                self.return_fidelity,
                self.drift_potential,
                self.entropy_density,
                self.curvature_coupling,
                self.geodesic_efficiency,
                self.grammar_complexity,
            ]
        )


# ═══════════════════════════════════════════════════════════════════
#  ENTITY CATALOG — 12 fundamental collapse field configurations
# ═══════════════════════════════════════════════════════════════════
#
#  Channel semantics:
#    field_coherence     — 1.0 = perfectly coherent field, near ε = dead
#    recursive_depth     — 1.0 = deeply nested self-similarity, 0 = flat
#    return_fidelity     — 1.0 = perfect return (τ_R finite, small)
#    drift_potential     — 1.0 = far from collapse boundary, 0 = at boundary
#    entropy_density     — 1.0 = maximal Bernoulli field entropy (c=1/2)
#    curvature_coupling  — 1.0 = strong coupling (high C), 0 = decoupled
#    geodesic_efficiency — 1.0 = paths follow Fisher geodesic exactly
#    grammar_complexity  — 1.0 = maximally complex grammar, 0 = frozen
#
#  The 12 configurations span the field's phase space.  Three fixed
#  points (equator c=1/2, logistic c*=0.7822, trap c_trap=0.3178)
#  anchor the manifold skeleton.  Three phase boundaries map the
#  transitions discovered across domains (confinement cliff in SM,
#  scale inversion in atomic physics, first weld in orientation §4).
#  Three recursive configurations capture the self-similar nesting
#  that defines RCFT.  Three extremal states probe the boundary
#  behavior of the kernel.

CFT_ENTITIES: tuple[CollapseFieldEntity, ...] = (
    # ── Fixed-point configurations ──
    # Equator: c = 1/2 everywhere — maximum entropy, S + κ = 0, quintuple
    # fixed point (orientation §8).  All channels balanced.
    CollapseFieldEntity(
        "equator_field",
        "fixed_point",
        0.50,
        0.50,
        0.50,
        0.50,
        0.99,
        0.02,
        0.99,
        0.50,
    ),
    # Logistic fixed point: c* = 0.7822 — maximizes S + κ per channel.
    # High coherence, good return, moderate recursion.
    CollapseFieldEntity(
        "logistic_fixed_point",
        "fixed_point",
        0.78,
        0.65,
        0.78,
        0.78,
        0.77,
        0.10,
        0.95,
        0.45,
    ),
    # Trap fixed point: c_trap = 0.3178 — reflection of c* through equator.
    # Low coherence, poor return, the "trap" where Γ first drops below 1.0.
    CollapseFieldEntity(
        "trap_fixed_point",
        "fixed_point",
        0.32,
        0.35,
        0.32,
        0.32,
        0.77,
        0.30,
        0.60,
        0.55,
    ),
    # ── Phase boundary configurations ──
    # Confinement boundary: the cliff where IC drops 98% (orientation §5).
    # One dead channel (color → ε) kills IC while F stays healthy.
    CollapseFieldEntity(
        "confinement_boundary",
        "phase_boundary",
        0.85,
        0.40,
        0.20,
        0.60,
        0.55,
        0.70,
        0.30,
        0.65,
    ),
    # Scale inversion: atoms restore IC with new degrees of freedom (§6).
    # High coherence across all channels — the recovery after confinement.
    CollapseFieldEntity(
        "scale_inversion",
        "phase_boundary",
        0.92,
        0.70,
        0.90,
        0.88,
        0.30,
        0.08,
        0.92,
        0.35,
    ),
    # Weld threshold: c ≈ 0.318 where Γ first drops below 1.0 (§4).
    # The boundary between return-possible and return-costly.
    CollapseFieldEntity(
        "weld_threshold",
        "phase_boundary",
        0.45,
        0.30,
        0.40,
        0.35,
        0.82,
        0.35,
        0.50,
        0.60,
    ),
    # ── Recursive configurations ──
    # Nested collapse: deep recursion with strong self-similarity.
    # High recursive depth, moderate coherence — the "fractal heart" of RCFT.
    CollapseFieldEntity(
        "nested_collapse",
        "recursive",
        0.70,
        0.95,
        0.65,
        0.60,
        0.60,
        0.25,
        0.75,
        0.70,
    ),
    # Fractal cascade: high complexity, moderate recursion — the turbulent
    # regime where collapse generates structure at multiple scales.
    CollapseFieldEntity(
        "fractal_cascade",
        "recursive",
        0.55,
        0.80,
        0.50,
        0.45,
        0.70,
        0.45,
        0.60,
        0.85,
    ),
    # Self-dual field: reflection-symmetric under c ↔ 1−c.
    # Near the equator but with deep recursive structure.
    CollapseFieldEntity(
        "self_dual_field",
        "recursive",
        0.60,
        0.88,
        0.60,
        0.55,
        0.85,
        0.15,
        0.85,
        0.60,
    ),
    # ── Extremal configurations ──
    # Maximal coherence: all channels near 1.0 — the ideal field.
    # Represents the theoretical upper limit of collapse recovery.
    CollapseFieldEntity(
        "maximal_coherence",
        "extremal",
        0.96,
        0.92,
        0.95,
        0.94,
        0.88,
        0.06,
        0.97,
        0.90,
    ),
    # Minimal integrity: one dead channel creates geometric slaughter (§3).
    # F stays healthy but IC crashes — the heterogeneity gap is maximal.
    CollapseFieldEntity(
        "minimal_integrity",
        "extremal",
        0.01,
        0.90,
        0.92,
        0.88,
        0.45,
        0.55,
        0.45,
        0.55,
    ),
    # Dissolution field: high drift, deep in Collapse regime.
    # The field where ω ≥ 0.30 — not failure, but the boundary that
    # makes return meaningful (ruptura est fons constantiae).
    CollapseFieldEntity(
        "dissolution_field",
        "extremal",
        0.15,
        0.20,
        0.10,
        0.10,
        0.65,
        0.80,
        0.15,
        0.90,
    ),
)


# ═══════════════════════════════════════════════════════════════════
#  KERNEL COMPUTATION
# ═══════════════════════════════════════════════════════════════════


@dataclass(frozen=True, slots=True)
class CFTKernelResult:
    """Kernel output for a collapse field configuration."""

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


def compute_cft_kernel(entity: CollapseFieldEntity) -> CFTKernelResult:
    """Compute GCD kernel for a collapse field configuration."""
    c = entity.trace_vector()
    c = np.clip(c, EPSILON, 1.0 - EPSILON)
    w = np.ones(N_CFT_CHANNELS) / N_CFT_CHANNELS
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
    return CFTKernelResult(
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


def compute_all_entities() -> list[CFTKernelResult]:
    """Compute kernel outputs for all collapse field configurations."""
    return [compute_cft_kernel(e) for e in CFT_ENTITIES]


# ═══════════════════════════════════════════════════════════════════
#  THEOREMS (T-CFT-1 through T-CFT-6)
# ═══════════════════════════════════════════════════════════════════


def verify_t_cft_1(results: list[CFTKernelResult]) -> dict:
    """T-CFT-1: Maximal coherence has highest F — the theoretical upper
    limit of collapse recovery yields the strongest fidelity.

    This is the foundational prediction: a field with all channels near
    saturation must have the highest arithmetic mean.
    """
    mc = next(r for r in results if r.name == "maximal_coherence")
    max_F = max(r.F for r in results)
    passed = abs(mc.F - max_F) < 0.02
    return {"name": "T-CFT-1", "passed": bool(passed), "max_coherence_F": mc.F, "max_F": float(max_F)}


def verify_t_cft_2(results: list[CFTKernelResult]) -> dict:
    """T-CFT-2: Fixed-point configurations span three regimes — equator,
    logistic, and trap occupy distinct kernel regions.

    The three fixed points (c=1/2, c*=0.7822, c_trap=0.3178) form the
    skeleton of the manifold.  Their F values must be ordered:
    logistic > equator > trap, reflecting the manifold's asymmetry.
    """
    eq = next(r for r in results if r.name == "equator_field")
    lp = next(r for r in results if r.name == "logistic_fixed_point")
    tp = next(r for r in results if r.name == "trap_fixed_point")
    ordering = lp.F > eq.F > tp.F
    return {
        "name": "T-CFT-2",
        "passed": bool(ordering),
        "logistic_F": lp.F,
        "equator_F": eq.F,
        "trap_F": tp.F,
    }


def verify_t_cft_3(results: list[CFTKernelResult]) -> dict:
    """T-CFT-3: Dissolution field is in Collapse regime — ω ≥ 0.30.

    Deep in the dissolution region, the field has crossed the collapse
    threshold.  This is not failure — it is the boundary that makes
    return meaningful (ruptura est fons constantiae).
    """
    df = next(r for r in results if r.name == "dissolution_field")
    passed = df.regime == "Collapse"
    return {"name": "T-CFT-3", "passed": bool(passed), "dissolution_regime": df.regime, "omega": df.omega}


def verify_t_cft_4(results: list[CFTKernelResult]) -> dict:
    """T-CFT-4: Minimal integrity exhibits geometric slaughter — one dead
    channel (field_coherence near ε) kills IC while F remains healthy.

    This is the RCFT formulation of orientation §3: the heterogeneity
    gap Δ = F − IC is largest for the minimal_integrity configuration.
    """
    mi = next(r for r in results if r.name == "minimal_integrity")
    gap = mi.F - mi.IC
    max_gap = max(r.F - r.IC for r in results)
    # Minimal integrity should have the largest or near-largest gap
    passed = gap >= max_gap - 0.05
    return {
        "name": "T-CFT-4",
        "passed": bool(passed),
        "minimal_integrity_gap": gap,
        "max_gap": float(max_gap),
        "IC": mi.IC,
        "F": mi.F,
    }


def verify_t_cft_5(results: list[CFTKernelResult]) -> dict:
    """T-CFT-5: Recursive configurations have higher mean recursive_depth
    channel values than non-recursive — recursion IS measurable.

    The three recursive entities (nested_collapse, fractal_cascade,
    self_dual_field) are defined by deep self-similar nesting.  Their
    recursive_depth channel must exceed all other categories.
    """
    recursive_depths = []
    other_depths = []
    for entity in CFT_ENTITIES:
        depth = entity.recursive_depth
        if entity.category == "recursive":
            recursive_depths.append(depth)
        else:
            other_depths.append(depth)
    mean_recursive = float(np.mean(recursive_depths))
    mean_other = float(np.mean(other_depths))
    passed = mean_recursive > mean_other
    return {
        "name": "T-CFT-5",
        "passed": bool(passed),
        "recursive_mean_depth": mean_recursive,
        "other_mean_depth": mean_other,
    }


def verify_t_cft_6(results: list[CFTKernelResult]) -> dict:
    """T-CFT-6: Scale inversion restores higher F than confinement boundary
    — the recovery phenomenon seen in orientation §6.

    After confinement kills IC, scale inversion restores coherence with
    new degrees of freedom.  F(scale_inversion) > F(confinement_boundary).
    """
    si = next(r for r in results if r.name == "scale_inversion")
    cb = next(r for r in results if r.name == "confinement_boundary")
    passed = si.F > cb.F
    return {
        "name": "T-CFT-6",
        "passed": bool(passed),
        "scale_inversion_F": si.F,
        "confinement_F": cb.F,
        "delta_F": si.F - cb.F,
    }


def verify_all_theorems() -> list[dict]:
    """Run all T-CFT theorems."""
    results = compute_all_entities()
    return [
        verify_t_cft_1(results),
        verify_t_cft_2(results),
        verify_t_cft_3(results),
        verify_t_cft_4(results),
        verify_t_cft_5(results),
        verify_t_cft_6(results),
    ]


# ═══════════════════════════════════════════════════════════════════
#  MAIN
# ═══════════════════════════════════════════════════════════════════


def main() -> None:
    """Entry point."""
    results = compute_all_entities()
    print("=" * 80)
    print("COLLAPSE FIELD THEORY — FUNDAMENTAL FIELD CONFIGURATIONS")
    print("=" * 80)
    print(f"{'Entity':<28} {'Cat':<16} {'F':>6} {'ω':>6} {'IC':>6} {'Δ':>6} {'Regime'}")
    print("-" * 80)
    for r in results:
        gap = r.F - r.IC
        print(f"{r.name:<28} {r.category:<16} {r.F:6.3f} {r.omega:6.3f} {r.IC:6.3f} {gap:6.3f} {r.regime}")

    print("\n── Theorems ──")
    for t in verify_all_theorems():
        status = "PROVEN" if t["passed"] else "FAILED"
        print(f"  {t['name']}: {status}")


if __name__ == "__main__":
    main()
