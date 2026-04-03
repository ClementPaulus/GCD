"""Immunology closure domain — Tier-2 expansion.

Four sub-closures spanning the immune system:
  - immune_cell_kernel   : 16 immune cell populations, 8 channels, 6 theorems
  - cytokine_network     : 12 cytokine mediators, 8 channels, 6 theorems
  - vaccine_response     : 12 vaccine platform entities, 8 channels, 6 theorems
  - autoimmune_kernel    : 12 autoimmune diseases, 8 channels, 6 theorems

Total: 52 entities, 24 theorems (T-IC, T-CY, T-VR, T-AI prefixes).
"""

from closures.immunology.autoimmune_kernel import (
    AI_ENTITIES,
)
from closures.immunology.autoimmune_kernel import (
    compute_all_entities as compute_all_ai_entities,
)
from closures.immunology.autoimmune_kernel import (
    verify_all_theorems as verify_all_ai_theorems,
)
from closures.immunology.cytokine_network import (
    CY_ENTITIES,
)
from closures.immunology.cytokine_network import (
    compute_all_entities as compute_all_cy_entities,
)
from closures.immunology.cytokine_network import (
    verify_all_theorems as verify_all_cy_theorems,
)
from closures.immunology.immune_cell_kernel import (
    IC_ENTITIES,
)
from closures.immunology.immune_cell_kernel import (
    compute_all_entities as compute_all_ic_entities,
)
from closures.immunology.immune_cell_kernel import (
    verify_all_theorems as verify_all_ic_theorems,
)
from closures.immunology.vaccine_response import (
    VR_ENTITIES,
)
from closures.immunology.vaccine_response import (
    compute_all_entities as compute_all_vr_entities,
)
from closures.immunology.vaccine_response import (
    verify_all_theorems as verify_all_vr_theorems,
)

__all__ = [
    "AI_ENTITIES",
    "CY_ENTITIES",
    "IC_ENTITIES",
    "VR_ENTITIES",
    "compute_all_ai_entities",
    "compute_all_cy_entities",
    "compute_all_ic_entities",
    "compute_all_vr_entities",
    "verify_all_ai_theorems",
    "verify_all_cy_theorems",
    "verify_all_ic_theorems",
    "verify_all_vr_theorems",
]
