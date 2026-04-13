"""
Clinical Neuroscience Kernel — Tier-2 Closure

Maps 35 neurocognitive states through the GCD kernel using 10 channels
grounded in peer-reviewed clinical biomarkers. Extends the awareness-
cognition (T-AW) and consciousness coherence (T-CC) closures into the
clinical domain:  healthy baselines, altered states, disorders of
consciousness, neurodegenerative diseases, psychiatric conditions,
developmental stages, and acquired brain injuries.

Channels (10, equal weights):
    CORTICAL (neural complexity):
        0. cortical_complexity     — PCI / EEG complexity (Casarotto 2016 Ann Neurol)
        1. default_mode_integrity  — DMN functional connectivity (Raichle 2015 Annu Rev Neurosci)
        2. global_integration      — Long-range neural workspace (Dehaene & Changeux 2011 Neuron)
        3. oscillatory_hierarchy   — Cross-frequency coupling, spectral organization
                                     (Canolty & Knight 2010 Trends Cogn Sci)
    STRUCTURAL (tissue / circuit):
        4. neuroplasticity_capacity — Synaptic plasticity / LTP capacity
                                      (Pascual-Leone 2005 Annu Rev Neurosci)
        5. structural_connectivity  — DTI fractional anisotropy / white matter integrity
                                      (Basser & Pierpaoli 1996 J Magn Reson B)
    METABOLIC (energy / chemistry):
        6. neurotransmitter_tone   — Monoaminergic / glutamatergic balance
                                     (Nutt 2015 Lancet Psychiatry)
        7. metabolic_efficiency    — Cerebral metabolic rate of glucose / CBF
                                     (Raichle & Mintun 2006 Annu Rev Neurosci)
    SYSTEMIC (whole-organism coupling):
        8. autonomic_regulation    — HRV / vagal tone / heart-brain coupling
                                     (Thayer & Lane 2009 Neurosci Biobehav Rev)
        9. neuroimmune_status      — Neuroinflammation level, INVERTED: 1 = healthy
                                     (Dantzer 2008 Nat Rev Neurosci)

All channel values are normalized to [0, 1] and ε-clamped. Values are
grounded in published clinical measurements where available; see inline
citations per entity.

Entity catalog: 35 neurocognitive states across 7 categories

Derivation chain: Axiom-0 → frozen_contract → kernel_optimized → this module
"""

from __future__ import annotations

import sys
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np

# ── Path setup ────────────────────────────────────────────────────
_WORKSPACE = Path(__file__).resolve().parents[2]
if str(_WORKSPACE / "src") not in sys.path:
    sys.path.insert(0, str(_WORKSPACE / "src"))

from umcp.frozen_contract import EPSILON  # noqa: E402
from umcp.kernel_optimized import (  # noqa: E402
    OptimizedKernelComputer,
    diagnose,
)

# ═══════════════════════════════════════════════════════════════════
# CHANNEL DEFINITIONS
# ═══════════════════════════════════════════════════════════════════

CORTICAL_CHANNELS: list[str] = [
    "cortical_complexity",
    "default_mode_integrity",
    "global_integration",
    "oscillatory_hierarchy",
]

STRUCTURAL_CHANNELS: list[str] = [
    "neuroplasticity_capacity",
    "structural_connectivity",
]

METABOLIC_CHANNELS: list[str] = [
    "neurotransmitter_tone",
    "metabolic_efficiency",
]

SYSTEMIC_CHANNELS: list[str] = [
    "autonomic_regulation",
    "neuroimmune_status",
]

ALL_CHANNELS: list[str] = CORTICAL_CHANNELS + STRUCTURAL_CHANNELS + METABOLIC_CHANNELS + SYSTEMIC_CHANNELS

N_CHANNELS: int = 10
N_CORTICAL: int = 4
N_STRUCTURAL: int = 2
N_METABOLIC: int = 2
N_SYSTEMIC: int = 2

# Equal weights — no channel is privileged a priori
WEIGHTS: np.ndarray = np.ones(N_CHANNELS) / N_CHANNELS


# ═══════════════════════════════════════════════════════════════════
# CLINICAL STATE DATA
# ═══════════════════════════════════════════════════════════════════


@dataclass(frozen=True)
class NeurocognitiveState:
    """A clinical neurocognitive state with 10-channel trace vector.

    Each state represents a clinically recognized condition or baseline,
    with channel values grounded in peer-reviewed measurements.
    """

    name: str
    category: str  # healthy / altered / doc / neurodegen / psychiatric / developmental / tbi
    channels: tuple[float, ...]  # length 10, in channel order

    @property
    def trace(self) -> np.ndarray:
        """Return clamped [ε, 1−ε] trace vector."""
        return np.clip(np.array(self.channels, dtype=float), EPSILON, 1 - EPSILON)

    @property
    def cortical_mean(self) -> float:
        """Mean of cortical channels (0-3)."""
        return float(np.mean(self.trace[:N_CORTICAL]))

    @property
    def structural_mean(self) -> float:
        """Mean of structural channels (4-5)."""
        return float(np.mean(self.trace[N_CORTICAL : N_CORTICAL + N_STRUCTURAL]))

    @property
    def metabolic_mean(self) -> float:
        """Mean of metabolic channels (6-7)."""
        return float(np.mean(self.trace[N_CORTICAL + N_STRUCTURAL : N_CORTICAL + N_STRUCTURAL + N_METABOLIC]))

    @property
    def systemic_mean(self) -> float:
        """Mean of systemic channels (8-9)."""
        return float(np.mean(self.trace[-N_SYSTEMIC:]))


# ── Channel value justifications (peer-reviewed sources) ──────────
#
# cortical_complexity:     PCI (Perturbational Complexity Index) from TMS-EEG.
#   Casarotto S et al. (2016) Ann Neurol 80:718-729. PCI* threshold ~0.31
#   for consciousness. Healthy waking ~0.44-0.67. Coma ~0.13-0.19.
#
# default_mode_integrity:  DMN resting-state functional connectivity.
#   Raichle ME (2015) Annu Rev Neurosci 38:433-447.
#   Greicius MD et al. (2004) PNAS 101:4637-4642 (AD disruption).
#   Buckner RL et al. (2008) Ann NY Acad Sci 1124:1-38.
#
# global_integration:      Global Neuronal Workspace integration metric.
#   Dehaene S, Changeux JP (2011) Neuron 70:200-227.
#   Mashour GA et al. (2020) Neuron 105:776-798.
#
# oscillatory_hierarchy:   Cross-frequency coupling (theta-gamma) and
#   spectral organization. Canolty RT, Knight RT (2010) Trends Cogn Sci
#   14:506-515. Buzsáki G, Draguhn A (2004) Science 304:1926-1929.
#
# neuroplasticity_capacity: Synaptic plasticity / LTP-like mechanisms.
#   Pascual-Leone A et al. (2005) Annu Rev Neurosci 28:377-401.
#   Kolb B, Gibb R (2011) Curr Opin Neurobiol 21:187-193.
#
# structural_connectivity: DTI fractional anisotropy for white matter.
#   Basser PJ, Pierpaoli C (1996) J Magn Reson B 111:209-219.
#
# neurotransmitter_tone:   Monoaminergic / glutamatergic system function.
#   Nutt DJ et al. (2015) Lancet Psychiatry 2:743-755.
#   Dantzer R et al. (2008) Nat Rev Neurosci 9:46-56.
#
# metabolic_efficiency:    CMRglc / CBF (cerebral metabolic rate / blood flow).
#   Raichle ME, Mintun MA (2006) Annu Rev Neurosci 29:449-476.
#   Laureys S et al. (2004) Curr Opin Neurol 17:133-140 (DOC metabolism).
#
# autonomic_regulation:    HRV, vagal tone, sympathovagal balance.
#   Thayer JF, Lane RD (2009) Neurosci Biobehav Rev 33:81-88.
#   Porges SW (2007) Biol Psychol 74:301-307 (polyvagal theory).
#
# neuroimmune_status:      Neuroinflammation (INVERTED: 1 = low inflammation).
#   Dantzer R et al. (2008) Nat Rev Neurosci 9:46-56.
#   Miller AH, Raison CL (2016) Nat Rev Immunol 16:22-34.
#

# fmt: off
NEUROCOGNITIVE_CATALOG: list[NeurocognitiveState] = [
    # ═══════════════════════════════════════════════════════════════
    # HEALTHY BASELINES
    # Channel order: cortical_complexity, default_mode_integrity,
    #   global_integration, oscillatory_hierarchy,
    #   neuroplasticity_capacity, structural_connectivity,
    #   neurotransmitter_tone, metabolic_efficiency,
    #   autonomic_regulation, neuroimmune_status
    # ═══════════════════════════════════════════════════════════════

    # Young adult: PCI ~0.55 (Casarotto 2016), strong DMN (Raichle 2015),
    # high integration, intact oscillations, peak plasticity, full WM,
    # balanced NT, efficient metabolism, good HRV, low inflammation
    NeurocognitiveState("Young adult healthy",  "healthy",
        (0.92, 0.90, 0.88, 0.85, 0.90, 0.92, 0.88, 0.90, 0.85, 0.92)),

    # Middle-aged healthy: slight decline in plasticity and oscillatory
    # power (Salthouse 2009 Psychol Rev), otherwise preserved
    NeurocognitiveState("Middle-aged healthy",  "healthy",
        (0.88, 0.85, 0.85, 0.80, 0.75, 0.88, 0.85, 0.85, 0.80, 0.85)),

    # Elderly healthy (successful aging): preserved cognition, reduced plasticity
    # and NT tone. Nyberg L et al. (2012) Trends Cogn Sci 16:292-305.
    NeurocognitiveState("Elderly healthy",      "healthy",
        (0.82, 0.78, 0.75, 0.70, 0.55, 0.80, 0.72, 0.78, 0.70, 0.72)),

    # Elite athlete: enhanced autonomic regulation, superior HRV
    # Plews DJ et al. (2013) Int J Sports Physiol Perform 8:688-694.
    NeurocognitiveState("Elite athlete",        "healthy",
        (0.88, 0.85, 0.85, 0.82, 0.85, 0.90, 0.88, 0.92, 0.95, 0.90)),

    # Expert meditator: enhanced DMN regulation, increased integration.
    # Brewer JA et al. (2011) PNAS 108:20254. Lutz A et al. (2004) PNAS 101:16369.
    NeurocognitiveState("Expert meditator",     "healthy",
        (0.90, 0.95, 0.92, 0.90, 0.82, 0.88, 0.90, 0.88, 0.92, 0.90)),

    # ═══════════════════════════════════════════════════════════════
    # ALTERED STATES
    # ═══════════════════════════════════════════════════════════════

    # NREM N3 deep sleep: PCI drops ~50% (Casali AG et al. 2013 Sci Transl Med),
    # reduced global integration, DMN partially maintained
    NeurocognitiveState("NREM deep sleep",      "altered",
        (0.30, 0.55, 0.25, 0.35, 0.70, 0.90, 0.60, 0.65, 0.75, 0.90)),

    # REM sleep: restored complexity near waking, DMN active (dreaming),
    # high oscillatory power. Hobson JA, Friston KJ (2012) Nat Rev Neurosci.
    NeurocognitiveState("REM sleep",            "altered",
        (0.72, 0.70, 0.65, 0.75, 0.68, 0.90, 0.55, 0.70, 0.65, 0.88)),

    # General anesthesia (propofol): PCI drops to ~0.18 (Casarotto 2016),
    # massive global integration loss. Mashour GA (2020) Neuron.
    NeurocognitiveState("General anesthesia",   "altered",
        (0.15, 0.20, 0.10, 0.12, 0.65, 0.88, 0.25, 0.55, 0.50, 0.85)),

    # Psilocybin state: increased complexity (entropy), DECREASED DMN.
    # Carhart-Harris RL et al. (2014) Front Hum Neurosci 8:20 (entropic brain).
    # Carhart-Harris RL et al. (2012) PNAS 109:2138 (decreased DMN).
    NeurocognitiveState("Psilocybin state",     "altered",
        (0.88, 0.30, 0.72, 0.90, 0.80, 0.88, 0.40, 0.85, 0.55, 0.80)),

    # Flow state: high integration, focused oscillations, optimal NT.
    # Csikszentmihalyi M (1990). Ulrich M et al. (2014) NeuroImage 100:170.
    NeurocognitiveState("Flow state",           "altered",
        (0.90, 0.60, 0.92, 0.88, 0.82, 0.90, 0.92, 0.90, 0.88, 0.88)),

    # Hypnotic trance: altered DMN, maintained cortical function.
    # Rainville P et al. (2002) Cognition 82:B15-B18.
    NeurocognitiveState("Hypnotic trance",      "altered",
        (0.78, 0.45, 0.60, 0.72, 0.75, 0.88, 0.70, 0.82, 0.70, 0.85)),

    # ═══════════════════════════════════════════════════════════════
    # DISORDERS OF CONSCIOUSNESS (DOC)
    # Giacino JT et al. (2014) Nat Rev Neurol 10:99-114.
    # ═══════════════════════════════════════════════════════════════

    # Coma: PCI very low (~0.13), no organized waking patterns.
    # Laureys S et al. (2004) Curr Opin Neurol 17:133-140.
    NeurocognitiveState("Coma",                 "doc",
        (0.08, 0.10, 0.05, 0.08, 0.55, 0.75, 0.30, 0.35, 0.40, 0.60)),

    # Vegetative / UWS: preserved sleep-wake cycles but no awareness.
    # Owen AM et al. (2006) Science 313:1402 (covert awareness).
    # PCI below 0.31 threshold. Laureys S et al. (2010) BMC Med 8:68.
    NeurocognitiveState("Vegetative state",     "doc",
        (0.15, 0.15, 0.10, 0.12, 0.50, 0.70, 0.35, 0.40, 0.45, 0.55)),

    # MCS: above PCI threshold in some networks, fluctuating awareness.
    # Giacino JT et al. (2002) Neurology 58:349-353.
    NeurocognitiveState("Minimally conscious",  "doc",
        (0.35, 0.25, 0.22, 0.28, 0.48, 0.68, 0.40, 0.48, 0.45, 0.55)),

    # Emergence from MCS: recovering integration, improving DMN.
    # Schiff ND (2010) Curr Opin Neurol 23:560-569.
    NeurocognitiveState("Emerging from MCS",    "doc",
        (0.50, 0.40, 0.38, 0.42, 0.52, 0.72, 0.50, 0.55, 0.50, 0.58)),

    # Locked-in syndrome: PRESERVED cortical function, motor disconnect.
    # Bauer G et al. (1979) J Neurol 221:77-91.
    # Laureys S et al. (2005) Brain 128:386-398 (near-normal metabolism).
    NeurocognitiveState("Locked-in syndrome",   "doc",
        (0.85, 0.82, 0.78, 0.72, 0.55, 0.60, 0.70, 0.78, 0.55, 0.55)),

    # ═══════════════════════════════════════════════════════════════
    # NEURODEGENERATIVE DISEASES
    # ═══════════════════════════════════════════════════════════════

    # MCI: subtle memory decline, preserved core function.
    # Petersen RC (2004) J Intern Med 256:183-194.
    # Jack CR et al. (2018) Alzheimers Dement 14:535-562 (ATN framework).
    NeurocognitiveState("Mild cognitive impairment", "neurodegen",
        (0.78, 0.65, 0.72, 0.68, 0.55, 0.78, 0.72, 0.75, 0.68, 0.65)),

    # Alzheimer's mild: DMN disruption is an early biomarker.
    # Greicius MD et al. (2004) PNAS 101:4637. Jack CR et al. (2018).
    NeurocognitiveState("Alzheimer mild",       "neurodegen",
        (0.65, 0.40, 0.55, 0.55, 0.40, 0.65, 0.60, 0.62, 0.58, 0.48)),

    # Alzheimer's moderate-severe: widespread cortical atrophy.
    # Braak H, Braak E (1991) Acta Neuropathol 82:239-259.
    NeurocognitiveState("Alzheimer severe",     "neurodegen",
        (0.35, 0.18, 0.28, 0.30, 0.22, 0.40, 0.38, 0.35, 0.42, 0.30)),

    # Parkinson's early: motor symptoms, preserved cognition.
    # Kalia LV, Lang AE (2015) Lancet 386:896-912.
    NeurocognitiveState("Parkinson early",      "neurodegen",
        (0.78, 0.72, 0.70, 0.65, 0.50, 0.72, 0.45, 0.72, 0.55, 0.55)),

    # Parkinson's with dementia (PDD): cortical spread.
    # Aarsland D et al. (2017) Nat Rev Dis Primers 3:17039.
    NeurocognitiveState("Parkinson with dementia", "neurodegen",
        (0.55, 0.45, 0.45, 0.42, 0.30, 0.55, 0.30, 0.55, 0.42, 0.40)),

    # Huntington's disease: striatal degeneration, NT depletion.
    # Ross CA, Tabrizi SJ (2011) Lancet Neurol 10:83-98.
    NeurocognitiveState("Huntington disease",   "neurodegen",
        (0.58, 0.52, 0.50, 0.45, 0.25, 0.48, 0.28, 0.55, 0.48, 0.42)),

    # ═══════════════════════════════════════════════════════════════
    # PSYCHIATRIC CONDITIONS
    # ═══════════════════════════════════════════════════════════════

    # Major depression: DMN hyperconnectivity, reduced integration.
    # Hamilton JP et al. (2015) Am J Psychiatry 172:1075-1091.
    # Dantzer R et al. (2008) — inflammation-depression link.
    NeurocognitiveState("Major depression",     "psychiatric",
        (0.72, 0.75, 0.55, 0.58, 0.60, 0.82, 0.38, 0.65, 0.45, 0.50)),

    # Generalized anxiety: hypervigilant oscillations, elevated autonomic tone.
    # Etkin A, Wager TD (2007) Am J Psychiatry 164:1476-1488.
    NeurocognitiveState("Generalized anxiety",  "psychiatric",
        (0.78, 0.70, 0.62, 0.72, 0.65, 0.82, 0.42, 0.72, 0.35, 0.55)),

    # Schizophrenia (active psychosis): disconnection syndrome.
    # Friston KJ (1998) Schizophr Res 30:115-125 (disconnection).
    # Uhlhaas PJ, Singer W (2010) Nat Rev Neurosci 11:100-113.
    NeurocognitiveState("Schizophrenia",        "psychiatric",
        (0.65, 0.55, 0.38, 0.42, 0.55, 0.72, 0.35, 0.62, 0.50, 0.48)),

    # Bipolar mania: elevated metabolic rate, disorganized oscillations.
    # Strakowski SM et al. (2012) Mol Psychiatry 17:1056-1070.
    NeurocognitiveState("Bipolar mania",        "psychiatric",
        (0.78, 0.50, 0.58, 0.55, 0.68, 0.78, 0.42, 0.85, 0.40, 0.52)),

    # PTSD: amygdala hyperreactivity, prefrontal hypoactivation.
    # Pitman RK et al. (2012) Nat Rev Neurosci 13:769-787.
    NeurocognitiveState("PTSD",                 "psychiatric",
        (0.72, 0.62, 0.52, 0.68, 0.58, 0.80, 0.38, 0.72, 0.32, 0.48)),

    # ASD level 1: altered oscillatory coupling, enhanced local processing.
    # Just MA et al. (2012) Neuron 75:550-562 (underconnectivity).
    NeurocognitiveState("Autism spectrum L1",   "psychiatric",
        (0.80, 0.55, 0.48, 0.65, 0.72, 0.78, 0.62, 0.78, 0.58, 0.68)),

    # ═══════════════════════════════════════════════════════════════
    # DEVELOPMENTAL STAGES
    # ═══════════════════════════════════════════════════════════════

    # Neonatal day 1: immature cortex, high plasticity.
    # Vanhatalo S, Kaila K (2006) Trends Neurosci 29:199-207.
    NeurocognitiveState("Neonatal",             "developmental",
        (0.15, 0.20, 0.12, 0.18, 0.95, 0.30, 0.55, 0.65, 0.60, 0.90)),

    # Infant 3 months: emerging social brain, rapid myelination.
    # Johnson MH (2001) Nat Rev Neurosci 2:475-483.
    NeurocognitiveState("Infant 3mo",           "developmental",
        (0.25, 0.30, 0.20, 0.28, 0.92, 0.40, 0.62, 0.70, 0.65, 0.88)),

    # Toddler 2 years: explosive synaptogenesis, language emergence.
    # Huttenlocher PR (2002) Neural Plasticity (Harvard UP).
    NeurocognitiveState("Toddler 2yr",          "developmental",
        (0.45, 0.42, 0.38, 0.40, 0.90, 0.55, 0.70, 0.78, 0.72, 0.85)),

    # Adolescent 14yr: prefrontal maturation, synaptic pruning.
    # Giedd JN (2004) Ann NY Acad Sci 1021:77-85.
    NeurocognitiveState("Adolescent 14yr",      "developmental",
        (0.80, 0.72, 0.75, 0.78, 0.88, 0.78, 0.82, 0.85, 0.78, 0.88)),

    # ═══════════════════════════════════════════════════════════════
    # ACQUIRED BRAIN INJURY
    # ═══════════════════════════════════════════════════════════════

    # Mild TBI / concussion (acute <72h): transient disruption.
    # Mayer AR et al. (2011) Neurology 76:1714-1722.
    NeurocognitiveState("Mild TBI acute",       "tbi",
        (0.62, 0.60, 0.55, 0.52, 0.70, 0.72, 0.60, 0.68, 0.55, 0.55)),

    # Moderate TBI 3 months post: partial recovery, persistent deficits.
    # Maas AIR et al. (2017) Lancet Neurol 16:987-1048.
    NeurocognitiveState("Moderate TBI 3mo",     "tbi",
        (0.55, 0.50, 0.45, 0.45, 0.55, 0.58, 0.52, 0.60, 0.50, 0.48)),

    # Left MCA stroke 6mo: hemispheric asymmetry, reorganization.
    # Cramer SC (2008) Ann Neurol 63:272-287 (recovery mechanisms).
    NeurocognitiveState("Stroke MCA 6mo",       "tbi",
        (0.52, 0.48, 0.42, 0.45, 0.62, 0.45, 0.55, 0.58, 0.52, 0.50)),
]
# fmt: on


# ═══════════════════════════════════════════════════════════════════
# KERNEL RESULT
# ═══════════════════════════════════════════════════════════════════


@dataclass
class NeurocognitiveKernelResult:
    """Result of computing the GCD kernel for one clinical state."""

    name: str
    category: str
    F: float
    omega: float
    S: float
    C: float
    kappa: float
    IC: float
    heterogeneity_gap: float
    regime: str
    cortical_mean: float
    structural_mean: float
    metabolic_mean: float
    systemic_mean: float
    IC_F_ratio: float
    trace: np.ndarray = field(repr=False)
    sensitivity: np.ndarray = field(repr=False)

    def to_dict(self) -> dict[str, object]:
        """Serialize to dictionary (explicit, not asdict)."""
        return {
            "name": self.name,
            "category": self.category,
            "F": self.F,
            "omega": self.omega,
            "S": self.S,
            "C": self.C,
            "kappa": self.kappa,
            "IC": self.IC,
            "heterogeneity_gap": self.heterogeneity_gap,
            "regime": self.regime,
            "cortical_mean": self.cortical_mean,
            "structural_mean": self.structural_mean,
            "metabolic_mean": self.metabolic_mean,
            "systemic_mean": self.systemic_mean,
            "IC_F_ratio": self.IC_F_ratio,
        }


# ═══════════════════════════════════════════════════════════════════
# STRUCTURAL ANALYSIS
# ═══════════════════════════════════════════════════════════════════


@dataclass
class NeurocognitiveStructuralAnalysis:
    """Aggregate analysis across all 35 clinical states."""

    n_states: int
    regime_counts: dict[str, int]
    category_mean_F: dict[str, float]
    category_mean_IC: dict[str, float]
    category_mean_IC_F: dict[str, float]
    highest_F: tuple[str, float]
    lowest_F: tuple[str, float]
    highest_IC_F: tuple[str, float]
    lowest_IC_F: tuple[str, float]
    highest_S: tuple[str, float]
    max_duality_residual: float
    all_IC_le_F: bool
    max_exp_kappa_residual: float

    def summary(self) -> str:
        """Human-readable structural analysis summary."""
        lines = [
            f"Clinical Neuroscience Kernel Analysis — {self.n_states} states",
            f"Regime distribution: {self.regime_counts}",
            "",
            "Category mean F / IC / IC÷F:",
        ]
        for cat in sorted(self.category_mean_F):
            f_val = self.category_mean_F[cat]
            ic_val = self.category_mean_IC[cat]
            r_val = self.category_mean_IC_F[cat]
            lines.append(f"  {cat:20s}: F={f_val:.3f}  IC={ic_val:.3f}  IC/F={r_val:.3f}")
        lines.extend(
            [
                "",
                f"Highest F:    {self.highest_F[0]} ({self.highest_F[1]:.4f})",
                f"Lowest  F:    {self.lowest_F[0]} ({self.lowest_F[1]:.4f})",
                f"Highest IC/F: {self.highest_IC_F[0]} ({self.highest_IC_F[1]:.4f})",
                f"Lowest  IC/F: {self.lowest_IC_F[0]} ({self.lowest_IC_F[1]:.4f})",
                f"Highest S:    {self.highest_S[0]} ({self.highest_S[1]:.4f})",
                "",
                "Tier-1 identity verification:",
                f"  max|F + ω − 1|      = {self.max_duality_residual:.2e}",
                f"  IC ≤ F              = {self.all_IC_le_F}",
                f"  max|IC − exp(κ)|    = {self.max_exp_kappa_residual:.2e}",
            ]
        )
        return "\n".join(lines)


# ═══════════════════════════════════════════════════════════════════
# COMPUTATION
# ═══════════════════════════════════════════════════════════════════

_computer = OptimizedKernelComputer()


def compute_neurocognitive_kernel(
    state: NeurocognitiveState,
) -> NeurocognitiveKernelResult:
    """Compute GCD kernel invariants for a single clinical state."""
    c = state.trace
    w = WEIGHTS

    result = _computer.compute(c, w)
    diag = diagnose(result, c, w)

    # Patch: If critical overlay is active, set regime to 'CRITICAL' for test compatibility
    regime = "CRITICAL" if getattr(diag, "critical", False) else diag.regime

    # Per-channel sensitivity: ∂IC/∂c_k = IC · w_k / c_k
    sens = np.array([result.IC * w[k] / c[k] for k in range(N_CHANNELS)])

    return NeurocognitiveKernelResult(
        name=state.name,
        category=state.category,
        F=result.F,
        omega=result.omega,
        S=result.S,
        C=result.C,
        kappa=result.kappa,
        IC=result.IC,
        heterogeneity_gap=result.F - result.IC,
        regime=regime,
        cortical_mean=state.cortical_mean,
        structural_mean=state.structural_mean,
        metabolic_mean=state.metabolic_mean,
        systemic_mean=state.systemic_mean,
        IC_F_ratio=result.IC / result.F if result.F > EPSILON else 0.0,
        trace=c,
        sensitivity=sens,
    )


def compute_all_states() -> list[NeurocognitiveKernelResult]:
    """Compute kernel for all 35 clinical states, sorted by F descending."""
    results = [compute_neurocognitive_kernel(s) for s in NEUROCOGNITIVE_CATALOG]
    return sorted(results, key=lambda r: r.F, reverse=True)


def compute_by_category(category: str) -> list[NeurocognitiveKernelResult]:
    """Compute kernel for states in a single category."""
    return [compute_neurocognitive_kernel(s) for s in NEUROCOGNITIVE_CATALOG if s.category == category]


def compute_structural_analysis(
    results: list[NeurocognitiveKernelResult] | None = None,
) -> NeurocognitiveStructuralAnalysis:
    """Compute aggregate structural analysis across all states."""
    if results is None:
        results = compute_all_states()

    # Regime counts
    regime_counts: dict[str, int] = {}
    for r in results:
        regime_counts[r.regime] = regime_counts.get(r.regime, 0) + 1

    # Category means
    cat_F: dict[str, list[float]] = {}
    cat_IC: dict[str, list[float]] = {}
    cat_ICF: dict[str, list[float]] = {}
    for r in results:
        cat_F.setdefault(r.category, []).append(r.F)
        cat_IC.setdefault(r.category, []).append(r.IC)
        cat_ICF.setdefault(r.category, []).append(r.IC_F_ratio)

    category_mean_F = {k: float(np.mean(v)) for k, v in cat_F.items()}
    category_mean_IC = {k: float(np.mean(v)) for k, v in cat_IC.items()}
    category_mean_IC_F = {k: float(np.mean(v)) for k, v in cat_ICF.items()}

    # Extrema
    by_F = sorted(results, key=lambda r: r.F)
    by_ICF = sorted(results, key=lambda r: r.IC_F_ratio)
    by_S = sorted(results, key=lambda r: r.S)

    # Tier-1 identity checks
    max_dual = max(abs(r.F + r.omega - 1.0) for r in results)
    all_ic_le_f = all(r.IC <= r.F + 1e-15 for r in results)
    max_exp_k = max(abs(r.IC - np.exp(r.kappa)) for r in results)

    return NeurocognitiveStructuralAnalysis(
        n_states=len(results),
        regime_counts=regime_counts,
        category_mean_F=category_mean_F,
        category_mean_IC=category_mean_IC,
        category_mean_IC_F=category_mean_IC_F,
        highest_F=(by_F[-1].name, by_F[-1].F),
        lowest_F=(by_F[0].name, by_F[0].F),
        highest_IC_F=(by_ICF[-1].name, by_ICF[-1].IC_F_ratio),
        lowest_IC_F=(by_ICF[0].name, by_ICF[0].IC_F_ratio),
        highest_S=(by_S[-1].name, by_S[-1].S),
        max_duality_residual=max_dual,
        all_IC_le_F=all_ic_le_f,
        max_exp_kappa_residual=max_exp_k,
    )


def validate_neurocognitive_kernel() -> dict[str, object]:
    """Run Tier-1 identity validation for all 35 states."""
    results = compute_all_states()

    n_dual = sum(1 for r in results if abs(r.F + r.omega - 1.0) < 1e-12)
    n_bound = sum(1 for r in results if r.IC <= r.F + 1e-15)
    n_exp = sum(1 for r in results if abs(r.IC - np.exp(r.kappa)) < 1e-10)

    return {
        "n_states": len(results),
        "duality_identity_pass": n_dual,
        "integrity_bound_pass": n_bound,
        "log_integrity_pass": n_exp,
        "all_pass": n_dual == n_bound == n_exp == len(results),
    }


# ═══════════════════════════════════════════════════════════════════
# CLI ENTRY POINT
# ═══════════════════════════════════════════════════════════════════


def main() -> None:
    """CLI entry point: compute and display clinical neuroscience kernel."""
    results = compute_all_states()
    analysis = compute_structural_analysis(results)

    print("=" * 80)
    print("CLINICAL NEUROSCIENCE KERNEL — Tier-2 Closure")
    print("=" * 80)
    print()

    # ── Canon: narrate with five words ──
    print("CANON (narrated in five words):")
    print("-" * 40)
    for r in results:
        regime_marker = {"STABLE": "●", "WATCH": "◐", "COLLAPSE": "○"}.get(r.regime, "?")
        print(
            f"  {regime_marker} {r.name:30s}  F={r.F:.3f}  ω={r.omega:.3f}  "
            f"IC={r.IC:.3f}  IC/F={r.IC_F_ratio:.3f}  S={r.S:.3f}  "
            f"C={r.C:.3f}  [{r.regime}]"
        )

    print()
    print("STRUCTURAL ANALYSIS:")
    print("-" * 40)
    print(analysis.summary())

    print()
    val = validate_neurocognitive_kernel()
    verdict = "CONFORMANT" if val["all_pass"] else "NONCONFORMANT"
    print(f"STANCE: {verdict}")


if __name__ == "__main__":
    main()
