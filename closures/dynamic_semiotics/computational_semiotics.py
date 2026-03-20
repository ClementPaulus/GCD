"""Computational Semiotics Closure — Dynamic Semiotics Domain.

Tier-2 closure mapping 12 computational sign-processing systems through
the GCD kernel.  Each system is characterized by 8 channels drawn from
computational linguistics, information retrieval, and digital communication.

Channels (8, equal weights w_i = 1/8):
  0  semantic_fidelity       — meaning preservation (1 = perfect)
  1  syntactic_regularity    — rule-following in form (1 = perfectly regular)
  2  context_sensitivity     — responsiveness to context (1 = fully context-aware)
  3  referential_grounding   — connection to real-world referents (1 = fully grounded)
  4  compositionality        — meaning derivable from parts (1 = fully compositional)
  5  interpretive_stability  — consistency across interpreters (1 = perfectly stable)
  6  noise_resistance        — robustness to degradation (1 = noise-proof)
  7  generative_capacity     — ability to produce novel signs (1 = unlimited)

12 entities across 4 categories:
  Algorithmic (3): spell_checker, grammar_parser, sentiment_analyzer
  Social media (3): hashtag_system, emoji_language, meme_propagation
  Translation (3): machine_translation, cross_lingual_retrieval, code_switching
  Generative (3): text_generator, image_captioner, sign_language_synthesis

6 theorems (T-CS-1 through T-CS-6).
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

CS_CHANNELS = [
    "semantic_fidelity",
    "syntactic_regularity",
    "context_sensitivity",
    "referential_grounding",
    "compositionality",
    "interpretive_stability",
    "noise_resistance",
    "generative_capacity",
]
N_CS_CHANNELS = len(CS_CHANNELS)


@dataclass(frozen=True, slots=True)
class ComputationalSemioticEntity:
    """A computational sign-processing system with 8 measurable channels."""

    name: str
    category: str
    semantic_fidelity: float
    syntactic_regularity: float
    context_sensitivity: float
    referential_grounding: float
    compositionality: float
    interpretive_stability: float
    noise_resistance: float
    generative_capacity: float

    def trace_vector(self) -> np.ndarray:
        return np.array(
            [
                self.semantic_fidelity,
                self.syntactic_regularity,
                self.context_sensitivity,
                self.referential_grounding,
                self.compositionality,
                self.interpretive_stability,
                self.noise_resistance,
                self.generative_capacity,
            ]
        )


CS_ENTITIES: tuple[ComputationalSemioticEntity, ...] = (
    # Algorithmic — rule-based, deterministic, narrow scope
    ComputationalSemioticEntity("spell_checker", "algorithmic", 0.75, 0.95, 0.30, 0.70, 0.50, 0.90, 0.85, 0.20),
    ComputationalSemioticEntity("grammar_parser", "algorithmic", 0.80, 0.85, 0.55, 0.65, 0.85, 0.85, 0.70, 0.25),
    ComputationalSemioticEntity("sentiment_analyzer", "algorithmic", 0.60, 0.50, 0.70, 0.45, 0.40, 0.55, 0.50, 0.15),
    # Social media — informal, context-heavy, rapid drift
    ComputationalSemioticEntity("hashtag_system", "social_media", 0.40, 0.30, 0.75, 0.25, 0.20, 0.30, 0.35, 0.85),
    ComputationalSemioticEntity("emoji_language", "social_media", 0.35, 0.20, 0.80, 0.35, 0.15, 0.25, 0.50, 0.70),
    ComputationalSemioticEntity("meme_propagation", "social_media", 0.20, 0.10, 0.85, 0.15, 0.10, 0.10, 0.20, 0.80),
    # Translation — cross-linguistic mapping, moderate complexity
    ComputationalSemioticEntity("machine_translation", "translation", 0.85, 0.85, 0.45, 0.70, 0.75, 0.55, 0.30, 0.85),
    ComputationalSemioticEntity(
        "cross_lingual_retrieval", "translation", 0.65, 0.55, 0.60, 0.70, 0.50, 0.65, 0.60, 0.30
    ),
    ComputationalSemioticEntity("code_switching", "translation", 0.55, 0.35, 0.90, 0.60, 0.45, 0.40, 0.35, 0.75),
    # Generative — novel sign production, high generative capacity
    ComputationalSemioticEntity("text_generator", "generative", 0.55, 0.80, 0.70, 0.40, 0.65, 0.45, 0.50, 0.95),
    ComputationalSemioticEntity("image_captioner", "generative", 0.65, 0.75, 0.50, 0.70, 0.55, 0.55, 0.45, 0.80),
    ComputationalSemioticEntity(
        "sign_language_synthesis", "generative", 0.50, 0.60, 0.65, 0.60, 0.70, 0.40, 0.35, 0.85
    ),
)


@dataclass(frozen=True, slots=True)
class CSKernelResult:
    """Kernel output for a computational semiotic entity."""

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


def compute_cs_kernel(entity: ComputationalSemioticEntity) -> CSKernelResult:
    """Compute GCD kernel for a computational semiotic entity."""
    c = entity.trace_vector()
    c = np.clip(c, EPSILON, 1.0 - EPSILON)
    w = np.ones(N_CS_CHANNELS) / N_CS_CHANNELS
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
    return CSKernelResult(
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


def compute_all_entities() -> list[CSKernelResult]:
    """Compute kernel outputs for all computational semiotic entities."""
    return [compute_cs_kernel(e) for e in CS_ENTITIES]


# ── Theorems ──────────────────────────────────────────────────────────


def verify_t_cs_1(results: list[CSKernelResult]) -> dict:
    """T-CS-1: Spell checker has highest syntactic regularity — rule-based,
    deterministic correction operates on fixed lexical rules.
    """
    sc = next(e for e in CS_ENTITIES if e.name == "spell_checker")
    max_syn = max(e.syntactic_regularity for e in CS_ENTITIES)
    passed = abs(sc.syntactic_regularity - max_syn) < 0.01
    return {
        "name": "T-CS-1",
        "passed": bool(passed),
        "spell_checker_syn": sc.syntactic_regularity,
        "max_syn": float(max_syn),
    }


def verify_t_cs_2(results: list[CSKernelResult]) -> dict:
    """T-CS-2: Social media category has lowest mean referential grounding —
    hashtags, emoji, and memes are loosely connected to fixed referents.
    """
    cats = {e.category for e in CS_ENTITIES}
    cat_means = {}
    for cat in cats:
        vals = [e.referential_grounding for e in CS_ENTITIES if e.category == cat]
        cat_means[cat] = float(np.mean(vals))
    sm_mean = cat_means["social_media"]
    passed = all(sm_mean <= v + 1e-9 for v in cat_means.values())
    return {
        "name": "T-CS-2",
        "passed": bool(passed),
        "social_media_ref": sm_mean,
        "all_means": cat_means,
    }


def verify_t_cs_3(results: list[CSKernelResult]) -> dict:
    """T-CS-3: Meme propagation is in Collapse regime — rapid semantic drift,
    near-zero interpretive stability, and minimal compositionality.
    """
    meme = next(r for r in results if r.name == "meme_propagation")
    passed = meme.regime == "Collapse"
    return {
        "name": "T-CS-3",
        "passed": bool(passed),
        "meme_regime": meme.regime,
        "meme_omega": meme.omega,
    }


def verify_t_cs_4(results: list[CSKernelResult]) -> dict:
    """T-CS-4: Machine translation has largest heterogeneity gap among
    translation systems — high syntactic regularity and generative capacity
    paired with low noise resistance creates channel divergence.
    """
    trans = [r for r in results if r.category == "translation"]
    gaps = {r.name: r.F - r.IC for r in trans}
    mt_gap = gaps["machine_translation"]
    passed = all(mt_gap >= v - 1e-9 for v in gaps.values())
    return {
        "name": "T-CS-4",
        "passed": bool(passed),
        "mt_gap": float(mt_gap),
        "translation_gaps": {k: float(v) for k, v in gaps.items()},
    }


def verify_t_cs_5(results: list[CSKernelResult]) -> dict:
    """T-CS-5: Generative category has highest mean generative capacity —
    text generators, captioners, and synthesis systems are designed to produce.
    """
    cats = {e.category for e in CS_ENTITIES}
    cat_means = {}
    for cat in cats:
        vals = [e.generative_capacity for e in CS_ENTITIES if e.category == cat]
        cat_means[cat] = float(np.mean(vals))
    gen_mean = cat_means["generative"]
    passed = all(gen_mean >= v - 1e-9 for v in cat_means.values())
    return {
        "name": "T-CS-5",
        "passed": bool(passed),
        "generative_cap": gen_mean,
        "all_means": cat_means,
    }


def verify_t_cs_6(results: list[CSKernelResult]) -> dict:
    """T-CS-6: Grammar parser has highest F among algorithmic systems —
    compositional analysis over structured input gives balanced channel profile.
    """
    alg = [r for r in results if r.category == "algorithmic"]
    gp = next(r for r in alg if r.name == "grammar_parser")
    max_F = max(r.F for r in alg)
    passed = abs(gp.F - max_F) < 0.02
    return {
        "name": "T-CS-6",
        "passed": bool(passed),
        "grammar_parser_F": gp.F,
        "algorithmic_max_F": float(max_F),
    }


def verify_all_theorems() -> list[dict]:
    """Run all T-CS theorems."""
    results = compute_all_entities()
    return [
        verify_t_cs_1(results),
        verify_t_cs_2(results),
        verify_t_cs_3(results),
        verify_t_cs_4(results),
        verify_t_cs_5(results),
        verify_t_cs_6(results),
    ]


def main() -> None:
    """Entry point."""
    results = compute_all_entities()
    print("=" * 78)
    print("COMPUTATIONAL SEMIOTICS — GCD KERNEL ANALYSIS")
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
