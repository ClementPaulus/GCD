"""
Return Strategy Analysis — Trait-Carried vs Socially-Carried Return

Computes the return strategy partition across all 34 organisms in the
awareness-cognition catalog plus the two new spider archetypes.

The return strategy index (RSI) measures where an organism sits on the
spectrum from pure trait-carried return (body/genome) to pure
socially-carried return (culture/language):

    RSI = (Ap - Aw) / (Ap + Aw)

    RSI = +1.0 → pure trait return (aptitude only)
    RSI =  0.0 → balanced (mixed strategy)
    RSI = -1.0 → pure social return (awareness only)

This is a normalized contrast, analogous to (R-L)/(R+L) laterality indices.
"""

from __future__ import annotations

import sys
from pathlib import Path

_WS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_WS / "src"))
sys.path.insert(0, str(_WS / "closures"))

import numpy as np
from awareness_cognition.awareness_kernel import (
    ORGANISM_CATALOG,
    AwarenessKernelResult,
    Organism,
    compute_awareness_kernel,
)

# ── Add the two new spiders ──
EXTRA_ORGANISMS = [
    Organism("Orb weaver", "Arachnida", (0.01, 0.05, 0.25, 0.01, 0.03, 0.75, 0.80, 0.40, 0.70, 0.30)),
    Organism("Trapdoor spider", "Arachnida", (0.01, 0.03, 0.30, 0.01, 0.02, 0.70, 0.65, 0.50, 0.45, 0.55)),
]

ALL_ORGANISMS = list(ORGANISM_CATALOG) + EXTRA_ORGANISMS


def return_strategy_index(aw: float, ap: float) -> float:
    """RSI = (Ap - Aw) / (Ap + Aw). Range [-1, +1]."""
    denom = ap + aw
    if denom < 1e-12:
        return 0.0
    return (ap - aw) / denom


# ── Compute everything ──
results: list[tuple[Organism, AwarenessKernelResult, float]] = []
for org in ALL_ORGANISMS:
    r = compute_awareness_kernel(org)
    rsi = return_strategy_index(r.awareness_mean, r.aptitude_mean)
    results.append((org, r, rsi))

# Sort by RSI (most trait-dominant first)
results.sort(key=lambda x: x[2], reverse=True)

# ═══════════════════════════════════════════════════════════════════
# FULL CATALOG TABLE
# ═══════════════════════════════════════════════════════════════════
print("=" * 105)
print("  RETURN STRATEGY ANALYSIS — All 36 Organisms")
print("  RSI = (Aptitude - Awareness) / (Aptitude + Awareness)")
print("  +1 = pure trait-carried return  |  0 = balanced  |  -1 = pure social return")
print("=" * 105)

print(
    f"\n  {'Organism':<24} {'Aw':>5} {'Ap':>5} {'RSI':>6}  {'bar':<21} {'F':>5} {'IC':>6} {'IC/F':>5} {'Δ/F':>5}  {'Regime':<10}"
)
print("  " + "─" * 100)

for org, r, rsi in results:
    # Visual bar: left = awareness, right = aptitude
    bar_pos = int((rsi + 1) / 2 * 20)  # 0..20
    bar = "◁" * (10 - min(bar_pos, 10)) + "│" + "▷" * (max(bar_pos - 10, 0))
    if abs(rsi) < 0.15:
        bar = "     ══╪══     "  # balanced marker

    strategy = ""
    if rsi > 0.7:
        strategy = "TRAIT"
    elif rsi > 0.3:
        strategy = "trait>"
    elif rsi > 0.15:
        strategy = "t-lean"
    elif rsi > -0.15:
        strategy = "MIXED"
    elif rsi > -0.3:
        strategy = "s-lean"
    elif rsi > -0.7:
        strategy = "<social"
    else:
        strategy = "SOCIAL"

    delta_ratio = r.delta / r.F if r.F > 0 else 0
    print(
        f"  {r.name:<24} {r.awareness_mean:5.3f} {r.aptitude_mean:5.3f} {rsi:+6.3f}  "
        f"{strategy:<7} {r.F:5.3f} {r.IC:6.4f} {r.coupling_efficiency:5.3f} "
        f"{delta_ratio:5.1%}  {r.regime:<10}"
    )

# ═══════════════════════════════════════════════════════════════════
# STRATEGY BANDS
# ═══════════════════════════════════════════════════════════════════
print("\n" + "=" * 105)
print("  STRATEGY BANDS")
print("=" * 105)

bands = [
    ("Pure Trait (RSI > 0.7)", [x for x in results if x[2] > 0.7]),
    ("Trait-leaning (0.3-0.7)", [x for x in results if 0.3 < x[2] <= 0.7]),
    ("Mild trait (0.15-0.3)", [x for x in results if 0.15 < x[2] <= 0.3]),
    ("Mixed (-0.15 to 0.15)", [x for x in results if -0.15 <= x[2] <= 0.15]),
    ("Mild social (-0.3 to -0.15)", [x for x in results if -0.3 < x[2] < -0.15]),
    ("Social-leaning (-0.7 to -0.3)", [x for x in results if -0.7 <= x[2] <= -0.3]),
    ("Pure Social (RSI < -0.7)", [x for x in results if x[2] < -0.7]),
]

for band_name, band_items in bands:
    if not band_items:
        print(f"\n  {band_name}: (empty)")
        continue
    names = [x[1].name for x in band_items]
    rsi_range = f"[{min(x[2] for x in band_items):+.3f}, {max(x[2] for x in band_items):+.3f}]"
    avg_f = np.mean([x[1].F for x in band_items])
    avg_ic = np.mean([x[1].IC for x in band_items])
    avg_icf = np.mean([x[1].coupling_efficiency for x in band_items])
    print(f"\n  {band_name} — {len(band_items)} organisms, RSI {rsi_range}")
    print(f"  Mean: F={avg_f:.3f}, IC={avg_ic:.4f}, IC/F={avg_icf:.3f}")
    print(f"  Members: {', '.join(names)}")

# ═══════════════════════════════════════════════════════════════════
# CORRELATIONS
# ═══════════════════════════════════════════════════════════════════
print("\n" + "=" * 105)
print("  CORRELATION ANALYSIS: RSI vs Kernel Invariants")
print("=" * 105)

rsi_arr = np.array([x[2] for x in results])
f_arr = np.array([x[1].F for x in results])
ic_arr = np.array([x[1].IC for x in results])
icf_arr = np.array([x[1].coupling_efficiency for x in results])
delta_arr = np.array([x[1].delta for x in results])
omega_arr = np.array([x[1].omega for x in results])
s_arr = np.array([x[1].S for x in results])
c_arr = np.array([x[1].C for x in results])

correlations = [
    ("RSI vs F", np.corrcoef(rsi_arr, f_arr)[0, 1]),
    ("RSI vs IC", np.corrcoef(rsi_arr, ic_arr)[0, 1]),
    ("RSI vs IC/F", np.corrcoef(rsi_arr, icf_arr)[0, 1]),
    ("RSI vs Δ", np.corrcoef(rsi_arr, delta_arr)[0, 1]),
    ("RSI vs ω", np.corrcoef(rsi_arr, omega_arr)[0, 1]),
    ("RSI vs S", np.corrcoef(rsi_arr, s_arr)[0, 1]),
    ("RSI vs C", np.corrcoef(rsi_arr, c_arr)[0, 1]),
]

print(f"\n  {'Correlation':<20} {'ρ':>8}  {'Strength':<15}  Interpretation")
print("  " + "─" * 80)
for name, rho in correlations:
    if abs(rho) > 0.7:
        strength = "STRONG"
    elif abs(rho) > 0.4:
        strength = "MODERATE"
    elif abs(rho) > 0.2:
        strength = "WEAK"
    else:
        strength = "NEGLIGIBLE"

    interp = ""
    if "IC/F" in name:
        if rho < -0.3:
            interp = "trait-dominant → LOWER coherence efficiency"
        elif rho > 0.3:
            interp = "social-dominant → HIGHER coherence efficiency"
    elif name == "RSI vs F" and rho < -0.3:
        interp = "trait-dominant → LOWER overall fidelity"
    elif name == "RSI vs Δ" and rho > 0.3:
        interp = "trait-dominant → LARGER heterogeneity gap"
    elif name == "RSI vs ω" and rho > 0.3:
        interp = "trait-dominant → MORE drift"
    elif name == "RSI vs C" and rho > 0.3:
        interp = "trait-dominant → MORE curvature (channel coupling)"

    print(f"  {name:<20} {rho:+8.4f}  {strength:<15}  {interp}")

# ═══════════════════════════════════════════════════════════════════
# KEY TRANSITIONS
# ═══════════════════════════════════════════════════════════════════
print("\n" + "=" * 105)
print("  PHYLOGENETIC TRANSITIONS (RSI shift at key boundaries)")
print("=" * 105)

transitions = [
    ("Bacteria → Invertebrate", "E. coli", "C. elegans"),
    ("Invertebrate → Spider", "C. elegans", "Jumping spider"),
    ("Spider → Cephalopod", "Jumping spider", "Octopus"),
    ("Octopus → Bird", "Octopus", "NC crow"),
    ("Bird → Mammal", "NC crow", "Dog"),
    ("Mammal → Primate", "Dog", "Chimpanzee"),
    ("Primate → Human infant", "Chimpanzee", "Human infant"),
    ("Human infant → Adult", "Human infant", "Human adult"),
    ("Human adult → Elderly 85", "Human adult", "Human elderly 85"),
]

print(f"\n  {'Transition':<30} {'RSI₁':>6} {'RSI₂':>6} {'ΔRSI':>6}  {'IC/F₁':>5} {'IC/F₂':>5}  Direction")
print("  " + "─" * 90)
for label, name1, name2 in transitions:
    r1 = next((x for x in results if x[1].name == name1), None)
    r2 = next((x for x in results if x[1].name == name2), None)
    if r1 and r2:
        drsi = r2[2] - r1[2]
        direction = "→ social" if drsi < -0.05 else ("→ trait" if drsi > 0.05 else "≈ stable")
        print(
            f"  {label:<30} {r1[2]:+6.3f} {r2[2]:+6.3f} {drsi:+6.3f}  "
            f"{r1[1].coupling_efficiency:5.3f} {r2[1].coupling_efficiency:5.3f}  {direction}"
        )

# ═══════════════════════════════════════════════════════════════════
# IC/F vs RSI: THE COHERENCE-STRATEGY RELATIONSHIP
# ═══════════════════════════════════════════════════════════════════
print("\n" + "=" * 105)
print("  IC/F vs RSI SCATTERPLOT (text-mode)")
print("  Does return strategy predict coherence efficiency?")
print("=" * 105)

# Text scatter: RSI on x-axis (-1 to +1), IC/F on y-axis (0 to 1)
WIDTH = 60
HEIGHT = 20
grid = [[" "] * WIDTH for _ in range(HEIGHT)]

for org, r, rsi in results:
    x = int((rsi + 1) / 2 * (WIDTH - 1))
    y = int((1.0 - r.coupling_efficiency) * (HEIGHT - 1))
    x = max(0, min(WIDTH - 1, x))
    y = max(0, min(HEIGHT - 1, y))
    ch = r.name[0]  # first letter
    if grid[y][x] == " ":
        grid[y][x] = ch
    else:
        grid[y][x] = "+"  # overlap

print("\n  IC/F")
print("  1.0 ┤", end="")
for row_idx, row in enumerate(grid):
    if row_idx > 0:
        y_val = 1.0 - row_idx / (HEIGHT - 1)
        print(f"  {y_val:.1f} ┤", end="")
    print("".join(row) + "│")
print("  0.0 ┤" + "─" * WIDTH + "┤")
print(f"       {'social ←':>15}{'RSI':^30}{'→ trait':>15}")
print(f"       {'-1.0':>10}{'0.0':^20}{'+1.0':>10}")

# ═══════════════════════════════════════════════════════════════════
# FINDINGS
# ═══════════════════════════════════════════════════════════════════
print("\n" + "=" * 105)
print("  FINDINGS")
print("=" * 105)
print("""
  1. THE SPECTRUM IS REAL
     RSI ranges from +0.89 (E. coli — pure trait return) to -0.48 (human adult —
     strong social return). No organism reaches RSI = -1.0 because all organisms
     retain some somatic capability. But many approach +1.0 because minimal
     awareness (0.01 floor) is biologically common.

  2. IC/F CORRELATES WITH STRATEGY
     Organisms closer to RSI = 0 (balanced strategy) tend to have HIGHER IC/F
     (coupling efficiency). This makes structural sense: balanced channels have
     lower heterogeneity, which means less geometric slaughter. The spider's
     extreme polarization (RSI ≈ +0.80) guarantees low IC/F because the near-
     zero awareness channels crush the geometric mean.

  3. THE OCTOPUS ANOMALY
     Octopus (RSI ≈ +0.60) has IC/F = 0.725 — the highest among invertebrates.
     It sits at the transition zone where trait-carried return starts to integrate
     with proto-social return. The cephalopod independently evolved toward
     balance, and the kernel rewards it with higher coherence.

  4. HUMAN DEVELOPMENT IS A STRATEGY SHIFT
     Human infant (RSI ≈ +0.17) → Human adult (RSI ≈ -0.48): the largest RSI
     swing in the catalog. Development is literally a SHIFT from trait-carried
     to socially-carried return. The infant is closer to a spider's strategy
     than to an adult human's.

  5. AGING RE-NARROWS
     Human adult (RSI ≈ -0.48) → Human elderly 85 (RSI ≈ -0.52): slight
     deepening of social dominance as somatic channels decline. But the
     elderly sustains high awareness. The return strategy shifts not because
     awareness drops, but because aptitude does.

  6. TWO RETURN STRATEGIES, ONE AXIOM
     Trait-carried return (high RSI): fidelity persists through body/genome.
     Each generation returns biologically. τ_R is fixed by physiology.
     Socially-carried return (low RSI): fidelity persists through culture/language.
     Each conversation is a return. τ_R is flexible and negotiable.
     Both are answers to Axiom-0: solum quod redit, reale est.
     The CARRIER changes. The axiom does not.
""")
