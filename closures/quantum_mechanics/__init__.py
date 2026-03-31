"""Quantum Mechanics closures for UMCP — QM.INTSTACK.v1.

Seven closures mapping quantum observables to UMCP Tier-1 invariants:
  1. wavefunction_collapse — Born rule, state fidelity, purity
  2. entanglement — concurrence, Bell parameter, von Neumann entropy
  3. tunneling — barrier transmission, decay constant
  4. harmonic_oscillator — energy quantization, coherent states
  5. spin_measurement — Stern-Gerlach, Zeeman, Larmor
  6. uncertainty_principle — Heisenberg bounds
  7. fqhe_bilayer_graphene — FQHE AB interference, Kim et al. Nature 2026
  8. photonic_confinement — CPM photonic confinement, Caputo 2026
  9. indefinite_causal_order — VBC inequality, Richter et al. PRX Quantum 2026

Cross-references:
    Contract:  contracts/QM.INTSTACK.v1.yaml
    Canon:     canon/qm_anchors.yaml
    Registry:  closures/registry.yaml (extensions.quantum_mechanics)
"""

from __future__ import annotations

from closures.quantum_mechanics.entanglement import compute_entanglement
from closures.quantum_mechanics.fqhe_bilayer_graphene import compute_all_states as compute_fqhe_states
from closures.quantum_mechanics.harmonic_oscillator import compute_harmonic_oscillator
from closures.quantum_mechanics.indefinite_causal_order import (
    ICO_ENTITIES,
    run_all_ico_theorems,
)
from closures.quantum_mechanics.indefinite_causal_order import (
    compute_all_entities as compute_all_ico_entities,
)
from closures.quantum_mechanics.photonic_confinement import compute_all_entities as compute_cpm_entities
from closures.quantum_mechanics.spin_measurement import compute_spin_measurement
from closures.quantum_mechanics.spliceosome_dynamics import SD_ENTITIES
from closures.quantum_mechanics.spliceosome_dynamics import (
    compute_all_entities as compute_all_sd_entities,
)
from closures.quantum_mechanics.spliceosome_dynamics import (
    verify_all_theorems as verify_all_sd_theorems,
)
from closures.quantum_mechanics.topological_band_structures import (
    TB_ENTITIES,
)
from closures.quantum_mechanics.topological_band_structures import (
    compute_all_entities as compute_all_tb_entities,
)
from closures.quantum_mechanics.topological_band_structures import (
    verify_all_theorems as verify_all_tb_theorems,
)
from closures.quantum_mechanics.tunneling import compute_tunneling
from closures.quantum_mechanics.uncertainty_principle import compute_uncertainty
from closures.quantum_mechanics.wavefunction_collapse import compute_wavefunction_collapse

__all__ = [
    "ICO_ENTITIES",
    "SD_ENTITIES",
    "TB_ENTITIES",
    "compute_all_ico_entities",
    "compute_all_sd_entities",
    "compute_all_tb_entities",
    "compute_cpm_entities",
    "compute_entanglement",
    "compute_fqhe_states",
    "compute_harmonic_oscillator",
    "compute_spin_measurement",
    "compute_tunneling",
    "compute_uncertainty",
    "compute_wavefunction_collapse",
    "run_all_ico_theorems",
    "verify_all_sd_theorems",
    "verify_all_tb_theorems",
]
