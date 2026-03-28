"""Nuclear Physics Closures — NUC.INTSTACK.v1

Provides closures for nuclear binding, decay dynamics, shell structure,
fissility assessment, decay chains, the double-sided collapse overlay,
and the RHIC quark-gluon plasma (QGP) kernel analysis.

Cross-references:
  Contract:  contracts/NUC.INTSTACK.v1.yaml
  Canon:     canon/nuc_anchors.yaml
  Registry:  closures/registry.yaml (extensions.nuclear_physics)
"""

from __future__ import annotations

from closures.nuclear_physics.alpha_decay import compute_alpha_decay
from closures.nuclear_physics.cosmic_ray_airshower import (
    AS_ENTITIES,
)
from closures.nuclear_physics.cosmic_ray_airshower import (
    compute_all_entities as compute_all_as_entities,
)
from closures.nuclear_physics.cosmic_ray_airshower import (
    verify_all_theorems as verify_all_as_theorems,
)
from closures.nuclear_physics.cosmic_ray_propagation import (
    CR_ENTITIES,
)
from closures.nuclear_physics.cosmic_ray_propagation import (
    compute_all_entities as compute_all_cr_entities,
)
from closures.nuclear_physics.cosmic_ray_propagation import (
    verify_all_theorems as verify_all_cr_theorems,
)
from closures.nuclear_physics.decay_chain import compute_decay_chain
from closures.nuclear_physics.double_sided_collapse import compute_double_sided
from closures.nuclear_physics.fissility import compute_fissility
from closures.nuclear_physics.nuclide_binding import compute_binding
from closures.nuclear_physics.qgp_rhic import run_full_analysis as compute_qgp_rhic
from closures.nuclear_physics.reaction_channels import (
    RC_ENTITIES,
)
from closures.nuclear_physics.reaction_channels import (
    compute_all_entities as compute_all_rc_entities,
)
from closures.nuclear_physics.reaction_channels import (
    verify_all_theorems as verify_all_rc_theorems,
)
from closures.nuclear_physics.shell_structure import compute_shell

__all__ = [
    "AS_ENTITIES",
    "CR_ENTITIES",
    "RC_ENTITIES",
    "compute_all_as_entities",
    "compute_all_cr_entities",
    "compute_all_rc_entities",
    "compute_alpha_decay",
    "compute_binding",
    "compute_decay_chain",
    "compute_double_sided",
    "compute_fissility",
    "compute_qgp_rhic",
    "compute_shell",
    "verify_all_as_theorems",
    "verify_all_cr_theorems",
    "verify_all_rc_theorems",
]
