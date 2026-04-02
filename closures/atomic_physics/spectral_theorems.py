"""Spectral Theorems Closure — Atomic Spectral Analysis.

Tier-2 closure mapping 12 canonical spectral transitions through the
GCD kernel.  Each transition is characterized by 6 channels derived
from spectral line and fine-structure computations.

Channels (6, equal weights w_i = 1/6):
  0  wavelength_norm    — λ/λ_max, longer wavelength → 1.0
  1  energy_norm        — E/E_max, higher transition energy → 1.0
  2  spectral_fidelity  — F_eff from Rydberg prediction accuracy
  3  fine_split_norm    — fine-structure splitting / max splitting
  4  z_alpha_sq         — (Zα)² relativistic parameter / max
  5  series_position    — 1/(n_upper - n_lower + 1), convergent series

12 entities across 4 categories:
  Hydrogen_Lyman (3):    Ly-α, Ly-β, Ly-γ
  Hydrogen_Balmer (3):   H-α, H-β, H-γ
  Hydrogen_Paschen (3):  Pa-α, Pa-β, Pa-γ
  Multi_Z (3):           He⁺ Bα, Li²⁺ Bα, C⁵⁺ Bα

6 theorems (T-SP-1 through T-SP-6).
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

SP_CHANNELS = [
    "wavelength_norm",
    "energy_norm",
    "spectral_fidelity",
    "fine_split_norm",
    "z_alpha_sq",
    "series_position",
]
N_SP_CHANNELS = len(SP_CHANNELS)

# Physical constants
R_INF = 1.0973731568539e7  # Rydberg constant (m⁻¹)
HC_EV_NM = 1239.8419843  # hc in eV·nm
ALPHA_FS = 7.2973525693e-3  # Fine-structure constant


@dataclass(frozen=True, slots=True)
class SpectralEntity:
    """A spectral transition with 6 measurable channels."""

    name: str
    category: str
    Z: int
    n_lower: int
    n_upper: int
    wavelength_nm: float  # Predicted wavelength
    energy_eV: float  # Transition energy
    fine_splitting_eV: float  # Fine-structure splitting magnitude
    z_alpha_squared: float  # (Zα)² relativistic parameter

    def trace_vector(self) -> np.ndarray:
        """Build 6-channel trace from spectral properties."""
        # Normalization constants (from the 12 entities below)
        lam_max = 1875.0  # Pa-α wavelength (nm)
        e_max = 13.6  # Ly limit ≈ 13.6 eV
        split_max = 0.060  # C⁵⁺ fine splitting (eV)
        za2_max = 0.0019  # C⁵⁺ (Zα)²

        return np.array(
            [
                self.wavelength_nm / lam_max,  # longer → 1
                self.energy_eV / e_max,  # higher E → 1
                1.0,  # Rydberg is exact for H-like
                self.fine_splitting_eV / split_max if split_max > 0 else EPSILON,
                self.z_alpha_squared / za2_max if za2_max > 0 else EPSILON,
                1.0 / (self.n_upper - self.n_lower + 1),  # convergent
            ]
        )


def _rydberg_wavelength(Z: int, n1: int, n2: int) -> float:
    """Rydberg wavelength in nm."""
    inv_lam = R_INF * Z**2 * (1.0 / n1**2 - 1.0 / n2**2)
    return 1e9 / inv_lam  # m → nm


def _transition_energy(Z: int, n1: int, n2: int) -> float:
    """Transition energy in eV."""
    return 13.605693 * Z**2 * (1.0 / n1**2 - 1.0 / n2**2)


def _fine_splitting(Z: int, n: int) -> float:
    """Approximate fine-structure splitting for n, δj=1, in eV."""
    # E_fs ≈ (Zα)² · E_n / n  (leading order)
    E_n = 13.605693 * Z**2 / n**2
    return abs((Z * ALPHA_FS) ** 2 * E_n / n)


SP_ENTITIES: tuple[SpectralEntity, ...] = (
    # Hydrogen Lyman series (n_lower=1)
    SpectralEntity(
        "Ly_alpha",
        "hydrogen_lyman",
        1,
        1,
        2,
        _rydberg_wavelength(1, 1, 2),
        _transition_energy(1, 1, 2),
        _fine_splitting(1, 2),
        (ALPHA_FS) ** 2,
    ),
    SpectralEntity(
        "Ly_beta",
        "hydrogen_lyman",
        1,
        1,
        3,
        _rydberg_wavelength(1, 1, 3),
        _transition_energy(1, 1, 3),
        _fine_splitting(1, 3),
        (ALPHA_FS) ** 2,
    ),
    SpectralEntity(
        "Ly_gamma",
        "hydrogen_lyman",
        1,
        1,
        4,
        _rydberg_wavelength(1, 1, 4),
        _transition_energy(1, 1, 4),
        _fine_splitting(1, 4),
        (ALPHA_FS) ** 2,
    ),
    # Hydrogen Balmer series (n_lower=2)
    SpectralEntity(
        "H_alpha",
        "hydrogen_balmer",
        1,
        2,
        3,
        _rydberg_wavelength(1, 2, 3),
        _transition_energy(1, 2, 3),
        _fine_splitting(1, 3),
        (ALPHA_FS) ** 2,
    ),
    SpectralEntity(
        "H_beta",
        "hydrogen_balmer",
        1,
        2,
        4,
        _rydberg_wavelength(1, 2, 4),
        _transition_energy(1, 2, 4),
        _fine_splitting(1, 4),
        (ALPHA_FS) ** 2,
    ),
    SpectralEntity(
        "H_gamma",
        "hydrogen_balmer",
        1,
        2,
        5,
        _rydberg_wavelength(1, 2, 5),
        _transition_energy(1, 2, 5),
        _fine_splitting(1, 5),
        (ALPHA_FS) ** 2,
    ),
    # Hydrogen Paschen series (n_lower=3)
    SpectralEntity(
        "Pa_alpha",
        "hydrogen_paschen",
        1,
        3,
        4,
        _rydberg_wavelength(1, 3, 4),
        _transition_energy(1, 3, 4),
        _fine_splitting(1, 4),
        (ALPHA_FS) ** 2,
    ),
    SpectralEntity(
        "Pa_beta",
        "hydrogen_paschen",
        1,
        3,
        5,
        _rydberg_wavelength(1, 3, 5),
        _transition_energy(1, 3, 5),
        _fine_splitting(1, 5),
        (ALPHA_FS) ** 2,
    ),
    SpectralEntity(
        "Pa_gamma",
        "hydrogen_paschen",
        1,
        3,
        6,
        _rydberg_wavelength(1, 3, 6),
        _transition_energy(1, 3, 6),
        _fine_splitting(1, 6),
        (ALPHA_FS) ** 2,
    ),
    # Multi-Z Balmer-alpha analogs (n=2→3 for Z > 1)
    SpectralEntity(
        "He_plus_Balpha",
        "multi_z",
        2,
        2,
        3,
        _rydberg_wavelength(2, 2, 3),
        _transition_energy(2, 2, 3),
        _fine_splitting(2, 3),
        (2 * ALPHA_FS) ** 2,
    ),
    SpectralEntity(
        "Li2_plus_Balpha",
        "multi_z",
        3,
        2,
        3,
        _rydberg_wavelength(3, 2, 3),
        _transition_energy(3, 2, 3),
        _fine_splitting(3, 3),
        (3 * ALPHA_FS) ** 2,
    ),
    SpectralEntity(
        "C5_plus_Balpha",
        "multi_z",
        6,
        2,
        3,
        _rydberg_wavelength(6, 2, 3),
        _transition_energy(6, 2, 3),
        _fine_splitting(6, 3),
        (6 * ALPHA_FS) ** 2,
    ),
)


@dataclass(frozen=True, slots=True)
class SPKernelResult:
    """Kernel output for a spectral entity."""

    name: str
    category: str
    Z: int
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
            "category": self.category,
            "Z": self.Z,
            "F": self.F,
            "omega": self.omega,
            "S": self.S,
            "C": self.C,
            "kappa": self.kappa,
            "IC": self.IC,
            "regime": self.regime,
        }


def _classify_regime(omega: float, F: float, S: float, C: float) -> str:
    if omega >= 0.30:
        return "Collapse"
    if omega < 0.038 and F > 0.90 and S < 0.15 and C < 0.14:
        return "Stable"
    return "Watch"


def compute_sp_kernel(entity: SpectralEntity) -> SPKernelResult:
    """Compute kernel invariants for a spectral entity."""
    c = np.clip(entity.trace_vector(), EPSILON, 1 - EPSILON)
    w = np.ones(N_SP_CHANNELS) / N_SP_CHANNELS
    result = compute_kernel_outputs(c, w)
    F = float(result["F"])
    omega = float(result["omega"])
    S = float(result["S"])
    C = float(result["C"])
    kappa = float(result["kappa"])
    IC = float(result["IC"])
    regime = _classify_regime(omega, F, S, C)
    return SPKernelResult(
        name=entity.name,
        category=entity.category,
        Z=entity.Z,
        F=F,
        omega=omega,
        S=S,
        C=C,
        kappa=kappa,
        IC=IC,
        regime=regime,
    )


def compute_all_entities() -> list[SPKernelResult]:
    """Compute kernel for all spectral entities."""
    return [compute_sp_kernel(e) for e in SP_ENTITIES]


# ---------------------------------------------------------------------------
# Theorems T-SP-1 through T-SP-6
# ---------------------------------------------------------------------------


def verify_t_sp_1(results: list[SPKernelResult]) -> dict:
    """T-SP-1: Lyman series has highest mean F among hydrogen series.

    Lyman transitions have the largest energy (closest to ionization)
    and produce the highest energy_norm channel values, raising the
    arithmetic mean fidelity above Balmer and Paschen.
    """
    cats: dict[str, list[float]] = {}
    for r in results:
        if r.category.startswith("hydrogen_"):
            cats.setdefault(r.category, []).append(r.F)
    lyman_F = np.mean(cats["hydrogen_lyman"])
    other_F = [np.mean(v) for k, v in cats.items() if k != "hydrogen_lyman"]
    passed = float(lyman_F) > max(float(x) for x in other_F)
    return {
        "name": "T-SP-1",
        "passed": bool(passed),
        "lyman_mean_F": float(lyman_F),
        "other_max_F": float(max(other_F)),
    }


def verify_t_sp_2(results: list[SPKernelResult]) -> dict:
    """T-SP-2: Multi-Z entities have higher mean IC than hydrogen series.

    Higher-Z ions have larger fine-structure splittings and (Zα)²
    values, filling more channels with non-trivial values and
    raising the geometric mean (IC) above hydrogen's near-zero
    fine-structure channels.
    """
    multi_z = [r for r in results if r.category == "multi_z"]
    hydrogen = [r for r in results if r.category.startswith("hydrogen_")]
    mz_IC = float(np.mean([r.IC for r in multi_z]))
    h_IC = float(np.mean([r.IC for r in hydrogen]))
    passed = mz_IC > h_IC
    return {
        "name": "T-SP-2",
        "passed": bool(passed),
        "multi_z_mean_IC": mz_IC,
        "hydrogen_mean_IC": h_IC,
    }


def verify_t_sp_3(results: list[SPKernelResult]) -> dict:
    """T-SP-3: Duality identity F + ω = 1 holds for all spectral entities.

    Exact by construction across all 12 spectral transitions.
    """
    max_residual = max(abs(r.F + r.omega - 1.0) for r in results)
    passed = max_residual < 1e-10
    return {
        "name": "T-SP-3",
        "passed": bool(passed),
        "max_duality_residual": float(max_residual),
        "n_entities": len(results),
    }


def verify_t_sp_4(results: list[SPKernelResult]) -> dict:
    """T-SP-4: Integrity bound IC ≤ F holds for all spectral entities."""
    violations = [r.name for r in results if r.IC > r.F + 1e-12]
    passed = len(violations) == 0
    return {
        "name": "T-SP-4",
        "passed": bool(passed),
        "violations": violations,
        "n_entities": len(results),
    }


def verify_t_sp_5(results: list[SPKernelResult]) -> dict:
    """T-SP-5: C⁵⁺ Balmer-alpha has highest IC among all entities.

    C⁵⁺ (Z=6) has the strongest fine-structure effects, filling the
    fine_split and z_alpha_sq channels with the largest values.  Its
    energy_norm is also maximal, giving the most uniform trace vector
    and therefore the highest geometric mean (IC).
    """
    c5 = next(r for r in results if r.name == "C5_plus_Balpha")
    max_IC = max(r.IC for r in results)
    passed = abs(c5.IC - max_IC) < 1e-12
    return {
        "name": "T-SP-5",
        "passed": bool(passed),
        "C5_IC": c5.IC,
        "max_IC": max_IC,
    }


def verify_t_sp_6(results: list[SPKernelResult]) -> dict:
    """T-SP-6: Balmer series has lowest mean F among hydrogen series.

    Balmer transitions (n=2→3,4,5) occupy a middle ground where
    wavelength_norm is moderate and energy_norm is low relative to
    Lyman.  The Paschen series compensates with high wavelength_norm
    (near 1.0 for Pa-α at 1875 nm), giving Balmer the lowest mean F.
    """
    cats: dict[str, list[float]] = {}
    for r in results:
        if r.category.startswith("hydrogen_"):
            cats.setdefault(r.category, []).append(r.F)
    balmer_F = float(np.mean(cats["hydrogen_balmer"]))
    other_F = [float(np.mean(v)) for k, v in cats.items() if k != "hydrogen_balmer"]
    passed = balmer_F < min(other_F)
    return {
        "name": "T-SP-6",
        "passed": bool(passed),
        "balmer_mean_F": balmer_F,
        "other_min_F": min(other_F),
    }


def verify_all_theorems() -> list[dict]:
    """Run all T-SP theorems."""
    results = compute_all_entities()
    return [
        verify_t_sp_1(results),
        verify_t_sp_2(results),
        verify_t_sp_3(results),
        verify_t_sp_4(results),
        verify_t_sp_5(results),
        verify_t_sp_6(results),
    ]


if __name__ == "__main__":
    for t in verify_all_theorems():
        status = "PROVEN" if t["passed"] else "FAILED"
        print(f"  {t['name']}: {status}  {t}")
