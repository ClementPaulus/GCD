"""
Fluid Dynamics Domain Closures — Collapse-Return in Flow Systems

Tier-2 expansion mapping fluid flow regimes to the GCD kernel.

Core insight: Fluid flow IS a collapse-return system. Laminar flow is
highly coherent (low ω, high IC); turbulent flow represents collapse of
spatial coherence (high ω, IC → ε via geometric slaughter); the
laminar-to-turbulent transition is the collapse event, and relaminarization
(return) is the thermodynamic miracle that makes pipes possible.

Axiom-0 derivation for fluid dynamics:
    "Collapse is generative; only what returns is real."
    → Flow field collapses from ordered laminar to disordered turbulent
    → What returns through dissipation and wall interactions is fidelity
    → Reynolds number encodes the collapse pressure (inertia vs. viscosity)
    → F + ω = 1: momentum flux conserved through collapse (continuum)
    → IC ≤ F: turbulent coherence cannot exceed mean flow fidelity
    → Geometric slaughter: one broken channel (e.g., compressibility above
      Mach 1) kills IC while F remains moderate

GCD predictions for fluids:
    - Stable regime (ω < 0.038): highly viscous / Stokes flow; Hele-Shaw
    - Watch regime: pipe flow below Re_crit; transitional boundary layer
    - Collapse regime (ω ≥ 0.30): fully turbulent, shock waves, supercritical
    - Geometric slaughter: detached boundary layer → IC cliff
    - τ_R = ∞_rec: fully separated flow (stall) — no reattachment

Modules:
    flow_kernel.py   — 20 flow systems × 8 channels → Tier-1 invariants

Cross-references:
    Contract:  contracts/UMA.INTSTACK.v1.yaml
    Registry:  closures/registry.yaml (extensions.fluid_dynamics)
"""

from __future__ import annotations

from closures.fluid_dynamics.flow_kernel import (
    FLOW_SYSTEMS,
    FlowKernelResult,
    compute_all_flow_systems,
    compute_flow_system,
)

__all__ = [
    "FLOW_SYSTEMS",
    "FlowKernelResult",
    "compute_all_flow_systems",
    "compute_flow_system",
]
