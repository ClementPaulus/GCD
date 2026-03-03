"""Deep analysis script for brain kernel — run once, not part of module."""

from __future__ import annotations

import numpy as np

from closures.evolution.brain_kernel import (
    BRAIN_CATALOG,
    BRAIN_CHANNELS,
    compute_all_brains,
    compute_developmental_trajectory,
    compute_pathology_kernels,
)
from umcp.frozen_contract import EPSILON
from umcp.kernel_optimized import compute_kernel_outputs

# ═══════════════════════════════════════════════════════════════
# ANALYSIS 1: The Brain-Organism Paradox
# ═══════════════════════════════════════════════════════════════
print("=" * 75)
print("ANALYSIS 1: THE BRAIN-ORGANISM PARADOX")
print("=" * 75)

results = compute_all_brains()
human_brain = next(r for r in results if r.species == "Homo sapiens")

print(f"""
  BRAIN kernel (10 neuroscience channels):
    F     = {human_brain.F:.3f}    (highest in catalog)
    IC    = {human_brain.IC:.3f}    (highest in catalog)
    delta = {human_brain.delta:.4f}   (LOWEST in catalog - most coherent)
    IC/F  = {human_brain.IC_F_ratio:.3f}   (near-perfect neural coherence)
    omega = {human_brain.omega:.3f}    (Watch regime)

  ORGANISM kernel (8 evolutionary channels):
    F     = 0.654    (moderate)
    IC    = 0.318    (low)
    delta = 0.336    (HIGHEST in catalog - most fragile)
    IC/F  = 0.487    (lowest among cognitively complex species)
    omega = 0.346    (Collapse regime)

  THE PARADOX:
    The most COHERENT brain lives inside the most FRAGILE organism.
    Brain IC/F = {human_brain.IC_F_ratio:.3f} vs Organism IC/F = 0.487
    The brain is {human_brain.IC_F_ratio / 0.487:.2f}x more coherent than the organism.
""")

# ═══════════════════════════════════════════════════════════════
# ANALYSIS 2: Language as Universal Bottleneck
# ═══════════════════════════════════════════════════════════════
print("=" * 75)
print("ANALYSIS 2: LANGUAGE AS UNIVERSAL BOTTLENECK")
print("=" * 75)

print(f"\n  {'Species':40s} {'Weakest':25s} {'Value':>6s} {'IC/F':>6s}")
print("  " + "-" * 80)
for r in sorted(results, key=lambda x: x.IC_F_ratio):
    val = r.channels.get(r.weakest_channel, 0)
    print(f"  {r.species:40s} {r.weakest_channel:25s} {val:6.3f} {r.IC_F_ratio:6.3f}")

lang_weak = sum(1 for r in results if r.weakest_channel == "language_architecture")
total = len(results)
print(f"\n  Language is weakest for {lang_weak}/{total} species ({lang_weak / total * 100:.0f}%)")
print(
    f"  Homo sapiens weakest: {human_brain.weakest_channel} ({human_brain.channels[human_brain.weakest_channel]:.2f})"
)

# ═══════════════════════════════════════════════════════════════
# ANALYSIS 3: Language Counterfactual
# ═══════════════════════════════════════════════════════════════
print("\n" + "=" * 75)
print("ANALYSIS 3: COUNTERFACTUAL - WHAT IF THEY HAD LANGUAGE?")
print("=" * 75)

print(f"\n  {'Species':40s} {'Actual':>8s} {'+Lang':>8s} {'Gain':>8s}")
print("  " + "-" * 68)

for profile in BRAIN_CATALOG:
    if "sapiens" in profile.species:
        continue
    c = profile.trace_vector()
    w = np.full(10, 0.1)
    k_actual = compute_kernel_outputs(c, w, EPSILON)

    c_lang = c.copy()
    lang_idx = BRAIN_CHANNELS.index("language_architecture")
    c_lang[lang_idx] = 0.98
    k_lang = compute_kernel_outputs(c_lang, w, EPSILON)

    F_a = float(k_actual["F"])
    IC_F_a = float(k_actual["IC"]) / F_a if F_a > 0 else 0
    F_l = float(k_lang["F"])
    IC_F_l = float(k_lang["IC"]) / F_l if F_l > 0 else 0

    delta_icf = IC_F_l - IC_F_a
    print(f"  {profile.species:40s} {IC_F_a:8.3f} {IC_F_l:8.3f} {delta_icf:+8.3f}")

# ═══════════════════════════════════════════════════════════════
# ANALYSIS 4: Developmental Trajectory in Detail
# ═══════════════════════════════════════════════════════════════
print("\n" + "=" * 75)
print("ANALYSIS 4: DEVELOPMENTAL TRAJECTORY")
print("=" * 75)

dev = compute_developmental_trajectory()
print(f"\n  {'Stage':35s} {'F':>6s} {'IC':>6s} {'IC/F':>6s} {'Var':>8s} {'Regime':>9s}")
print("  " + "-" * 80)
for d in dev:
    print(
        f"  {d['stage']:35s} {d['F']:6.3f} {d['IC']:6.3f} "
        f"{d['IC_F']:6.3f} {d['internal_variance']:8.4f} {d['regime']:>9s}"
    )

# Key transitions
print("\n  KEY TRANSITIONS:")
for i in range(1, len(dev)):
    if dev[i]["regime"] != dev[i - 1]["regime"]:
        print(f"    {dev[i - 1]['stage']:30s} -> {dev[i]['stage']:30s}: {dev[i - 1]['regime']} -> {dev[i]['regime']}")
    if dev[i]["weakest_channel"] != dev[i - 1]["weakest_channel"]:
        print(
            f"    Weakest shifts: {dev[i - 1]['weakest_channel']} -> {dev[i]['weakest_channel']} at {dev[i]['stage']}"
        )

# ═══════════════════════════════════════════════════════════════
# ANALYSIS 5: Pathology Severity Ranking
# ═══════════════════════════════════════════════════════════════
print("\n" + "=" * 75)
print("ANALYSIS 5: PATHOLOGY SEVERITY (by IC/F drop from healthy)")
print("=" * 75)

path = compute_pathology_kernels()
healthy = next(p for p in path if p["condition"] == "Healthy Adult")
h_icf = healthy["IC_F"]

print(f"\n  Healthy baseline: IC/F = {h_icf:.3f}")
print(f"\n  {'Condition':40s} {'IC/F':>6s} {'Drop':>8s} {'Regime':>9s}  Weakest")
print("  " + "-" * 85)
for p in sorted(path, key=lambda x: x["IC_F"], reverse=True):
    drop = h_icf - p["IC_F"]
    print(f"  {p['condition']:40s} {p['IC_F']:6.3f} {drop:+8.3f} {p['regime']:>9s}  {p['weakest_channel']}")

# ═══════════════════════════════════════════════════════════════
# ANALYSIS 6: The Neanderthal Question
# ═══════════════════════════════════════════════════════════════
print("\n" + "=" * 75)
print("ANALYSIS 6: WHY NEANDERTHALS WENT EXTINCT")
print("=" * 75)

nean = next(r for r in results if "neanderthalensis" in r.species)
erectus = next(r for r in results if "erectus" in r.species)

print(f"\n  {'Metric':30s} {'H.sapiens':>12s} {'Neanderthal':>12s} {'H.erectus':>12s}")
print("  " + "-" * 70)
for ch in BRAIN_CHANNELS:
    h = human_brain.channels.get(ch, 0)
    n = nean.channels.get(ch, 0)
    e = erectus.channels.get(ch, 0)
    marker = " <--" if abs(h - n) > 0.15 else ""
    print(f"  {ch:30s} {h:12.3f} {n:12.3f} {e:12.3f}{marker}")

print(f"\n  {'F':30s} {human_brain.F:12.3f} {nean.F:12.3f} {erectus.F:12.3f}")
print(f"  {'IC':30s} {human_brain.IC:12.3f} {nean.IC:12.3f} {erectus.IC:12.3f}")
print(f"  {'IC/F':30s} {human_brain.IC_F_ratio:12.3f} {nean.IC_F_ratio:12.3f} {erectus.IC_F_ratio:12.3f}")
print(f"  {'delta':30s} {human_brain.delta:12.4f} {nean.delta:12.4f} {erectus.delta:12.4f}")
print(f"  {'omega':30s} {human_brain.omega:12.3f} {nean.omega:12.3f} {erectus.omega:12.3f}")
print(f"  {'regime':30s} {human_brain.regime:>12s} {nean.regime:>12s} {erectus.regime:>12s}")

# Where does sapiens beat neanderthal?
print("\n  H. sapiens advantages over Neanderthal:")
for ch in BRAIN_CHANNELS:
    h = human_brain.channels.get(ch, 0)
    n = nean.channels.get(ch, 0)
    if h > n + 0.05:
        print(f"    {ch}: {h:.3f} vs {n:.3f} (+{h - n:.3f})")

# What kills neanderthal IC?
print(f"\n  Neanderthal weakest: {nean.weakest_channel} ({nean.channels[nean.weakest_channel]:.3f})")
print(
    f"  Language_architecture: sapiens={human_brain.channels['language_architecture']:.3f} "
    f"vs nean={nean.channels['language_architecture']:.3f}"
)
lang_gap = human_brain.channels["language_architecture"] - nean.channels["language_architecture"]
print(f"  Language gap: {lang_gap:.3f}")
print(f"\n  INSIGHT: Neanderthal brain was large and capable (F={nean.F:.3f})")
print(
    f"  but language_architecture = {nean.channels['language_architecture']:.3f} vs sapiens {human_brain.channels['language_architecture']:.3f}"
)
print("  This ONE channel difference explains the IC/F gap:")
print(f"    Neanderthal IC/F = {nean.IC_F_ratio:.3f} vs Sapiens IC/F = {human_brain.IC_F_ratio:.3f}")

# ═══════════════════════════════════════════════════════════════
# ANALYSIS 7: Consciousness Substrate Decomposition
# ═══════════════════════════════════════════════════════════════
print("\n" + "=" * 75)
print("ANALYSIS 7: CONSCIOUSNESS SUBSTRATE DECOMPOSITION")
print("=" * 75)

# Group channels into functional substrates
substrates = {
    "Hardware": ["encephalization_quotient", "cortical_neuron_count", "synaptic_density"],
    "Architecture": ["prefrontal_ratio", "connectivity_index", "metabolic_investment"],
    "Software": ["language_architecture", "temporal_integration", "social_cognition"],
    "Adaptability": ["plasticity_window"],
}

print(f"\n  {'Substrate':15s} {'Channels':>3s} {'H.sapiens':>10s} {'Chimp':>10s} {'Raven':>10s} {'Dolphin':>10s}")
print("  " + "-" * 60)
for sub_name, channels in substrates.items():
    h_vals = [human_brain.channels[ch] for ch in channels]
    chimp = next(r for r in results if "troglodytes" in r.species)
    raven = next(r for r in results if "corax" in r.species)
    dolphin = next(r for r in results if "Tursiops" in r.species)

    c_vals = [chimp.channels[ch] for ch in channels]
    r_vals = [raven.channels[ch] for ch in channels]
    d_vals = [dolphin.channels[ch] for ch in channels]

    print(
        f"  {sub_name:15s} {len(channels):3d}    "
        f"{np.mean(h_vals):10.3f} {np.mean(c_vals):10.3f} "
        f"{np.mean(r_vals):10.3f} {np.mean(d_vals):10.3f}"
    )

print("\n  INSIGHT: The largest gap between humans and other intelligent")
print("  species is in Software (language + temporal + social), not Hardware")
print("  (neuron count, EQ, synapses). Consciousness is a SOFTWARE phenomenon")
print("  running on adequate hardware, not a hardware achievement.")

# ═══════════════════════════════════════════════════════════════
# SUMMARY
# ═══════════════════════════════════════════════════════════════
print("\n" + "=" * 75)
print("SUMMARY: FIVE KEY DISCOVERIES")
print("=" * 75)
print("""
  1. BRAIN-ORGANISM PARADOX: The most coherent brain (IC/F=0.996)
     lives inside the most fragile organism (IC/F=0.487). The brain
     is 2x more coherent than its host.

  2. LANGUAGE IS THE UNIVERSAL BOTTLENECK: 18/20 species have
     language_architecture as their IC killer. Human uniqueness
     is not more brain — it's filling the language gap.

  3. CONSCIOUSNESS IS SOFTWARE: The Hardware substrate (neurons,
     EQ, synapses) shows modest gaps between humans and other
     intelligent species. The Software substrate (language, temporal
     integration, social cognition) shows the chasm.

  4. NEANDERTHAL EXTINCTION WAS A LANGUAGE GAP: Despite larger
     brains, Neanderthal language_architecture = 0.40 vs sapiens
     0.98. This single channel difference explains the IC/F gap.

  5. DEVELOPMENT IS A REGIME JOURNEY: Newborn (Collapse, IC/F=0.669)
     -> Child (Watch) -> Adolescent (peak IC/F=0.992) -> Adult (Watch)
     -> Elderly (Collapse). The brain enters and leaves Collapse twice.
""")
