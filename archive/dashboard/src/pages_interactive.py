"""
Interactive dashboard pages: Test Templates, Batch Validation, Live Runner, Work Templates.
"""
# pyright: reportUnknownMemberType=false
# pyright: reportUnknownVariableType=false
# pyright: reportUnknownArgumentType=false
# pyright: reportOptionalMemberAccess=false
# pyright: reportMissingTypeStubs=false

from __future__ import annotations

import json
import subprocess
import sys
from datetime import datetime
from typing import Any

from umcp.dashboard._deps import np, pd, st
from umcp.dashboard._utils import (
    STATUS_COLORS,
    classify_regime,
    get_regime_color,
    get_repo_root,
    load_casepacks,
)
from umcp.dashboard.pages_physics import render_gcd_panel, translate_to_gcd

# Import optimized kernel computer for real computation
try:
    from umcp.kernel_optimized import OptimizedKernelComputer

    _HAS_KERNEL = True
except ImportError:  # pragma: no cover
    _HAS_KERNEL = False


def render_test_templates_page() -> None:
    """
    Render the Test Templates page for interactive tier translation.

    Allows users to:
    1. Input Tier 0 raw data (coordinates, weights)
    2. See Tier 1 transformation (kernel invariants)
    3. See Tier 2 outputs (regime classification, diagnostics)
    4. Get a full audit trail
    """
    if st is None or pd is None or np is None:
        return

    st.title("🧮 Test Templates")
    st.caption("Transform your data through UMCP tiers with full audit trail")

    # Initialize session state for templates
    if "template_coords" not in st.session_state:
        st.session_state.template_coords = [0.85, 0.72, 0.91, 0.68]
    if "template_weights" not in st.session_state:
        st.session_state.template_weights = [0.25, 0.25, 0.25, 0.25]
    if "audit_log" not in st.session_state:
        st.session_state.audit_log = []

    # ========== TIER 0: Input Layer ==========
    st.header("📥 Tier 0: Interface Layer (Raw Input)")
    st.markdown("""
    **Tier 0** declares raw measurements and converts them to bounded trace Ψ(t) ∈ [0,1]ⁿ.
    Enter your coordinates (values should be in range [0, 1]) and weights (must sum to 1.0).
    """)

    with st.expander("📖 About Tier 0", expanded=False):
        st.markdown("""
        **Tier 0 Scope:**
        - Observables: Raw measurements with units
        - Embedding: Map x(t) → Ψ(t) ∈ [0,1]ⁿ
        - Weights: w_i ≥ 0, Σw_i = 1
        - OOR Policy: Out-of-range handling

        **Key Rule:** Tier 0 is frozen before Tier 1 computes.
        """)

    # Template presets
    st.subheader("📋 Template Presets")
    preset_cols = st.columns(5)

    presets = {
        "Stable": {"coords": [0.85, 0.80, 0.82, 0.78], "weights": [0.25, 0.25, 0.25, 0.25]},
        "Watch": {"coords": [0.45, 0.42, 0.48, 0.40], "weights": [0.25, 0.25, 0.25, 0.25]},
        "Collapse": {"coords": [0.12, 0.08, 0.15, 0.05], "weights": [0.25, 0.25, 0.25, 0.25]},
        "Heterogeneous": {"coords": [0.95, 0.20, 0.80, 0.35], "weights": [0.30, 0.20, 0.30, 0.20]},
        "Homogeneous": {"coords": [0.75, 0.75, 0.75, 0.75], "weights": [0.25, 0.25, 0.25, 0.25]},
    }

    for i, (name, preset) in enumerate(presets.items()):
        with preset_cols[i]:
            if st.button(f"📌 {name}", key=f"preset_{name}", use_container_width=True):
                st.session_state.template_coords = preset["coords"]
                st.session_state.template_weights = preset["weights"]
                st.rerun()

    st.divider()

    # Coordinate input
    st.subheader("🎯 Coordinates (Ψ)")

    n_dims = st.slider(
        "Number of dimensions",
        min_value=2,
        max_value=8,
        value=len(st.session_state.template_coords),
        help="Trace vector dimensionality",
    )

    # Adjust arrays if dimension changed
    while len(st.session_state.template_coords) < n_dims:
        st.session_state.template_coords.append(0.5)
        st.session_state.template_weights.append(1.0 / n_dims)
    while len(st.session_state.template_coords) > n_dims:
        st.session_state.template_coords.pop()
        st.session_state.template_weights.pop()

    # Normalize weights after dimension change
    w_sum = sum(st.session_state.template_weights)
    if abs(w_sum - 1.0) > 0.01:
        st.session_state.template_weights = [w / w_sum for w in st.session_state.template_weights]

    coord_cols = st.columns(n_dims)
    coords = []
    for i in range(n_dims):
        with coord_cols[i]:
            val = st.number_input(
                f"c_{i + 1}",
                min_value=0.0,
                max_value=1.0,
                value=float(st.session_state.template_coords[i]),
                step=0.01,
                format="%.3f",
                key=f"coord_{i}",
            )
            coords.append(val)

    # Weight input
    st.subheader("⚖️ Weights (w)")
    weight_cols = st.columns(n_dims)
    weights = []
    for i in range(n_dims):
        with weight_cols[i]:
            val = st.number_input(
                f"w_{i + 1}",
                min_value=0.0,
                max_value=1.0,
                value=float(st.session_state.template_weights[i]),
                step=0.05,
                format="%.3f",
                key=f"weight_{i}",
            )
            weights.append(val)

    # Weight validation
    weight_sum = sum(weights)
    if abs(weight_sum - 1.0) > 1e-6:
        st.warning(f"⚠️ Weights sum to {weight_sum:.4f}, should sum to 1.0")
        if st.button("🔧 Normalize Weights"):
            weights = [w / weight_sum for w in weights]
            st.session_state.template_weights = weights
            st.rerun()
    else:
        st.success(f"✅ Weights sum to {weight_sum:.6f}")

    # Store in session state
    st.session_state.template_coords = coords
    st.session_state.template_weights = weights

    # Epsilon clipping
    st.subheader("🔒 ε-Clipping Policy")
    epsilon = st.select_slider(
        "Epsilon (ε)",
        options=[1e-8, 1e-7, 1e-6, 1e-5, 1e-4],
        value=1e-6,
        format_func=lambda x: f"{x:.0e}",
        help="Guard band for coordinate clamping",
    )

    st.divider()

    # ========== PROCESS BUTTON ==========
    process_col1, process_col2, process_col3 = st.columns([2, 1, 1])
    with process_col1:
        process_button = st.button("🚀 Run Tier Translation", type="primary", use_container_width=True)
    with process_col2:
        if st.button("🗑️ Clear Audit Log", use_container_width=True):
            st.session_state.audit_log = []
            st.rerun()
    with process_col3:
        export_audit = st.button("📤 Export Audit", use_container_width=True)

    if process_button:
        # Start audit
        audit_entry = {
            "timestamp": datetime.now().isoformat(),
            "tier0": {},
            "tier1": {},
            "tier2": {},
            "status": "PROCESSING",
        }

        # ========== TIER 0 PROCESSING ==========
        st.header("⚙️ Processing...")
        progress = st.progress(0, text="Starting tier translation...")

        # Tier 0: Validate and prepare inputs
        progress.progress(10, text="Tier 0: Validating inputs...")

        c_raw = np.array(coords)
        w_raw = np.array(weights)

        # Apply epsilon clipping
        c_clipped = np.clip(c_raw, epsilon, 1 - epsilon)
        clip_count = np.sum(c_raw != c_clipped)
        clip_perturbation = np.sum(np.abs(c_raw - c_clipped))

        audit_entry["tier0"] = {
            "raw_coordinates": coords,
            "raw_weights": weights,
            "epsilon": epsilon,
            "clipped_coordinates": c_clipped.tolist(),
            "clip_count": int(clip_count),
            "clip_perturbation": float(clip_perturbation),
            "weight_sum": float(weight_sum),
            "n_dimensions": n_dims,
        }

        progress.progress(30, text="Tier 1: Computing kernel invariants...")

        # ========== TIER 1: KERNEL COMPUTATION ==========
        try:
            # Use OptimizedKernelComputer for auditable, lemma-verified computation
            if _HAS_KERNEL:
                computer = OptimizedKernelComputer(epsilon=epsilon)
                outputs = computer.compute(c_clipped, w_raw)
                fidelity = outputs.F
                drift = outputs.omega
                log_ic = outputs.kappa
                integrity_composite = outputs.IC
                entropy = outputs.S
                curvature = outputs.C
                heterogeneity_gap = outputs.heterogeneity_gap
                is_homogeneous = outputs.is_homogeneous
                het_regime = outputs.regime
                computation_mode = outputs.computation_mode

                # Lipschitz error bounds (OPT-12)
                error_bounds = computer.propagate_coordinate_error(epsilon)
            else:
                # Fallback: inline computation
                fidelity = float(np.sum(w_raw * c_clipped))
                drift = 1 - fidelity
                log_ic = float(np.sum(w_raw * np.log(c_clipped)))
                integrity_composite = float(np.exp(log_ic))
                entropy = 0.0
                for ci, wi in zip(c_clipped, w_raw, strict=False):
                    if wi > 0 and 0 < ci < 1:
                        entropy += wi * (-ci * np.log(ci) - (1 - ci) * np.log(1 - ci))
                entropy = float(entropy)
                curvature = float(np.std(c_clipped, ddof=0) / 0.5)
                heterogeneity_gap = fidelity - integrity_composite
                is_homogeneous = np.allclose(c_clipped, c_clipped[0], atol=1e-15)
                if heterogeneity_gap < 1e-6:
                    het_regime = "homogeneous"
                elif heterogeneity_gap < 0.01:
                    het_regime = "coherent"
                elif heterogeneity_gap < 0.05:
                    het_regime = "heterogeneous"
                else:
                    het_regime = "fragmented"
                computation_mode = "inline_fallback"
                error_bounds = None

            # Validate bounds (Lemma 1)
            bounds_valid = (
                0 <= fidelity <= 1
                and 0 <= drift <= 1
                and 0 <= curvature <= 1
                and epsilon <= integrity_composite <= 1 - epsilon
                and np.isfinite(log_ic)
                and 0 <= entropy <= np.log(2)
            )

            audit_entry["tier1"] = {
                "F": fidelity,
                "omega": drift,
                "S": entropy,
                "C": curvature,
                "kappa": log_ic,
                "IC": integrity_composite,
                "heterogeneity_gap": heterogeneity_gap,
                "is_homogeneous": bool(is_homogeneous),
                "heterogeneity_regime": het_regime,
                "computation_mode": computation_mode,
                "bounds_valid": bounds_valid,
                "identity_F_omega": abs(fidelity + drift - 1.0) < 1e-9,
                "identity_IC_kappa": abs(integrity_composite - np.exp(log_ic)) < 1e-9,
                "error_bounds": {
                    "F": error_bounds.F,
                    "omega": error_bounds.omega,
                    "kappa": error_bounds.kappa,
                    "S": error_bounds.S,
                }
                if error_bounds is not None
                else None,
            }

            progress.progress(60, text="Tier 2: Computing diagnostics and regime...")

            # ========== TIER 2: DIAGNOSTICS & REGIME ==========

            # Regime classification
            regime = classify_regime(drift)

            # Stability metrics
            freshness = 1 - drift  # How "fresh" the state is

            # Return time estimate (simplified)
            if regime == "STABLE":
                tau_R_est = "≤ 10 steps"
            elif regime == "WATCH":
                tau_R_est = "10-50 steps"
            elif regime == "COLLAPSE":
                tau_R_est = "∞_rec (no return expected)"
            else:
                tau_R_est = "CRITICAL (seam failure)"

            # Stability score (0-100)
            stability_score = int(fidelity * 100 * (1 - curvature))

            # Risk level
            if regime == "STABLE":
                risk = "LOW"
            elif regime == "WATCH":
                risk = "MEDIUM"
            else:
                risk = "HIGH"

            # Recommendations
            recommendations = []
            if drift > 0.5:
                recommendations.append("High drift detected - review data sources")
            if curvature > 0.3:
                recommendations.append("High curvature - coordinates are dispersed")
            if heterogeneity_gap > 0.1:
                recommendations.append("Large heterogeneity gap - significant heterogeneity")
            if not bounds_valid:
                recommendations.append("⚠️ Lemma 1 bounds violated - check inputs")
            if not recommendations:
                recommendations.append("✅ All metrics within normal ranges")

            audit_entry["tier2"] = {
                "regime": regime,
                "freshness": freshness,
                "tau_R_estimate": tau_R_est,
                "stability_score": stability_score,
                "risk_level": risk,
                "recommendations": recommendations,
                "classification_criteria": {
                    "omega_threshold_collapse": "ω < 0.1 or ω > 0.9",
                    "omega_threshold_stable": "0.3 ≤ ω ≤ 0.7",
                    "omega_threshold_watch": "otherwise",
                },
            }

            audit_entry["status"] = "COMPLETE"
            progress.progress(100, text="Complete!")

        except Exception as e:
            audit_entry["status"] = "ERROR"
            audit_entry["error"] = str(e)
            st.error(f"❌ Processing error: {e}")
            progress.progress(100, text="Error!")

        # Add to audit log
        st.session_state.audit_log.append(audit_entry)

        # ========== DISPLAY RESULTS ==========
        st.divider()

        if audit_entry["status"] == "COMPLETE":
            # Results header with regime color
            regime = audit_entry["tier2"]["regime"]
            regime_color = get_regime_color(regime)
            st.markdown(
                f"""<div style="padding: 20px; border-left: 6px solid {regime_color};
                    background: {regime_color}22; border-radius: 8px; margin-bottom: 20px;">
                    <h2 style="margin: 0; color: {regime_color};">🎯 Result: {regime}</h2>
                    <p style="margin: 5px 0 0 0;">Stability Score: {audit_entry["tier2"]["stability_score"]}/100 • Risk: {audit_entry["tier2"]["risk_level"]}</p>
                </div>""",
                unsafe_allow_html=True,
            )

            # Three-column tier display
            tier_cols = st.columns(3)

            # TIER 0 OUTPUT
            with tier_cols[0]:
                st.markdown("### 📥 Tier 0: Interface")
                t0 = audit_entry["tier0"]
                st.metric("Dimensions", t0["n_dimensions"])
                st.metric("Clipped Values", t0["clip_count"])
                st.metric("ε-Perturbation", f"{t0['clip_perturbation']:.2e}")

                with st.expander("Raw Data"):
                    t0_df = pd.DataFrame(
                        {
                            "Coordinate": [f"c_{i + 1}" for i in range(len(t0["raw_coordinates"]))],
                            "Raw": t0["raw_coordinates"],
                            "Clipped": t0["clipped_coordinates"],
                            "Weight": t0["raw_weights"],
                        }
                    )
                    st.dataframe(t0_df, hide_index=True, use_container_width=True)

            # TIER 1 OUTPUT
            with tier_cols[1]:
                st.markdown("### ⚙️ Tier 1: Kernel")
                t1 = audit_entry["tier1"]

                col1, col2 = st.columns(2)
                with col1:
                    st.metric("F (Fidelity)", f"{t1['F']:.4f}")
                    st.metric("ω (Drift)", f"{t1['omega']:.4f}")
                    st.metric("S (Entropy)", f"{t1['S']:.4f}")
                with col2:
                    st.metric("C (Curvature)", f"{t1['C']:.4f}")
                    st.metric("κ (Log-IC)", f"{t1['kappa']:.4f}")
                    st.metric("IC", f"{t1['IC']:.4f}")

                st.markdown(f"**Heterogeneity Gap:** {t1['heterogeneity_gap']:.4f}")
                st.markdown(f"**Heterogeneity:** {t1['heterogeneity_regime']}")

                # Identity checks
                st.markdown("**Identity Checks:**")
                id1 = "✅" if t1["identity_F_omega"] else "❌"
                id2 = "✅" if t1["identity_IC_kappa"] else "❌"
                st.markdown(f"- {id1} F + ω = 1")
                st.markdown(f"- {id2} IC = exp(κ)")
                st.markdown(f"- {'✅' if t1['bounds_valid'] else '❌'} Lemma 1 bounds")

            # TIER 2 OUTPUT
            with tier_cols[2]:
                st.markdown("### 📊 Tier 2: Diagnostics")
                t2 = audit_entry["tier2"]

                st.metric("Regime", t2["regime"])
                st.metric("Freshness (1-ω)", f"{t2['freshness']:.2%}")
                st.metric("τ_R Estimate", t2["tau_R_estimate"])

                st.markdown("**Recommendations:**")
                for rec in t2["recommendations"]:
                    st.markdown(f"- {rec}")

            # ========== FULL AUDIT TRAIL ==========
            st.divider()
            st.subheader("📋 Full Audit Trail")

            with st.expander("🔍 View Complete Audit JSON", expanded=False):
                st.json(audit_entry)

            # ========== GCD TRANSLATION PANEL ==========
            st.divider()
            st.subheader("🌀 GCD Translation (Generative Collapse Dynamics)")
            st.caption("Native Tier-1 interpretation using the GCD framework for intuitive understanding")

            # Translate tier1 values to GCD
            gcd_translation = translate_to_gcd(audit_entry["tier1"])
            audit_entry["gcd"] = gcd_translation

            render_gcd_panel(gcd_translation, compact=False)

            # Additional interpretive summary for test templates
            st.markdown("#### 📖 Plain Language Interpretation")
            omega_val = audit_entry["tier1"]["omega"]
            fidelity_val = audit_entry["tier1"]["F"]
            ic_val = audit_entry["tier1"]["IC"]

            gcd_regime = gcd_translation["regime"]
            if gcd_regime == "STABLE":
                interpretation = f"""
                Your data shows **high coherence** with minimal drift (ω = {omega_val:.4f}).
                The system is in a **stable generative state** where collapse events produce
                meaningful structure. Fidelity remains high at F = {fidelity_val:.4f}, indicating
                strong alignment with the reference trace.
                """
            elif gcd_regime == "WATCH":
                interpretation = f"""
                Your data shows **moderate drift** (ω = {omega_val:.4f}), placing the system
                in a **watch regime**. Collapse dynamics are active but not yet overwhelming
                the generative capacity. Monitor the IC value ({ic_val:.4f}) for further degradation.
                """
            else:
                interpretation = f"""
                Your data indicates **significant drift** (ω = {omega_val:.4f}), placing the
                system in a **collapse regime**. The generative capacity is compromised, and
                the integrity composite has degraded to IC = {ic_val:.4f}. Recovery may require
                substantial intervention.
                """
            st.info(interpretation.strip())

            # Tier flow visualization
            st.markdown("### 🔄 Tier Flow Diagram")
            st.markdown(f"""
            ```
            ┌─────────────────────────────────────────────────────────────────────────┐
            │                           TIER TRANSLATION                               │
            ├─────────────────────────────────────────────────────────────────────────┤
            │                                                                         │
            │  TIER 0 (Interface)              TIER 1 (Kernel)         TIER 2 (Diag)  │
            │  ═══════════════════             ═══════════════         ══════════════ │
            │                                                                         │
            │  Raw Coordinates:                Computed:               Classification:│
            │  c = {[f"{c:.2f}" for c in coords]}     F = {t1["F"]:.4f}              Regime: {regime}      │
            │                                  ω = {t1["omega"]:.4f}              Risk: {t2["risk_level"]}       │
            │  Weights:                        S = {t1["S"]:.4f}                                │
            │  w = {[f"{w:.2f}" for w in weights]}    C = {t1["C"]:.4f}              Return Est:   │
            │                                  κ = {t1["kappa"]:.4f}             {t2["tau_R_estimate"]}  │
            │  ε = {epsilon:.0e}                       IC = {t1["IC"]:.4f}                               │
            │                                                                         │
            │        ────────────>         ────────────>         ────────────>        │
            │           freeze                compute                classify         │
            │                                                                         │
            └─────────────────────────────────────────────────────────────────────────┘
            ```
            """)

    # Export audit
    if export_audit and st.session_state.audit_log:
        st.download_button(
            label="📥 Download Audit Log (JSON)",
            data=json.dumps(st.session_state.audit_log, indent=2),
            file_name=f"umcp_audit_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json",
        )

    # ========== AUDIT HISTORY ==========
    st.divider()
    st.subheader("📜 Audit History")

    if st.session_state.audit_log:
        for i, entry in enumerate(reversed(st.session_state.audit_log[-10:])):
            status_icon = "✅" if entry["status"] == "COMPLETE" else "❌"
            regime = entry.get("tier2", {}).get("regime", "N/A")
            regime_color = get_regime_color(regime)

            with st.expander(
                f"{status_icon} Run {len(st.session_state.audit_log) - i} — {regime} @ {entry['timestamp'][:19]}"
            ):
                t0 = entry.get("tier0", {})
                t1 = entry.get("tier1", {})
                t2 = entry.get("tier2", {})

                cols = st.columns(3)
                with cols[0]:
                    st.markdown("**Tier 0:**")
                    st.markdown(f"- Dims: {t0.get('n_dimensions', 'N/A')}")
                    st.markdown(f"- Clipped: {t0.get('clip_count', 'N/A')}")
                with cols[1]:
                    st.markdown("**Tier 1:**")
                    st.markdown(
                        f"- F: {t1.get('F', 'N/A'):.4f}" if isinstance(t1.get("F"), int | float) else "- F: N/A"
                    )
                    st.markdown(
                        f"- ω: {t1.get('omega', 'N/A'):.4f}" if isinstance(t1.get("omega"), int | float) else "- ω: N/A"
                    )
                with cols[2]:
                    st.markdown("**Tier 2:**")
                    st.markdown(f"- Regime: {regime}")
                    st.markdown(f"- Score: {t2.get('stability_score', 'N/A')}")
    else:
        st.info("No audit history yet. Run a tier translation to start logging.")


# ============================================================================
# Expansion Features - Export, Comparison, Notifications, Bookmarks
# ============================================================================


def render_batch_validation_page() -> None:
    """Render the batch validation page for running multiple casepacks."""
    if st is None:
        return

    st.title("📦 Batch Validation")
    st.caption("Run validation on multiple casepacks with a summary report")

    # Initialize batch results
    if "batch_results" not in st.session_state:
        st.session_state.batch_results = []

    repo_root = get_repo_root()
    casepacks = load_casepacks()

    if not casepacks:
        st.warning("No casepacks found in the repository.")
        return

    # ========== Casepack Selection ==========
    st.subheader("📦 Select Casepacks")

    col1, col2 = st.columns([2, 1])

    with col1:
        selected_casepacks = st.multiselect(
            "Choose casepacks to validate",
            [cp["id"] for cp in casepacks],
            default=[cp["id"] for cp in casepacks[:3]] if len(casepacks) >= 3 else [cp["id"] for cp in casepacks],
            help="Pick casepacks for batch validation",
        )

    with col2:
        if st.button("✅ Select All"):
            st.session_state["batch_select_all"] = True
            st.rerun()
        if st.button("❌ Clear All"):
            st.session_state["batch_select_all"] = False
            st.rerun()

    # ========== Validation Options ==========
    st.subheader("⚙️ Options")

    opt_cols = st.columns(4)
    with opt_cols[0]:
        strict_mode = st.checkbox("Strict Mode", value=False, help="Fail on warnings")
    with opt_cols[1]:
        verbose = st.checkbox("Verbose Output", value=False, help="Show full stdout/stderr")
    with opt_cols[2]:
        fail_fast = st.checkbox("Fail Fast", value=False, help="Stop on first failure")
    with opt_cols[3]:
        st.checkbox("Parallel (simulated)", value=False, disabled=True, help="Coming soon")

    st.divider()

    # ========== Run Batch ==========
    if st.button("🚀 Run Batch Validation", use_container_width=True, disabled=not selected_casepacks):
        results = []
        progress = st.progress(0, text="Starting batch validation...")
        status_container = st.container()

        total = len(selected_casepacks)
        passed = 0
        failed = 0

        for i, cp_id in enumerate(selected_casepacks):
            progress.progress((i + 1) / total, text=f"Validating {cp_id}... ({i + 1}/{total})")

            try:
                cmd = [sys.executable, "-m", "umcp", "validate", f"casepacks/{cp_id}"]
                if strict_mode:
                    cmd.append("--strict")
                if verbose:
                    cmd.append("--verbose")

                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    timeout=60,
                    cwd=repo_root,
                )

                status = "CONFORMANT" if result.returncode == 0 else "NONCONFORMANT"
                if status == "CONFORMANT":
                    passed += 1
                else:
                    failed += 1

                results.append(
                    {
                        "casepack": cp_id,
                        "status": status,
                        "return_code": result.returncode,
                        "stdout": result.stdout[:500] if result.stdout else "",
                        "stderr": result.stderr[:500] if result.stderr else "",
                        "timestamp": datetime.now().isoformat(),
                    }
                )

                if fail_fast and status == "NONCONFORMANT":
                    st.warning(f"⚠️ Fail-fast triggered at {cp_id}")
                    break

            except subprocess.TimeoutExpired:
                failed += 1
                results.append(
                    {
                        "casepack": cp_id,
                        "status": "TIMEOUT",
                        "return_code": -1,
                        "stdout": "",
                        "stderr": "Validation timed out after 60 seconds",
                        "timestamp": datetime.now().isoformat(),
                    }
                )
            except Exception as e:
                failed += 1
                results.append(
                    {
                        "casepack": cp_id,
                        "status": "ERROR",
                        "return_code": -1,
                        "stdout": "",
                        "stderr": str(e),
                        "timestamp": datetime.now().isoformat(),
                    }
                )

        progress.progress(1.0, text="Complete!")

        # Store results
        batch_run = {
            "id": len(st.session_state.batch_results) + 1,
            "timestamp": datetime.now().isoformat(),
            "total": total,
            "passed": passed,
            "failed": failed,
            "results": results,
        }
        st.session_state.batch_results.append(batch_run)

        # Summary
        with status_container:
            st.markdown("### 📊 Batch Summary")

            summary_cols = st.columns(4)
            with summary_cols[0]:
                st.metric("Total", total)
            with summary_cols[1]:
                st.metric("Passed", passed, delta=None)
            with summary_cols[2]:
                st.metric("Failed", failed, delta=None)
            with summary_cols[3]:
                rate = (passed / total * 100) if total > 0 else 0
                st.metric("Pass Rate", f"{rate:.1f}%")

            # Results table
            if pd is not None:
                results_df = pd.DataFrame(
                    [{"Casepack": r["casepack"], "Status": r["status"], "Time": r["timestamp"][:19]} for r in results]
                )

                def color_status(val: str) -> str:
                    if val == "CONFORMANT":
                        return "background-color: #d4edda"
                    elif val == "NONCONFORMANT":
                        return "background-color: #f8d7da"
                    return "background-color: #fff3cd"

                st.dataframe(
                    results_df.style.map(color_status, subset=["Status"]), use_container_width=True, hide_index=True
                )

    st.divider()

    # ========== Batch History ==========
    st.subheader("📜 Batch History")

    if st.session_state.batch_results:
        for batch in reversed(st.session_state.batch_results[-5:]):
            status_icon = "✅" if batch["failed"] == 0 else "⚠️" if batch["passed"] > 0 else "❌"

            with st.expander(
                f"{status_icon} Batch #{batch['id']} — {batch['passed']}/{batch['total']} passed @ {batch['timestamp'][:19]}"
            ):
                for r in batch["results"]:
                    icon = "✅" if r["status"] == "CONFORMANT" else "❌"
                    st.markdown(f"{icon} **{r['casepack']}** — {r['status']}")

                st.download_button(
                    label="📥 Download Report",
                    data=json.dumps(batch, indent=2),
                    file_name=f"batch_report_{batch['id']}.json",
                    mime="application/json",
                )
    else:
        st.info("No batch runs yet. Run a batch validation to see history.")


def render_live_runner_page() -> None:
    """Render live validation runner with real-time controls."""
    if st is None or pd is None:
        return

    st.title("▶️ Live Validation Runner")
    st.caption("Run validations interactively with real-time feedback")

    repo_root = get_repo_root()
    casepacks = load_casepacks()

    # ========== Control Panel ==========
    st.subheader("🎛️ Control Panel")

    with st.container(border=True):
        ctrl_cols = st.columns([2, 1, 1, 1])

        with ctrl_cols[0]:
            casepack_options = ["Repository (All)"] + [cp["id"] for cp in casepacks]
            selected_target = st.selectbox("Target", casepack_options, help="Select what to validate")

        with ctrl_cols[1]:
            strict_mode = st.toggle("Strict Mode", value=False, help="Enable strict validation")

        with ctrl_cols[2]:
            verbose = st.toggle("Verbose Output", value=False, help="Show detailed output")

        with ctrl_cols[3]:
            fail_on_warning = st.toggle("Fail on Warning", value=False, help="Treat warnings as errors")

    st.divider()

    # ========== Run Controls ==========
    run_cols = st.columns([1, 1, 2])

    with run_cols[0]:
        run_button = st.button("▶️ Run Validation", use_container_width=True, type="primary")

    with run_cols[1]:
        # Stop button placeholder (for future async support)
        st.button("⏹️ Stop", use_container_width=True, disabled=True)

    with run_cols[2]:
        st.empty()  # Spacer

    # ========== Results Area ==========
    if run_button:
        st.divider()
        st.subheader("📋 Validation Results")

        # Build command
        cmd = [sys.executable, "-m", "umcp", "validate"]

        if selected_target != "Repository (All)":
            cmd.append(f"casepacks/{selected_target}")

        if strict_mode:
            cmd.append("--strict")
        if verbose:
            cmd.append("--verbose")
        if fail_on_warning:
            cmd.append("--fail-on-warning")

        # Display command
        with st.expander("📝 Command", expanded=False):
            st.code(" ".join(cmd), language="bash")

        # Run with progress
        progress_bar = st.progress(0, text="Starting validation...")
        status_container = st.empty()
        output_container = st.container()

        try:
            progress_bar.progress(20, text="Running validation...")

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=120,
                cwd=repo_root,
            )

            progress_bar.progress(100, text="Complete!")

            # Parse result
            if result.returncode == 0:
                status_container.success("✅ **CONFORMANT** - All validations passed!")

                # Try to parse JSON output
                try:
                    # Find JSON in output
                    output = result.stdout
                    json_start = output.find("{")
                    json_end = output.rfind("}") + 1
                    if json_start >= 0 and json_end > json_start:
                        json_str = output[json_start:json_end]
                        result_data = json.loads(json_str)

                        # Display metrics
                        with output_container:
                            metric_cols = st.columns(4)
                            with metric_cols[0]:
                                st.metric("Status", result_data.get("run_status", "N/A"))
                            with metric_cols[1]:
                                counts = result_data.get("summary", {}).get("counts", {})
                                st.metric("Errors", counts.get("errors", 0))
                            with metric_cols[2]:
                                st.metric("Warnings", counts.get("warnings", 0))
                            with metric_cols[3]:
                                st.metric("Targets", counts.get("targets_total", 0))

                            # Targets breakdown
                            st.markdown("**Validated Targets:**")
                            targets = result_data.get("targets", [])
                            for target in targets:
                                status_icon = "✅" if target.get("run_status") == "CONFORMANT" else "❌"
                                st.markdown(
                                    f"- {status_icon} `{target.get('target_path', 'unknown')}` — {target.get('run_status', 'N/A')}"
                                )
                except (json.JSONDecodeError, KeyError):
                    pass
            else:
                status_container.error("❌ **NONCONFORMANT** - Validation failed!")

            # Raw output
            with st.expander("📄 Full Output", expanded=False):
                st.code(
                    result.stdout + result.stderr if result.stdout or result.stderr else "No output", language="text"
                )

            # Store result in session
            st.session_state.last_validation = {
                "target": selected_target,
                "status": "CONFORMANT" if result.returncode == 0 else "NONCONFORMANT",
                "timestamp": datetime.now().isoformat(),
            }

        except subprocess.TimeoutExpired:
            progress_bar.progress(100, text="Timeout!")
            status_container.error("⏱️ Validation timed out after 120 seconds")
        except Exception as e:
            progress_bar.progress(100, text="Error!")
            status_container.error(f"❌ Error running validation: {e}")

    st.divider()

    # ========== History ==========
    st.subheader("📜 Recent Runs")

    if st.session_state.last_validation:
        last = st.session_state.last_validation
        status_color = STATUS_COLORS.get(last["status"], "#6c757d")
        st.markdown(
            f"""<div style="padding: 10px; border-left: 4px solid {status_color}; background: {status_color}22; border-radius: 4px;">
            <strong>{last["status"]}</strong> — {last["target"]} @ {last["timestamp"][:19]}
            </div>""",
            unsafe_allow_html=True,
        )
    else:
        st.info("No validation runs yet. Click 'Run Validation' to start.")

    st.divider()

    # ========== Casepack Quick Selector ==========
    st.subheader("📦 Quick Casepack Runner")

    # Grid of casepack buttons
    cols_per_row = 3
    for i in range(0, len(casepacks), cols_per_row):
        cols = st.columns(cols_per_row)
        for j, col in enumerate(cols):
            if i + j < len(casepacks):
                cp = casepacks[i + j]
                with col, st.container(border=True):
                    st.markdown(f"**{cp['id']}**")
                    st.caption(f"v{cp['version']} • {cp['test_vectors']} vectors")
                    if st.button("▶️ Run", key=f"run_{cp['id']}", use_container_width=True):
                        with st.spinner(f"Validating {cp['id']}..."):
                            result = subprocess.run(
                                [sys.executable, "-m", "umcp", "validate", f"casepacks/{cp['id']}"],
                                capture_output=True,
                                text=True,
                                timeout=60,
                                cwd=repo_root,
                            )
                            if result.returncode == 0:
                                st.success("✅ Pass")
                            else:
                                st.error("❌ Fail")


# ============================================================================
# Work Templates — Guided domain closure implementation with 5 full examples
# ============================================================================

# Pre-built work template examples (domain → config)
_WORK_TEMPLATE_EXAMPLES: dict[str, dict[str, Any]] = {
    "Weather Station": {
        "description": (
            "A weather monitoring station with 6 sensors. Each sensor reading is "
            "normalized to [0,1] to form the trace vector. Channel death occurs when "
            "a sensor fails (value → ε), triggering geometric slaughter in IC."
        ),
        "domain": "Environmental Science",
        "channels": [
            ("temperature", 0.82, 0.20, "°C normalized: (T - T_min) / (T_max - T_min)"),
            ("humidity", 0.65, 0.15, "Relative humidity / 100"),
            ("pressure", 0.91, 0.20, "Barometric: (P - 950) / (1050 - 950) hPa"),
            ("wind_speed", 0.45, 0.15, "Wind: min(v, v_max) / v_max"),
            ("visibility", 0.78, 0.15, "Visibility: min(d, 20km) / 20km"),
            ("uv_index", 0.33, 0.15, "UV: min(uv, 11) / 11"),
        ],
        "contract_notes": (
            "**Normalization**: All sensors map to [0,1] using domain bounds. "
            "Pressure uses 950-1050 hPa range. Wind caps at 100 km/h. "
            "**ε-policy**: Failed sensors clamp to ε = 10⁻⁸ (frozen). "
            "**Expected regime**: Stable when all sensors operational. "
            "Watch when 1-2 sensors degrade. Collapse on multi-sensor failure."
        ),
    },
    "Software Deployment": {
        "description": (
            "Monitoring a software release pipeline. Each channel tracks a deployment "
            "health dimension. The trace vector captures whether the system is returning "
            "to stable operation after a release (deployment = collapse event)."
        ),
        "domain": "DevOps / SRE",
        "channels": [
            ("error_rate", 0.95, 0.20, "1 - (errors/requests), high = healthy"),
            ("latency_p99", 0.72, 0.20, "1 - min(p99/budget, 1), budget=500ms"),
            ("cpu_headroom", 0.68, 0.15, "1 - (cpu_usage / cpu_limit)"),
            ("memory_headroom", 0.81, 0.15, "1 - (mem_usage / mem_limit)"),
            ("test_coverage", 0.88, 0.15, "Fraction of tests passing"),
            ("rollback_distance", 0.60, 0.15, "1 - (changes / max_changes)"),
        ],
        "contract_notes": (
            "**Interpretation**: A deployment is a collapse event. τ_R measures how many "
            "monitoring intervals until metrics return to pre-deploy baselines. "
            "**Drift** = how far metrics have moved from the healthy baseline. "
            "**Return** = demonstrated recovery (metrics back within SLO). "
            "**IC killer**: A single channel at ε (e.g., error_rate crash) triggers "
            "geometric slaughter — IC collapses even if other channels are fine."
        ),
    },
    "Clinical Trial Cohort": {
        "description": (
            "Tracking a clinical trial cohort across 5 measurable endpoints. "
            "Each endpoint is normalized against the expected therapeutic window. "
            "The kernel detects whether the cohort maintains coherence across all "
            "endpoints or shows heterogeneous response (high Δ = F - IC)."
        ),
        "domain": "Biomedical Research",
        "channels": [
            ("primary_endpoint", 0.74, 0.30, "Efficacy: response rate vs. target"),
            ("safety_score", 0.88, 0.25, "1 - (adverse_events / threshold)"),
            ("adherence", 0.91, 0.15, "Protocol adherence rate"),
            ("biomarker_response", 0.42, 0.15, "Biomarker change vs. expected"),
            ("retention", 0.85, 0.15, "Patient retention rate"),
        ],
        "contract_notes": (
            "**Heterogeneity gap matters**: F may look acceptable while IC reveals "
            "that one endpoint (e.g., biomarker at 0.42) is dragging coherence down. "
            "**NON_EVALUABLE**: If data is insufficient for an endpoint, the verdict "
            "is the third state — not 'pass' or 'fail' but 'cannot evaluate'. "
            "**Seam**: Each interim analysis is a seam crossing. Policy changes "
            "require a formal weld (pre/post tests, κ-continuity)."
        ),
    },
    "Supply Chain Resilience": {
        "description": (
            "Measuring supply chain resilience across 7 dimensions. Each channel "
            "represents a measurable aspect of the supply network. The kernel "
            "reveals whether apparent average health (F) masks fragility in "
            "specific links (low IC from channel heterogeneity)."
        ),
        "domain": "Operations / Logistics",
        "channels": [
            ("supplier_diversity", 0.62, 0.15, "1 - HHI concentration index"),
            ("lead_time_reliability", 0.78, 0.15, "On-time delivery fraction"),
            ("inventory_coverage", 0.85, 0.15, "Days of supply / target days"),
            ("transport_redundancy", 0.55, 0.10, "Alternative routes / total"),
            ("quality_yield", 0.92, 0.15, "Acceptance rate at inspection"),
            ("cost_stability", 0.71, 0.15, "1 - |ΔP/P| over period"),
            ("demand_forecast_accuracy", 0.68, 0.15, "1 - MAPE"),
        ],
        "contract_notes": (
            "**The gap is the insight**: A supply chain with F=0.73 (looks okay) but "
            "IC=0.45 (one link is fragile) has Δ=0.28 — the average hides the risk. "
            "**Transport redundancy** at 0.55 with weight 0.10 is the IC killer here. "
            "Even at low weight, the geometric mean punishes it. "
            "**Regime interpretation**: Stable = resilient network. Watch = monitor fragile links. "
            "Collapse = critical path failure imminent."
        ),
    },
    "Student Learning Assessment": {
        "description": (
            "Assessing student learning coherence across 6 competency dimensions. "
            "Each channel measures demonstrated proficiency normalized to [0,1]. "
            "The kernel reveals whether learning is uniform (IC ≈ F, low Δ) or "
            "whether excellence in some areas masks gaps in others."
        ),
        "domain": "Education / Assessment",
        "channels": [
            ("conceptual_understanding", 0.81, 0.20, "Conceptual assessment score"),
            ("procedural_fluency", 0.77, 0.15, "Procedural skill score"),
            ("problem_solving", 0.65, 0.20, "Novel problem performance"),
            ("communication", 0.88, 0.15, "Written/oral explanation quality"),
            ("collaboration", 0.72, 0.15, "Peer assessment of teamwork"),
            ("self_regulation", 0.58, 0.15, "Metacognitive skill score"),
        ],
        "contract_notes": (
            "**F vs IC tells the story**: A student with F=0.74 (B-grade average) and "
            "IC=0.71 (coherent across channels) is in a different position than F=0.74 "
            "with IC=0.35 (brilliant at some, struggling at others). "
            "**Self-regulation** at 0.58 is the weakest channel. If it drops further, "
            "geometric slaughter begins — overall coherence degrades faster than the "
            "average suggests. "
            "**Return**: Demonstrated improvement over time = re-entry to higher IC. "
            "τ_R measures how many assessment cycles until coherence is restored."
        ),
    },
}


def render_work_template_page() -> None:
    """Render the Work Template page — guided domain closure implementation.

    Provides 5 full worked examples showing how to take a real-world domain,
    define channels, compute kernel invariants, and interpret the results
    through the GCD lens. Each example is a complete, runnable spine traversal.
    """
    if st is None or np is None or pd is None:
        return

    st.title("📐 Work Templates")
    st.caption(
        "Guided examples for implementing your own domain closure — 5 complete worked examples from diverse fields"
    )

    # ========== Introduction ==========
    st.markdown("""
    **What is a Work Template?** A step-by-step guide for taking *your* domain data,
    encoding it as a trace vector, running it through the GCD kernel, and reading the
    results. Each example below is a complete implementation — from channel definition
    through kernel computation to verdict interpretation.

    **The pattern is always the same** (the Spine):

    1. **Contract** — Define your channels, normalization, and weights *before* looking at data
    2. **Canon** — Compute F, ω, S, C, κ, IC from the trace vector
    3. **Closures** — Apply regime gates and seam budget
    4. **Integrity Ledger** — Verify identities (F + ω = 1, IC ≤ F, IC = exp(κ))
    5. **Stance** — Read the verdict: Stable / Watch / Collapse
    """)

    st.info(
        "💡 **Quick start**: Pick an example below that's closest to your domain, "
        "then modify the channels and weights for your data."
    )

    st.divider()

    # ========== Example Selector ==========
    example_names = list(_WORK_TEMPLATE_EXAMPLES.keys())
    selected_example = st.selectbox(
        "Select a worked example",
        example_names,
        help="Each example includes full channel definitions, computation, and interpretation",
    )

    example = _WORK_TEMPLATE_EXAMPLES[selected_example]

    # ========== Example Header ==========
    st.markdown(f"## 📋 Example: {selected_example}")
    st.markdown(f"**Domain**: {example['domain']}")
    st.markdown(example["description"])

    st.divider()

    # ========== STOP 1: Contract ==========
    st.markdown("### 🔒 Stop 1: Contract (*Liga*)")
    st.markdown(
        "Define channels, normalization rules, and weights **before** examining data. "
        "The contract is frozen for the duration of the analysis."
    )

    with st.expander("📖 Contract Notes", expanded=True):
        st.markdown(example["contract_notes"])

    # Channel table with editable values
    st.markdown("#### Channel Definitions")

    channels = example["channels"]
    channel_names = [ch[0] for ch in channels]
    channel_defaults = [ch[1] for ch in channels]
    channel_weights = [ch[2] for ch in channels]
    channel_descs = [ch[3] for ch in channels]

    # Allow users to modify values
    n_ch = len(channels)
    edited_values: list[float] = []
    edited_weights: list[float] = []

    # Display as a structured table with inputs
    for i in range(0, n_ch, 3):
        cols = st.columns(min(3, n_ch - i))
        for j, col in enumerate(cols):
            idx = i + j
            if idx < n_ch:
                with col, st.container(border=True):
                    st.markdown(f"**{channel_names[idx]}**")
                    st.caption(channel_descs[idx])
                    val = st.number_input(
                        "Value",
                        min_value=0.0,
                        max_value=1.0,
                        value=float(channel_defaults[idx]),
                        step=0.01,
                        format="%.3f",
                        key=f"wt_{selected_example}_{idx}_v",
                    )
                    wt = st.number_input(
                        "Weight",
                        min_value=0.0,
                        max_value=1.0,
                        value=float(channel_weights[idx]),
                        step=0.01,
                        format="%.3f",
                        key=f"wt_{selected_example}_{idx}_w",
                    )
                    edited_values.append(val)
                    edited_weights.append(wt)

    # Weight normalization
    w_sum = sum(edited_weights)
    if abs(w_sum - 1.0) > 1e-6:
        st.warning(f"⚠️ Weights sum to {w_sum:.4f} — normalizing to 1.0")
        edited_weights = [w / w_sum for w in edited_weights]

    # Frozen parameters display
    st.markdown("#### Frozen Parameters (*Trans Suturam Congelatum*)")
    param_cols = st.columns(5)
    frozen_labels = [
        ("ε", "1e-8", "Guard band"),
        ("p", "3", "Drift exponent"),
        ("α", "1.0", "Curvature cost"),
        ("tol_seam", "0.005", "Seam tolerance"),
        ("c*", "0.7822", "Self-dual fixed point"),
    ]
    for col, (sym, val, desc) in zip(param_cols, frozen_labels, strict=False):
        with col:
            st.metric(sym, val, help=desc)

    st.divider()

    # ========== STOP 2: Canon — Compute kernel ==========
    st.markdown("### ⚙️ Stop 2: Canon (*Dic*)")
    st.markdown("Compute the six kernel invariants from the trace vector.")

    c_arr = np.array(edited_values)
    w_arr = np.array(edited_weights)

    # Epsilon clamp — frozen parameter from contract
    from umcp.frozen_contract import EPSILON

    c_clamped = np.clip(c_arr, EPSILON, 1.0 - EPSILON)

    # Compute kernel invariants
    if _HAS_KERNEL:
        computer = OptimizedKernelComputer(epsilon=EPSILON)
        outputs = computer.compute(c_clamped, w_arr)
        F = outputs.F
        omega = outputs.omega
        S = outputs.S
        C = outputs.C
        kappa = outputs.kappa
        IC = outputs.IC
        het_gap = outputs.heterogeneity_gap
    else:
        F = float(np.sum(w_arr * c_clamped))
        omega = 1.0 - F
        kappa = float(np.sum(w_arr * np.log(c_clamped)))
        IC = float(np.exp(kappa))
        S = 0.0
        for ci, wi in zip(c_clamped, w_arr, strict=False):
            if wi > 0 and 0 < ci < 1:
                S += wi * (-ci * np.log(ci) - (1 - ci) * np.log(1 - ci))
        S = float(S)
        C = float(np.std(c_clamped, ddof=0) / 0.5)
        het_gap = F - IC

    # Display invariants
    inv_cols = st.columns(6)
    invariant_data = [
        ("F", F, "Fidelity — what survived"),
        ("ω", omega, "Drift — what was lost"),
        ("S", S, "Bernoulli field entropy"),
        ("C", C, "Curvature — channel coupling"),
        ("κ", kappa, "Log-integrity"),
        ("IC", IC, "Integrity composite"),
    ]
    for col, (sym, val, desc) in zip(inv_cols, invariant_data, strict=False):
        with col:
            st.metric(sym, f"{val:.6f}", help=desc)

    st.metric("Δ (heterogeneity gap)", f"{het_gap:.6f}", help="F − IC: how much the average hides")

    # Bar chart of channels
    if pd is not None:
        ch_df = pd.DataFrame(
            {
                "Channel": channel_names[: len(edited_values)],
                "Value": edited_values,
                "Weight": edited_weights,
            }
        )
        st.bar_chart(ch_df.set_index("Channel")["Value"], use_container_width=True)

    st.divider()

    # ========== STOP 3: Closures — Regime gates ==========
    st.markdown("### 📏 Stop 3: Closures (*Reconcilia*)")
    st.markdown("Apply the four-gate regime classification and seam budget.")

    # Regime gates
    gate_omega = omega < 0.038
    gate_F = F > 0.90
    gate_S = S < 0.15
    gate_C = C < 0.14
    all_stable = gate_omega and gate_F and gate_S and gate_C

    if all_stable:
        regime = "STABLE"
    elif omega >= 0.30:
        regime = "COLLAPSE"
    else:
        regime = "WATCH"

    critical_overlay = IC < 0.30

    # Gate display
    gate_cols = st.columns(4)
    gates = [
        ("ω < 0.038", gate_omega, f"ω = {omega:.4f}"),
        ("F > 0.90", gate_F, f"F = {F:.4f}"),
        ("S < 0.15", gate_S, f"S = {S:.4f}"),
        ("C < 0.14", gate_C, f"C = {C:.4f}"),
    ]
    for col, (label, passed, detail) in zip(gate_cols, gates, strict=False):
        with col:
            icon = "✅" if passed else "❌"
            st.markdown(f"{icon} **{label}**")
            st.caption(detail)

    # Regime badge
    regime_colors = {"STABLE": "#28a745", "WATCH": "#ffc107", "COLLAPSE": "#dc3545"}
    color = regime_colors.get(regime, "#6c757d")
    st.markdown(
        f'<div style="padding: 12px; border-left: 6px solid {color}; '
        f'background: {color}22; border-radius: 8px; margin: 10px 0;">'
        f'<h3 style="margin: 0; color: {color};">Regime: {regime}'
        f"{'  ⚠️ CRITICAL' if critical_overlay else ''}</h3>"
        f"</div>",
        unsafe_allow_html=True,
    )

    # Seam budget
    gamma = omega**3 / (1 - omega + EPSILON)
    d_c = 1.0 * C  # α = 1.0
    total_debit = gamma + d_c

    budget_cols = st.columns(3)
    with budget_cols[0]:
        st.metric("Γ(ω)", f"{gamma:.6f}", help="Drift cost: ω³/(1-ω+ε)")
    with budget_cols[1]:
        st.metric("D_C", f"{d_c:.6f}", help="Curvature debit: α·C")
    with budget_cols[2]:
        st.metric("Total Debit", f"{total_debit:.6f}", help="Γ(ω) + D_C")

    st.divider()

    # ========== STOP 4: Integrity Ledger ==========
    st.markdown("### 📒 Stop 4: Integrity Ledger (*Inscribe*)")
    st.markdown("Verify the three algebraic identities — these must hold by construction.")

    id_1_residual = abs(F + omega - 1.0)
    id_2_holds = IC <= F + 1e-12
    id_3_residual = abs(IC - np.exp(kappa))

    check_cols = st.columns(3)
    with check_cols[0]:
        icon = "✅" if id_1_residual < 1e-9 else "❌"
        st.markdown(f"{icon} **F + ω = 1** (duality identity)")
        st.caption(f"|residual| = {id_1_residual:.2e}")
    with check_cols[1]:
        icon = "✅" if id_2_holds else "❌"
        st.markdown(f"{icon} **IC ≤ F** (integrity bound)")
        st.caption(f"IC = {IC:.6f}, F = {F:.6f}")
    with check_cols[2]:
        icon = "✅" if id_3_residual < 1e-9 else "❌"
        st.markdown(f"{icon} **IC = exp(κ)** (log-integrity relation)")
        st.caption(f"|residual| = {id_3_residual:.2e}")

    st.divider()

    # ========== STOP 5: Stance ==========
    st.markdown("### 📜 Stop 5: Stance (*Sententia*)")
    st.markdown("The verdict is **derived**, never asserted.")

    verdict_all_pass = id_1_residual < 1e-9 and id_2_holds and id_3_residual < 1e-9
    verdict = "CONFORMANT" if verdict_all_pass else "NONCONFORMANT"

    st.markdown(
        f'<div style="padding: 16px; border: 2px solid {"#28a745" if verdict_all_pass else "#dc3545"}; '
        f'border-radius: 8px; text-align: center; margin: 10px 0;">'
        f'<h2 style="margin: 0;">{"✅" if verdict_all_pass else "❌"} {verdict}</h2>'
        f'<p style="margin: 5px 0 0 0;">Regime: {regime} · Δ = {het_gap:.4f} · '
        f"IC/F = {IC / F:.4f}</p></div>",
        unsafe_allow_html=True,
    )

    # Interpretation in context
    st.markdown("#### 📖 Domain Interpretation")

    # Identify weakest channel
    min_idx = int(np.argmin(c_clamped))
    min_name = channel_names[min_idx] if min_idx < len(channel_names) else f"c_{min_idx + 1}"
    min_val = float(c_clamped[min_idx])

    ic_f_ratio = IC / F if F > 0 else 0

    if regime == "STABLE":
        st.success(
            f"**{selected_example}** is in a **Stable** regime. All channels are healthy, "
            f"coherence is high (IC/F = {ic_f_ratio:.3f}), and drift is minimal. "
            f"The weakest channel is **{min_name}** at {min_val:.3f} — monitor it for degradation."
        )
    elif regime == "WATCH":
        st.warning(
            f"**{selected_example}** is in a **Watch** regime. "
            f"Drift ω = {omega:.4f} indicates the system has moved from its baseline. "
            f"The heterogeneity gap Δ = {het_gap:.4f} suggests {'some channels are weaker than the average implies' if het_gap > 0.05 else 'channels are relatively uniform'}. "
            f"The weakest channel (**{min_name}** = {min_val:.3f}) is the primary IC drag."
        )
    else:
        st.error(
            f"**{selected_example}** is in a **Collapse** regime. "
            f"Drift ω = {omega:.4f} exceeds the 0.30 threshold. "
            f"{'IC is critically low (' + f'{IC:.4f}' + ')' if critical_overlay else ''} "
            f"The geometric mean has been destroyed by channel heterogeneity — "
            f"**{min_name}** at {min_val:.3f} is the primary cause."
        )

    st.divider()

    # ========== Implementation Guide ==========
    st.markdown("### 🛠️ Implement This in Your Code")
    st.markdown("Copy this minimal implementation to apply the GCD kernel to your own data.")

    code_channels = ", ".join([f'"{n}"' for n in channel_names[: len(edited_values)]])
    code_values = ", ".join([f"{v:.3f}" for v in edited_values])
    code_weights = ", ".join([f"{w:.3f}" for w in edited_weights])

    st.code(
        f'''"""
{selected_example} — GCD Kernel Implementation
Domain: {example["domain"]}
"""
from umcp.kernel_optimized import OptimizedKernelComputer
from umcp.frozen_contract import EPSILON
import numpy as np

# --- Stop 1: Contract (freeze before evidence) ---
channels = [{code_channels}]
c = np.array([{code_values}])           # trace vector
w = np.array([{code_weights}])           # weights (sum = 1)

# --- Stop 2: Canon (compute kernel) ---
computer = OptimizedKernelComputer(epsilon=EPSILON)
result = computer.compute(np.clip(c, EPSILON, 1 - EPSILON), w)

print(f"F  = {{result.F:.6f}}")           # Fidelity
print(f"ω  = {{result.omega:.6f}}")       # Drift
print(f"S  = {{result.S:.6f}}")           # Bernoulli field entropy
print(f"C  = {{result.C:.6f}}")           # Curvature
print(f"κ  = {{result.kappa:.6f}}")       # Log-integrity
print(f"IC = {{result.IC:.6f}}")          # Integrity composite
print(f"Δ  = {{result.heterogeneity_gap:.6f}}")  # Het gap

# --- Stop 3: Closures (regime gates) ---
stable = (result.omega < 0.038 and result.F > 0.90
          and result.S < 0.15 and result.C < 0.14)
regime = "STABLE" if stable else "COLLAPSE" if result.omega >= 0.30 else "WATCH"
print(f"Regime: {{regime}}")

# --- Stop 4: Ledger (verify identities) ---
assert abs(result.F + result.omega - 1.0) < 1e-9, "Duality violated"
assert result.IC <= result.F + 1e-12, "Integrity bound violated"
assert abs(result.IC - np.exp(result.kappa)) < 1e-9, "Log-integrity violated"

# --- Stop 5: Stance ---
print("CONFORMANT — all identities hold")
''',
        language="python",
    )

    st.divider()

    # ========== All Examples Reference ==========
    st.markdown("### 📚 All Work Template Examples")

    for name, ex in _WORK_TEMPLATE_EXAMPLES.items():
        icon = "📌" if name == selected_example else "📋"
        with st.expander(f"{icon} {name} — {ex['domain']}", expanded=False):
            st.markdown(ex["description"])
            ch_data = []
            for ch_name, ch_val, ch_wt, ch_desc in ex["channels"]:
                ch_data.append(
                    {
                        "Channel": ch_name,
                        "Default Value": f"{ch_val:.3f}",
                        "Weight": f"{ch_wt:.3f}",
                        "Description": ch_desc,
                    }
                )
            if pd is not None:
                st.dataframe(
                    pd.DataFrame(ch_data),
                    use_container_width=True,
                    hide_index=True,
                )
