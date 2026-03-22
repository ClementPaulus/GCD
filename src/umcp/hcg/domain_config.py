"""
Domain Configuration — Routes TARGET_DOMAIN to the correct closure subset.

Each domain gets a DomainConfig specifying its anchor file prefix, contract
pattern, color scheme, and Rosetta lens defaults.  The builder uses this to
construct hermetic, fully-themed sites per domain.

Usage:
    export TARGET_DOMAIN=astronomy
    python -m umcp.hcg.builder   # builds only the astronomy site
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field


@dataclass(frozen=True)
class DomainConfig:
    """Configuration for one autonomous domain site."""

    # Identity
    slug: str  # e.g. "astronomy"
    display_name: str  # e.g. "Astronomy"
    tagline: str  # one-line description
    anchor_prefix: str  # prefix in canon/ (e.g. "astro")

    # Visual
    primary_color: str = "#2563eb"  # Tailwind blue-600 default
    accent_color: str = "#7c3aed"  # Tailwind violet-600 default
    icon: str = "telescope"  # Lucide icon name

    # Rosetta
    default_lens: str = "Ontology"  # Default Rosetta lens for this domain

    # Content
    hero_title: str = ""  # Override for homepage hero
    hero_subtitle: str = ""  # Override for homepage subtitle

    # Deployment
    base_url: str = ""  # e.g. "https://astronomy.gcd-kernel.org"
    deploy_target: str = "github-pages"  # github-pages | vercel | netlify

    # Filtering
    contract_patterns: list[str] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Domain registry — all 20 domains + GCD root
# ---------------------------------------------------------------------------

_DOMAINS: dict[str, DomainConfig] = {
    "gcd": DomainConfig(
        slug="gcd",
        display_name="Generative Collapse Dynamics",
        tagline="The axiom. The kernel. The spine.",
        anchor_prefix="gcd",
        primary_color="#0f172a",
        accent_color="#f59e0b",
        icon="atom",
        default_lens="Epistemology",
        hero_title="Collapse is Generative",
        hero_subtitle="Only what returns is real.",
    ),
    "rcft": DomainConfig(
        slug="rcft",
        display_name="Recursive Collapse Field Theory",
        tagline="Fractal recursion through the kernel.",
        anchor_prefix="rcft",
        primary_color="#7c3aed",
        accent_color="#a78bfa",
        icon="layers",
        default_lens="Ontology",
    ),
    "kinematics": DomainConfig(
        slug="kinematics",
        display_name="Kinematics",
        tagline="Motion analysis through collapse invariants.",
        anchor_prefix="kin",
        primary_color="#0891b2",
        accent_color="#22d3ee",
        icon="move",
        default_lens="Ontology",
    ),
    "weyl": DomainConfig(
        slug="weyl",
        display_name="WEYL Cosmology",
        tagline="Modified gravity through the integrity bound.",
        anchor_prefix="weyl",
        primary_color="#1e3a5f",
        accent_color="#60a5fa",
        icon="globe",
        default_lens="Ontology",
    ),
    "security": DomainConfig(
        slug="security",
        display_name="Security & Audit",
        tagline="Input validation and cryptographic integrity.",
        anchor_prefix="sec",
        primary_color="#dc2626",
        accent_color="#f87171",
        icon="shield",
        default_lens="Policy",
    ),
    "astronomy": DomainConfig(
        slug="astronomy",
        display_name="Astronomy",
        tagline="Stellar classification through the kernel.",
        anchor_prefix="astro",
        primary_color="#1e1b4b",
        accent_color="#818cf8",
        icon="telescope",
        default_lens="Ontology",
    ),
    "nuclear_physics": DomainConfig(
        slug="nuclear_physics",
        display_name="Nuclear Physics",
        tagline="Binding energy, decay chains, QGP transitions.",
        anchor_prefix="nuc",
        primary_color="#b91c1c",
        accent_color="#fca5a5",
        icon="zap",
        default_lens="Ontology",
    ),
    "quantum_mechanics": DomainConfig(
        slug="quantum_mechanics",
        display_name="Quantum Mechanics",
        tagline="Wavefunction coherence and entanglement.",
        anchor_prefix="qm",
        primary_color="#4338ca",
        accent_color="#a78bfa",
        icon="activity",
        default_lens="Ontology",
    ),
    "finance": DomainConfig(
        slug="finance",
        display_name="Finance",
        tagline="Portfolio continuity and market coherence.",
        anchor_prefix="finance",
        primary_color="#065f46",
        accent_color="#34d399",
        icon="trending-up",
        default_lens="Policy",
    ),
    "atomic_physics": DomainConfig(
        slug="atomic_physics",
        display_name="Atomic Physics",
        tagline="118 elements through the periodic kernel.",
        anchor_prefix="atom",
        primary_color="#92400e",
        accent_color="#fbbf24",
        icon="atom",
        default_lens="Ontology",
    ),
    "materials_science": DomainConfig(
        slug="materials_science",
        display_name="Materials Science",
        tagline="Element database and material coherence.",
        anchor_prefix="matl",
        primary_color="#78350f",
        accent_color="#d97706",
        icon="box",
        default_lens="Ontology",
    ),
    "everyday_physics": DomainConfig(
        slug="everyday_physics",
        display_name="Everyday Physics",
        tagline="Thermodynamics, optics, fluids through collapse.",
        anchor_prefix="evday",
        primary_color="#0e7490",
        accent_color="#67e8f9",
        icon="sun",
        default_lens="Phenomenology",
    ),
    "evolution": DomainConfig(
        slug="evolution",
        display_name="Evolution & Neuroscience",
        tagline="40 organisms, 10-channel brain kernel.",
        anchor_prefix="evo",
        primary_color="#166534",
        accent_color="#86efac",
        icon="dna",
        default_lens="Ontology",
    ),
    "dynamic_semiotics": DomainConfig(
        slug="dynamic_semiotics",
        display_name="Dynamic Semiotics",
        tagline="30 sign systems through the semiotic kernel.",
        anchor_prefix="semiotics",
        primary_color="#831843",
        accent_color="#f9a8d4",
        icon="message-circle",
        default_lens="Semiotics",
    ),
    "consciousness_coherence": DomainConfig(
        slug="consciousness_coherence",
        display_name="Consciousness Coherence",
        tagline="20 systems, coherence kernel, 7 theorems.",
        anchor_prefix="cons",
        primary_color="#581c87",
        accent_color="#c084fc",
        icon="brain",
        default_lens="Phenomenology",
    ),
    "continuity_theory": DomainConfig(
        slug="continuity_theory",
        display_name="Continuity Theory",
        tagline="Topological persistence and organizational resilience.",
        anchor_prefix="ct",
        primary_color="#0c4a6e",
        accent_color="#38bdf8",
        icon="link",
        default_lens="History",
    ),
    "awareness_cognition": DomainConfig(
        slug="awareness_cognition",
        display_name="Awareness & Cognition",
        tagline="Awareness-aptitude kernel across phylogeny.",
        anchor_prefix="awc",
        primary_color="#4c1d95",
        accent_color="#a78bfa",
        icon="eye",
        default_lens="Phenomenology",
    ),
    "standard_model": DomainConfig(
        slug="standard_model",
        display_name="Standard Model",
        tagline="31 particles, 27 theorems in the subatomic kernel.",
        anchor_prefix="sm",
        primary_color="#991b1b",
        accent_color="#fca5a5",
        icon="atom",
        default_lens="Ontology",
    ),
    "clinical_neuroscience": DomainConfig(
        slug="clinical_neuroscience",
        display_name="Clinical Neuroscience",
        tagline="10-channel cortical kernel and neurotransmitter systems.",
        anchor_prefix="clin",
        primary_color="#701a75",
        accent_color="#e879f9",
        icon="heart-pulse",
        default_lens="Phenomenology",
    ),
    "spacetime_memory": DomainConfig(
        slug="spacetime_memory",
        display_name="Spacetime Memory",
        tagline="Gravitational wave memory and temporal topology.",
        anchor_prefix="st",
        primary_color="#0f172a",
        accent_color="#94a3b8",
        icon="orbit",
        default_lens="Ontology",
    ),
}


def get_domain_config(domain: str | None = None) -> DomainConfig:
    """Return config for *domain*, falling back to TARGET_DOMAIN env var."""
    if domain is None:
        domain = os.environ.get("TARGET_DOMAIN", "gcd")
    domain = domain.lower().strip()
    if domain not in _DOMAINS:
        msg = f"Unknown domain: {domain!r}. Available: {sorted(_DOMAINS)}"
        raise ValueError(msg)
    return _DOMAINS[domain]


def list_domains() -> list[str]:
    """Return sorted list of registered domain slugs."""
    return sorted(_DOMAINS)
