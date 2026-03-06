"""
Semiotics Domain Closures — Collapse-Return Dynamics of Sign Systems

Tier-2 expansion mapping semiotic phenomena to the GCD kernel.

Core insight: Semiosis IS recursive collapse-return. A sign collapses the
undifferentiated field of potential meaning into a specific interpretant.
Only the interpretant that returns through re-use, convention, and shared
practice is real (*solum quod redit, reale est*). Failed signs — gestures
whose meaning does not survive transmission — have τ_R = ∞_rec.

Axiom-0 derivation for semiotics:
    "Collapse is generative; only what returns is real."
    → Signification collapses meaning space into a sign-interpretant pair
    → What the receiver reconstructs (returns) is the interpretant
    → Fidelity (F) measures how much of the original meaning survives
    → Drift (ω) measures semiotic loss — noise, ambiguity, cultural gap
    → IC ≤ F: composite sign coherence cannot exceed mean channel fidelity
    → Geometric slaughter: ONE broken channel (e.g., absent context) kills IC

GCD predictions for semiotics:
    - Iconic signs (resemblance): high syntactic + semantic fidelity, low ω
    - Indexical signs (causal link): moderate F, high pragmatic coherence
    - Symbolic signs (arbitrary convention): low IC unless convention is shared
    - Dead metaphors: τ_R = ∞_rec — the sign no longer generates interpretants
    - Polysemy: high S (Bernoulli field entropy), high C (curvature)
    - Pidgin/creole formation: collapse → return arc visible in F trajectory

Modules:
    sign_kernel.py   — 20 sign systems × 8 channels → Tier-1 invariants

Cross-references:
    Contract:  contracts/UMA.INTSTACK.v1.yaml
    Registry:  closures/registry.yaml (extensions.semiotics)
"""

from __future__ import annotations

from closures.semiotics.sign_kernel import (
    SIGN_SYSTEMS,
    SignKernelResult,
    compute_all_sign_systems,
    compute_sign_system,
)

__all__ = [
    "SIGN_SYSTEMS",
    "SignKernelResult",
    "compute_all_sign_systems",
    "compute_sign_system",
]
