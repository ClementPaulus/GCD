"""
Diagnostic dashboard pages: τ_R* Thermodynamics, Epistemic Classification, Insights Engine.

These pages integrate three previously untapped core engine modules into the
dashboard, providing deep visibility into GCD's diagnostic machinery:

- tau_r_star.py     → Phase diagram, arrow of time, trapping analysis
- epistemic_weld.py → RETURN/GESTURE/DISSOLUTION trichotomy, positional illusion
- insights.py       → Pattern discovery, cross-domain correlations

Tier Architecture:
    All pages read Tier-1 kernel outputs and produce Tier-2 diagnostics.
    No back-edges: nothing on these pages modifies Tier-0 or Tier-1.
"""
# pyright: reportUnknownMemberType=false
# pyright: reportUnknownVariableType=false
# pyright: reportUnknownArgumentType=false
# pyright: reportOptionalMemberAccess=false
# pyright: reportMissingTypeStubs=false

from __future__ import annotations

from typing import Any

from umcp.dashboard._deps import go, np, pd, st

# ============================================================================
# Page 1: τ_R* Thermodynamic Diagnostic
# ============================================================================


def render_tau_r_star_page() -> None:
    """Render the τ_R* Thermodynamic Diagnostic page.

    Integrates tau_r_star.py to provide:
    - Interactive τ_R* computation from kernel state
    - Phase diagram (ω vs C with phase coloring)
    - Budget decomposition (Γ vs αC vs Δκ dominance)
    - Arrow of time visualization (degradation vs improvement asymmetry)
    - Trapping threshold analysis
    - R_critical and R_min computation
    """
    if st is None:
        return
    if go is None or np is None or pd is None:
        st.error(
            "Dashboard dependencies (numpy, pandas, plotly) could not be loaded. Install with: `pip install umcp[viz]`"
        )
        return

    st.title("🌡️ τ_R* Thermodynamic Diagnostic")
    st.caption("Phase classification • Budget decomposition • Arrow of time • Trapping analysis")

    # Import engine modules
    try:
        from umcp.frozen_contract import (
            ALPHA,
            TOL_SEAM,
            gamma_omega,
        )
        from umcp.tau_r_star import (
            ThermodynamicPhase,
            compute_R_critical,
            compute_R_min,
            compute_tau_R_star,
            compute_trapping_threshold,
        )
    except ImportError:
        st.error("Required modules not available: tau_r_star, frozen_contract")
        return

    # ========== Theory Panel ==========
    with st.expander("📖 τ_R* Theory (Budget Identity)", expanded=False):
        st.markdown(r"""
        **Definition T1**: The critical return delay is:

        $$\tau_R^* = \frac{\Gamma(\omega) + \alpha C + \Delta\kappa}{R}$$

        where:
        - $\Gamma(\omega) = \frac{\omega^p}{1 - \omega + \varepsilon}$ — drift cost (simple pole at $\omega = 1$)
        - $\alpha C$ — curvature cost (coupling to uncontrolled degrees of freedom)
        - $\Delta\kappa$ — memory/degradation term (arrow of time)
        - $R$ — return rate (the only externally controllable variable)

        **Phase classification** (Theorem T2):
        - **SURPLUS** ($\tau_R^* < 0$): System generates budget credit — spontaneous return
        - **FREE_RETURN** ($\tau_R^* \approx 0$): Break-even surface
        - **DEFICIT** ($\tau_R^* > 0$): Return costs more than budget allows
        - **TRAPPED** ($\tau_R^* > 0$ AND no single-step escape): Structural intervention required
        - **POLE** ($\omega \to 1$): $\Gamma$ diverges — information cannot return

        **Frozen parameters**: $p = 3$, $\alpha = 1.0$, $\varepsilon = 10^{-8}$, $\text{tol\_seam} = 0.005$
        """)

    st.divider()

    # ========== Interactive State Input ==========
    st.subheader("🎛️ State Input")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        omega_input = st.slider(
            "ω (Drift)",
            0.001,
            0.999,
            0.15,
            0.001,
            help="Drift proxy = 1 − F",
            key="tau_omega",
        )
    with col2:
        C_input = st.slider(
            "C (Curvature)",
            0.0,
            1.0,
            0.10,
            0.01,
            help="Curvature proxy = std(cᵢ)/0.5",
            key="tau_C",
        )
    with col3:
        R_input = st.slider(
            "R (Return Rate)",
            0.001,
            0.5,
            0.05,
            0.001,
            help="Return credit rate (external)",
            key="tau_R_rate",
        )
    with col4:
        dk_input = st.slider(
            "Δκ (Memory)",
            -0.5,
            0.5,
            0.0,
            0.01,
            help="Memory term κ(t₁) − κ(t₀)",
            key="tau_dk",
        )

    # ========== Compute τ_R* ==========
    result = compute_tau_R_star(omega_input, C_input, R_input, dk_input)
    R_crit = compute_R_critical(omega_input, C_input, dk_input)
    R_min_val = compute_R_min(omega_input, C_input, tau_R_target=1.0, delta_kappa=dk_input)
    c_trap = compute_trapping_threshold()

    # Phase classification
    if omega_input > 1.0 - 1e-4:
        phase = ThermodynamicPhase.POLE
    elif abs(result.tau_R_star) < 1e-6:
        phase = ThermodynamicPhase.FREE_RETURN
    elif result.tau_R_star < 0:
        phase = ThermodynamicPhase.SURPLUS
    elif (1 - omega_input) < c_trap:
        phase = ThermodynamicPhase.TRAPPED
    else:
        phase = ThermodynamicPhase.DEFICIT

    # Phase colors
    phase_colors = {
        ThermodynamicPhase.SURPLUS: "#28a745",
        ThermodynamicPhase.DEFICIT: "#ffc107",
        ThermodynamicPhase.FREE_RETURN: "#17a2b8",
        ThermodynamicPhase.TRAPPED: "#dc3545",
        ThermodynamicPhase.POLE: "#6f42c1",
    }
    phase_color = phase_colors.get(phase, "#6c757d")

    # ========== Result Display ==========
    st.subheader("📊 Diagnostic Results")

    # Phase banner
    st.markdown(
        f"""
    <div style="background-color: {phase_color}22; border-left: 4px solid {phase_color};
                padding: 15px; border-radius: 5px; margin-bottom: 15px;">
        <h2 style="color: {phase_color}; margin: 0;">Phase: {phase.value}</h2>
        <p style="margin: 5px 0 0 0; font-family: monospace; font-size: 1.1em;">
            τ_R* = {result.tau_R_star:.6f}
        </p>
    </div>
    """,
        unsafe_allow_html=True,
    )

    # Metrics row
    m1, m2, m3, m4, m5 = st.columns(5)
    with m1:
        st.metric("τ_R*", f"{result.tau_R_star:.4f}")
    with m2:
        st.metric("Γ(ω)", f"{result.gamma:.6f}")
    with m3:
        st.metric("αC", f"{result.D_C:.4f}")
    with m4:
        st.metric("R_critical", f"{R_crit:.4f}")
    with m5:
        st.metric("c_trap", f"{c_trap:.4f}")

    st.divider()

    # ========== Budget Decomposition ==========
    st.subheader("🔬 Budget Decomposition")

    decomp_col1, decomp_col2 = st.columns([2, 1])

    with decomp_col1:
        # Pie chart of budget terms
        numerator_parts = {
            "Γ(ω) — Drift Cost": result.gamma,
            "αC — Curvature Cost": result.D_C,
        }
        if dk_input != 0:
            numerator_parts["|Δκ| — Memory"] = abs(dk_input)

        labels = list(numerator_parts.keys())
        values = list(numerator_parts.values())
        colors = ["#dc3545", "#ffc107", "#17a2b8"]

        fig_pie = go.Figure(
            data=[
                go.Pie(
                    labels=labels,
                    values=values,
                    marker={"colors": colors[: len(values)]},
                    textinfo="label+percent",
                    hovertemplate="%{label}<br>Value: %{value:.6f}<extra></extra>",
                )
            ]
        )
        fig_pie.update_layout(height=300, title="Budget Term Dominance")
        st.plotly_chart(fig_pie, use_container_width=True)

    with decomp_col2:
        # Dominance classification
        terms = {"Γ(ω)": result.gamma, "αC": result.D_C, "Δκ": abs(dk_input)}
        dominant = max(terms, key=lambda k: terms[k])

        st.markdown("##### Dominance Analysis")
        for name, val in terms.items():
            frac = val / result.numerator * 100 if result.numerator > 0 else 0
            st.markdown(f"**{name}**: {val:.6f} ({frac:.1f}%)")
            st.progress(min(frac / 100, 1.0))

        st.info(f"**Dominant term**: {dominant}")

        # Regime-dependent expectation
        if omega_input < 0.038:
            expected = "Δκ (STABLE regime)"
        elif omega_input < 0.30:
            expected = "αC (WATCH regime)"
        else:
            expected = "Γ(ω) (COLLAPSE regime)"

        st.caption(f"Theorem T1 expects: {expected}")

    st.divider()

    # ========== Phase Diagram ==========
    st.subheader("🗺️ Phase Diagram")

    st.markdown("""
    The phase diagram shows τ_R* over the (ω, C) plane at fixed R and Δκ.
    The **free-return surface** (τ_R* = 0) separates surplus from deficit.
    """)

    # Compute phase surface
    omega_range = np.linspace(0.001, 0.999, 80)
    C_range = np.linspace(0.0, 0.8, 60)
    tau_grid = np.zeros((len(C_range), len(omega_range)))

    for i, c_val in enumerate(C_range):
        for j, om_val in enumerate(omega_range):
            r = compute_tau_R_star(om_val, c_val, R_input, dk_input)
            tau_grid[i, j] = np.clip(r.tau_R_star, -5, 50)

    fig_phase = go.Figure(
        data=go.Heatmap(
            x=omega_range,
            y=C_range,
            z=tau_grid,
            colorscale="RdYlGn_r",
            zmin=-2,
            zmax=10,
            colorbar={"title": "τ_R*"},
            hovertemplate="ω=%{x:.3f}<br>C=%{y:.3f}<br>τ_R*=%{z:.4f}<extra></extra>",
        )
    )

    # Add contour at τ_R* = 0 (free-return surface)
    fig_phase.add_trace(
        go.Contour(
            x=omega_range,
            y=C_range,
            z=tau_grid,
            contours={
                "start": 0,
                "end": 0,
                "size": 1,
                "showlabels": True,
            },
            line={"width": 3, "color": "white"},
            showscale=False,
            name="Free Return (τ_R* = 0)",
        )
    )

    # Mark current state
    fig_phase.add_trace(
        go.Scatter(
            x=[omega_input],
            y=[C_input],
            mode="markers",
            marker={"size": 15, "color": phase_color, "symbol": "x", "line": {"width": 2, "color": "white"}},
            name="Current State",
        )
    )

    # Regime boundaries
    fig_phase.add_vline(x=0.038, line_dash="dash", line_color="green", annotation_text="STABLE|WATCH")
    fig_phase.add_vline(x=0.30, line_dash="dash", line_color="red", annotation_text="WATCH|COLLAPSE")

    fig_phase.update_layout(
        height=500,
        xaxis_title="ω (Drift)",
        yaxis_title="C (Curvature)",
        title=f"Phase Diagram (R={R_input}, Δκ={dk_input})",
    )
    st.plotly_chart(fig_phase, use_container_width=True)

    st.divider()

    # ========== Arrow of Time ==========
    st.subheader("⏳ Arrow of Time (Theorem T7)")

    st.markdown("""
    **Second Law analog**: Degradation is free (releases surplus); improvement costs time.
    At $c = 0.60$, improvement costs ~200× more than degradation.
    The arrow emerges from budget arithmetic — no postulate required.
    """)

    arrow_col1, arrow_col2 = st.columns(2)

    with arrow_col1:
        # Γ(ω) curve — the drift cost function
        om_sweep = np.linspace(0.001, 0.999, 200)
        gamma_vals = [gamma_omega(om) for om in om_sweep]

        fig_gamma = go.Figure()
        fig_gamma.add_trace(
            go.Scatter(
                x=om_sweep,
                y=gamma_vals,
                mode="lines",
                line={"color": "#dc3545", "width": 2},
                name="Γ(ω)",
                hovertemplate="ω=%{x:.3f}<br>Γ=%{y:.6f}<extra></extra>",
            )
        )

        # Mark current state
        g_current = gamma_omega(omega_input)
        fig_gamma.add_trace(
            go.Scatter(
                x=[omega_input],
                y=[g_current],
                mode="markers",
                marker={"size": 12, "color": phase_color, "symbol": "diamond"},
                name=f"Current (ω={omega_input:.3f})",
            )
        )

        # Regime boundaries
        fig_gamma.add_vline(x=0.038, line_dash="dot", line_color="green")
        fig_gamma.add_vline(x=0.30, line_dash="dot", line_color="red")

        fig_gamma.update_layout(
            height=350,
            xaxis_title="ω (Drift)",
            yaxis_title="Γ(ω)",
            title="Drift Cost Function Γ(ω) = ω³/(1−ω+ε)",
            yaxis_type="log",
        )
        st.plotly_chart(fig_gamma, use_container_width=True)

    with arrow_col2:
        # Improvement vs degradation asymmetry
        c_values = np.linspace(0.1, 0.95, 50)
        improvement_cost = []
        degradation_cost = []

        for c_val in c_values:
            omega_val = 1 - c_val
            dc = 0.05  # Small step
            # Improvement: c → c + dc (ω decreases)
            if c_val + dc < 1.0:
                g_before = gamma_omega(omega_val)
                improvement_cost.append(g_before + ALPHA * C_input)
            else:
                improvement_cost.append(float("nan"))

            # Degradation: c → c - dc (ω increases)
            if c_val - dc > 0.0:
                g_degrade = gamma_omega(1 - (c_val - dc))
                degradation_cost.append(g_degrade + ALPHA * C_input)
            else:
                degradation_cost.append(float("nan"))

        fig_arrow = go.Figure()
        fig_arrow.add_trace(
            go.Scatter(
                x=c_values,
                y=improvement_cost,
                mode="lines",
                name="Improvement Cost",
                line={"color": "#28a745", "width": 2},
            )
        )
        fig_arrow.add_trace(
            go.Scatter(
                x=c_values,
                y=degradation_cost,
                mode="lines",
                name="Degradation Cost",
                line={"color": "#dc3545", "width": 2, "dash": "dash"},
            )
        )

        fig_arrow.update_layout(
            height=350,
            xaxis_title="Fidelity c",
            yaxis_title="Budget Cost",
            title="Arrow of Time: Improvement vs Degradation",
            yaxis_type="log",
        )
        st.plotly_chart(fig_arrow, use_container_width=True)

    st.divider()

    # ========== Trapping Analysis ==========
    st.subheader("🪤 Trapping Threshold (Theorem T3)")

    trap_col1, trap_col2 = st.columns([1, 1])

    with trap_col1:
        F_current = 1 - omega_input
        is_trapped = F_current < c_trap

        st.markdown(f"""
        **Trapping threshold**: c_trap = {c_trap:.4f} (ω_trap = {1 - c_trap:.4f})

        Below c_trap, no single-step curvature correction can achieve τ_R* ≤ 0.
        The system is **trapped** — structural intervention (not incremental
        improvement) is required.

        **Current state**: F = {F_current:.4f} {"< c_trap ⚠️ TRAPPED" if is_trapped else "≥ c_trap ✅ Recoverable"}
        """)

        st.metric(
            "R_critical",
            f"{R_crit:.4f}",
            help="Minimum R for seam viability (Theorem T4)",
        )
        st.metric(
            "R_min (τ_R=1)",
            f"{R_min_val:.4f}",
            help="Minimum R to close seam with τ_R = 1 (Theorem T5)",
        )

    with trap_col2:
        # R_min divergence
        om_for_rmin = np.linspace(0.01, 0.9, 100)
        rmin_vals = []
        for om_val in om_for_rmin:
            rm = compute_R_min(om_val, C_input, tau_R_target=1.0)
            rmin_vals.append(min(rm, 1000))  # Cap for display

        fig_rmin = go.Figure()
        fig_rmin.add_trace(
            go.Scatter(
                x=om_for_rmin,
                y=rmin_vals,
                mode="lines",
                line={"color": "#6f42c1", "width": 2},
                name="R_min(ω)",
            )
        )
        fig_rmin.add_vline(x=1 - c_trap, line_dash="dash", line_color="red", annotation_text="ω_trap")
        fig_rmin.update_layout(
            height=300,
            xaxis_title="ω (Drift)",
            yaxis_title="R_min",
            title=f"R_min Divergence (C={C_input:.2f}, Theorem T5)",
            yaxis_type="log",
        )
        st.plotly_chart(fig_rmin, use_container_width=True)

    st.divider()

    # ========== Measurement Cost (Zeno Analog) ==========
    st.subheader("👁️ Measurement Cost (Theorem T9 — Zeno Analog)")

    st.markdown("""
    Each observation incurs Γ(ω) overhead. N observations of a stationary system
    cost N×Γ(ω). There is no vantage point outside the system from which collapse
    can be observed without cost.
    """)

    zeno_col1, zeno_col2 = st.columns(2)

    with zeno_col1:
        n_obs = st.slider(
            "Number of observations N", 1, 100, 10, key="n_obs_zeno", help="Observation count for Zeno cost"
        )
        gamma_current = gamma_omega(omega_input)
        total_cost = n_obs * gamma_current
        budget_fraction = total_cost / TOL_SEAM

        st.metric("Γ(ω) per observation", f"{gamma_current:.2e}")
        st.metric("Total cost (N×Γ)", f"{total_cost:.2e}")
        st.metric("Budget consumed", f"{budget_fraction * 100:.2f}%")

        if budget_fraction >= 1.0:
            st.error("⚠️ Observation alone exhausts seam budget — positional illusion is fatal")
        elif budget_fraction > 0.5:
            st.warning("⚠️ Observation consumes >50% of seam budget")
        else:
            st.success("✅ Observation cost is manageable")

    with zeno_col2:
        # Cost vs N
        n_range = np.arange(1, 101)
        costs = n_range * gamma_current

        fig_zeno = go.Figure()
        fig_zeno.add_trace(
            go.Scatter(
                x=n_range,
                y=costs,
                mode="lines",
                line={"color": "#17a2b8", "width": 2},
                name="N × Γ(ω)",
            )
        )
        fig_zeno.add_hline(y=TOL_SEAM, line_dash="dash", line_color="red", annotation_text="tol_seam")
        fig_zeno.add_trace(
            go.Scatter(
                x=[n_obs],
                y=[total_cost],
                mode="markers",
                marker={"size": 12, "color": "#dc3545", "symbol": "diamond"},
                name=f"N={n_obs}",
            )
        )
        fig_zeno.update_layout(
            height=300,
            xaxis_title="Number of Observations N",
            yaxis_title="Total Measurement Cost",
            title="Measurement Cost Accumulation",
        )
        st.plotly_chart(fig_zeno, use_container_width=True)


# ============================================================================
# Page 2: Epistemic Classification
# ============================================================================


def render_epistemic_page() -> None:
    """Render the Epistemic Classification page.

    Integrates epistemic_weld.py to provide:
    - Interactive RETURN/GESTURE/DISSOLUTION classification
    - Positional illusion severity mapping
    - Gesture anatomy (why seams fail)
    - Epistemic trace metadata viewer
    - Cross-regime epistemic landscape
    """
    if st is None:
        return
    if go is None or np is None or pd is None:
        st.error(
            "Dashboard dependencies (numpy, pandas, plotly) could not be loaded. Install with: `pip install umcp[viz]`"
        )
        return

    st.title("🔮 Epistemic Classification")
    st.caption("Return vs Gesture vs Dissolution • Positional illusion • Seam epistemology")

    # Import engine modules
    try:
        from umcp.epistemic_weld import (
            EpistemicVerdict,
            classify_epistemic_act,
            quantify_positional_illusion,
        )
        from umcp.frozen_contract import Regime
    except ImportError:
        st.error("Required module not available: epistemic_weld")
        return

    # ========== Theory Panel ==========
    with st.expander("📖 Epistemic Framework ('The Seam of Reality')", expanded=False):
        st.markdown(r"""
        **Core trichotomy** — every epistemic emission is exactly one of:

        | Verdict | Condition | Meaning |
        |---------|-----------|---------|
        | **RETURN** | Seam passes, τ_R finite, regime ≠ COLLAPSE | What came back is real |
        | **GESTURE** | Seam fails OR τ_R = ∞ | Emission without return — no epistemic credit |
        | **DISSOLUTION** | Regime = COLLAPSE (ω ≥ 0.30) | Trace degraded past viable return |

        **Positional Illusion**: The belief that one can observe without cost.
        Each observation costs Γ(ω). At severity ≥ 1.0, observation alone
        exhausts the seam budget.

        **Gesture Reasons**:
        - `SEAM_RESIDUAL_EXCEEDED`: |s| > tol_seam
        - `NO_FINITE_RETURN`: τ_R = ∞_rec
        - `IDENTITY_MISMATCH`: |I_post/I_pre − exp(Δκ)| ≥ tol_exp
        - `FROZEN_PARAMETER_DRIFT`: Parameters changed between collapse and return
        - `TIER0_INCOMPLETE`: Missing trace data

        *"Reality is not a property things possess; it is a verdict things earn by returning."*
        """)

    st.divider()

    # ========== Interactive Classifier ==========
    st.subheader("🎛️ Epistemic Classifier")

    class_col1, class_col2, class_col3 = st.columns(3)

    with class_col1:
        regime_str = st.selectbox(
            "Regime",
            ["STABLE", "WATCH", "COLLAPSE"],
            index=0,
            key="epist_regime",
            help="Current system regime label",
        )
        regime = Regime(regime_str)

    with class_col2:
        seam_pass = st.toggle("Seam Pass", value=True, key="epist_seam", help="Did the seam residual pass?")
        tau_R_val = st.number_input(
            "τ_R (Return Time)",
            min_value=0.0,
            max_value=1000.0,
            value=1.85,
            step=0.1,
            key="epist_tau",
        )

    with class_col3:
        use_inf = st.toggle("τ_R = ∞ (No Return)", value=False, key="epist_inf", help="Set τ_R = ∞_rec (no return)")
        if use_inf:
            tau_R_val = float("inf")

        seam_failures: list[str] = []
        if not seam_pass:
            failure_options = [
                "|s| > tol_seam",
                "INF_REC: not finite",
                "exp identity mismatch",
            ]
            seam_failures = st.multiselect("Failure Reasons", failure_options, key="epist_failures")

    # Classify
    verdict, reasons = classify_epistemic_act(
        seam_pass=seam_pass,
        tau_R=tau_R_val,
        regime=regime,
        seam_failures=seam_failures if seam_failures else None,
    )

    # Verdict colors
    verdict_colors = {
        EpistemicVerdict.RETURN: "#28a745",
        EpistemicVerdict.GESTURE: "#ffc107",
        EpistemicVerdict.DISSOLUTION: "#dc3545",
    }
    v_color = verdict_colors.get(verdict, "#6c757d")

    verdict_icons = {
        EpistemicVerdict.RETURN: "✅",
        EpistemicVerdict.GESTURE: "⚠️",
        EpistemicVerdict.DISSOLUTION: "💀",
    }
    v_icon = verdict_icons.get(verdict, "?")

    # Verdict display
    st.markdown(
        f"""
    <div style="background-color: {v_color}22; border: 3px solid {v_color};
                padding: 20px; border-radius: 10px; text-align: center; margin: 15px 0;">
        <h1 style="color: {v_color}; margin: 0;">{v_icon} {verdict.value.upper()}</h1>
        <p style="margin: 10px 0 0 0; font-size: 1.1em;">
            {
            "What came back is real — epistemic credit earned"
            if verdict == EpistemicVerdict.RETURN
            else "Emission without return — no epistemic standing"
            if verdict == EpistemicVerdict.GESTURE
            else "Trace degraded past return viability — boundary condition"
        }
        </p>
    </div>
    """,
        unsafe_allow_html=True,
    )

    if reasons:
        st.markdown("##### Gesture Reasons")
        for reason in reasons:
            st.warning(f"**{reason.value}**: {_gesture_reason_description(reason)}")

    st.divider()

    # ========== Positional Illusion Landscape ==========
    st.subheader("👁️ Positional Illusion Landscape")

    st.markdown("""
    The positional illusion quantifies how much budget is consumed by observation
    alone. At severity ≥ 1.0, the observer cannot even verify return.
    """)

    ill_input_cols = st.columns([1, 1])
    with ill_input_cols[0]:
        omega_pi = st.slider(
            "ω for illusion", 0.001, 0.99, 0.15, 0.001, key="pi_omega", help="Drift value for illusion analysis"
        )
    with ill_input_cols[1]:
        n_pi = st.slider("N observations", 1, 50, 5, key="pi_n", help="Number of observations to model")

    ill_col1, ill_col2 = st.columns([2, 1])

    with ill_col1:
        # Severity heatmap over (ω, N)
        om_range = np.linspace(0.001, 0.99, 80)
        n_range = np.arange(1, 51)
        severity_grid = np.zeros((len(n_range), len(om_range)))

        for i, n_val in enumerate(n_range):
            for j, om_val in enumerate(om_range):
                pi_grid = quantify_positional_illusion(om_val, n_observations=int(n_val))
                severity_grid[i, j] = min(pi_grid.illusion_severity, 5.0)

        fig_illusion = go.Figure(
            data=go.Heatmap(
                x=om_range,
                y=n_range,
                z=severity_grid,
                colorscale="Reds",
                zmin=0,
                zmax=2.0,
                colorbar={"title": "Severity"},
                hovertemplate="ω=%{x:.3f}<br>N=%{y}<br>Severity=%{z:.3f}<extra></extra>",
            )
        )

        # Severity = 1.0 contour (fatal line)
        fig_illusion.add_trace(
            go.Contour(
                x=om_range,
                y=n_range,
                z=severity_grid,
                contours={"start": 1.0, "end": 1.0, "size": 1},
                line={"width": 3, "color": "white"},
                showscale=False,
                name="Fatal (severity = 1.0)",
            )
        )

        # Add current-state marker
        fig_illusion.add_trace(
            go.Scatter(
                x=[omega_pi],
                y=[n_pi],
                mode="markers",
                marker={"size": 14, "color": "cyan", "symbol": "x", "line": {"width": 2, "color": "white"}},
                name="Current State",
                showlegend=True,
            )
        )

        fig_illusion.update_layout(
            height=400,
            xaxis_title="ω (Drift)",
            yaxis_title="N (Observations)",
            title="Positional Illusion Severity (white line = fatal threshold)",
        )
        st.plotly_chart(fig_illusion, use_container_width=True)

    with ill_col2:
        # Current state assessment
        pi = quantify_positional_illusion(omega_pi, n_observations=n_pi)

        st.metric("Γ(ω)", f"{pi.gamma:.2e}")
        st.metric("Total Cost", f"{pi.total_cost:.2e}")
        st.metric("Budget Fraction", f"{pi.budget_fraction * 100:.2f}%")

        severity_bar_color = (
            "#28a745" if pi.illusion_severity < 0.5 else "#ffc107" if pi.illusion_severity < 1.0 else "#dc3545"
        )
        st.markdown(
            f"""<div style="background: {severity_bar_color}33; padding: 10px;
            border-radius: 5px; text-align: center;">
            <b>Severity: {pi.illusion_severity:.3f}</b>
            {
                "<br>✅ Affordable"
                if pi.illusion_severity < 0.5
                else "<br>⚠️ Significant"
                if pi.illusion_severity < 1.0
                else "<br>💀 Fatal"
            }
            </div>""",
            unsafe_allow_html=True,
        )

    st.divider()

    # ========== Epistemic Landscape ==========
    st.subheader("🗺️ Epistemic Verdict Landscape")

    st.markdown("""
    Verdict map across (ω, τ_R) space. Shows where each of the three
    verdicts dominates when the seam residual is within tolerance.
    """)

    om_land = np.linspace(0.001, 0.60, 100)
    tau_land = np.linspace(0.1, 20.0, 80)
    verdict_grid = np.zeros((len(tau_land), len(om_land)))

    for i, tau_val in enumerate(tau_land):
        for j, om_val in enumerate(om_land):
            if om_val >= 0.30:
                regime_l = Regime.COLLAPSE
            elif om_val >= 0.038:
                regime_l = Regime.WATCH
            else:
                regime_l = Regime.STABLE

            v, _ = classify_epistemic_act(seam_pass=True, tau_R=tau_val, regime=regime_l)
            if v == EpistemicVerdict.RETURN:
                verdict_grid[i, j] = 0
            elif v == EpistemicVerdict.GESTURE:
                verdict_grid[i, j] = 1
            else:
                verdict_grid[i, j] = 2

    fig_land = go.Figure(
        data=go.Heatmap(
            x=om_land,
            y=tau_land,
            z=verdict_grid,
            colorscale=[
                [0, "#28a745"],
                [0.33, "#28a745"],
                [0.34, "#ffc107"],
                [0.66, "#ffc107"],
                [0.67, "#dc3545"],
                [1.0, "#dc3545"],
            ],
            zmin=0,
            zmax=2,
            showscale=False,
            hovertemplate="ω=%{x:.3f}<br>τ_R=%{y:.1f}<extra></extra>",
        )
    )

    fig_land.add_vline(
        x=0.038, line_dash="dash", line_color="white", annotation_text="STABLE|WATCH", annotation_font_color="white"
    )
    fig_land.add_vline(
        x=0.30, line_dash="dash", line_color="white", annotation_text="WATCH|COLLAPSE", annotation_font_color="white"
    )

    # Map current regime to representative ω for marker placement
    _regime_omega_map = {"STABLE": 0.02, "WATCH": 0.10, "COLLAPSE": 0.35}
    _marker_omega = _regime_omega_map.get(regime_str, 0.10)

    fig_land.add_trace(
        go.Scatter(
            x=[_marker_omega],
            y=[tau_R_val],
            mode="markers",
            marker={"size": 14, "color": "cyan", "symbol": "x", "line": {"width": 2, "color": "white"}},
            name="Current State",
            showlegend=True,
        )
    )

    fig_land.update_layout(
        height=400,
        xaxis_title="ω (Drift)",
        yaxis_title="τ_R (Return Time)",
        title="Epistemic Verdict Map (Green=RETURN, Yellow=GESTURE, Red=DISSOLUTION)",
    )
    st.plotly_chart(fig_land, use_container_width=True)


def _gesture_reason_description(reason: Any) -> str:
    """Human-readable description for a GestureReason."""
    descriptions = {
        "seam_residual_exceeded": "The budget did not close — |s| > tol_seam",
        "no_finite_return": "Nothing returned within the recovery horizon — τ_R = ∞_rec",
        "identity_mismatch": "Exponential identity failed — |I_post/I_pre − exp(Δκ)| ≥ tol_exp",
        "frozen_parameter_drift": "Parameters changed between collapse and return — seam is incomparable",
        "tier0_incomplete": "Missing N_K or Ψ(t) — there is no trace to evaluate",
    }
    return descriptions.get(reason.value, "Unknown failure mode")


# ============================================================================
# Page 3: Insights & Pattern Discovery
# ============================================================================


def render_insights_page() -> None:
    """Render the Insights & Pattern Discovery page.

    Integrates insights.py to provide:
    - PatternDatabase browser with filtering
    - Severity and type distribution
    - Cross-domain correlation viewer
    - Live pattern discovery from canon data
    - Rotating insight spotlight
    """
    if st is None:
        return
    if pd is None or np is None:
        st.error("Dashboard dependencies (numpy, pandas) could not be loaded. Install with: `pip install umcp[viz]`")
        return

    st.title("💡 Insights & Pattern Discovery")
    st.caption("Lessons learned • Cross-domain patterns • Severity classification")

    # Import engine module
    try:
        from umcp.insights import (
            InsightSeverity,
            PatternDatabase,
        )
    except ImportError:
        st.error("Required module not available: umcp.insights")
        return

    # ========== Load Pattern Database ==========
    db = PatternDatabase()
    yaml_count = db.load_yaml()
    canon_count = db.load_canon()
    total = db.count()

    # ========== Overview Metrics ==========
    m1, m2, m3, m4 = st.columns(4)

    with m1:
        st.metric("Total Patterns", total)
    with m2:
        st.metric("From YAML DB", yaml_count)
    with m3:
        st.metric("From Canon", canon_count)
    with m4:
        st.metric("Domains", len(db.domains()))

    st.divider()

    if total == 0:
        st.info("""
        No patterns loaded. This can happen if:
        - `closures/materials_science/lessons_db.yaml` does not exist yet
        - `canon/matl_anchors.yaml` has no `lessons_learned` entries

        Try running `InsightEngine().discover_all()` to populate the database.
        """)
        return

    # ========== Spotlight ==========
    st.subheader("🔦 Insight Spotlight")

    if "spotlight_idx" not in st.session_state:
        st.session_state.spotlight_idx = 0

    entry = db.entries[st.session_state.spotlight_idx % total]

    severity_colors = {
        InsightSeverity.FUNDAMENTAL: "#dc3545",
        InsightSeverity.STRUCTURAL: "#6f42c1",
        InsightSeverity.EMPIRICAL: "#17a2b8",
        InsightSeverity.CURIOUS: "#28a745",
    }
    s_color = severity_colors.get(entry.severity, "#6c757d")

    st.markdown(
        f"""
    <div style="background: {s_color}15; border-left: 4px solid {s_color};
                padding: 15px; border-radius: 5px;">
        <h4 style="color: {s_color}; margin: 0 0 5px 0;">
            [{entry.severity.value}] {entry.pattern}
        </h4>
        <p style="margin: 5px 0;"><b>Lesson</b>: {entry.lesson}</p>
        <p style="margin: 5px 0;"><b>Implication</b>: {entry.implication}</p>
        <p style="color: #888; margin: 5px 0 0 0; font-size: 0.9em;">
            Domain: {entry.domain} | Type: {entry.pattern_type.value} |
            Source: {entry.source} | ID: {entry.id}
        </p>
    </div>
    """,
        unsafe_allow_html=True,
    )

    spot_col1, spot_col2, _ = st.columns([1, 1, 4])
    with spot_col1:
        if st.button("⬅️ Previous", key="spot_prev"):
            st.session_state.spotlight_idx = (st.session_state.spotlight_idx - 1) % total
            st.rerun()
    with spot_col2:
        if st.button("➡️ Next", key="spot_next"):
            st.session_state.spotlight_idx = (st.session_state.spotlight_idx + 1) % total
            st.rerun()

    st.divider()

    # ========== Distribution Charts ==========
    st.subheader("📊 Pattern Distributions")

    dist_col1, dist_col2 = st.columns(2)

    with dist_col1:
        # Severity distribution
        sev_counts: dict[str, int] = {}
        for e in db.entries:
            sev_counts[e.severity.value] = sev_counts.get(e.severity.value, 0) + 1

        sev_labels = list(sev_counts.keys())
        sev_values = list(sev_counts.values())
        sev_colors_list = [severity_colors.get(InsightSeverity(s), "#6c757d") for s in sev_labels]

        fig_sev = go.Figure(
            data=[
                go.Pie(
                    labels=sev_labels,
                    values=sev_values,
                    marker={"colors": sev_colors_list},
                    textinfo="label+value",
                )
            ]
        )
        fig_sev.update_layout(height=300, title="By Severity")
        st.plotly_chart(fig_sev, use_container_width=True)

    with dist_col2:
        # Pattern type distribution
        type_counts: dict[str, int] = {}
        for e in db.entries:
            type_counts[e.pattern_type.value] = type_counts.get(e.pattern_type.value, 0) + 1

        fig_type = go.Figure(
            data=[
                go.Bar(
                    x=list(type_counts.keys()),
                    y=list(type_counts.values()),
                    marker_color="#17a2b8",
                )
            ]
        )
        fig_type.update_layout(
            height=300,
            title="By Pattern Type",
            xaxis_title="Pattern Type",
            yaxis_title="Count",
        )
        st.plotly_chart(fig_type, use_container_width=True)

    st.divider()

    # ========== Filterable Browser ==========
    st.subheader("🔍 Pattern Browser")

    filter_col1, filter_col2, filter_col3 = st.columns(3)

    with filter_col1:
        domain_filter = st.selectbox(
            "Domain",
            ["All", *db.domains()],
            key="insight_domain",
            help="Filter patterns by domain",
        )
    with filter_col2:
        severity_filter = st.selectbox(
            "Severity",
            ["All"] + [s.value for s in InsightSeverity],
            key="insight_severity",
            help="Filter by severity level",
        )
    with filter_col3:
        source_filter = st.selectbox(
            "Source",
            ["All", "canon", "discovered", "cross-closure"],
            key="insight_source",
            help="Filter by pattern origin",
        )

    # Apply filters
    filtered = db.query(
        domain=domain_filter if domain_filter != "All" else None,
        severity=InsightSeverity(severity_filter) if severity_filter != "All" else None,
        source=source_filter if source_filter != "All" else None,
    )

    st.caption(f"Showing {len(filtered)} of {total} patterns")

    if filtered:
        rows = []
        for e in filtered:
            rows.append(
                {
                    "ID": e.id,
                    "Domain": e.domain,
                    "Severity": e.severity.value,
                    "Type": e.pattern_type.value,
                    "Pattern": e.pattern[:80] + ("..." if len(e.pattern) > 80 else ""),
                    "Source": e.source,
                }
            )

        df_patterns = pd.DataFrame(rows)
        st.dataframe(df_patterns, use_container_width=True, hide_index=True)

        # Detail view
        if st.session_state.get("show_detail", False):
            detail_idx = st.number_input("Detail index", 0, len(filtered) - 1, 0, key="detail_idx")
            detail = filtered[detail_idx]

            st.markdown(f"""
            **ID**: {detail.id}
            **Domain**: {detail.domain}
            **Pattern**: {detail.pattern}
            **Lesson**: {detail.lesson}
            **Implication**: {detail.implication}
            **Severity**: {detail.severity.value}
            **Type**: {detail.pattern_type.value}
            **Source**: {detail.source}
            **Elements**: {", ".join(detail.elements) if detail.elements else "N/A"}
            **ω Range**: [{detail.omega_range[0]:.3f}, {detail.omega_range[1]:.3f}]
            """)

        st.toggle("Show detail view", key="show_detail")
    else:
        st.info("No patterns match the current filters.")

    st.divider()

    # ========== Domain Coverage Map ==========
    st.subheader("🗺️ Domain Coverage")

    domain_rows = []
    for domain in db.domains():
        domain_entries = db.query(domain=domain)
        sev_dist = {}
        for e in domain_entries:
            sev_dist[e.severity.value] = sev_dist.get(e.severity.value, 0) + 1
        domain_rows.append(
            {
                "Domain": domain,
                "Total": len(domain_entries),
                "Fundamental": sev_dist.get("Fundamental", 0),
                "Structural": sev_dist.get("Structural", 0),
                "Empirical": sev_dist.get("Empirical", 0),
                "Curious": sev_dist.get("Curious", 0),
            }
        )

    if domain_rows:
        df_domains = pd.DataFrame(domain_rows)
        st.dataframe(df_domains, use_container_width=True, hide_index=True)

        # Stacked bar
        fig_stack = go.Figure()
        for sev, color in severity_colors.items():
            fig_stack.add_trace(
                go.Bar(
                    x=df_domains["Domain"],
                    y=df_domains[sev.value],
                    name=sev.value,
                    marker_color=color,
                )
            )
        fig_stack.update_layout(
            barmode="stack",
            height=300,
            title="Patterns by Domain and Severity",
            xaxis_title="Domain",
            yaxis_title="Count",
        )
        st.plotly_chart(fig_stack, use_container_width=True)


# ============================================================================
# Exports
# ============================================================================

__all__ = [
    "render_epistemic_page",
    "render_insights_page",
    "render_tau_r_star_page",
]
