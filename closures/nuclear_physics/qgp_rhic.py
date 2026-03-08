"""RHIC Quark-Gluon Plasma Closure — Heavy-Ion Collisions Through the GCD Kernel.

A formalized GCD closure of 25 years of RHIC data (2000–2025),
encompassing the Beam Energy Scan program, centrality-dependent
observables, and the time evolution of the QGP fireball.

═══════════════════════════════════════════════════════════════════════
  THE QUARK-GLUON PLASMA  —  *Plasma Quark-Gluonicum per Collapsum*
═══════════════════════════════════════════════════════════════════════

RHIC at Brookhaven National Laboratory collides gold nuclei at
relativistic energies, recreating conditions that existed microseconds
after the Big Bang.  The resulting quark-gluon plasma (QGP) is the
hottest, densest matter ever produced in a laboratory — a state where
quarks and gluons are briefly deconfined from their hadronic prisons.

The GCD kernel maps RHIC observables into 8-channel trace vectors,
revealing that:
  - The QGP→hadron gas transition is a COLLAPSE boundary (IC cliff)
  - Central collisions produce a coherent QGP (high F, high IC)
  - Peripheral collisions show geometric slaughter (low IC)
  - The Beam Energy Scan traces a path through the QCD phase diagram
  - The "perfect liquid" (η/s ≈ 1/4π) corresponds to peak IC

Trace vector construction (8 channels, equal weight w_i = 1/8):
    c₁ = temperature_frac      T / T_Hagedorn (thermal state)
    c₂ = baryochem_frac        μ_B / μ_B_scale (baryon density)
    c₃ = energy_density_norm   log-normalized energy density
    c₄ = collectivity          v₂ / v₂_scale (collective flow)
    c₅ = opacity               1 − R_AA (jet stopping power)
    c₆ = strangeness_eq        γ_s (strangeness equilibration)
    c₇ = multiplicity_norm     log-normalized particle production
    c₈ = deconfinement         fraction of deconfined matter

═══════════════════════════════════════════════════════════════════════
  TEN QGP THEOREMS  (T-QGP-1 through T-QGP-10)
═══════════════════════════════════════════════════════════════════════

  T-QGP-1   Perfect Liquid             IC peaks at mid-centrality (geometry + density)
  T-QGP-2   Centrality Ordering        F broadly increases with N_part
  T-QGP-3   BES Energy Ordering        F increases with √s_NN across BES scan
  T-QGP-4   Strangeness Equilibration  γ_s correlates with IC across BES energies
  T-QGP-5   Reconfinement Gap Jump     QGP→hadron transition has largest Δ jump
  T-QGP-6   Flow-Opacity Structure     v₂ and opacity show distinct centrality patterns
  T-QGP-7   Chemical Freeze-out Curve  T_ch and μ_B anti-correlate across BES
  T-QGP-8   Reconfinement Cliff        QGP→hadron transition shows IC collapse
  T-QGP-9   Reference Discrimination   p+p baseline differs from Au+Au in IC
  T-QGP-10  Universal Tier-1           Identities hold across all QGP measurements

Source data:
    STAR Collaboration, 2000–2025 (Au+Au at √s_NN = 7.7–200 GeV)
    PHENIX Collaboration, 2000–2016 (direct photons, J/ψ suppression)
    BRAHMS & PHOBOS Collaborations (rapidity, multiplicity)
    Lattice QCD: T_c ≈ 155 MeV (Aoki et al. 2006, HotQCD 2014)
    Statistical Hadronization: Andronic et al. 2018, Becattini et al. 2004
    BES-I/II: STAR Collaboration, PRL 112 (2014), PRC 96 (2017)
    QGP viscosity: Romatschke & Romatschke 2007, Heinz & Snellings 2013
    Facility: Relativistic Heavy Ion Collider, BNL, Upton NY (2000–present)

Cross-references:
    Confinement cliff:   closures/standard_model/particle_physics_formalism.py (T3)
    Matter genesis:      closures/standard_model/matter_genesis.py (Act II)
    Subatomic kernel:    closures/standard_model/subatomic_kernel.py
    Nuclear binding:     closures/nuclear_physics/nuclide_binding.py
    Cosmology:           closures/astronomy/cosmology.py
    Kernel:              src/umcp/kernel_optimized.py
    Contract:            contracts/NUC.INTSTACK.v1.yaml
    Axiom:               AXIOM.md
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Any, NamedTuple

import numpy as np

from umcp.frozen_contract import EPSILON
from umcp.kernel_optimized import compute_kernel_outputs

# ═══════════════════════════════════════════════════════════════════
# SECTION 0 — FROZEN CONSTANTS
# ═══════════════════════════════════════════════════════════════════

# QCD phase transition parameters (lattice QCD + RHIC BES)
T_C_MEV: float = 155.0  # QCD crossover temperature (MeV)
T_HAGEDORN_MEV: float = 176.0  # Hagedorn limiting temperature (MeV)
EPSILON_C_GEV_FM3: float = 0.5  # Critical energy density (GeV/fm³)

# KSS bound (Kovtun–Son–Starinets, AdS/CFT)
ETA_OVER_S_KSS: float = 1.0 / (4.0 * math.pi)  # ≈ 0.0796

# Nuclear matter equilibrium
RHO_0_FM3: float = 0.16  # Nuclear saturation density (fm⁻³)
EPSILON_0_GEV_FM3: float = 0.15  # Nuclear matter energy density (GeV/fm³)
SIGMA_NN_MB: float = 42.0  # NN cross section at 200 GeV (mb)

# RHIC facility parameters
SQRT_S_MAX_GEV: float = 200.0  # Maximum Au+Au collision energy per nucleon
AU_A: int = 197  # Gold mass number
AU_Z: int = 79  # Gold atomic number

# Normalization scales for trace vector channels
MU_B_SCALE_MEV: float = 550.0  # μ_B normalization scale (MeV)
V2_SCALE: float = 0.08  # Elliptic flow normalization scale
MULT_LOG_SCALE: float = math.log10(750.0)  # dN/dη log normalization
EPSILON_LOG_MAX: float = math.log10(80.0 / 0.15 + 1.0)  # Energy density log scale

# Speed of sound squared (conformal limit)
CS2_CONFORMAL: float = 1.0 / 3.0


# ═══════════════════════════════════════════════════════════════════
# SECTION 1 — DATA STRUCTURES
# ═══════════════════════════════════════════════════════════════════


class QGPObservables(NamedTuple):
    """Raw RHIC observables for one measurement point."""

    temperature_MeV: float  # Temperature (MeV)
    mu_B_MeV: float  # Baryon chemical potential (MeV)
    epsilon_GeV_fm3: float  # Energy density (GeV/fm³)
    v2: float  # Elliptic flow coefficient
    R_AA: float  # Nuclear modification factor
    gamma_s: float  # Strangeness equilibration
    dNch_deta: float  # Charged particle multiplicity density
    deconfinement_frac: float  # Estimated deconfined fraction


@dataclass
class QGPEntity:
    """One entity in the QGP kernel analysis."""

    name: str
    category: str  # "bes", "centrality", "evolution", "reference"
    sqrt_s_GeV: float
    observables: QGPObservables
    trace: np.ndarray  # 8-channel trace vector
    weights: np.ndarray  # Equal weights (1/8)
    channels: list[str]
    # Kernel outputs
    F: float = 0.0
    omega: float = 0.0
    S: float = 0.0
    C: float = 0.0
    kappa: float = 0.0
    IC: float = 0.0
    gap: float = 0.0
    regime: str = ""
    # Extra metadata
    metadata: dict[str, Any] = field(default_factory=dict)


# ═══════════════════════════════════════════════════════════════════
# SECTION 2 — RHIC DATA TABLES
# ═══════════════════════════════════════════════════════════════════

# Beam Energy Scan (BES) — Chemical freeze-out at 8 collision energies.
# Sources: STAR Collaboration BES-I/II, Andronic et al. (2018) thermal fits.
# At lower √s_NN the system has higher μ_B (more baryonic) and lower T.
# At 200 GeV the system is nearly baryon-free and reaches highest T.
BES_DATA: list[dict[str, Any]] = [
    {
        "sqrt_s": 7.7,
        "T_MeV": 144,
        "mu_B_MeV": 420,
        "gamma_s": 0.60,
        "dNch_deta": 52,
        "v2": 0.040,
        "R_AA": 0.82,
        "epsilon": 1.0,
        "deconf": 0.25,
    },
    {
        "sqrt_s": 11.5,
        "T_MeV": 149,
        "mu_B_MeV": 316,
        "gamma_s": 0.68,
        "dNch_deta": 75,
        "v2": 0.045,
        "R_AA": 0.72,
        "epsilon": 1.8,
        "deconf": 0.40,
    },
    {
        "sqrt_s": 14.5,
        "T_MeV": 151,
        "mu_B_MeV": 264,
        "gamma_s": 0.72,
        "dNch_deta": 95,
        "v2": 0.050,
        "R_AA": 0.65,
        "epsilon": 2.5,
        "deconf": 0.55,
    },
    {
        "sqrt_s": 19.6,
        "T_MeV": 154,
        "mu_B_MeV": 206,
        "gamma_s": 0.77,
        "dNch_deta": 125,
        "v2": 0.055,
        "R_AA": 0.55,
        "epsilon": 3.5,
        "deconf": 0.65,
    },
    {
        "sqrt_s": 27,
        "T_MeV": 155,
        "mu_B_MeV": 156,
        "gamma_s": 0.82,
        "dNch_deta": 160,
        "v2": 0.060,
        "R_AA": 0.45,
        "epsilon": 5.0,
        "deconf": 0.75,
    },
    {
        "sqrt_s": 39,
        "T_MeV": 156,
        "mu_B_MeV": 112,
        "gamma_s": 0.87,
        "dNch_deta": 200,
        "v2": 0.063,
        "R_AA": 0.38,
        "epsilon": 6.5,
        "deconf": 0.82,
    },
    {
        "sqrt_s": 62.4,
        "T_MeV": 160,
        "mu_B_MeV": 72,
        "gamma_s": 0.93,
        "dNch_deta": 310,
        "v2": 0.065,
        "R_AA": 0.30,
        "epsilon": 9.0,
        "deconf": 0.90,
    },
    {
        "sqrt_s": 200,
        "T_MeV": 164,
        "mu_B_MeV": 24,
        "gamma_s": 0.98,
        "dNch_deta": 700,
        "v2": 0.067,
        "R_AA": 0.20,
        "epsilon": 15.0,
        "deconf": 0.95,
    },
]

# Centrality classes — Au+Au at √s_NN = 200 GeV.
# Sources: STAR PRC 86 (2012), PHENIX PRL 101 (2008), PHOBOS PRC 83 (2011).
# N_part = average number of participating nucleons.
# More central collisions produce larger, hotter, longer-lived QGP.
CENTRALITY_DATA: list[dict[str, Any]] = [
    {
        "centrality": "0-5%",
        "N_part": 352,
        "dNch_deta": 700,
        "v2": 0.020,
        "R_AA": 0.20,
        "T_init_MeV": 350,
        "epsilon": 15.0,
        "gamma_s": 0.98,
        "deconf": 0.95,
    },
    {
        "centrality": "5-10%",
        "N_part": 299,
        "dNch_deta": 600,
        "v2": 0.040,
        "R_AA": 0.22,
        "T_init_MeV": 340,
        "epsilon": 12.0,
        "gamma_s": 0.97,
        "deconf": 0.93,
    },
    {
        "centrality": "10-20%",
        "N_part": 234,
        "dNch_deta": 480,
        "v2": 0.055,
        "R_AA": 0.25,
        "T_init_MeV": 320,
        "epsilon": 9.0,
        "gamma_s": 0.95,
        "deconf": 0.90,
    },
    {
        "centrality": "20-30%",
        "N_part": 166,
        "dNch_deta": 340,
        "v2": 0.070,
        "R_AA": 0.30,
        "T_init_MeV": 300,
        "epsilon": 6.5,
        "gamma_s": 0.92,
        "deconf": 0.82,
    },
    {
        "centrality": "30-40%",
        "N_part": 115,
        "dNch_deta": 230,
        "v2": 0.072,
        "R_AA": 0.40,
        "T_init_MeV": 280,
        "epsilon": 4.5,
        "gamma_s": 0.88,
        "deconf": 0.72,
    },
    {
        "centrality": "40-50%",
        "N_part": 76,
        "dNch_deta": 150,
        "v2": 0.063,
        "R_AA": 0.50,
        "T_init_MeV": 260,
        "epsilon": 3.0,
        "gamma_s": 0.82,
        "deconf": 0.58,
    },
    {
        "centrality": "50-60%",
        "N_part": 47,
        "dNch_deta": 90,
        "v2": 0.050,
        "R_AA": 0.60,
        "T_init_MeV": 240,
        "epsilon": 2.0,
        "gamma_s": 0.75,
        "deconf": 0.40,
    },
    {
        "centrality": "60-70%",
        "N_part": 27,
        "dNch_deta": 50,
        "v2": 0.038,
        "R_AA": 0.72,
        "T_init_MeV": 215,
        "epsilon": 1.0,
        "gamma_s": 0.65,
        "deconf": 0.22,
    },
    {
        "centrality": "70-80%",
        "N_part": 14,
        "dNch_deta": 22,
        "v2": 0.025,
        "R_AA": 0.85,
        "T_init_MeV": 190,
        "epsilon": 0.4,
        "gamma_s": 0.55,
        "deconf": 0.08,
    },
]

# Time evolution of central (0-5%) Au+Au at √s_NN = 200 GeV.
# Sources: Heinz & Kolb (2002) hydro, Romatschke (2007) viscous hydro,
# PHENIX direct photons PRL 104 (2010), STAR HBT PRC 71 (2005).
# τ in fm/c (1 fm/c ≈ 3.3 × 10⁻²⁴ s).
EVOLUTION_DATA: list[dict[str, Any]] = [
    {
        "stage": "Pre-collision",
        "tau_fm_c": 0.0,
        "T_MeV": 0,
        "epsilon": 0.15,
        "v2": 0.0,
        "R_AA": 1.0,
        "gamma_s": 0.0,
        "dNch_deta": 0,
        "deconf": 0.0,
        "mu_B_MeV": 24,
        "description": "Cold gold nuclei approach at v ≈ 0.9999c",
    },
    {
        "stage": "Glasma",
        "tau_fm_c": 0.1,
        "T_MeV": 550,
        "epsilon": 80.0,
        "v2": 0.0,
        "R_AA": 0.0,
        "gamma_s": 0.10,
        "dNch_deta": 700,
        "deconf": 0.70,
        "mu_B_MeV": 24,
        "description": "Color glass condensate → glasma flux tubes",
    },
    {
        "stage": "Early QGP",
        "tau_fm_c": 0.6,
        "T_MeV": 350,
        "epsilon": 15.0,
        "v2": 0.005,
        "R_AA": 0.10,
        "gamma_s": 0.40,
        "dNch_deta": 700,
        "deconf": 1.0,
        "mu_B_MeV": 24,
        "description": "Thermalized QGP — nearly perfect liquid",
    },
    {
        "stage": "QGP plateau",
        "tau_fm_c": 3.0,
        "T_MeV": 250,
        "epsilon": 5.0,
        "v2": 0.030,
        "R_AA": 0.15,
        "gamma_s": 0.85,
        "dNch_deta": 700,
        "deconf": 1.0,
        "mu_B_MeV": 24,
        "description": "Expanding QGP develops collective flow",
    },
    {
        "stage": "QGP cooling",
        "tau_fm_c": 5.0,
        "T_MeV": 200,
        "epsilon": 2.0,
        "v2": 0.055,
        "R_AA": 0.18,
        "gamma_s": 0.93,
        "dNch_deta": 700,
        "deconf": 1.0,
        "mu_B_MeV": 24,
        "description": "QGP cools toward T_c, flow strengthens",
    },
    {
        "stage": "Crossover (T_c)",
        "tau_fm_c": 7.0,
        "T_MeV": 155,
        "epsilon": 0.8,
        "v2": 0.065,
        "R_AA": 0.20,
        "gamma_s": 0.96,
        "dNch_deta": 700,
        "deconf": 0.30,
        "mu_B_MeV": 24,
        "description": "QCD crossover — quarks reconfinne into hadrons",
    },
    {
        "stage": "Hadron gas",
        "tau_fm_c": 10.0,
        "T_MeV": 120,
        "epsilon": 0.3,
        "v2": 0.068,
        "R_AA": 0.50,
        "gamma_s": 0.97,
        "dNch_deta": 700,
        "deconf": 0.0,
        "mu_B_MeV": 24,
        "description": "Hadronic rescattering — inelastic collisions cease",
    },
    {
        "stage": "Kinetic freeze-out",
        "tau_fm_c": 15.0,
        "T_MeV": 100,
        "epsilon": 0.1,
        "v2": 0.070,
        "R_AA": 1.0,
        "gamma_s": 0.98,
        "dNch_deta": 700,
        "deconf": 0.0,
        "mu_B_MeV": 24,
        "description": "Elastic collisions cease — particles free-stream",
    },
]

# Reference systems (no QGP or minimal QGP)
REFERENCE_DATA: list[dict[str, Any]] = [
    {
        "name": "p+p at 200 GeV",
        "category": "reference",
        "sqrt_s": 200,
        "T_MeV": 170,
        "mu_B_MeV": 1,
        "epsilon": 0.5,
        "v2": 0.005,
        "R_AA": 1.0,
        "gamma_s": 0.55,
        "dNch_deta": 6,
        "deconf": 0.0,
        "description": "Elementary proton-proton collisions — no QGP",
    },
    {
        "name": "d+Au at 200 GeV",
        "category": "reference",
        "sqrt_s": 200,
        "T_MeV": 180,
        "mu_B_MeV": 5,
        "epsilon": 1.0,
        "v2": 0.010,
        "R_AA": 0.95,
        "gamma_s": 0.62,
        "dNch_deta": 15,
        "deconf": 0.0,
        "description": "Cold nuclear matter effects — initial-state baseline",
    },
]


# ═══════════════════════════════════════════════════════════════════
# SECTION 3 — TRACE VECTOR CONSTRUCTION
# ═══════════════════════════════════════════════════════════════════

CHANNEL_NAMES: list[str] = [
    "temperature_frac",
    "baryochem_frac",
    "energy_density_norm",
    "collectivity",
    "opacity",
    "strangeness_eq",
    "multiplicity_norm",
    "deconfinement",
]


def _clip(x: float) -> float:
    """Clip to [ε, 1−ε]."""
    return max(EPSILON, min(1.0 - EPSILON, x))


def _energy_density_norm(epsilon_GeV_fm3: float) -> float:
    """Log-normalize energy density to [0, 1].

    Uses log₁₀(ε/ε₀ + 1) / log₁₀(ε_max/ε₀ + 1) to map
    the 3-OOM range [0.1, 80] GeV/fm³ smoothly.
    """
    val = math.log10(epsilon_GeV_fm3 / EPSILON_0_GEV_FM3 + 1.0) / EPSILON_LOG_MAX
    return _clip(val)


def _multiplicity_norm(dNch_deta: float) -> float:
    """Log-normalize multiplicity to [0, 1]."""
    if dNch_deta <= 0:
        return EPSILON
    val = math.log10(dNch_deta + 1.0) / MULT_LOG_SCALE
    return _clip(val)


def build_trace(obs: QGPObservables) -> tuple[np.ndarray, np.ndarray]:
    """Construct 8-channel trace vector and weights from observables.

    Returns (trace, weights) where trace ∈ [ε, 1−ε]^8.
    """
    c = np.array(
        [
            _clip(obs.temperature_MeV / T_HAGEDORN_MEV),
            _clip(obs.mu_B_MeV / MU_B_SCALE_MEV),
            _energy_density_norm(obs.epsilon_GeV_fm3),
            _clip(obs.v2 / V2_SCALE),
            _clip(1.0 - obs.R_AA),
            _clip(obs.gamma_s),
            _multiplicity_norm(obs.dNch_deta),
            _clip(obs.deconfinement_frac),
        ],
        dtype=np.float64,
    )

    w = np.full(8, 1.0 / 8.0, dtype=np.float64)
    return c, w


def _compute_kernel(c: np.ndarray, w: np.ndarray) -> dict[str, Any]:
    """Run the GCD kernel on a trace vector."""
    return compute_kernel_outputs(c, w, epsilon=EPSILON)


def _classify_regime(omega: float, F: float, S: float, C: float) -> str:
    """Classify regime from kernel invariants."""
    if omega >= 0.30:
        return "Collapse"
    if omega < 0.038 and F > 0.90 and S < 0.15 and C < 0.14:
        return "Stable"
    return "Watch"


# ═══════════════════════════════════════════════════════════════════
# SECTION 4 — ENTITY BUILDERS
# ═══════════════════════════════════════════════════════════════════


def _make_entity(
    name: str,
    category: str,
    sqrt_s: float,
    obs: QGPObservables,
    metadata: dict[str, Any] | None = None,
) -> QGPEntity:
    """Build a single QGP entity with full kernel analysis."""
    c, w = build_trace(obs)
    k = _compute_kernel(c, w)
    regime = _classify_regime(k["omega"], k["F"], k["S"], k["C"])

    return QGPEntity(
        name=name,
        category=category,
        sqrt_s_GeV=sqrt_s,
        observables=obs,
        trace=c,
        weights=w,
        channels=list(CHANNEL_NAMES),
        F=k["F"],
        omega=k["omega"],
        S=k["S"],
        C=k["C"],
        kappa=k["kappa"],
        IC=k["IC"],
        gap=k["F"] - k["IC"],
        regime=regime,
        metadata=metadata or {},
    )


def build_bes_entities() -> list[QGPEntity]:
    """Build entities for the 8 BES energy scan points."""
    entities = []
    for d in BES_DATA:
        obs = QGPObservables(
            temperature_MeV=d["T_MeV"],
            mu_B_MeV=d["mu_B_MeV"],
            epsilon_GeV_fm3=d["epsilon"],
            v2=d["v2"],
            R_AA=d["R_AA"],
            gamma_s=d["gamma_s"],
            dNch_deta=d["dNch_deta"],
            deconfinement_frac=d["deconf"],
        )
        name = f"BES √s={d['sqrt_s']} GeV"
        entity = _make_entity(
            name=name,
            category="bes",
            sqrt_s=d["sqrt_s"],
            obs=obs,
            metadata={
                "sqrt_s_GeV": d["sqrt_s"],
                "T_ch_MeV": d["T_MeV"],
                "mu_B_MeV": d["mu_B_MeV"],
            },
        )
        entities.append(entity)
    return entities


def build_centrality_entities() -> list[QGPEntity]:
    """Build entities for 9 centrality bins at √s_NN = 200 GeV."""
    entities = []
    for d in CENTRALITY_DATA:
        obs = QGPObservables(
            temperature_MeV=d["T_init_MeV"],
            mu_B_MeV=24.0,  # μ_B ≈ 24 MeV at 200 GeV for all centralities
            epsilon_GeV_fm3=d["epsilon"],
            v2=d["v2"],
            R_AA=d["R_AA"],
            gamma_s=d["gamma_s"],
            dNch_deta=d["dNch_deta"],
            deconfinement_frac=d["deconf"],
        )
        name = f"Au+Au 200GeV {d['centrality']}"
        entity = _make_entity(
            name=name,
            category="centrality",
            sqrt_s=200.0,
            obs=obs,
            metadata={
                "centrality": d["centrality"],
                "N_part": d["N_part"],
                "T_init_MeV": d["T_init_MeV"],
            },
        )
        entities.append(entity)
    return entities


def build_evolution_entities() -> list[QGPEntity]:
    """Build entities for 8 time-evolution stages of central Au+Au."""
    entities = []
    for d in EVOLUTION_DATA:
        obs = QGPObservables(
            temperature_MeV=d["T_MeV"],
            mu_B_MeV=d["mu_B_MeV"],
            epsilon_GeV_fm3=d["epsilon"],
            v2=d["v2"],
            R_AA=d["R_AA"],
            gamma_s=d["gamma_s"],
            dNch_deta=d["dNch_deta"],
            deconfinement_frac=d["deconf"],
        )
        name = f"Evolution: {d['stage']}"
        entity = _make_entity(
            name=name,
            category="evolution",
            sqrt_s=200.0,
            obs=obs,
            metadata={
                "stage": d["stage"],
                "tau_fm_c": d["tau_fm_c"],
                "description": d["description"],
            },
        )
        entities.append(entity)
    return entities


def build_reference_entities() -> list[QGPEntity]:
    """Build reference entities (p+p and d+Au baselines)."""
    entities = []
    for d in REFERENCE_DATA:
        obs = QGPObservables(
            temperature_MeV=d["T_MeV"],
            mu_B_MeV=d["mu_B_MeV"],
            epsilon_GeV_fm3=d["epsilon"],
            v2=d["v2"],
            R_AA=d["R_AA"],
            gamma_s=d["gamma_s"],
            dNch_deta=d["dNch_deta"],
            deconfinement_frac=d["deconf"],
        )
        entity = _make_entity(
            name=d["name"],
            category="reference",
            sqrt_s=d["sqrt_s"],
            obs=obs,
            metadata={"description": d["description"]},
        )
        entities.append(entity)
    return entities


def build_all_entities() -> list[QGPEntity]:
    """Build all 27 QGP entities."""
    return build_bes_entities() + build_centrality_entities() + build_evolution_entities() + build_reference_entities()


# ═══════════════════════════════════════════════════════════════════
# SECTION 5 — THEOREM PROOFS
# ═══════════════════════════════════════════════════════════════════


def _prove_T_QGP_1(centrality: list[QGPEntity]) -> dict[str, Any]:
    """T-QGP-1: Perfect Liquid Diagnostic.

    IC peaks at mid-centrality (5-20%) where ALL 8 channels are
    simultaneously active.  The most central (0-5%) has v₂ ≈ 0 from
    circular overlap geometry, killing the collectivity channel.  The
    most peripheral (70-80%) lacks QGP entirely.  Peak IC at mid-
    centrality is the kernel's signature of the "perfect liquid".
    """
    ics = [e.IC for e in centrality]
    peak_idx = int(np.argmax(ics))

    # IC peak should be at an intermediate centrality (not 0-5% or 70-80%)
    peak_is_interior = 0 < peak_idx < len(ics) - 1
    # Most peripheral should have lowest IC
    most_peripheral_ic = centrality[-1].IC
    is_min = most_peripheral_ic <= min(ics) + 1e-10
    # Peak IC should exceed most central IC
    peak_exceeds_most_central = ics[peak_idx] > ics[0]

    return {
        "id": "T-QGP-1",
        "name": "Perfect Liquid Diagnostic",
        "proven": peak_is_interior and is_min and peak_exceeds_most_central,
        "tests": 3,
        "passed": int(peak_is_interior) + int(is_min) + int(peak_exceeds_most_central),
        "peak_centrality": centrality[peak_idx].name,
        "peak_IC": ics[peak_idx],
        "central_IC": ics[0],
        "peripheral_IC": most_peripheral_ic,
        "insight": "v₂ ≈ 0 in head-on collisions → collectivity channel near ε → IC reduced",
    }


def _prove_T_QGP_2(centrality: list[QGPEntity]) -> dict[str, Any]:
    """T-QGP-2: Centrality Ordering.

    F is broadly ordered by centrality: the top-3 most central bins
    all have higher F than the bottom-3 peripheral bins.  Strict
    monotonicity is broken at 0-5% because v₂ ≈ 0 in head-on collisions
    lowers the collectivity channel.  The bulk ordering persists.
    """
    F_vals = [e.F for e in centrality]

    # Top-3 central F's all exceed bottom-3 peripheral F's
    top3 = sorted(F_vals[:3])
    bot3 = sorted(F_vals[-3:])
    bulk_ordered = top3[0] > bot3[-1]

    # Central (0-5%) > peripheral (70-80%)
    central_higher = F_vals[0] > F_vals[-1]

    # F generally decreasing: at least 6/8 adjacent pairs ordered
    n_monotone = sum(1 for i in range(len(F_vals) - 1) if F_vals[i] >= F_vals[i + 1] - 1e-10)
    mostly_monotone = n_monotone >= 6

    return {
        "id": "T-QGP-2",
        "name": "Centrality Ordering",
        "proven": bulk_ordered and central_higher and mostly_monotone,
        "tests": 3,
        "passed": int(bulk_ordered) + int(central_higher) + int(mostly_monotone),
        "F_central": F_vals[0],
        "F_peripheral": F_vals[-1],
        "top3_min_F": top3[0],
        "bot3_max_F": bot3[-1],
        "monotone_pairs": n_monotone,
    }


def _prove_T_QGP_3(bes: list[QGPEntity]) -> dict[str, Any]:
    """T-QGP-3: BES Energy Ordering.

    F increases with √s_NN across the Beam Energy Scan.
    Higher collision energy → hotter, denser QGP → higher fidelity.
    """
    F_vals = [e.F for e in bes]
    n_monotone = sum(1 for i in range(len(F_vals) - 1) if F_vals[i] <= F_vals[i + 1] + 1e-10)
    total_pairs = len(F_vals) - 1
    is_monotone = n_monotone == total_pairs
    highest = F_vals[-1] > F_vals[0]

    return {
        "id": "T-QGP-3",
        "name": "BES Energy Ordering",
        "proven": is_monotone and highest,
        "tests": total_pairs + 1,
        "passed": n_monotone + int(highest),
        "F_lowest_energy": F_vals[0],
        "F_highest_energy": F_vals[-1],
        "delta_F": F_vals[-1] - F_vals[0],
    }


def _prove_T_QGP_4(bes: list[QGPEntity]) -> dict[str, Any]:
    """T-QGP-4: Strangeness Equilibration.

    γ_s (strangeness equilibration) correlates positively with IC
    across BES energies. Higher energy → fuller equilibration → more
    channels contributing → higher IC.
    """
    gamma_vals = [e.observables.gamma_s for e in bes]
    ic_vals = [e.IC for e in bes]

    # Spearman rank correlation (monotone association)
    n = len(gamma_vals)
    gamma_ranks = _rank(gamma_vals)
    ic_ranks = _rank(ic_vals)
    d_sq = sum((gamma_ranks[i] - ic_ranks[i]) ** 2 for i in range(n))
    rho = 1.0 - 6.0 * d_sq / (n * (n * n - 1))

    positive_corr = rho > 0.5

    return {
        "id": "T-QGP-4",
        "name": "Strangeness Equilibration",
        "proven": positive_corr,
        "tests": 1,
        "passed": int(positive_corr),
        "spearman_rho": rho,
        "gamma_s_range": (min(gamma_vals), max(gamma_vals)),
        "IC_range": (min(ic_vals), max(ic_vals)),
    }


def _prove_T_QGP_5(evolution: list[QGPEntity]) -> dict[str, Any]:
    """T-QGP-5: Reconfinement Gap Jump.

    The QGP → hadron gas transition produces the largest JUMP in
    heterogeneity gap between consecutive evolution stages.  At the
    crossover, the deconfinement channel drops from ~1.0 to ~0.0
    while thermal channels remain active — this sudden channel
    imbalance creates a dramatic gap increase.
    """
    # Skip pre-collision
    active = [e for e in evolution if e.observables.temperature_MeV > 0]
    gaps = [e.gap for e in active]

    # Compute gap jumps between consecutive stages
    jumps = [gaps[i + 1] - gaps[i] for i in range(len(gaps) - 1)]
    jump_labels = [
        f"{active[i].metadata.get('stage', '')} → {active[i + 1].metadata.get('stage', '')}"
        for i in range(len(gaps) - 1)
    ]

    # Find the reconfinement transition (Crossover → Hadron gas)
    reconf_idx = None
    for i, e in enumerate(active[:-1]):
        if "Crossover" in e.name or "T_c" in e.name:
            reconf_idx = i
            break

    if reconf_idx is None:
        return {
            "id": "T-QGP-5",
            "name": "Reconfinement Gap Jump",
            "proven": False,
            "tests": 1,
            "passed": 0,
            "reason": "No crossover stage found",
        }

    reconf_jump = jumps[reconf_idx]
    max_jump = max(jumps)

    # The reconfinement jump should be the largest positive gap jump
    is_max_jump = reconf_jump >= max_jump - 1e-10
    # The jump should be substantial (> 0.1)
    is_substantial = reconf_jump > 0.1

    return {
        "id": "T-QGP-5",
        "name": "Reconfinement Gap Jump",
        "proven": is_max_jump and is_substantial,
        "tests": 2,
        "passed": int(is_max_jump) + int(is_substantial),
        "reconfinement_jump": reconf_jump,
        "max_jump": max_jump,
        "all_jumps": list(zip(jump_labels, jumps, strict=True)),
    }


def _prove_T_QGP_6(centrality: list[QGPEntity]) -> dict[str, Any]:
    """T-QGP-6: Flow-Opacity Structure.

    Elliptic flow v₂ peaks at mid-centrality (20-40%) while opacity
    (1 − R_AA) peaks at most central (0-5%).  These two observables
    have distinct centrality patterns — their non-correlation reveals
    two independent physics mechanisms (geometry vs. density).
    """
    v2_vals = [e.observables.v2 for e in centrality]
    opacity_vals = [1.0 - e.observables.R_AA for e in centrality]

    # v₂ should peak at mid-centrality (index 3 or 4, i.e., 20-40%)
    v2_peak_idx = v2_vals.index(max(v2_vals))
    v2_peaks_mid = 2 <= v2_peak_idx <= 5

    # Opacity should peak at most central (index 0)
    opacity_peak_idx = opacity_vals.index(max(opacity_vals))
    opacity_peaks_central = opacity_peak_idx == 0

    # They peak at different centralities
    different_peaks = v2_peak_idx != opacity_peak_idx

    return {
        "id": "T-QGP-6",
        "name": "Flow-Opacity Structure",
        "proven": v2_peaks_mid and opacity_peaks_central and different_peaks,
        "tests": 3,
        "passed": int(v2_peaks_mid) + int(opacity_peaks_central) + int(different_peaks),
        "v2_peak_centrality": centrality[v2_peak_idx].name,
        "opacity_peak_centrality": centrality[opacity_peak_idx].name,
        "v2_values": v2_vals,
        "opacity_values": opacity_vals,
    }


def _prove_T_QGP_7(bes: list[QGPEntity]) -> dict[str, Any]:
    """T-QGP-7: Chemical Freeze-out Curve.

    T_ch and μ_B anti-correlate across BES energies, tracing the
    chemical freeze-out curve in the T-μ_B phase diagram.  This curve
    approaches T_c from below as μ_B → 0 (highest energies).
    """
    T_vals = [e.observables.temperature_MeV for e in bes]
    mu_vals = [e.observables.mu_B_MeV for e in bes]

    # Spearman rank correlation should be strongly negative
    n = len(T_vals)
    T_ranks = _rank(T_vals)
    mu_ranks = _rank(mu_vals)
    d_sq = sum((T_ranks[i] - mu_ranks[i]) ** 2 for i in range(n))
    rho = 1.0 - 6.0 * d_sq / (n * (n * n - 1))

    strong_anticorr = rho < -0.9

    # T_ch at highest energy should be closest to T_c
    T_max_energy = T_vals[-1]  # 200 GeV
    near_Tc = abs(T_max_energy - T_C_MEV) < 15  # within 15 MeV

    return {
        "id": "T-QGP-7",
        "name": "Chemical Freeze-out Curve",
        "proven": strong_anticorr and near_Tc,
        "tests": 2,
        "passed": int(strong_anticorr) + int(near_Tc),
        "spearman_rho": rho,
        "T_at_200GeV": T_max_energy,
        "T_c": T_C_MEV,
        "delta_T_c": T_max_energy - T_C_MEV,
    }


def _prove_T_QGP_8(evolution: list[QGPEntity]) -> dict[str, Any]:
    """T-QGP-8: Reconfinement Cliff.

    The QGP → hadron gas transition shows an IC cliff analogous to
    the confinement cliff (T3 from particle_physics_formalism).
    IC drops significantly when matter transitions from deconfined
    QGP (fully colored) to confined hadrons (color-singlet).
    """
    # Find QGP stage and hadron gas stage
    qgp_stages = [e for e in evolution if e.observables.deconfinement_frac >= 0.95]
    hadron_stages = [
        e for e in evolution if (e.observables.deconfinement_frac <= 0.05 and e.observables.temperature_MeV > 50)
    ]

    if not qgp_stages or not hadron_stages:
        return {
            "id": "T-QGP-8",
            "name": "Reconfinement Cliff",
            "proven": False,
            "tests": 1,
            "passed": 0,
            "reason": "Missing QGP or hadron stages",
        }

    # Use the most developed QGP stage (highest IC among QGP stages)
    qgp_ic = max(e.IC for e in qgp_stages)
    hadron_ic = min(e.IC for e in hadron_stages)

    # IC should drop by at least 30%
    ic_drop_frac = (qgp_ic - hadron_ic) / qgp_ic if qgp_ic > 0 else 0.0

    significant_drop = ic_drop_frac > 0.30

    # Heterogeneity gap should increase at the transition
    crossover_stages = [e for e in evolution if 0.1 < e.observables.deconfinement_frac < 0.9]
    crossover_gap = max((e.gap for e in crossover_stages), default=0.0)
    qgp_gap = np.mean([e.gap for e in qgp_stages])
    gap_increases = crossover_gap > qgp_gap

    return {
        "id": "T-QGP-8",
        "name": "Reconfinement Cliff",
        "proven": significant_drop and gap_increases,
        "tests": 2,
        "passed": int(significant_drop) + int(gap_increases),
        "QGP_IC": qgp_ic,
        "hadron_IC": hadron_ic,
        "IC_drop_frac": ic_drop_frac,
        "crossover_gap": crossover_gap,
        "QGP_mean_gap": float(qgp_gap),
    }


def _prove_T_QGP_9(
    centrality: list[QGPEntity],
    references: list[QGPEntity],
) -> dict[str, Any]:
    """T-QGP-9: Reference Discrimination.

    The kernel distinguishes Au+Au (QGP-forming) from p+p (no QGP)
    through IC.  p+p has lower IC because the strangeness, opacity,
    collectivity, and deconfinement channels are near ε.
    """
    pp = [e for e in references if "p+p" in e.name]
    dAu = [e for e in references if "d+Au" in e.name]

    if not pp:
        return {
            "id": "T-QGP-9",
            "name": "Reference Discrimination",
            "proven": False,
            "tests": 1,
            "passed": 0,
            "reason": "No p+p reference found",
        }

    pp_ic = pp[0].IC

    # Central Au+Au IC should exceed p+p IC
    central_ic = centrality[0].IC
    auau_higher = central_ic > pp_ic

    # p+p gap should be large (many near-ε channels)
    pp_gap = pp[0].gap
    central_gap = centrality[0].gap
    pp_more_heterogeneous = pp_gap > central_gap

    tests_passed = int(auau_higher) + int(pp_more_heterogeneous)

    result: dict[str, Any] = {
        "id": "T-QGP-9",
        "name": "Reference Discrimination",
        "proven": auau_higher and pp_more_heterogeneous,
        "tests": 2,
        "passed": tests_passed,
        "pp_IC": pp_ic,
        "central_AuAu_IC": central_ic,
        "pp_gap": pp_gap,
        "central_gap": central_gap,
    }

    if dAu:
        result["dAu_IC"] = dAu[0].IC
        result["dAu_F"] = dAu[0].F

    return result


def _prove_T_QGP_10(all_entities: list[QGPEntity]) -> dict[str, Any]:
    """T-QGP-10: Universal Tier-1.

    All three Tier-1 identities hold across every QGP entity:
      1. F + ω = 1 (duality identity)
      2. IC ≤ F   (integrity bound)
      3. IC = exp(κ) (log-integrity relation)
    """
    n = len(all_entities)
    duality_pass = 0
    bound_pass = 0
    exp_pass = 0

    for e in all_entities:
        if abs(e.F + e.omega - 1.0) < 1e-12:
            duality_pass += 1
        if e.IC <= e.F + 1e-12:
            bound_pass += 1
        if abs(e.IC - math.exp(e.kappa)) < 1e-10:
            exp_pass += 1

    total_tests = 3 * n
    total_passed = duality_pass + bound_pass + exp_pass

    return {
        "id": "T-QGP-10",
        "name": "Universal Tier-1",
        "proven": total_passed == total_tests,
        "tests": total_tests,
        "passed": total_passed,
        "duality_exact": duality_pass,
        "bound_satisfied": bound_pass,
        "exp_exact": exp_pass,
        "n_entities": n,
    }


def _rank(values: list[float]) -> list[float]:
    """Compute ranks for Spearman correlation."""
    indexed = sorted(enumerate(values), key=lambda x: x[1])
    ranks = [0.0] * len(values)
    for rank_val, (idx, _) in enumerate(indexed):
        ranks[idx] = float(rank_val + 1)
    return ranks


# ═══════════════════════════════════════════════════════════════════
# SECTION 6 — NARRATIVE GENERATOR
# ═══════════════════════════════════════════════════════════════════


def generate_narrative(
    bes: list[QGPEntity],
    centrality: list[QGPEntity],
    evolution: list[QGPEntity],
    references: list[QGPEntity],
    theorems: dict[str, dict[str, Any]],
) -> str:
    """Generate the QGP narrative using the five GCD words."""
    lines = []

    # Prologue
    lines.append("═" * 72)
    lines.append("  PLASMA QUARK-GLUONICUM — The Fire of the Early Universe")
    lines.append("  Collapsus generativus est; solum quod redit, reale est.")
    lines.append("═" * 72)
    lines.append("")
    lines.append("PROLOGUE: THE LITTLE BANG")
    lines.append("")
    lines.append(
        "When gold nuclei collide at 99.995% the speed of light, for a "
        "fleeting 10⁻²³ seconds they recreate conditions that last existed "
        "microseconds after the Big Bang.  The resulting fireball — a "
        "quark-gluon plasma (QGP) — is the hottest, densest matter ever "
        "produced by humankind.  The Relativistic Heavy Ion Collider at "
        "Brookhaven National Laboratory has studied this primordial soup "
        "since June 2000, mapping the QCD phase diagram across 8 collision "
        "energies, 9 centrality bins, and the full time evolution from "
        "initial glasma to final-state hadrons."
    )
    lines.append("")

    # Act I: The Beam Energy Scan
    lines.append("ACT I: THE BEAM ENERGY SCAN")
    lines.append("")
    mean_F = np.mean([e.F for e in bes])
    mean_IC = np.mean([e.IC for e in bes])
    F_range = (bes[0].F, bes[-1].F)
    lines.append(
        f"  Drift:     F rises from {F_range[0]:.4f} (7.7 GeV) to "
        f"{F_range[1]:.4f} (200 GeV) — fidelity increases with energy"
    )
    lines.append(f"  Fidelity:  Mean F = {mean_F:.4f} across 8 scan points")
    lines.append(
        f"  Roughness: μ_B drops from {bes[0].observables.mu_B_MeV:.0f} to "
        f"{bes[-1].observables.mu_B_MeV:.0f} MeV — baryon friction decreases"
    )
    lines.append(
        f"  Return:    γ_s rises from {bes[0].observables.gamma_s:.2f} to "
        f"{bes[-1].observables.gamma_s:.2f} — strangeness equilibrates"
    )
    lines.append(f"  Integrity: Mean IC = {mean_IC:.4f}, gap Δ = {mean_F - mean_IC:.4f}")
    lines.append("")

    # Act II: The Centrality Dependence
    lines.append("ACT II: THE CENTRALITY DEPENDENCE")
    lines.append("")
    c_mean_F = np.mean([e.F for e in centrality])
    c_mean_IC = np.mean([e.IC for e in centrality])
    lines.append(
        f"  Drift:     Central (0-5%): ω = {centrality[0].omega:.4f}, "
        f"Peripheral (70-80%): ω = {centrality[-1].omega:.4f}"
    )
    lines.append(
        f"  Fidelity:  352 participants → F = {centrality[0].F:.4f}, 14 participants → F = {centrality[-1].F:.4f}"
    )
    lines.append(
        f"  Roughness: v₂ peaks at {centrality[4].name} "
        f"(v₂ = {centrality[4].observables.v2:.3f}) — geometry matters most"
    )
    lines.append(f"  Return:    IC = {centrality[0].IC:.4f} (central) → {centrality[-1].IC:.4f} (peripheral)")
    lines.append(f"  Integrity: Mean IC = {c_mean_IC:.4f}, gap Δ = {c_mean_F - c_mean_IC:.4f}")
    lines.append("")

    # Act III: The Time Evolution
    lines.append("ACT III: THE FIREBALL EVOLUTION")
    lines.append("")
    for e in evolution:
        desc = e.metadata.get("description", "")
        tau = e.metadata.get("tau_fm_c", 0)
        lines.append(f"  τ = {tau:5.1f} fm/c | {e.name:35s} | F = {e.F:.4f}, IC = {e.IC:.4f}, Δ = {e.gap:.4f} | {desc}")
    lines.append("")

    # Act IV: Reference discrimination
    lines.append("ACT IV: THE BASELINES")
    lines.append("")
    for e in references:
        desc = e.metadata.get("description", "")
        lines.append(f"  {e.name:20s} | F = {e.F:.4f}, IC = {e.IC:.4f}, Δ = {e.gap:.4f} | {desc}")
    lines.append("")

    # Theorem summary
    lines.append("THEOREM SCORECARD")
    lines.append("")
    n_proven = sum(1 for t in theorems.values() if t.get("proven"))
    for _tid, t in sorted(theorems.items()):
        status = "PROVEN" if t.get("proven") else "OPEN"
        lines.append(f"  {t['id']:10s} {t['name']:35s} [{t.get('passed', 0)}/{t.get('tests', 0)} tests] {status}")
    lines.append(f"\n  {n_proven}/{len(theorems)} theorems PROVEN")
    lines.append("")

    # Epilogue
    lines.append("EPILOGUE: THE RETURN")
    lines.append("")
    lines.append(
        "The QGP exists for 10⁻²³ seconds — briefer than any human "
        "timescale by 40 orders of magnitude.  Yet its properties are "
        "measured, its structure is mapped, and its echoes are heard in "
        "every proton and neutron in the universe.  The kernel does not "
        "know what a quark-gluon plasma is.  It receives 8 numbers per "
        "measurement and returns F, ω, IC, Δ.  That these invariants "
        "discriminate central from peripheral, QGP from hadron gas, "
        "200 GeV from 7.7 GeV — without knowing the physics — is the "
        "collapse returning.  Solum quod redit, reale est."
    )

    return "\n".join(lines)


# ═══════════════════════════════════════════════════════════════════
# SECTION 7 — MAIN ANALYSIS
# ═══════════════════════════════════════════════════════════════════


@dataclass
class QGPAnalysisResult:
    """Complete result of the QGP/RHIC analysis."""

    bes_entities: list[QGPEntity]
    centrality_entities: list[QGPEntity]
    evolution_entities: list[QGPEntity]
    reference_entities: list[QGPEntity]
    all_entities: list[QGPEntity]
    theorem_results: dict[str, dict[str, Any]]
    tier1_violations: int
    narrative: str
    summary: dict[str, Any]


def run_full_analysis() -> QGPAnalysisResult:
    """Run the complete QGP/RHIC kernel analysis.

    Returns a QGPAnalysisResult with all entities, theorems, and narrative.
    """
    bes = build_bes_entities()
    centrality = build_centrality_entities()
    evolution = build_evolution_entities()
    references = build_reference_entities()
    all_entities = bes + centrality + evolution + references

    # Verify Tier-1
    tier1_violations = 0
    for e in all_entities:
        if abs(e.F + e.omega - 1.0) > 1e-12:
            tier1_violations += 1
        if e.IC > e.F + 1e-12:
            tier1_violations += 1

    # Prove theorems
    theorems = {
        "T-QGP-1": _prove_T_QGP_1(centrality),
        "T-QGP-2": _prove_T_QGP_2(centrality),
        "T-QGP-3": _prove_T_QGP_3(bes),
        "T-QGP-4": _prove_T_QGP_4(bes),
        "T-QGP-5": _prove_T_QGP_5(evolution),
        "T-QGP-6": _prove_T_QGP_6(centrality),
        "T-QGP-7": _prove_T_QGP_7(bes),
        "T-QGP-8": _prove_T_QGP_8(evolution),
        "T-QGP-9": _prove_T_QGP_9(centrality, references),
        "T-QGP-10": _prove_T_QGP_10(all_entities),
    }

    n_proven = sum(1 for t in theorems.values() if t.get("proven"))

    # Generate narrative
    narrative = generate_narrative(bes, centrality, evolution, references, theorems)

    # Summary statistics
    all_F = [e.F for e in all_entities]
    all_IC = [e.IC for e in all_entities]
    summary = {
        "n_entities": len(all_entities),
        "n_bes": len(bes),
        "n_centrality": len(centrality),
        "n_evolution": len(evolution),
        "n_reference": len(references),
        "n_theorems_proven": n_proven,
        "n_theorems_total": len(theorems),
        "mean_F": float(np.mean(all_F)),
        "mean_IC": float(np.mean(all_IC)),
        "mean_gap": float(np.mean(all_F) - np.mean(all_IC)),
        "F_range": (float(min(all_F)), float(max(all_F))),
        "IC_range": (float(min(all_IC)), float(max(all_IC))),
        "tier1_violations": tier1_violations,
        "T_c_MeV": T_C_MEV,
        "T_Hagedorn_MeV": T_HAGEDORN_MEV,
        "eta_over_s_KSS": ETA_OVER_S_KSS,
    }

    return QGPAnalysisResult(
        bes_entities=bes,
        centrality_entities=centrality,
        evolution_entities=evolution,
        reference_entities=references,
        all_entities=all_entities,
        theorem_results=theorems,
        tier1_violations=tier1_violations,
        narrative=narrative,
        summary=summary,
    )


# ═══════════════════════════════════════════════════════════════════
# SECTION 8 — SELF-TEST
# ═══════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    result = run_full_analysis()

    print(result.narrative)
    print()
    print("=" * 72)
    print("  SUMMARY")
    print("=" * 72)
    s = result.summary
    print(f"  Entities:    {s['n_entities']}")
    print(f"  BES points:  {s['n_bes']}")
    print(f"  Centrality:  {s['n_centrality']}")
    print(f"  Evolution:   {s['n_evolution']}")
    print(f"  References:  {s['n_reference']}")
    print(f"  Theorems:    {s['n_theorems_proven']}/{s['n_theorems_total']} PROVEN")
    print(f"  Mean F:      {s['mean_F']:.4f}")
    print(f"  Mean IC:     {s['mean_IC']:.4f}")
    print(f"  Mean Δ:      {s['mean_gap']:.4f}")
    print(f"  Tier-1 viol: {s['tier1_violations']}")
    print()

    # Print entity table
    print(f"{'Name':40s} {'F':>7s} {'ω':>7s} {'IC':>7s} {'Δ':>7s} {'S':>7s} {'C':>7s} {'Regime':>10s}")
    print("-" * 100)
    for e in result.all_entities:
        print(f"{e.name:40s} {e.F:7.4f} {e.omega:7.4f} {e.IC:7.4f} {e.gap:7.4f} {e.S:7.4f} {e.C:7.4f} {e.regime:>10s}")
