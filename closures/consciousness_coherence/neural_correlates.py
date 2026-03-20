"""Neural Correlates Closure — Consciousness Coherence Domain.

Tier-2 closure mapping 12 neural correlate of consciousness (NCC) systems
through the GCD kernel.  Each system is characterized by 8 channels drawn
from cognitive neuroscience and consciousness research.

Channels (8, equal weights w_i = 1/8):
  0  temporal_integration    — integration across time windows (1 = perfect)
  1  spatial_coherence       — synchronized activity across brain regions (1 = full)
  2  information_complexity  — richness of representational content (1 = maximal)
  3  recurrent_processing    — degree of re-entrant/feedback processing (1 = fully recurrent)
  4  reportability           — accessibility to conscious report (1 = fully reportable)
  5  selectivity             — discriminative power (1 = perfectly selective)
  6  stability_duration      — duration of coherent state (1 = indefinitely stable)
  7  metabolic_efficiency    — energetic efficiency (1 = efficient/low demand)

12 entities across 4 categories:
  Binding (3): gamma_oscillation, cross_frequency_coupling, phase_amplitude_coupling
  Network (3): default_mode_network, global_workspace, frontoparietal_network
  Gating (3): thalamic_relay, reticular_nucleus, pulvinar_gate
  Modulation (3): cholinergic_arousal, noradrenergic_alerting, dopaminergic_salience

6 theorems (T-NC-1 through T-NC-6).
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

NC_CHANNELS = [
    "temporal_integration",
    "spatial_coherence",
    "information_complexity",
    "recurrent_processing",
    "reportability",
    "selectivity",
    "stability_duration",
    "metabolic_efficiency",
]
N_NC_CHANNELS = len(NC_CHANNELS)


@dataclass(frozen=True, slots=True)
class NeuralCorrelateEntity:
    """A neural correlate of consciousness system with 8 measurable channels."""

    name: str
    category: str
    temporal_integration: float
    spatial_coherence: float
    information_complexity: float
    recurrent_processing: float
    reportability: float
    selectivity: float
    stability_duration: float
    metabolic_efficiency: float

    def trace_vector(self) -> np.ndarray:
        return np.array(
            [
                self.temporal_integration,
                self.spatial_coherence,
                self.information_complexity,
                self.recurrent_processing,
                self.reportability,
                self.selectivity,
                self.stability_duration,
                self.metabolic_efficiency,
            ]
        )


NC_ENTITIES: tuple[NeuralCorrelateEntity, ...] = (
    # Binding — high temporal integration, high spatial coherence
    NeuralCorrelateEntity("gamma_oscillation", "binding", 0.95, 0.85, 0.65, 0.80, 0.60, 0.75, 0.55, 0.65),
    NeuralCorrelateEntity("cross_frequency_coupling", "binding", 0.85, 0.90, 0.70, 0.80, 0.55, 0.75, 0.55, 0.60),
    NeuralCorrelateEntity("phase_amplitude_coupling", "binding", 0.80, 0.85, 0.70, 0.80, 0.55, 0.75, 0.55, 0.65),
    # Network — high complexity, reportability, recurrent processing
    NeuralCorrelateEntity("default_mode_network", "network", 0.60, 0.75, 0.85, 0.80, 0.70, 0.50, 0.75, 0.60),
    NeuralCorrelateEntity("global_workspace", "network", 0.75, 0.85, 0.90, 0.85, 0.90, 0.60, 0.70, 0.65),
    NeuralCorrelateEntity("frontoparietal_network", "network", 0.70, 0.80, 0.80, 0.75, 0.80, 0.65, 0.65, 0.55),
    # Gating — high selectivity, narrow function
    NeuralCorrelateEntity("thalamic_relay", "gating", 0.45, 0.30, 0.25, 0.20, 0.55, 0.95, 0.70, 0.75),
    NeuralCorrelateEntity("reticular_nucleus", "gating", 0.35, 0.25, 0.20, 0.25, 0.20, 0.85, 0.30, 0.65),
    NeuralCorrelateEntity("pulvinar_gate", "gating", 0.55, 0.50, 0.40, 0.35, 0.45, 0.80, 0.50, 0.60),
    # Modulation — diffuse neuromodulatory systems
    NeuralCorrelateEntity("cholinergic_arousal", "modulation", 0.65, 0.55, 0.50, 0.45, 0.60, 0.55, 0.55, 0.40),
    NeuralCorrelateEntity("noradrenergic_alerting", "modulation", 0.70, 0.50, 0.45, 0.40, 0.55, 0.60, 0.50, 0.45),
    NeuralCorrelateEntity("dopaminergic_salience", "modulation", 0.60, 0.60, 0.55, 0.50, 0.65, 0.70, 0.45, 0.35),
)


@dataclass(frozen=True, slots=True)
class NCKernelResult:
    """Kernel output for a neural correlate entity."""

    name: str
    category: str
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
            "F": self.F,
            "omega": self.omega,
            "S": self.S,
            "C": self.C,
            "kappa": self.kappa,
            "IC": self.IC,
            "regime": self.regime,
        }


def compute_nc_kernel(entity: NeuralCorrelateEntity) -> NCKernelResult:
    """Compute GCD kernel for a neural correlate entity."""
    c = entity.trace_vector()
    c = np.clip(c, EPSILON, 1.0 - EPSILON)
    w = np.ones(N_NC_CHANNELS) / N_NC_CHANNELS
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
    return NCKernelResult(
        name=entity.name,
        category=entity.category,
        F=F,
        omega=omega,
        S=S,
        C=C_val,
        kappa=kappa,
        IC=IC,
        regime=regime,
    )


def compute_all_entities() -> list[NCKernelResult]:
    """Compute kernel outputs for all neural correlate entities."""
    return [compute_nc_kernel(e) for e in NC_ENTITIES]


# ── Theorems ──────────────────────────────────────────────────────────


def verify_t_nc_1(results: list[NCKernelResult]) -> dict:
    """T-NC-1: Global workspace has highest F — broad integration across
    temporal, spatial, complexity, recurrent, and reportability channels.
    """
    gws = next(r for r in results if r.name == "global_workspace")
    max_F = max(r.F for r in results)
    passed = abs(gws.F - max_F) < 0.02
    return {"name": "T-NC-1", "passed": bool(passed), "gws_F": gws.F, "max_F": float(max_F)}


def verify_t_nc_2(results: list[NCKernelResult]) -> dict:
    """T-NC-2: Gating category has lowest mean F — narrow function
    with high selectivity but limited integration across other channels.
    """
    cats = {r.category for r in results}
    cat_means = {}
    for cat in cats:
        vals = [r.F for r in results if r.category == cat]
        cat_means[cat] = float(np.mean(vals))
    gating_mean = cat_means["gating"]
    passed = all(gating_mean <= v + 1e-9 for v in cat_means.values())
    return {
        "name": "T-NC-2",
        "passed": bool(passed),
        "gating_mean_F": gating_mean,
        "all_means": cat_means,
    }


def verify_t_nc_3(results: list[NCKernelResult]) -> dict:
    """T-NC-3: Gamma oscillation has highest temporal integration —
    40 Hz binding rhythm is the fastest large-scale integration mechanism.
    """
    gamma = next(e for e in NC_ENTITIES if e.name == "gamma_oscillation")
    max_ti = max(e.temporal_integration for e in NC_ENTITIES)
    passed = abs(gamma.temporal_integration - max_ti) < 0.01
    return {
        "name": "T-NC-3",
        "passed": bool(passed),
        "gamma_ti": gamma.temporal_integration,
        "max_ti": float(max_ti),
    }


def verify_t_nc_4(results: list[NCKernelResult]) -> dict:
    """T-NC-4: Thalamic relay has largest heterogeneity gap — extreme
    selectivity (0.95) paired with minimal complexity/recurrence creates
    maximal channel divergence.
    """
    gaps = {r.name: r.F - r.IC for r in results}
    thal_gap = gaps["thalamic_relay"]
    max_gap = max(gaps.values())
    passed = abs(thal_gap - max_gap) < 0.01
    return {
        "name": "T-NC-4",
        "passed": bool(passed),
        "thalamic_gap": float(thal_gap),
        "max_gap": float(max_gap),
    }


def verify_t_nc_5(results: list[NCKernelResult]) -> dict:
    """T-NC-5: Binding category has highest mean spatial coherence —
    oscillatory binding mechanisms synchronize across distributed regions.
    """
    cats = {e.category for e in NC_ENTITIES}
    cat_means = {}
    for cat in cats:
        vals = [e.spatial_coherence for e in NC_ENTITIES if e.category == cat]
        cat_means[cat] = float(np.mean(vals))
    bind_mean = cat_means["binding"]
    passed = all(bind_mean >= v - 1e-9 for v in cat_means.values())
    return {
        "name": "T-NC-5",
        "passed": bool(passed),
        "binding_spatial": bind_mean,
        "all_means": cat_means,
    }


def verify_t_nc_6(results: list[NCKernelResult]) -> dict:
    """T-NC-6: Reticular nucleus is in Collapse regime — the most
    constrained gating mechanism, with minimal reportability and
    stability duration.
    """
    rn = next(r for r in results if r.name == "reticular_nucleus")
    passed = rn.regime == "Collapse"
    return {"name": "T-NC-6", "passed": bool(passed), "rn_regime": rn.regime, "rn_omega": rn.omega}


def verify_all_theorems() -> list[dict]:
    """Run all T-NC theorems."""
    results = compute_all_entities()
    return [
        verify_t_nc_1(results),
        verify_t_nc_2(results),
        verify_t_nc_3(results),
        verify_t_nc_4(results),
        verify_t_nc_5(results),
        verify_t_nc_6(results),
    ]


def main() -> None:
    """Entry point."""
    results = compute_all_entities()
    print("=" * 78)
    print("NEURAL CORRELATES OF CONSCIOUSNESS — GCD KERNEL ANALYSIS")
    print("=" * 78)
    print(f"{'Entity':<28} {'Cat':<14} {'F':>6} {'ω':>6} {'IC':>6} {'Δ':>6} {'Regime'}")
    print("-" * 78)
    for r in results:
        gap = r.F - r.IC
        print(f"{r.name:<28} {r.category:<14} {r.F:6.3f} {r.omega:6.3f} {r.IC:6.3f} {gap:6.3f} {r.regime}")

    print("\n── Theorems ──")
    for t in verify_all_theorems():
        print(f"  {t['name']}: {'PROVEN' if t['passed'] else 'FAILED'}")


if __name__ == "__main__":
    main()
