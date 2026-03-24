"""Translation Levels Closure — ULRC Cross-Level Translation Analysis.

Tier-2 closure mapping 12 translation-level systems through the GCD kernel.
Each system represents a distinct level at which meaning transforms — both
in natural language (linguistic) and in formal systems (mathematical).

The ULRC (Unified Language of Recursive Collapse) establishes that the
kernel IS a grammar (Proposition: Kernel-Grammar Isomorphism). Translation
between levels is governed by the Rosetta invariance property: the budget
Δκ, regime classification, and three-valued verdict are identical across
lenses; only the dialect changes.

This closure quantifies WHAT SURVIVES each level transition — measuring
fidelity loss, structural roughness, and return capacity at each
translation level.

Channels (8, equal weights w_i = 1/8):
  0  semantic_preservation      — meaning retained across level (1 = perfect)
  1  structural_fidelity        — formal structure kept intact (1 = isomorphic)
  2  compositional_transparency — parts compose predictably (1 = fully transparent)
  3  referential_grounding      — connection to referent survives (1 = grounded)
  4  invertibility              — translation is reversible (1 = fully invertible)
  5  cross_level_coherence      — coherent with adjacent levels (1 = seamless)
  6  loss_resistance            — robustness to information loss (1 = lossless)
  7  generative_productivity    — novel forms producible at this level (1 = unlimited)

12 entities across 2 categories (6 linguistic + 6 mathematical):

  Linguistic levels (6):
    phonological    — sound pattern to morpheme boundary
    morphological   — morpheme to word formation
    syntactic       — word order to clause structure
    semantic        — clause meaning to propositional content
    pragmatic       — propositional content to speaker intent
    discourse       — utterance sequence to coherent narrative

  Mathematical levels (6):
    symbolic        — token manipulation (algebra, rewriting)
    algebraic       — structure-preserving maps (homomorphisms)
    topological     — continuity and deformation invariants
    measure_theoretic — integration, probability, σ-algebra
    categorical     — functors between categories (universal properties)
    type_theoretic  — type systems, proof-as-program correspondence

6 theorems (T-TL-1 through T-TL-6):
  T-TL-1: Syntactic level has highest structural fidelity among linguistic
           levels — syntax is the most rule-governed linguistic level.
  T-TL-2: Pragmatic level has lowest invertibility among linguistic levels —
           speaker intent is not recoverable from propositional content.
  T-TL-3: Categorical level has highest cross-level coherence among
           mathematical levels — functors are the universal translation
           mechanism.
  T-TL-4: Mathematical levels have higher mean invertibility than
           linguistic levels — formal systems preserve reversibility.
  T-TL-5: Discourse (linguistic) and categorical (mathematical) share the
           highest generative productivity — both produce unbounded novel
           forms through recursive composition.
  T-TL-6: Mean heterogeneity gap is larger for linguistic levels than
           mathematical levels — language translation loses more to
           channel divergence than formal translation.
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

TL_CHANNELS = [
    "semantic_preservation",
    "structural_fidelity",
    "compositional_transparency",
    "referential_grounding",
    "invertibility",
    "cross_level_coherence",
    "loss_resistance",
    "generative_productivity",
]
N_TL_CHANNELS = len(TL_CHANNELS)


@dataclass(frozen=True, slots=True)
class TranslationLevelEntity:
    """A translation level with 8 measurable channels."""

    name: str
    domain: str  # "linguistic" or "mathematical"
    semantic_preservation: float
    structural_fidelity: float
    compositional_transparency: float
    referential_grounding: float
    invertibility: float
    cross_level_coherence: float
    loss_resistance: float
    generative_productivity: float

    def trace_vector(self) -> np.ndarray:
        return np.array(
            [
                self.semantic_preservation,
                self.structural_fidelity,
                self.compositional_transparency,
                self.referential_grounding,
                self.invertibility,
                self.cross_level_coherence,
                self.loss_resistance,
                self.generative_productivity,
            ]
        )


# ── Entity Catalog ────────────────────────────────────────────────────
#
# Channel values reflect the structural properties of each translation
# level. Linguistic levels are grounded in empirical linguistics;
# mathematical levels in formal properties of each framework.

TL_ENTITIES: tuple[TranslationLevelEntity, ...] = (
    # ── Linguistic levels ── (ordered from surface to discourse)
    #
    # Phonological: sound patterns → morpheme boundaries. High structural
    # fidelity (phonotactic rules are rigid), low semantic preservation
    # (sounds carry minimal meaning), moderate invertibility (spectrograms
    # can recover phonemes but not always), low generative productivity
    # (finite phoneme inventory per language).
    TranslationLevelEntity(
        "phonological",
        "linguistic",
        0.25,
        0.85,
        0.70,
        0.15,
        0.65,
        0.80,
        0.60,
        0.20,
    ),
    # Morphological: morphemes → words. Good compositionality (agglutinative
    # languages show this clearly), moderate semantic preservation (affixes
    # carry meaning), moderate invertibility (parsing recovers morphemes),
    # moderate generative capacity (productive derivation & compounding).
    TranslationLevelEntity(
        "morphological",
        "linguistic",
        0.50,
        0.75,
        0.80,
        0.40,
        0.60,
        0.75,
        0.55,
        0.55,
    ),
    # Syntactic: word order → clause structure. Highest structural fidelity
    # among linguistic levels (formal grammars capture syntax precisely),
    # high compositionality, high invertibility (parse trees are unique for
    # unambiguous grammars), strong coherence with adjacent levels.
    TranslationLevelEntity(
        "syntactic",
        "linguistic",
        0.65,
        0.92,
        0.85,
        0.50,
        0.75,
        0.85,
        0.70,
        0.70,
    ),
    # Semantic: clause meaning → propositional content. High semantic
    # preservation (this IS the meaning level), moderate structural fidelity
    # (formal semantics captures some but not all), lower invertibility
    # (multiple surface forms map to same meaning — many-to-one).
    TranslationLevelEntity(
        "semantic",
        "linguistic",
        0.90,
        0.60,
        0.65,
        0.80,
        0.45,
        0.60,
        0.50,
        0.60,
    ),
    # Pragmatic: propositional content → speaker intent. Lowest invertibility
    # among linguistic levels (intent is not recoverable from proposition
    # alone — "Can you pass the salt?" is a request, not a question about
    # ability). High context sensitivity but low structural fidelity.
    TranslationLevelEntity(
        "pragmatic",
        "linguistic",
        0.70,
        0.30,
        0.35,
        0.75,
        0.20,
        0.40,
        0.25,
        0.50,
    ),
    # Discourse: utterance sequences → coherent narrative. High generative
    # productivity (unbounded composition of clauses into texts), moderate
    # semantic preservation, low structural fidelity (discourse structure
    # is contested — RST, SDRT, centering theory disagree), high referential
    # grounding (discourse tracks entities across text).
    TranslationLevelEntity(
        "discourse",
        "linguistic",
        0.60,
        0.35,
        0.50,
        0.70,
        0.30,
        0.45,
        0.30,
        0.90,
    ),
    # ── Mathematical levels ── (ordered from concrete to abstract)
    #
    # Symbolic: token manipulation, algebraic rewriting. High structural
    # fidelity (rewrite rules are deterministic), high invertibility
    # (term rewriting is often reversible), moderate semantic preservation
    # (symbols are uninterpreted in pure syntax), low cross-level coherence
    # (symbolic ≠ semantic in general).
    TranslationLevelEntity(
        "symbolic",
        "mathematical",
        0.40,
        0.90,
        0.75,
        0.30,
        0.85,
        0.50,
        0.80,
        0.60,
    ),
    # Algebraic: structure-preserving maps (homomorphisms). Very high
    # structural fidelity and invertibility (isomorphisms by definition),
    # strong compositionality (homomorphisms compose), moderate semantic
    # preservation (abstract algebra is structure-about-structure).
    TranslationLevelEntity(
        "algebraic",
        "mathematical",
        0.55,
        0.95,
        0.90,
        0.45,
        0.90,
        0.70,
        0.85,
        0.65,
    ),
    # Topological: continuity, deformation invariants. Moderate semantic
    # preservation (topology preserves qualitative properties), very high
    # loss resistance (invariants survive deformation), high cross-level
    # coherence (topology bridges algebra and analysis).
    TranslationLevelEntity(
        "topological",
        "mathematical",
        0.60,
        0.80,
        0.70,
        0.50,
        0.75,
        0.85,
        0.90,
        0.55,
    ),
    # Measure-theoretic: integration, probability, σ-algebra. High
    # referential grounding (measures tie to physical observables), high
    # loss resistance (integration smooths but preserves totals), moderate
    # invertibility (Radon-Nikodym recovers densities, but integration
    # loses pointwise information). Moderate generative productivity
    # (product measures, pushforward measures, conditional expectations).
    TranslationLevelEntity(
        "measure_theoretic",
        "mathematical",
        0.65,
        0.75,
        0.65,
        0.80,
        0.62,
        0.75,
        0.85,
        0.55,
    ),
    # Categorical: functors between categories. Highest cross-level
    # coherence (category theory IS the language of translation between
    # mathematical structures via natural transformations), very high
    # compositionality, highest generative productivity in math (every
    # category produces new functors).
    TranslationLevelEntity(
        "categorical",
        "mathematical",
        0.70,
        0.85,
        0.95,
        0.35,
        0.80,
        0.95,
        0.75,
        0.90,
    ),
    # Type-theoretic: type systems, Curry-Howard correspondence (proofs
    # as programs). High structural fidelity (types are precise), very
    # high invertibility (extraction from proofs), high compositionality
    # (dependent types compose), strong cross-level coherence (bridges
    # logic, computation, and category theory).
    TranslationLevelEntity(
        "type_theoretic",
        "mathematical",
        0.65,
        0.90,
        0.85,
        0.55,
        0.85,
        0.85,
        0.80,
        0.70,
    ),
)


@dataclass(frozen=True, slots=True)
class TLKernelResult:
    """Kernel output for a translation level entity."""

    name: str
    domain: str
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
            "domain": self.domain,
            "F": self.F,
            "omega": self.omega,
            "S": self.S,
            "C": self.C,
            "kappa": self.kappa,
            "IC": self.IC,
            "regime": self.regime,
        }


def compute_tl_kernel(entity: TranslationLevelEntity) -> TLKernelResult:
    """Compute GCD kernel for a translation level entity."""
    c = entity.trace_vector()
    c = np.clip(c, EPSILON, 1.0 - EPSILON)
    w = np.ones(N_TL_CHANNELS) / N_TL_CHANNELS
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
    return TLKernelResult(
        name=entity.name,
        domain=entity.domain,
        F=F,
        omega=omega,
        S=S,
        C=C_val,
        kappa=kappa,
        IC=IC,
        regime=regime,
    )


def compute_all_entities() -> list[TLKernelResult]:
    """Compute kernel outputs for all translation level entities."""
    return [compute_tl_kernel(e) for e in TL_ENTITIES]


# ── Theorems ──────────────────────────────────────────────────────────


def verify_t_tl_1(results: list[TLKernelResult]) -> dict:
    """T-TL-1: Syntactic level has highest structural fidelity among
    linguistic levels — syntax is the most rule-governed linguistic level.
    Formal grammars (CFG, HPSG, LFG) capture syntactic structure with
    precision unmatched at other linguistic levels.
    """
    ling = [e for e in TL_ENTITIES if e.domain == "linguistic"]
    syn = next(e for e in ling if e.name == "syntactic")
    max_sf = max(e.structural_fidelity for e in ling)
    passed = abs(syn.structural_fidelity - max_sf) < 0.01
    return {
        "name": "T-TL-1",
        "passed": bool(passed),
        "syntactic_sf": syn.structural_fidelity,
        "linguistic_max_sf": float(max_sf),
    }


def verify_t_tl_2(results: list[TLKernelResult]) -> dict:
    """T-TL-2: Pragmatic level has lowest invertibility among linguistic
    levels — speaker intent is not recoverable from propositional content
    alone. 'Can you pass the salt?' maps to a request, but no formal
    operation restores the original speech act from its propositional
    form without context.
    """
    ling = [e for e in TL_ENTITIES if e.domain == "linguistic"]
    prag = next(e for e in ling if e.name == "pragmatic")
    min_inv = min(e.invertibility for e in ling)
    passed = abs(prag.invertibility - min_inv) < 0.01
    return {
        "name": "T-TL-2",
        "passed": bool(passed),
        "pragmatic_inv": prag.invertibility,
        "linguistic_min_inv": float(min_inv),
    }


def verify_t_tl_3(results: list[TLKernelResult]) -> dict:
    """T-TL-3: Categorical level has highest cross-level coherence among
    mathematical levels — functors and natural transformations ARE the
    universal mechanism for translating between mathematical structures.
    Category theory is, by construction, the mathematics of translation.
    """
    math_ents = [e for e in TL_ENTITIES if e.domain == "mathematical"]
    cat = next(e for e in math_ents if e.name == "categorical")
    max_clc = max(e.cross_level_coherence for e in math_ents)
    passed = abs(cat.cross_level_coherence - max_clc) < 0.01
    return {
        "name": "T-TL-3",
        "passed": bool(passed),
        "categorical_clc": cat.cross_level_coherence,
        "mathematical_max_clc": float(max_clc),
    }


def verify_t_tl_4(results: list[TLKernelResult]) -> dict:
    """T-TL-4: Mathematical levels have higher mean invertibility than
    linguistic levels — formal systems preserve reversibility because
    their transformations are structure-preserving by construction,
    while natural language transformations are lossy (many-to-one
    mappings, context dependence, pragmatic ambiguity).
    """
    ling = [e for e in TL_ENTITIES if e.domain == "linguistic"]
    math_ents = [e for e in TL_ENTITIES if e.domain == "mathematical"]
    ling_inv = float(np.mean([e.invertibility for e in ling]))
    math_inv = float(np.mean([e.invertibility for e in math_ents]))
    passed = math_inv > ling_inv
    return {
        "name": "T-TL-4",
        "passed": bool(passed),
        "linguistic_mean_inv": ling_inv,
        "mathematical_mean_inv": math_inv,
        "difference": math_inv - ling_inv,
    }


def verify_t_tl_5(results: list[TLKernelResult]) -> dict:
    """T-TL-5: Discourse (linguistic) and categorical (mathematical) share
    the highest generative productivity in their respective domains —
    both produce unbounded novel forms through recursive composition.
    Discourse composes clauses into unlimited narrative structures;
    category theory composes functors into unlimited diagram structures.
    """
    disc = next(e for e in TL_ENTITIES if e.name == "discourse")
    cat = next(e for e in TL_ENTITIES if e.name == "categorical")
    ling = [e for e in TL_ENTITIES if e.domain == "linguistic"]
    math_ents = [e for e in TL_ENTITIES if e.domain == "mathematical"]
    disc_max_gp = max(e.generative_productivity for e in ling)
    cat_max_gp = max(e.generative_productivity for e in math_ents)
    passed = (
        abs(disc.generative_productivity - disc_max_gp) < 0.01 and abs(cat.generative_productivity - cat_max_gp) < 0.01
    )
    return {
        "name": "T-TL-5",
        "passed": bool(passed),
        "discourse_gp": disc.generative_productivity,
        "categorical_gp": cat.generative_productivity,
        "linguistic_max_gp": float(disc_max_gp),
        "mathematical_max_gp": float(cat_max_gp),
    }


def verify_t_tl_6(results: list[TLKernelResult]) -> dict:
    """T-TL-6: Mean heterogeneity gap (Δ = F − IC) is larger for linguistic
    levels than mathematical levels — natural language translation loses
    more coherence to channel divergence because linguistic levels have
    wider variation across channels (high semantic preservation but low
    invertibility, or vice versa). Mathematical levels maintain more
    uniform channel profiles.
    """
    ling_results = [r for r in results if r.domain == "linguistic"]
    math_results = [r for r in results if r.domain == "mathematical"]
    ling_gaps = [r.F - r.IC for r in ling_results]
    math_gaps = [r.F - r.IC for r in math_results]
    ling_mean_gap = float(np.mean(ling_gaps))
    math_mean_gap = float(np.mean(math_gaps))
    passed = ling_mean_gap > math_mean_gap
    return {
        "name": "T-TL-6",
        "passed": bool(passed),
        "linguistic_mean_gap": ling_mean_gap,
        "mathematical_mean_gap": math_mean_gap,
        "difference": ling_mean_gap - math_mean_gap,
    }


def verify_all_theorems() -> list[dict]:
    """Run all T-TL theorems."""
    results = compute_all_entities()
    return [
        verify_t_tl_1(results),
        verify_t_tl_2(results),
        verify_t_tl_3(results),
        verify_t_tl_4(results),
        verify_t_tl_5(results),
        verify_t_tl_6(results),
    ]


# ── Cross-Level Analysis ─────────────────────────────────────────────


def analyze_translation_structure() -> dict:
    """Structural analysis across all 12 translation levels.

    Computes per-domain statistics, identifies the levels where fidelity
    concentrates vs. where it drops, and measures the Rosetta invariance
    property: same kernel, different domains, comparable verdicts.
    """
    results = compute_all_entities()
    domains = {"linguistic", "mathematical"}
    analysis: dict = {"per_domain": {}, "all_results": [r.to_dict() for r in results]}

    for d in domains:
        dr = [r for r in results if r.domain == d]
        analysis["per_domain"][d] = {
            "mean_F": float(np.mean([r.F for r in dr])),
            "mean_IC": float(np.mean([r.IC for r in dr])),
            "mean_omega": float(np.mean([r.omega for r in dr])),
            "mean_gap": float(np.mean([r.F - r.IC for r in dr])),
            "regimes": {r.name: r.regime for r in dr},
        }

    # Rosetta invariance check: same identities hold for both domains
    all_duality = all(abs(r.F + r.omega - 1.0) < 1e-12 for r in results)
    all_bound = all(r.IC <= r.F + 1e-12 for r in results)
    analysis["rosetta_invariance"] = {
        "duality_all_hold": all_duality,
        "integrity_bound_all_hold": all_bound,
    }

    return analysis
