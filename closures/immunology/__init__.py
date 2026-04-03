"""Immunology closure domain — Tier-2 expansion.

Six sub-closures spanning the immune system and its neural interfaces:
  - immune_cell_kernel       : 16 immune cell populations, 8 channels, 6 theorems
  - cytokine_network         : 12 cytokine mediators, 8 channels, 6 theorems
  - vaccine_response         : 12 vaccine platform entities, 8 channels, 6 theorems
  - autoimmune_kernel        : 12 autoimmune diseases, 8 channels, 6 theorems
  - neuroimmune_bridge       : 12 neuroimmune interface states, 8 channels, 6 theorems
  - psychoneuroimmunology    : 12 PNI paradigms, 8 channels, 6 theorems

Total: 76 entities, 36 theorems (T-IC, T-CY, T-VR, T-AI, T-NI, T-PNI prefixes).
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
from closures.immunology.neuroimmune_bridge import (
    NI_ENTITIES,
)
from closures.immunology.neuroimmune_bridge import (
    compute_all_entities as compute_all_ni_entities,
)
from closures.immunology.neuroimmune_bridge import (
    verify_all_theorems as verify_all_ni_theorems,
)
from closures.immunology.psychoneuroimmunology import (
    PNI_ENTITIES,
)
from closures.immunology.psychoneuroimmunology import (
    compute_all_entities as compute_all_pni_entities,
)
from closures.immunology.psychoneuroimmunology import (
    verify_all_theorems as verify_all_pni_theorems,
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
    "NI_ENTITIES",
    "PNI_ENTITIES",
    "VR_ENTITIES",
    "compute_all_ai_entities",
    "compute_all_cy_entities",
    "compute_all_ic_entities",
    "compute_all_ni_entities",
    "compute_all_pni_entities",
    "compute_all_vr_entities",
    "verify_all_ai_theorems",
    "verify_all_cy_theorems",
    "verify_all_ic_theorems",
    "verify_all_ni_theorems",
    "verify_all_pni_theorems",
    "verify_all_vr_theorems",
]
