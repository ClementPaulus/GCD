"""
Semiotic Kernel — The GCD Kernel Applied to Dynamic Semiotics

Maps 30 sign systems across the phylogenesis of meaning to 8-channel trace
vectors and computes Tier-1 invariants. Demonstrates that semiotic processes
are instances of collapse-return structure.

Channels (8):
    1. sign_repertoire      — Vocabulary size / symbol space richness
    2. interpretant_depth   — Recursion depth of interpretation chains
    3. ground_stability     — Convention persistence (how frozen is the contract?)
    4. translation_fidelity — Cross-lens Rosetta preservation (F across lenses)
    5. semiotic_density     — Signs per unit of discourse
    6. indexical_coupling   — Connection strength between sign and object (C-like)
    7. iconic_persistence   — How well the sign resembles its object over time
    8. symbolic_recursion   — Self-referential capacity (language about language)

Key GCD predictions for sign systems:
    - F + ω = 1: What a sign system preserves + what it loses = 1 (exhaustive)
    - IC ≤ F: Semiotic coherence cannot exceed mean channel fidelity
    - Geometric slaughter: ONE dead channel kills IC → a sign system with
      zero ground stability or zero interpretant depth collapses regardless
      of how rich its vocabulary is
    - Heterogeneity gap Δ = F - IC: semiotic fragility metric
    - Natural languages: high sign_repertoire, high symbolic_recursion,
      moderate iconic_persistence → high Δ (fragile to convention drift)
    - Formal systems: high ground_stability, low iconic_persistence →
      low Δ (robust but brittle to breakage)
    - Dead languages: τ_R = ∞_rec (no living community → the sign system
      is a gestus — internally consistent but non-returning)

Connection to brain_kernel channel 8 (language_architecture):
    The brain kernel measures language_architecture = 0.98 for Homo sapiens
    as a single normalized channel. This module unpacks that channel into
    8 measurable dimensions of the sign systems that language_architecture
    enables. The semiotic kernel is the Tier-2 formalization of what the
    brain kernel registers as raw neural capacity.

Data sources:
    Trait values are normalized estimates from linguistics, semiotics,
    information science, and communication theory literature. Each value
    represents a structural ranking within the diversity of sign systems,
    not absolute measurements. The kernel results are structural — they
    depend on the pattern of channels, not the exact values.

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

# ── Guard band ────────────────────────────────────────────────────
EPS = 1e-6  # Closure-level epsilon (above frozen ε = 1e-8)


# ═════════════════════════════════════════════════════════════════════
# SECTION 1: CHANNEL DEFINITIONS
# ═════════════════════════════════════════════════════════════════════

SEMIOTIC_CHANNELS: list[str] = [
    "sign_repertoire",  # Vocabulary size / symbol space richness
    "interpretant_depth",  # Recursion depth of interpretation chains
    "ground_stability",  # Convention persistence (how frozen is the contract?)
    "translation_fidelity",  # Cross-lens Rosetta preservation (F across lenses)
    "semiotic_density",  # Signs per unit of discourse
    "indexical_coupling",  # Connection strength between sign and object
    "iconic_persistence",  # How well the sign resembles its object over time
    "symbolic_recursion",  # Self-referential capacity (language about language)
]

N_SEMIOTIC_CHANNELS = len(SEMIOTIC_CHANNELS)  # 8


# ═════════════════════════════════════════════════════════════════════
# SECTION 2: SIGN SYSTEM PROFILE
# ═════════════════════════════════════════════════════════════════════


@dataclass(frozen=True, slots=True)
class SignSystem:
    """A sign system profiled across 8 semiotic channels.

    All values normalized to [0, 1] representing relative standing
    within the full diversity of sign systems. These are structural
    rankings from semiotics, linguistics, and information theory,
    not absolute measurements.
    """

    # Identity
    name: str
    category: str  # Natural Language, Formal System, Sensory Code, etc.
    medium: str  # Spoken, Written, Visual, Gestural, Digital, Chemical, etc.
    status: str  # "living", "dead", "extinct", "artificial"

    # 8 channels — normalized [0, 1]
    sign_repertoire: float  # Vocabulary / symbol space richness
    interpretant_depth: float  # Recursion depth of interpretation chains
    ground_stability: float  # Convention persistence
    translation_fidelity: float  # Cross-context meaning preservation
    semiotic_density: float  # Signs per unit of discourse
    indexical_coupling: float  # Connection strength: sign ↔ object
    iconic_persistence: float  # Resemblance persistence over time
    symbolic_recursion: float  # Self-referential capacity

    def trace_vector(self) -> np.ndarray:
        """Return 8-channel trace vector, ε-clamped."""
        c = np.array(
            [
                self.sign_repertoire,
                self.interpretant_depth,
                self.ground_stability,
                self.translation_fidelity,
                self.semiotic_density,
                self.indexical_coupling,
                self.iconic_persistence,
                self.symbolic_recursion,
            ],
            dtype=np.float64,
        )
        return np.clip(c, EPSILON, 1.0 - EPSILON)


# ═════════════════════════════════════════════════════════════════════
# SECTION 3: RESULT CONTAINER
# ═════════════════════════════════════════════════════════════════════


@dataclass
class SemioticKernelResult:
    """Kernel result for a single sign system.

    Contains Tier-1 invariants (immutable structural identities),
    identity verification flags, and domain-specific classification.
    """

    # Identity
    name: str
    category: str
    medium: str
    status: str

    # Kernel input
    n_channels: int
    channel_labels: list[str]
    trace_vector: list[float]

    # Tier-1 invariants (IMMUTABLE — from kernel_optimized)
    F: float  # Fidelity = mean channel value
    omega: float  # Drift = 1 - F
    S: float  # Bernoulli field entropy
    C: float  # Curvature
    kappa: float  # Log-integrity
    IC: float  # Integrity composite = exp(κ)
    heterogeneity_gap: float  # Δ = F - IC

    # Identity checks (Tier-1 verification)
    F_plus_omega: float
    IC_leq_F: bool
    IC_eq_exp_kappa: bool

    # Classification (domain-specific)
    regime: str  # Stable | Watch | Collapse
    semiotic_type: str  # Alive Recursive | Stable Formal | etc.

    # Channel extrema
    weakest_channel: str
    weakest_value: float
    strongest_channel: str
    strongest_value: float

    # Sensitivity: IC contribution per channel
    channel_sensitivities: dict[str, float]

    def to_dict(self) -> dict[str, Any]:
        """Serialize to dictionary."""
        return asdict(self)


# ═════════════════════════════════════════════════════════════════════
# SECTION 4: SIGN SYSTEM CATALOG (30 systems)
# ═════════════════════════════════════════════════════════════════════
#
# Normalization conventions:
#   sign_repertoire: vocabulary size normalized to [0,1]
#     (Natural language ~100K+ words → high; pheromones ~20 → low)
#   interpretant_depth: layers of interpretation possible
#     (Literature/philosophy → 0.95; traffic signs → 0.05)
#   ground_stability: how frozen/persistent are conventions
#     (Mathematical notation → 0.98; slang → 0.15)
#   translation_fidelity: meaning preservation across contexts
#     (Formal logic → 0.95; poetry → 0.25)
#   semiotic_density: signs packed per unit of discourse
#     (Chinese characters → 0.90; Morse code → 0.10)
#   indexical_coupling: how tightly sign connects to object
#     (Pointing gesture → 0.95; abstract art → 0.10)
#   iconic_persistence: resemblance stability over time
#     (Pictograms → 0.85; metaphors → 0.20)
#   symbolic_recursion: language-about-language capacity
#     (Natural language → 0.95; bee dance → 0.001)

SIGN_SYSTEMS: tuple[SignSystem, ...] = (
    # ── NATURAL LANGUAGES (living) ─────────────────────────────────
    SignSystem(
        name="Modern English",
        category="Natural Language",
        medium="Spoken/Written",
        status="living",
        sign_repertoire=0.92,  # ~170K words in OED
        interpretant_depth=0.90,  # Deep literary/philosophical tradition
        ground_stability=0.55,  # Moderate — evolving rapidly
        translation_fidelity=0.60,  # Cross-cultural loss significant
        semiotic_density=0.65,  # Medium density (analytic grammar)
        indexical_coupling=0.40,  # Largely arbitrary sign-object
        iconic_persistence=0.25,  # Few onomatopoeia survive
        symbolic_recursion=0.95,  # Full metalinguistic capacity
    ),
    SignSystem(
        name="Mandarin Chinese",
        category="Natural Language",
        medium="Spoken/Written",
        status="living",
        sign_repertoire=0.88,  # ~50K characters, rich compounds
        interpretant_depth=0.85,  # Deep philosophical tradition
        ground_stability=0.70,  # Character system persists millennia
        translation_fidelity=0.50,  # Tonal + cultural loss in translation
        semiotic_density=0.90,  # Characters pack meaning densely
        indexical_coupling=0.45,  # Some ideographic residue
        iconic_persistence=0.55,  # Radical system retains pictographic traces
        symbolic_recursion=0.90,  # Full metalinguistic capacity
    ),
    SignSystem(
        name="Arabic (Modern Standard)",
        category="Natural Language",
        medium="Spoken/Written",
        status="living",
        sign_repertoire=0.85,  # Root-pattern morphology → massive derivation
        interpretant_depth=0.88,  # Quranic + literary exegesis tradition
        ground_stability=0.75,  # Classical anchor stabilizes MSA
        translation_fidelity=0.55,  # Diglossia complicates translation
        semiotic_density=0.80,  # Triliteral roots pack meaning
        indexical_coupling=0.35,  # Arbitrary sign-object
        iconic_persistence=0.20,  # Root structure is abstract
        symbolic_recursion=0.88,  # Strong grammatical tradition
    ),
    SignSystem(
        name="Japanese",
        category="Natural Language",
        medium="Spoken/Written",
        status="living",
        sign_repertoire=0.90,  # Kanji + hiragana + katakana + English loans
        interpretant_depth=0.85,  # Literary + aesthetic tradition
        ground_stability=0.65,  # Writing system stable, spoken evolves
        translation_fidelity=0.45,  # High context-dependence → loss
        semiotic_density=0.88,  # Multiple scripts densely packed
        indexical_coupling=0.50,  # Kanji retains ideographic nature
        iconic_persistence=0.50,  # Kanji ideograms persist
        symbolic_recursion=0.85,  # Full metalinguistic capacity
    ),
    SignSystem(
        name="Pirahã",
        category="Natural Language",
        medium="Spoken",
        status="living",
        sign_repertoire=0.15,  # ~100 words, no color terms, no numerals
        interpretant_depth=0.20,  # Immediacy of experience only
        ground_stability=0.80,  # Extremely stable (no borrowing)
        translation_fidelity=0.10,  # Near-untranslatable cultural categories
        semiotic_density=0.25,  # Sparse vocabulary, tonal richness
        indexical_coupling=0.85,  # Highly indexical — present-reference only
        iconic_persistence=0.60,  # Iconic/onomatopoetic elements persist
        symbolic_recursion=0.05,  # No embedding, no recursion reported
    ),
    # ── NATURAL LANGUAGES (dead/extinct) ──────────────────────────
    SignSystem(
        name="Latin (Classical)",
        category="Natural Language",
        medium="Written",
        status="dead",
        sign_repertoire=0.75,  # ~50K attested words
        interpretant_depth=0.92,  # 2000+ years of scholarly exegesis
        ground_stability=0.95,  # Frozen corpus — maximum stability
        translation_fidelity=0.70,  # Well-studied translation traditions
        semiotic_density=0.82,  # Inflected grammar packs case/tense
        indexical_coupling=0.30,  # No living speech community
        iconic_persistence=0.35,  # Abstract morphology
        symbolic_recursion=0.85,  # Full recursive grammar
    ),
    SignSystem(
        name="Sumerian",
        category="Natural Language",
        medium="Written (cuneiform)",
        status="extinct",
        sign_repertoire=0.40,  # ~1000 cuneiform signs
        interpretant_depth=0.50,  # Partial decipherment
        ground_stability=0.92,  # Clay is durable
        translation_fidelity=0.30,  # Major gaps in understanding
        semiotic_density=0.60,  # Logographic/syllabic mix
        indexical_coupling=0.15,  # No community, partial reference
        iconic_persistence=0.65,  # Early pictographic origins preserved
        symbolic_recursion=0.35,  # Some embedding, limited metalanguage
    ),
    # ── FORMAL SYSTEMS ─────────────────────────────────────────────
    SignSystem(
        name="Mathematical Notation",
        category="Formal System",
        medium="Written/Digital",
        status="living",
        sign_repertoire=0.70,  # Greek + Latin + specialized symbols
        interpretant_depth=0.95,  # Unlimited derivation depth
        ground_stability=0.98,  # Centuries of frozen convention
        translation_fidelity=0.95,  # Cross-cultural near-perfect
        semiotic_density=0.95,  # Maximally dense (equations)
        indexical_coupling=0.15,  # Abstract — no physical referent
        iconic_persistence=0.30,  # Some geometric icons persist
        symbolic_recursion=0.98,  # Full Gödelian self-reference
    ),
    SignSystem(
        name="Formal Logic (First-Order)",
        category="Formal System",
        medium="Written/Digital",
        status="living",
        sign_repertoire=0.30,  # Small alphabet: ∀ ∃ → ∧ ∨ ¬
        interpretant_depth=0.92,  # Deep proof chains
        ground_stability=0.98,  # Frege → now, nearly unchanged
        translation_fidelity=0.98,  # Model-theoretic precision
        semiotic_density=0.85,  # Dense in proof texts
        indexical_coupling=0.05,  # Pure abstraction
        iconic_persistence=0.10,  # No iconic element
        symbolic_recursion=0.95,  # Self-reference central (Gödel)
    ),
    SignSystem(
        name="Programming Languages (general)",
        category="Formal System",
        medium="Digital",
        status="living",
        sign_repertoire=0.65,  # Keywords + APIs + identifiers
        interpretant_depth=0.80,  # Call stacks, metaprogramming
        ground_stability=0.60,  # Rapid evolution (1-5 yr cycles)
        translation_fidelity=0.75,  # Transpilation, polyglot possible
        semiotic_density=0.80,  # Dense instruction per line
        indexical_coupling=0.70,  # Variables bind to memory addresses
        iconic_persistence=0.15,  # Abstract syntax
        symbolic_recursion=0.90,  # Reflection, macros, quines
    ),
    SignSystem(
        name="DNA/RNA Genetic Code",
        category="Formal System",
        medium="Chemical",
        status="living",
        sign_repertoire=0.10,  # 4 bases, 64 codons, 20 amino acids
        interpretant_depth=0.70,  # Gene → mRNA → protein → phenotype
        ground_stability=0.99,  # 3.8 Gyr, near-universal
        translation_fidelity=0.92,  # Central dogma is highly conserved
        semiotic_density=0.95,  # 3 bases = 1 amino acid, maximally dense
        indexical_coupling=0.90,  # Direct causal: codon → amino acid
        iconic_persistence=0.05,  # No resemblance sign-object
        symbolic_recursion=0.15,  # Regulatory genes (meta-coding) are limited
    ),
    # ── VISUAL SIGN SYSTEMS ───────────────────────────────────────
    SignSystem(
        name="International Road Signs",
        category="Visual Code",
        medium="Visual/Physical",
        status="living",
        sign_repertoire=0.20,  # ~200 standard signs
        interpretant_depth=0.05,  # Single-layer: sign → action
        ground_stability=0.90,  # Vienna Convention 1968 → stable
        translation_fidelity=0.85,  # Cross-cultural by design
        semiotic_density=0.10,  # One sign at a time
        indexical_coupling=0.80,  # Points to immediate context
        iconic_persistence=0.90,  # Pictographic — high resemblance
        symbolic_recursion=0.001,  # No metalinguistic capacity
    ),
    SignSystem(
        name="Egyptian Hieroglyphs",
        category="Visual Code",
        medium="Written (carved/painted)",
        status="extinct",
        sign_repertoire=0.55,  # ~700-1000 standard hieroglyphs
        interpretant_depth=0.60,  # Religious, administrative, literary
        ground_stability=0.88,  # 3000+ years of use
        translation_fidelity=0.40,  # Partially deciphered via Rosetta Stone
        semiotic_density=0.70,  # Logographic + phonetic
        indexical_coupling=0.25,  # Community extinct
        iconic_persistence=0.85,  # Highly pictographic
        symbolic_recursion=0.30,  # Some rebus/determinative metalayers
    ),
    SignSystem(
        name="Emoji (Unicode Standard)",
        category="Visual Code",
        medium="Digital",
        status="living",
        sign_repertoire=0.45,  # ~3600 standard emoji
        interpretant_depth=0.25,  # Shallow: emotional/iconic
        ground_stability=0.40,  # Rapid drift in interpretation
        translation_fidelity=0.35,  # Culture-dependent reading
        semiotic_density=0.60,  # Can densely supplement text
        indexical_coupling=0.50,  # Some point to real objects
        iconic_persistence=0.70,  # Strong visual resemblance
        symbolic_recursion=0.10,  # Minimal meta-capacity
    ),
    SignSystem(
        name="Abstract Painting (Modern Art)",
        category="Aesthetic System",
        medium="Visual",
        status="living",
        sign_repertoire=0.80,  # Unlimited formal vocabulary
        interpretant_depth=0.85,  # Deep critical/philosophical readings
        ground_stability=0.15,  # Deliberately unstable conventions
        translation_fidelity=0.10,  # Radically context-dependent
        semiotic_density=0.70,  # Dense visual information
        indexical_coupling=0.10,  # Deliberate decoupling from referent
        iconic_persistence=0.20,  # Anti-representational
        symbolic_recursion=0.65,  # Art about art is central
    ),
    # ── AUDITORY SIGN SYSTEMS ─────────────────────────────────────
    SignSystem(
        name="Western Tonal Music",
        category="Auditory System",
        medium="Auditory/Written",
        status="living",
        sign_repertoire=0.75,  # 12-TET, harmonic vocabulary
        interpretant_depth=0.80,  # Deep musicological analysis
        ground_stability=0.70,  # Common practice period stable
        translation_fidelity=0.55,  # Cultural encoding varies
        semiotic_density=0.85,  # Polyphonic: multiple streams
        indexical_coupling=0.30,  # Emotional, not referential
        iconic_persistence=0.50,  # Some word-painting traditions
        symbolic_recursion=0.60,  # Musical quotation, fugue subjects
    ),
    SignSystem(
        name="Morse Code",
        category="Formal System",
        medium="Auditory/Visual",
        status="dead",
        sign_repertoire=0.12,  # 26 letters + 10 digits + punctuation
        interpretant_depth=0.10,  # 1:1 encoding → decoding
        ground_stability=0.95,  # Frozen for 170+ years
        translation_fidelity=0.95,  # Perfect: isomorphic to alphabet
        semiotic_density=0.10,  # Sparse (sequential pulses)
        indexical_coupling=0.05,  # Pure encoding, no referent
        iconic_persistence=0.05,  # No resemblance
        symbolic_recursion=0.05,  # No metalinguistic layer
    ),
    # ── GESTURAL & EMBODIED ───────────────────────────────────────
    SignSystem(
        name="American Sign Language (ASL)",
        category="Natural Language",
        medium="Gestural/Visual",
        status="living",
        sign_repertoire=0.70,  # Full natural language vocabulary
        interpretant_depth=0.80,  # Literary, poetic, philosophical use
        ground_stability=0.55,  # Evolving, community-driven
        translation_fidelity=0.55,  # ASL ≠ signed English
        semiotic_density=0.75,  # Simultaneous morphology (classifiers)
        indexical_coupling=0.65,  # Spatial grammar points to referents
        iconic_persistence=0.60,  # Many iconic signs persist
        symbolic_recursion=0.85,  # Full recursive grammar
    ),
    SignSystem(
        name="Pointing Gesture (Deixis)",
        category="Gestural",
        medium="Embodied",
        status="living",
        sign_repertoire=0.05,  # One gesture type
        interpretant_depth=0.03,  # Immediate reference only
        ground_stability=0.95,  # Universal across cultures
        translation_fidelity=0.90,  # Nearly universal
        semiotic_density=0.05,  # One sign at a time
        indexical_coupling=0.99,  # Maximal: sign IS its direction
        iconic_persistence=0.90,  # The point resembles its reference axis
        symbolic_recursion=0.001,  # Cannot point at pointing
    ),
    # ── ANIMAL COMMUNICATION ──────────────────────────────────────
    SignSystem(
        name="Honeybee Waggle Dance",
        category="Animal Communication",
        medium="Embodied/Visual",
        status="living",
        sign_repertoire=0.08,  # Direction + distance + quality
        interpretant_depth=0.10,  # Fixed interpretation: food source
        ground_stability=0.95,  # Genetically encoded, species-wide
        translation_fidelity=0.85,  # Works across colonies
        semiotic_density=0.15,  # One message per dance
        indexical_coupling=0.90,  # Points to actual location
        iconic_persistence=0.70,  # Dance angle = sun angle (iconic)
        symbolic_recursion=0.001,  # No meta-dance
    ),
    SignSystem(
        name="Vervet Monkey Alarm Calls",
        category="Animal Communication",
        medium="Auditory",
        status="living",
        sign_repertoire=0.08,  # ~6 distinct alarm types
        interpretant_depth=0.10,  # Fixed: call → predator type → action
        ground_stability=0.90,  # Genetic + early learning
        translation_fidelity=0.80,  # Cross-group intelligibility
        semiotic_density=0.05,  # One call at a time
        indexical_coupling=0.85,  # Refers to present threat
        iconic_persistence=0.30,  # Some acoustic resemblance to threat
        symbolic_recursion=0.001,  # No meta-calls
    ),
    SignSystem(
        name="Whale Song (Humpback)",
        category="Animal Communication",
        medium="Auditory",
        status="living",
        sign_repertoire=0.35,  # ~100-300 units, hierarchical
        interpretant_depth=0.30,  # Population-level themes, unknown depth
        ground_stability=0.30,  # Songs evolve annually
        translation_fidelity=0.25,  # Populations diverge
        semiotic_density=0.40,  # Extended temporal sequences
        indexical_coupling=0.40,  # Social/territorial reference
        iconic_persistence=0.20,  # Unknown iconic content
        symbolic_recursion=0.10,  # Hierarchical but no proven recursion
    ),
    SignSystem(
        name="Ant Pheromone Trails",
        category="Animal Communication",
        medium="Chemical",
        status="living",
        sign_repertoire=0.06,  # ~20 pheromone types
        interpretant_depth=0.05,  # Fixed: pheromone → action
        ground_stability=0.98,  # Genetically hardwired
        translation_fidelity=0.85,  # Species-specific but reliable
        semiotic_density=0.08,  # Binary: trail present/absent
        indexical_coupling=0.95,  # Chemical directly at location
        iconic_persistence=0.05,  # No resemblance
        symbolic_recursion=0.001,  # No meta-pheromone
    ),
    # ── DIGITAL / ARTIFICIAL ──────────────────────────────────────
    SignSystem(
        name="HTML/Web Markup",
        category="Formal System",
        medium="Digital",
        status="living",
        sign_repertoire=0.50,  # ~100 elements + attributes
        interpretant_depth=0.40,  # DOM tree → rendering → user
        ground_stability=0.55,  # W3C standards, but version churn
        translation_fidelity=0.70,  # Cross-browser rendering
        semiotic_density=0.75,  # Dense markup per document
        indexical_coupling=0.60,  # URLs point to resources
        iconic_persistence=0.10,  # Abstract tags
        symbolic_recursion=0.50,  # Templates, components
    ),
    SignSystem(
        name="Bitcoin Blockchain",
        category="Formal System",
        medium="Digital/Cryptographic",
        status="living",
        sign_repertoire=0.15,  # Transactions, blocks, scripts
        interpretant_depth=0.50,  # Transaction → verification → consensus
        ground_stability=0.92,  # Protocol extremely stable
        translation_fidelity=0.90,  # Deterministic: all nodes agree
        semiotic_density=0.30,  # One transaction, full provenance
        indexical_coupling=0.85,  # Hash → exact block (causal chain)
        iconic_persistence=0.05,  # No resemblance
        symbolic_recursion=0.20,  # Smart contracts limited (Bitcoin Script)
    ),
    SignSystem(
        name="Large Language Model Output",
        category="Artificial System",
        medium="Digital/Textual",
        status="living",
        sign_repertoire=0.93,  # Token vocabulary ~100K+
        interpretant_depth=0.75,  # Multi-turn, contextual
        ground_stability=0.20,  # Probabilistic, non-deterministic
        translation_fidelity=0.55,  # Cross-prompt inconsistency
        semiotic_density=0.85,  # Dense natural language output
        indexical_coupling=0.15,  # No causal grounding in world
        iconic_persistence=0.10,  # No stable resemblance
        symbolic_recursion=0.70,  # Can discuss its own output
    ),
    # ── SPECIALIZED CODES ─────────────────────────────────────────
    SignSystem(
        name="Braille",
        category="Tactile Code",
        medium="Tactile",
        status="living",
        sign_repertoire=0.35,  # 63 cells (2×3 dot matrix)
        interpretant_depth=0.15,  # 1:1 encoding of text
        ground_stability=0.90,  # Frozen since 1829
        translation_fidelity=0.92,  # Isomorphic to print
        semiotic_density=0.40,  # Sequential reading
        indexical_coupling=0.10,  # Pure encoding
        iconic_persistence=0.05,  # No resemblance to referent
        symbolic_recursion=0.10,  # No meta-layer
    ),
    SignSystem(
        name="Maritime Flag Signals",
        category="Visual Code",
        medium="Visual/Physical",
        status="living",
        sign_repertoire=0.18,  # 26 letter + 10 numeral + special flags
        interpretant_depth=0.10,  # Fixed meanings per flag
        ground_stability=0.88,  # International Signal Code stable
        translation_fidelity=0.90,  # Cross-national by design
        semiotic_density=0.08,  # One flag hoist at a time
        indexical_coupling=0.70,  # Refers to immediate maritime context
        iconic_persistence=0.40,  # Some flags iconic (red = danger)
        symbolic_recursion=0.001,  # No meta-flag
    ),
    SignSystem(
        name="Chemical Formula Notation",
        category="Formal System",
        medium="Written",
        status="living",
        sign_repertoire=0.45,  # 118 elements + bonds + notation
        interpretant_depth=0.75,  # Formula → structure → properties
        ground_stability=0.95,  # IUPAC conventions frozen
        translation_fidelity=0.95,  # Universal across all chemistry
        semiotic_density=0.90,  # H₂SO₄ encodes full structure
        indexical_coupling=0.80,  # Direct: symbol → element
        iconic_persistence=0.15,  # No visual resemblance to molecules
        symbolic_recursion=0.40,  # Functional group abstraction
    ),
    SignSystem(
        name="Musical Score (Western Notation)",
        category="Formal System",
        medium="Written/Visual",
        status="living",
        sign_repertoire=0.55,  # Notes, rests, dynamics, tempo marks
        interpretant_depth=0.50,  # Score → performance → listener
        ground_stability=0.85,  # Staff notation stable since ~1600
        translation_fidelity=0.70,  # Interpretation varies by performer
        semiotic_density=0.80,  # Full orchestra on one page
        indexical_coupling=0.60,  # Pitch maps to frequency
        iconic_persistence=0.55,  # Note height = pitch height (iconic)
        symbolic_recursion=0.30,  # Da capo, repeats, codas
    ),
)

N_SIGN_SYSTEMS = len(SIGN_SYSTEMS)  # 30


# ═════════════════════════════════════════════════════════════════════
# SECTION 5: NORMALIZATION
# ═════════════════════════════════════════════════════════════════════


def normalize_sign_system(ss: SignSystem) -> tuple[np.ndarray, np.ndarray, list[str]]:
    """Map sign system traits to ε-clamped trace vector.

    Returns (c, w, labels) where c ∈ [ε, 1-ε]^8 and w sums to 1.
    Equal weights across all 8 channels — no a priori privileging
    of any semiotic dimension.
    """
    c = ss.trace_vector()
    w = np.ones(N_SEMIOTIC_CHANNELS, dtype=np.float64) / N_SEMIOTIC_CHANNELS
    return c, w, list(SEMIOTIC_CHANNELS)


# ═════════════════════════════════════════════════════════════════════
# SECTION 6: REGIME & CLASSIFICATION
# ═════════════════════════════════════════════════════════════════════


def _classify_regime(omega: float, F: float, S: float, C: float) -> str:
    """Standard four-gate regime classification (from frozen_contract).

    Stable:   ω < 0.038  AND  F > 0.90  AND  S < 0.15  AND  C < 0.14
    Watch:    intermediate
    Collapse: ω ≥ 0.30
    """
    if omega >= 0.30:
        return "Collapse"
    if omega < 0.038 and F > 0.90 and S < 0.15 and C < 0.14:
        return "Stable"
    return "Watch"


def _classify_semiotic_type(F: float, IC: float, delta: float, C: float, ss: SignSystem) -> str:
    """Domain-specific semiotic type classification.

    Maps kernel invariants to semiotic interpretation.
    Order matters — checks proceed from most specific to most general:
    1. Dead/extinct → Gestus (no living community completes return)
    2. Animal Communication → Biological Signal (genetically encoded)
    3. High indexical + low recursion → Fixed Signal (pointing, road signs)
    4. High stability + high fidelity + low recursion → Stable Formal
    5. High recursion + high depth → Alive Recursive
    6. High delta → Heterogeneous (Fragile)
    7. Default → Mixed Semiotic
    """
    # Dead/extinct systems — no living interpretive community
    if ss.status in ("dead", "extinct"):
        return "Gestus (Dead System)"

    # Animal communication: genetically encoded signals
    if ss.category == "Animal Communication":
        return "Biological Signal"

    # High indexical coupling with low recursion = fixed signal
    if ss.indexical_coupling > 0.70 and ss.symbolic_recursion < 0.15:
        return "Fixed Signal"

    # Formal systems: high ground stability + high translation fidelity
    # but NOT high symbolic recursion (that's alive recursive)
    if ss.ground_stability > 0.85 and ss.translation_fidelity > 0.80 and ss.symbolic_recursion < 0.70:
        return "Stable Formal"

    # High recursion + high interpretant depth = alive recursive
    if ss.symbolic_recursion > 0.70 and ss.interpretant_depth > 0.70:
        if delta < 0.20:
            return "Alive Recursive (Balanced)"
        return "Alive Recursive (Fragile)"

    # High heterogeneity gap = fragile semiotic system
    if delta > 0.25:
        return "Heterogeneous (Fragile)"

    return "Mixed Semiotic"


# ═════════════════════════════════════════════════════════════════════
# SECTION 7: KERNEL COMPUTATION
# ═════════════════════════════════════════════════════════════════════


def compute_semiotic_kernel(ss: SignSystem) -> SemioticKernelResult:
    """Compute full GCD kernel for a single sign system.

    Maps sign system → 8-channel trace → Tier-1 invariants.
    Verifies all three structural identities: F+ω=1, IC≤F, IC≈exp(κ).
    """
    # Step 1: Normalize to trace vector
    c, w, labels = normalize_sign_system(ss)

    # Step 2: Call the immutable kernel
    k = compute_kernel_outputs(c, w, EPSILON)

    # Step 3: Extract Tier-1 invariants
    F = float(k["F"])
    omega = float(k["omega"])
    S = float(k["S"])
    C = float(k["C"])
    kappa = float(k["kappa"])
    IC = float(k["IC"])
    delta = float(k["heterogeneity_gap"])

    # Step 4: Verify Tier-1 identities
    F_plus_omega = F + omega
    IC_leq_F = IC <= F + 1e-12
    IC_eq_exp_kappa = abs(IC - math.exp(kappa)) < 1e-9

    # Step 5: Domain-specific classification
    regime = _classify_regime(omega, F, S, C)
    semiotic_type = _classify_semiotic_type(F, IC, delta, C, ss)

    # Step 6: Channel analysis
    min_idx = int(np.argmin(c))
    max_idx = int(np.argmax(c))

    # Step 7: Sensitivity analysis (IC contribution per channel)
    sens: dict[str, float] = {}
    for i, lab in enumerate(labels):
        ci = max(float(c[i]), float(EPSILON))
        sens[lab] = float(IC / ci)

    # Step 8: Return result
    return SemioticKernelResult(
        name=ss.name,
        category=ss.category,
        medium=ss.medium,
        status=ss.status,
        n_channels=N_SEMIOTIC_CHANNELS,
        channel_labels=labels,
        trace_vector=c.tolist(),
        F=F,
        omega=omega,
        S=S,
        C=C,
        kappa=kappa,
        IC=IC,
        heterogeneity_gap=delta,
        F_plus_omega=F_plus_omega,
        IC_leq_F=IC_leq_F,
        IC_eq_exp_kappa=IC_eq_exp_kappa,
        regime=regime,
        semiotic_type=semiotic_type,
        weakest_channel=labels[min_idx],
        weakest_value=float(c[min_idx]),
        strongest_channel=labels[max_idx],
        strongest_value=float(c[max_idx]),
        channel_sensitivities=sens,
    )


def compute_all_sign_systems() -> list[SemioticKernelResult]:
    """Compute kernel for all 30 sign systems."""
    return [compute_semiotic_kernel(ss) for ss in SIGN_SYSTEMS]


# ═════════════════════════════════════════════════════════════════════
# SECTION 8: CROSS-DOMAIN ANALYSIS
# ═════════════════════════════════════════════════════════════════════


@dataclass(frozen=True, slots=True)
class SemioticStructuralAnalysis:
    """Structural analysis of semiotic patterns across all sign systems.

    Reveals which channels drive semiotic coherence and fragility,
    and how the landscape of sign systems maps to the Bernoulli manifold.
    """

    n_systems: int
    mean_F: float
    mean_IC: float
    mean_delta: float
    mean_IC_F_ratio: float

    # Category means
    category_means: dict[str, dict[str, float]]

    # Channel rankings (which channels most/least contribute to IC)
    channel_mean_values: dict[str, float]
    ic_killer_channel: str  # Channel with lowest mean value
    ic_anchor_channel: str  # Channel with highest mean value

    # Regime distribution
    n_stable: int
    n_watch: int
    n_collapse: int

    # Living vs dead
    mean_F_living: float
    mean_F_dead: float
    mean_IC_living: float
    mean_IC_dead: float


def analyze_semiotic_structure() -> SemioticStructuralAnalysis:
    """Compute structural analysis across all sign systems.

    Identifies which channels drive semiotic coherence, which
    categories of sign systems are most robust, and where the
    landscape of meaning maps to the Bernoulli manifold.
    """
    results = compute_all_sign_systems()
    n = len(results)

    # Global means
    mean_F = sum(r.F for r in results) / n
    mean_IC = sum(r.IC for r in results) / n
    mean_delta = sum(r.heterogeneity_gap for r in results) / n
    mean_ratio = sum(r.IC / r.F if r.F > 0 else 0.0 for r in results) / n

    # Category-level analysis
    categories: dict[str, list[SemioticKernelResult]] = {}
    for r in results:
        categories.setdefault(r.category, []).append(r)

    category_means: dict[str, dict[str, float]] = {}
    for cat, cat_results in sorted(categories.items()):
        cn = len(cat_results)
        category_means[cat] = {
            "n": float(cn),
            "mean_F": sum(r.F for r in cat_results) / cn,
            "mean_IC": sum(r.IC for r in cat_results) / cn,
            "mean_delta": sum(r.heterogeneity_gap for r in cat_results) / cn,
        }

    # Channel-level means (which channels are globally strongest/weakest)
    channel_sums: dict[str, float] = dict.fromkeys(SEMIOTIC_CHANNELS, 0.0)
    for r in results:
        for i, ch in enumerate(SEMIOTIC_CHANNELS):
            channel_sums[ch] += r.trace_vector[i]

    channel_means = {ch: v / n for ch, v in channel_sums.items()}
    ic_killer = min(channel_means, key=channel_means.get)  # type: ignore[arg-type]
    ic_anchor = max(channel_means, key=channel_means.get)  # type: ignore[arg-type]

    # Regime distribution
    n_stable = sum(1 for r in results if r.regime == "Stable")
    n_watch = sum(1 for r in results if r.regime == "Watch")
    n_collapse = sum(1 for r in results if r.regime == "Collapse")

    # Living vs dead/extinct
    living = [r for r in results if r.status == "living"]
    dead = [r for r in results if r.status in ("dead", "extinct")]

    mean_F_living = sum(r.F for r in living) / len(living) if living else 0.0
    mean_F_dead = sum(r.F for r in dead) / len(dead) if dead else 0.0
    mean_IC_living = sum(r.IC for r in living) / len(living) if living else 0.0
    mean_IC_dead = sum(r.IC for r in dead) / len(dead) if dead else 0.0

    return SemioticStructuralAnalysis(
        n_systems=n,
        mean_F=mean_F,
        mean_IC=mean_IC,
        mean_delta=mean_delta,
        mean_IC_F_ratio=mean_ratio,
        category_means=category_means,
        channel_mean_values=channel_means,
        ic_killer_channel=ic_killer,
        ic_anchor_channel=ic_anchor,
        n_stable=n_stable,
        n_watch=n_watch,
        n_collapse=n_collapse,
        mean_F_living=mean_F_living,
        mean_F_dead=mean_F_dead,
        mean_IC_living=mean_IC_living,
        mean_IC_dead=mean_IC_dead,
    )


# ═════════════════════════════════════════════════════════════════════
# SECTION 9: BRAIN KERNEL BRIDGE
# ═════════════════════════════════════════════════════════════════════


def bridge_to_brain_kernel() -> dict[str, Any]:
    """Connect semiotic kernel to brain kernel channel 8.

    The brain kernel's language_architecture channel (channel 8) is scored
    0.98 for Homo sapiens — nearly maximal. This function computes the
    cross-kernel bridge: how does the 8-dimensional semiotic profile of
    "Modern English" (the sign system enabled by that 0.98) map to
    the single-channel reading in brain_kernel?

    Returns a dictionary with the bridge analysis.
    """
    # Find Modern English in our catalog
    english = next(ss for ss in SIGN_SYSTEMS if ss.name == "Modern English")
    english_result = compute_semiotic_kernel(english)

    # The bridge: brain_kernel channel 8 = 0.98
    # This single value is "unpacked" by our 8 channels
    brain_language_score = 0.98

    # Human semiotic profile IS what language_architecture = 0.98 means
    return {
        "brain_kernel_channel_8": brain_language_score,
        "semiotic_F": english_result.F,
        "semiotic_IC": english_result.IC,
        "semiotic_delta": english_result.heterogeneity_gap,
        "semiotic_regime": english_result.regime,
        "semiotic_type": english_result.semiotic_type,
        "weakest_channel": english_result.weakest_channel,
        "strongest_channel": english_result.strongest_channel,
        "interpretation": (
            f"brain_kernel scores language_architecture = {brain_language_score}. "
            f"The semiotic kernel unpacks this into 8 channels: "
            f"F = {english_result.F:.3f}, IC = {english_result.IC:.3f}, "
            f"Δ = {english_result.heterogeneity_gap:.3f}. "
            f"The weakest channel ({english_result.weakest_channel} = "
            f"{english_result.weakest_value:.3f}) explains why high "
            f"language_architecture coexists with semiotic fragility."
        ),
    }


# ═════════════════════════════════════════════════════════════════════
# SECTION 10: VALIDATION
# ═════════════════════════════════════════════════════════════════════


def validate_semiotic_kernel() -> dict[str, Any]:
    """Run full Tier-1 validation sweep across all sign systems.

    Checks:
      - F + ω = 1 (duality identity)
      - IC ≤ F (integrity bound)
      - IC = exp(κ) (log-integrity relation)

    Returns summary with pass/fail counts and any violations.
    """
    results = compute_all_sign_systems()
    n = len(results)

    duality_pass = 0
    bound_pass = 0
    log_pass = 0
    violations: list[str] = []

    for r in results:
        # Duality identity
        if abs(r.F_plus_omega - 1.0) < 1e-12:
            duality_pass += 1
        else:
            violations.append(f"{r.name}: F+ω = {r.F_plus_omega}")

        # Integrity bound
        if r.IC_leq_F:
            bound_pass += 1
        else:
            violations.append(f"{r.name}: IC={r.IC} > F={r.F}")

        # Log-integrity
        if r.IC_eq_exp_kappa:
            log_pass += 1
        else:
            exp_k = math.exp(r.kappa) if r.kappa > -30 else 0.0
            violations.append(f"{r.name}: IC={r.IC} vs exp(κ)={exp_k}")

    total_checks = n * 3
    total_pass = duality_pass + bound_pass + log_pass

    return {
        "n_systems": n,
        "total_checks": total_checks,
        "total_pass": total_pass,
        "total_fail": total_checks - total_pass,
        "duality_pass": duality_pass,
        "bound_pass": bound_pass,
        "log_pass": log_pass,
        "violations": violations,
        "verdict": "CONFORMANT" if total_pass == total_checks else "NONCONFORMANT",
    }
