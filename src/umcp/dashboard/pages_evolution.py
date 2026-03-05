"""
Evolution domain dashboard pages: Evolution Kernel, Brain Kernel,
Awareness Manifold, Cognitive Traversal.

Covers the ``closures/evolution/`` domain (14th domain closure):
  - 40-organism evolution kernel (8 channels)
  - 19-species brain kernel (10 channels, developmental trajectory, pathologies)
  - Awareness manifold analysis (floor constraints, emergence thresholds)
  - Cognitive traversal analysis (regime distance, species comparison)

Derivation chain: Axiom-0 → frozen_contract → kernel_optimized → evolution closures
"""
# pyright: reportUnknownMemberType=false
# pyright: reportUnknownVariableType=false
# pyright: reportUnknownArgumentType=false
# pyright: reportOptionalMemberAccess=false
# pyright: reportMissingTypeStubs=false

from __future__ import annotations

from typing import Any

from umcp.dashboard._deps import go, np, pd, st
from umcp.dashboard._utils import _ensure_closures_path
from umcp.frozen_contract import EPSILON

# ═════════════════════════════════════════════════════════════════════
# CONSTANTS
# ═════════════════════════════════════════════════════════════════════

REGIME_COLORS_EVO = {
    "Stable": "#28a745",
    "Watch": "#ffc107",
    "Collapse": "#dc3545",
}

STRATEGY_COLORS = {
    "Robust Generalist": "#2ecc71",
    "Adapted Specialist": "#3498db",
    "Resilient Ancient": "#9b59b6",
    "Vulnerable Specialist": "#e67e22",
    "Minimal Viable": "#95a5a6",
}

CLADE_COLORS = {
    "Nematoda": "#7f8c8d",
    "Arthropoda": "#e67e22",
    "Mollusca": "#9b59b6",
    "Actinopterygii": "#3498db",
    "Chondrichthyes": "#2980b9",
    "Amphibia": "#27ae60",
    "Reptilia": "#16a085",
    "Aves": "#f39c12",
    "Mammalia": "#e74c3c",
    "Primates": "#c0392b",
    "Primates (Great Ape)": "#8e44ad",
    "Primates (Old World monkey)": "#c0392b",
    "Hominidae": "#8e44ad",
    "Rodentia": "#e67e22",
    "Carnivora": "#e74c3c",
    "Cetacea": "#2980b9",
    "Proboscidea": "#795548",
    "Proteobacteria": "#1abc9c",
    "Cyanobacteria": "#2ecc71",
    "Euryarchaeota": "#d35400",
    "Amoebozoa": "#bdc3c7",
    "Fungi": "#795548",
    "Plantae": "#4caf50",
}


# ═════════════════════════════════════════════════════════════════════
# PAGE 1: EVOLUTION KERNEL — 40 organisms across tree of life
# ═════════════════════════════════════════════════════════════════════


def render_evolution_kernel_page() -> None:
    """Render the Evolution Kernel page — 40 organisms, 8 channels."""
    if st is None:
        return
    if go is None or pd is None or np is None:
        st.error(
            "Dashboard dependencies (numpy, pandas, plotly) could not be loaded. Install with: `pip install umcp[viz]`"
        )
        return

    _ensure_closures_path()

    st.title("🧬 Evolution Kernel")
    st.caption("EVO.INTSTACK.v1 — 40 organisms across the tree of life | 8-channel trace → Tier-1 invariants")

    with st.expander("📖 Domain Overview", expanded=False):
        st.markdown("""
        The **Evolution Kernel** maps 40 organisms from prokaryotes to mammals
        through 8-channel trace vectors, computing Tier-1 invariants.

        **Channels (8):**

        | # | Channel | Measures |
        |---|---------|----------|
        | 1 | genetic_diversity | Population heterozygosity |
        | 2 | morphological_fitness | Body plan complexity |
        | 3 | reproductive_success | Fecundity × survival |
        | 4 | metabolic_efficiency | Energy conversion |
        | 5 | immune_competence | Defense system breadth |
        | 6 | environmental_breadth | Niche width |
        | 7 | behavioral_complexity | Repertoire richness |
        | 8 | lineage_persistence | Geological duration |

        **Key GCD predictions:**
        - F + ω = 1: What selection preserves + removes = 1 (exhaustive)
        - IC ≤ F: Organism coherence ≤ mean trait fitness (integrity bound)
        - Geometric slaughter: ONE non-viable trait kills IC → purifying selection
        - Heterogeneity gap Δ = F − IC: evolutionary fragility metric
        - Extinct lineages: τ_R = ∞_rec (no return — the lineage is a *gestus*)
        """)

    # ── Import evolution closure ──
    evo_available = False
    try:
        from closures.evolution.evolution_kernel import (
            CHANNEL_LABELS,
            compute_all_organisms,
        )

        evo_available = True
    except Exception as e:
        st.error(f"Evolution kernel not available: {e}")
        return

    if not evo_available:
        return

    # ── Compute all organisms ──
    with st.spinner("Computing evolution kernel for 40 organisms..."):
        try:
            results = compute_all_organisms()
        except Exception as e:
            st.error(f"Computation error: {e}")
            return

    # ── Build DataFrame ──
    rows = []
    for r in results:
        row: dict[str, Any] = {
            "Organism": r.name,
            "Domain": r.domain_of_life,
            "Kingdom": r.kingdom,
            "Clade": r.clade,
            "Status": r.status,
            "F": round(r.F, 4),
            "ω": round(r.omega, 4),
            "IC": round(r.IC, 4),
            "Δ": round(r.heterogeneity_gap, 4),
            "S": round(r.S, 4),
            "C": round(r.C, 4),
            "κ": round(r.kappa, 4),
            "Regime": r.regime,
            "Strategy": r.evolutionary_strategy,
            "Weakest": r.weakest_channel,
            "Strongest": r.strongest_channel,
        }
        rows.append(row)

    df = pd.DataFrame(rows)

    # ── Summary Metrics ──
    st.markdown("### 📊 Summary")
    c1, c2, c3, c4, c5 = st.columns(5)
    with c1:
        st.metric("Organisms", len(results))
    with c2:
        st.metric("Extant", sum(1 for r in results if r.status == "extant"))
    with c3:
        st.metric("Extinct", sum(1 for r in results if r.status == "extinct"))
    with c4:
        stable_count = sum(1 for r in results if r.regime == "Stable")
        st.metric("Stable Regime", stable_count)
    with c5:
        avg_F = sum(r.F for r in results) / len(results)
        st.metric("Mean F", f"{avg_F:.3f}")

    st.divider()

    # ── Tabs ──
    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        [
            "📋 Organism Table",
            "🗺️ Phase Space",
            "📊 Strategy Analysis",
            "🧬 Channel Profiles",
            "🔍 Deep Dive",
        ]
    )

    # ── Tab 1: Organism Table ──
    with tab1:
        st.subheader("📋 Full Organism Table")

        # Filters
        fc1, fc2, fc3 = st.columns(3)
        with fc1:
            domain_filter = st.selectbox(
                "Filter by Domain",
                ["All", *sorted(df["Domain"].unique().tolist())],
                key="evo_domain_filter",
                help="Filter organisms by domain of life",
            )
        with fc2:
            status_filter = st.selectbox(
                "Filter by Status",
                ["All", "extant", "extinct"],
                key="evo_status_filter",
            )
        with fc3:
            regime_filter = st.selectbox(
                "Filter by Regime",
                ["All", *sorted(df["Regime"].unique().tolist())],
                key="evo_regime_filter",
                help="Filter by GCD regime classification",
            )

        filtered = df.copy()
        if domain_filter != "All":
            filtered = filtered[filtered["Domain"] == domain_filter]
        if status_filter != "All":
            filtered = filtered[filtered["Status"] == status_filter]
        if regime_filter != "All":
            filtered = filtered[filtered["Regime"] == regime_filter]

        st.dataframe(filtered, use_container_width=True, hide_index=True, height=500)

    # ── Tab 2: Phase Space ──
    with tab2:
        st.subheader("🗺️ F vs IC Phase Space")

        # Scatter plot: F vs IC, colored by strategy
        fig = go.Figure()
        for strategy, color in STRATEGY_COLORS.items():
            subset = [r for r in results if r.evolutionary_strategy == strategy]
            if subset:
                fig.add_trace(
                    go.Scatter(
                        x=[r.F for r in subset],
                        y=[r.IC for r in subset],
                        mode="markers+text",
                        marker={"size": 10, "color": color, "opacity": 0.8},
                        text=[r.name[:15] for r in subset],
                        textposition="top center",
                        textfont={"size": 8},
                        name=strategy,
                        hovertemplate=(
                            "<b>%{text}</b><br>"
                            "F=%{x:.3f}, IC=%{y:.3f}<br>"
                            "Δ=%{customdata[0]:.3f}, ω=%{customdata[1]:.3f}"
                            "<extra></extra>"
                        ),
                        customdata=[[r.heterogeneity_gap, r.omega] for r in subset],
                    )
                )

        # Add IC = F line (integrity bound)
        fig.add_trace(
            go.Scatter(
                x=[0, 1],
                y=[0, 1],
                mode="lines",
                line={"dash": "dash", "color": "rgba(128,128,128,0.5)"},
                name="IC = F (bound)",
                showlegend=True,
            )
        )

        fig.update_layout(
            title="Evolutionary Phase Space: F vs IC",
            xaxis_title="F (Fidelity — what selection preserves)",
            yaxis_title="IC (Integrity Composite — multiplicative coherence)",
            height=550,
            xaxis={"range": [0, 1]},
            yaxis={"range": [0, 1]},
        )
        st.plotly_chart(fig, use_container_width=True)

        # Regime distribution
        st.markdown("#### Regime Distribution")
        regime_counts = df["Regime"].value_counts()
        fig2 = go.Figure(
            go.Pie(
                labels=regime_counts.index.tolist(),
                values=regime_counts.values.tolist(),
                marker={"colors": [REGIME_COLORS_EVO.get(r, "#999") for r in regime_counts.index]},
                hole=0.4,
            )
        )
        fig2.update_layout(title="Regime Classification", height=350)
        st.plotly_chart(fig2, use_container_width=True)

    # ── Tab 3: Strategy Analysis ──
    with tab3:
        st.subheader("📊 Evolutionary Strategy Classification")

        strategy_counts = df["Strategy"].value_counts()
        fig3 = go.Figure(
            go.Bar(
                x=strategy_counts.index.tolist(),
                y=strategy_counts.values.tolist(),
                marker_color=[STRATEGY_COLORS.get(s, "#999") for s in strategy_counts.index],
            )
        )
        fig3.update_layout(
            title="Strategy Distribution",
            xaxis_title="Evolutionary Strategy",
            yaxis_title="Count",
            height=400,
        )
        st.plotly_chart(fig3, use_container_width=True)

        st.markdown("""
        **Strategy definitions (from kernel invariants):**

        | Strategy | Criterion | Ecological Meaning |
        |----------|-----------|-------------------|
        | Robust Generalist | F≥0.65, Δ<0.15 | Survives perturbation, wide niche |
        | Adapted Specialist | F≥0.55, Δ≥0.15, C<0.30 | Dominates stable niches, fragile |
        | Resilient Ancient | F<0.55, Δ<0.10, IC>0.30 | Living fossils, moderate fidelity |
        | Vulnerable Specialist | F≥0.45, Δ≥0.20 | At risk of extinction |
        | Minimal Viable | Low F, low IC | Edge of viability |
        """)

        # Strategy by domain of life
        if "Domain" in df.columns and "Strategy" in df.columns:
            st.markdown("#### Strategy × Domain Cross-Tab")
            cross = pd.crosstab(df["Domain"], df["Strategy"])
            st.dataframe(cross, use_container_width=True)

    # ── Tab 4: Channel Profiles ──
    with tab4:
        st.subheader("🧬 Channel Profiles")

        selected_orgs = st.multiselect(
            "Compare organisms",
            [r.name for r in results],
            default=[r.name for r in results[:4]],
            key="evo_compare",
            help="Pick organisms for radar comparison",
        )

        if selected_orgs:
            fig4 = go.Figure()
            categories = [*CHANNEL_LABELS, CHANNEL_LABELS[0]]

            for org_name in selected_orgs:
                r = next(r for r in results if r.name == org_name)
                values = [r.trace_vector[i] for i in range(len(CHANNEL_LABELS))]
                values.append(values[0])
                fig4.add_trace(
                    go.Scatterpolar(
                        r=values,
                        theta=categories,
                        fill="toself",
                        name=org_name[:25],
                        opacity=0.6,
                    )
                )

            fig4.update_layout(
                polar={"radialaxis": {"visible": True, "range": [0, 1]}},
                title="Channel Radar Comparison",
                height=500,
            )
            st.plotly_chart(fig4, use_container_width=True)

    # ── Tab 5: Deep Dive ──
    with tab5:
        st.subheader("🔍 Organism Deep Dive")

        selected_org = st.selectbox(
            "Select organism",
            [r.name for r in results],
            key="evo_deep",
            help="Choose organism for detailed analysis",
        )

        if selected_org:
            r = next(r for r in results if r.name == selected_org)

            ic1, ic2, ic3, ic4 = st.columns(4)
            with ic1:
                st.metric("F (Fidelity)", f"{r.F:.4f}")
            with ic2:
                st.metric("IC (Integrity)", f"{r.IC:.4f}")
            with ic3:
                st.metric("Δ (Gap)", f"{r.heterogeneity_gap:.4f}")
            with ic4:
                regime_emoji = {"Stable": "🟢", "Watch": "🟡", "Collapse": "🔴"}
                st.metric("Regime", f"{regime_emoji.get(r.regime, '⚪')} {r.regime}")

            mc1, mc2, mc3, mc4 = st.columns(4)
            with mc1:
                st.metric("ω (Drift)", f"{r.omega:.4f}")
            with mc2:
                st.metric("S (Entropy)", f"{r.S:.4f}")
            with mc3:
                st.metric("C (Curvature)", f"{r.C:.4f}")
            with mc4:
                st.metric("Strategy", r.evolutionary_strategy)

            st.info(
                f"**Weakest channel**: {r.weakest_channel} ({r.weakest_value:.3f})  \n"
                f"**Strongest channel**: {r.strongest_channel} ({r.strongest_value:.3f})"
            )

            # Identity verification
            st.markdown("**Tier-1 Identity Checks:**")
            id_col = st.columns(3)
            with id_col[0]:
                st.metric("F + ω", f"{r.F_plus_omega:.6f}", delta="✅" if abs(r.F_plus_omega - 1.0) < 1e-6 else "❌")
            with id_col[1]:
                st.metric("IC ≤ F", "✅" if r.IC_leq_F else "❌")
            with id_col[2]:
                st.metric("IC ≈ exp(κ)", "✅" if r.IC_eq_exp_kappa else "❌")


# ═════════════════════════════════════════════════════════════════════
# PAGE 2: BRAIN KERNEL — Comparative neuroscience
# ═════════════════════════════════════════════════════════════════════


def render_brain_kernel_page() -> None:
    """Render the Brain Kernel page — 19 species, 10 channels, development."""
    if st is None:
        return
    if go is None or pd is None or np is None:
        st.error(
            "Dashboard dependencies (numpy, pandas, plotly) could not be loaded. Install with: `pip install umcp[viz]`"
        )
        return

    _ensure_closures_path()

    st.title("🧠 Brain Kernel")
    st.caption(
        "Comparative Neuroscience through GCD | "
        "19 species × 10 channels | Developmental trajectory | Pathology analysis"
    )

    with st.expander("📖 Domain Overview", expanded=False):
        st.markdown("""
        The **Brain Kernel** maps brains across species to 10-channel trace vectors.
        Reveals WHY the human brain is structurally unique through Tier-1 invariants.

        **Channels (10):**

        | # | Channel | Measures |
        |---|---------|----------|
        | 1 | encephalization_quotient | Brain/body mass ratio |
        | 2 | cortical_neuron_count | Absolute cortical neurons |
        | 3 | prefrontal_ratio | PFC / total cortex |
        | 4 | synaptic_density | Synapses per cortical volume |
        | 5 | connectivity_index | Long-range white matter |
        | 6 | metabolic_investment | % BMR consumed by brain |
        | 7 | plasticity_window | Duration of neuroplasticity |
        | 8 | language_architecture | Recursive language circuitry |
        | 9 | temporal_integration | Working memory / time travel |
        | 10 | social_cognition | Theory of mind capacity |

        **Key findings:**
        - Human brain has highest F but NOT highest IC/F ratio
        - Consciousness emerges from heterogeneity PRESSURE, not raw capacity
        - Geometric slaughter: ONE missing capacity kills IC
        - Language architecture is the channel that separates humans from all other species
        """)

    brain_available = False
    try:
        from closures.evolution.brain_kernel import (
            BRAIN_CATALOG,
            BRAIN_CHANNELS,
            analyze_brain_structure,
            compute_all_brains,
            compute_developmental_trajectory,
            compute_pathology_kernels,
        )

        brain_available = True
    except Exception as e:
        st.error(f"Brain kernel not available: {e}")
        return

    if not brain_available:
        return

    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        [
            "🧠 Species Comparison",
            "📈 Developmental Trajectory",
            "🔬 Structural Analysis",
            "🩺 Pathology Analysis",
            "📡 Channel Radar",
        ]
    )

    # ── Tab 1: Species Comparison ──
    with tab1:
        st.subheader("🧠 Cross-Species Brain Analysis")

        with st.spinner("Computing brain kernel for all species..."):
            try:
                brain_results = compute_all_brains()
            except Exception as e:
                st.error(f"Error: {e}")
                return

        # Build DataFrame
        brain_rows = []
        for r in brain_results:
            brain_rows.append(
                {
                    "Species": r.species,
                    "Clade": r.clade,
                    "Brain (g)": f"{r.brain_mass_g:.1f}",
                    "F": round(r.F, 4),
                    "IC": round(r.IC, 4),
                    "IC/F": round(r.IC_F_ratio, 4),
                    "Δ": round(r.delta, 4),
                    "ω": round(r.omega, 4),
                    "Regime": r.regime,
                    "Weakest": r.weakest_channel,
                    "Strongest": r.strongest_channel,
                }
            )

        brain_df = pd.DataFrame(brain_rows)

        # Summary metrics
        human = next(r for r in brain_results if r.species == "Homo sapiens")
        mc1, mc2, mc3, mc4, mc5 = st.columns(5)
        with mc1:
            st.metric("Species", len(brain_results))
        with mc2:
            st.metric("Human F", f"{human.F:.4f}")
        with mc3:
            st.metric("Human IC", f"{human.IC:.4f}")
        with mc4:
            st.metric("Human Δ", f"{human.delta:.4f}")
        with mc5:
            st.metric("Human IC/F", f"{human.IC_F_ratio:.4f}")

        st.dataframe(brain_df, use_container_width=True, hide_index=True, height=500)

        # F vs IC scatter
        st.markdown("#### F vs IC: All Species")
        fig = go.Figure()

        # Group by clade
        clades = sorted({r.clade for r in brain_results})
        for clade in clades:
            subset = [r for r in brain_results if r.clade == clade]
            color = CLADE_COLORS.get(clade, "#999")
            fig.add_trace(
                go.Scatter(
                    x=[r.F for r in subset],
                    y=[r.IC for r in subset],
                    mode="markers+text",
                    marker={"size": 12, "color": color, "opacity": 0.8},
                    text=[r.species.split("(")[0].strip()[:20] for r in subset],
                    textposition="top center",
                    textfont={"size": 7},
                    name=clade,
                    hovertemplate=(
                        "<b>%{text}</b><br>F=%{x:.4f}<br>IC=%{y:.4f}<br>Δ=%{customdata[0]:.4f}<extra></extra>"
                    ),
                    customdata=[[r.delta] for r in subset],
                )
            )

        fig.add_trace(
            go.Scatter(
                x=[0, 1],
                y=[0, 1],
                mode="lines",
                line={"dash": "dash", "color": "rgba(128,128,128,0.4)"},
                name="IC = F",
                showlegend=True,
            )
        )

        fig.update_layout(
            title="Brain Phase Space: F vs IC (sorted by heterogeneity gap Δ)",
            xaxis_title="F (Fidelity)",
            yaxis_title="IC (Integrity Composite)",
            height=550,
            xaxis={"range": [0, 1]},
            yaxis={"range": [0, 1]},
        )
        st.plotly_chart(fig, use_container_width=True)

        # Heterogeneity gap bar chart
        st.markdown("#### Heterogeneity Gap Δ = F − IC (ranked)")
        sorted_by_delta = sorted(brain_results, key=lambda r: r.delta, reverse=True)
        fig_delta = go.Figure(
            go.Bar(
                x=[r.species.split("(")[0].strip()[:20] for r in sorted_by_delta],
                y=[r.delta for r in sorted_by_delta],
                marker_color=[
                    "#c0392b"
                    if r.species == "Homo sapiens"
                    else "#2980b9"
                    if "neanderthalensis" in r.species
                    else "#95a5a6"
                    for r in sorted_by_delta
                ],
                hovertemplate="<b>%{x}</b><br>Δ = %{y:.4f}<extra></extra>",
            )
        )
        fig_delta.update_layout(
            title="Heterogeneity Gap by Species",
            yaxis_title="Δ = F − IC",
            height=400,
            xaxis_tickangle=-45,
        )
        st.plotly_chart(fig_delta, use_container_width=True)

    # ── Tab 2: Developmental Trajectory ──
    with tab2:
        st.subheader("📈 Human Brain Developmental Trajectory")
        st.markdown(
            "The human brain kernel changes across the lifespan. Each stage maps to different Tier-1 invariant values."
        )

        try:
            dev_trajectory = compute_developmental_trajectory()
        except Exception as e:
            st.error(f"Error: {e}")
            return

        dev_df = pd.DataFrame(dev_trajectory)

        # F, IC, IC/F across development
        stages = [d["stage"] for d in dev_trajectory]

        fig_dev = go.Figure()
        fig_dev.add_trace(
            go.Scatter(
                x=stages,
                y=[d["F"] for d in dev_trajectory],
                mode="lines+markers",
                name="F (Fidelity)",
                line={"color": "#2ecc71", "width": 2},
            )
        )
        fig_dev.add_trace(
            go.Scatter(
                x=stages,
                y=[d["IC"] for d in dev_trajectory],
                mode="lines+markers",
                name="IC (Integrity)",
                line={"color": "#3498db", "width": 2},
            )
        )
        fig_dev.add_trace(
            go.Scatter(
                x=stages,
                y=[d["IC_F"] for d in dev_trajectory],
                mode="lines+markers",
                name="IC/F (Efficiency)",
                line={"color": "#e74c3c", "width": 2},
            )
        )
        fig_dev.add_trace(
            go.Scatter(
                x=stages,
                y=[d["delta"] for d in dev_trajectory],
                mode="lines+markers",
                name="Δ (Gap)",
                line={"color": "#f39c12", "width": 2, "dash": "dot"},
            )
        )

        fig_dev.update_layout(
            title="Kernel Invariants Across Human Development",
            xaxis_title="Developmental Stage",
            yaxis_title="Value",
            height=500,
            xaxis_tickangle=-30,
        )
        st.plotly_chart(fig_dev, use_container_width=True)

        # Development table
        st.dataframe(
            dev_df[["stage", "F", "IC", "IC_F", "delta", "omega", "regime", "weakest_channel"]],
            use_container_width=True,
            hide_index=True,
        )

        # Regime timeline
        st.markdown("#### Regime Across Development")
        regime_map = {"Stable": 0, "Watch": 1, "Collapse": 2}
        fig_regime = go.Figure(
            go.Scatter(
                x=stages,
                y=[regime_map.get(d["regime"], 1) for d in dev_trajectory],
                mode="lines+markers",
                marker={
                    "size": 14,
                    "color": [REGIME_COLORS_EVO.get(d["regime"], "#999") for d in dev_trajectory],
                },
                line={"color": "#aaa"},
                text=[d["regime"] for d in dev_trajectory],
                hovertemplate="<b>%{x}</b><br>Regime: %{text}<extra></extra>",
            )
        )
        fig_regime.update_layout(
            title="Regime Classification Through Development",
            yaxis={
                "tickvals": [0, 1, 2],
                "ticktext": ["Stable", "Watch", "Collapse"],
                "range": [-0.5, 2.5],
            },
            height=350,
            xaxis_tickangle=-30,
        )
        st.plotly_chart(fig_regime, use_container_width=True)

        # Insight callout
        st.info(
            "**Key insight**: The generative sweet spot is the **Child (6-8 years)** stage, "
            "where the product IC/F × S peaks. Watch regime IS the evolutionary optimum — "
            "it maximizes generative potential, not stability."
        )

    # ── Tab 3: Structural Analysis ──
    with tab3:
        st.subheader("🔬 Structural Analysis")

        try:
            analysis = analyze_brain_structure()
        except Exception as e:
            st.error(f"Error: {e}")
            return

        st.markdown("#### Human Rankings")
        rc1, rc2, rc3, rc4 = st.columns(4)
        with rc1:
            st.metric("F Rank", f"#{analysis.human_F_rank}")
        with rc2:
            st.metric("IC Rank", f"#{analysis.human_IC_rank}")
        with rc3:
            st.metric("Δ Rank", f"#{analysis.human_delta_rank}")
        with rc4:
            st.metric("IC/F Rank", f"#{analysis.human_IC_F_rank}")

        st.markdown("#### Channel Heterogeneity")
        hc1, hc2, hc3 = st.columns(3)
        with hc1:
            st.metric("Channel Range", f"{analysis.human_channel_range:.3f}")
        with hc2:
            st.metric("Channel Variance", f"{analysis.human_channel_variance:.4f}")
        with hc3:
            st.metric("Synaptic Rank", f"#{analysis.human_synaptic_rank}")

        st.markdown("#### Synaptic Density Paradox")
        st.info(analysis.pruning_insight)

        st.markdown("#### Human vs Neanderthal")
        nc1, nc2, nc3 = st.columns(3)
        with nc1:
            st.metric("Neanderthal F", f"{analysis.neanderthal_F:.4f}")
        with nc2:
            st.metric("Neanderthal IC/F", f"{analysis.neanderthal_IC_F:.4f}")
        with nc3:
            st.metric("Neanderthal Weakest", analysis.neanderthal_weakest)

        if analysis.human_advantage_channels:
            st.success(f"**Human advantage channels**: {', '.join(analysis.human_advantage_channels)}")

    # ── Tab 4: Pathology Analysis ──
    with tab4:
        st.subheader("🩺 Brain Pathology Analysis")
        st.markdown(
            "Brain pathologies as channel attacks — each condition selectively damages "
            "specific channels. The kernel reveals which are survivable vs catastrophic."
        )

        try:
            pathology_results = compute_pathology_kernels()
        except Exception as e:
            st.error(f"Error: {e}")
            return

        path_rows = []
        for p in pathology_results:
            path_rows.append(
                {
                    "Condition": p["condition"],
                    "F": round(p["F"], 4),
                    "IC": round(p["IC"], 4),
                    "IC/F": round(p["IC_F"], 4),
                    "Δ": round(p["delta"], 4),
                    "Regime": p["regime"],
                    "Weakest": p["weakest_channel"],
                }
            )

        path_df = pd.DataFrame(path_rows)
        st.dataframe(path_df, use_container_width=True, hide_index=True)

        # Bar chart: IC/F by condition
        fig_path = go.Figure(
            go.Bar(
                x=[p["condition"] for p in pathology_results],
                y=[p["IC_F"] for p in pathology_results],
                marker_color=[
                    "#2ecc71" if p["IC_F"] > 0.8 else "#f39c12" if p["IC_F"] > 0.5 else "#e74c3c"
                    for p in pathology_results
                ],
            )
        )
        fig_path.update_layout(
            title="Neural Integrity Ratio (IC/F) by Condition",
            yaxis_title="IC/F",
            height=400,
            xaxis_tickangle=-45,
        )
        st.plotly_chart(fig_path, use_container_width=True)

    # ── Tab 5: Channel Radar ──
    with tab5:
        st.subheader("📡 Species Channel Radar Comparison")

        species_names = [p.species for p in BRAIN_CATALOG]
        selected_species = st.multiselect(
            "Select species to compare",
            species_names,
            default=["Homo sapiens", "Pan troglodytes (chimpanzee)"],
            key="brain_radar_select",
            help="Pick species for radar comparison",
        )

        if selected_species:
            fig_radar = go.Figure()
            categories = [*BRAIN_CHANNELS, BRAIN_CHANNELS[0]]

            for sp_name in selected_species:
                profile = next(p for p in BRAIN_CATALOG if p.species == sp_name)
                c = profile.trace_vector()
                values = [*list(c), c[0]]
                fig_radar.add_trace(
                    go.Scatterpolar(
                        r=values,
                        theta=categories,
                        fill="toself",
                        name=sp_name[:25],
                        opacity=0.5,
                    )
                )

            fig_radar.update_layout(
                polar={"radialaxis": {"visible": True, "range": [0, 1]}},
                title="10-Channel Brain Profile Radar",
                height=550,
            )
            st.plotly_chart(fig_radar, use_container_width=True)


# ═════════════════════════════════════════════════════════════════════
# PAGE 3: AWARENESS MANIFOLD — Floor constraints and emergence
# ═════════════════════════════════════════════════════════════════════


def render_awareness_manifold_page() -> None:
    """Render the Awareness Manifold page — emergence, persistence, dissolution."""
    if st is None:
        return
    if go is None or pd is None or np is None:
        st.error(
            "Dashboard dependencies (numpy, pandas, plotly) could not be loaded. Install with: `pip install umcp[viz]`"
        )
        return

    _ensure_closures_path()

    st.title("🌀 Awareness Manifold")
    st.caption("Floor constraints, emergence thresholds, and dissolution boundaries | 12 analyses, 30/30 assertions")

    with st.expander("📖 Analysis Overview", expanded=False):
        st.markdown("""
        The **Awareness Manifold** maps the structural conditions under which
        awareness-correlated neural patterns emerge, persist, and dissolve.

        **Key findings (30/30 assertions PASS):**
        1. Awareness is a **floor constraint** — minimum channel thresholds, not a peak
        2. 9+ species cross proto-awareness thresholds; awareness is NOT uniquely human
        3. Awareness **can be lost** — pathologies show dissolution paths
        4. Plasticity is the **maintenance channel** — without it, awareness degrades
        5. You cannot **inject** awareness — no single channel boost induces it
        6. The heterogeneity gap Δ discriminates aware from non-aware better than F alone
        """)

    # ── Compute awareness analysis inline ──
    try:
        from closures.evolution.brain_kernel import (
            compute_all_brains,
        )
    except Exception as e:
        st.error(f"Brain kernel not available: {e}")
        return

    tab1, tab2, tab3 = st.tabs(
        [
            "🌱 Emergence Thresholds",
            "🔬 Floor Constraint Map",
            "📊 Awareness Discrimination",
        ]
    )

    # ── Tab 1: Emergence Thresholds ──
    with tab1:
        st.subheader("🌱 Awareness Emergence Thresholds")

        with st.spinner("Computing awareness manifold..."):
            brain_results = compute_all_brains()

        # Define awareness-correlated channels
        awareness_channels = [
            "temporal_integration",
            "social_cognition",
            "prefrontal_ratio",
            "language_architecture",
        ]

        # Compute awareness cluster minimum for each species
        awareness_data = []
        for r in brain_results:
            cluster_min = min(r.channels.get(ch, 0.0) for ch in awareness_channels)
            awareness_data.append(
                {
                    "Species": r.species,
                    "F": r.F,
                    "IC": r.IC,
                    "IC/F": r.IC_F_ratio,
                    "Δ": r.delta,
                    "Awareness Min": round(cluster_min, 4),
                    "Regime": r.regime,
                    "Proto-Aware": cluster_min > 0.15,
                }
            )

        aw_df = pd.DataFrame(awareness_data)

        # Summary
        proto_count = sum(1 for d in awareness_data if d["Proto-Aware"])
        st.metric("Proto-Aware Species (cluster_min > 0.15)", f"{proto_count}/{len(awareness_data)}")

        # Scatter: Awareness Cluster Min vs IC/F
        fig_aw = go.Figure()
        for proto in [True, False]:
            subset = [d for d in awareness_data if d["Proto-Aware"] == proto]
            fig_aw.add_trace(
                go.Scatter(
                    x=[d["Awareness Min"] for d in subset],
                    y=[d["IC/F"] for d in subset],
                    mode="markers+text",
                    marker={
                        "size": 12,
                        "color": "#2ecc71" if proto else "#95a5a6",
                        "opacity": 0.8,
                    },
                    text=[d["Species"][:15] for d in subset],
                    textposition="top center",
                    textfont={"size": 7},
                    name="Proto-Aware" if proto else "Sub-Threshold",
                )
            )

        fig_aw.add_vline(x=0.15, line_dash="dash", line_color="red", annotation_text="Threshold")
        fig_aw.update_layout(
            title="Awareness Cluster Minimum vs IC/F Ratio",
            xaxis_title="Awareness Cluster Minimum",
            yaxis_title="IC/F (Neural Efficiency)",
            height=500,
        )
        st.plotly_chart(fig_aw, use_container_width=True)

        st.dataframe(aw_df, use_container_width=True, hide_index=True)

    # ── Tab 2: Floor Constraint Map ──
    with tab2:
        st.subheader("🔬 Floor Constraint Map")
        st.markdown(
            "Awareness is a **floor constraint**: it requires minimum levels across "
            "multiple channels simultaneously. No single high channel creates awareness."
        )

        brain_results = compute_all_brains()

        # Heatmap: species × awareness channels
        species_labels = [r.species[:20] for r in brain_results]
        awareness_channels_full = [
            "temporal_integration",
            "social_cognition",
            "prefrontal_ratio",
            "language_architecture",
            "plasticity_window",
        ]

        z_data = []
        for r in brain_results:
            row_vals = [r.channels.get(ch, 0.0) for ch in awareness_channels_full]
            z_data.append(row_vals)

        fig_hm = go.Figure(
            go.Heatmap(
                z=z_data,
                x=awareness_channels_full,
                y=species_labels,
                colorscale="Viridis",
                colorbar_title="Channel Value",
            )
        )
        fig_hm.update_layout(
            title="Awareness-Correlated Channel Values by Species",
            height=600,
            xaxis_title="Channel",
            yaxis_title="Species",
        )
        st.plotly_chart(fig_hm, use_container_width=True)

        st.info(
            "**Floor constraint pattern**: Species that cross awareness thresholds have "
            "ALL awareness-correlated channels above minimum values simultaneously. "
            "High values in some channels with zeros in others does NOT produce awareness — "
            "this is geometric slaughter in action."
        )

    # ── Tab 3: Awareness Discrimination ──
    with tab3:
        st.subheader("📊 Awareness Discrimination Analysis")

        brain_results = compute_all_brains()

        # What separates aware from non-aware?
        metrics = ["F", "IC", "IC/F", "Δ"]
        metric_data = {m: {"aware": [], "non_aware": []} for m in metrics}

        for r in brain_results:
            cluster_min = min(
                r.channels.get(ch, 0.0)
                for ch in [
                    "temporal_integration",
                    "social_cognition",
                    "prefrontal_ratio",
                    "language_architecture",
                ]
            )
            is_aware = cluster_min > 0.15
            key = "aware" if is_aware else "non_aware"
            metric_data["F"][key].append(r.F)
            metric_data["IC"][key].append(r.IC)
            metric_data["IC/F"][key].append(r.IC_F_ratio)
            metric_data["Δ"][key].append(r.delta)

        # Bar chart: mean of each metric for aware vs non-aware
        fig_disc = go.Figure()
        x_labels = metrics
        aware_means = [np.mean(metric_data[m]["aware"]) if metric_data[m]["aware"] else 0 for m in metrics]
        non_aware_means = [np.mean(metric_data[m]["non_aware"]) if metric_data[m]["non_aware"] else 0 for m in metrics]

        fig_disc.add_trace(
            go.Bar(
                x=x_labels,
                y=aware_means,
                name="Proto-Aware",
                marker_color="#2ecc71",
            )
        )
        fig_disc.add_trace(
            go.Bar(
                x=x_labels,
                y=non_aware_means,
                name="Sub-Threshold",
                marker_color="#95a5a6",
            )
        )

        fig_disc.update_layout(
            title="Mean Invariants: Proto-Aware vs Sub-Threshold Species",
            barmode="group",
            height=400,
            yaxis_title="Mean Value",
        )
        st.plotly_chart(fig_disc, use_container_width=True)

        # Separation analysis
        for m in metrics:
            aware_vals = metric_data[m]["aware"]
            non_aware_vals = metric_data[m]["non_aware"]
            if aware_vals and non_aware_vals:
                separation = abs(np.mean(aware_vals) - np.mean(non_aware_vals))
                st.metric(
                    f"{m} separation",
                    f"{separation:.4f}",
                    help=f"Abs difference in mean {m} between proto-aware and sub-threshold groups",
                )


# ═════════════════════════════════════════════════════════════════════
# PAGE 4: COGNITIVE TRAVERSAL — Regime distance and convergence
# ═════════════════════════════════════════════════════════════════════


def render_cognitive_traversal_page() -> None:
    """Render the Cognitive Traversal page — regime distance, convergence rates."""
    if st is None:
        return
    if go is None or pd is None or np is None:
        st.error(
            "Dashboard dependencies (numpy, pandas, plotly) could not be loaded. Install with: `pip install umcp[viz]`"
        )
        return

    _ensure_closures_path()

    st.title("🚀 Cognitive Traversal")
    st.caption(
        "Regime distance, convergence rates, and traversal efficiency | "
        "12 analyses, 30/30 assertions | Proximitas, Non Compositio"
    )

    with st.expander("📖 Analysis Overview", expanded=False):
        st.markdown("""
        **Cognitive Traversal** formalizes the question: *"Can humans traverse cognition
        exponentially due to high physiological baseline?"*

        **Core finding — Proximitas, Non Compositio:**
        The human advantage is POSITIONAL (proximity to Stable regime), not exponential.
        All species decelerate, but humans decelerate LEAST because they start closest.

        **Key results:**
        - Human: 15 steps to Stable vs C. elegans: 470 (31:1 ratio)
        - Correlation(baseline IC/F, absolute gain) = −0.98 (diminishing returns)
        - All species' acceleration is predominantly negative (deceleration)
        - Sensitivity concentrates at floor channels (1.4x ratio)
        - Generative sweet spot: Child stage, IC/F × S peaks at 0.50
        - Watch IS the evolutionary optimum — Stable kills generativity
        """)

    try:
        from closures.evolution.brain_kernel import (
            BRAIN_CATALOG,
            BRAIN_CHANNELS,
            compute_developmental_trajectory,
        )
        from umcp.kernel_optimized import compute_kernel_outputs
    except Exception as e:
        st.error(f"Required modules not available: {e}")
        return

    N_CH = len(BRAIN_CHANNELS)

    def _kernel(c: Any) -> dict[str, float]:
        """Compute kernel from trace vector."""
        w = np.full(N_CH, 1.0 / N_CH)
        c_safe = np.clip(c, EPSILON, 1.0 - EPSILON)
        return compute_kernel_outputs(c_safe, w, EPSILON)

    def _steps_to_stable(c_init: Any, max_steps: int = 1000) -> int:
        """Count steps to reach Stable regime (ω < 0.038)."""
        c = c_init.copy()
        step_size = 0.02
        for step in range(1, max_steps + 1):
            k = _kernel(c)
            if k["omega"] < 0.038:
                return step
            c = np.clip(c + step_size, EPSILON, 1.0 - EPSILON)
        return max_steps

    tab1, tab2, tab3, tab4 = st.tabs(
        [
            "📏 Species Distance",
            "📉 Convergence Curves",
            "🎯 Sweet Spot",
            "🔬 Channel Sensitivity",
        ]
    )

    # ── Tab 1: Species Distance ──
    with tab1:
        st.subheader("📏 Steps to Stable Regime by Species")

        # Compute for representative species
        key_species = [
            "Homo sapiens",
            "Pan troglodytes (chimpanzee)",
            "Canis lupus familiaris (dog)",
            "Corvus corax (raven)",
            "Apis mellifera (honeybee)",
            "Octopus vulgaris",
            "Caenorhabditis elegans",
        ]

        with st.spinner("Computing traversal distances..."):
            traversal_data = []
            for sp_name in key_species:
                try:
                    profile = next(p for p in BRAIN_CATALOG if p.species == sp_name)
                except StopIteration:
                    continue
                c = profile.trace_vector()
                k0 = _kernel(c)
                steps = _steps_to_stable(c)
                traversal_data.append(
                    {
                        "Species": sp_name,
                        "Baseline F": round(k0["F"], 4),
                        "Baseline IC": round(k0["IC"], 4),
                        "Baseline ω": round(k0["omega"], 4),
                        "Steps to Stable": steps,
                        "Regime": "Stable" if k0["omega"] < 0.038 else "Watch" if k0["omega"] < 0.30 else "Collapse",
                    }
                )

        trav_df = pd.DataFrame(traversal_data)
        st.dataframe(trav_df, use_container_width=True, hide_index=True)

        # Bar chart: steps to stable
        fig_steps = go.Figure(
            go.Bar(
                x=[d["Species"][:20] for d in traversal_data],
                y=[d["Steps to Stable"] for d in traversal_data],
                marker_color=[
                    "#c0392b"
                    if d["Species"] == "Homo sapiens"
                    else "#3498db"
                    if "chimp" in d["Species"].lower()
                    else "#95a5a6"
                    for d in traversal_data
                ],
                text=[str(d["Steps to Stable"]) for d in traversal_data],
                textposition="auto",
            )
        )
        fig_steps.update_layout(
            title="Steps to Stable Regime (ω < 0.038)",
            yaxis_title="Steps",
            height=450,
            xaxis_tickangle=-35,
        )
        st.plotly_chart(fig_steps, use_container_width=True)

        # Efficiency ratio
        if len(traversal_data) >= 2:
            human_steps = next((d["Steps to Stable"] for d in traversal_data if d["Species"] == "Homo sapiens"), None)
            if human_steps and human_steps > 0:
                st.markdown("#### Efficiency Ratios (vs Human)")
                for d in traversal_data:
                    if d["Species"] != "Homo sapiens":
                        ratio = d["Steps to Stable"] / human_steps
                        st.metric(d["Species"][:25], f"{ratio:.1f}x")

    # ── Tab 2: Convergence Curves ──
    with tab2:
        st.subheader("📉 Convergence Curves")
        st.markdown(
            "How ω decreases as each species improves uniformly. "
            "All species decelerate — the curve flattens as they approach Stable."
        )

        species_to_plot = st.multiselect(
            "Select species",
            [p.species for p in BRAIN_CATALOG],
            default=["Homo sapiens", "Pan troglodytes (chimpanzee)", "Caenorhabditis elegans"],
            key="trav_curves_select",
            help="Pick species for convergence curves",
        )

        if species_to_plot:
            fig_conv = go.Figure()

            for sp_name in species_to_plot:
                try:
                    profile = next(p for p in BRAIN_CATALOG if p.species == sp_name)
                except StopIteration:
                    continue

                c = profile.trace_vector()
                omegas = []
                max_steps = 50
                step_size = 0.02

                for _step in range(max_steps):
                    k = _kernel(c)
                    omegas.append(k["omega"])
                    c = np.clip(c + step_size, EPSILON, 1.0 - EPSILON)

                fig_conv.add_trace(
                    go.Scatter(
                        x=list(range(max_steps)),
                        y=omegas,
                        mode="lines",
                        name=sp_name[:25],
                        line={"width": 2},
                    )
                )

            # Add Stable threshold line
            fig_conv.add_hline(
                y=0.038,
                line_dash="dash",
                line_color="green",
                annotation_text="Stable threshold (ω=0.038)",
            )

            fig_conv.update_layout(
                title="ω Convergence Curves (uniform +0.02 steps)",
                xaxis_title="Step",
                yaxis_title="ω (Drift)",
                height=500,
            )
            st.plotly_chart(fig_conv, use_container_width=True)

    # ── Tab 3: Generative Sweet Spot ──
    with tab3:
        st.subheader("🎯 Generative Sweet Spot")
        st.markdown(
            "The **generative sweet spot** is where IC/F × S peaks — the regime "
            "that maximizes both integrity AND informational richness."
        )

        try:
            dev_trajectory = compute_developmental_trajectory()
            from closures.evolution.brain_kernel import DEVELOPMENT_STAGES as _STAGES
        except Exception as e:
            st.error(f"Error: {e}")
            return

        # Compute IC/F × S for each developmental stage
        sweet_data = []
        for d in dev_trajectory:
            ic_f = d.get("IC_F", 0)
            stage_name = d["stage"]
            matching = [s for s in _STAGES if s[0] == stage_name]
            if matching:
                stage_channels = matching[0][1]
                c = np.array([stage_channels[ch] for ch in BRAIN_CHANNELS], dtype=np.float64)
                c = np.clip(c, EPSILON, 1.0 - EPSILON)
                k = _kernel(c)
                product = ic_f * k["S"]
                sweet_data.append(
                    {
                        "Stage": stage_name,
                        "IC/F": round(ic_f, 4),
                        "S": round(k["S"], 4),
                        "IC/F × S": round(product, 4),
                        "F": round(d["F"], 4),
                        "Regime": d["regime"],
                    }
                )

        if sweet_data:
            sweet_df = pd.DataFrame(sweet_data)
            st.dataframe(sweet_df, use_container_width=True, hide_index=True)

            # Line plot
            fig_sweet = go.Figure()
            fig_sweet.add_trace(
                go.Scatter(
                    x=[d["Stage"] for d in sweet_data],
                    y=[d["IC/F × S"] for d in sweet_data],
                    mode="lines+markers",
                    name="IC/F × S (Generative Product)",
                    line={"color": "#e74c3c", "width": 3},
                    marker={"size": 10},
                )
            )
            fig_sweet.add_trace(
                go.Scatter(
                    x=[d["Stage"] for d in sweet_data],
                    y=[d["IC/F"] for d in sweet_data],
                    mode="lines+markers",
                    name="IC/F (Efficiency)",
                    line={"color": "#3498db", "width": 2, "dash": "dot"},
                )
            )
            fig_sweet.add_trace(
                go.Scatter(
                    x=[d["Stage"] for d in sweet_data],
                    y=[d["S"] for d in sweet_data],
                    mode="lines+markers",
                    name="S (Bernoulli Field Entropy)",
                    line={"color": "#2ecc71", "width": 2, "dash": "dot"},
                )
            )

            fig_sweet.update_layout(
                title="Generative Product Across Development",
                xaxis_title="Stage",
                yaxis_title="Value",
                height=450,
                xaxis_tickangle=-30,
            )
            st.plotly_chart(fig_sweet, use_container_width=True)

            # Find peak
            peak = max(sweet_data, key=lambda d: d["IC/F × S"])
            st.success(f"**Peak generative product**: {peak['Stage']} — IC/F × S = {peak['IC/F × S']:.4f}")

            st.info(
                "**The Transcendence Paradox**: Reaching Stable regime kills generativity — "
                "S collapses to near-zero as all channels saturate. "
                "Watch IS the evolutionary optimum because it maintains the tension "
                "between integrity and entropy that drives generation."
            )

    # ── Tab 4: Channel Sensitivity ──
    with tab4:
        st.subheader("🔬 Channel Sensitivity Analysis")
        st.markdown(
            "Kappa derivative dκ/dcᵢ = wᵢ/cᵢ — sensitivity is **inversely proportional** "
            "to channel value. The WEAKEST channels have the MOST leverage."
        )

        selected_sp = st.selectbox(
            "Select species for sensitivity analysis",
            [p.species for p in BRAIN_CATALOG],
            key="trav_sens_species",
            help="Species for dκ/dcᵢ sensitivity analysis",
        )

        if selected_sp:
            profile = next(p for p in BRAIN_CATALOG if p.species == selected_sp)
            c = profile.trace_vector()
            w = np.full(N_CH, 1.0 / N_CH)

            # Compute dκ/dcᵢ = wᵢ/cᵢ
            sensitivities = {}
            for i, ch in enumerate(BRAIN_CHANNELS):
                ci = max(c[i], EPSILON)
                sensitivities[ch] = w[i] / ci

            sens_sorted = sorted(sensitivities.items(), key=lambda x: x[1], reverse=True)

            fig_sens = go.Figure(
                go.Bar(
                    x=[s[0] for s in sens_sorted],
                    y=[s[1] for s in sens_sorted],
                    marker_color=[
                        "#e74c3c"
                        if s[1] == sens_sorted[0][1]
                        else "#f39c12"
                        if s[1] > sens_sorted[-1][1] * 1.2
                        else "#3498db"
                        for s in sens_sorted
                    ],
                )
            )
            fig_sens.update_layout(
                title=f"κ Sensitivity (dκ/dcᵢ = wᵢ/cᵢ) — {selected_sp[:30]}",
                yaxis_title="dκ/dcᵢ",
                height=450,
                xaxis_tickangle=-45,
            )
            st.plotly_chart(fig_sens, use_container_width=True)

            # Ratio analysis
            max_sens = max(sensitivities.values())
            min_sens = min(sensitivities.values())
            ratio = max_sens / min_sens if min_sens > 0 else float("inf")
            st.metric("Sensitivity ratio (weakest/strongest)", f"{ratio:.2f}x")

            st.info(
                "**Investment implication**: Improving the weakest channel yields "
                f"{ratio:.1f}× more κ-gain than improving the strongest. "
                "This is why floor constraints matter more than ceiling capacity."
            )


# ═════════════════════════════════════════════════════════════════════
# PUBLIC API
# ═════════════════════════════════════════════════════════════════════

__all__ = [
    "render_awareness_manifold_page",
    "render_brain_kernel_page",
    "render_cognitive_traversal_page",
    "render_evolution_kernel_page",
]
