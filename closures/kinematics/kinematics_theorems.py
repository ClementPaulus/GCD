"""Kinematics domain theorems (T-KN-1 through T-KN-10).

Computation-based theorems testing physics conservation laws, phase space
properties, stability analysis, and regime classification across the full
kinematics closure suite.

Theorem index
─────────────
  T-KN-1  Elastic Conservation Law
  T-KN-2  Energy Additivity
  T-KN-3  Work-Energy Theorem
  T-KN-4  Energy Conservation Detection
  T-KN-5  Oscillation Classification
  T-KN-6  Stability Ordering
  T-KN-7  Stability Trend Detection
  T-KN-8  Motion Regime Classification
  T-KN-9  Phase Space Geometry
  T-KN-10 Cross-Module Consistency Chain
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True, slots=True)
class TheoremResult:
    name: str
    statement: str
    n_tests: int
    n_passed: int
    n_failed: int
    details: dict
    verdict: str


# ── T-KN-1: Elastic Conservation Law ──────────────────────────────


def prove_elastic_conservation() -> TheoremResult:
    """All elastic collisions conserve momentum AND energy."""
    from closures.kinematics.momentum_dynamics import compute_collision_1d

    scenarios = [
        (1.0, 2.0, 1.0, 0.0),
        (2.0, 3.0, 1.0, 0.0),
        (1.0, 5.0, 1.0, -5.0),
        (0.5, 1.0, 2.0, 0.5),
        (3.0, 2.0, 2.0, 1.0),
    ]
    passed = 0
    for m1, v1, m2, v2 in scenarios:
        r = compute_collision_1d(m1, v1, m2, v2, "elastic")
        if r["momentum_conserved"] and r["energy_conserved"]:
            passed += 1
    return TheoremResult(
        name="T-KN-1",
        statement="Elastic collisions conserve both momentum and energy",
        n_tests=len(scenarios),
        n_passed=passed,
        n_failed=len(scenarios) - passed,
        details={"n_scenarios": len(scenarios)},
        verdict="PROVEN" if passed == len(scenarios) else "FAILED",
    )


# ── T-KN-2: Energy Additivity ─────────────────────────────────────


def prove_energy_additivity() -> TheoremResult:
    """E_mechanical = E_kinetic + E_potential to machine precision."""
    from closures.kinematics.energy_mechanics import compute_mechanical_energy

    test_cases = [
        (0.0, 0.0),
        (1.0, 0.0),
        (0.0, 1.0),
        (3.0, 4.0),
        (10.0, 20.0),
        (0.5, 0.5),
        (100.0, 0.0),
        (0.0, 100.0),
        (7.0, 3.0),
        (1.0, 1.0),
    ]
    passed = 0
    max_err = 0.0
    for v, h in test_cases:
        r = compute_mechanical_energy(float(v), float(h))
        err = abs(r["E_mechanical"] - r["E_kinetic"] - r["E_potential"])
        max_err = max(max_err, err)
        if err < 1e-12:
            passed += 1
    return TheoremResult(
        name="T-KN-2",
        statement="Mechanical energy equals kinetic plus potential to machine precision",
        n_tests=len(test_cases),
        n_passed=passed,
        n_failed=len(test_cases) - passed,
        details={"max_error": max_err},
        verdict="PROVEN" if passed == len(test_cases) else "FAILED",
    )


# ── T-KN-3: Work-Energy Theorem ───────────────────────────────────


def prove_work_energy_theorem() -> TheoremResult:
    """Work-energy theorem: valid when W_net = ΔKE, invalid otherwise."""
    from closures.kinematics.energy_mechanics import verify_work_energy_theorem

    tests = [
        # (W_net, KE_i, KE_f, expected_valid)
        (5.0, 10.0, 15.0, True),
        (0.0, 5.0, 5.0, True),
        (10.0, 0.0, 10.0, True),
        (-3.0, 8.0, 5.0, True),
        (5.0, 10.0, 20.0, False),
        (1.0, 0.0, 0.0, False),
        (0.0, 0.0, 5.0, False),
    ]
    passed = 0
    for w, ki, kf, expected in tests:
        r = verify_work_energy_theorem(w, ki, kf, tol=0.01)
        if r["is_valid"] == expected:
            passed += 1
    return TheoremResult(
        name="T-KN-3",
        statement="Work-energy theorem correctly validates W_net = delta_KE",
        n_tests=len(tests),
        n_passed=passed,
        n_failed=len(tests) - passed,
        details={"n_valid_cases": sum(1 for *_, e in tests if e)},
        verdict="PROVEN" if passed == len(tests) else "FAILED",
    )


# ── T-KN-4: Energy Conservation Detection ─────────────────────────


def prove_energy_conservation_detection() -> TheoremResult:
    """Conservation detector: constant series → conserved, decaying → not."""
    from closures.kinematics.energy_mechanics import verify_energy_conservation

    tests_pass = 0
    n_tests = 0

    # Perfectly conserved series
    for val in [1.0, 0.5, 10.0]:
        n_tests += 1
        r = verify_energy_conservation(np.full(20, val), tol=0.01)
        if r["is_conserved"]:
            tests_pass += 1

    # Decaying series — not conserved
    for decay in [0.95, 0.90, 0.80]:
        n_tests += 1
        series = np.array([10.0 * decay**i for i in range(20)])
        r = verify_energy_conservation(series, tol=0.01)
        if not r["is_conserved"]:
            tests_pass += 1

    # Noisy but bounded series
    n_tests += 1
    rng = np.random.RandomState(42)
    noisy = 5.0 + rng.normal(0, 0.001, 50)
    r = verify_energy_conservation(noisy, tol=0.01)
    if r["is_conserved"]:
        tests_pass += 1

    return TheoremResult(
        name="T-KN-4",
        statement="Energy conservation detection distinguishes conserved from dissipative",
        n_tests=n_tests,
        n_passed=tests_pass,
        n_failed=n_tests - tests_pass,
        details={},
        verdict="PROVEN" if tests_pass == n_tests else "FAILED",
    )


# ── T-KN-5: Oscillation Classification ────────────────────────────


def prove_oscillation_classification() -> TheoremResult:
    """Sinusoidal → oscillatory; linear/constant → Non_Oscillatory."""
    from closures.kinematics.phase_space_return import detect_oscillation

    n_tests = 0
    passed = 0

    # Sinusoidal inputs ≠ Non_Oscillatory
    for freq in [1, 2, 4]:
        t = np.linspace(0, 4 * np.pi, 100)
        x = np.sin(freq * t)
        v = freq * np.cos(freq * t)
        r = detect_oscillation(x, v)
        n_tests += 1
        if r["oscillation_type"] != "Non_Oscillatory":
            passed += 1

    # Linear → Non_Oscillatory
    x_lin = np.linspace(0, 10, 100)
    v_const = np.ones(100) * 0.5
    r = detect_oscillation(x_lin, v_const)
    n_tests += 1
    if r["oscillation_type"] == "Non_Oscillatory":
        passed += 1

    # Constant → Non_Oscillatory
    x_const = np.ones(100) * 3.0
    v_zero = np.zeros(100)
    r = detect_oscillation(x_const, v_zero)
    n_tests += 1
    if r["oscillation_type"] == "Non_Oscillatory":
        passed += 1

    # Oscillatory should have sign_changes > 0
    t2 = np.linspace(0, 4 * np.pi, 100)
    r2 = detect_oscillation(np.sin(t2), np.cos(t2))
    n_tests += 1
    if r2["sign_changes"] > 0:
        passed += 1

    return TheoremResult(
        name="T-KN-5",
        statement="Oscillation classification separates periodic from monotone motion",
        n_tests=n_tests,
        n_passed=passed,
        n_failed=n_tests - passed,
        details={},
        verdict="PROVEN" if passed == n_tests else "FAILED",
    )


# ── T-KN-6: Stability Ordering ────────────────────────────────────


def prove_stability_ordering() -> TheoremResult:
    """Tighter trajectories have higher K_stability than wider ones."""
    from closures.kinematics.kinematic_stability import compute_kinematic_stability

    n_tests = 0
    passed = 0

    # Generate pairs: tight vs wide
    pairs = [
        (
            np.array([1.0, 1.01, 0.99, 1.0, 1.01]),
            np.array([0.5, 0.51, 0.49, 0.50, 0.51]),
            np.array([0.0, 5.0, -3.0, 8.0, -1.0]),
            np.array([0.0, 3.0, -2.0, 5.0, -4.0]),
        ),
        (
            np.array([2.0, 2.02, 1.98, 2.01, 1.99]),
            np.array([1.0, 1.01, 0.99, 1.0, 1.01]),
            np.array([0.0, 10.0, -5.0, 15.0, -8.0]),
            np.array([0.0, 8.0, -4.0, 12.0, -6.0]),
        ),
    ]
    k_values = []
    for x_tight, v_tight, x_wide, v_wide in pairs:
        r_tight = compute_kinematic_stability(x_tight, v_tight)
        r_wide = compute_kinematic_stability(x_wide, v_wide)
        n_tests += 1
        k_values.append((r_tight["K_stability"], r_wide["K_stability"]))
        if r_tight["K_stability"] > r_wide["K_stability"]:
            passed += 1

    # Tight should be 'Stable', wide should be 'Unstable'
    r_t = compute_kinematic_stability(
        np.array([1.0, 1.01, 0.99, 1.0, 1.01]),
        np.array([0.5, 0.51, 0.49, 0.50, 0.51]),
    )
    r_w = compute_kinematic_stability(
        np.array([0.0, 5.0, -3.0, 8.0, -1.0]),
        np.array([0.0, 3.0, -2.0, 5.0, -4.0]),
    )
    n_tests += 1
    if r_t["regime"] == "Stable" and r_w["regime"] == "Unstable":
        passed += 1

    return TheoremResult(
        name="T-KN-6",
        statement="Tight trajectories yield higher K_stability than spread trajectories",
        n_tests=n_tests,
        n_passed=passed,
        n_failed=n_tests - passed,
        details={"K_pairs": k_values},
        verdict="PROVEN" if passed == n_tests else "FAILED",
    )


# ── T-KN-7: Stability Trend Detection ─────────────────────────────


def prove_stability_trend() -> TheoremResult:
    """Monotone K series correctly classified as Degrading/Improving/Stable."""
    from closures.kinematics.kinematic_stability import compute_stability_trend

    tests = [
        (np.array([0.9, 0.85, 0.80, 0.75, 0.70]), "Degrading"),
        (np.array([0.5, 0.55, 0.60, 0.65, 0.70]), "Improving"),
        (np.array([0.8, 0.8, 0.8, 0.8, 0.8]), "Stable"),
        (np.array([0.95, 0.90, 0.85, 0.80, 0.75, 0.70, 0.65]), "Degrading"),
        (np.array([0.3, 0.4, 0.5, 0.6, 0.7, 0.8]), "Improving"),
    ]
    passed = 0
    for k_series, expected in tests:
        r = compute_stability_trend(k_series)
        if r["trend_direction"] == expected:
            passed += 1

    # Degrading slope should be negative
    r_deg = compute_stability_trend(np.array([0.9, 0.85, 0.80, 0.75, 0.70]))
    n_tests = len(tests) + 1
    if r_deg["trend_slope"] < 0:
        passed += 1

    return TheoremResult(
        name="T-KN-7",
        statement="Stability trend classifier detects degrading, improving, and stable dynamics",
        n_tests=n_tests,
        n_passed=passed,
        n_failed=n_tests - passed,
        details={},
        verdict="PROVEN" if passed == n_tests else "FAILED",
    )


# ── T-KN-8: Motion Regime Classification ──────────────────────────


def prove_motion_regime_classification() -> TheoremResult:
    """Five regimes reachable via explicit parameter combinations."""
    from closures.kinematics.kinematic_stability import classify_motion_regime

    cases = [
        # (v_mean, a_mean, K_stability, tau_kin, expected_regime)
        (0.01, 0.0, 0.9, 10.0, "Static"),
        (0.1, 0.01, 0.7, 5.0, "Uniform"),
        (0.5, 0.1, 0.8, 2.0, "Oscillatory"),
        (0.5, 0.5, 0.2, 200.0, "Chaotic"),
        (0.5, 0.5, 0.6, 200.0, "Transient"),
    ]
    passed = 0
    for vm, am, k, tau, expected in cases:
        r = classify_motion_regime(vm, am, k, tau)
        if r["motion_regime"] == expected:
            passed += 1

    # Also verify all outputs carry input values
    n_extra = 0
    for vm, am, k, tau, _ in cases:
        r = classify_motion_regime(vm, am, k, tau)
        n_extra += 1
        if r["v_mean"] == vm and r["a_mean"] == am and r["K_stability"] == k and r["tau_kin"] == tau:
            passed += 1

    return TheoremResult(
        name="T-KN-8",
        statement="Five motion regimes are reachable: Static, Uniform, Oscillatory, Chaotic, Transient",
        n_tests=len(cases) + n_extra,
        n_passed=passed,
        n_failed=len(cases) + n_extra - passed,
        details={"regimes": [c[-1] for c in cases]},
        verdict="PROVEN" if passed == len(cases) + n_extra else "FAILED",
    )


# ── T-KN-9: Phase Space Geometry ──────────────────────────────────


def prove_phase_space_geometry() -> TheoremResult:
    """Phase trajectories have non-negative path length and enclosed area."""
    from closures.kinematics.phase_space_return import compute_phase_trajectory

    scenarios: list[tuple[str, np.ndarray, np.ndarray]] = [
        ("circle", np.sin(np.linspace(0, 2 * np.pi, 100)), np.cos(np.linspace(0, 2 * np.pi, 100))),
        ("line", np.linspace(0, 10, 100), np.ones(100)),
        ("point", np.zeros(100), np.zeros(100)),
        (
            "spiral",
            np.linspace(0, 1, 100) * np.sin(np.linspace(0, 6 * np.pi, 100)),
            np.linspace(0, 1, 100) * np.cos(np.linspace(0, 6 * np.pi, 100)),
        ),
    ]
    passed = 0
    n_tests = 0
    for _label, x, v in scenarios:
        r = compute_phase_trajectory(x, v)
        # Path length ≥ 0
        n_tests += 1
        if r["path_length"] >= 0:
            passed += 1
        # Enclosed area ≥ 0
        n_tests += 1
        if r["enclosed_area"] >= 0:
            passed += 1
        # n_points matches input
        n_tests += 1
        if r["n_points"] == len(x):
            passed += 1

    # Circle should have nonzero area
    r_circ = compute_phase_trajectory(
        np.sin(np.linspace(0, 2 * np.pi, 100)),
        np.cos(np.linspace(0, 2 * np.pi, 100)),
    )
    n_tests += 1
    if r_circ["enclosed_area"] > 0:
        passed += 1

    return TheoremResult(
        name="T-KN-9",
        statement="Phase trajectories have non-negative path length and area, size matches input",
        n_tests=n_tests,
        n_passed=passed,
        n_failed=n_tests - passed,
        details={},
        verdict="PROVEN" if passed == n_tests else "FAILED",
    )


# ── T-KN-10: Cross-Module Consistency Chain ───────────────────────


def prove_cross_module_consistency() -> TheoremResult:
    """Full chain: kinematics → energy → phase → stability is consistent."""
    from closures.kinematics.energy_mechanics import (
        compute_mechanical_energy,
        verify_energy_conservation,
    )
    from closures.kinematics.kinematic_stability import (
        compute_kinematic_stability,
        compute_stability_margin,
        compute_stability_trend,
    )
    from closures.kinematics.linear_kinematics import compute_linear_kinematics
    from closures.kinematics.momentum_dynamics import (
        compute_impulse,
        compute_linear_momentum,
    )
    from closures.kinematics.phase_space_return import (
        compute_phase_trajectory,
        detect_oscillation,
    )

    n_tests = 0
    passed = 0

    # 1. Linear kinematics outputs have required keys
    kin = compute_linear_kinematics(x=0.0, v=5.0, a=-1.0, dt=0.1)
    for key in ["position", "velocity", "acceleration", "phase_magnitude", "regime"]:
        n_tests += 1
        if key in kin:
            passed += 1

    # 2. Energy outputs have required keys
    eng = compute_mechanical_energy(5.0, 3.0)
    for key in ["E_mechanical", "E_kinetic", "E_potential"]:
        n_tests += 1
        if key in eng:
            passed += 1

    # 3. Momentum outputs have required keys
    mom = compute_linear_momentum(v=5.0)
    n_tests += 1
    if "p" in mom:
        passed += 1

    # 4. Impulse outputs
    imp = compute_impulse(F_net=10.0, dt=0.5)
    n_tests += 1
    if "J" in imp:
        passed += 1

    # 5. Phase trajectory outputs
    t = np.linspace(0, 2 * np.pi, 50)
    pt = compute_phase_trajectory(np.sin(t), np.cos(t))
    for key in ["path_length", "enclosed_area", "n_points"]:
        n_tests += 1
        if key in pt:
            passed += 1

    # 6. Oscillation outputs
    osc = detect_oscillation(np.sin(t), np.cos(t))
    for key in ["oscillation_type", "sign_changes"]:
        n_tests += 1
        if key in osc:
            passed += 1

    # 7. Stability outputs
    x_arr = np.array([0.0, 1.0, 2.0, 3.0, 4.0])
    v_arr = np.array([1.0, 1.1, 0.9, 1.0, 1.05])
    stab = compute_kinematic_stability(x_arr, v_arr)
    for key in ["K_stability", "regime"]:
        n_tests += 1
        if key in stab:
            passed += 1

    # 8. Stability margin valid
    margin = compute_stability_margin(stab["K_stability"])
    n_tests += 1
    if "margin" in margin and "margin_status" in margin:
        passed += 1

    # 9. Trend outputs
    trend = compute_stability_trend(np.array([0.9, 0.85, 0.8, 0.75]))
    n_tests += 1
    if "trend_direction" in trend and "trend_slope" in trend:
        passed += 1

    # 10. Conservation detection outputs
    econs = verify_energy_conservation(np.ones(10))
    n_tests += 1
    if "is_conserved" in econs:
        passed += 1

    return TheoremResult(
        name="T-KN-10",
        statement="All kinematic modules return well-typed outputs with required keys",
        n_tests=n_tests,
        n_passed=passed,
        n_failed=n_tests - passed,
        details={"modules_tested": 6},
        verdict="PROVEN" if passed == n_tests else "FAILED",
    )


# ── Public interface ──────────────────────────────────────────────

ALL_THEOREMS = [
    prove_elastic_conservation,
    prove_energy_additivity,
    prove_work_energy_theorem,
    prove_energy_conservation_detection,
    prove_oscillation_classification,
    prove_stability_ordering,
    prove_stability_trend,
    prove_motion_regime_classification,
    prove_phase_space_geometry,
    prove_cross_module_consistency,
]


def run_all_theorems() -> list[TheoremResult]:
    return [t() for t in ALL_THEOREMS]


if __name__ == "__main__":
    total_t = total_p = total_f = 0
    for r in run_all_theorems():
        total_t += r.n_tests
        total_p += r.n_passed
        total_f += r.n_failed
        print(f"  {r.name}: {r.verdict}  ({r.n_passed}/{r.n_tests})")
    print(f"\n  Overall: {total_p}/{total_t} passed, {total_f} failed")
    print(f"  All proven: {total_f == 0}")
