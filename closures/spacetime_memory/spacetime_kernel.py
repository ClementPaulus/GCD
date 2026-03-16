"""
Spacetime Memory Kernel — Tier-2 Closure

Formalizes the connection between Space, Time, Gravity, Memory Wells,
and Gravitational Lensing as structural consequences of the budget
surface Gamma(omega) = omega^3 / (1 - omega + epsilon).

Key insight: All five phenomena derive from a SINGLE surface:
    z(omega, C) = Gamma(omega) + alpha * C

    - DIMENSION = rank of the kernel = 3  (F, kappa, C)
    - TIME = poloidal circulation on the budget surface
    - GRAVITY = gradient of the budget surface d_Gamma/d_omega
    - MASS = accumulated |kappa| from iterated collapse-return cycles
    - LENSING = trajectory deflection near a memory well

Channels (8, equal weights):
    0. coherence_persistence  — Fraction of kappa retained per cycle
    1. cycle_return_rate      — Fraction of cycles achieving tau_R < inf
    2. well_depth_norm        — Accumulated |kappa| normalized to max
    3. gradient_strength      — d_Gamma/d_omega normalized to regime
    4. tidal_symmetry         — 1 - |asymmetry| of d2_Gamma across well
    5. trajectory_closure     — Loop closure gap in (F, kappa, C) space
    6. circulation_area       — Enclosed area of collapse-return loop
    7. heterogeneity_profile  — 1 - Delta/F (channel uniformity)

Entity catalog: 37 spacetime objects across 8 categories:
    - subatomic (5):   Up quark, Electron, Proton, Neutron, Photon
    - nuclear_atomic (3): Helium-4 nucleus, Iron-56 nucleus, Carbon-12 atom
    - stellar (7):     Star, Neutron star, White dwarf, Red giant,
                        Black hole, Magnetar, Pulsar
    - planetary (5):   Rocky planet, Gas giant, Ice giant, Dwarf planet, Moon
    - diffuse (4):     Molecular cloud, Dust lane, Nebula, Intergalactic medium
    - composite (5):   Galaxy, Galaxy cluster, Binary star, Accretion disk,
                        Cosmic filament
    - cognitive (4):   Healthy memory, Trauma well (PTSD), Habit loop,
                        Grief cycle
    - biological (4):  Neuron, Cortical network, Heart rhythm, Immune response

The cognitive category demonstrates the cross-domain unification:
the exact same budget surface geometry that creates a stellar gravity
well also creates a psychological memory well. PTSD is an asymmetric
well with high heterogeneity gap Delta; a healthy habit is a symmetric
well with low Delta.

GR -> GCD translation (formalized from scripts/gravity_definition.py):
    Mass          = accumulated |kappa|
    Curvature     = extrinsic curvature of budget surface
    Geodesic      = least-budget path (Christoffel ODE)
    Event horizon = omega = 1 pole (Gamma -> infinity)
    Graviton      = minimum |Delta_kappa| deposit
    Time dilation = tau_R* increases near wells
    Tidal force   = d2_Gamma/d_omega2
    Einstein ring = closed deflection orbit
    Lensing shape = controlled by heterogeneity gap Delta

Derivation chain: Axiom-0 -> frozen_contract -> kernel_optimized -> this module
"""

from __future__ import annotations

import sys
from dataclasses import dataclass
from pathlib import Path

import numpy as np

# -- Path setup ---------------------------------------------------------------
_WORKSPACE = Path(__file__).resolve().parents[2]
if str(_WORKSPACE / "src") not in sys.path:
    sys.path.insert(0, str(_WORKSPACE / "src"))
if str(_WORKSPACE) not in sys.path:
    sys.path.insert(0, str(_WORKSPACE))

from umcp.frozen_contract import ALPHA, EPSILON, P_EXPONENT  # noqa: E402
from umcp.kernel_optimized import compute_kernel_outputs  # noqa: E402

# ===========================================================================
# BUDGET SURFACE FUNCTIONS (from frozen parameters, never hardcoded)
# ===========================================================================


def gamma(omega: float) -> float:
    """Budget cost function Gamma(omega) = omega^p / (1 - omega + epsilon)."""
    return omega**P_EXPONENT / (1.0 - omega + EPSILON)


def d_gamma(omega: float) -> float:
    """First derivative d_Gamma/d_omega (gravitational field strength)."""
    h = 1e-7
    return (gamma(omega + h) - gamma(omega - h)) / (2.0 * h)


def d2_gamma(omega: float) -> float:
    """Second derivative d2_Gamma/d_omega2 (tidal force)."""
    h = 1e-7
    return (gamma(omega + h) - 2.0 * gamma(omega) + gamma(omega - h)) / (h * h)


def d3_gamma(omega: float) -> float:
    """Third derivative d3_Gamma/d_omega3 (tidal gradient / jerk)."""
    h = 1e-6
    return (d2_gamma(omega + h) - d2_gamma(omega - h)) / (2.0 * h)


def budget_surface_height(omega: float, C: float) -> float:
    """Full budget surface z(omega, C) = Gamma(omega) + alpha * C."""
    return gamma(omega) + ALPHA * C


# ===========================================================================
# MEMORY WELL COMPUTATION
# ===========================================================================


def compute_well_depth(kappa_per_cycle: float, n_cycles: int) -> float:
    """Accumulated memory well depth from iterated collapse-return cycles.

    Well depth = N * |Delta_kappa|. Each cycle that returns (tau_R < inf)
    deposits |Delta_kappa| into the budget surface.
    """
    return n_cycles * abs(kappa_per_cycle)


def compute_deflection_angle(well_kappa: float, impact_parameter: float) -> float:
    """Trajectory deflection angle near a memory well.

    delta_theta = 2 * |kappa_well| / (b^2 + 0.1)

    The 0.1 softening prevents divergence at b = 0 and provides
    a finite core radius for the well.
    """
    return 2.0 * abs(well_kappa) / (impact_parameter**2 + 0.1)


def classify_lensing_morphology(delta: float) -> str:
    """Classify lensing shape from heterogeneity gap Delta = F - IC.

    Delta ~ 0    -> Perfect ring (symmetric gradient)
    Delta small  -> Thick arc (slight asymmetry)
    Delta large  -> Thin arc (strong asymmetry)
    Delta ~ F    -> Distorted (IC killed, anisotropic gradient)
    """
    if delta < 0.02:
        return "perfect_ring"
    if delta < 0.10:
        return "thick_arc"
    if delta < 0.30:
        return "thin_arc"
    return "distorted"


# ===========================================================================
# TIME-AS-VORTEX COMPUTATION
# ===========================================================================


def compute_descent_cost(omega_start: float, omega_end: float, n_steps: int = 50) -> float:
    """Cumulative Gamma cost descending from omega_start to omega_end."""
    omegas = np.linspace(omega_start, omega_end, n_steps)
    return float(np.trapezoid([gamma(w) for w in omegas], omegas))


def compute_ascent_cost(omega_start: float, omega_end: float, n_steps: int = 50) -> float:
    """Cumulative Gamma cost ascending from omega_start back to omega_end."""
    omegas = np.linspace(omega_start, omega_end, n_steps)
    return float(np.trapezoid([gamma(w) for w in omegas], omegas))


def compute_arrow_asymmetry(omega_mid: float = 0.5) -> float:
    """Ratio of ascent cost to descent cost at a given omega.

    Values >> 1.0 indicate strong time asymmetry (cheap descent, costly ascent).
    """
    descent = compute_descent_cost(0.01, omega_mid)
    ascent = compute_ascent_cost(omega_mid, 0.99)
    if abs(descent) < 1e-15:
        return float("inf")
    return ascent / descent


def compute_loop_area(
    channels: np.ndarray,
    weights: np.ndarray,
    degradation_rate: float = 0.03,
    recovery_rate: float = 0.025,
    n_steps: int = 40,
) -> dict[str, float]:
    """Compute enclosed area of a collapse-return loop in (F, kappa, C) space.

    Simulates degradation (collapse) and recovery (return) with different
    rates to produce an asymmetric loop. Nonzero area => vortex topology.
    """
    F_trace: list[float] = []
    kappa_trace: list[float] = []
    C_trace: list[float] = []

    c = channels.copy()
    w = weights / weights.sum()

    # Degradation phase
    for _ in range(n_steps):
        c_clamped = np.clip(c, EPSILON, 1.0 - EPSILON)
        F_val = float(np.dot(w, c_clamped))
        kappa_val = float(np.dot(w, np.log(c_clamped)))
        C_val = float(np.std(c_clamped) / 0.5)
        F_trace.append(F_val)
        kappa_trace.append(kappa_val)
        C_trace.append(C_val)
        c = np.clip(c - degradation_rate * np.random.default_rng(42).uniform(0.5, 1.5, len(c)), EPSILON, 1.0)

    # Recovery phase (slower, different path)
    for _ in range(n_steps):
        c_clamped = np.clip(c, EPSILON, 1.0 - EPSILON)
        F_val = float(np.dot(w, c_clamped))
        kappa_val = float(np.dot(w, np.log(c_clamped)))
        C_val = float(np.std(c_clamped) / 0.5)
        F_trace.append(F_val)
        kappa_trace.append(kappa_val)
        C_trace.append(C_val)
        c = np.clip(c + recovery_rate * np.random.default_rng(73).uniform(0.3, 1.0, len(c)), EPSILON, 1.0)

    Fa = np.array(F_trace)
    Ka = np.array(kappa_trace)
    Ca = np.array(C_trace)

    # Shoelace formula for enclosed area in each plane
    area_FK = 0.5 * float(np.abs(np.sum(Fa[:-1] * Ka[1:] - Fa[1:] * Ka[:-1])))
    area_FC = 0.5 * float(np.abs(np.sum(Fa[:-1] * Ca[1:] - Fa[1:] * Ca[:-1])))
    area_KC = 0.5 * float(np.abs(np.sum(Ka[:-1] * Ca[1:] - Ka[1:] * Ca[:-1])))

    closure_gap = float(np.sqrt((Fa[0] - Fa[-1]) ** 2 + (Ka[0] - Ka[-1]) ** 2 + (Ca[0] - Ca[-1]) ** 2))

    return {
        "area_FK": area_FK,
        "area_FC": area_FC,
        "area_KC": area_KC,
        "total_area": area_FK + area_FC + area_KC,
        "closure_gap": closure_gap,
    }


# ===========================================================================
# SPACETIME ENTITY — THE TRACE VECTOR
# ===========================================================================


@dataclass
class SpacetimeEntity:
    """A spacetime object mapped onto the 8-channel trace vector."""

    name: str
    category: str  # stellar, planetary, diffuse, composite, cognitive
    channels: tuple[float, ...]  # 8 channels
    description: str = ""

    def __post_init__(self) -> None:
        if len(self.channels) != 8:
            msg = f"{self.name}: expected 8 channels, got {len(self.channels)}"
            raise ValueError(msg)


# Channel names (for reference and display)
CHANNEL_NAMES: list[str] = [
    "coherence_persistence",  # 0: fraction of kappa retained per cycle
    "cycle_return_rate",  # 1: fraction of cycles achieving tau_R < inf
    "well_depth_norm",  # 2: accumulated |kappa| normalized
    "gradient_strength",  # 3: d_Gamma/d_omega normalized
    "tidal_symmetry",  # 4: 1 - |asymmetry| of d2_Gamma across well
    "trajectory_closure",  # 5: loop closure gap (1 = perfect close)
    "circulation_area",  # 6: enclosed area of collapse-return loop
    "heterogeneity_profile",  # 7: 1 - Delta/F (channel uniformity)
]


# ===========================================================================
# ENTITY CATALOG — 25 Spacetime Objects
# ===========================================================================
# Channel values grounded in astrophysical scaling relations and
# cognitive neuroscience biomarkers. Each value in [0, 1].
#
# Channels:  coh_per  cyc_ret  well_d   grad_s   tid_sym  traj_cl  circ_ar  het_pro

SPACETIME_CATALOG: list[SpacetimeEntity] = [
    # ── SUBATOMIC (5) ────────────────────────────────────────────
    # Fundamental particles and hadrons. Confinement cliff visible
    # as IC/F drop from quarks to protons/neutrons.
    SpacetimeEntity(
        "Up quark",
        "subatomic",
        (0.95, 0.98, 0.55, 0.50, 0.92, 0.90, 0.45, 0.88),
        "Confined within hadrons; high coherence, strong binding cycle.",
    ),
    SpacetimeEntity(
        "Electron",
        "subatomic",
        (0.92, 0.95, 0.30, 0.10, 0.95, 0.88, 0.25, 0.90),
        "Stable lepton; excellent coherence, negligible gravity well.",
    ),
    SpacetimeEntity(
        "Proton",
        "subatomic",
        (0.97, 0.99, 0.45, 0.05, 0.55, 0.15, 0.35, 0.30),
        "Confinement signature: dead trajectory/heterogeneity channels.",
    ),
    SpacetimeEntity(
        "Neutron",
        "subatomic",
        (0.80, 0.60, 0.46, 0.05, 0.50, 0.12, 0.30, 0.25),
        "Free neutron beta-decays; lower return rate than proton.",
    ),
    SpacetimeEntity(
        "Photon",
        "subatomic",
        (0.99, 0.01, 0.001, 0.001, 0.99, 0.01, 0.001, 0.10),
        "Massless boson; dead well/gradient/circulation channels.",
    ),
    # ── NUCLEAR / ATOMIC (3) ─────────────────────────────────────
    # Nuclear binding restores coherence that confinement destroyed.
    SpacetimeEntity(
        "Helium-4 nucleus",
        "nuclear_atomic",
        (0.98, 0.99, 0.55, 0.25, 0.95, 0.92, 0.50, 0.93),
        "Doubly magic; nuclear binding restores coherence from hadron cliff.",
    ),
    SpacetimeEntity(
        "Iron-56 nucleus",
        "nuclear_atomic",
        (0.95, 0.98, 0.70, 0.35, 0.88, 0.90, 0.55, 0.85),
        "Peak binding energy per nucleon; deepest nuclear well.",
    ),
    SpacetimeEntity(
        "Carbon-12 atom",
        "nuclear_atomic",
        (0.90, 0.95, 0.50, 0.20, 0.92, 0.88, 0.45, 0.90),
        "Basis of organic chemistry; triple-alpha process endpoint.",
    ),
    # ── STELLAR (7) ──────────────────────────────────────────────
    # Stars: high coherence, deep wells, strong gradients.
    # Coherence from nuclear fusion cycle stability.
    SpacetimeEntity(
        "Main-sequence star",
        "stellar",
        (0.92, 0.95, 0.80, 0.35, 0.90, 0.88, 0.72, 0.91),
        "Stable hydrogen fusion; deep symmetric well.",
    ),
    SpacetimeEntity(
        "Red giant",
        "stellar",
        (0.78, 0.85, 0.75, 0.40, 0.82, 0.70, 0.65, 0.80),
        "Expanded envelope; shallower well, higher gradient.",
    ),
    SpacetimeEntity(
        "White dwarf",
        "stellar",
        (0.88, 0.90, 0.70, 0.30, 0.92, 0.85, 0.58, 0.89),
        "Degenerate core; compact well, low gradient.",
    ),
    SpacetimeEntity(
        "Neutron star",
        "stellar",
        (0.95, 0.92, 0.92, 0.88, 0.85, 0.90, 0.80, 0.82),
        "Extreme density; very deep well, strong tidal forces.",
    ),
    SpacetimeEntity(
        "Black hole",
        "stellar",
        (0.99, 0.50, 0.99, 0.99, 0.60, 0.10, 0.95, 0.40),
        "Maximum well depth; event horizon = omega->1 pole; low return rate.",
    ),
    SpacetimeEntity(
        "Magnetar",
        "stellar",
        (0.90, 0.80, 0.88, 0.92, 0.75, 0.78, 0.85, 0.72),
        "Extreme magnetic field; deep well with tidal asymmetry.",
    ),
    SpacetimeEntity(
        "Pulsar",
        "stellar",
        (0.93, 0.98, 0.82, 0.70, 0.88, 0.95, 0.78, 0.85),
        "Spinning neutron star; excellent trajectory closure (periodic).",
    ),
    # ── PLANETARY (5) ────────────────────────────────────────────
    # Planets: moderate coherence, varying well depths.
    SpacetimeEntity(
        "Rocky planet",
        "planetary",
        (0.75, 0.88, 0.45, 0.15, 0.92, 0.82, 0.40, 0.88),
        "Solid body; moderate well, low gradient, symmetric.",
    ),
    SpacetimeEntity(
        "Gas giant",
        "planetary",
        (0.80, 0.90, 0.65, 0.30, 0.85, 0.78, 0.55, 0.82),
        "Massive envelope; deeper well, moderate gradient.",
    ),
    SpacetimeEntity(
        "Ice giant", "planetary", (0.72, 0.85, 0.50, 0.20, 0.88, 0.80, 0.42, 0.85), "Icy mantle; moderate well."
    ),
    SpacetimeEntity(
        "Dwarf planet",
        "planetary",
        (0.65, 0.82, 0.30, 0.08, 0.90, 0.75, 0.30, 0.88),
        "Small body; shallow well, minimal gradient.",
    ),
    SpacetimeEntity(
        "Moon",
        "planetary",
        (0.60, 0.80, 0.25, 0.05, 0.92, 0.70, 0.25, 0.90),
        "Tidal-locked satellite; very shallow well.",
    ),
    # ── DIFFUSE (4) ──────────────────────────────────────────────
    # Diffuse systems: low coherence, wide asymmetric wells.
    SpacetimeEntity(
        "Molecular cloud",
        "diffuse",
        (0.35, 0.40, 0.20, 0.05, 0.55, 0.30, 0.15, 0.45),
        "Pre-stellar; low coherence, wide well, high heterogeneity.",
    ),
    SpacetimeEntity(
        "Dust lane",
        "diffuse",
        (0.25, 0.30, 0.15, 0.03, 0.50, 0.20, 0.10, 0.35),
        "Obscuring dust; very low coherence, asymmetric well.",
    ),
    SpacetimeEntity(
        "Nebula",
        "diffuse",
        (0.40, 0.45, 0.25, 0.08, 0.60, 0.35, 0.20, 0.50),
        "Emission/reflection; moderate heterogeneity.",
    ),
    SpacetimeEntity(
        "Intergalactic medium",
        "diffuse",
        (0.15, 0.20, 0.08, 0.01, 0.45, 0.15, 0.05, 0.30),
        "Sparse; minimal well, near-zero gradient.",
    ),
    # ── COMPOSITE (5) ────────────────────────────────────────────
    # Composite: aggregated wells, complex structure.
    SpacetimeEntity(
        "Spiral galaxy",
        "composite",
        (0.82, 0.88, 0.85, 0.55, 0.75, 0.80, 0.70, 0.78),
        "Billions of stars; deep composite well.",
    ),
    SpacetimeEntity(
        "Galaxy cluster",
        "composite",
        (0.70, 0.75, 0.90, 0.65, 0.60, 0.65, 0.80, 0.60),
        "Cluster of galaxies; deepest composite well, high gradient.",
    ),
    SpacetimeEntity(
        "Binary star",
        "composite",
        (0.88, 0.92, 0.78, 0.50, 0.70, 0.90, 0.75, 0.75),
        "Two stars orbiting; periodic trajectory with tidal interaction.",
    ),
    SpacetimeEntity(
        "Accretion disk",
        "composite",
        (0.60, 0.55, 0.70, 0.80, 0.50, 0.45, 0.65, 0.48),
        "Inspiraling matter; high gradient, low return rate.",
    ),
    SpacetimeEntity(
        "Cosmic filament",
        "composite",
        (0.50, 0.60, 0.55, 0.25, 0.65, 0.50, 0.40, 0.62),
        "Large-scale structure; moderate well, wide distribution.",
    ),
    # ── COGNITIVE (4) ────────────────────────────────────────────
    # Cognitive memory wells: the SAME geometry as astrophysical wells.
    # Channel values grounded in neuroscience biomarkers.
    SpacetimeEntity(
        "Healthy memory",
        "cognitive",
        (0.85, 0.92, 0.65, 0.55, 0.90, 0.88, 0.60, 0.90),
        "Symmetric well from repeated successful recall cycles.",
    ),
    SpacetimeEntity(
        "Trauma well (PTSD)",
        "cognitive",
        (0.75, 0.30, 0.80, 0.70, 0.20, 0.10, 0.85, 0.15),
        "Deep asymmetric well; dead closure/symmetry channels, high gradient.",
    ),
    SpacetimeEntity(
        "Habit loop",
        "cognitive",
        (0.88, 0.95, 0.55, 0.15, 0.90, 0.92, 0.45, 0.92),
        "Well-worn symmetric track; excellent closure and return.",
    ),
    SpacetimeEntity(
        "Grief cycle",
        "cognitive",
        (0.60, 0.55, 0.65, 0.45, 0.55, 0.50, 0.70, 0.45),
        "Uniform moderate depression; low F but low gap — sadness not fragmentation.",
    ),
    # ── BIOLOGICAL (4) ───────────────────────────────────────────
    # Living oscillators: the bridge from cosmic geometry to memory.
    SpacetimeEntity(
        "Neuron",
        "biological",
        (0.82, 0.90, 0.40, 0.30, 0.85, 0.88, 0.50, 0.78),
        "Action potential cycle; refractory period guarantees return.",
    ),
    SpacetimeEntity(
        "Cortical network",
        "biological",
        (0.75, 0.82, 0.60, 0.35, 0.65, 0.68, 0.58, 0.55),
        "Composite of neurons; oscillatory binding, moderate heterogeneity.",
    ),
    SpacetimeEntity(
        "Heart rhythm",
        "biological",
        (0.95, 0.98, 0.50, 0.40, 0.92, 0.95, 0.55, 0.90),
        "Sinus rhythm: most regular biological oscillator.",
    ),
    SpacetimeEntity(
        "Immune response",
        "biological",
        (0.70, 0.80, 0.45, 0.40, 0.60, 0.65, 0.55, 0.55),
        "Inflammatory-resolution cycle; memory B cells enable return.",
    ),
]


# ===========================================================================
# KERNEL RESULT
# ===========================================================================


@dataclass
class SpacetimeKernelResult:
    """Result of computing the GCD kernel for one spacetime entity."""

    name: str
    category: str
    description: str
    channels: tuple[float, ...]
    F: float
    omega: float
    S: float
    C: float
    kappa: float
    IC: float
    delta: float  # heterogeneity gap F - IC
    regime: str  # Stable / Watch / Collapse
    well_depth: float  # accumulated |kappa| from channels
    gradient: float  # d_Gamma/d_omega at this omega
    tidal: float  # d2_Gamma/d_omega2 at this omega
    lensing_morphology: str  # perfect_ring / thick_arc / thin_arc / distorted
    arrow_asymmetry: float  # ascent/descent cost ratio at this omega


def _classify_regime(omega: float, F: float, S: float, C: float) -> str:
    """Three-valued regime classification from frozen thresholds."""
    if omega >= 0.30:
        return "Collapse"
    if omega < 0.038 and F > 0.90 and S < 0.15 and C < 0.14:
        return "Stable"
    return "Watch"


# ===========================================================================
# KERNEL COMPUTATION
# ===========================================================================


def compute_entity_kernel(entity: SpacetimeEntity) -> SpacetimeKernelResult:
    """Compute GCD kernel for a single spacetime entity."""
    c = np.array(entity.channels, dtype=np.float64)
    w = np.ones(len(c), dtype=np.float64) / len(c)

    result = compute_kernel_outputs(c, w)
    F = float(result["F"])
    omega = float(result["omega"])
    S = float(result["S"])
    C = float(result["C"])
    kappa = float(result["kappa"])
    IC = float(result["IC"])
    delta = F - IC

    regime = _classify_regime(omega, F, S, C)
    well_d = abs(kappa) * 50  # 50 nominal cycles for well depth
    grad = d_gamma(omega)
    tidal = d2_gamma(omega)
    lensing = classify_lensing_morphology(delta)

    # Arrow asymmetry: ratio of ascent to descent cost
    if omega > 0.02:
        descent = compute_descent_cost(0.01, omega)
        ascent = compute_ascent_cost(omega, min(omega + 0.3, 0.98))
        arrow = ascent / descent if abs(descent) > 1e-15 else float("inf")
    else:
        arrow = 1.0

    return SpacetimeKernelResult(
        name=entity.name,
        category=entity.category,
        description=entity.description,
        channels=entity.channels,
        F=F,
        omega=omega,
        S=S,
        C=C,
        kappa=kappa,
        IC=IC,
        delta=delta,
        regime=regime,
        well_depth=well_d,
        gradient=grad,
        tidal=tidal,
        lensing_morphology=lensing,
        arrow_asymmetry=arrow,
    )


def compute_all_spacetime() -> list[SpacetimeKernelResult]:
    """Compute kernel for all 25 spacetime entities."""
    return [compute_entity_kernel(e) for e in SPACETIME_CATALOG]


# ===========================================================================
# MAIN — Run and display results
# ===========================================================================


def main() -> None:
    """Run kernel computation and display results."""
    results = compute_all_spacetime()

    print("=" * 100)
    print("SPACETIME MEMORY KERNEL — 25 Entities Across 5 Categories")
    print("Channels: coherence_persistence, cycle_return_rate, well_depth_norm,")
    print("          gradient_strength, tidal_symmetry, trajectory_closure,")
    print("          circulation_area, heterogeneity_profile")
    print("=" * 100)

    for cat in ["stellar", "planetary", "diffuse", "composite", "cognitive"]:
        cat_results = [r for r in results if r.category == cat]
        print(f"\n{'─' * 100}")
        print(f"  {cat.upper()} ({len(cat_results)} entities)")
        print(f"{'─' * 100}")
        print(
            f"  {'Entity':<25s} {'F':>6s} {'omega':>7s} {'IC':>7s} {'Delta':>7s} "
            f"{'Regime':<10s} {'Well':>8s} {'Grad':>10s} {'Lensing':<15s}"
        )
        for r in cat_results:
            print(
                f"  {r.name:<25s} {r.F:6.4f} {r.omega:7.4f} {r.IC:7.4f} {r.delta:7.4f} "
                f"{r.regime:<10s} {r.well_depth:8.2f} {r.gradient:10.4f} {r.lensing_morphology:<15s}"
            )

    # Summary statistics
    print(f"\n{'=' * 100}")
    print("CROSS-CATEGORY SUMMARY")
    print(f"{'=' * 100}")
    for cat in ["stellar", "planetary", "diffuse", "composite", "cognitive"]:
        cat_results = [r for r in results if r.category == cat]
        avg_F = np.mean([r.F for r in cat_results])
        avg_IC = np.mean([r.IC for r in cat_results])
        avg_delta = np.mean([r.delta for r in cat_results])
        avg_well = np.mean([r.well_depth for r in cat_results])
        print(f"  {cat:<12s}  <F>={avg_F:.4f}  <IC>={avg_IC:.4f}  <Delta>={avg_delta:.4f}  <WellDepth>={avg_well:.2f}")

    # Tier-1 identity check
    print(f"\n{'=' * 100}")
    print("TIER-1 IDENTITY VERIFICATION")
    print(f"{'=' * 100}")
    violations = 0
    for r in results:
        if abs(r.F + r.omega - 1.0) > 1e-12:
            print(f"  VIOLATION: {r.name} F+omega={r.F + r.omega}")
            violations += 1
        if r.IC > r.F + 1e-12:
            print(f"  VIOLATION: {r.name} IC={r.IC} > F={r.F}")
            violations += 1
    print(f"  Violations: {violations}")
    print(f"  Duality F+omega=1: {'EXACT' if violations == 0 else 'FAILED'}")
    print(f"  Integrity IC<=F:   {'HOLDS' if violations == 0 else 'FAILED'}")


if __name__ == "__main__":
    main()
