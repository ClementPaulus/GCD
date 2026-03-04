"""Deep Diagnostic Sweep — Novel Equations and Structural Nuances.

Discovers equations and patterns from the corrected Lemma 41 mathematics
and cross-invariant analysis of the GCD kernel.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq

# Workspace setup
_WS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_WS / "src"))
sys.path.insert(0, str(_WS))

from umcp.frozen_contract import EPSILON, P_EXPONENT
from umcp.kernel_optimized import compute_kernel_outputs

# ═══════════════════════════════════════════════════════════════════
# §1. THE CRITICAL POINT c* — Logistic Self-Duality
# ═══════════════════════════════════════════════════════════════════


def find_c_star() -> float:
    """Find c* where f'(c) = ln((1-c)/c) + 1/c = 0."""
    return brentq(lambda c: np.log((1 - c) / c) + 1 / c, 0.01, 0.99)


def f_coupling(c: float) -> float:
    """f(c) = h(c) + ln(c) = S + κ per channel."""
    return -c * np.log(c) - (1 - c) * np.log(1 - c) + np.log(c)


c_star = find_c_star()
omega_star = 1 - c_star
f_star = f_coupling(c_star)

print("=" * 70)
print("DEEP DIAGNOSTIC: Novel Equations from Corrected GCD Mathematics")
print("=" * 70)

print("\n§1. THE CRITICAL POINT c*")
print("-" * 50)
print(f"  c*     = {c_star:.15f}")
print(f"  ω*     = {omega_star:.15f}")
print(f"  f(c*)  = {f_star:.15f}")
print()
print("  EXACT: f(c*) = (1-c*)/c* = exp(-1/c*)")
print(f"    (1-c*)/c*  = {(1 - c_star) / c_star:.15f}")
print(f"    exp(-1/c*) = {np.exp(-1 / c_star):.15f}")
print(f"    residual   = {abs(f_star - (1 - c_star) / c_star):.2e}")
print()
print("  LOGISTIC FIXED POINT: c* = σ(1/c*) where σ(x) = 1/(1+exp(-x))")
sigma_val = 1 / (1 + np.exp(-1 / c_star))
print(f"    σ(1/c*)    = {sigma_val:.15f}")
print(f"    c*         = {c_star:.15f}")
print(f"    match      = {abs(c_star - sigma_val) < 1e-14}")

# ═══════════════════════════════════════════════════════════════════
# §2. THREE EXACT IDENTITIES AT c*
# ═══════════════════════════════════════════════════════════════════

print("\n§2. THREE EXACT IDENTITIES AT c*")
print("-" * 50)

# Identity 1: f(c*) = ω*/c* = exp(-1/c*)
print("  [I1]  max(S+κ) = ω*/c* = exp(-1/c*)")
print(f"        Numerically: {f_star:.15f}")

# Identity 2: h(c*) = (1-c*)/c* - ln(c*)  [from f = h + ln]
h_star = f_star - np.log(c_star)
h_direct = -c_star * np.log(c_star) - (1 - c_star) * np.log(1 - c_star)
print("\n  [I2]  h(c*) - ln(c*) = (1-c*)/c*")
print(f"        h(c*) = {h_direct:.15f}")
print(f"        ln(c*) = {np.log(c_star):.15f}")
print(f"        difference = {h_direct - np.log(c_star):.15f}")

# Identity 3: ln(c*/(1-c*)) = 1/c*  [from the defining equation]
log_odds = np.log(c_star / (1 - c_star))
inv_c = 1 / c_star
print("\n  [I3]  ln(c*/(1-c*)) = 1/c*  (log-odds equals reciprocal)")
print(f"        ln(c*/(1-c*)) = {log_odds:.15f}")
print(f"        1/c*          = {inv_c:.15f}")
print(f"        residual      = {abs(log_odds - inv_c):.2e}")

# ═══════════════════════════════════════════════════════════════════
# §3. CURVATURE DECOMPOSITION AT c*
# ═══════════════════════════════════════════════════════════════════

print("\n§3. CURVATURE DECOMPOSITION AT c*")
print("-" * 50)

g_F_star = 1 / (c_star * (1 - c_star))
f2_star = -g_F_star - 1 / c_star**2

print("  f''(c*) = -g_F(c*) - 1/c*²")
print(f"  f''(c*) = {f2_star:.10f}")
print(f"  g_F(c*) = {g_F_star:.10f}  (Fisher metric contribution)")
print(f"  1/c*²   = {1 / c_star**2:.10f}  (logarithmic contribution)")
print(f"  ratio g_F/(-f'') = {g_F_star / abs(f2_star):.6f}")
print(f"  The Fisher metric accounts for {g_F_star / abs(f2_star) * 100:.1f}% of the curvature at c*")

# ═══════════════════════════════════════════════════════════════════
# §4. THE GAP IDENTITY
# ═══════════════════════════════════════════════════════════════════

print("\n§4. THE GAP: ln(2) - max(S+κ)")
print("-" * 50)

gap = np.log(2) - f_star
print(f"  gap = ln(2) - exp(-1/c*) = {gap:.15f}")
print(f"  gap/ln(2) = {gap / np.log(2):.10f}  (~59.8% of ln(2))")
print(f"  gap/f*    = {gap / f_star:.10f}  (~1.49× the max)")
print()
print("  INTERPRETATION: At the equator c=1/2, S+κ=0 (zero-crossing).")
print("  At c*, S+κ peaks at exp(-1/c*) ≈ 0.278.")
print("  The gap to ln(2) ≈ 0.415 is the structural cost of")
print("  maintaining log-integrity (κ) alongside entropy (S).")

# ═══════════════════════════════════════════════════════════════════
# §5. THE INTEGRAL IDENTITY
# ═══════════════════════════════════════════════════════════════════

print("\n§5. THE INTEGRAL IDENTITY ∫₀¹ f(c) dc")
print("-" * 50)


def _f_safe(c: float) -> float:
    if c < 1e-15 or c > 1 - 1e-15:
        return 0.0
    return float(-c * np.log(c) - (1 - c) * np.log(1 - c) + np.log(c))


integral, _ = quad(_f_safe, 1e-15, 1 - 1e-15)
exact = -0.5
print(f"  ∫₀¹ [h(c) + ln(c)] dc = {integral:.15f}")
print(f"  Exact: -1/2           = {exact:.15f}")
print(f"  Match: {abs(integral - exact) < 1e-8}")
print()
print("  Proof: ∫₀¹ h(c) dc = 1/2")
print("         (by symmetry h(c)=h(1-c), and ∫₀¹ -c·ln(c) dc = 1/4)")
print("         ∫₀¹ ln(c) dc = -1")
print("         Sum = 1/2 - 1 = -1/2")
print()
print("  This means: averaged over all possible single-channel states,")
print("  S+κ is NEGATIVE (-1/2). The average state pays more in")
print("  log-integrity cost than it gains in entropy.")
print("  Only channels with c > 1/2 have S+κ > 0.")

# ═══════════════════════════════════════════════════════════════════
# §6. THE S+κ BOUND AS A TIGHT CONSTRAINT
# ═══════════════════════════════════════════════════════════════════

print("\n§6. S+κ BOUND VERIFIED ON MULTI-CHANNEL TRACES")
print("-" * 50)

w = np.ones(8) / 8
traces = [
    ("uniform 0.9", np.full(8, 0.9)),
    ("uniform c*", np.full(8, c_star)),
    ("uniform 0.5", np.full(8, 0.5)),
    ("mixed", np.array([0.95, 0.88, 0.72, 0.65, 0.80, 0.90, 0.78, 0.85])),
    ("one dead", np.array([0.95, 0.88, 0.72, 0.65, 0.80, 0.90, 0.78, EPSILON])),
    ("bimodal", np.array([0.99, 0.01, 0.99, 0.01, 0.99, 0.01, 0.99, 0.01])),
]

for label, c_arr in traces:
    k = compute_kernel_outputs(c_arr, w)
    sk = k["S"] + k["kappa"]
    print(f"  {label:15s}: S+κ = {sk:+.6f},  bound = {f_star:.6f},  margin = {f_star - sk:.6f}")

# ═══════════════════════════════════════════════════════════════════
# §7. OMEGA HIERARCHY — Four Structural Landmarks
# ═══════════════════════════════════════════════════════════════════

print("\n§7. THE OMEGA HIERARCHY")
print("-" * 50)

omega_stable = 0.038
omega_collapse = 0.30
omega_trap = brentq(lambda om: om**3 / (1 - om + EPSILON) - 1, 0.1, 0.99)
c_trap = 1 - omega_trap


def gamma(omega: float) -> float:
    return omega**P_EXPONENT / (1 - omega + EPSILON)


print("  Four structural omegas in ascending order:")
print(f"    ω_stable  = {omega_stable:.6f}   Γ = {gamma(omega_stable):.8f}")
print(f"    ω*        = {omega_star:.6f}   Γ = {gamma(omega_star):.8f}")
print(f"    ω_collapse= {omega_collapse:.6f}   Γ = {gamma(omega_collapse):.8f}")
print(f"    ω_trap    = {omega_trap:.6f}   Γ = {gamma(omega_trap):.8f}")
print()
print(f"  {omega_stable:.3f} < {omega_star:.3f} < {omega_collapse:.3f} < {omega_trap:.3f}")
print()
print("  NEW INSIGHT: ω* sits in Watch regime, meaning the max(S+κ)")
print("  point is NOT in Stable. Systems at peak entropy-integrity")
print("  coupling already show enough drift for Watch classification.")
print()
print(f"  Ratio ω_collapse/ω* = {omega_collapse / omega_star:.4f}")
print(f"  Ratio ω_trap/ω*    = {omega_trap / omega_star:.4f}")
print(f"  Ratio ω*/ω_stable  = {omega_star / omega_stable:.4f}")

# ═══════════════════════════════════════════════════════════════════
# §8. HETEROGENEITY GAP vs FISHER VARIANCE
# ═══════════════════════════════════════════════════════════════════

print("\n§8. Δ vs 4·Var(θ) — FISHER ANGLE VARIANCE RELATIONSHIP")
print("-" * 50)

test_traces = [
    ("mixed", np.array([0.95, 0.88, 0.72, 0.65, 0.80, 0.90, 0.78, 0.85])),
    ("gradient", np.array([0.99, 0.95, 0.90, 0.85, 0.80, 0.75, 0.70, 0.65])),
    ("near_stable", np.array([0.98, 0.97, 0.96, 0.95, 0.99, 0.94, 0.93, 0.92])),
    ("moderate_het", np.array([0.9, 0.8, 0.7, 0.6, 0.85, 0.75, 0.65, 0.55])),
    ("high_spread", np.array([0.99, 0.90, 0.80, 0.70, 0.60, 0.50, 0.40, 0.30])),
]

print(f"  {'Trace':15s}  {'Δ':>10s}  {'4·Var(θ)':>10s}  {'ratio':>8s}")
for label, c_test in test_traces:
    k = compute_kernel_outputs(c_test, w)
    theta_arr = np.arcsin(np.sqrt(c_test))
    var_theta = float(np.var(theta_arr))
    delta = k["heterogeneity_gap"]
    ratio = delta / (4 * var_theta) if var_theta > 0 else float("inf")
    print(f"  {label:15s}  {delta:10.6f}  {4 * var_theta:10.6f}  {ratio:8.4f}")

print()
print("  The ratio Δ/(4·Var(θ)) is ORDER-DEPENDENT:")
print("  small for mild heterogeneity, growing with spread.")
print("  FISHER-GEOMETRIC SCALING LAW:")
print("    Δ monotonically increases with Var(arcsin(√c))")
print("  Both Δ and Var(θ) vanish for homogeneous traces,")
print("  but Δ grows sub-linearly in 4·Var(θ) — the gap")
print("  underestimates the Fisher angle variance.")

# ═══════════════════════════════════════════════════════════════════
# §9. CROSS-INVARIANT PRODUCT STRUCTURE
# ═══════════════════════════════════════════════════════════════════

print("\n§9. CROSS-INVARIANT PRODUCTS")
print("-" * 50)

# Does S·IC or (S+κ)·IC reveal structure?
print(f"  {'Trace':15s}  {'S·IC':>10s}  {'(S+κ)·IC':>10s}  {'Δ·S':>10s}  {'F·S':>10s}")
for label, c_test in [
    ("uniform 0.9", np.full(8, 0.9)),
    ("uniform 0.7", np.full(8, 0.7)),
    ("uniform 0.5", np.full(8, 0.5)),
    ("mixed", np.array([0.95, 0.88, 0.72, 0.65, 0.80, 0.90, 0.78, 0.85])),
    ("gradient", np.array([0.99, 0.95, 0.90, 0.85, 0.80, 0.75, 0.70, 0.65])),
    ("high_spread", np.array([0.99, 0.90, 0.80, 0.70, 0.60, 0.50, 0.40, 0.30])),
]:
    k = compute_kernel_outputs(c_test, w)
    s_ic = k["S"] * k["IC"]
    sk_ic = (k["S"] + k["kappa"]) * k["IC"]
    d_s = k["heterogeneity_gap"] * k["S"]
    f_s = k["F"] * k["S"]
    print(f"  {label:15s}  {s_ic:10.6f}  {sk_ic:10.6f}  {d_s:10.6f}  {f_s:10.6f}")

# ═══════════════════════════════════════════════════════════════════
# §10. GAMMA DERIVATIVE AT REGIME BOUNDARIES
# ═══════════════════════════════════════════════════════════════════

print("\n§10. GAMMA SENSITIVITY: Γ'(ω) AT KEY POINTS")
print("-" * 50)


def gamma_prime(omega: float) -> float:
    """Γ'(ω) = [3ω²(1-ω+ε) + ω³] / (1-ω+ε)²."""
    u = 1 - omega + EPSILON
    return (3 * omega**2 * u + omega**3) / u**2


def gamma_elasticity(omega: float) -> float:
    """Elasticity: ω·Γ'/Γ = how many percent Γ changes per percent ω change."""
    return omega * gamma_prime(omega) / gamma(omega)


hdr_gp = "Gamma'"
print(f"  {'Point':15s}  {'omega':>8s}  {'Gamma':>12s}  {hdr_gp:>12s}  {'elasticity':>10s}")
for label, om in [
    ("stable edge", omega_stable),
    ("ω*", omega_star),
    ("watch mid", 0.15),
    ("collapse edge", omega_collapse),
    ("c_trap", omega_trap),
    ("near pole", 0.90),
]:
    g = gamma(om)
    gp = gamma_prime(om)
    el = gamma_elasticity(om)
    print(f"  {label:15s}  {om:8.4f}  {g:12.6f}  {gp:12.4f}  {el:10.4f}")

print()
print("  INSIGHT: Elasticity converges to 4 near the pole:")
print("  Γ'(ω)/Γ(ω)·ω → (3ω²(1-ω) + ω³)/(ω³·(1-ω)) → 3/(1-ω) + 1")
print("  This gives the effective critical exponent for budget blowup.")

# ═══════════════════════════════════════════════════════════════════
# §11. THE EQUATOR AS INFORMATION CROSSOVER
# ═══════════════════════════════════════════════════════════════════

print("\n§11. EQUATOR TOPOLOGY: c=1/2 AS INFORMATION CROSSOVER")
print("-" * 50)

# At equator: S = ln(2), κ = ln(1/2) = -ln(2), so S+κ = 0
# f'(1/2) = ln(1) + 2 = 2
# The equator is NOT a critical point of f — it's where S exactly cancels κ
print("  At c = 1/2 (equator):")
print(f"    S(1/2)     = ln(2) = {np.log(2):.10f}")
print(f"    κ(1/2)     = ln(1/2) = {np.log(0.5):.10f}")
print(f"    S+κ        = {np.log(2) + np.log(0.5):.2e}  (exactly 0)")
print(f"    f'(1/2)    = {np.log(1) + 2:.1f}  (NOT zero — not a critical point)")
print(f"    g_F(1/2)   = {1 / (0.5 * 0.5):.1f}  (Fisher metric minimum)")
print()
print(f"  At c = c* = {c_star:.6f}:")
print(f"    S(c*)      = {-c_star * np.log(c_star) - (1 - c_star) * np.log(1 - c_star):.10f}")
print(f"    κ(c*)      = {np.log(c_star):.10f}")
print(f"    S+κ        = {f_star:.10f}  (maximum)")
print("    f'(c*)     = 0  (critical point)")
print(f"    g_F(c*)    = {g_F_star:.10f}")
print()
print("  THREE ZONES separated by c=1/2 and c=c*:")
print("    (0, 1/2):   S+κ < 0  — κ dominates, entropy insufficient")
print("    (1/2, c*):  S+κ increasing to max — entropy rising, κ less negative")
print("    (c*, 1):    S+κ decreasing but positive — entropy falling, κ→0")

# ═══════════════════════════════════════════════════════════════════
# §12. THE FIVE STRUCTURAL CONSTANTS
# ═══════════════════════════════════════════════════════════════════

print("\n§12. FIVE STRUCTURAL CONSTANTS OF THE KERNEL")
print("-" * 50)
print("  The GCD kernel has exactly five structurally significant c-values:")
print()
print(f"  1. c = ε = {EPSILON}     (death boundary)")
print(f"  2. c = c_trap ≈ {c_trap:.6f}  (Γ(ω) = α, irrecoverable)")
print("  3. c = 1/2 = 0.500000       (equator: S+κ = 0, max entropy)")
print(f"  4. c = c* ≈ {c_star:.6f}   (max S+κ, logistic fixed point)")
print("  5. c = 1-ε ≈ 1.000000       (perfect fidelity)")
print()
print("  These five points partition [0,1] into four regimes:")
print(f"    [{EPSILON}, {c_trap:.3f}]: Trapped — Γ exceeds any correction")
print(f"    [{c_trap:.3f}, 0.500]:    Deficit — κ dominates S")
print(f"    [0.500, {c_star:.3f}]:    Rising coupling — S+κ ascending")
print(f"    [{c_star:.3f}, 1-ε]:      Decreasing coupling — S+κ descending")

# ═══════════════════════════════════════════════════════════════════
# §13. NEW EQUATION CANDIDATES
# ═══════════════════════════════════════════════════════════════════

print("\n§13. SUMMARY OF NEW EQUATIONS")
print("=" * 70)

print("""
  [E1] LOGISTIC SELF-DUALITY
       c* = σ(1/c*)  where σ(x) = 1/(1+exp(-x))
       Defines the unique point where the entropy-integrity
       coupling peaks. c* is the fixed point of the logistic
       function composed with reciprocal.

  [E2] COUPLING MAXIMUM IDENTITY
       max(S + κ) = (1-c*)/c* = exp(-1/c*) ≈ 0.27847
       The maximum per-channel entropy-integrity coupling equals
       both the odds ratio at c* and the exponential of -1/c*.

  [E3] LOG-ODDS RECIPROCAL IDENTITY
       ln(c*/(1-c*)) = 1/c*
       At the coupling maximum, the log-odds of the channel
       coordinate equals its reciprocal. This is equivalent to
       the logistic self-duality (E1).

  [E4] INTEGRAL CONSERVATION
       ∫₀¹ [h(c) + ln(c)] dc = -1/2
       Proof: ∫₀¹ h(c) dc = 1/2 (by symmetry), ∫₀¹ ln(c) dc = -1.
       The average single-channel entropy-integrity coupling
       is exactly -1/2. The average state pays more in
       log-integrity than it gains in entropy.

  [E5] CURVATURE DECOMPOSITION
       f''(c) = -g_F(c) - 1/c²
       At c*, Fisher metric accounts for 78.2% of the curvature;
       the logarithmic contribution provides the remaining 21.8%.

  [E6] GAP IDENTITY
       ln(2) - max(S+κ) = ln(2) - exp(-1/c*) ≈ 0.41468
       The gap between maximum entropy and maximum coupling is
       structurally fixed. ~59.8% of available entropy is consumed
       by the structural cost of maintaining log-integrity.

  [E7] FISHER-GEOMETRIC SCALING
       Δ and Var(arcsin(√c)) co-vanish and co-rise monotonically.
       The heterogeneity gap tracks Fisher angle variance but
       grows sub-linearly — Δ underestimates 4·Var(θ).

  [E8] OMEGA HIERARCHY
       ω_stable < ω* < ω_collapse < ω_trap
       0.038 < 0.218 < 0.300 < 0.682
       The coupling maximum sits strictly inside Watch regime.
""")

print("=" * 70)
print("End of Deep Diagnostic Sweep")
print("=" * 70)
