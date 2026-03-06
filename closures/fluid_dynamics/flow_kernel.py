"""
Fluid Dynamics Kernel — GCD Applied to Flow Systems

Maps 20 canonical fluid flow regimes and configurations to 8-channel
trace vectors and computes Tier-1 invariants (F, ω, S, C, κ, IC).

Channels (8, equal weight w_i = 1/8):
    1. viscous_fidelity       — Momentum preserved by viscous forces (μ/ρ dominance)
    2. inertial_coherence     — Coherence of inertial momentum transfer
    3. pressure_integrity     — Smoothness and recoverability of pressure field
    4. boundary_adherence     — No-slip condition satisfaction (near-wall fidelity)
    5. vorticity_control      — Organized vorticity; low → turbulent diffusion loss
    6. thermal_coupling       — Energy equation coupling (relevant for compressible flow)
    7. compressibility_margin — Distance from compressibility effects (1 − Ma)
    8. return_to_laminar      — Tendency toward relaminarization under favorable gradient

GCD predictions for fluid dynamics (derivable from Axiom-0):
    - Stable (ω < 0.038): Stokes / creeping flow; highly viscous lubrication
    - Watch (0.038 ≤ ω < 0.30): transitional pipe / channel flow; boundary layer
    - Collapse (ω ≥ 0.30): fully turbulent; supersonic shock; separated flow
    - Geometric slaughter: detached boundary layer kills boundary_adherence → IC cliff
      while F (mean) stays moderate (parallel to quark confinement cliff in T3)
    - τ_R = ∞_rec: fully separated stall — no reattachment path; gestus

Key dimensionless parameters encoded in channels:
    - Reynolds number (Re):  inertial_coherence × viscous_fidelity^{-1}
    - Mach number (Ma):      compressibility_margin = 1 − Ma (clipped)
    - Nusselt number (Nu):   thermal_coupling (heat transfer fidelity)
    - Stokes number (St):    vorticity_control (particle-laden flows)
    - Womersley number:      return_to_laminar (pulsatile biological flows)

Data sources:
    Channel values are consensus estimates from fluid mechanics literature
    (Schlichting & Gersten 2017, Pope 2000, White 2011, Batchelor 1967).
    Values represent structural rankings within the typology of flow regimes,
    not absolute measurements. Kernel results are structural, not empirical.

Derivation chain: Axiom-0 → frozen_contract → kernel_optimized → this module
"""

from __future__ import annotations

import math
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import numpy as np

# ── Path setup ────────────────────────────────────────────────────
_WORKSPACE = Path(__file__).resolve().parents[2]
if str(_WORKSPACE / "src") not in sys.path:
    sys.path.insert(0, str(_WORKSPACE / "src"))
if str(_WORKSPACE) not in sys.path:
    sys.path.insert(0, str(_WORKSPACE))

from umcp.frozen_contract import EPSILON  # noqa: E402
from umcp.kernel_optimized import compute_kernel_outputs  # noqa: E402

# ── Constants ─────────────────────────────────────────────────────
EPS = 1e-6  # Closure-level epsilon (above frozen ε = 1e-8)

CHANNEL_LABELS: list[str] = [
    "viscous_fidelity",
    "inertial_coherence",
    "pressure_integrity",
    "boundary_adherence",
    "vorticity_control",
    "thermal_coupling",
    "compressibility_margin",
    "return_to_laminar",
]

N_CHANNELS = len(CHANNEL_LABELS)

# Regime thresholds (aligned with frozen_contract.RegimeThresholds defaults)
OMEGA_STABLE = 0.038
OMEGA_WATCH = 0.30


# ═════════════════════════════════════════════════════════════════════
# SECTION 1: FLOW SYSTEM DATA
# ═════════════════════════════════════════════════════════════════════


@dataclass(frozen=True, slots=True)
class FlowSystem:
    """A fluid flow regime or configuration with normalized channel scores.

    Channel values are normalized structural rankings in [0, 1], representing
    relative position within the typology of flow regimes. These are
    structural rankings derived from fluid mechanics theory, not direct
    physical measurements.

    Fields
    ------
    name : str
        Descriptive name of the flow system.
    regime_class : str
        Classical flow classification (laminar/turbulent/transitional/
        compressible/geophysical/biological/etc.)
    re_range : str
        Approximate Reynolds number range characterizing this flow.
    notes : str
        Key structural observation (e.g., collapse trigger, return mechanism).
    viscous_fidelity : float
        Momentum preserved by viscous dissipation [0, 1]. High in low-Re flows.
    inertial_coherence : float
        Coherence of inertial momentum transport [0, 1]. High in organized flows.
    pressure_integrity : float
        Smoothness and recoverability of the pressure field [0, 1].
    boundary_adherence : float
        No-slip condition satisfaction / near-wall fidelity [0, 1].
    vorticity_control : float
        Organized vorticity; low in turbulent diffusion-dominated flow [0, 1].
    thermal_coupling : float
        Energy equation coupling strength [0, 1]. Relevant in compressible flows.
    compressibility_margin : float
        Distance from compressibility effects (≈ 1 − Ma) [0, 1].
    return_to_laminar : float
        Tendency toward relaminarization under favorable pressure gradient [0, 1].
    """

    name: str
    regime_class: str
    re_range: str
    notes: str

    # 8 channels — normalized fluid kernel scores [0, 1]
    viscous_fidelity: float
    inertial_coherence: float
    pressure_integrity: float
    boundary_adherence: float
    vorticity_control: float
    thermal_coupling: float
    compressibility_margin: float
    return_to_laminar: float

    def trace(self) -> list[float]:
        """Return the 8-channel trace vector."""
        return [
            self.viscous_fidelity,
            self.inertial_coherence,
            self.pressure_integrity,
            self.boundary_adherence,
            self.vorticity_control,
            self.thermal_coupling,
            self.compressibility_margin,
            self.return_to_laminar,
        ]


# ── Flow system catalog ────────────────────────────────────────────
# 20 representative flow systems spanning the fluid mechanics typology.
# Channel values are structural rankings from fluid mechanics literature.
FLOW_SYSTEMS: list[FlowSystem] = [
    # ── Viscous / Stokes / Creeping Flows ─────────────────────────
    FlowSystem(
        name="Stokes (Creeping) Flow",
        regime_class="laminar",
        re_range="Re < 1",
        notes="Inertia negligible; fully viscous-dominated; near-perfect regime stability",
        viscous_fidelity=0.98,
        inertial_coherence=0.05,
        pressure_integrity=0.96,
        boundary_adherence=0.99,
        vorticity_control=0.95,
        thermal_coupling=0.30,
        compressibility_margin=0.99,
        return_to_laminar=0.99,
    ),
    FlowSystem(
        name="Hele-Shaw Flow",
        regime_class="laminar",
        re_range="Re ≪ 1 (thin gap)",
        notes="2D quasi-static flow between plates; visually time-reversible",
        viscous_fidelity=0.97,
        inertial_coherence=0.04,
        pressure_integrity=0.98,
        boundary_adherence=0.99,
        vorticity_control=0.96,
        thermal_coupling=0.25,
        compressibility_margin=0.99,
        return_to_laminar=0.99,
    ),
    FlowSystem(
        name="Laminar Pipe Flow (Hagen-Poiseuille)",
        regime_class="laminar",
        re_range="Re < 2300",
        notes="Parabolic profile; exact analytical solution; high structural integrity",
        viscous_fidelity=0.92,
        inertial_coherence=0.35,
        pressure_integrity=0.94,
        boundary_adherence=0.97,
        vorticity_control=0.88,
        thermal_coupling=0.40,
        compressibility_margin=0.98,
        return_to_laminar=0.92,
    ),
    # ── Transitional Flows ────────────────────────────────────────
    FlowSystem(
        name="Transitional Pipe Flow",
        regime_class="transitional",
        re_range="2300 < Re < 4000",
        notes="Collapse begins: puffs and slugs; bistable laminar/turbulent dynamics",
        viscous_fidelity=0.62,
        inertial_coherence=0.58,
        pressure_integrity=0.60,
        boundary_adherence=0.65,
        vorticity_control=0.45,
        thermal_coupling=0.50,
        compressibility_margin=0.97,
        return_to_laminar=0.55,
    ),
    FlowSystem(
        name="Transitional Boundary Layer",
        regime_class="transitional",
        re_range="Re_x ≈ 5×10⁵",
        notes="Tollmien-Schlichting waves → turbulent spots; F still moderate",
        viscous_fidelity=0.58,
        inertial_coherence=0.60,
        pressure_integrity=0.55,
        boundary_adherence=0.60,
        vorticity_control=0.40,
        thermal_coupling=0.48,
        compressibility_margin=0.96,
        return_to_laminar=0.45,
    ),
    # ── Fully Turbulent Flows ──────────────────────────────────────
    FlowSystem(
        name="Turbulent Pipe Flow",
        regime_class="turbulent",
        re_range="Re > 4000",
        notes="Log-law velocity profile; strong inertial transport; IC collapse",
        viscous_fidelity=0.30,
        inertial_coherence=0.85,
        pressure_integrity=0.40,
        boundary_adherence=0.45,
        vorticity_control=0.20,
        thermal_coupling=0.72,
        compressibility_margin=0.95,
        return_to_laminar=0.10,
    ),
    FlowSystem(
        name="Turbulent Boundary Layer",
        regime_class="turbulent",
        re_range="Re_x > 5×10⁵",
        notes="Rich vortex structure; high skin friction; IC severely reduced",
        viscous_fidelity=0.28,
        inertial_coherence=0.82,
        pressure_integrity=0.38,
        boundary_adherence=0.42,
        vorticity_control=0.18,
        thermal_coupling=0.70,
        compressibility_margin=0.94,
        return_to_laminar=0.08,
    ),
    FlowSystem(
        name="Free Turbulent Jet",
        regime_class="turbulent",
        re_range="Re > 10³ (jet)",
        notes="Unbounded turbulence; no wall constraint; minimal boundary fidelity",
        viscous_fidelity=0.18,
        inertial_coherence=0.80,
        pressure_integrity=0.50,
        boundary_adherence=0.05,
        vorticity_control=0.15,
        thermal_coupling=0.55,
        compressibility_margin=0.90,
        return_to_laminar=0.05,
    ),
    FlowSystem(
        name="Turbulent Wake",
        regime_class="turbulent",
        re_range="Re > 40 (cylinder wake)",
        notes="Kármán vortex street at low Re → turbulent at high Re; periodic → chaos",
        viscous_fidelity=0.22,
        inertial_coherence=0.75,
        pressure_integrity=0.35,
        boundary_adherence=0.20,
        vorticity_control=0.25,
        thermal_coupling=0.50,
        compressibility_margin=0.92,
        return_to_laminar=0.12,
    ),
    # ── Separated / Stalled Flows ─────────────────────────────────
    FlowSystem(
        name="Separated Flow (Adverse Gradient)",
        regime_class="separated",
        re_range="Re varies",
        notes="Boundary layer detaches; τ_R → ∞_rec for reattachment without forcing",
        viscous_fidelity=0.20,
        inertial_coherence=0.55,
        pressure_integrity=0.15,
        boundary_adherence=0.05,
        vorticity_control=0.12,
        thermal_coupling=0.40,
        compressibility_margin=0.88,
        return_to_laminar=0.03,
    ),
    FlowSystem(
        name="Airfoil Stall",
        regime_class="separated",
        re_range="Re varies (α > α_stall)",
        notes="Catastrophic IC collapse: lift lost, boundary layer fully separated",
        viscous_fidelity=0.15,
        inertial_coherence=0.48,
        pressure_integrity=0.10,
        boundary_adherence=0.03,
        vorticity_control=0.10,
        thermal_coupling=0.35,
        compressibility_margin=0.85,
        return_to_laminar=0.02,
    ),
    # ── Compressible / High-Speed Flows ───────────────────────────
    FlowSystem(
        name="Subsonic Compressible Flow (Ma < 0.8)",
        regime_class="compressible_subsonic",
        re_range="Re > 10⁵, Ma < 0.8",
        notes="Compressibility corrections moderate; pressure integrity still high",
        viscous_fidelity=0.55,
        inertial_coherence=0.72,
        pressure_integrity=0.70,
        boundary_adherence=0.60,
        vorticity_control=0.50,
        thermal_coupling=0.65,
        compressibility_margin=0.55,
        return_to_laminar=0.30,
    ),
    FlowSystem(
        name="Transonic Flow (Ma ≈ 1)",
        regime_class="transonic",
        re_range="0.8 < Ma < 1.2",
        notes="Mixed subsonic/supersonic; shock formation; IC drops sharply",
        viscous_fidelity=0.40,
        inertial_coherence=0.65,
        pressure_integrity=0.35,
        boundary_adherence=0.42,
        vorticity_control=0.30,
        thermal_coupling=0.72,
        compressibility_margin=0.15,
        return_to_laminar=0.18,
    ),
    FlowSystem(
        name="Supersonic Flow with Normal Shock",
        regime_class="supersonic",
        re_range="Ma > 1.5",
        notes="Shock collapses pressure integrity; entropy rise irreversible across shock",
        viscous_fidelity=0.35,
        inertial_coherence=0.70,
        pressure_integrity=0.20,
        boundary_adherence=0.38,
        vorticity_control=0.28,
        thermal_coupling=0.85,
        compressibility_margin=0.05,
        return_to_laminar=0.10,
    ),
    FlowSystem(
        name="Hypersonic Flow (Ma > 5)",
        regime_class="hypersonic",
        re_range="Ma > 5",
        notes="Extreme thermal coupling; chemical dissociation; compressibility margin ≈ ε",
        viscous_fidelity=0.38,
        inertial_coherence=0.72,
        pressure_integrity=0.25,
        boundary_adherence=0.40,
        vorticity_control=0.30,
        thermal_coupling=0.96,
        compressibility_margin=0.03,
        return_to_laminar=0.08,
    ),
    # ── Geophysical / Environmental Flows ─────────────────────────
    FlowSystem(
        name="Atmospheric Boundary Layer",
        regime_class="geophysical",
        re_range="Re ~ 10⁸ (atmospheric)",
        notes="Wall-bounded turbulence at planetary scale; stable boundary layer at night",
        viscous_fidelity=0.12,
        inertial_coherence=0.88,
        pressure_integrity=0.60,
        boundary_adherence=0.30,
        vorticity_control=0.22,
        thermal_coupling=0.78,
        compressibility_margin=0.85,
        return_to_laminar=0.15,
    ),
    FlowSystem(
        name="Ocean Thermohaline Circulation",
        regime_class="geophysical",
        re_range="Re ≫ 1 (Ro ≈ 0.1)",
        notes="Driven by density differences; slow but persistent return; high pressure integrity",
        viscous_fidelity=0.50,
        inertial_coherence=0.62,
        pressure_integrity=0.82,
        boundary_adherence=0.55,
        vorticity_control=0.58,
        thermal_coupling=0.92,
        compressibility_margin=0.95,
        return_to_laminar=0.60,
    ),
    # ── Biological / Micro-scale Flows ────────────────────────────
    FlowSystem(
        name="Blood Flow in Aorta",
        regime_class="biological",
        re_range="Re ≈ 2000–4000 (pulsatile)",
        notes="Womersley flow; pulsatile → intermittent transition; return in diastole",
        viscous_fidelity=0.70,
        inertial_coherence=0.55,
        pressure_integrity=0.75,
        boundary_adherence=0.80,
        vorticity_control=0.60,
        thermal_coupling=0.50,
        compressibility_margin=0.98,
        return_to_laminar=0.72,
    ),
    FlowSystem(
        name="Microfluidic Channel (Lab-on-chip)",
        regime_class="microfluidic",
        re_range="Re < 1 (micro-scale)",
        notes="Stokes regime at micro-scale; diffusion-dominated mixing; near-perfect stability",
        viscous_fidelity=0.96,
        inertial_coherence=0.04,
        pressure_integrity=0.95,
        boundary_adherence=0.98,
        vorticity_control=0.94,
        thermal_coupling=0.35,
        compressibility_margin=0.99,
        return_to_laminar=0.98,
    ),
    FlowSystem(
        name="Turbulent River (Open Channel)",
        regime_class="turbulent",
        re_range="Re > 10⁴ (open channel)",
        notes="Free-surface turbulence; bed roughness kills boundary fidelity",
        viscous_fidelity=0.20,
        inertial_coherence=0.78,
        pressure_integrity=0.45,
        boundary_adherence=0.25,
        vorticity_control=0.20,
        thermal_coupling=0.60,
        compressibility_margin=0.95,
        return_to_laminar=0.08,
    ),
]


# ═════════════════════════════════════════════════════════════════════
# SECTION 2: RESULT DATACLASS
# ═════════════════════════════════════════════════════════════════════


@dataclass
class FlowKernelResult:
    """GCD kernel result for a single fluid flow system.

    Tier-1 invariants (F, ω, S, C, κ, IC) satisfy:
        F + ω = 1      (duality identity — complementum perfectum)
        IC ≤ F         (integrity bound — limbus integritatis)
        IC = exp(κ)    (log-integritas)
    """

    # Identity
    name: str
    regime_class: str
    re_range: str
    notes: str

    # Kernel input
    n_channels: int
    channel_labels: list[str]
    trace_vector: list[float]

    # Tier-1 invariants
    F: float  # Fidelity (weighted mean of trace)
    omega: float  # Drift = 1 − F
    S: float  # Bernoulli field entropy
    C: float  # Curvature (dispersion proxy)
    kappa: float  # Log-integrity = Σ w_i ln(c_i,ε)
    IC: float  # Integrity composite = exp(κ)
    heterogeneity_gap: float  # Δ = F − IC (always ≥ 0)

    # Tier-1 identity checks (to machine precision)
    F_plus_omega: float  # Should equal 1.0
    IC_leq_F: bool  # Should be True
    IC_eq_exp_kappa: bool  # Should be True

    # Classification
    regime: str  # Stable | Watch | Collapse

    # Flow-specific diagnostics
    strongest_channel: str  # Highest-scoring channel (most coherent)
    strongest_value: float
    weakest_channel: str  # Lowest-scoring channel (collapse driver)
    weakest_value: float

    def to_dict(self) -> dict[str, Any]:
        """Serialize to dictionary."""
        return asdict(self)


# ═════════════════════════════════════════════════════════════════════
# SECTION 3: KERNEL COMPUTATION
# ═════════════════════════════════════════════════════════════════════


def _clip(x: float) -> float:
    """Clip to [ε, 1 − ε]."""
    return max(EPSILON, min(1.0 - EPSILON, x))


def _classify_regime(omega: float) -> str:
    """Classify flow regime from drift ω."""
    if omega < OMEGA_STABLE:
        return "Stable"
    if omega < OMEGA_WATCH:
        return "Watch"
    return "Collapse"


def compute_flow_system(fs: FlowSystem) -> FlowKernelResult:
    """Compute GCD kernel for one fluid flow system.

    Parameters
    ----------
    fs : FlowSystem
        The flow system to analyse.

    Returns
    -------
    FlowKernelResult
        Tier-1 invariants and flow classification.
    """
    raw = fs.trace()
    c = np.array([_clip(v) for v in raw], dtype=float)
    w = np.full(N_CHANNELS, 1.0 / N_CHANNELS, dtype=float)

    k = compute_kernel_outputs(c, w, EPSILON)

    F = float(k["F"])
    omega = float(k["omega"])
    S = float(k["S"])
    C_val = float(k["C"])
    kappa = float(k["kappa"])
    IC = float(k["IC"])
    gap = F - IC

    # Tier-1 identity checks
    F_po = F + omega
    ic_leq = IC <= F + 1e-12
    ic_exp = abs(IC - math.exp(kappa)) < 1e-9

    regime = _classify_regime(omega)

    # Identify strongest and weakest channels
    strong_idx = int(np.argmax(c))
    weak_idx = int(np.argmin(c))

    return FlowKernelResult(
        name=fs.name,
        regime_class=fs.regime_class,
        re_range=fs.re_range,
        notes=fs.notes,
        n_channels=N_CHANNELS,
        channel_labels=list(CHANNEL_LABELS),
        trace_vector=[round(float(v), 6) for v in c],
        F=round(F, 6),
        omega=round(omega, 6),
        S=round(S, 6),
        C=round(C_val, 6),
        kappa=round(kappa, 6),
        IC=round(IC, 6),
        heterogeneity_gap=round(gap, 6),
        F_plus_omega=round(F_po, 9),
        IC_leq_F=bool(ic_leq),
        IC_eq_exp_kappa=bool(ic_exp),
        regime=regime,
        strongest_channel=CHANNEL_LABELS[strong_idx],
        strongest_value=round(float(c[strong_idx]), 6),
        weakest_channel=CHANNEL_LABELS[weak_idx],
        weakest_value=round(float(c[weak_idx]), 6),
    )


def compute_all_flow_systems() -> list[FlowKernelResult]:
    """Compute GCD kernel for all 20 flow systems.

    Returns
    -------
    list[FlowKernelResult]
        Kernel results in catalog order.
    """
    return [compute_flow_system(fs) for fs in FLOW_SYSTEMS]


# ═════════════════════════════════════════════════════════════════════
# SECTION 4: FLUID STRUCTURAL ANALYSIS
# ═════════════════════════════════════════════════════════════════════


def analyze_regime_class_profiles(results: list[FlowKernelResult]) -> dict[str, dict[str, float]]:
    """Compute mean Tier-1 invariants per classical flow regime class.

    Returns
    -------
    dict[str, dict[str, float]]
        Mapping from regime class to mean invariant values.
    """
    from collections import defaultdict

    buckets: dict[str, list[FlowKernelResult]] = defaultdict(list)
    for r in results:
        buckets[r.regime_class].append(r)

    profile: dict[str, dict[str, float]] = {}
    for rc, rs in buckets.items():
        n = len(rs)
        profile[rc] = {
            "mean_F": round(sum(r.F for r in rs) / n, 4),
            "mean_omega": round(sum(r.omega for r in rs) / n, 4),
            "mean_IC": round(sum(r.IC for r in rs) / n, 4),
            "mean_S": round(sum(r.S for r in rs) / n, 4),
            "mean_gap": round(sum(r.heterogeneity_gap for r in rs) / n, 4),
            "count": float(n),
        }
    return profile


def find_geometric_slaughter_flows(
    results: list[FlowKernelResult], ic_threshold: float = 0.30
) -> list[FlowKernelResult]:
    """Return flow systems where IC < threshold — geometric slaughter candidates.

    In fluid dynamics, geometric slaughter corresponds to catastrophic loss
    of flow coherence when a single channel (e.g., boundary_adherence after
    separation) collapses to near-ε, dragging IC down regardless of the
    other channels.
    """
    return [r for r in results if ic_threshold > r.IC]


def fluid_structural_summary(results: list[FlowKernelResult]) -> dict[str, Any]:
    """Produce a structural summary of the fluid dynamics kernel sweep.

    Returns counts by regime, mean F per regime class, and the laminar-
    turbulent split visible in the kernel.
    """
    n = len(results)

    regime_counts = {"Stable": 0, "Watch": 0, "Collapse": 0}
    for r in results:
        regime_counts[r.regime] += 1

    # Mean F per regime class
    from collections import defaultdict

    rc_F: dict[str, list[float]] = defaultdict(list)
    for r in results:
        rc_F[r.regime_class].append(r.F)
    mean_F_per_class = {rc: round(sum(vs) / len(vs), 4) for rc, vs in rc_F.items()}

    # Geometric slaughter candidates
    slaughter = find_geometric_slaughter_flows(results)

    # Laminar-turbulent F split (laminar: F > 0.80, turbulent: F < 0.50)
    laminar_results = [r for r in results if r.regime_class in ("laminar", "microfluidic")]
    turbulent_results = [r for r in results if r.regime_class == "turbulent"]
    mean_F_laminar = sum(r.F for r in laminar_results) / len(laminar_results) if laminar_results else 0.0
    mean_F_turbulent = sum(r.F for r in turbulent_results) / len(turbulent_results) if turbulent_results else 0.0

    return {
        "n_flow_systems": n,
        "regime_counts": regime_counts,
        "mean_F_per_class": mean_F_per_class,
        "n_slaughter_candidates": len(slaughter),
        "slaughter_candidates": [r.name for r in slaughter],
        "mean_F_laminar": round(mean_F_laminar, 4),
        "mean_F_turbulent": round(mean_F_turbulent, 4),
        "laminar_turbulent_F_split": round(mean_F_laminar - mean_F_turbulent, 4),
    }


# ═════════════════════════════════════════════════════════════════════
# SECTION 5: SELF-TEST
# ═════════════════════════════════════════════════════════════════════


if __name__ == "__main__":
    results = compute_all_flow_systems()

    print("=" * 76)
    print("  FLUID DYNAMICS KERNEL — GCD Applied to Flow Systems")
    print("=" * 76)
    print(f"\n  {len(results)} flow systems × {N_CHANNELS} channels\n")
    print(f"  {'Name':<36s}  {'F':>6s}  {'ω':>6s}  {'IC':>6s}  {'Δ':>6s}  {'Regime':<10s}")
    print("  " + "-" * 74)

    for r in results:
        print(f"  {r.name:<36s}  {r.F:6.3f}  {r.omega:6.3f}  {r.IC:6.3f}  {r.heterogeneity_gap:6.3f}  {r.regime:<10s}")

    summary = fluid_structural_summary(results)
    print(f"\n  Regime distribution: {summary['regime_counts']}")
    print(f"  Mean F (laminar):    {summary['mean_F_laminar']:.3f}")
    print(f"  Mean F (turbulent):  {summary['mean_F_turbulent']:.3f}")
    print(f"  F split:             {summary['laminar_turbulent_F_split']:.3f}")
    print(f"  Geometric slaughter candidates (IC < 0.30): {summary['n_slaughter_candidates']}")

    # Verify Tier-1 identities
    duality_ok = all(abs(r.F_plus_omega - 1.0) < 1e-9 for r in results)
    bound_ok = all(r.IC_leq_F for r in results)
    exp_ok = all(r.IC_eq_exp_kappa for r in results)

    print("\n  Tier-1 identity checks:")
    print(f"    F + ω = 1:     {'PASS' if duality_ok else 'FAIL'}")
    print(f"    IC ≤ F:        {'PASS' if bound_ok else 'FAIL'}")
    print(f"    IC = exp(κ):   {'PASS' if exp_ok else 'FAIL'}")
