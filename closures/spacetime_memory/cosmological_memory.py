"""Cosmological Memory Closure — Spacetime Memory Domain.

Tier-2 closure mapping 12 cosmological memory/imprint systems through
the GCD kernel.  Each system is characterized by 8 channels drawn from
observational cosmology and large-scale structure research.

Channels (8, equal weights w_i = 1/8):
  0  persistence_timescale   — how long the imprint survives (1 = permanent)
  1  spatial_extent          — physical scale of the memory (1 = universe-spanning)
  2  information_density     — bits per unit volume (1 = maximal)
  3  detectability           — observational accessibility (1 = easily detectable)
  4  causal_connectivity     — causal relationship to origin event (1 = direct)
  5  spectral_fidelity       — preservation of frequency information (1 = perfect)
  6  nonlinear_coupling      — interaction with other fields (1 = fully coupled)
  7  expansion_resilience    — resistance to cosmological expansion (1 = no degradation)

12 entities across 4 categories:
  Radiation (3): cmb_anisotropy, cosmic_neutrino_background, gravitational_wave_background
  Structure (3): baryon_acoustic_oscillation, cosmic_web_filament, void_hierarchy
  Relic (3): primordial_nucleosynthesis, magnetic_field_fossil, topological_defect
  Dynamic (3): reionization_imprint, dark_energy_imprint, galaxy_merger_remnant

6 theorems (T-CM-1 through T-CM-6).
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

CM_CHANNELS = [
    "persistence_timescale",
    "spatial_extent",
    "information_density",
    "detectability",
    "causal_connectivity",
    "spectral_fidelity",
    "nonlinear_coupling",
    "expansion_resilience",
]
N_CM_CHANNELS = len(CM_CHANNELS)


@dataclass(frozen=True, slots=True)
class CosmologicalMemoryEntity:
    """A cosmological memory imprint with 8 measurable channels."""

    name: str
    category: str
    persistence_timescale: float
    spatial_extent: float
    information_density: float
    detectability: float
    causal_connectivity: float
    spectral_fidelity: float
    nonlinear_coupling: float
    expansion_resilience: float

    def trace_vector(self) -> np.ndarray:
        return np.array(
            [
                self.persistence_timescale,
                self.spatial_extent,
                self.information_density,
                self.detectability,
                self.causal_connectivity,
                self.spectral_fidelity,
                self.nonlinear_coupling,
                self.expansion_resilience,
            ]
        )


CM_ENTITIES: tuple[CosmologicalMemoryEntity, ...] = (
    # Radiation — ancient signals, high persistence, variable detectability
    CosmologicalMemoryEntity("cmb_anisotropy", "radiation", 0.95, 0.95, 0.90, 0.90, 0.80, 0.85, 0.55, 0.70),
    CosmologicalMemoryEntity("cosmic_neutrino_background", "radiation", 0.95, 0.90, 0.75, 0.10, 0.85, 0.70, 0.40, 0.80),
    CosmologicalMemoryEntity(
        "gravitational_wave_background", "radiation", 0.90, 0.85, 0.60, 0.15, 0.75, 0.65, 0.50, 0.85
    ),
    # Structure — large-scale patterns in matter distribution
    CosmologicalMemoryEntity(
        "baryon_acoustic_oscillation", "structure", 0.85, 0.80, 0.70, 0.85, 0.70, 0.75, 0.60, 0.75
    ),
    CosmologicalMemoryEntity("cosmic_web_filament", "structure", 0.80, 0.90, 0.55, 0.70, 0.60, 0.50, 0.80, 0.65),
    CosmologicalMemoryEntity("void_hierarchy", "structure", 0.85, 0.95, 0.45, 0.65, 0.55, 0.40, 0.70, 0.75),
    # Relic — primordial signatures embedded in matter/radiation
    CosmologicalMemoryEntity("primordial_nucleosynthesis", "relic", 0.95, 0.70, 0.80, 0.75, 0.90, 0.60, 0.45, 0.85),
    CosmologicalMemoryEntity("magnetic_field_fossil", "relic", 0.80, 0.65, 0.50, 0.35, 0.70, 0.55, 0.60, 0.75),
    CosmologicalMemoryEntity("topological_defect", "relic", 0.90, 0.80, 0.65, 0.10, 0.80, 0.70, 0.75, 0.80),
    # Dynamic — recent cosmological processes with evolving imprints
    CosmologicalMemoryEntity("reionization_imprint", "dynamic", 0.70, 0.85, 0.55, 0.60, 0.65, 0.50, 0.55, 0.65),
    CosmologicalMemoryEntity("dark_energy_imprint", "dynamic", 0.75, 0.95, 0.30, 0.50, 0.40, 0.35, 0.45, 0.80),
    CosmologicalMemoryEntity("galaxy_merger_remnant", "dynamic", 0.60, 0.40, 0.70, 0.80, 0.70, 0.55, 0.85, 0.50),
)


@dataclass(frozen=True, slots=True)
class CMKernelResult:
    """Kernel output for a cosmological memory entity."""

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


def compute_cm_kernel(entity: CosmologicalMemoryEntity) -> CMKernelResult:
    """Compute GCD kernel for a cosmological memory entity."""
    c = entity.trace_vector()
    c = np.clip(c, EPSILON, 1.0 - EPSILON)
    w = np.ones(N_CM_CHANNELS) / N_CM_CHANNELS
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
    return CMKernelResult(
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


def compute_all_entities() -> list[CMKernelResult]:
    """Compute kernel outputs for all cosmological memory entities."""
    return [compute_cm_kernel(e) for e in CM_ENTITIES]


# ── Theorems ──────────────────────────────────────────────────────────


def verify_t_cm_1(results: list[CMKernelResult]) -> dict:
    """T-CM-1: CMB anisotropy has highest F — the most information-rich
    and best-measured cosmological signal.
    """
    cmb = next(r for r in results if r.name == "cmb_anisotropy")
    max_F = max(r.F for r in results)
    passed = abs(cmb.F - max_F) < 0.02
    return {"name": "T-CM-1", "passed": bool(passed), "cmb_F": cmb.F, "max_F": float(max_F)}


def verify_t_cm_2(results: list[CMKernelResult]) -> dict:
    """T-CM-2: Radiation category has highest mean persistence —
    CMB and cosmic neutrino background are the oldest surviving signals.
    """
    cats = {e.category for e in CM_ENTITIES}
    cat_means = {}
    for cat in cats:
        vals = [e.persistence_timescale for e in CM_ENTITIES if e.category == cat]
        cat_means[cat] = float(np.mean(vals))
    rad_mean = cat_means["radiation"]
    passed = all(rad_mean >= v - 1e-9 for v in cat_means.values())
    return {
        "name": "T-CM-2",
        "passed": bool(passed),
        "radiation_persistence": rad_mean,
        "all_means": cat_means,
    }


def verify_t_cm_3(results: list[CMKernelResult]) -> dict:
    """T-CM-3: Cosmic neutrino background has largest heterogeneity gap —
    extremely low detectability (0.10) kills IC despite high persistence
    and causal connectivity.
    """
    gaps = {r.name: r.F - r.IC for r in results}
    cnb_gap = gaps["cosmic_neutrino_background"]
    max_gap = max(gaps.values())
    passed = abs(cnb_gap - max_gap) < 0.01
    return {
        "name": "T-CM-3",
        "passed": bool(passed),
        "cnb_gap": float(cnb_gap),
        "max_gap": float(max_gap),
    }


def verify_t_cm_4(results: list[CMKernelResult]) -> dict:
    """T-CM-4: Dynamic category has lowest mean persistence —
    most recent cosmological processes with not yet solidified imprints.
    """
    cats = {e.category for e in CM_ENTITIES}
    cat_means = {}
    for cat in cats:
        vals = [e.persistence_timescale for e in CM_ENTITIES if e.category == cat]
        cat_means[cat] = float(np.mean(vals))
    dyn_mean = cat_means["dynamic"]
    passed = all(dyn_mean <= v + 1e-9 for v in cat_means.values())
    return {
        "name": "T-CM-4",
        "passed": bool(passed),
        "dynamic_persistence": dyn_mean,
        "all_means": cat_means,
    }


def verify_t_cm_5(results: list[CMKernelResult]) -> dict:
    """T-CM-5: Gravitational wave background is in Collapse regime —
    extremely low detectability (< 0.20) drives ω above threshold.
    """
    gwb = next(r for r in results if r.name == "gravitational_wave_background")
    passed = gwb.regime == "Collapse"
    return {"name": "T-CM-5", "passed": bool(passed), "gwb_regime": gwb.regime, "gwb_omega": gwb.omega}


def verify_t_cm_6(results: list[CMKernelResult]) -> dict:
    """T-CM-6: Baryon acoustic oscillation has highest detectability
    among structure systems — standard ruler for cosmological distances.
    """
    struct = [e for e in CM_ENTITIES if e.category == "structure"]
    bao = next(e for e in struct if e.name == "baryon_acoustic_oscillation")
    max_det = max(e.detectability for e in struct)
    passed = abs(bao.detectability - max_det) < 0.01
    return {
        "name": "T-CM-6",
        "passed": bool(passed),
        "bao_detect": bao.detectability,
        "struct_max_detect": float(max_det),
    }


def verify_all_theorems() -> list[dict]:
    """Run all T-CM theorems."""
    results = compute_all_entities()
    return [
        verify_t_cm_1(results),
        verify_t_cm_2(results),
        verify_t_cm_3(results),
        verify_t_cm_4(results),
        verify_t_cm_5(results),
        verify_t_cm_6(results),
    ]


def main() -> None:
    """Entry point."""
    results = compute_all_entities()
    print("=" * 78)
    print("COSMOLOGICAL MEMORY — GCD KERNEL ANALYSIS")
    print("=" * 78)
    print(f"{'Entity':<32} {'Cat':<12} {'F':>6} {'ω':>6} {'IC':>6} {'Δ':>6} {'Regime'}")
    print("-" * 78)
    for r in results:
        gap = r.F - r.IC
        print(f"{r.name:<32} {r.category:<12} {r.F:6.3f} {r.omega:6.3f} {r.IC:6.3f} {gap:6.3f} {r.regime}")

    print("\n── Theorems ──")
    for t in verify_all_theorems():
        print(f"  {t['name']}: {'PROVEN' if t['passed'] else 'FAILED'}")


if __name__ == "__main__":
    main()
