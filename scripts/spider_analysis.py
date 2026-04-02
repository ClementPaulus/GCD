"""
Spider Awareness Analysis — Kernel Computation

Analyzes the jumping spider (already catalogued) plus two additional spider
types to test the hypothesis: fragile body + high sensory channels + trap
behavior = distinctive kernel signature.
"""

from __future__ import annotations

import sys
from pathlib import Path

_WS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_WS / "src"))
sys.path.insert(0, str(_WS / "closures"))

import numpy as np
from awareness_cognition.awareness_kernel import (
    ALL_CHANNELS,
    ORGANISM_CATALOG,
    Organism,
    compute_awareness_kernel,
)

# ── Three spider archetypes ──
jumping = next(o for o in ORGANISM_CATALOG if o.name == "Jumping spider")

orb_weaver = Organism("Orb weaver", "Arachnida", (0.01, 0.05, 0.25, 0.01, 0.03, 0.75, 0.80, 0.40, 0.70, 0.30))

trapdoor = Organism("Trapdoor spider", "Arachnida", (0.01, 0.03, 0.30, 0.01, 0.02, 0.70, 0.65, 0.50, 0.45, 0.55))

spiders = [jumping, orb_weaver, trapdoor]
results = [compute_awareness_kernel(s) for s in spiders]

# Comparisons
comparisons = []
for name in ["Honeybee", "Octopus", "Mantis shrimp", "NC crow"]:
    org = next(o for o in ORGANISM_CATALOG if o.name == name)
    comparisons.append((org, compute_awareness_kernel(org)))

print("=" * 90)
print("  SPIDER AWARENESS ANALYSIS — Kernel Invariants")
print("  Axiom-0: Collapse is generative; only what returns is real")
print("=" * 90)

print(f"\n{'Organism':<20} {'F':>6} {'IC':>7} {'IC/F':>6} {'Δ':>7} {'ω':>6} {'S':>6} {'C':>6}  {'Regime':<10}")
print("─" * 90)

for r in results:
    print(
        f"  {r.name:<18} {r.F:6.3f} {r.IC:7.4f} {r.coupling_efficiency:6.3f} "
        f"{r.delta:7.4f} {r.omega:6.3f} {r.S:6.3f} {r.C:6.3f}  {r.regime:<10} ◄"
    )
print("  " + "─" * 86)
for org, r in comparisons:
    print(
        f"  {r.name:<18} {r.F:6.3f} {r.IC:7.4f} {r.coupling_efficiency:6.3f} "
        f"{r.delta:7.4f} {r.omega:6.3f} {r.S:6.3f} {r.C:6.3f}  {r.regime:<10}"
    )

# ── Channel profiles ──
print("\n" + "=" * 90)
print("  SPIDER CHANNEL PROFILES (5+5 partition)")
print("=" * 90)

for r, org in zip(results, spiders):
    c = org.trace
    print(f"\n  ── {r.name} ──")
    print("  Awareness subspace (reflective):")
    for i in range(5):
        bar = "█" * int(c[i] * 40)
        print(f"    {ALL_CHANNELS[i]:<25} {c[i]:5.2f}  {bar}")
    print("  Aptitude subspace (somatic):")
    for i in range(5, 10):
        bar = "█" * int(c[i] * 40)
        print(f"    {ALL_CHANNELS[i]:<25} {c[i]:5.2f}  {bar}")
    print(f"  Awareness mean: {r.awareness_mean:.3f}  |  Aptitude mean: {r.aptitude_mean:.3f}")
    print(f"  Subspace gap:   {r.gap:+.3f} ({'awareness > aptitude' if r.gap > 0 else 'aptitude > awareness'})")
    print(f"  Weakest:  {r.weakest_channel}  |  Strongest: {r.strongest_channel}")

# ── Planning / awareness ratio ──
print("\n" + "=" * 90)
print("  PLANNING-TO-AWARENESS RATIO")
print("=" * 90)

print(f"\n  {'Organism':<20} {'plan':>6} {'Aw_mean':>8} {'plan/Aw':>8}  note")
print("  " + "─" * 60)
all_items = [(s, r) for s, r in zip(spiders, results)] + comparisons
for org, r in all_items:
    planning = org.channels[2]
    ratio = planning / r.awareness_mean if r.awareness_mean > 0 else 0
    note = "← plan dominates awareness" if ratio > 3.0 else ""
    spider_mark = " ◄" if "spider" in r.name.lower() or "weaver" in r.name.lower() else ""
    print(f"  {r.name:<20} {planning:6.2f} {r.awareness_mean:8.3f} {ratio:8.2f}  {note}{spider_mark}")

# ── Heterogeneity gap ──
print("\n  HETEROGENEITY GAP DECOMPOSITION:")
print(f"  {'Organism':<20} {'F':>6} {'IC':>7} {'Δ':>7} {'Δ/F':>7}  Interpretation")
print("  " + "─" * 75)
for r in results:
    if r.delta_ratio > 0.5:
        interp = "EXTREME → channel death dominates"
    elif r.delta_ratio > 0.3:
        interp = "HIGH → strong awareness-aptitude split"
    else:
        interp = "MODERATE"
    print(f"  {r.name:<20} {r.F:6.3f} {r.IC:7.4f} {r.delta:7.4f} {r.delta_ratio:7.2%}  {interp}")

# ── κ-sensitivity ──
print("\n  κ-SENSITIVITY (which channels drive integrity):")
for r, org in zip(results, spiders):
    s = r.sensitivity
    sorted_idx = np.argsort(s)[::-1]
    print(f"\n  {r.name}:")
    for idx in sorted_idx[:5]:
        bar = "█" * int(s[idx] / max(np.max(s), 1e-12) * 30)
        print(f"    {ALL_CHANNELS[idx]:<25} κ-sens={s[idx]:.4f}  {bar}")

# ── Tier-1 identity check ──
print("\n" + "=" * 90)
print("  TIER-1 IDENTITY VERIFICATION (all three spiders)")
print("=" * 90)
for r in results:
    f_omega = r.F + r.omega
    ic_exp = np.exp(r.kappa)
    print(f"\n  {r.name}:")
    print(f"    F + ω = {f_omega:.15f}  (must = 1.0)  |F + ω - 1| = {abs(f_omega - 1):.1e}")
    print(f"    IC    = {r.IC:.15f}")
    print(f"    exp(κ)= {ic_exp:.15f}  |IC - exp(κ)| = {abs(r.IC - ic_exp):.1e}")
    print(f"    IC ≤ F: {r.IC:.6f} ≤ {r.F:.6f}  ✓" if r.IC <= r.F else "    IC ≤ F: VIOLATED!")

# ── Verdict ──
print("\n" + "=" * 90)
print("  VERDICT: The Ambush Archetype")
print("=" * 90)
print("""
  The kernel reveals a structural pattern: PREMEDITATION WITHOUT AWARENESS.

  Three signatures distinguishing the spider archetype:

  1. PLANNING DOMINANCE in awareness subspace
     Trapdoor spider: planning = 0.30, awareness mean = 0.074 → ratio 4.1×
     Orb weaver:      planning = 0.25, awareness mean = 0.070 → ratio 3.6×
     Compare NC crow: planning = 0.50, awareness mean = 0.360 → ratio 1.4×
     The crow's planning is integrated with metacognition + social cognition.
     The spider's planning is ISOLATED — the only lit awareness channel.

  2. GEOMETRIC SLAUGHTER within the awareness subspace
     Mirror = 0.01, symbol = 0.01, social = 0.02 → three near-dead channels.
     By §3 (trucidatio geometrica): IC_awareness is obliterated even though
     F_awareness is dragged up by the planning channel.
     The spider has awareness FIDELITY without awareness INTEGRITY.

  3. THE FRAGILITY-SENSOR TRADE
     Low resilience (0.30-0.55) + high sensory (0.70-0.90) = the body is
     expendable but the perceptual apparatus is not. Every encounter must
     count because there will not be many. The web / burrow / ambush stance
     is the structural answer: maximize the quality of each encounter.

  This produces the "ambush archetype": a system that PLANS (builds complex
  structure in anticipation of future events) without KNOWING it plans
  (no self-model, no symbolic representation, no social validation of the plan).

  The 5+5 partition makes this structurally visible. Planning_horizon and
  mirror_recognition are separate channels, and the kernel treats them
  independently. The spider scores high on one and near-zero on the other.
  The heterogeneity gap Δ captures exactly this: the mean looks reasonable,
  but the multiplicative coherence is destroyed.

  Biological conclusion: web construction, trap setting, and 20-year burrow
  occupation are PROCEDURAL planning — sequential motor programs that achieve
  delayed-return outcomes through hardwired behavioral routines, NOT through
  the reflective/representational channels that humans associate with "planning."

  The spider plans without awareness of planning.
  *Praemeditatio sine conscientia praemeditationis.*
""")
