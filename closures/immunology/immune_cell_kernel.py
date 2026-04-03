"""Immune Cell Kernel — Immunology Domain (Tier-2 Closure).

Maps 16 immune cell populations through the GCD kernel.
Each cell type is characterized by 8 measurable functional channels
drawn from immunology literature.

Channels (8, equal weights w_i = 1/8):
  0  activation_threshold    — stringency of activation gate (0=hair-trigger, 1=very stringent)
  1  proliferation_capacity  — clonal expansion magnitude after activation
  2  cytokine_breadth        — diversity of cytokine production profile (normalized)
  3  self_tolerance          — discrimination capacity between self and non-self
  4  tissue_residence        — fraction of population residing in peripheral tissues
  5  effector_potency        — killing or clearance efficiency per cell
  6  memory_formation        — capacity to form long-lived immunological memory
  7  regulatory_capacity     — ability to suppress or modulate other immune cells

16 entities across 2 arms:
  Innate   (8): neutrophil, macrophage, dendritic_cell, NK_cell,
                mast_cell, basophil, eosinophil, monocyte
  Adaptive (8): CD4_Th1, CD4_Th2, CD4_Treg, CD8_CTL,
                B_cell_naive, B_cell_plasma, memory_B, memory_T

6 theorems (T-IC-1 through T-IC-6).

References:
  Janeway CA et al. (2001) Immunobiology, 5th ed. Garland.
  Murphy K, Weaver C (2016) Janeway's Immunobiology, 9th ed.
  Akira S, Uematsu S, Takeuchi O (2006) Cell 124:783-801.
  Sakaguchi S et al. (2008) Cell 133:775-787 (Treg biology).
  Masopust D et al. (2017) Nat Immunol 18:844-848 (memory T cells).
  Lavin Y et al. (2014) Cell 159:1312-1326 (tissue macrophages).
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

IC_CHANNELS = [
    "activation_threshold",
    "proliferation_capacity",
    "cytokine_breadth",
    "self_tolerance",
    "tissue_residence",
    "effector_potency",
    "memory_formation",
    "regulatory_capacity",
]
N_IC_CHANNELS = len(IC_CHANNELS)


@dataclass(frozen=True, slots=True)
class ImmuneCellEntity:
    """An immune cell population with 8 measurable functional channels."""

    name: str
    arm: str  # "innate" or "adaptive"
    activation_threshold: float
    proliferation_capacity: float
    cytokine_breadth: float
    self_tolerance: float
    tissue_residence: float
    effector_potency: float
    memory_formation: float
    regulatory_capacity: float

    def trace_vector(self) -> np.ndarray:
        return np.array(
            [
                self.activation_threshold,
                self.proliferation_capacity,
                self.cytokine_breadth,
                self.self_tolerance,
                self.tissue_residence,
                self.effector_potency,
                self.memory_formation,
                self.regulatory_capacity,
            ]
        )


# --- Entity catalog ---
# Channel values normalized to [0, 1] from primary immunology literature.
# activation_threshold: LOW = hair-trigger (innate), HIGH = stringent (adaptive)
# All other channels: HIGH = strong functionality
IC_ENTITIES: tuple[ImmuneCellEntity, ...] = (
    # ── Innate arm ──────────────────────────────────────────────────────────
    # Neutrophil: fastest responder, short-lived, no MHC-II, no memory
    ImmuneCellEntity("neutrophil", "innate", 0.15, 0.30, 0.40, 0.35, 0.60, 0.85, 0.05, 0.10),
    # Macrophage: M1/M2 plasticity, tissue sentinel, strong phagocyte
    ImmuneCellEntity("macrophage", "innate", 0.30, 0.25, 0.80, 0.50, 0.85, 0.70, 0.20, 0.35),
    # Dendritic cell: bridge innate/adaptive, prime T cells via MHC-I/II
    ImmuneCellEntity("dendritic_cell", "innate", 0.40, 0.20, 0.75, 0.65, 0.70, 0.45, 0.15, 0.55),
    # NK cell: innate killer, MHC-I-independent cytotoxicity, limited memory
    ImmuneCellEntity("NK_cell", "innate", 0.25, 0.45, 0.35, 0.40, 0.55, 0.90, 0.10, 0.15),
    # Mast cell: tissue-resident, IgE-armed, allergy and parasite defense
    ImmuneCellEntity("mast_cell", "innate", 0.20, 0.15, 0.60, 0.30, 0.95, 0.55, 0.08, 0.25),
    # Basophil: circulating equivalent of mast cell, rare but potent
    ImmuneCellEntity("basophil", "innate", 0.18, 0.12, 0.45, 0.25, 0.25, 0.50, 0.05, 0.20),
    # Eosinophil: anti-helminth effector, major tissue damage potential
    ImmuneCellEntity("eosinophil", "innate", 0.22, 0.18, 0.35, 0.28, 0.70, 0.65, 0.05, 0.15),
    # Monocyte: circulating precursor to macrophage and DC
    ImmuneCellEntity("monocyte", "innate", 0.35, 0.30, 0.65, 0.45, 0.30, 0.55, 0.12, 0.30),
    # ── Adaptive arm ────────────────────────────────────────────────────────
    # CD4 Th1: coordinates cell-mediated immunity (IFN-γ, IL-2, TNF-α)
    ImmuneCellEntity("CD4_Th1", "adaptive", 0.55, 0.80, 0.70, 0.70, 0.50, 0.60, 0.75, 0.30),
    # CD4 Th2: coordinates humoral / anti-helminth immunity (IL-4, IL-5, IL-13)
    ImmuneCellEntity("CD4_Th2", "adaptive", 0.60, 0.75, 0.65, 0.75, 0.45, 0.50, 0.70, 0.40),
    # CD4 Treg: master suppressors maintaining peripheral tolerance (FOXP3+)
    ImmuneCellEntity("CD4_Treg", "adaptive", 0.70, 0.55, 0.40, 0.95, 0.60, 0.20, 0.65, 0.95),
    # CD8 CTL: cytotoxic T lymphocyte — primary anti-viral and anti-tumour
    ImmuneCellEntity("CD8_CTL", "adaptive", 0.60, 0.85, 0.50, 0.72, 0.55, 0.92, 0.80, 0.15),
    # B cell (naive): antigen-inexperienced, isotype IgM/IgD
    ImmuneCellEntity("B_cell_naive", "adaptive", 0.65, 0.70, 0.30, 0.80, 0.35, 0.40, 0.55, 0.45),
    # Plasma cell: terminally differentiated Ab factory, minimal proliferation
    ImmuneCellEntity("B_cell_plasma", "adaptive", 0.85, 0.10, 0.15, 0.90, 0.80, 0.85, 0.20, 0.05),
    # Memory B cell: rapid recall, isotype-switched, long-lived in marrow niches
    ImmuneCellEntity("memory_B", "adaptive", 0.75, 0.80, 0.25, 0.85, 0.55, 0.55, 0.95, 0.25),
    # Memory T cell (Tcm/Tem): long-lived sentinels with rapid recall kinetics
    ImmuneCellEntity("memory_T", "adaptive", 0.68, 0.85, 0.55, 0.82, 0.65, 0.75, 0.90, 0.30),
)


@dataclass(frozen=True, slots=True)
class ICKernelResult:
    """GCD kernel output for an immune cell entity."""

    name: str
    arm: str
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
            "arm": self.arm,
            "F": self.F,
            "omega": self.omega,
            "S": self.S,
            "C": self.C,
            "kappa": self.kappa,
            "IC": self.IC,
            "regime": self.regime,
        }


def compute_ic_kernel(entity: ImmuneCellEntity) -> ICKernelResult:
    """Compute GCD kernel for an immune cell entity."""
    c = entity.trace_vector()
    c = np.clip(c, EPSILON, 1.0 - EPSILON)
    w = np.ones(N_IC_CHANNELS) / N_IC_CHANNELS
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
    return ICKernelResult(
        name=entity.name,
        arm=entity.arm,
        F=F,
        omega=omega,
        S=S,
        C=C_val,
        kappa=kappa,
        IC=IC,
        regime=regime,
    )


def compute_all_entities() -> list[ICKernelResult]:
    """Compute kernel outputs for all immune cell entities."""
    return [compute_ic_kernel(e) for e in IC_ENTITIES]


# ── Theorems ──────────────────────────────────────────────────────────────────


def verify_t_ic_1(results: list[ICKernelResult]) -> dict:
    """T-IC-1: Adaptive arm has strictly higher mean self_tolerance than innate.

    Adaptive lymphocytes undergo thymic/bone-marrow negative selection,
    installing a high-fidelity self/non-self discrimination mechanism.
    Innate cells use germline-encoded receptors with lower self-specificity.
    References: Hogquist & Jameson (2014) Nat Immunol 15:123-128.
    """
    innate_tol = np.mean([e.self_tolerance for e in IC_ENTITIES if e.arm == "innate"])
    adaptive_tol = np.mean([e.self_tolerance for e in IC_ENTITIES if e.arm == "adaptive"])
    passed = bool(adaptive_tol > innate_tol)
    return {
        "name": "T-IC-1",
        "passed": passed,
        "innate_mean_self_tolerance": float(innate_tol),
        "adaptive_mean_self_tolerance": float(adaptive_tol),
        "delta": float(adaptive_tol - innate_tol),
    }


def verify_t_ic_2(results: list[ICKernelResult]) -> dict:
    """T-IC-2: Adaptive arm has strictly higher mean memory_formation than innate.

    Adaptive lymphocytes generate antigen-specific memory upon activation;
    innate cells have minimal clonal memory (with the exception of NK-cell
    memory, a recent discovery that remains quantitatively minor).
    References: Sallusto F et al. (1999) Nature 401:708-712.
    """
    innate_mem = np.mean([e.memory_formation for e in IC_ENTITIES if e.arm == "innate"])
    adaptive_mem = np.mean([e.memory_formation for e in IC_ENTITIES if e.arm == "adaptive"])
    passed = bool(adaptive_mem > innate_mem)
    return {
        "name": "T-IC-2",
        "passed": passed,
        "innate_mean_memory": float(innate_mem),
        "adaptive_mean_memory": float(adaptive_mem),
        "fold_increase": float(adaptive_mem / max(innate_mem, EPSILON)),
    }


def verify_t_ic_3(results: list[ICKernelResult]) -> dict:
    """T-IC-3: CD4_Treg maximizes both regulatory_capacity and self_tolerance.

    Foxp3+ Tregs are the primary suppressors of adaptive autoimmunity.
    Their unique dual specialization (highest regulatory + highest tolerance)
    distinguishes them from all other lineages structurally.
    References: Sakaguchi S et al. (2008) Cell 133:775-787.
    """
    treg = next(e for e in IC_ENTITIES if e.name == "CD4_Treg")
    max_reg = max(e.regulatory_capacity for e in IC_ENTITIES)
    max_tol = max(e.self_tolerance for e in IC_ENTITIES)
    reg_match = abs(treg.regulatory_capacity - max_reg) < 0.01
    tol_match = abs(treg.self_tolerance - max_tol) < 0.01
    passed = bool(reg_match and tol_match)
    return {
        "name": "T-IC-3",
        "passed": passed,
        "treg_regulatory_capacity": treg.regulatory_capacity,
        "treg_self_tolerance": treg.self_tolerance,
        "max_regulatory_capacity": float(max_reg),
        "max_self_tolerance": float(max_tol),
    }


def verify_t_ic_4(results: list[ICKernelResult]) -> dict:
    """T-IC-4: CD8_CTL has highest effector_potency among all lymphocytes.

    Cytotoxic T lymphocytes deploy perforin/granzyme B with single-cell
    precision — the highest killing efficiency per lymphocyte contact.
    References: Voskoboinik I et al. (2015) Nat Rev Immunol 15:388-400.
    """
    lymphocytes = ["CD4_Th1", "CD4_Th2", "CD4_Treg", "CD8_CTL", "B_cell_naive", "B_cell_plasma", "memory_B", "memory_T"]
    ctl = next(e for e in IC_ENTITIES if e.name == "CD8_CTL")
    lymph_potencies = [e.effector_potency for e in IC_ENTITIES if e.name in lymphocytes]
    max_potency = max(lymph_potencies)
    passed = bool(abs(ctl.effector_potency - max_potency) < 0.01)
    return {
        "name": "T-IC-4",
        "passed": passed,
        "CTL_effector_potency": ctl.effector_potency,
        "max_lymphocyte_effector_potency": float(max_potency),
    }


def verify_t_ic_5(results: list[ICKernelResult]) -> dict:
    """T-IC-5: B_cell_plasma has the lowest proliferation_capacity.

    Terminally differentiated plasma cells are replication-arrested,
    committed entirely to high-rate antibody secretion (10^3–10^4 Ab/s).
    References: Nutt SL et al. (2015) Nat Rev Immunol 15:160-171.
    """
    plasma = next(e for e in IC_ENTITIES if e.name == "B_cell_plasma")
    min_prolif = min(e.proliferation_capacity for e in IC_ENTITIES)
    passed = bool(abs(plasma.proliferation_capacity - min_prolif) < 0.01)
    return {
        "name": "T-IC-5",
        "passed": passed,
        "plasma_proliferation": plasma.proliferation_capacity,
        "global_min_proliferation": float(min_prolif),
    }


def verify_t_ic_6(results: list[ICKernelResult]) -> dict:
    """T-IC-6: Innate cells have larger mean heterogeneity gap (F - IC) than adaptive.

    Innate cells have extreme channel profiles (very fast activation but no
    memory, or high tissue-resident with low tolerance) creating geometric
    slaughter. Adaptive cells are functionally more balanced → smaller gap.
    References: Axiom-0 — geometric slaughter from channel heterogeneity.
    """
    innate_gaps = [r.F - r.IC for r in results if r.arm == "innate"]
    adaptive_gaps = [r.F - r.IC for r in results if r.arm == "adaptive"]
    innate_mean_gap = float(np.mean(innate_gaps))
    adaptive_mean_gap = float(np.mean(adaptive_gaps))
    passed = bool(innate_mean_gap > adaptive_mean_gap)
    return {
        "name": "T-IC-6",
        "passed": passed,
        "innate_mean_heterogeneity_gap": innate_mean_gap,
        "adaptive_mean_heterogeneity_gap": adaptive_mean_gap,
        "ratio": innate_mean_gap / max(adaptive_mean_gap, EPSILON),
    }


def verify_all_theorems() -> list[dict]:
    """Run all T-IC theorems and return results."""
    results = compute_all_entities()
    return [
        verify_t_ic_1(results),
        verify_t_ic_2(results),
        verify_t_ic_3(results),
        verify_t_ic_4(results),
        verify_t_ic_5(results),
        verify_t_ic_6(results),
    ]
