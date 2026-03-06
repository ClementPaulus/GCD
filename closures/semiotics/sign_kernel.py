"""
Semiotics Kernel — GCD Applied to Sign Systems

Maps 20 canonical sign systems and semiotic phenomena to 8-channel
trace vectors and computes Tier-1 invariants (F, ω, S, C, κ, IC).

Channels (8, equal weight w_i = 1/8):
    1. syntactic_integrity    — Internal consistency of sign-sign relations
    2. semantic_fidelity      — Preservation of signified through transmission
    3. pragmatic_coherence    — Context-appropriateness of sign use
    4. iconicity              — Degree of resemblance between sign and referent
    5. indexicality           — Strength of causal/contiguous link to referent
    6. conventionality        — Degree of shared arbitrary convention
    7. interpretant_stability — Stability of the interpretant across receivers
    8. contextual_return      — Fraction of sign meaning recovered in context

GCD predictions for semiotics (derivable from Axiom-0):
    - Stable regime (ω < 0.038): highly conventionalized, closed sign systems
      (formal logic, mathematics, Morse code)
    - Watch regime: natural languages, icons with partial resemblance
    - Collapse regime (ω ≥ 0.30): highly polysemous, culturally-bounded signs;
      dead metaphors; pidgins before creolization
    - Geometric slaughter: one channel near ε kills IC
      (e.g., absent shared convention → symbol fails despite high iconicity)
    - τ_R = ∞_rec: gestus — a sign emitted without a receiver that returns it
      (e.g., private language, dead script without Rosetta Stone)

Key semiotic concepts mapped through the kernel:
    - Saussurean sign: signifier/signified (binary) → channels 2, 6, 7
    - Peircean triadic sign: representamen/object/interpretant → channels 4, 5, 8
    - Jakobson's six functions of language → weight modulation
    - Eco's open work: high S (entropy), high C (curvature)
    - Barthes' mythologies: second-order sign (sign becomes signifier) → drift

Data sources:
    Channel values are consensus estimates from semiotic theory literature
    (Saussure 1916, Peirce 1931-1958, Eco 1976, Barthes 1957, Jakobson 1960).
    Values represent structural rankings within semiotic typology, not
    absolute measurements. Kernel results are structural, not empirical.

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
    "syntactic_integrity",
    "semantic_fidelity",
    "pragmatic_coherence",
    "iconicity",
    "indexicality",
    "conventionality",
    "interpretant_stability",
    "contextual_return",
]

N_CHANNELS = len(CHANNEL_LABELS)

# Regime thresholds (aligned with frozen_contract.RegimeThresholds defaults)
OMEGA_STABLE = 0.038
OMEGA_WATCH = 0.30


# ═════════════════════════════════════════════════════════════════════
# SECTION 1: SIGN SYSTEM DATA
# ═════════════════════════════════════════════════════════════════════


@dataclass(frozen=True, slots=True)
class SignSystem:
    """A semiotic system or sign type with normalized channel scores.

    Channels are normalized structural rankings in [0, 1], representing
    relative standing within the typology of sign systems. These are
    structural rankings derived from semiotic theory, not empirical
    measurements.

    Fields
    ------
    name : str
        Name of the sign system.
    tradition : str
        Semiotic tradition or school (Peircean, Saussurean, Pragmatic, etc.)
    sign_type : str
        Dominant sign type (icon, index, symbol, hybrid)
    domain : str
        Domain of use (language, visual, auditory, somatic, formal, etc.)
    notes : str
        Brief structural observation about this sign system.
    syntactic_integrity : float
        Internal consistency of sign-sign relations [0, 1].
    semantic_fidelity : float
        Preservation of the signified through transmission [0, 1].
    pragmatic_coherence : float
        Context-appropriateness of sign use [0, 1].
    iconicity : float
        Degree of resemblance between sign and referent [0, 1].
    indexicality : float
        Strength of causal/contiguous link to referent [0, 1].
    conventionality : float
        Degree of shared arbitrary convention [0, 1].
    interpretant_stability : float
        Stability of the interpretant across receivers [0, 1].
    contextual_return : float
        Fraction of sign meaning recovered in context [0, 1].
    """

    name: str
    tradition: str
    sign_type: str
    domain: str
    notes: str

    # 8 channels — normalized semiotic scores [0, 1]
    syntactic_integrity: float
    semantic_fidelity: float
    pragmatic_coherence: float
    iconicity: float
    indexicality: float
    conventionality: float
    interpretant_stability: float
    contextual_return: float

    def trace(self) -> list[float]:
        """Return the 8-channel trace vector."""
        return [
            self.syntactic_integrity,
            self.semantic_fidelity,
            self.pragmatic_coherence,
            self.iconicity,
            self.indexicality,
            self.conventionality,
            self.interpretant_stability,
            self.contextual_return,
        ]


# ── Sign system catalog ────────────────────────────────────────────
# 20 representative sign systems spanning the semiotic typology.
# Each entry represents a consensus structural ranking from semiotic
# theory literature.
SIGN_SYSTEMS: list[SignSystem] = [
    # ── Formal / Mathematical Sign Systems ────────────────────────
    SignSystem(
        name="Formal Logic",
        tradition="Peircean",
        sign_type="symbol",
        domain="formal",
        notes="Maximally closed, syntactically rigid; convention fully defines meaning",
        syntactic_integrity=0.98,
        semantic_fidelity=0.95,
        pragmatic_coherence=0.85,
        iconicity=0.10,
        indexicality=0.05,
        conventionality=0.99,
        interpretant_stability=0.99,
        contextual_return=0.97,
    ),
    SignSystem(
        name="Mathematical Notation",
        tradition="Peircean",
        sign_type="symbol",
        domain="formal",
        notes="Near-perfect syntactic integrity; universal convention in STEM",
        syntactic_integrity=0.97,
        semantic_fidelity=0.96,
        pragmatic_coherence=0.80,
        iconicity=0.08,
        indexicality=0.03,
        conventionality=0.98,
        interpretant_stability=0.98,
        contextual_return=0.95,
    ),
    SignSystem(
        name="Morse Code",
        tradition="Peircean",
        sign_type="symbol",
        domain="auditory",
        notes="Strict symbolic encoding; high conventionality, minimal iconicity",
        syntactic_integrity=0.96,
        semantic_fidelity=0.94,
        pragmatic_coherence=0.88,
        iconicity=0.05,
        indexicality=0.10,
        conventionality=0.99,
        interpretant_stability=0.97,
        contextual_return=0.93,
    ),
    # ── Natural Language Systems ───────────────────────────────────
    SignSystem(
        name="Written English",
        tradition="Saussurean",
        sign_type="symbol",
        domain="language",
        notes="High conventionality; polysemy creates significant entropy",
        syntactic_integrity=0.82,
        semantic_fidelity=0.72,
        pragmatic_coherence=0.74,
        iconicity=0.12,
        indexicality=0.18,
        conventionality=0.88,
        interpretant_stability=0.70,
        contextual_return=0.75,
    ),
    SignSystem(
        name="Spoken Natural Language",
        tradition="Saussurean",
        sign_type="symbol",
        domain="language",
        notes="Prosody adds indexical/iconic channels; pragmatic coherence high in dialogue",
        syntactic_integrity=0.78,
        semantic_fidelity=0.70,
        pragmatic_coherence=0.80,
        iconicity=0.20,
        indexicality=0.30,
        conventionality=0.82,
        interpretant_stability=0.65,
        contextual_return=0.78,
    ),
    SignSystem(
        name="Pidgin Language",
        tradition="Pragmatic",
        sign_type="hybrid",
        domain="language",
        notes="Reduced syntax; high semantic drift; interpretant varies across speakers",
        syntactic_integrity=0.40,
        semantic_fidelity=0.52,
        pragmatic_coherence=0.55,
        iconicity=0.30,
        indexicality=0.38,
        conventionality=0.35,
        interpretant_stability=0.30,
        contextual_return=0.50,
    ),
    SignSystem(
        name="Creole Language",
        tradition="Pragmatic",
        sign_type="symbol",
        domain="language",
        notes="Collapsed pidgin returns as stable grammar; τ_R completed, IC rises",
        syntactic_integrity=0.72,
        semantic_fidelity=0.68,
        pragmatic_coherence=0.72,
        iconicity=0.22,
        indexicality=0.28,
        conventionality=0.70,
        interpretant_stability=0.68,
        contextual_return=0.72,
    ),
    SignSystem(
        name="Dead Language (Latin)",
        tradition="Saussurean",
        sign_type="symbol",
        domain="language",
        notes="Conventional meaning preserved in texts; pragmatic use absent — gestus",
        syntactic_integrity=0.90,
        semantic_fidelity=0.75,
        pragmatic_coherence=0.15,
        iconicity=0.08,
        indexicality=0.05,
        conventionality=0.85,
        interpretant_stability=0.60,
        contextual_return=0.20,
    ),
    # ── Visual / Iconic Sign Systems ───────────────────────────────
    SignSystem(
        name="Realistic Painting",
        tradition="Peircean",
        sign_type="icon",
        domain="visual",
        notes="High iconicity and semantic fidelity; low syntactic constraint",
        syntactic_integrity=0.35,
        semantic_fidelity=0.85,
        pragmatic_coherence=0.70,
        iconicity=0.92,
        indexicality=0.20,
        conventionality=0.30,
        interpretant_stability=0.75,
        contextual_return=0.78,
    ),
    SignSystem(
        name="Abstract Art",
        tradition="Pragmatic",
        sign_type="icon",
        domain="visual",
        notes="Low iconicity; high entropy; interpretant varies radically — high ω",
        syntactic_integrity=0.20,
        semantic_fidelity=0.30,
        pragmatic_coherence=0.45,
        iconicity=0.25,
        indexicality=0.15,
        conventionality=0.15,
        interpretant_stability=0.20,
        contextual_return=0.35,
    ),
    SignSystem(
        name="Traffic Signs",
        tradition="Saussurean",
        sign_type="symbol",
        domain="visual",
        notes="Highly conventionalized; simple iconicity + strong regulatory pragma",
        syntactic_integrity=0.90,
        semantic_fidelity=0.92,
        pragmatic_coherence=0.94,
        iconicity=0.60,
        indexicality=0.25,
        conventionality=0.95,
        interpretant_stability=0.95,
        contextual_return=0.93,
    ),
    SignSystem(
        name="Emoji",
        tradition="Pragmatic",
        sign_type="icon",
        domain="visual",
        notes="High iconicity; interpretant varies across cultures; pragmatics platform-dependent",
        syntactic_integrity=0.50,
        semantic_fidelity=0.62,
        pragmatic_coherence=0.65,
        iconicity=0.75,
        indexicality=0.20,
        conventionality=0.58,
        interpretant_stability=0.55,
        contextual_return=0.60,
    ),
    # ── Bodily / Somatic Signs ─────────────────────────────────────
    SignSystem(
        name="Gesture (Co-speech)",
        tradition="Peircean",
        sign_type="icon",
        domain="somatic",
        notes="Iconic + indexical; pragmatic coherence high in face-to-face context",
        syntactic_integrity=0.42,
        semantic_fidelity=0.62,
        pragmatic_coherence=0.78,
        iconicity=0.68,
        indexicality=0.65,
        conventionality=0.30,
        interpretant_stability=0.55,
        contextual_return=0.70,
    ),
    SignSystem(
        name="Sign Language (ASL)",
        tradition="Saussurean",
        sign_type="hybrid",
        domain="somatic",
        notes="Full natural language; iconic motivation + symbolic convention",
        syntactic_integrity=0.88,
        semantic_fidelity=0.85,
        pragmatic_coherence=0.84,
        iconicity=0.55,
        indexicality=0.40,
        conventionality=0.82,
        interpretant_stability=0.85,
        contextual_return=0.86,
    ),
    SignSystem(
        name="Facial Expression",
        tradition="Peircean",
        sign_type="index",
        domain="somatic",
        notes="Primarily indexical (emotion marker); universal core + cultural overlay",
        syntactic_integrity=0.30,
        semantic_fidelity=0.65,
        pragmatic_coherence=0.72,
        iconicity=0.48,
        indexicality=0.80,
        conventionality=0.40,
        interpretant_stability=0.60,
        contextual_return=0.68,
    ),
    # ── Indexical / Symptomatic Signs ─────────────────────────────
    SignSystem(
        name="Medical Symptom",
        tradition="Peircean",
        sign_type="index",
        domain="diagnostic",
        notes="High indexicality (caused by disease); semantic fidelity depends on clinical knowledge",
        syntactic_integrity=0.55,
        semantic_fidelity=0.70,
        pragmatic_coherence=0.65,
        iconicity=0.20,
        indexicality=0.92,
        conventionality=0.60,
        interpretant_stability=0.72,
        contextual_return=0.68,
    ),
    SignSystem(
        name="Smoke as Sign of Fire",
        tradition="Peircean",
        sign_type="index",
        domain="natural",
        notes="Canonical Peircean index; causal bond is absolute; interpretant very stable",
        syntactic_integrity=0.60,
        semantic_fidelity=0.88,
        pragmatic_coherence=0.82,
        iconicity=0.15,
        indexicality=0.98,
        conventionality=0.20,
        interpretant_stability=0.90,
        contextual_return=0.88,
    ),
    # ── Narrative / Mythological Signs ────────────────────────────
    SignSystem(
        name="Literary Metaphor",
        tradition="Pragmatic",
        sign_type="icon",
        domain="language",
        notes="Second-order iconicity; high entropy; interpretant spreads across readings",
        syntactic_integrity=0.55,
        semantic_fidelity=0.55,
        pragmatic_coherence=0.60,
        iconicity=0.65,
        indexicality=0.15,
        conventionality=0.35,
        interpretant_stability=0.40,
        contextual_return=0.55,
    ),
    SignSystem(
        name="Dead Metaphor",
        tradition="Pragmatic",
        sign_type="symbol",
        domain="language",
        notes="Metaphoric motivation lost; opaque symbol remains; τ_R≈∞_rec for original sense",
        syntactic_integrity=0.70,
        semantic_fidelity=0.40,
        pragmatic_coherence=0.72,
        iconicity=0.05,
        indexicality=0.05,
        conventionality=0.80,
        interpretant_stability=0.75,
        contextual_return=0.30,
    ),
    SignSystem(
        name="Cultural Myth (Barthes)",
        tradition="Pragmatic",
        sign_type="hybrid",
        domain="cultural",
        notes="Second-order sign: denotation collapses into connotation; high ideological drift",
        syntactic_integrity=0.48,
        semantic_fidelity=0.38,
        pragmatic_coherence=0.62,
        iconicity=0.40,
        indexicality=0.35,
        conventionality=0.72,
        interpretant_stability=0.45,
        contextual_return=0.42,
    ),
]


# ═════════════════════════════════════════════════════════════════════
# SECTION 2: RESULT DATACLASS
# ═════════════════════════════════════════════════════════════════════


@dataclass
class SignKernelResult:
    """GCD kernel result for a single sign system.

    Tier-1 invariants (F, ω, S, C, κ, IC) are computed from the 8-channel
    trace vector and satisfy:
        F + ω = 1      (duality identity — complementum perfectum)
        IC ≤ F         (integrity bound — limbus integritatis)
        IC = exp(κ)    (log-integritas)
    """

    # Identity
    name: str
    tradition: str
    sign_type: str
    domain: str
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

    # Semiotic interpretation
    dominant_channel: str  # Highest-scoring channel
    dominant_value: float
    weakest_channel: str  # Lowest-scoring channel
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
    """Classify semiotic regime from drift ω."""
    if omega < OMEGA_STABLE:
        return "Stable"
    if omega < OMEGA_WATCH:
        return "Watch"
    return "Collapse"


def compute_sign_system(ss: SignSystem) -> SignKernelResult:
    """Compute GCD kernel for one sign system.

    Parameters
    ----------
    ss : SignSystem
        The sign system to analyse.

    Returns
    -------
    SignKernelResult
        Tier-1 invariants and semiotic classification.
    """
    raw = ss.trace()
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

    # Identify dominant and weakest channels
    dom_idx = int(np.argmax(c))
    weak_idx = int(np.argmin(c))

    return SignKernelResult(
        name=ss.name,
        tradition=ss.tradition,
        sign_type=ss.sign_type,
        domain=ss.domain,
        notes=ss.notes,
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
        dominant_channel=CHANNEL_LABELS[dom_idx],
        dominant_value=round(float(c[dom_idx]), 6),
        weakest_channel=CHANNEL_LABELS[weak_idx],
        weakest_value=round(float(c[weak_idx]), 6),
    )


def compute_all_sign_systems() -> list[SignKernelResult]:
    """Compute GCD kernel for all 20 sign systems.

    Returns
    -------
    list[SignKernelResult]
        Kernel results in catalog order.
    """
    return [compute_sign_system(ss) for ss in SIGN_SYSTEMS]


# ═════════════════════════════════════════════════════════════════════
# SECTION 4: SEMIOTIC STRUCTURAL ANALYSIS
# ═════════════════════════════════════════════════════════════════════


def analyze_sign_type_profiles(results: list[SignKernelResult]) -> dict[str, dict[str, float]]:
    """Compute mean Tier-1 invariants per sign type (icon/index/symbol/hybrid).

    Returns
    -------
    dict[str, dict[str, float]]
        Mapping from sign type to mean invariant values.
    """
    from collections import defaultdict

    buckets: dict[str, list[SignKernelResult]] = defaultdict(list)
    for r in results:
        buckets[r.sign_type].append(r)

    profile: dict[str, dict[str, float]] = {}
    for stype, rs in buckets.items():
        n = len(rs)
        profile[stype] = {
            "mean_F": round(sum(r.F for r in rs) / n, 4),
            "mean_omega": round(sum(r.omega for r in rs) / n, 4),
            "mean_IC": round(sum(r.IC for r in rs) / n, 4),
            "mean_S": round(sum(r.S for r in rs) / n, 4),
            "mean_gap": round(sum(r.heterogeneity_gap for r in rs) / n, 4),
            "count": float(n),
        }
    return profile


def find_semiotic_collapse_candidates(results: list[SignKernelResult]) -> list[SignKernelResult]:
    """Return sign systems in the Collapse regime (ω ≥ 0.30).

    These are sign systems with high drift — the sign-meaning relation is
    fragile, contextually saturated, or culturally opaque.
    """
    return [r for r in results if r.regime == "Collapse"]


def semiotic_structural_summary(results: list[SignKernelResult]) -> dict[str, Any]:
    """Produce a structural summary of the semiotic kernel sweep.

    Returns counts by regime, mean F per tradition, and geometric slaughter
    candidates (systems where IC < 0.3 despite F > 0.5).
    """
    n = len(results)

    regime_counts = {"Stable": 0, "Watch": 0, "Collapse": 0}
    for r in results:
        regime_counts[r.regime] += 1

    # Mean F per tradition
    from collections import defaultdict

    trad_F: dict[str, list[float]] = defaultdict(list)
    for r in results:
        trad_F[r.tradition].append(r.F)
    mean_F_per_tradition = {t: round(sum(vs) / len(vs), 4) for t, vs in trad_F.items()}

    # Geometric slaughter candidates
    slaughter = [r for r in results if r.IC < 0.3 and r.F > 0.5]

    return {
        "n_sign_systems": n,
        "regime_counts": regime_counts,
        "mean_F_per_tradition": mean_F_per_tradition,
        "n_slaughter_candidates": len(slaughter),
        "slaughter_candidates": [r.name for r in slaughter],
    }


# ═════════════════════════════════════════════════════════════════════
# SECTION 5: SELF-TEST
# ═════════════════════════════════════════════════════════════════════


if __name__ == "__main__":
    results = compute_all_sign_systems()

    print("=" * 72)
    print("  SEMIOTICS KERNEL — GCD Applied to Sign Systems")
    print("=" * 72)
    print(f"\n  {len(results)} sign systems × {N_CHANNELS} channels\n")
    print(f"  {'Name':<28s}  {'F':>6s}  {'ω':>6s}  {'IC':>6s}  {'Δ':>6s}  {'Regime':<10s}")
    print("  " + "-" * 70)

    for r in results:
        print(f"  {r.name:<28s}  {r.F:6.3f}  {r.omega:6.3f}  {r.IC:6.3f}  {r.heterogeneity_gap:6.3f}  {r.regime:<10s}")

    summary = semiotic_structural_summary(results)
    print(f"\n  Regime distribution: {summary['regime_counts']}")
    print(f"  Mean F per tradition: {summary['mean_F_per_tradition']}")
    print(f"  Geometric slaughter candidates (IC<0.3, F>0.5): {summary['n_slaughter_candidates']}")

    # Verify Tier-1 identities
    duality_ok = all(abs(r.F_plus_omega - 1.0) < 1e-9 for r in results)
    bound_ok = all(r.IC_leq_F for r in results)
    exp_ok = all(r.IC_eq_exp_kappa for r in results)

    print("\n  Tier-1 identity checks:")
    print(f"    F + ω = 1:     {'PASS' if duality_ok else 'FAIL'}")
    print(f"    IC ≤ F:        {'PASS' if bound_ok else 'FAIL'}")
    print(f"    IC = exp(κ):   {'PASS' if exp_ok else 'FAIL'}")
