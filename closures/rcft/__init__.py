"""RCFT Closures — RCFT.INTSTACK.v1

Recursive Collapse Field Theory extensions providing Tier-2 overlays
for fractal dimension, recursive fields, attractor basins, resonance
patterns, information geometry, universality classification, collapse
grammar, regime derivation, equator convergence, and epistemic agents.

Cross-references:
    Contract:  contracts/RCFT.INTSTACK.v1.yaml
    Canon:     canon/rcft_anchors.yaml
    Registry:  closures/registry.yaml (extensions.rcft)
"""

from __future__ import annotations

from closures.rcft.attractor_basin import compute_attractor_basin
from closures.rcft.coherence_pipeline_closure import (
    CoherenceDerivation,
    derive_coherence,
    verify_coherence_is_derived,
)
from closures.rcft.collapse_field_theory import (
    CFT_ENTITIES,
    CollapseFieldEntity,
    compute_cft_kernel,
)
from closures.rcft.collapse_field_theory import (
    compute_all_entities as compute_all_cft_entities,
)
from closures.rcft.collapse_field_theory import (
    verify_all_theorems as verify_all_cft_theorems,
)
from closures.rcft.collapse_grammar import diagnose_grammar
from closures.rcft.epistemic_agents import (
    EA_ENTITIES,
    EAKernelResult,
    EpistemicAgentEntity,
    compute_ea_kernel,
)
from closures.rcft.epistemic_agents import (
    compute_all_entities as compute_all_ea_entities,
)
from closures.rcft.epistemic_agents import (
    verify_all_theorems as verify_all_ea_theorems,
)
from closures.rcft.equator_convergence import (
    EQ_ENTITIES,
    EQKernelResult,
    EquatorConvergenceEntity,
    compute_eq_kernel,
)
from closures.rcft.equator_convergence import (
    compute_all_entities as compute_all_eq_entities,
)
from closures.rcft.equator_convergence import (
    verify_all_theorems as verify_all_eq_theorems,
)
from closures.rcft.fractal_dimension import compute_fractal_dimension
from closures.rcft.information_geometry import (
    compute_efficiency,
    compute_geodesic_budget_cost,
    fisher_distance_1d,
    fisher_distance_weighted,
    fisher_geodesic,
    verify_fano_fisher_duality,
)
from closures.rcft.recursive_field import compute_recursive_field
from closures.rcft.regime_derivation import (
    RD_ENTITIES,
    RDKernelResult,
    RegimeDerivationEntity,
    compute_rd_kernel,
)
from closures.rcft.regime_derivation import (
    compute_all_entities as compute_all_rd_entities,
)
from closures.rcft.regime_derivation import (
    verify_all_theorems as verify_all_rd_theorems,
)
from closures.rcft.resonance_pattern import compute_resonance_pattern
from closures.rcft.scale_recursion import (
    SR_ENTITIES,
    ScaleRecursionEntity,
    compute_sr_kernel,
)
from closures.rcft.scale_recursion import (
    compute_all_entities as compute_all_sr_entities,
)
from closures.rcft.scale_recursion import (
    verify_all_theorems as verify_all_sr_theorems,
)
from closures.rcft.universality_class import (
    compute_central_charge,
    compute_critical_exponents,
    compute_partition_function,
    verify_scaling_relations,
)

__all__ = [
    "CFT_ENTITIES",
    "EA_ENTITIES",
    "EQ_ENTITIES",
    "RD_ENTITIES",
    "SR_ENTITIES",
    "CoherenceDerivation",
    "CollapseFieldEntity",
    "EAKernelResult",
    "EQKernelResult",
    "EpistemicAgentEntity",
    "EquatorConvergenceEntity",
    "RDKernelResult",
    "RegimeDerivationEntity",
    "ScaleRecursionEntity",
    "compute_all_cft_entities",
    "compute_all_ea_entities",
    "compute_all_eq_entities",
    "compute_all_rd_entities",
    "compute_all_sr_entities",
    "compute_attractor_basin",
    "compute_central_charge",
    "compute_cft_kernel",
    "compute_critical_exponents",
    "compute_ea_kernel",
    "compute_efficiency",
    "compute_eq_kernel",
    "compute_fractal_dimension",
    "compute_geodesic_budget_cost",
    "compute_partition_function",
    "compute_rd_kernel",
    "compute_recursive_field",
    "compute_resonance_pattern",
    "compute_sr_kernel",
    "derive_coherence",
    "diagnose_grammar",
    "fisher_distance_1d",
    "fisher_distance_weighted",
    "fisher_geodesic",
    "verify_all_cft_theorems",
    "verify_all_ea_theorems",
    "verify_all_eq_theorems",
    "verify_all_rd_theorems",
    "verify_all_sr_theorems",
    "verify_coherence_is_derived",
    "verify_fano_fisher_duality",
    "verify_scaling_relations",
]
