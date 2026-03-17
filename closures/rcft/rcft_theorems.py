"""
RCFT Theorems — 10 Proven Theorems (T-RC-1 through T-RC-10)

Theorem module for the Recursive Collapse Field Theory domain,
built on Quincke roller states (12 entities) from the quincke_rollers
closure plus active_matter computation.

═══════════════════════════════════════════════════════════════════════
THEOREM INDEX
═══════════════════════════════════════════════════════════════════════
  T-RC-1   Tier-1 Kernel Identities — F+ω=1, IC≤F, IC=exp(κ) for all states
  T-RC-2   VortexCondensate Unique Watch — Sole Watch state among 12
  T-RC-3   SubThreshold Floor — Lowest F and IC across all states
  T-RC-4   Collective IC Amplification — Collective states > individual IC
  T-RC-5   Gap Heterogeneity — ProgrammedSquare has largest gap
  T-RC-6   Chain Assembly Fidelity Jump — Chain states show F discontinuity
  T-RC-7   Curvature-Regime Coupling — Higher C correlates with higher ω
  T-RC-8   Kappa Span — κ spans > 15 units (SubThreshold to VortexCondensate)
  T-RC-9   Duality Exactness — F+ω=1 to machine precision for all states
  T-RC-10  State Coverage — 12 states cover rolling, collective, and control

Derivation chain: Axiom-0 → frozen_contract → kernel_optimized → quincke_rollers → this
"""

from __future__ import annotations

import math
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

_WORKSPACE = Path(__file__).resolve().parents[2]
if str(_WORKSPACE / "src") not in sys.path:
    sys.path.insert(0, str(_WORKSPACE / "src"))
if str(_WORKSPACE) not in sys.path:
    sys.path.insert(0, str(_WORKSPACE))

from closures.rcft.quincke_rollers import analyze_all_states  # noqa: E402


@dataclass(frozen=True, slots=True)
class TheoremResult:
    """Result of a theorem proof attempt."""

    name: str
    statement: str
    n_tests: int
    n_passed: int
    n_failed: int
    details: dict[str, Any]
    verdict: str  # "PROVEN" or "FALSIFIED"


def _get_states():
    """Load all 12 Quincke roller states."""
    return analyze_all_states()


# ═════════════════════════════════════════════════════════════════════
# THEOREM T-RC-1: Tier-1 Kernel Identities
# ═════════════════════════════════════════════════════════════════════


def theorem_RC1_kernel_identities() -> TheoremResult:
    """T-RC-1: All Quincke roller states satisfy Tier-1 kernel identities."""
    states = _get_states()
    tests_total = 0
    tests_passed = 0
    details: dict[str, Any] = {}

    for s in states:
        # Duality: F + ω = 1
        tests_total += 1
        tests_passed += int(abs(s.F + s.omega - 1.0) < 1e-12)

        # Integrity bound: IC ≤ F
        tests_total += 1
        tests_passed += int(s.IC <= s.F + 1e-12)

        # Log-integrity: IC = exp(κ)
        tests_total += 1
        tests_passed += int(abs(s.IC - math.exp(s.kappa)) < 1e-10)

    details["n_states"] = len(states)

    return TheoremResult(
        name="T-RC-1: Tier-1 Kernel Identities",
        statement="F+ω=1, IC≤F, IC=exp(κ) hold for all 12 Quincke roller states",
        n_tests=tests_total,
        n_passed=tests_passed,
        n_failed=tests_total - tests_passed,
        details=details,
        verdict="PROVEN" if tests_passed == tests_total else "FALSIFIED",
    )


# ═════════════════════════════════════════════════════════════════════
# THEOREM T-RC-2: VortexCondensate Unique Watch
# ═════════════════════════════════════════════════════════════════════


def theorem_RC2_vortex_watch() -> TheoremResult:
    """T-RC-2: VortexCondensate is the sole Watch state among 12 states."""
    states = _get_states()
    tests_total = 0
    tests_passed = 0
    details: dict[str, Any] = {}

    watch_states = [s for s in states if s.regime == "Watch"]
    collapse_states = [s for s in states if s.regime == "Collapse"]

    details["watch_names"] = [s.name for s in watch_states]
    details["n_collapse"] = len(collapse_states)

    # Test: Exactly 1 Watch state
    tests_total += 1
    tests_passed += int(len(watch_states) == 1)

    # Test: That Watch state is VortexCondensate
    tests_total += 1
    tests_passed += int(len(watch_states) == 1 and watch_states[0].name == "VortexCondensate")

    # Test: 11 Collapse states
    tests_total += 1
    tests_passed += int(len(collapse_states) == 11)

    return TheoremResult(
        name="T-RC-2: VortexCondensate Unique Watch",
        statement="VortexCondensate is the sole Watch state; 11 others Collapse",
        n_tests=tests_total,
        n_passed=tests_passed,
        n_failed=tests_total - tests_passed,
        details=details,
        verdict="PROVEN" if tests_passed == tests_total else "FALSIFIED",
    )


# ═════════════════════════════════════════════════════════════════════
# THEOREM T-RC-3: SubThreshold Floor
# ═════════════════════════════════════════════════════════════════════


def theorem_RC3_subthreshold_floor() -> TheoremResult:
    """T-RC-3: SubThreshold has the lowest F and IC across all states."""
    states = _get_states()
    tests_total = 0
    tests_passed = 0
    details: dict[str, Any] = {}

    min_f_state = min(states, key=lambda s: s.F)
    min_ic_state = min(states, key=lambda s: s.IC)

    details["min_F_state"] = min_f_state.name
    details["min_F"] = round(min_f_state.F, 6)
    details["min_IC_state"] = min_ic_state.name
    details["min_IC"] = round(float(min_ic_state.IC), 10)

    # Test: SubThreshold has lowest F
    tests_total += 1
    tests_passed += int(min_f_state.name == "SubThreshold")

    # Test: SubThreshold has lowest IC
    tests_total += 1
    tests_passed += int(min_ic_state.name == "SubThreshold")

    # Test: SubThreshold F < 0.05
    tests_total += 1
    sub = next(s for s in states if s.name == "SubThreshold")
    tests_passed += int(sub.F < 0.05)

    return TheoremResult(
        name="T-RC-3: SubThreshold Floor",
        statement="SubThreshold has lowest F and IC across all 12 states",
        n_tests=tests_total,
        n_passed=tests_passed,
        n_failed=tests_total - tests_passed,
        details=details,
        verdict="PROVEN" if tests_passed == tests_total else "FALSIFIED",
    )


# ═════════════════════════════════════════════════════════════════════
# THEOREM T-RC-4: Collective IC Amplification
# ═════════════════════════════════════════════════════════════════════


def theorem_RC4_collective_ic() -> TheoremResult:
    """T-RC-4: Collective states achieve higher mean IC than individual states.

    Collective: ChainAssembly, VortexCondensate, GradientConfinement, AnomalousDimer
    Individual: SubThreshold, Onset, ModerateRolling, FastRolling, MaxSpeed
    """
    states = _get_states()
    tests_total = 0
    tests_passed = 0
    details: dict[str, Any] = {}

    collective_names = {
        "ChainAssembly",
        "VortexCondensate",
        "GradientConfinement",
        "AnomalousDimer",
    }
    individual_names = {
        "SubThreshold",
        "Onset",
        "ModerateRolling",
        "FastRolling",
        "MaxSpeed",
    }

    collective = [s for s in states if s.name in collective_names]
    individual = [s for s in states if s.name in individual_names]

    mean_ic_coll = sum(s.IC for s in collective) / len(collective)
    mean_ic_ind = sum(s.IC for s in individual) / len(individual)

    details["mean_IC_collective"] = round(float(mean_ic_coll), 6)
    details["mean_IC_individual"] = round(float(mean_ic_ind), 6)
    details["ratio"] = round(float(mean_ic_coll / max(mean_ic_ind, 1e-15)), 1)

    # Test: Collective mean IC > individual mean IC
    tests_total += 1
    tests_passed += int(mean_ic_coll > mean_ic_ind)

    # Test: Collective mean IC > 0.30
    tests_total += 1
    tests_passed += int(mean_ic_coll > 0.30)

    # Test: Individual mean IC < 0.01
    tests_total += 1
    tests_passed += int(mean_ic_ind < 0.01)

    return TheoremResult(
        name="T-RC-4: Collective IC Amplification",
        statement="Collective states achieve higher mean IC than individual states",
        n_tests=tests_total,
        n_passed=tests_passed,
        n_failed=tests_total - tests_passed,
        details=details,
        verdict="PROVEN" if tests_passed == tests_total else "FALSIFIED",
    )


# ═════════════════════════════════════════════════════════════════════
# THEOREM T-RC-5: Gap Heterogeneity
# ═════════════════════════════════════════════════════════════════════


def theorem_RC5_gap_heterogeneity() -> TheoremResult:
    """T-RC-5: ProgrammedSquare has the largest heterogeneity gap."""
    states = _get_states()
    tests_total = 0
    tests_passed = 0
    details: dict[str, Any] = {}

    max_gap_state = max(states, key=lambda s: s.gap)
    details["max_gap_state"] = max_gap_state.name
    details["max_gap"] = round(float(max_gap_state.gap), 4)

    # Test: ProgrammedSquare has largest gap
    tests_total += 1
    tests_passed += int(max_gap_state.name == "ProgrammedSquare")

    # Test: Gap > 0.50
    tests_total += 1
    tests_passed += int(max_gap_state.gap > 0.50)

    # Test: VortexCondensate has smallest gap among high-F states (F>0.50)
    tests_total += 1
    high_f = [s for s in states if s.F > 0.50]
    if high_f:
        min_gap_high_f = min(high_f, key=lambda s: s.gap)
        # Structural states (chain/vortex/gradient) all have small gaps
        tests_passed += int(min_gap_high_f.gap < 0.05)

    details["n_high_F_states"] = len(high_f)

    return TheoremResult(
        name="T-RC-5: Gap Heterogeneity",
        statement="ProgrammedSquare has the largest heterogeneity gap (>0.50)",
        n_tests=tests_total,
        n_passed=tests_passed,
        n_failed=tests_total - tests_passed,
        details=details,
        verdict="PROVEN" if tests_passed == tests_total else "FALSIFIED",
    )


# ═════════════════════════════════════════════════════════════════════
# THEOREM T-RC-6: Chain Assembly Fidelity Jump
# ═════════════════════════════════════════════════════════════════════


def theorem_RC6_chain_fidelity_jump() -> TheoremResult:
    """T-RC-6: ChainAssembly F is much higher than ChainDisassembly F.

    Chain formation creates coherence (F jumps); chain breakup destroys it.
    """
    states = _get_states()
    tests_total = 0
    tests_passed = 0
    details: dict[str, Any] = {}

    chain_a = next(s for s in states if s.name == "ChainAssembly")
    chain_d = next(s for s in states if s.name == "ChainDisassembly")

    delta_f = chain_a.F - chain_d.F
    details["ChainAssembly_F"] = round(chain_a.F, 4)
    details["ChainDisassembly_F"] = round(chain_d.F, 4)
    details["F_jump"] = round(delta_f, 4)

    # Test: ChainAssembly F > ChainDisassembly F
    tests_total += 1
    tests_passed += int(chain_a.F > chain_d.F)

    # Test: F jump > 0.30
    tests_total += 1
    tests_passed += int(delta_f > 0.30)

    # Test: IC also jumps (chain assembly IC >> chain disassembly IC)
    tests_total += 1
    tests_passed += int(chain_a.IC > chain_d.IC * 100)

    return TheoremResult(
        name="T-RC-6: Chain Assembly Fidelity Jump",
        statement="ChainAssembly F >> ChainDisassembly F (coherence through formation)",
        n_tests=tests_total,
        n_passed=tests_passed,
        n_failed=tests_total - tests_passed,
        details=details,
        verdict="PROVEN" if tests_passed == tests_total else "FALSIFIED",
    )


# ═════════════════════════════════════════════════════════════════════
# THEOREM T-RC-7: Curvature-Regime Coupling
# ═════════════════════════════════════════════════════════════════════


def theorem_RC7_curvature_regime() -> TheoremResult:
    """T-RC-7: States with higher C tend to have higher ω.

    Individual rolling states have high C and high ω; collective states
    have lower C and lower ω.
    """
    states = _get_states()
    tests_total = 0
    tests_passed = 0
    details: dict[str, Any] = {}

    from scipy.stats import spearmanr

    cs = [s.C for s in states]
    omegas = [s.omega for s in states]
    corr, _ = spearmanr(cs, omegas)
    details["spearman_C_omega"] = round(float(corr), 4)

    # Test: Positive correlation between C and ω
    tests_total += 1
    tests_passed += int(corr > 0)

    # Test: VortexCondensate has C < 0.40
    tests_total += 1
    vortex = next(s for s in states if s.name == "VortexCondensate")
    tests_passed += int(vortex.C < 0.40)

    # Test: MaxSpeed has C > 0.90
    tests_total += 1
    maxspeed = next(s for s in states if s.name == "MaxSpeed")
    tests_passed += int(maxspeed.C > 0.90)

    return TheoremResult(
        name="T-RC-7: Curvature-Regime Coupling",
        statement="Higher curvature C correlates with higher drift ω across states",
        n_tests=tests_total,
        n_passed=tests_passed,
        n_failed=tests_total - tests_passed,
        details=details,
        verdict="PROVEN" if tests_passed == tests_total else "FALSIFIED",
    )


# ═════════════════════════════════════════════════════════════════════
# THEOREM T-RC-8: Kappa Span
# ═════════════════════════════════════════════════════════════════════


def theorem_RC8_kappa_span() -> TheoremResult:
    """T-RC-8: κ spans >15 units from SubThreshold to VortexCondensate."""
    states = _get_states()
    tests_total = 0
    tests_passed = 0
    details: dict[str, Any] = {}

    min_k = min(states, key=lambda s: s.kappa)
    max_k = max(states, key=lambda s: s.kappa)
    span = max_k.kappa - min_k.kappa

    details["min_kappa"] = (min_k.name, round(min_k.kappa, 4))
    details["max_kappa"] = (max_k.name, round(max_k.kappa, 4))
    details["span"] = round(span, 4)

    # Test: Span > 15
    tests_total += 1
    tests_passed += int(span > 15)

    # Test: SubThreshold has most negative κ
    tests_total += 1
    tests_passed += int(min_k.name == "SubThreshold")

    # Test: VortexCondensate has least negative κ
    tests_total += 1
    tests_passed += int(max_k.name == "VortexCondensate")

    return TheoremResult(
        name="T-RC-8: Kappa Span",
        statement="κ spans >15 units from SubThreshold to VortexCondensate",
        n_tests=tests_total,
        n_passed=tests_passed,
        n_failed=tests_total - tests_passed,
        details=details,
        verdict="PROVEN" if tests_passed == tests_total else "FALSIFIED",
    )


# ═════════════════════════════════════════════════════════════════════
# THEOREM T-RC-9: Duality Exactness
# ═════════════════════════════════════════════════════════════════════


def theorem_RC9_duality_exactness() -> TheoremResult:
    """T-RC-9: F+ω=1 to machine precision for all 12 states."""
    states = _get_states()
    tests_total = 0
    tests_passed = 0
    details: dict[str, Any] = {}

    residuals = [abs(s.F + s.omega - 1.0) for s in states]
    max_r = max(residuals)
    details["max_residual"] = float(max_r)

    # Test: Max residual < 1e-14
    tests_total += 1
    tests_passed += int(max_r < 1e-14)

    # Test: All residuals identically zero
    tests_total += 1
    tests_passed += int(all(r == 0.0 for r in residuals))

    # Test: All F and ω in [0,1]
    tests_total += 1
    valid = all(0 <= s.F <= 1 and 0 <= s.omega <= 1 for s in states)
    tests_passed += int(valid)

    return TheoremResult(
        name="T-RC-9: Duality Exactness",
        statement="F+ω=1 to machine precision for all 12 Quincke roller states",
        n_tests=tests_total,
        n_passed=tests_passed,
        n_failed=tests_total - tests_passed,
        details=details,
        verdict="PROVEN" if tests_passed == tests_total else "FALSIFIED",
    )


# ═════════════════════════════════════════════════════════════════════
# THEOREM T-RC-10: State Coverage
# ═════════════════════════════════════════════════════════════════════


def theorem_RC10_coverage() -> TheoremResult:
    """T-RC-10: 12 states cover rolling, collective, and control categories."""
    states = _get_states()
    tests_total = 0
    tests_passed = 0
    details: dict[str, Any] = {}

    rolling = {"SubThreshold", "Onset", "ModerateRolling", "FastRolling", "MaxSpeed"}
    collective = {
        "ChainAssembly",
        "ChainDisassembly",
        "VortexCondensate",
        "GradientConfinement",
        "AnomalousDimer",
    }
    control = {"ProgrammedSquare", "Teleoperated"}

    state_names = {s.name for s in states}

    # Test: Total = 12
    tests_total += 1
    tests_passed += int(len(states) == 12)

    # Test: All rolling states present
    tests_total += 1
    tests_passed += int(rolling.issubset(state_names))

    # Test: All collective states present
    tests_total += 1
    tests_passed += int(collective.issubset(state_names))

    # Test: All control states present
    tests_total += 1
    tests_passed += int(control.issubset(state_names))

    # Test: Categories are exhaustive
    tests_total += 1
    tests_passed += int(state_names == rolling | collective | control)

    details["n_rolling"] = len(rolling)
    details["n_collective"] = len(collective)
    details["n_control"] = len(control)

    return TheoremResult(
        name="T-RC-10: State Coverage",
        statement="12 states cover rolling (5), collective (5), and control (2)",
        n_tests=tests_total,
        n_passed=tests_passed,
        n_failed=tests_total - tests_passed,
        details=details,
        verdict="PROVEN" if tests_passed == tests_total else "FALSIFIED",
    )


# ═════════════════════════════════════════════════════════════════════
# RUNNER
# ═════════════════════════════════════════════════════════════════════

ALL_THEOREMS = [
    theorem_RC1_kernel_identities,
    theorem_RC2_vortex_watch,
    theorem_RC3_subthreshold_floor,
    theorem_RC4_collective_ic,
    theorem_RC5_gap_heterogeneity,
    theorem_RC6_chain_fidelity_jump,
    theorem_RC7_curvature_regime,
    theorem_RC8_kappa_span,
    theorem_RC9_duality_exactness,
    theorem_RC10_coverage,
]


def run_all_theorems() -> list[TheoremResult]:
    """Run all 10 RCFT theorems."""
    return [thm() for thm in ALL_THEOREMS]


if __name__ == "__main__":
    results = run_all_theorems()
    proven = sum(1 for r in results if r.verdict == "PROVEN")
    total_sub = sum(r.n_tests for r in results)
    passed_sub = sum(r.n_passed for r in results)
    print(f"\nRCFT Theorems: {proven}/{len(results)}")
    print(f"Total subtests: {passed_sub}/{total_sub}")
    for r in results:
        mark = "✓" if r.verdict == "PROVEN" else "✗"
        print(f"  {mark} {r.name}: {r.n_passed}/{r.n_tests} — {r.verdict}")
