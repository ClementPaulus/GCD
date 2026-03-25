"""
Science domain dashboard pages: Cosmology, Astronomy, Nuclear, Quantum, Finance, RCFT,
Atomic Physics, Standard Model, Materials Science, Security.
"""
# pyright: reportUnknownMemberType=false
# pyright: reportUnknownVariableType=false
# pyright: reportUnknownArgumentType=false
# pyright: reportOptionalMemberAccess=false
# pyright: reportMissingTypeStubs=false

from __future__ import annotations

from umcp.dashboard._deps import go, np, pd, st
from umcp.dashboard._utils import (
    _ensure_closures_path,
)
from umcp.frozen_contract import EPSILON


def render_cosmology_page() -> None:
    """
    Render the WEYL Cosmology page for modified gravity analysis.

    Implements visualization of the WEYL.INTSTACK.v1 contract:
    - Σ(z) evolution and regime classification
    - ĥJ measurements from DES Y3 data
    - Weyl transfer function visualization
    - UMCP integration patterns

    Reference: Nature Communications 15:9295 (2024)
    """
    if st is None:
        return
    if np is None or pd is None or go is None:
        st.error(
            "Dashboard dependencies (numpy, pandas, plotly) could not be loaded. Install with: `pip install umcp[viz]`"
        )
        return

    st.title("🌌 WEYL Cosmology")
    st.caption("Modified gravity analysis with Σ(z) parametrization | Nature Comms 15:9295 (2024)")

    # Ensure closures path is available
    _ensure_closures_path()

    weyl_available = False
    Omega_Lambda_of_z = None  # Initialize for scope
    try:
        from closures.weyl import (
            DES_Y3_DATA,
            PLANCK_2018,
            D1_of_z,
            GzModel,
            H_of_z,
            Omega_Lambda_of_z,
            Sigma_to_UMCP_invariants,
            chi_of_z,
            compute_Sigma,
            sigma8_of_z,
        )

        weyl_available = True
    except ImportError as e:
        st.error(f"❌ WEYL closures import failed: {e}")

    if not weyl_available:
        st.error("❌ WEYL closures not available. Please ensure closures/weyl/ is installed.")
        st.code("# WEYL closures should be in closures/weyl/", language="python")
        return

    # Initialize session state
    if "weyl_params" not in st.session_state:
        st.session_state.weyl_params = {
            "Sigma_0": 0.24,
            "g_model": "constant",
            "z_max": 2.0,
            "n_points": 100,
        }

    # ========== Cosmological Background Section ==========
    st.header("🌍 Cosmological Background")

    with st.expander("📖 About ΛCDM Background", expanded=False):
        st.markdown("""
        **Planck 2018 Fiducial Cosmology:**
        - Matter density: Ω_m,0 = 0.315
        - Dark energy: Ω_Λ,0 = 0.685
        - Hubble constant: H₀ = 67.4 km/s/Mpc
        - σ8 amplitude: σ8,0 = 0.811

        **Key Functions:**
        - H(z) = H₀ √[Ω_m(1+z)³ + Ω_Λ] - Hubble parameter
        - χ(z) = ∫ c/H(z') dz' - Comoving distance
        - D₁(z) - Linear growth function (normalized to 1 at z=0)
        - σ8(z) = σ8,0 × D₁(z) - Amplitude evolution

        **UMCP Integration:**
        - Background cosmology = embedding specification (Tier-0)
        - Frozen parameters (Ω_m, σ8, H₀) define the coordinate system
        """)

    # Background visualization
    z_arr = np.linspace(0, 3, 100)
    H_arr = np.array([H_of_z(z) for z in z_arr])
    chi_arr = np.array([chi_of_z(z) for z in z_arr])
    D1_arr = np.array([D1_of_z(z) for z in z_arr])
    sigma8_arr = np.array([sigma8_of_z(z) for z in z_arr])

    bg_tabs = st.tabs(["📈 H(z)", "📏 χ(z)", "📊 D₁(z) & σ8(z)"])

    with bg_tabs[0]:
        fig_H = go.Figure()
        fig_H.add_trace(go.Scatter(x=z_arr, y=H_arr, mode="lines", name="H(z)", line={"color": "#1f77b4", "width": 2}))
        fig_H.update_layout(
            title="Hubble Parameter Evolution",
            xaxis_title="Redshift z",
            yaxis_title="H(z) [km/s/Mpc]",
            showlegend=True,
        )
        st.plotly_chart(fig_H, use_container_width=True)

    with bg_tabs[1]:
        fig_chi = go.Figure()
        fig_chi.add_trace(
            go.Scatter(x=z_arr, y=chi_arr, mode="lines", name="χ(z)", line={"color": "#2ca02c", "width": 2})
        )
        fig_chi.update_layout(
            title="Comoving Distance",
            xaxis_title="Redshift z",
            yaxis_title="χ(z) [Mpc/h]",
            showlegend=True,
        )
        st.plotly_chart(fig_chi, use_container_width=True)

    with bg_tabs[2]:
        fig_growth = go.Figure()
        fig_growth.add_trace(
            go.Scatter(x=z_arr, y=D1_arr, mode="lines", name="D₁(z)", line={"color": "#ff7f0e", "width": 2})
        )
        fig_growth.add_trace(
            go.Scatter(x=z_arr, y=sigma8_arr, mode="lines", name="σ8(z)", line={"color": "#d62728", "width": 2})
        )
        fig_growth.add_hline(y=PLANCK_2018.sigma8_0, line_dash="dash", line_color="gray", annotation_text="σ8,0")
        fig_growth.update_layout(
            title="Growth Function and σ8 Evolution",
            xaxis_title="Redshift z",
            yaxis_title="Value",
            showlegend=True,
        )
        st.plotly_chart(fig_growth, use_container_width=True)

    st.divider()

    # ========== Σ(z) Modified Gravity Section ==========
    st.header("🔬 Modified Gravity: Σ(z)")

    with st.expander("📖 About Σ Parametrization", expanded=False):
        st.markdown("""
        **Σ(z) Definition (Eq. 11):**

        The Σ parameter encodes deviations from General Relativity:

        $$ k^2 (\\Phi + \\Psi)/2 = -4\\pi G a^2 \\Sigma(z,k) \\bar{\\rho}(z) \\Delta_m(z,k) $$

        - **Σ = 1**: General Relativity
        - **Σ ≠ 1**: Modified gravity or gravitational slip

        **Parametrization (Eq. 13):**
        $$ \\Sigma(z) = 1 + \\Sigma_0 \\cdot g(z) $$

        Where g(z) models:
        - **constant**: g(z) = 1 for z ∈ [0,1]
        - **exponential**: g(z) = exp(1+z) for z ∈ [0,1]
        - **standard**: g(z) = Ω_Λ(z)

        **UMCP Regime Mapping:**
        | Σ₀ Range | Regime | UMCP Analog |
        |----------|--------|-------------|
        | |Σ₀| < 0.1 | GR_consistent | STABLE |
        | 0.1 ≤ |Σ₀| < 0.3 | Tension | WATCH |
        | |Σ₀| ≥ 0.3 | Modified_gravity | COLLAPSE |
        """)

    # Interactive Σ₀ controls
    control_cols = st.columns([1, 1, 1, 1])

    with control_cols[0]:
        sigma_0 = st.slider("Σ₀ (deviation amplitude)", -0.5, 0.5, 0.24, 0.01, help="DES Y3 finds Σ₀ ≈ 0.24 ± 0.14")
    with control_cols[1]:
        g_model_name = st.selectbox(
            "g(z) Model", ["constant", "exponential", "standard"], index=0, help="Redshift evolution model for Σ(z)"
        )
        g_model = GzModel(g_model_name)
    with control_cols[2]:
        z_max_sigma = st.slider("z_max", 0.5, 3.0, 2.0, 0.1, help="Maximum redshift for Σ(z) curve")
    with control_cols[3]:
        n_points = st.slider("Points", 20, 200, 100, 10, help="Number of redshift sample points")

    # Compute Σ(z)
    z_sigma = np.linspace(0, z_max_sigma, n_points)
    # Pass Omega_Lambda_of_z for standard model (required by closure)
    Sigma_results = [compute_Sigma(z, sigma_0, g_model, Omega_Lambda_z=Omega_Lambda_of_z) for z in z_sigma]
    Sigma_values = [r.Sigma for r in Sigma_results]
    regimes = [r.regime for r in Sigma_results]

    # Create Σ(z) plot with regime coloring
    fig_sigma = go.Figure()

    # Add Σ(z) curve
    fig_sigma.add_trace(
        go.Scatter(
            x=z_sigma,
            y=Sigma_values,
            mode="lines+markers",
            name="Σ(z)",
            line={"color": "#9467bd", "width": 2},
            marker={"size": 4},
        )
    )

    # Add GR line
    fig_sigma.add_hline(y=1.0, line_dash="dash", line_color="green", annotation_text="GR (Σ=1)")

    # Add regime bands
    fig_sigma.add_hrect(y0=0.9, y1=1.1, fillcolor="green", opacity=0.1, line_width=0)
    fig_sigma.add_hrect(y0=0.7, y1=0.9, fillcolor="yellow", opacity=0.1, line_width=0)
    fig_sigma.add_hrect(y0=1.1, y1=1.3, fillcolor="yellow", opacity=0.1, line_width=0)
    fig_sigma.add_hrect(y0=0.0, y1=0.7, fillcolor="red", opacity=0.1, line_width=0)
    fig_sigma.add_hrect(y0=1.3, y1=2.0, fillcolor="red", opacity=0.1, line_width=0)

    fig_sigma.update_layout(
        title=f"Σ(z) Evolution | Σ₀ = {sigma_0:.3f} | Model: {g_model_name}",
        xaxis_title="Redshift z",
        yaxis_title="Σ(z)",
        yaxis={"range": [0.5, 1.6]},
        showlegend=True,
    )
    st.plotly_chart(fig_sigma, use_container_width=True)

    # Regime summary
    regime_counts = {}
    for r in regimes:
        regime_counts[r] = regime_counts.get(r, 0) + 1

    regime_cols = st.columns(3)
    for i, (regime, count) in enumerate(regime_counts.items()):
        with regime_cols[i % 3]:
            st.markdown(f"**{regime}**: {count} points ({100 * count / len(regimes):.1f}%)")

    st.divider()

    # ========== DES Y3 Data Section ==========
    st.header("📊 DES Y3 Reference Data")

    with st.expander("📖 About DES Y3 Analysis", expanded=False):
        st.markdown("""
        **Dark Energy Survey Year 3 Results:**

        The Nature Communications paper analyzes:
        - 4 lens redshift bins: z ∈ [0.295, 0.467, 0.626, 0.771]
        - Galaxy-galaxy lensing + galaxy clustering
        - Cross-correlation with CMB lensing from Planck

        **Key Measurements (CMB prior):**
        - ĥJ(z₁) = 0.326 ± 0.062
        - ĥJ(z₂) = 0.332 ± 0.052
        - ĥJ(z₃) = 0.387 ± 0.059
        - ĥJ(z₄) = 0.354 ± 0.085

        **Fitted Σ₀:**
        - Standard model: Σ₀ = 0.17 ± 0.12
        - Constant model: Σ₀ = 0.24 ± 0.14
        - Exponential model: Σ₀ = 0.10 ± 0.05
        """)

    # Display DES Y3 data table
    des_df = pd.DataFrame(
        {
            "Bin": [1, 2, 3, 4],
            "z_eff": DES_Y3_DATA["z_bins"],
            "ĥJ (mean)": DES_Y3_DATA["hJ_cmb"]["mean"],
            "ĥJ (σ)": DES_Y3_DATA["hJ_cmb"]["sigma"],
        }
    )
    st.dataframe(des_df, hide_index=True, use_container_width=True)

    # Plot ĥJ measurements
    fig_hJ = go.Figure()
    fig_hJ.add_trace(
        go.Scatter(
            x=DES_Y3_DATA["z_bins"],
            y=DES_Y3_DATA["hJ_cmb"]["mean"],
            error_y={"type": "data", "array": DES_Y3_DATA["hJ_cmb"]["sigma"]},
            mode="markers",
            name="ĥJ (CMB prior)",
            marker={"size": 12, "color": "#1f77b4"},
        )
    )
    fig_hJ.update_layout(
        title="DES Y3 ĥJ Measurements",
        xaxis_title="Effective Redshift z",
        yaxis_title="ĥJ",
        showlegend=True,
    )
    st.plotly_chart(fig_hJ, use_container_width=True)

    st.divider()

    # ========== UMCP Integration Section ==========
    st.header("🔗 UMCP Integration")

    with st.expander("📖 About WEYL-UMCP Mapping", expanded=True):
        st.markdown("""
        **Core Principle Alignment:**
        > "Within-run: frozen causes only. Between-run: continuity only by return-weld."

        **WEYL Implementation:**
        - **Within-run**: Frozen cosmological parameters (Ω_m, σ8, z*) determine the Weyl trace
        - **Between-run**: Canonization requires return-weld (Σ → 1 at high z)

        **Invariant Mapping:**
        | WEYL Quantity | UMCP Analog | Interpretation |
        |---------------|-------------|----------------|
        | ĥJ | F (Fidelity) | Fraction of ideal response |
        | 1 - ĥJ | ω (Drift) | Distance from ideal |
        | Σ₀ | Deviation | Amplitude of departure from GR |
        | χ² improvement | Seam closure | Better fit = tighter weld |
        """)

    # Interactive UMCP mapping
    st.subheader("🧮 Compute UMCP Invariants")

    map_cols = st.columns(3)
    with map_cols[0]:
        input_sigma0 = st.number_input("Σ₀", value=0.24, step=0.01, format="%.3f")
    with map_cols[1]:
        chi2_sigma = st.number_input("χ² (Σ model)", value=1.1, step=0.1, format="%.2f")
    with map_cols[2]:
        chi2_lcdm = st.number_input("χ² (ΛCDM)", value=2.1, step=0.1, format="%.2f")

    if st.button("📊 Compute UMCP Mapping"):
        mapping = Sigma_to_UMCP_invariants(input_sigma0, chi2_sigma, chi2_lcdm)

        result_cols = st.columns(4)
        with result_cols[0]:
            st.metric("ω (Drift)", f"{mapping['omega_analog']:.3f}")
        with result_cols[1]:
            st.metric("F (Fidelity)", f"{mapping['F_analog']:.3f}")
        with result_cols[2]:
            st.metric("χ² Improvement", f"{mapping['chi2_improvement']:.1%}")
        with result_cols[3]:
            st.metric("Regime", mapping["regime"])

        st.success("✅ WEYL measurements mapped to UMCP invariants successfully!")


def render_astronomy_page() -> None:
    """Render interactive Astronomy domain page with all 6 closures."""
    if st is None:
        return
    if go is None or pd is None or np is None:
        st.error(
            "Dashboard dependencies (numpy, pandas, plotly) could not be loaded. Install with: `pip install umcp[viz]`"
        )
        return

    _ensure_closures_path()

    st.title("🔭 Astronomy Domain")
    st.caption(
        "ASTRO.INTSTACK.v1 — Stellar luminosity, distance ladder, spectral analysis, evolution, orbits, dynamics"
    )

    with st.expander("📖 Domain Overview", expanded=False):
        st.markdown("""
        The **Astronomy** domain embeds astrophysical observables into UMCP's [0, 1] contract space.
        Each closure maps physical measurements to Tier-1 invariants (ω, F, κ, IC) and classifies
        the measurement regime.

        | Closure | Physics | Key Observable |
        |---------|---------|---------------|
        | Stellar Luminosity | Stefan-Boltzmann, mass-luminosity | L★ / L☉ |
        | Distance Ladder | Parallax, modulus, Hubble flow | d (pc) consistency |
        | Spectral Analysis | Wien's law, B−V color index | λ_peak, T_eff |
        | Stellar Evolution | Main-sequence lifetime, HR track | t_MS, evolutionary phase |
        | Orbital Mechanics | Kepler III, vis-viva | P, v_orb |
        | Gravitational Dynamics | Virial theorem, rotation curves | M_virial, DM fraction |
        """)

    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(
        [
            "⭐ Stellar Luminosity",
            "📏 Distance Ladder",
            "🌈 Spectral Analysis",
            "🔄 Stellar Evolution",
            "🪐 Orbital Mechanics",
            "🌀 Gravitational Dynamics",
        ]
    )

    # ── Tab 1: Stellar Luminosity ──
    with tab1:
        st.subheader("⭐ Stellar Luminosity")
        st.markdown("""
        **Stefan-Boltzmann**: $L = 4\\pi R^2 \\sigma T_{\\text{eff}}^4$ ·
        **Mass-Luminosity**: $L \\propto M^{3.5}$ ·
        **Wien peak**: $\\lambda_{\\text{peak}} = b / T_{\\text{eff}}$
        """)

        preset_col, _ = st.columns([1, 2])
        with preset_col:
            preset = st.selectbox(
                "Presets",
                ["Custom", "☀️ Sun", "⭐ Sirius A", "🔴 Proxima Centauri", "💙 Rigel"],
                key="astro_lum_preset",
                help="Choose a known star or enter custom values",
            )
        presets_lum = {
            "☀️ Sun": (1.0, 5778.0, 1.0),
            "⭐ Sirius A": (2.06, 9940.0, 1.71),
            "🔴 Proxima Centauri": (0.122, 3042.0, 0.154),
            "💙 Rigel": (21.0, 12100.0, 78.9),
        }
        _m, _t, _r = presets_lum.get(preset, (1.0, 5778.0, 1.0))
        c1, c2, c3 = st.columns(3)
        with c1:
            m_star = st.number_input(
                "M★ (M☉)", 0.08, 150.0, _m, 0.1, key="astro_mstar", help="Stellar mass in solar masses"
            )
        with c2:
            t_eff = st.number_input(
                "T_eff (K)",
                2000.0,
                50000.0,
                _t,
                100.0,
                key="astro_teff",
                help="Effective surface temperature in Kelvin",
            )
        with c3:
            r_star = st.number_input(
                "R★ (R☉)", 0.01, 1500.0, _r, 0.1, key="astro_rstar", help="Stellar radius in solar radii"
            )

        if st.button("Compute Luminosity", key="astro_lum", type="primary"):
            try:
                from closures.astronomy.stellar_luminosity import compute_stellar_luminosity

                result = compute_stellar_luminosity(m_star, t_eff, r_star)
                regime = result["regime"]
                regime_color = {"Consistent": "🟢", "Mild": "🟡"}.get(regime, "🔴")

                rc1, rc2, rc3, rc4 = st.columns(4)
                with rc1:
                    st.metric("L_predicted (L☉)", f"{result['L_predicted']:.4f}")
                with rc2:
                    st.metric("L_SB (L☉)", f"{result['L_SB']:.4f}")
                with rc3:
                    st.metric("δ_L", f"{result['delta_L']:.6f}")
                with rc4:
                    st.metric("Regime", f"{regime_color} {regime}")

                # Wien peak
                st.info(f"**Wien Peak**: λ_peak = {result['lambda_peak']:.1f} nm")

                # Visualization: luminosity comparison bar
                fig = go.Figure()
                fig.add_trace(
                    go.Bar(
                        x=["L_predicted (M-L relation)", "L_SB (Stefan-Boltzmann)"],
                        y=[result["L_predicted"], result["L_SB"]],
                        marker_color=["#007bff", "#28a745"],
                        text=[f"{result['L_predicted']:.4f}", f"{result['L_SB']:.4f}"],
                        textposition="outside",
                    )
                )
                fig.update_layout(
                    title="Luminosity Comparison",
                    yaxis_title="L / L☉",
                    height=300,
                    margin={"t": 40, "b": 20, "l": 40, "r": 20},
                )
                st.plotly_chart(fig, use_container_width=True)
            except Exception as e:
                st.error(f"Computation error: {e}")

    # ── Tab 2: Distance Ladder ──
    with tab2:
        st.subheader("📏 Distance Ladder Cross-Validation")
        st.markdown("""
        Three independent distance measures are compared for consistency:
        - **Distance modulus**: $d = 10^{(m - M + 5)/5}$ pc
        - **Trigonometric parallax**: $d = 1/\\pi$ pc
        - **Hubble flow**: $d = cz / H_0$
        """)

        preset_col2, _ = st.columns([1, 2])
        with preset_col2:
            dp = st.selectbox(
                "Presets", ["Custom", "⭐ Vega", "🌟 Cepheid (LMC)", "🌌 Distant Galaxy"], key="astro_dist_preset"
            )
        presets_dist = {
            "⭐ Vega": (0.03, 0.58, 0.1289, 0.0),
            "🌟 Cepheid (LMC)": (13.5, -5.0, 0.00002, 0.003),
            "🌌 Distant Galaxy": (22.0, -21.0, 0.00001, 0.1),
        }
        _ma, _mab, _pi, _zc = presets_dist.get(dp, (10.0, 4.83, 0.01, 0.01))
        c1, c2 = st.columns(2)
        with c1:
            m_app = st.number_input("m (apparent mag)", -30.0, 30.0, _ma, 0.1, key="astro_mapp")
            m_abs = st.number_input("M (absolute mag)", -30.0, 30.0, _mab, 0.1, key="astro_mabs")
        with c2:
            pi_arcsec = st.number_input("π (arcsec)", 1e-6, 1.0, _pi, 0.001, key="astro_pi", format="%.6f")
            z_cosmo = st.number_input("z (redshift)", 0.0, 10.0, _zc, 0.001, key="astro_z", format="%.4f")

        if st.button("Compute Distances", key="astro_dist", type="primary"):
            try:
                from closures.astronomy.distance_ladder import compute_distance_ladder

                result = compute_distance_ladder(m_app, m_abs, pi_arcsec, z_cosmo)
                regime = result["regime"]
                regime_color = {"High": "🟢", "Moderate": "🟡"}.get(regime, "🔴")

                rc1, rc2, rc3 = st.columns(3)
                with rc1:
                    st.metric("d_modulus (pc)", f"{result['d_modulus']:.2f}")
                with rc2:
                    st.metric("d_parallax (pc)", f"{result['d_parallax']:.2f}")
                with rc3:
                    st.metric("d_Hubble (pc)", f"{result['d_hubble']:.2f}")

                mc1, mc2 = st.columns(2)
                with mc1:
                    st.metric("Consistency", f"{result['distance_consistency']:.4f}")
                with mc2:
                    st.metric("Regime", f"{regime_color} {regime}")

                # Bar chart of distances
                fig = go.Figure()
                methods = ["Modulus", "Parallax", "Hubble"]
                vals = [result["d_modulus"], result["d_parallax"], result["d_hubble"]]
                fig.add_trace(
                    go.Bar(
                        x=methods,
                        y=vals,
                        marker_color=["#007bff", "#28a745", "#fd7e14"],
                        text=[f"{v:.1f}" for v in vals],
                        textposition="outside",
                    )
                )
                fig.update_layout(
                    title="Distance Ladder Comparison",
                    yaxis_title="Distance (pc)",
                    yaxis_type="log",
                    height=300,
                    margin={"t": 40, "b": 20},
                )
                st.plotly_chart(fig, use_container_width=True)
            except Exception as e:
                st.error(f"Computation error: {e}")

    # ── Tab 3: Spectral Analysis ──
    with tab3:
        st.subheader("🌈 Spectral Analysis")
        st.markdown("""
        **Wien's displacement**: $\\lambda_{\\text{peak}} = 2.898 \\times 10^6 / T_{\\text{eff}}$ nm ·
        **Ballesteros B−V→T**: $T = 4600 (1/(0.92 (B-V) + 1.7) + 1/(0.92 (B-V) + 0.62))$
        """)
        c1, c2, c3 = st.columns(3)
        with c1:
            t_eff_s = st.number_input("T_eff (K)", 2000.0, 50000.0, 5778.0, 100.0, key="astro_teff_s")
        with c2:
            b_v = st.number_input("B−V (mag)", -0.5, 2.5, 0.65, 0.01, key="astro_bv")
        with c3:
            spec_class = st.selectbox("Spectral Class", ["O", "B", "A", "F", "G", "K", "M"], index=4, key="astro_spec")

        if st.button("Analyze Spectrum", key="astro_spec_btn", type="primary"):
            try:
                from closures.astronomy.spectral_analysis import compute_spectral_analysis

                result = compute_spectral_analysis(t_eff_s, b_v, spec_class)
                regime = result["regime"]
                regime_color = {"Excellent": "🟢", "Good": "🟡", "Marginal": "🟡"}.get(regime, "🔴")

                rc1, rc2, rc3, rc4 = st.columns(4)
                with rc1:
                    st.metric("λ_peak (nm)", f"{result['lambda_peak']:.1f}")
                with rc2:
                    st.metric("T from B−V (K)", f"{result['T_from_BV']:.0f}")
                with rc3:
                    st.metric("χ² spectral", f"{result['chi2_spectral']:.4f}")
                with rc4:
                    st.metric("Regime", f"{regime_color} {regime}")

                # Spectral class bar
                spectral_temps = {"O": 40000, "B": 20000, "A": 8500, "F": 6500, "G": 5500, "K": 4000, "M": 3000}
                fig = go.Figure()
                classes = list(spectral_temps.keys())
                temps = list(spectral_temps.values())
                colors = ["#9bb0ff", "#aabfff", "#cad7ff", "#f8f7ff", "#fff4e8", "#ffd2a1", "#ffcc6f"]
                fig.add_trace(go.Bar(x=classes, y=temps, marker_color=colors, name="Typical T_eff"))
                fig.add_hline(
                    y=t_eff_s, line_dash="dash", line_color="red", annotation_text=f"Input T_eff = {t_eff_s:.0f} K"
                )
                fig.update_layout(
                    title="Spectral Class Temperature Scale",
                    yaxis_title="T_eff (K)",
                    height=300,
                    margin={"t": 40, "b": 20},
                )
                st.plotly_chart(fig, use_container_width=True)
            except Exception as e:
                st.error(f"Computation error: {e}")

    # ── Tab 4: Stellar Evolution ──
    with tab4:
        st.subheader("🔄 Stellar Evolution")
        st.markdown("""
        **Main-sequence lifetime**: $t_{MS} \\approx 10 \\times (M/M_\\odot)^{-2.5}$ Gyr ·
        Compares observed luminosity and temperature against ZAMS predictions.
        """)
        preset_col3, _ = st.columns([1, 2])
        with preset_col3:
            ep = st.selectbox(
                "Presets",
                ["Custom", "☀️ Sun (4.6 Gyr)", "⭐ Sirius (0.24 Gyr)", "🔴 Red Giant (10 Gyr)"],
                key="astro_evol_preset",
            )
        presets_evol = {
            "☀️ Sun (4.6 Gyr)": (1.0, 1.0, 5778.0, 4.6),
            "⭐ Sirius (0.24 Gyr)": (2.06, 25.4, 9940.0, 0.24),
            "🔴 Red Giant (10 Gyr)": (1.0, 100.0, 4500.0, 10.0),
        }
        _me, _le, _te, _ae = presets_evol.get(ep, (1.0, 1.0, 5778.0, 4.6))
        c1, c2 = st.columns(2)
        with c1:
            m_star_e = st.number_input("M★ (M☉)", 0.08, 150.0, _me, 0.1, key="astro_mstar_e")
            l_obs = st.number_input("L_obs (L☉)", 0.0001, 1e6, _le, 0.1, key="astro_lobs")
        with c2:
            t_eff_e = st.number_input("T_eff (K)", 2000.0, 50000.0, _te, 100.0, key="astro_teff_e")
            age_gyr = st.number_input("Age (Gyr)", 0.001, 15.0, _ae, 0.1, key="astro_age")

        if st.button("Compute Evolution", key="astro_evol", type="primary"):
            try:
                from closures.astronomy.stellar_evolution import compute_stellar_evolution

                result = compute_stellar_evolution(m_star_e, l_obs, t_eff_e, age_gyr)
                regime = result["regime"]

                rc1, rc2, rc3, rc4 = st.columns(4)
                with rc1:
                    st.metric("t_MS (Gyr)", f"{result['t_MS']:.3f}")
                with rc2:
                    st.metric("Phase", result["evolutionary_phase"])
                with rc3:
                    st.metric("L_ZAMS (L☉)", f"{result['L_ZAMS']:.4f}")
                with rc4:
                    st.metric("Regime", regime)

                # Age vs MS lifetime gauge
                frac = min(age_gyr / max(result["t_MS"], 0.001), 2.0)
                fig = go.Figure(
                    go.Indicator(
                        mode="gauge+number",
                        value=frac * 100,
                        title={"text": "Age / t_MS (%)"},
                        gauge={
                            "axis": {"range": [0, 200]},
                            "bar": {"color": "#007bff"},
                            "steps": [
                                {"range": [0, 80], "color": "#d4edda"},
                                {"range": [80, 100], "color": "#fff3cd"},
                                {"range": [100, 200], "color": "#f8d7da"},
                            ],
                        },
                    )
                )
                fig.update_layout(height=250, margin={"t": 40, "b": 10})
                st.plotly_chart(fig, use_container_width=True)
            except Exception as e:
                st.error(f"Computation error: {e}")

    # ── Tab 5: Orbital Mechanics ──
    with tab5:
        st.subheader("🪐 Orbital Mechanics")
        st.markdown("""
        **Kepler III**: $P^2 = 4\\pi^2 a^3 / (G M)$ ·
        **Vis-viva**: $v = \\sqrt{GM(2/r - 1/a)}$ ·
        Validates observed period against Kepler prediction.
        """)
        preset_col4, _ = st.columns([1, 2])
        with preset_col4:
            op = st.selectbox("Presets", ["Custom", "🌍 Earth", "♃ Jupiter", "☿ Mercury"], key="astro_orbit_preset")
        presets_orb = {
            "🌍 Earth": (1.0, 1.0, 1.0, 0.017),
            "♃ Jupiter": (11.86, 5.20, 1.0, 0.049),
            "☿ Mercury": (0.2408, 0.387, 1.0, 0.206),
        }
        _po, _ao, _mo, _eo = presets_orb.get(op, (1.0, 1.0, 1.0, 0.017))
        c1, c2 = st.columns(2)
        with c1:
            p_orb = st.number_input("P_orb (years)", 0.001, 1000.0, _po, 0.01, key="astro_porb")
            a_semi = st.number_input("a (AU)", 0.01, 100.0, _ao, 0.01, key="astro_asemi")
        with c2:
            m_total = st.number_input("M_total (M☉)", 0.01, 100.0, _mo, 0.1, key="astro_mtotal")
            e_orb = st.number_input("e (eccentricity)", 0.0, 0.99, _eo, 0.001, key="astro_eorb", format="%.3f")

        if st.button("Compute Orbit", key="astro_orbit", type="primary"):
            try:
                from closures.astronomy.orbital_mechanics import compute_orbital_mechanics

                result = compute_orbital_mechanics(p_orb, a_semi, m_total, e_orb)
                regime = result["regime"]
                regime_color = {"Stable": "🟢", "Eccentric": "🟡"}.get(regime, "🔴")

                rc1, rc2, rc3, rc4 = st.columns(4)
                with rc1:
                    st.metric("P_predicted (yr)", f"{result['P_predicted']:.4f}")
                with rc2:
                    st.metric("Kepler residual", f"{result['kepler_residual']:.6f}")
                with rc3:
                    st.metric("v_orb (km/s)", f"{result['v_orb'] / 1000:.2f}")
                with rc4:
                    st.metric("Regime", f"{regime_color} {regime}")

                # Orbital ellipse visualization
                import math

                theta = [i * 2 * math.pi / 100 for i in range(101)]
                r_vals = [a_semi * (1 - e_orb**2) / (1 + e_orb * math.cos(t)) for t in theta]
                x_vals = [r * math.cos(t) for r, t in zip(r_vals, theta, strict=False)]
                y_vals = [r * math.sin(t) for r, t in zip(r_vals, theta, strict=False)]
                fig = go.Figure()
                fig.add_trace(
                    go.Scatter(x=x_vals, y=y_vals, mode="lines", name="Orbit", line={"color": "#007bff", "width": 2})
                )
                fig.add_trace(
                    go.Scatter(
                        x=[0],
                        y=[0],
                        mode="markers",
                        name="Central body",
                        marker={"size": 12, "color": "#ffc107", "symbol": "star"},
                    )
                )
                fig.update_layout(
                    title=f"Orbital Ellipse (e = {e_orb:.3f})",
                    xaxis_title="x (AU)",
                    yaxis_title="y (AU)",
                    height=350,
                    margin={"t": 40, "b": 20},
                    yaxis_scaleanchor="x",
                    yaxis_scaleratio=1,
                )
                st.plotly_chart(fig, use_container_width=True)
            except Exception as e:
                st.error(f"Computation error: {e}")

    # ── Tab 6: Gravitational Dynamics ──
    with tab6:
        st.subheader("🌀 Gravitational Dynamics")
        st.markdown("""
        **Virial mass**: $M_{\\text{vir}} = R \\sigma_v^2 / G$ ·
        **Dark matter fraction**: $f_{DM} = 1 - M_{\\text{lum}} / M_{\\text{vir}}$ ·
        Tests virial equilibrium in galaxy-scale systems.
        """)
        preset_col5, _ = st.columns([1, 2])
        with preset_col5:
            gp = st.selectbox(
                "Presets",
                ["Custom", "🌌 Milky Way", "🌀 Andromeda (M31)", "🔴 Dwarf Spheroidal"],
                key="astro_dyn_preset",
            )
        presets_dyn = {
            "🌌 Milky Way": (220.0, 8.0, 150.0, 5e10),
            "🌀 Andromeda (M31)": (250.0, 20.0, 180.0, 7e10),
            "🔴 Dwarf Spheroidal": (10.0, 0.3, 8.0, 1e7),
        }
        _vr, _ro, _sv, _ml = presets_dyn.get(gp, (220.0, 8.0, 150.0, 5e10))
        c1, c2 = st.columns(2)
        with c1:
            v_rot = st.number_input("v_rot (km/s)", 1.0, 500.0, _vr, 1.0, key="astro_vrot")
            r_obs = st.number_input("r_obs (kpc)", 0.01, 1000.0, _ro, 0.1, key="astro_robs")
        with c2:
            sigma_v = st.number_input("σ_v (km/s)", 1.0, 500.0, _sv, 1.0, key="astro_sigmav")
            m_lum = st.number_input("M_lum (M☉)", 1e5, 1e13, _ml, 1e9, key="astro_mlum", format="%.2e")

        if st.button("Compute Dynamics", key="astro_dyn", type="primary"):
            try:
                from closures.astronomy.gravitational_dynamics import compute_gravitational_dynamics

                result = compute_gravitational_dynamics(v_rot, r_obs, sigma_v, m_lum)
                regime = result["regime"]
                regime_color = {"Equilibrium": "🟢", "Relaxing": "🟡"}.get(regime, "🔴")

                rc1, rc2, rc3, rc4 = st.columns(4)
                with rc1:
                    st.metric("M_virial (M☉)", f"{result['M_virial']:.3e}")
                with rc2:
                    st.metric("M_dynamic (M☉)", f"{result['M_dynamic']:.3e}")
                with rc3:
                    st.metric("DM fraction", f"{result['dark_matter_fraction']:.2%}")
                with rc4:
                    st.metric("Regime", f"{regime_color} {regime}")

                st.metric("Virial ratio", f"{result['virial_ratio']:.4f}")

                # Pie chart: luminous vs dark matter
                dm_frac = max(0, min(result["dark_matter_fraction"], 1.0))
                fig = go.Figure(
                    go.Pie(
                        labels=["Luminous Matter", "Dark Matter"],
                        values=[1 - dm_frac, dm_frac],
                        marker={"colors": ["#ffc107", "#343a40"]},
                        hole=0.4,
                        textinfo="label+percent",
                    )
                )
                fig.update_layout(title="Mass Budget", height=300, margin={"t": 40, "b": 20})
                st.plotly_chart(fig, use_container_width=True)
            except Exception as e:
                st.error(f"Computation error: {e}")


def render_nuclear_page() -> None:
    """Render interactive Nuclear Physics domain page with all 6 closures."""
    if st is None:
        return
    if go is None or pd is None or np is None:
        st.error(
            "Dashboard dependencies (numpy, pandas, plotly) could not be loaded. Install with: `pip install umcp[viz]`"
        )
        return

    _ensure_closures_path()

    st.title("☢️ Nuclear Physics Domain")
    st.caption(
        "NUC.INTSTACK.v1 — Binding energy, alpha decay, shell structure, fissility, decay chains, double-sided collapse"
    )

    with st.expander("📖 Domain Overview", expanded=False):
        st.markdown("""
        The **Nuclear Physics** domain maps nuclear observables into UMCP contract space.
        All closures return **NamedTuple** results with UMCP invariants (ω_eff, F_eff, Ψ).

        | Closure | Physics | Key Observable | Reference |
        |---------|---------|---------------|-----------|
        | Binding Energy | Semi-Empirical Mass Formula (Weizsäcker) | BE/A (MeV/nucleon) | Ni-62 = 8.7945 MeV |
        | Alpha Decay | Geiger-Nuttall / Gamow tunneling | log₁₀(T½) | ²³⁸U → ²³⁴Th |
        | Shell Structure | Magic numbers: 2, 8, 20, 28, 50, 82, 126 | Shell closure strength | ²⁰⁸Pb doubly magic |
        | Fissility | Z²/A vs critical fissility | x = (Z²/A) / (Z²/A)_crit | (Z²/A)_crit ≈ 48.26 |
        | Decay Chain | Sequential α/β decay pathway | Chain length, bottleneck | ²³⁸U → ²⁰⁶Pb (14 steps) |
        | Double-Sided Collapse | Fusion ↔ Fission convergence | Iron peak distance | Fe-56 = 0 distance |
        """)

    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(
        [
            "⚛️ Binding Energy",
            "💫 Alpha Decay",
            "🐚 Shell Structure",
            "💣 Fissility",
            "🔗 Decay Chain",
            "🔄 Double-Sided Collapse",
        ]
    )

    # ── Tab 1: Binding Energy (SEMF) ──
    with tab1:
        st.subheader("⚛️ Nuclide Binding Energy (SEMF)")
        st.markdown("""
        **Weizsäcker formula**: $B(Z,A) = a_V A - a_S A^{2/3} - a_C Z(Z-1)A^{-1/3} - a_A (A-2Z)^2/A + \\delta$

        The iron peak (Ni-62, Fe-56) at **8.79 MeV/nucleon** defines the maximum binding energy per nucleon —
        the UMCP collapse attractor for nuclear matter.
        """)

        preset_col, _ = st.columns([1, 2])
        with preset_col:
            bp = st.selectbox(
                "Presets",
                [
                    "Custom",
                    "⚛️ Fe-56 (Iron)",
                    "☢️ U-238",
                    "🔵 Pb-208 (Doubly Magic)",
                    "🧪 He-4 (Alpha)",
                    "💎 C-12 (Carbon)",
                ],
                key="nuc_bind_preset",
                help="Select a nuclide or enter custom Z, A",
            )
        presets_bind = {
            "⚛️ Fe-56 (Iron)": (26, 56),
            "☢️ U-238": (92, 238),
            "🔵 Pb-208 (Doubly Magic)": (82, 208),
            "🧪 He-4 (Alpha)": (2, 4),
            "💎 C-12 (Carbon)": (6, 12),
        }
        _z, _a = presets_bind.get(bp, (26, 56))
        c1, c2 = st.columns(2)
        with c1:
            z_val = st.number_input("Z (protons)", 1, 120, _z, key="nuc_z", help="Atomic number (number of protons)")
        with c2:
            a_val = st.number_input(
                "A (mass number)", 1, 300, _a, key="nuc_a", help="Total nucleon count (protons + neutrons)"
            )

        if st.button("Compute Binding", key="nuc_bind", type="primary"):
            try:
                from closures.nuclear_physics import compute_binding

                result = compute_binding(z_val, a_val)
                rd = result._asdict()
                regime = rd["regime"]
                regime_color = {"Peak": "🟢", "Plateau": "🟢", "Slope": "🟡"}.get(regime, "🔴")

                rc1, rc2, rc3, rc4 = st.columns(4)
                with rc1:
                    st.metric("BE/A (MeV)", f"{rd['BE_per_A']:.4f}")
                with rc2:
                    st.metric("BE_total (MeV)", f"{rd['BE_total']:.2f}")
                with rc3:
                    st.metric("ω_eff (deficit)", f"{rd['omega_eff']:.4f}")
                with rc4:
                    st.metric("Regime", f"{regime_color} {regime}")

                mc1, mc2 = st.columns(2)
                with mc1:
                    st.metric("F_eff = 1 − ω", f"{rd['F_eff']:.4f}")
                with mc2:
                    st.metric("Ψ_BE (embedding)", f"{rd['Psi_BE']:.4f}")

                # Binding energy curve visualization
                from closures.nuclear_physics import compute_binding as _cb

                a_range = list(range(4, 260, 2))
                be_curve = []
                for _ai in a_range:
                    _zi = max(1, round(_ai * 0.42))  # approximate Z ≈ 0.42 * A
                    try:
                        _ri = _cb(_zi, _ai)
                        be_curve.append({"A": _ai, "BE/A": _ri.BE_per_A})
                    except Exception:
                        pass

                if be_curve:
                    fig = go.Figure()
                    fig.add_trace(
                        go.Scatter(
                            x=[d["A"] for d in be_curve],
                            y=[d["BE/A"] for d in be_curve],
                            mode="lines",
                            name="SEMF Curve",
                            line={"color": "#007bff", "width": 2},
                        )
                    )
                    fig.add_trace(
                        go.Scatter(
                            x=[a_val],
                            y=[rd["BE_per_A"]],
                            mode="markers",
                            name=f"Z={z_val}, A={a_val}",
                            marker={"size": 12, "color": "red", "symbol": "star"},
                        )
                    )
                    fig.add_hline(
                        y=8.7945, line_dash="dash", line_color="green", annotation_text="Iron peak (8.7945 MeV)"
                    )
                    fig.update_layout(
                        title="Nuclear Binding Energy Curve",
                        xaxis_title="Mass Number A",
                        yaxis_title="BE/A (MeV/nucleon)",
                        height=350,
                        margin={"t": 40, "b": 20},
                    )
                    st.plotly_chart(fig, use_container_width=True)
            except Exception as e:
                st.error(f"Computation error: {e}")

    # ── Tab 2: Alpha Decay ──
    with tab2:
        st.subheader("💫 Alpha Decay (Geiger-Nuttall)")
        st.markdown("""
        **Geiger-Nuttall law**: $\\log_{10}(T_{1/2}) = a / \\sqrt{Q_\\alpha} + b$

        An alpha particle (⁴He) tunnels through the Coulomb barrier.
        The Q-value determines disintegration energy; the Gamow factor sets the tunneling probability.
        """)
        preset_col2, _ = st.columns([1, 2])
        with preset_col2:
            ap = st.selectbox(
                "Presets",
                [
                    "Custom",
                    "☢️ U-238 (Q=4.27 MeV)",
                    "☢️ Pu-239 (Q=5.24 MeV)",
                    "☢️ Ra-226 (Q=4.87 MeV)",
                    "☢️ Po-210 (Q=5.41 MeV)",
                ],
                key="nuc_alpha_preset",
            )
        presets_alpha = {
            "☢️ U-238 (Q=4.27 MeV)": (92, 238, 4.27),
            "☢️ Pu-239 (Q=5.24 MeV)": (94, 239, 5.24),
            "☢️ Ra-226 (Q=4.87 MeV)": (88, 226, 4.87),
            "☢️ Po-210 (Q=5.41 MeV)": (84, 210, 5.41),
        }
        _za, _aa, _qa = presets_alpha.get(ap, (92, 238, 4.27))
        c1, c2, c3 = st.columns(3)
        with c1:
            z_ad = st.number_input("Z (parent)", 2, 120, _za, key="nuc_z_ad")
        with c2:
            a_ad = st.number_input("A (parent)", 4, 300, _aa, key="nuc_a_ad")
        with c3:
            q_alpha = st.number_input("Q_α (MeV)", 0.1, 15.0, _qa, 0.01, key="nuc_qalpha")

        if st.button("Compute Alpha Decay", key="nuc_alpha", type="primary"):
            try:
                from closures.nuclear_physics import compute_alpha_decay

                result = compute_alpha_decay(z_ad, a_ad, q_alpha)
                rd = result._asdict()
                regime = rd["regime"]
                regime_color = {"Stable": "🟢", "Geological": "🟢", "Laboratory": "🟡", "Eternal": "🟢"}.get(
                    regime, "🔴"
                )

                rc1, rc2, rc3, rc4 = st.columns(4)
                with rc1:
                    st.metric("Q_α (MeV)", f"{rd['Q_alpha']:.4f}")
                with rc2:
                    st.metric("log₁₀(T½/s)", f"{rd['log10_half_life_s']:.2f}")
                with rc3:
                    st.metric("Ψ_Q_α", f"{rd['Psi_Q_alpha']:.4f}")
                with rc4:
                    st.metric("Regime", f"{regime_color} {regime}")

                mc1, mc2 = st.columns(2)
                with mc1:
                    st.metric("T½ (s)", f"{rd['half_life_s']:.3e}")
                with mc2:
                    st.metric("Mean lifetime τ (s)", f"{rd['mean_lifetime_s']:.3e}")

                # Decay scheme visualization
                parent = f"Z={z_ad}, A={a_ad}"
                daughter = f"Z={z_ad - 2}, A={a_ad - 4}"
                fig = go.Figure()
                fig.add_trace(
                    go.Bar(
                        x=[parent, "α particle (⁴He)", daughter],
                        y=[a_ad, 4, a_ad - 4],
                        marker_color=["#dc3545", "#ffc107", "#28a745"],
                        text=[f"A={a_ad}", "A=4", f"A={a_ad - 4}"],
                        textposition="outside",
                    )
                )
                fig.update_layout(
                    title=f"Alpha Decay: {parent} → {daughter} + α",
                    yaxis_title="Mass Number A",
                    height=300,
                    margin={"t": 40, "b": 20},
                )
                st.plotly_chart(fig, use_container_width=True)
            except Exception as e:
                st.error(f"Computation error: {e}")

    # ── Tab 3: Shell Structure ──
    with tab3:
        st.subheader("🐚 Shell Structure")
        st.markdown("""
        **Nuclear magic numbers**: 2, 8, 20, 28, 50, 82, 126

        Nuclei at or near magic numbers have enhanced stability (closed shells).
        **Doubly-magic** nuclei (both Z and N magic) are exceptionally stable: ⁴He, ¹⁶O, ⁴⁰Ca, ⁴⁸Ca, ⁴⁸Ni, ²⁰⁸Pb.
        """)
        preset_col3, _ = st.columns([1, 2])
        with preset_col3:
            sp = st.selectbox(
                "Presets",
                [
                    "Custom",
                    "🔵 Pb-208 (Z=82, N=126)",
                    "⚛️ Ca-40 (Z=20, N=20)",
                    "🧪 O-16 (Z=8, N=8)",
                    "☢️ Sn-132 (Z=50, N=82)",
                ],
                key="nuc_shell_preset",
            )
        presets_shell = {
            "🔵 Pb-208 (Z=82, N=126)": (82, 208),
            "⚛️ Ca-40 (Z=20, N=20)": (20, 40),
            "🧪 O-16 (Z=8, N=8)": (8, 16),
            "☢️ Sn-132 (Z=50, N=82)": (50, 132),
        }
        _zs, _as = presets_shell.get(sp, (50, 120))
        c1, c2 = st.columns(2)
        with c1:
            z_sh = st.number_input("Z (protons)", 1, 120, _zs, key="nuc_z_sh")
        with c2:
            a_sh = st.number_input("A (mass number)", 1, 300, _as, key="nuc_a_sh")

        if st.button("Compute Shell", key="nuc_shell", type="primary"):
            try:
                from closures.nuclear_physics import compute_shell

                result = compute_shell(z_sh, a_sh)
                rd = result._asdict()
                regime = rd["regime"]
                regime_color = {"DoublyMagic": "🟢", "SinglyMagic": "🟢", "NearMagic": "🟡"}.get(regime, "🔴")
                n_val = rd["N"]

                rc1, rc2, rc3, rc4 = st.columns(4)
                with rc1:
                    st.metric("Z", rd["Z"])
                with rc2:
                    st.metric("N", n_val)
                with rc3:
                    st.metric("Doubly Magic", "Yes ✨" if rd["doubly_magic"] else "No")
                with rc4:
                    st.metric("Regime", f"{regime_color} {regime}")

                mc1, mc2, mc3, mc4 = st.columns(4)
                with mc1:
                    st.metric("Magic Z?", "Yes" if rd["magic_proton"] else "No")
                with mc2:
                    st.metric("Nearest Magic Z", f"{rd['nearest_magic_Z']}")
                with mc3:
                    st.metric("Magic N?", "Yes" if rd["magic_neutron"] else "No")
                with mc4:
                    st.metric("Nearest Magic N", f"{rd['nearest_magic_N']}")

                dc1, dc2 = st.columns(2)
                with dc1:
                    st.metric("Distance to Magic Z", f"{rd['distance_to_magic_Z']}")
                with dc2:
                    st.metric("Distance to Magic N", f"{rd['distance_to_magic_N']}")
                st.metric("Shell Correction (MeV)", f"{rd['shell_correction']:.4f}")

                # Magic numbers proximity chart
                magic = [2, 8, 20, 28, 50, 82, 126]
                fig = go.Figure()
                fig.add_trace(
                    go.Scatter(
                        x=magic,
                        y=[0] * len(magic),
                        mode="markers+text",
                        marker={"size": 20, "color": "#28a745", "symbol": "diamond"},
                        text=[str(m) for m in magic],
                        textposition="top center",
                        name="Magic Numbers",
                    )
                )
                fig.add_trace(
                    go.Scatter(
                        x=[z_sh],
                        y=[0.1],
                        mode="markers+text",
                        marker={"size": 15, "color": "#dc3545"},
                        text=[f"Z={z_sh}"],
                        textposition="top center",
                        name="Proton count",
                    )
                )
                fig.add_trace(
                    go.Scatter(
                        x=[n_val],
                        y=[-0.1],
                        mode="markers+text",
                        marker={"size": 15, "color": "#007bff"},
                        text=[f"N={n_val}"],
                        textposition="bottom center",
                        name="Neutron count",
                    )
                )
                fig.update_layout(
                    title="Magic Number Proximity",
                    xaxis_title="Nucleon Count",
                    yaxis={"visible": False, "range": [-0.5, 0.5]},
                    height=250,
                    margin={"t": 40, "b": 20},
                    showlegend=True,
                )
                st.plotly_chart(fig, use_container_width=True)
            except Exception as e:
                st.error(f"Computation error: {e}")

    # ── Tab 4: Fissility ──
    with tab4:
        st.subheader("💣 Fissility Assessment")
        st.markdown("""
        **Fissility parameter**: $x = (Z^2/A) / (Z^2/A)_{\\text{crit}}$

        When $x \\geq 1$, the Coulomb repulsion overcomes surface tension and the nucleus is
        **spontaneously fissile**. $(Z^2/A)_{\\text{crit}} \\approx 48.26$ (liquid drop model).
        """)
        preset_col4, _ = st.columns([1, 2])
        with preset_col4:
            fp = st.selectbox(
                "Presets",
                ["Custom", "☢️ U-235 (fissile)", "☢️ U-238", "☢️ Pu-239", "⚛️ Fe-56 (stable)"],
                key="nuc_fiss_preset",
            )
        presets_fiss = {
            "☢️ U-235 (fissile)": (92, 235),
            "☢️ U-238": (92, 238),
            "☢️ Pu-239": (94, 239),
            "⚛️ Fe-56 (stable)": (26, 56),
        }
        _zf, _af = presets_fiss.get(fp, (92, 235))
        c1, c2 = st.columns(2)
        with c1:
            z_fi = st.number_input("Z", 1, 120, _zf, key="nuc_z_fi")
        with c2:
            a_fi = st.number_input("A", 1, 300, _af, key="nuc_a_fi")

        if st.button("Compute Fissility", key="nuc_fiss", type="primary"):
            try:
                from closures.nuclear_physics import compute_fissility

                result = compute_fissility(z_fi, a_fi)
                rd = result._asdict()
                regime = rd["regime"]
                regime_color = {"Subfissile": "🟢", "Transitional": "🟡", "Fissile": "🔴"}.get(regime, "🔴")

                rc1, rc2, rc3, rc4 = st.columns(4)
                with rc1:
                    st.metric("x (fissility)", f"{rd['fissility_x']:.4f}")
                with rc2:
                    st.metric("Z²/A", f"{rd['Z_squared_over_A']:.2f}")
                with rc3:
                    st.metric("Ψ_fiss", f"{rd['Psi_fiss']:.4f}")
                with rc4:
                    st.metric("Regime", f"{regime_color} {regime}")

                mc1, mc2 = st.columns(2)
                with mc1:
                    st.metric("Coulomb Energy (MeV)", f"{rd['coulomb_energy']:.2f}")
                with mc2:
                    st.metric("Surface Energy (MeV)", f"{rd['surface_energy']:.2f}")

                # Fissility gauge
                x_val = rd["fissility_x"]
                fig = go.Figure(
                    go.Indicator(
                        mode="gauge+number",
                        value=x_val,
                        title={"text": "Fissility Parameter x"},
                        gauge={
                            "axis": {"range": [0, 1.5]},
                            "bar": {"color": "#dc3545" if x_val >= 1.0 else "#ffc107" if x_val >= 0.7 else "#28a745"},
                            "steps": [
                                {"range": [0, 0.7], "color": "#d4edda"},
                                {"range": [0.7, 1.0], "color": "#fff3cd"},
                                {"range": [1.0, 1.5], "color": "#f8d7da"},
                            ],
                            "threshold": {"line": {"color": "red", "width": 3}, "value": 1.0},
                        },
                    )
                )
                fig.update_layout(height=250, margin={"t": 40, "b": 10})
                st.plotly_chart(fig, use_container_width=True)
            except Exception as e:
                st.error(f"Computation error: {e}")

    # ── Tab 5: Decay Chain ──
    with tab5:
        st.subheader("🔗 Decay Chain Analysis")
        st.markdown("""
        Analyzes a sequential decay pathway. Provide the chain steps as a series of α and β decays.
        The closure computes chain statistics: total nucleon shedding, bottleneck half-life, and endpoint.

        *Note: This closure takes pre-defined chain steps (isotope, decay mode, half-life, Q-value).*
        """)

        st.info("📋 Using the standard **²³⁸U → ²⁰⁶Pb** decay chain (14 α + β steps)")

        if st.button("Analyze U-238 Decay Chain", key="nuc_chain", type="primary"):
            try:
                from closures.nuclear_physics.decay_chain import ChainStep, compute_decay_chain

                # Standard U-238 → Pb-206 decay chain
                u238_chain = [
                    ChainStep(isotope="U-238", Z=92, A=238, decay_mode="alpha", half_life_s=1.41e17, Q_MeV=4.27),
                    ChainStep(isotope="Th-234", Z=90, A=234, decay_mode="beta_minus", half_life_s=2.08e6, Q_MeV=0.27),
                    ChainStep(isotope="Pa-234", Z=91, A=234, decay_mode="beta_minus", half_life_s=70.2, Q_MeV=2.20),
                    ChainStep(isotope="U-234", Z=92, A=234, decay_mode="alpha", half_life_s=7.75e12, Q_MeV=4.86),
                    ChainStep(isotope="Th-230", Z=90, A=230, decay_mode="alpha", half_life_s=2.38e12, Q_MeV=4.77),
                    ChainStep(isotope="Ra-226", Z=88, A=226, decay_mode="alpha", half_life_s=5.05e10, Q_MeV=4.87),
                    ChainStep(isotope="Rn-222", Z=86, A=222, decay_mode="alpha", half_life_s=3.30e5, Q_MeV=5.59),
                    ChainStep(isotope="Po-218", Z=84, A=218, decay_mode="alpha", half_life_s=186.0, Q_MeV=6.11),
                    ChainStep(isotope="Pb-214", Z=82, A=214, decay_mode="beta_minus", half_life_s=1608.0, Q_MeV=1.02),
                    ChainStep(isotope="Bi-214", Z=83, A=214, decay_mode="beta_minus", half_life_s=1194.0, Q_MeV=3.27),
                    ChainStep(isotope="Po-214", Z=84, A=214, decay_mode="alpha", half_life_s=1.64e-4, Q_MeV=7.83),
                    ChainStep(isotope="Pb-210", Z=82, A=210, decay_mode="beta_minus", half_life_s=7.01e8, Q_MeV=0.06),
                    ChainStep(isotope="Bi-210", Z=83, A=210, decay_mode="beta_minus", half_life_s=4.33e5, Q_MeV=1.16),
                    ChainStep(isotope="Po-210", Z=84, A=210, decay_mode="alpha", half_life_s=1.20e7, Q_MeV=5.41),
                ]

                result = compute_decay_chain(u238_chain)
                rd = result._asdict()
                regime = rd["regime"]
                regime_color = {"ZeroStep": "🟢", "Dominated": "🟢", "Cascade": "🟡"}.get(regime, "🔴")

                rc1, rc2, rc3, rc4 = st.columns(4)
                with rc1:
                    st.metric("Chain Length", rd["chain_length"])
                with rc2:
                    st.metric("α decays", rd["alpha_count"])
                with rc3:
                    st.metric("β⁻ decays", rd["beta_minus_count"])
                with rc4:
                    st.metric("Regime", f"{regime_color} {regime}")

                mc1, mc2, mc3, mc4 = st.columns(4)
                with mc1:
                    st.metric("Endpoint", rd["endpoint_isotope"])
                with mc2:
                    st.metric("Total Q (MeV)", f"{rd['total_Q_MeV']:.2f}")
                with mc3:
                    st.metric("Nucleons shed", rd["total_nucleons_shed"])
                with mc4:
                    st.metric("Bottleneck", f"{rd['bottleneck_step']}")

                # Chain visualization
                chain_data = []
                for step in u238_chain:
                    chain_data.append(
                        {
                            "Isotope": step.isotope,
                            "Z": step.Z,
                            "A": step.A,
                            "Decay": step.decay_mode,
                            "T½ (s)": f"{step.half_life_s:.2e}",
                            "Q (MeV)": f"{step.Q_MeV:.2f}",
                        }
                    )
                chain_data.append(
                    {"Isotope": "Pb-206 (stable)", "Z": 82, "A": 206, "Decay": "—", "T½ (s)": "stable", "Q (MeV)": "—"}
                )
                st.dataframe(pd.DataFrame(chain_data), use_container_width=True, hide_index=True)

                # A vs step chart
                fig = go.Figure()
                a_vals = [s.A for s in u238_chain] + [206]
                labels = [s.isotope for s in u238_chain] + ["Pb-206"]
                fig.add_trace(
                    go.Scatter(
                        x=list(range(len(a_vals))),
                        y=a_vals,
                        mode="lines+markers+text",
                        text=labels,
                        textposition="top center",
                        name="Mass Number A",
                        marker={"size": 8, "color": "#007bff"},
                        line={"width": 2},
                    )
                )
                fig.update_layout(
                    title="Decay Chain: Mass Number vs Step",
                    xaxis_title="Step",
                    yaxis_title="A",
                    height=350,
                    margin={"t": 40, "b": 20},
                )
                st.plotly_chart(fig, use_container_width=True)
            except Exception as e:
                st.error(f"Computation error: {e}")

    # ── Tab 6: Double-Sided Collapse ──
    with tab6:
        st.subheader("🔄 Double-Sided Collapse")
        st.markdown("""
        **AX-N4**: Nuclear binding energy converges on the iron peak from **both sides**:
        - **Light nuclei** (A < 56): energy released by **fusion** → moving right on the curve
        - **Heavy nuclei** (A > 56): energy released by **fission** → moving left on the curve

        The signed distance from Fe-56 quantifies how far a nuclide is from the collapse attractor.
        """)
        preset_col6, _ = st.columns([1, 2])
        with preset_col6:
            dsp = st.selectbox(
                "Presets",
                [
                    "Custom",
                    "⚛️ Fe-56 (at peak)",
                    "🧪 He-4 (fusion fuel)",
                    "☢️ U-238 (fission fuel)",
                    "💎 C-12 (stellar fusion)",
                ],
                key="nuc_ds_preset",
            )
        presets_ds = {
            "⚛️ Fe-56 (at peak)": (26, 56),
            "🧪 He-4 (fusion fuel)": (2, 4),
            "☢️ U-238 (fission fuel)": (92, 238),
            "💎 C-12 (stellar fusion)": (6, 12),
        }
        _zd, _ad = presets_ds.get(dsp, (26, 56))
        c1, c2 = st.columns(2)
        with c1:
            z_ds = st.number_input("Z", 1, 120, _zd, key="nuc_z_ds")
        with c2:
            a_ds = st.number_input("A", 1, 300, _ad, key="nuc_a_ds")

        if st.button("Compute Double-Sided", key="nuc_ds", type="primary"):
            try:
                from closures.nuclear_physics import compute_binding, compute_double_sided

                binding = compute_binding(z_ds, a_ds)
                result = compute_double_sided(z_ds, a_ds, binding.BE_per_A)
                rd = result._asdict()
                regime = rd["regime"]
                regime_color = {"AtPeak": "🟢", "NearPeak": "🟢", "Convergent": "🟡"}.get(regime, "🔴")

                rc1, rc2, rc3, rc4 = st.columns(4)
                with rc1:
                    st.metric("BE/A (MeV)", f"{rd['BE_per_A']:.4f}")
                with rc2:
                    st.metric("Signed Distance", f"{rd['signed_distance']:.4f}")
                with rc3:
                    st.metric("Side", rd["side"])
                with rc4:
                    st.metric("Regime", f"{regime_color} {regime}")

                mc1, mc2, mc3 = st.columns(3)
                with mc1:
                    st.metric("|Distance|", f"{rd['abs_distance']:.4f}")
                with mc2:
                    st.metric("Convergence", rd["convergence_direction"])
                with mc3:
                    st.metric("ω_eff", f"{rd['omega_eff']:.4f}")

                # Double-sided visualization: position on the binding curve
                from closures.nuclear_physics import compute_binding as _cb2

                a_range2 = list(range(4, 260, 2))
                be_data2 = []
                for _ai2 in a_range2:
                    _zi2 = max(1, round(_ai2 * 0.42))
                    try:
                        _ri2 = _cb2(_zi2, _ai2)
                        be_data2.append({"A": _ai2, "BE/A": _ri2.BE_per_A})
                    except Exception:
                        pass

                if be_data2:
                    fig = go.Figure()
                    # Color the curve by side
                    a_list = [d["A"] for d in be_data2]
                    be_list = [d["BE/A"] for d in be_data2]
                    fusion_a = [a for a in a_list if a <= 56]
                    fusion_be = [be for a, be in zip(a_list, be_list, strict=False) if a <= 56]
                    fission_a = [a for a in a_list if a >= 56]
                    fission_be = [be for a, be in zip(a_list, be_list, strict=False) if a >= 56]
                    fig.add_trace(
                        go.Scatter(
                            x=fusion_a,
                            y=fusion_be,
                            mode="lines",
                            name="Fusion side",
                            line={"color": "#007bff", "width": 2},
                            fill="tozeroy",
                            fillcolor="rgba(0,123,255,0.1)",
                        )
                    )
                    fig.add_trace(
                        go.Scatter(
                            x=fission_a,
                            y=fission_be,
                            mode="lines",
                            name="Fission side",
                            line={"color": "#dc3545", "width": 2},
                            fill="tozeroy",
                            fillcolor="rgba(220,53,69,0.1)",
                        )
                    )
                    fig.add_trace(
                        go.Scatter(
                            x=[a_ds],
                            y=[rd["BE_per_A"]],
                            mode="markers",
                            name=f"Z={z_ds}, A={a_ds}",
                            marker={
                                "size": 14,
                                "color": "#ffc107",
                                "symbol": "star",
                                "line": {"width": 2, "color": "black"},
                            },
                        )
                    )
                    # Arrow showing convergence direction
                    fig.add_annotation(
                        x=56, y=8.8, text="← Fusion | Fission →", showarrow=False, font={"size": 12, "color": "gray"}
                    )
                    fig.update_layout(
                        title="Double-Sided Collapse: Convergence on Iron Peak",
                        xaxis_title="A",
                        yaxis_title="BE/A (MeV/nucleon)",
                        height=380,
                        margin={"t": 40, "b": 20},
                    )
                    st.plotly_chart(fig, use_container_width=True)
            except Exception as e:
                st.error(f"Computation error: {e}")


def render_quantum_page() -> None:
    """Render interactive Quantum Mechanics domain page with all 6 closures."""
    if st is None:
        return
    if go is None or pd is None or np is None:
        st.error(
            "Dashboard dependencies (numpy, pandas, plotly) could not be loaded. Install with: `pip install umcp[viz]`"
        )
        return

    _ensure_closures_path()

    st.title("🔮 Quantum Mechanics Domain")
    st.caption("QM.INTSTACK.v1 — Born rule, entanglement, tunneling, harmonic oscillator, spin, uncertainty")

    with st.expander("📖 Domain Overview", expanded=False):
        st.markdown("""
        The **Quantum Mechanics** domain maps quantum observables into UMCP contract space.
        Each closure validates a fundamental quantum principle against measurement data.

        | Closure | Principle | Key Observable |
        |---------|-----------|---------------|
        | Wavefunction Collapse | Born rule: P = |ψ|² | Born deviation δP |
        | Entanglement | Bell's theorem, CHSH inequality | Concurrence, S_vN |
        | Tunneling | WKB approximation, Gamow factor | Transmission coefficient T |
        | Harmonic Oscillator | E_n = ℏω(n + ½) | Energy level spacing |
        | Spin Measurement | Stern-Gerlach, Zeeman effect | Larmor frequency |
        | Uncertainty Principle | ΔxΔp ≥ ℏ/2 | Heisenberg ratio |
        """)

    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(
        [
            "🎲 Wavefunction Collapse",
            "🔗 Entanglement",
            "🚇 Tunneling",
            "🎵 Harmonic Oscillator",
            "🧭 Spin Measurement",
            "📏 Uncertainty Principle",
        ]
    )

    # ── Tab 1: Wavefunction Collapse ──
    with tab1:
        st.subheader("🎲 Wavefunction Collapse (Born Rule)")
        st.markdown("""
        **Born rule**: $P_i = |\\langle i | \\psi \\rangle|^2$ — the probability of measuring
        outcome $i$ equals the squared amplitude of the wavefunction projected onto that eigenstate.

        Enter wavefunction amplitudes and observed measurement probabilities to test Born-rule fidelity.
        """)

        preset_col, _ = st.columns([1, 2])
        with preset_col:
            qcp = st.selectbox(
                "Presets",
                ["Custom", "🎯 Perfect Born", "📐 Superposition", "🌀 Decoherent"],
                key="qm_coll_preset",
                help="Choose a quantum state scenario",
            )
        presets_coll = {
            "🎯 Perfect Born": ("0.6, 0.8", "0.36, 0.64"),
            "📐 Superposition": ("0.707, 0.707", "0.50, 0.50"),
            "🌀 Decoherent": ("0.6, 0.8", "0.50, 0.50"),
        }
        _psi, _prob = presets_coll.get(qcp, ("0.6, 0.8", "0.35, 0.65"))
        c1, c2 = st.columns(2)
        with c1:
            psi_str = st.text_input(
                "ψ amplitudes (comma-separated)", _psi, key="qm_psi", help="Wavefunction amplitudes, e.g. 0.6, 0.8"
            )
        with c2:
            prob_str = st.text_input(
                "P measured (comma-separated)", _prob, key="qm_prob", help="Observed probabilities, e.g. 0.36, 0.64"
            )

        if st.button("Compute Collapse", key="qm_collapse", type="primary"):
            try:
                from closures.quantum_mechanics.wavefunction_collapse import compute_wavefunction_collapse

                psi = [float(x.strip()) for x in psi_str.split(",")]
                probs = [float(x.strip()) for x in prob_str.split(",")]
                result = compute_wavefunction_collapse(psi, probs)
                regime = result["regime"]
                regime_color = {"Faithful": "🟢", "Perturbed": "🟡"}.get(regime, "🔴")

                rc1, rc2, rc3, rc4 = st.columns(4)
                with rc1:
                    st.metric("P_born", f"{result['P_born']:.4f}")
                with rc2:
                    st.metric("δP (deviation)", f"{result['delta_P']:.6f}")
                with rc3:
                    st.metric("Fidelity", f"{result['fidelity_state']:.4f}")
                with rc4:
                    st.metric("Regime", f"{regime_color} {regime}")
                st.metric("Purity", f"{result['purity']:.4f}")

                # Born vs observed bar chart
                born_probs = [abs(float(x.strip())) ** 2 for x in psi_str.split(",")]
                norm = sum(born_probs)
                born_probs = [p / norm for p in born_probs]
                meas_probs = [float(x.strip()) for x in prob_str.split(",")]
                labels = [f"|{i}⟩" for i in range(len(born_probs))]

                fig = go.Figure()
                fig.add_trace(go.Bar(x=labels, y=born_probs, name="Born prediction", marker_color="#007bff"))
                fig.add_trace(go.Bar(x=labels, y=meas_probs, name="Measured", marker_color="#dc3545"))
                fig.update_layout(
                    title="Born Rule: Predicted vs Measured",
                    yaxis_title="Probability",
                    barmode="group",
                    height=300,
                    margin={"t": 40, "b": 20},
                )
                st.plotly_chart(fig, use_container_width=True)
            except Exception as e:
                st.error(f"Computation error: {e}")

    # ── Tab 2: Entanglement ──
    with tab2:
        st.subheader("🔗 Entanglement Analysis")
        st.markdown("""
        **Von Neumann entropy**: $S_{vN} = -\\text{tr}(\\rho \\ln \\rho)$ ·
        **Bell-CHSH inequality**: $|S| \\leq 2$ (classical), $|S| \\leq 2\\sqrt{2}$ (quantum max)

        Enter the density matrix eigenvalues and optional Bell correlations.
        """)
        preset_col2, _ = st.columns([1, 2])
        with preset_col2:
            ep = st.selectbox(
                "Presets", ["Custom", "🔗 Bell State (maximal)", "📐 Separable", "🌀 Mixed"], key="qm_ent_preset"
            )
        presets_ent = {
            "🔗 Bell State (maximal)": ("0.5, 0.5, 0.0, 0.0", "0.707, 0.707, 0.707, -0.707"),
            "📐 Separable": ("1.0, 0.0, 0.0, 0.0", "0.5, 0.5, 0.5, -0.5"),
            "🌀 Mixed": ("0.5, 0.3, 0.15, 0.05", "0.7, 0.7, 0.7, -0.7"),
        }
        _rho, _bell = presets_ent.get(ep, ("0.5, 0.3, 0.15, 0.05", "0.7, 0.7, 0.7, -0.7"))
        rho_str = st.text_input("ρ eigenvalues (comma-separated)", _rho, key="qm_rho")
        bell_str = st.text_input("Bell correlations (4 values)", _bell, key="qm_bell")

        if st.button("Compute Entanglement", key="qm_ent", type="primary"):
            try:
                from closures.quantum_mechanics.entanglement import compute_entanglement

                rho = [float(x.strip()) for x in rho_str.split(",")]
                bell = [float(x.strip()) for x in bell_str.split(",")] if bell_str.strip() else None
                result = compute_entanglement(rho, bell)
                regime = result["regime"]
                regime_color = {"Maximal": "🟢", "Strong": "🟢", "Weak": "🟡"}.get(regime, "⚪")

                rc1, rc2, rc3, rc4 = st.columns(4)
                with rc1:
                    st.metric("Concurrence", f"{result['concurrence']:.4f}")
                with rc2:
                    st.metric("S_vN (entropy)", f"{result['S_vN']:.4f}")
                with rc3:
                    st.metric("Bell parameter S", f"{result['bell_parameter']:.4f}")
                with rc4:
                    st.metric("Regime", f"{regime_color} {regime}")
                st.metric("Negativity", f"{result['negativity']:.4f}")

                # Entanglement measures radar
                fig = go.Figure()
                cats = ["Concurrence", "S_vN / ln(2)", "Bell/2√2", "Negativity"]
                vals_r = [
                    result["concurrence"],
                    result["S_vN"] / 0.6931 if result["S_vN"] > 0 else 0,
                    result["bell_parameter"] / 2.828 if result["bell_parameter"] > 0 else 0,
                    result["negativity"],
                ]
                vals_r = [min(v, 1.0) for v in vals_r]
                fig.add_trace(
                    go.Scatterpolar(
                        r=[*vals_r, vals_r[0]],
                        theta=[*cats, cats[0]],
                        fill="toself",
                        name="Entanglement",
                        fillcolor="rgba(111, 66, 193, 0.2)",
                        line={"color": "#6f42c1"},
                    )
                )
                fig.update_layout(
                    polar={"radialaxis": {"visible": True, "range": [0, 1]}},
                    height=320,
                    margin={"t": 30, "b": 20},
                    title="Entanglement Signature",
                )
                st.plotly_chart(fig, use_container_width=True)

                # Bell inequality check
                bell_val = result["bell_parameter"]
                if bell_val > 2:
                    st.success(
                        f"🔔 Bell inequality **violated** (S = {bell_val:.3f} > 2): quantum correlations confirmed"
                    )
                else:
                    st.info(f"Bell inequality satisfied (S = {bell_val:.3f} ≤ 2): classically explicable")
            except Exception as e:
                st.error(f"Computation error: {e}")

    # ── Tab 3: Tunneling ──
    with tab3:
        st.subheader("🚇 Quantum Tunneling (WKB)")
        st.markdown("""
        **WKB transmission**: $T \\approx \\exp\\left(-2 \\int_0^L \\kappa(x) \\, dx\\right)$
        where $\\kappa = \\sqrt{2m(V - E)} / \\hbar$

        A particle with energy E < V can tunnel through a potential barrier of height V and width L.
        """)
        preset_col3, _ = st.columns([1, 2])
        with preset_col3:
            tp = st.selectbox(
                "Presets",
                ["Custom", "⚛️ Alpha Decay", "🔬 STM Tip (thin barrier)", "🧱 Thick Barrier"],
                key="qm_tun_preset",
            )
        presets_tun = {
            "⚛️ Alpha Decay": (4.0, 30.0, 0.01),
            "🔬 STM Tip (thin barrier)": (4.0, 5.0, 0.5),
            "🧱 Thick Barrier": (1.0, 10.0, 5.0),
        }
        _ep, _vb, _bw = presets_tun.get(tp, (5.0, 10.0, 1.0))
        c1, c2, c3 = st.columns(3)
        with c1:
            e_p = st.number_input("E particle (eV)", 0.01, 100.0, _ep, 0.1, key="qm_ep")
        with c2:
            v_b = st.number_input("V barrier (eV)", 0.01, 200.0, _vb, 0.1, key="qm_vb")
        with c3:
            bw = st.number_input("Barrier width (nm)", 0.001, 50.0, _bw, 0.01, key="qm_bw")

        if st.button("Compute Tunneling", key="qm_tunnel", type="primary"):
            try:
                from closures.quantum_mechanics.tunneling import compute_tunneling

                result = compute_tunneling(e_p, v_b, bw)
                regime = result["regime"]
                regime_color = {"Transparent": "🟢", "Moderate": "🟡"}.get(regime, "🔴")

                rc1, rc2, rc3, rc4 = st.columns(4)
                with rc1:
                    st.metric("T (transmission)", f"{result['T_coeff']:.6e}")
                with rc2:
                    st.metric("κ barrier (1/nm)", f"{result['kappa_barrier']:.4f}")
                with rc3:
                    _t_ratio = result["T_ratio"]
                    _t_str = "INF_REC" if _t_ratio == "INF_REC" else f"{_t_ratio:.4e}"
                    st.metric("T/T_classical", _t_str)
                with rc4:
                    st.metric("Regime", f"{regime_color} {regime}")

                # Barrier potential diagram
                import math

                x_pts = 200
                x = [i * (bw * 3) / x_pts for i in range(x_pts)]
                v_profile = []
                psi_profile = []
                barrier_start = bw * 0.8
                barrier_end = barrier_start + bw
                for xi in x:
                    if barrier_start <= xi <= barrier_end:
                        v_profile.append(v_b)
                        psi_profile.append(e_p * math.exp(-result["kappa_barrier"] * (xi - barrier_start)))
                    else:
                        v_profile.append(0)
                        psi_profile.append(e_p)

                fig = go.Figure()
                fig.add_trace(
                    go.Scatter(
                        x=x,
                        y=v_profile,
                        mode="lines",
                        name="V(x)",
                        fill="tozeroy",
                        fillcolor="rgba(220,53,69,0.2)",
                        line={"color": "#dc3545", "width": 2},
                    )
                )
                fig.add_trace(
                    go.Scatter(
                        x=x,
                        y=psi_profile,
                        mode="lines",
                        name="|ψ|² (schematic)",
                        line={"color": "#007bff", "width": 2, "dash": "dash"},
                    )
                )
                fig.add_hline(y=e_p, line_dash="dot", line_color="green", annotation_text=f"E = {e_p:.1f} eV")
                fig.update_layout(
                    title="Barrier Potential & Tunneling",
                    xaxis_title="x (nm)",
                    yaxis_title="Energy (eV)",
                    height=300,
                    margin={"t": 40, "b": 20},
                )
                st.plotly_chart(fig, use_container_width=True)
            except Exception as e:
                st.error(f"Computation error: {e}")

    # ── Tab 4: Harmonic Oscillator ──
    with tab4:
        st.subheader("🎵 Quantum Harmonic Oscillator")
        st.markdown("""
        **Energy levels**: $E_n = \\hbar\\omega(n + \\frac{1}{2})$

        The quantum harmonic oscillator has equally-spaced energy levels. Compare predicted vs observed energy.
        """)
        c1, c2, c3 = st.columns(3)
        with c1:
            n_q = st.number_input("n (quantum number)", 0, 100, 0, key="qm_n")
        with c2:
            omega_f = st.number_input("ω (rad/s)", 1e10, 1e16, 1e13, key="qm_omega", format="%.2e")
        with c3:
            e_obs = st.number_input("E_obs (eV)", 0.0, 100.0, 0.05, 0.001, key="qm_eobs", format="%.4f")

        if st.button("Compute Oscillator", key="qm_osc", type="primary"):
            try:
                from closures.quantum_mechanics.harmonic_oscillator import compute_harmonic_oscillator

                result = compute_harmonic_oscillator(n_q, omega_f, e_obs)
                regime = result["regime"]
                regime_color = {"Pure": "🟢", "High": "🟢", "Mixed": "🟡"}.get(regime, "🔴")

                rc1, rc2, rc3, rc4 = st.columns(4)
                with rc1:
                    st.metric("E_predicted (eV)", f"{result['E_predicted']:.6f}")
                with rc2:
                    st.metric("E_observed (eV)", f"{e_obs:.6f}")
                with rc3:
                    st.metric("δE", f"{result['delta_E']:.6f}")
                with rc4:
                    st.metric("Regime", f"{regime_color} {regime}")

                # Energy level diagram
                import math

                hbar_eV = 6.582e-16  # eV·s
                e_levels = [(nn + 0.5) * hbar_eV * omega_f for nn in range(min(n_q + 5, 15))]
                fig = go.Figure()
                for nn, en in enumerate(e_levels):
                    color = "#dc3545" if nn == n_q else "#007bff"
                    width = 3 if nn == n_q else 1
                    fig.add_trace(
                        go.Scatter(
                            x=[0, 1],
                            y=[en, en],
                            mode="lines",
                            line={"color": color, "width": width},
                            name=f"n={nn}",
                            showlegend=(nn <= n_q + 2),
                        )
                    )
                    fig.add_annotation(x=1.1, y=en, text=f"n={nn}: {en:.4f} eV", showarrow=False, font={"size": 9})
                fig.update_layout(
                    title="Energy Level Diagram",
                    yaxis_title="E (eV)",
                    xaxis={"visible": False},
                    height=350,
                    margin={"t": 40, "b": 20, "r": 120},
                )
                st.plotly_chart(fig, use_container_width=True)
            except Exception as e:
                st.error(f"Computation error: {e}")

    # ── Tab 5: Spin Measurement ──
    with tab5:
        st.subheader("🧭 Spin Measurement (Stern-Gerlach)")
        st.markdown("""
        **Spin quantization**: $S_z = m_s \\hbar$ where $m_s = -s, -s+1, ..., +s$ ·
        **Larmor frequency**: $\\omega_L = g \\mu_B B / \\hbar$ ·
        **Zeeman splitting**: $\\Delta E = g \\mu_B B$
        """)
        preset_col5, _ = st.columns([1, 2])
        with preset_col5:
            spp = st.selectbox(
                "Presets",
                ["Custom", "⬆️ Spin-½ up (electron)", "🔄 Spin-1 (deuterium)", "⚛️ Spin-3/2"],
                key="qm_spin_preset",
            )
        presets_spin = {
            "⬆️ Spin-½ up (electron)": (0.5, 0.5, 1.0),
            "🔄 Spin-1 (deuterium)": (1.0, 1.0, 2.0),
            "⚛️ Spin-3/2": (1.5, 0.5, 1.0),
        }
        _st_val, _sz, _bf = presets_spin.get(spp, (0.5, 0.5, 1.0))
        c1, c2, c3 = st.columns(3)
        with c1:
            s_tot = st.number_input("S total", 0.0, 10.0, _st_val, 0.5, key="qm_stot")
        with c2:
            sz_obs = st.number_input("S_z observed", -10.0, 10.0, _sz, 0.5, key="qm_sz")
        with c3:
            b_field = st.number_input("B field (T)", 0.001, 50.0, _bf, 0.1, key="qm_bfield")

        if st.button("Compute Spin", key="qm_spin", type="primary"):
            try:
                from closures.quantum_mechanics.spin_measurement import compute_spin_measurement

                result = compute_spin_measurement(s_tot, sz_obs, b_field)
                regime = result["regime"]
                regime_color = {"Faithful": "🟢", "Perturbed": "🟡"}.get(regime, "🔴")

                rc1, rc2, rc3, rc4 = st.columns(4)
                with rc1:
                    st.metric("S_z predicted", f"{result['S_z_predicted']:.4f}")
                with rc2:
                    st.metric("Spin fidelity", f"{result['spin_fidelity']:.4f}")
                with rc3:
                    st.metric("Larmor (GHz)", f"{result['larmor_freq'] / 1e9:.4f}")
                with rc4:
                    st.metric("Regime", f"{regime_color} {regime}")

                st.metric("Zeeman splitting (eV)", f"{result['zeeman_split']:.6e}")

                # Spin state visualization
                allowed_mz = [s_tot - i for i in range(int(2 * s_tot) + 1)]
                fig = go.Figure()
                for mz in allowed_mz:
                    is_obs = abs(mz - sz_obs) < 0.01
                    fig.add_trace(
                        go.Scatter(
                            x=[0, 1],
                            y=[mz, mz],
                            mode="lines",
                            line={"color": "#dc3545" if is_obs else "#007bff", "width": 3 if is_obs else 1.5},
                            name=f"m_s = {mz:+.1f}" + (" ← observed" if is_obs else ""),
                        )
                    )
                fig.update_layout(
                    title=f"Spin-{s_tot} Projections (2s+1 = {int(2 * s_tot + 1)} states)",
                    yaxis_title="m_s",
                    xaxis={"visible": False},
                    height=280,
                    margin={"t": 40, "b": 20},
                )
                st.plotly_chart(fig, use_container_width=True)
            except Exception as e:
                st.error(f"Computation error: {e}")

    # ── Tab 6: Uncertainty Principle ──
    with tab6:
        st.subheader("📏 Heisenberg Uncertainty Principle")
        st.markdown("""
        **Heisenberg** (1927): $\\Delta x \\cdot \\Delta p \\geq \\frac{\\hbar}{2}$

        The product of position and momentum uncertainties has a fundamental quantum lower bound.
        The ratio to ℏ/2 measures how close the state is to a minimum-uncertainty wavepacket.
        """)
        preset_col6, _ = st.columns([1, 2])
        with preset_col6:
            up = st.selectbox(
                "Presets",
                ["Custom", "📏 Minimum Uncertainty", "🌊 Spread Wavepacket", "⚛️ Atomic Scale"],
                key="qm_unc_preset",
            )
        presets_unc = {
            "📏 Minimum Uncertainty": (0.1, 5.27e-25),
            "🌊 Spread Wavepacket": (10.0, 1e-24),
            "⚛️ Atomic Scale": (0.053, 1.99e-24),
        }
        _dx, _dp = presets_unc.get(up, (1.0, 5.27e-25))
        c1, c2 = st.columns(2)
        with c1:
            dx = st.number_input("Δx (nm)", 0.001, 10000.0, _dx, 0.01, key="qm_dx")
        with c2:
            dp = st.number_input("Δp (kg·m/s)", 1e-30, 1e-18, _dp, 1e-26, key="qm_dp", format="%.4e")

        if st.button("Check Uncertainty", key="qm_unc", type="primary"):
            try:
                from closures.quantum_mechanics.uncertainty_principle import compute_uncertainty

                result = compute_uncertainty(dx * 1e-9, dp)  # Convert nm → meters
                regime = result["regime"]
                regime_color = {"Minimum": "🟢", "Moderate": "🟡", "Dispersed": "🟡"}.get(regime, "🔴")

                rc1, rc2, rc3, rc4 = st.columns(4)
                with rc1:
                    st.metric("ΔxΔp", f"{result['heisenberg_product']:.4e}")
                with rc2:
                    st.metric("Ratio to ℏ/2", f"{result['heisenberg_ratio']:.4f}")
                with rc3:
                    st.metric("ℏ/2", f"{result['min_uncertainty']:.4e}")
                with rc4:
                    st.metric("Regime", f"{regime_color} {regime}")

                # Heisenberg bound visualization
                ratio = result["heisenberg_ratio"]
                fig = go.Figure(
                    go.Indicator(
                        mode="gauge+number",
                        value=ratio,
                        title={"text": "ΔxΔp / (ℏ/2)"},
                        gauge={
                            "axis": {"range": [0, max(10, ratio * 1.5)]},
                            "bar": {"color": "#007bff"},
                            "steps": [
                                {"range": [0, 1], "color": "#f8d7da"},
                                {"range": [1, 2], "color": "#d4edda"},
                                {"range": [2, 5], "color": "#fff3cd"},
                                {"range": [5, max(10, ratio * 1.5)], "color": "#e2e3e5"},
                            ],
                            "threshold": {"line": {"color": "red", "width": 3}, "value": 1.0},
                        },
                    )
                )
                fig.update_layout(height=250, margin={"t": 40, "b": 10})
                st.plotly_chart(fig, use_container_width=True)
                if ratio >= 1:
                    st.success("✅ Heisenberg bound satisfied (ΔxΔp ≥ ℏ/2)")
                else:
                    st.error("⚠️ Heisenberg bound **violated** — check input units")
            except Exception as e:
                st.error(f"Computation error: {e}")


def render_finance_page() -> None:
    """Render interactive Finance domain page with professional visualizations."""
    if st is None:
        return
    if go is None or pd is None or np is None:
        st.error(
            "Dashboard dependencies (numpy, pandas, plotly) could not be loaded. Install with: `pip install umcp[viz]`"
        )
        return

    _ensure_closures_path()

    st.title("💰 Finance Domain")
    st.caption("FINANCE.INTSTACK.v1 — Business financial continuity validation via UMCP embedding")

    with st.expander("📖 Domain Overview", expanded=False):
        st.markdown("""
        The **Finance** domain maps raw financial records into UMCP's [0, 1]⁴ coordinate space,
        enabling contract-based validation of business health.

        **Embedding coordinates** (each clipped to [ε, 1−ε]):

        | Coordinate | Formula | Measures |
        |-----------|---------|----------|
        | c₁ (Revenue) | min(revenue / target, 1.0) | Revenue performance vs goal |
        | c₂ (Expense) | min(budget / expenses, 1.0) | Expense control efficiency |
        | c₃ (Margin) | (revenue − COGS) / revenue | Gross margin profitability |
        | c₄ (Cashflow) | min(cashflow / target, 1.0) | Cash flow health |

        **Default weights**: w = [0.30, 0.25, 0.25, 0.20]

        Once embedded, the standard UMCP invariants (ω, F, κ, IC) are computed and the
        regime is classified as **STABLE** / **WATCH** / **COLLAPSE**.
        """)

    st.divider()

    # ── Preset selection ──
    preset_col, _ = st.columns([1, 2])
    with preset_col:
        fp = st.selectbox(
            "Scenario Presets",
            [
                "Custom",
                "🏢 Healthy Business",
                "📈 Growth Phase",
                "📉 Cash Crunch",
                "⚠️ Margin Squeeze",
                "🔴 Distressed",
            ],
            key="fin_preset",
            help="Pre-configured financial scenarios",
        )

    presets_fin: dict[str, dict[str, float | str]] = {
        "🏢 Healthy Business": {
            "month": "2026-01",
            "rev": 500000,
            "exp": 380000,
            "cogs": 200000,
            "cf": 90000,
            "rev_t": 500000,
            "exp_t": 450000,
            "cf_t": 75000,
        },
        "📈 Growth Phase": {
            "month": "2026-03",
            "rev": 650000,
            "exp": 500000,
            "cogs": 260000,
            "cf": 120000,
            "rev_t": 500000,
            "exp_t": 450000,
            "cf_t": 75000,
        },
        "📉 Cash Crunch": {
            "month": "2026-06",
            "rev": 480000,
            "exp": 460000,
            "cogs": 200000,
            "cf": 15000,
            "rev_t": 500000,
            "exp_t": 450000,
            "cf_t": 75000,
        },
        "⚠️ Margin Squeeze": {
            "month": "2026-09",
            "rev": 500000,
            "exp": 420000,
            "cogs": 400000,
            "cf": 60000,
            "rev_t": 500000,
            "exp_t": 450000,
            "cf_t": 75000,
        },
        "🔴 Distressed": {
            "month": "2026-12",
            "rev": 200000,
            "exp": 550000,
            "cogs": 180000,
            "cf": -50000,
            "rev_t": 500000,
            "exp_t": 450000,
            "cf_t": 75000,
        },
    }

    p = presets_fin.get(
        fp,
        {
            "month": "2026-01",
            "rev": 500000,
            "exp": 400000,
            "cogs": 200000,
            "cf": 80000,
            "rev_t": 500000,
            "exp_t": 450000,
            "cf_t": 75000,
        },
    )

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**📈 Financial Record**")
        month = st.text_input(
            "Month (YYYY-MM)", str(p["month"]), key="fin_month", help="Reporting period in YYYY-MM format"
        )
        revenue = st.number_input(
            "Revenue ($)", 0.0, 1e9, float(p["rev"]), 1000.0, key="fin_rev", help="Total revenue for the period"
        )
        expenses = st.number_input(
            "Expenses ($)", 0.0, 1e9, float(p["exp"]), 1000.0, key="fin_exp", help="Total operating expenses"
        )
        cogs = st.number_input("COGS ($)", 0.0, 1e9, float(p["cogs"]), 1000.0, key="fin_cogs")
        cashflow = st.number_input("Cashflow ($)", -1e9, 1e9, float(p["cf"]), 1000.0, key="fin_cf")

    with col2:
        st.markdown("**🎯 Targets**")
        rev_target = st.number_input("Revenue Target ($)", 0.0, 1e9, float(p["rev_t"]), 1000.0, key="fin_rev_t")
        exp_budget = st.number_input("Expense Budget ($)", 0.0, 1e9, float(p["exp_t"]), 1000.0, key="fin_exp_t")
        cf_target = st.number_input("Cashflow Target ($)", 0.0, 1e9, float(p["cf_t"]), 1000.0, key="fin_cf_t")

    if st.button("💹 Embed & Analyze", key="fin_embed", type="primary"):
        try:
            from closures.finance.finance_embedding import FinanceRecord, FinanceTargets, embed_finance

            record = FinanceRecord(month=month, revenue=revenue, expenses=expenses, cogs=cogs, cashflow=cashflow)
            targets = FinanceTargets(revenue_target=rev_target, expense_budget=exp_budget, cashflow_target=cf_target)
            embedded = embed_finance(record, targets)

            st.divider()
            st.subheader("📐 UMCP Embedding Coordinates")
            coord_names = ["c₁ Revenue", "c₂ Expense", "c₃ Margin", "c₄ Cashflow"]
            c_cols = st.columns(4)
            for i, (name, val) in enumerate(zip(coord_names, embedded.c, strict=False)):
                with c_cols[i]:
                    flag = "⚠️ OOR" if embedded.oor_flags[i] else "✅ In-range"
                    st.metric(name, f"{val:.4f}", delta=flag)

            # Compute UMCP invariants from coordinates using kernel_optimized
            from umcp.kernel_optimized import compute_kernel_outputs

            c_arr = np.array(embedded.c, dtype=float)
            w_arr = np.array([0.30, 0.25, 0.25, 0.20], dtype=float)
            kernel = compute_kernel_outputs(c_arr, w_arr, epsilon=EPSILON)
            f_val = kernel["F"]
            omega = kernel["omega"]
            kappa = kernel["kappa"]
            ic = kernel["IC"]
            regime = kernel["regime"]

            st.divider()
            st.subheader("🧮 UMCP Invariants")
            inv_cols = st.columns(5)
            with inv_cols[0]:
                st.metric("ω (drift)", f"{omega:.4f}")
            with inv_cols[1]:
                st.metric("F = 1−ω", f"{f_val:.4f}")
            with inv_cols[2]:
                st.metric("κ", f"{kappa:.4f}")
            with inv_cols[3]:
                st.metric("IC = exp(κ)", f"{ic:.4f}")
            with inv_cols[4]:
                color = "🟢" if regime == "STABLE" else "🟡" if regime == "WATCH" else "🔴"
                st.metric("Regime", f"{color} {regime}")

            # Identity checks
            import math

            st.divider()
            ic_le_f = ic <= f_val + 1e-9
            f_plus_omega = f_val + omega
            st.subheader("📋 Tier-1 Identity Verification")
            id_cols = st.columns(3)
            with id_cols[0]:
                st.markdown(f"**F + ω = {f_plus_omega:.6f}** {'✅' if abs(f_plus_omega - 1.0) < 1e-6 else '⚠️'}")
                st.caption("Must equal 1.0 (budget identity)")
            with id_cols[1]:
                st.markdown(f"**IC ≤ F** → {ic:.4f} ≤ {f_val:.4f} {'✅' if ic_le_f else '❌'}")
                st.caption("Integrity bound (IC ≤ F; the classical inequality is a degenerate limit)")
            with id_cols[2]:
                ic_target = math.exp(kappa)
                st.markdown(
                    f"**IC ≈ exp(κ)** → {ic:.6f} ≈ {ic_target:.6f} {'✅' if abs(ic - ic_target) < 1e-9 else '⚠️'}"
                )
                st.caption("Exponential consistency check")

            st.divider()

            # Two-column visualization
            viz_left, viz_right = st.columns(2)

            with viz_left:
                # Radar chart
                fig = go.Figure()
                fig.add_trace(
                    go.Scatterpolar(
                        r=[*list(embedded.c), embedded.c[0]],
                        theta=[*coord_names, coord_names[0]],
                        fill="toself",
                        name="Financial Health",
                        fillcolor="rgba(0, 123, 255, 0.15)",
                        line={"color": "#007bff", "width": 2},
                    )
                )
                # Add target ring at 1.0
                fig.add_trace(
                    go.Scatterpolar(
                        r=[1.0] * 5,
                        theta=[*coord_names, coord_names[0]],
                        mode="lines",
                        name="Target (1.0)",
                        line={"color": "#28a745", "width": 1, "dash": "dash"},
                    )
                )
                fig.update_layout(
                    polar={"radialaxis": {"visible": True, "range": [0, 1.1]}},
                    height=380,
                    margin={"t": 40, "b": 30},
                    title="Financial Health Radar",
                    showlegend=True,
                    legend={"x": 0.7, "y": 0.05},
                )
                st.plotly_chart(fig, use_container_width=True)

            with viz_right:
                # Bar chart comparing actuals vs targets
                categories = ["Revenue", "Expenses", "Cashflow"]
                actuals = [revenue, expenses, cashflow]
                targets_vals = [rev_target, exp_budget, cf_target]
                fig = go.Figure()
                fig.add_trace(
                    go.Bar(x=categories, y=actuals, name="Actual", marker_color=["#007bff", "#dc3545", "#28a745"])
                )
                fig.add_trace(
                    go.Bar(
                        x=categories,
                        y=targets_vals,
                        name="Target",
                        marker_color=["#007bff55", "#dc354555", "#28a74555"],
                    )
                )
                fig.update_layout(
                    title="Actual vs Target",
                    barmode="group",
                    yaxis_title="$ (USD)",
                    height=380,
                    margin={"t": 40, "b": 20},
                )
                st.plotly_chart(fig, use_container_width=True)

            # Profitability breakdown
            gross_profit = revenue - cogs
            operating_income = revenue - expenses
            margin_pct = (gross_profit / revenue * 100) if revenue > 0 else 0

            st.subheader("📊 Financial Summary")
            sum_cols = st.columns(4)
            with sum_cols[0]:
                st.metric("Gross Profit", f"${gross_profit:,.0f}", delta=f"{margin_pct:.1f}% margin")
            with sum_cols[1]:
                st.metric(
                    "Operating Income", f"${operating_income:,.0f}", delta=f"{'✅' if operating_income > 0 else '🔴'}"
                )
            with sum_cols[2]:
                rev_ratio = (revenue / rev_target * 100) if rev_target > 0 else 0
                st.metric(
                    "Revenue vs Target",
                    f"{rev_ratio:.0f}%",
                    delta=f"{'▲' if rev_ratio >= 100 else '▼'} {abs(rev_ratio - 100):.0f}%",
                )
            with sum_cols[3]:
                cf_ratio = (cashflow / cf_target * 100) if cf_target > 0 else 0
                st.metric(
                    "Cashflow vs Target",
                    f"{cf_ratio:.0f}%",
                    delta=f"{'▲' if cf_ratio >= 100 else '▼'} {abs(cf_ratio - 100):.0f}%",
                )

            # Waterfall chart of P&L
            fig_wf = go.Figure(
                go.Waterfall(
                    name="P&L Flow",
                    orientation="v",
                    measure=["absolute", "relative", "relative", "relative", "total"],
                    x=["Revenue", "COGS", "OpEx", "Cashflow Adj.", "Net Position"],
                    y=[
                        revenue,
                        -cogs,
                        -(expenses - cogs),
                        cashflow - operating_income,
                        operating_income + (cashflow - operating_income),
                    ],
                    connector={"line": {"color": "rgb(63, 63, 63)"}},
                    increasing={"marker": {"color": "#28a745"}},
                    decreasing={"marker": {"color": "#dc3545"}},
                    totals={"marker": {"color": "#007bff"}},
                )
            )
            fig_wf.update_layout(title="P&L Waterfall", yaxis_title="$ (USD)", height=350, margin={"t": 40, "b": 20})
            st.plotly_chart(fig_wf, use_container_width=True)

        except Exception as e:
            st.error(f"Computation error: {e}")


def render_rcft_page() -> None:
    """Render interactive RCFT domain page with 7 closures and professional visualizations."""
    if st is None:
        return
    if go is None or pd is None or np is None:
        st.error(
            "Dashboard dependencies (plotly, pandas, numpy) are required for this page. Install with: `pip install plotly pandas numpy`"
        )
        return

    _ensure_closures_path()

    st.title("🌀 RCFT Domain")
    st.caption(
        "RCFT.INTSTACK.v1 — Recursive Collapse Field Theory: fractal dimension, recursive fields, attractor basins, resonance"
    )

    with st.expander("📖 Domain Overview", expanded=False):
        st.markdown("""
        **Recursive Collapse Field Theory** (RCFT) extends UMCP into dynamical systems territory.
        It analyzes time-series of Tier-1 invariants (ω, S, C, F) to detect:

        - **Fractal structure** in collapse trajectories (box-counting dimension D_f)
        - **Recursive field strength** Ψ_r = Σ αⁿ · Ψₙ (memory-weighted invariant accumulation)
        - **Attractor topology** in (ω, S, C) phase space (monostable vs multistable)
        - **Resonance patterns** via FFT (dominant wavelength λ, phase coherence Θ)
        - **Information geometry** on the Bernoulli manifold (Fisher distance, geodesics)
        - **Universality class** via partition function Z(β) (central charge, critical exponents)
        - **Collapse grammar** as Markov chain (transfer matrix, spectral gap, entropy rate)

        | Closure | Output | Regime Classification |
        |---------|--------|----------------------|
        | Fractal Dimension | D_f ∈ [1, 3] | Smooth < 1.2 · Wrinkled 1.2–1.8 · Turbulent ≥ 1.8 |
        | Recursive Field | Ψ_r ≥ 0 | Dormant < 0.1 · Active 0.1–1.0 · Resonant ≥ 1.0 |
        | Attractor Basin | n_attractors ≥ 1 | Monostable · Bistable · Multistable |
        | Resonance Pattern | λ, Θ | Standing · Traveling · Mixed |
        | Information Geometry | d_F, η | Geodesic · SubOptimal · Divergent |
        | Universality Class | c_eff, ν, γ | Ising · GCD · MeanField |
        | Collapse Grammar | h, Δ | FROZEN · ORDERED · COMPLEX · CHAOTIC |
        """)

    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(
        [
            "📐 Fractal Dimension",
            "🌊 Recursive Field",
            "🎯 Attractor Basin",
            "🔊 Resonance Pattern",
            "📐 Information Geometry",
            "🌡️ Universality Class",
            "🔤 Collapse Grammar",
        ]
    )

    # ── Tab 1: Fractal Dimension ──
    with tab1:
        st.subheader("📐 Fractal Dimension (Box-Counting)")
        st.markdown("""
        **Box-counting dimension**: $D_f = \\lim_{\\varepsilon \\to 0} \\frac{\\log N(\\varepsilon)}{\\log(1/\\varepsilon)}$

        The fractal dimension D_f quantifies the complexity of collapse trajectories in invariant space.
        A smooth trajectory has D_f ≈ 1 (line); a turbulent one approaches D_f ≈ 2 (space-filling).
        """)

        preset_col, _ = st.columns([1, 2])
        with preset_col:
            fp1 = st.selectbox(
                "Presets",
                [
                    "Custom",
                    "🟢 Smooth Orbit (low noise)",
                    "🟡 Wrinkled Spiral (moderate)",
                    "🔴 Turbulent Cloud (high noise)",
                    "⭕ Clean Circle",
                ],
                key="rcft_frac_preset",
                help="Trajectory preset with varying complexity",
            )

        presets_frac = {
            "🟢 Smooth Orbit (low noise)": (200, 0.05),
            "🟡 Wrinkled Spiral (moderate)": (300, 0.4),
            "🔴 Turbulent Cloud (high noise)": (400, 0.9),
            "⭕ Clean Circle": (500, 0.0),
        }
        _npts, _noise = presets_frac.get(fp1, (200, 0.3))

        c1, c2 = st.columns(2)
        with c1:
            n_pts = st.slider(
                "Trajectory points", 50, 500, _npts, key="rcft_npts", help="Number of points in the trajectory"
            )
        with c2:
            noise = st.slider(
                "Noise level", 0.0, 1.0, _noise, 0.05, key="rcft_noise", help="Random perturbation amplitude (0=clean)"
            )

        if st.button("Compute Fractal Dimension", key="rcft_frac", type="primary"):
            try:
                from closures.rcft.fractal_dimension import compute_fractal_dimension

                t = np.linspace(0, 10, n_pts)
                trajectory = np.column_stack(
                    [np.sin(t) + noise * np.random.randn(n_pts), np.cos(t) + noise * np.random.randn(n_pts)]
                )
                result = compute_fractal_dimension(trajectory)

                st.divider()
                rc1, rc2, rc3, rc4 = st.columns(4)
                with rc1:
                    st.metric("D_fractal", f"{result['D_fractal']:.4f}")
                with rc2:
                    st.metric("R²", f"{result.get('r_squared', 0):.4f}")
                with rc3:
                    regime = result["regime"]
                    color = "🟢" if regime == "Smooth" else "🟡" if regime == "Wrinkled" else "🔴"
                    st.metric("Regime", f"{color} {regime}")
                with rc4:
                    st.metric("log slope", f"{result.get('log_slope', result['D_fractal']):.4f}")

                # Two-column visualization
                viz_l, viz_r = st.columns(2)
                with viz_l:
                    # Trajectory scatter plot
                    fig = go.Figure()
                    fig.add_trace(
                        go.Scatter(
                            x=trajectory[:, 0],
                            y=trajectory[:, 1],
                            mode="markers",
                            marker={
                                "size": 3,
                                "color": list(range(n_pts)),
                                "colorscale": "Viridis",
                                "colorbar": {"title": "t"},
                            },
                            name="Trajectory",
                        )
                    )
                    fig.update_layout(
                        title=f"Collapse Trajectory (D_f = {result['D_fractal']:.3f})",
                        xaxis_title="sin(t) + noise",
                        yaxis_title="cos(t) + noise",
                        height=350,
                        margin={"t": 40, "b": 20},
                    )
                    st.plotly_chart(fig, use_container_width=True)

                with viz_r:
                    # Log-log box counting plot
                    eps_used = result.get("eps_used", None)
                    box_counts = result.get("box_counts", None)
                    if eps_used is not None and box_counts is not None:
                        log_eps = np.log(1.0 / np.array(eps_used))
                        log_n = np.log(np.array(box_counts).astype(float) + 1)
                        fig2 = go.Figure()
                        fig2.add_trace(
                            go.Scatter(
                                x=log_eps.tolist(),
                                y=log_n.tolist(),
                                mode="markers+lines",
                                name="Box counts",
                                marker={"color": "#007bff", "size": 6},
                            )
                        )
                        fig2.update_layout(
                            title="Box-Counting (log-log)",
                            xaxis_title="log(1/ε)",
                            yaxis_title="log N(ε)",
                            height=350,
                            margin={"t": 40, "b": 20},
                        )
                        st.plotly_chart(fig2, use_container_width=True)
                    else:
                        # Dimension gauge
                        fig2 = go.Figure(
                            go.Indicator(
                                mode="gauge+number",
                                value=result["D_fractal"],
                                title={"text": "Fractal Dimension"},
                                gauge={
                                    "axis": {"range": [1, 3]},
                                    "bar": {"color": "#007bff"},
                                    "steps": [
                                        {"range": [1, 1.2], "color": "#d4edda"},
                                        {"range": [1.2, 1.8], "color": "#fff3cd"},
                                        {"range": [1.8, 3], "color": "#f8d7da"},
                                    ],
                                },
                            )
                        )
                        fig2.update_layout(height=300, margin={"t": 40, "b": 10})
                        st.plotly_chart(fig2, use_container_width=True)
            except Exception as e:
                st.error(f"Computation error: {e}")

    # ── Tab 2: Recursive Field ──
    with tab2:
        st.subheader("🌊 Recursive Field Strength (Ψ_r)")
        st.markdown("""
        **Recursive field**: $\\Psi_r = \\sum_{n=0}^{N} \\alpha^n \\cdot \\Psi_n$
        where $\\Psi_n = \\sqrt{S_n^2 + C_n^2} \\cdot (1 - F_n)$

        The field accumulates history with exponential decay α, measuring how strongly
        past invariant states influence the current collapse trajectory.
        """)

        preset_col2, _ = st.columns([1, 2])
        with preset_col2:
            fp2 = st.selectbox(
                "Presets",
                [
                    "Custom",
                    "💤 Dormant (stable system)",
                    "⚡ Active (moderate dynamics)",
                    "🔥 Resonant (high memory)",
                ],
                key="rcft_field_preset",
            )

        presets_field = {
            "💤 Dormant (stable system)": (30, 0.3, (0.1, 0.2), (0.05, 0.1), (0.85, 0.95)),
            "⚡ Active (moderate dynamics)": (80, 0.8, (0.3, 0.7), (0.2, 0.5), (0.3, 0.7)),
            "🔥 Resonant (high memory)": (150, 0.95, (0.5, 0.9), (0.3, 0.8), (0.1, 0.4)),
        }
        _ns, _alpha, _s_range, _c_range, _f_range = presets_field.get(
            fp2, (50, 0.8, (0.2, 0.8), (0.1, 0.5), (0.3, 0.9))
        )

        c1, c2 = st.columns(2)
        with c1:
            n_series = st.slider("Series length", 10, 200, _ns, key="rcft_nseries")
        with c2:
            alpha_param = st.slider("α (decay)", 0.1, 0.99, _alpha, 0.01, key="rcft_alpha")

        if st.button("Compute Recursive Field", key="rcft_field", type="primary"):
            try:
                from closures.rcft.recursive_field import compute_recursive_field

                S_arr = np.random.uniform(_s_range[0], _s_range[1], n_series)
                C_arr = np.random.uniform(_c_range[0], _c_range[1], n_series)
                F_arr = np.random.uniform(_f_range[0], _f_range[1], n_series)
                result = compute_recursive_field(S_arr, C_arr, F_arr, alpha=alpha_param)

                st.divider()
                rc1, rc2, rc3, rc4 = st.columns(4)
                with rc1:
                    st.metric("Ψ_recursive", f"{result['Psi_recursive']:.4f}")
                with rc2:
                    st.metric("Iterations", str(result.get("n_iterations", "N/A")))
                with rc3:
                    converged = result.get("convergence_achieved", False)
                    st.metric("Converged", "✅ Yes" if converged else "⏳ No")
                with rc4:
                    regime = result["regime"]
                    color = "💤" if regime == "Dormant" else "⚡" if regime == "Active" else "🔥"
                    st.metric("Regime", f"{color} {regime}")

                viz_l, viz_r = st.columns(2)
                with viz_l:
                    # Weighted contributions over time
                    weighted = result.get("weighted_contributions", None)
                    if weighted is not None:
                        fig = go.Figure()
                        fig.add_trace(
                            go.Scatter(
                                y=weighted.tolist(),
                                mode="lines+markers",
                                marker={"size": 3, "color": "#007bff"},
                                line={"color": "#007bff", "width": 1},
                                name="αⁿ · Ψₙ",
                            )
                        )
                        fig.add_trace(
                            go.Scatter(
                                y=result.get("decay_factors", np.array([])).tolist(),
                                mode="lines",
                                line={"color": "#dc3545", "width": 1, "dash": "dash"},
                                name="αⁿ envelope",
                            )
                        )
                        fig.update_layout(
                            title="Weighted Contributions",
                            xaxis_title="n (iteration)",
                            yaxis_title="αⁿ · Ψₙ",
                            height=350,
                            margin={"t": 40, "b": 20},
                        )
                        st.plotly_chart(fig, use_container_width=True)

                with viz_r:
                    # Input invariant time series
                    fig2 = go.Figure()
                    fig2.add_trace(
                        go.Scatter(y=S_arr.tolist(), name="S (entropy)", line={"color": "#007bff", "width": 1})
                    )
                    fig2.add_trace(
                        go.Scatter(y=C_arr.tolist(), name="C (curvature)", line={"color": "#28a745", "width": 1})
                    )
                    fig2.add_trace(
                        go.Scatter(y=F_arr.tolist(), name="F (fidelity)", line={"color": "#dc3545", "width": 1})
                    )
                    fig2.update_layout(
                        title="Input Invariant Series",
                        xaxis_title="Time step",
                        yaxis_title="Value",
                        height=350,
                        margin={"t": 40, "b": 20},
                    )
                    st.plotly_chart(fig2, use_container_width=True)

                # Components summary
                components = result.get("components", {})
                if components:
                    st.markdown("**📊 Field Components**")
                    comp_cols = st.columns(5)
                    comp_items = list(components.items())[:5]
                    for i, (k, v) in enumerate(comp_items):
                        with comp_cols[i]:
                            label = k.replace("_", " ").title()
                            st.metric(label, f"{v:.4f}" if isinstance(v, float) else str(v))

            except Exception as e:
                st.error(f"Computation error: {e}")

    # ── Tab 3: Attractor Basin ──
    with tab3:
        st.subheader("🎯 Attractor Basin Topology")
        st.markdown("""
        Analyzes the phase-space structure of collapse trajectories in (ω, S, C) coordinates.
        Classifies the system as **Monostable** (single attractor), **Bistable** (two),
        or **Multistable** (three+). The dominant attractor indicates the most probable
        collapse endpoint.
        """)

        preset_col3, _ = st.columns([1, 2])
        with preset_col3:
            fp3 = st.selectbox(
                "Presets",
                [
                    "Custom",
                    "🎯 Monostable (tight cluster)",
                    "⚖️ Bistable (two basins)",
                    "🌀 Multistable (chaotic)",
                ],
                key="rcft_basin_preset",
            )

        presets_basin = {
            "🎯 Monostable (tight cluster)": (100, "monostable"),
            "⚖️ Bistable (two basins)": (200, "bistable"),
            "🌀 Multistable (chaotic)": (400, "multistable"),
        }
        _nb, _mode_basin = presets_basin.get(fp3, (100, "bistable"))

        n_basin = st.slider("Series length", 20, 500, _nb, key="rcft_nbasin")

        if st.button("Compute Attractor Basin", key="rcft_basin", type="primary"):
            try:
                from closures.rcft.attractor_basin import compute_attractor_basin

                # Generate time-correlated trajectories so the pathway connects
                t_basin = np.linspace(0, 10, n_basin)
                if _mode_basin == "monostable":
                    # Exponential convergence to a single fixed point
                    omega_arr = 0.05 + 0.25 * np.exp(-t_basin / 2) + 0.01 * np.random.randn(n_basin)
                    S_arr = 0.10 + 0.15 * np.exp(-t_basin / 2) + 0.01 * np.random.randn(n_basin)
                    C_arr = 0.03 + 0.10 * np.exp(-t_basin / 2) + 0.005 * np.random.randn(n_basin)
                elif _mode_basin == "bistable":
                    # Oscillation between two attractor basins
                    omega_arr = 0.15 + 0.12 * np.sin(2 * np.pi * t_basin / 5) + 0.02 * np.random.randn(n_basin)
                    S_arr = 0.20 + 0.10 * np.sin(2 * np.pi * t_basin / 5 + np.pi / 2) + 0.02 * np.random.randn(n_basin)
                    C_arr = 0.10 + 0.08 * np.sin(2 * np.pi * t_basin / 5) + 0.01 * np.random.randn(n_basin)
                else:
                    # Random walk — chaotic / multistable
                    omega_arr = np.clip(0.20 + 0.05 * np.random.randn(n_basin).cumsum() / 10, 0, 0.5)
                    S_arr = np.clip(0.30 + 0.08 * np.random.randn(n_basin).cumsum() / 10, 0, 1)
                    C_arr = np.clip(0.15 + 0.05 * np.random.randn(n_basin).cumsum() / 10, 0, 0.5)
                omega_arr = np.clip(omega_arr, 0, 1)
                S_arr = np.clip(S_arr, 0, 1)
                C_arr = np.clip(C_arr, 0, 1)
                result = compute_attractor_basin(omega_arr, S_arr, C_arr)

                st.divider()
                rc1, rc2, rc3, rc4 = st.columns(4)
                n_att = result.get("n_attractors_found", 0)
                with rc1:
                    st.metric("Attractors Found", str(n_att))
                with rc2:
                    st.metric("Dominant", str(result.get("dominant_attractor", "N/A")))
                with rc3:
                    max_strength = result.get("max_basin_strength", 0)
                    st.metric(
                        "Max Strength", f"{max_strength:.4f}" if isinstance(max_strength, float) else str(max_strength)
                    )
                with rc4:
                    regime = result.get("regime", "Unknown")
                    color = "🎯" if regime == "Monostable" else "⚖️" if regime == "Bistable" else "🌀"
                    st.metric("Regime", f"{color} {regime}")

                viz_l, viz_r = st.columns(2)
                with viz_l:
                    # 3D trajectory with connected pathway and basin coloring
                    traj_class = result.get("trajectory_classification", [])
                    fig = go.Figure()
                    # Connected trajectory line (the pathway)
                    fig.add_trace(
                        go.Scatter3d(
                            x=omega_arr.tolist(),
                            y=S_arr.tolist(),
                            z=C_arr.tolist(),
                            mode="lines",
                            line={"color": "rgba(0,123,255,0.3)", "width": 2},
                            name="Trajectory path",
                            showlegend=True,
                        )
                    )
                    # Points colored by basin assignment
                    if len(traj_class) == n_basin:
                        fig.add_trace(
                            go.Scatter3d(
                                x=omega_arr.tolist(),
                                y=S_arr.tolist(),
                                z=C_arr.tolist(),
                                mode="markers",
                                marker={
                                    "size": 3,
                                    "color": list(traj_class),
                                    "colorscale": "Set1",
                                    "colorbar": {"title": "Basin"},
                                },
                                name="Points (basin)",
                            )
                        )
                    else:
                        fig.add_trace(
                            go.Scatter3d(
                                x=omega_arr.tolist(),
                                y=S_arr.tolist(),
                                z=C_arr.tolist(),
                                mode="markers",
                                marker={"size": 3, "color": "#007bff"},
                                name="Points",
                            )
                        )
                    # Mark start and end of trajectory
                    fig.add_trace(
                        go.Scatter3d(
                            x=[omega_arr[0]],
                            y=[S_arr[0]],
                            z=[C_arr[0]],
                            mode="markers",
                            marker={"size": 8, "color": "#28a745", "symbol": "circle"},
                            name="Start",
                        )
                    )
                    fig.add_trace(
                        go.Scatter3d(
                            x=[omega_arr[-1]],
                            y=[S_arr[-1]],
                            z=[C_arr[-1]],
                            mode="markers",
                            marker={"size": 8, "color": "#ffc107", "symbol": "square"},
                            name="End",
                        )
                    )

                    # Mark attractor locations
                    locs = result.get("attractor_locations", [])
                    for idx, loc in enumerate(locs):
                        if len(loc) >= 3:
                            fig.add_trace(
                                go.Scatter3d(
                                    x=[loc[0]],
                                    y=[loc[1]],
                                    z=[loc[2]],
                                    mode="markers",
                                    marker={"size": 10, "color": "red", "symbol": "diamond"},
                                    name=f"Attractor {idx}",
                                )
                            )

                    fig.update_layout(
                        title=f"Phase Space ({regime})",
                        scene={"xaxis_title": "ω", "yaxis_title": "S", "zaxis_title": "C"},
                        height=400,
                        margin={"t": 40, "b": 10},
                    )
                    st.plotly_chart(fig, use_container_width=True)

                with viz_r:
                    # Basin strength bar chart
                    strengths = result.get("basin_strengths", [])
                    volumes = result.get("basin_volumes", [])
                    if strengths:
                        basin_labels = [f"Basin {i}" for i in range(len(strengths))]
                        fig2 = go.Figure()
                        fig2.add_trace(
                            go.Bar(
                                x=basin_labels,
                                y=strengths,
                                name="Strength",
                                marker_color=["#007bff", "#dc3545", "#28a745", "#ffc107", "#6f42c1"][: len(strengths)],
                            )
                        )
                        if volumes:
                            fig2.add_trace(
                                go.Bar(
                                    x=basin_labels,
                                    y=volumes,
                                    name="Volume fraction",
                                    marker_color=["#007bff55", "#dc354555", "#28a74555", "#ffc10755", "#6f42c155"][
                                        : len(volumes)
                                    ],
                                )
                            )
                        fig2.update_layout(
                            title="Basin Properties",
                            barmode="group",
                            yaxis_title="Value",
                            height=400,
                            margin={"t": 40, "b": 20},
                        )
                        st.plotly_chart(fig2, use_container_width=True)

                    # Convergence rates
                    rates = result.get("convergence_rates", [])
                    if rates:
                        st.markdown("**📉 Convergence Rates**")
                        rate_cols = st.columns(min(len(rates), 4))
                        for i, r in enumerate(rates[:4]):
                            with rate_cols[i]:
                                st.metric(f"Basin {i}", f"{r:.4f}" if isinstance(r, float) else str(r))

            except Exception as e:
                st.error(f"Computation error: {e}")

    # ── Tab 4: Resonance Pattern ──
    with tab4:
        st.subheader("🔊 Resonance Pattern (FFT)")
        st.markdown("""
        Extracts the dominant wavelength λ and phase angle Θ from field time series via FFT.
        - **Standing** pattern: high phase coherence, stationary nodes
        - **Traveling** pattern: propagating wave structure
        - **Mixed**: superposition of standing and traveling components
        """)

        preset_col4, _ = st.columns([1, 2])
        with preset_col4:
            fp4 = st.selectbox(
                "Presets",
                [
                    "Custom",
                    "🎵 Pure Sine (f = 0.1)",
                    "🎶 Harmonic Mix (f = 0.05 + 0.15)",
                    "📻 Noisy Signal (f = 0.2, high noise)",
                    "🔇 White Noise (no signal)",
                ],
                key="rcft_res_preset",
            )

        presets_res: dict[str, tuple[int, float, float, str]] = {
            "🎵 Pure Sine (f = 0.1)": (256, 0.1, 0.05, "pure"),
            "🎶 Harmonic Mix (f = 0.05 + 0.15)": (256, 0.05, 0.1, "harmonic"),
            "📻 Noisy Signal (f = 0.2, high noise)": (256, 0.2, 0.8, "pure"),
            "🔇 White Noise (no signal)": (256, 0.0, 1.0, "noise"),
        }
        _nr, _freq, _noise_r, _mode = presets_res.get(fp4, (128, 0.1, 0.3, "pure"))

        c1, c2 = st.columns(2)
        with c1:
            n_res = st.slider("Series length", 32, 512, _nr, key="rcft_nres")
        with c2:
            freq = st.slider("Primary frequency", 0.01, 0.5, _freq, 0.01, key="rcft_freq")
        noise_res = st.slider("Noise amplitude", 0.0, 2.0, _noise_r, 0.05, key="rcft_noise_res")

        if st.button("Compute Resonance", key="rcft_res", type="primary"):
            try:
                from closures.rcft.resonance_pattern import compute_resonance_pattern

                t = np.arange(n_res)
                if _mode == "harmonic":
                    signal = (
                        np.sin(2 * np.pi * freq * t)
                        + 0.5 * np.sin(2 * np.pi * 3 * freq * t)
                        + noise_res * np.random.randn(n_res)
                    )
                elif _mode == "noise":
                    signal = noise_res * np.random.randn(n_res)
                else:
                    signal = np.sin(2 * np.pi * freq * t) + noise_res * np.random.randn(n_res)

                result = compute_resonance_pattern(signal)

                st.divider()
                rc1, rc2, rc3, rc4 = st.columns(4)
                with rc1:
                    st.metric("λ_pattern", f"{result['lambda_pattern']:.4f}")
                with rc2:
                    st.metric("Θ_phase", f"{result['Theta_phase']:.4f}")
                with rc3:
                    dom_f = result.get("dominant_frequency", 0.0)
                    st.metric("f_dominant", f"{dom_f:.4f}")
                with rc4:
                    ptype = result.get("pattern_type", "")
                    color = "🎵" if ptype == "Standing" else "🌊" if ptype == "Traveling" else "🔀"
                    st.metric("Pattern", f"{color} {ptype}")

                # Additional metrics
                coh = result.get("phase_coherence", 0.0)
                harm = result.get("harmonic_content", 0.0)
                st.columns(3)[0].metric("Phase Coherence", f"{coh:.4f}")
                st.columns(3)[1].metric("Harmonic Content", f"{harm:.4f}")

                viz_l, viz_r = st.columns(2)
                with viz_l:
                    # Time-domain signal
                    fig = go.Figure()
                    fig.add_trace(
                        go.Scatter(
                            y=signal.tolist(), mode="lines", line={"color": "#007bff", "width": 1}, name="Signal"
                        )
                    )
                    fig.update_layout(
                        title="Time-Domain Signal",
                        xaxis_title="Sample",
                        yaxis_title="Amplitude",
                        height=320,
                        margin={"t": 40, "b": 20},
                    )
                    st.plotly_chart(fig, use_container_width=True)

                with viz_r:
                    # Power spectrum
                    spectrum = result.get("frequency_spectrum", None)
                    if spectrum is not None:
                        freqs = np.fft.rfftfreq(n_res).tolist()
                        powers = np.array(spectrum).tolist()
                        # Truncate to same length
                        min_len = min(len(freqs), len(powers))
                        fig2 = go.Figure()
                        fig2.add_trace(
                            go.Scatter(
                                x=freqs[:min_len],
                                y=powers[:min_len],
                                mode="lines",
                                fill="tozeroy",
                                fillcolor="rgba(220, 53, 69, 0.15)",
                                line={"color": "#dc3545", "width": 1.5},
                                name="Power",
                            )
                        )
                        # Mark dominant frequency
                        if dom_f > 0:
                            fig2.add_vline(
                                x=dom_f, line_dash="dash", line_color="#28a745", annotation_text=f"f = {dom_f:.3f}"
                            )
                        fig2.update_layout(
                            title="FFT Power Spectrum",
                            xaxis_title="Frequency",
                            yaxis_title="Power",
                            height=320,
                            margin={"t": 40, "b": 20},
                        )
                        st.plotly_chart(fig2, use_container_width=True)

            except Exception as e:
                st.error(f"Computation error: {e}")

    # ── Tab 5: Information Geometry ───────────────────────────────
    with tab5:
        st.subheader("📐 Information Geometry (Fisher Geodesics)")
        st.markdown(
            "**Fisher distance**: d_F(c₁,c₂) = 2|arcsin(√c₁) − arcsin(√c₂)|  \n"
            "**Geodesic**: c(t) = sin²((1−t)θ₁ + tθ₂)  \n"
            "**Efficiency**: η = d_F / L(path) ∈ (0,1]"
        )

        c1_ig, c2_ig = st.columns(2)
        with c1_ig:
            st.markdown("**State A**")
            ca1 = st.slider("c₁ (A)", 0.01, 0.99, 0.10, 0.01, key="ig_ca1")
            ca2 = st.slider("c₂ (A)", 0.01, 0.99, 0.20, 0.01, key="ig_ca2")
            ca3 = st.slider("c₃ (A)", 0.01, 0.99, 0.30, 0.01, key="ig_ca3")
        with c2_ig:
            st.markdown("**State B**")
            cb1 = st.slider("c₁ (B)", 0.01, 0.99, 0.80, 0.01, key="ig_cb1")
            cb2 = st.slider("c₂ (B)", 0.01, 0.99, 0.70, 0.01, key="ig_cb2")
            cb3 = st.slider("c₃ (B)", 0.01, 0.99, 0.90, 0.01, key="ig_cb3")

        if st.button("Compute Fisher Geometry", key="ig_compute", type="primary"):
            try:
                from closures.rcft.information_geometry import (
                    fisher_distance_weighted,
                    fisher_geodesic,
                    verify_fano_fisher_duality,
                )

                c_a = [ca1, ca2, ca3]
                c_b = [cb1, cb2, cb3]
                w = [1.0 / 3, 1.0 / 3, 1.0 / 3]

                dist_result = fisher_distance_weighted(c_a, c_b, w)
                r = dist_result._asdict()

                rc1, rc2, rc3 = st.columns(3)
                with rc1:
                    st.metric(
                        "Fisher Distance",
                        f"{r['distance']:.4f} rad",
                    )
                with rc2:
                    st.metric(
                        "Max Possible",
                        f"{r['max_possible']:.4f} rad",
                    )
                with rc3:
                    st.metric(
                        "Normalized",
                        f"{r['normalized']:.4f}",
                    )

                # Geodesic path visualization
                geodesic_pts = fisher_geodesic(ca1, cb1, n_points=50)
                if geodesic_pts:
                    fig = go.Figure()
                    ts = [pt.t for pt in geodesic_pts]
                    cs = [pt.c for pt in geodesic_pts]
                    thetas = [pt.theta for pt in geodesic_pts]

                    fig.add_trace(
                        go.Scatter(
                            x=ts,
                            y=cs,
                            mode="lines",
                            name="c(t) geodesic",
                            line={"color": "#007bff", "width": 2},
                        )
                    )
                    fig.add_trace(
                        go.Scatter(
                            x=ts,
                            y=thetas,
                            mode="lines",
                            name="θ(t)",
                            line={
                                "color": "#dc3545",
                                "dash": "dash",
                                "width": 1.5,
                            },
                        )
                    )
                    fig.add_trace(
                        go.Scatter(
                            x=[0, 1],
                            y=[ca1, cb1],
                            mode="markers",
                            marker={
                                "size": 12,
                                "color": "#28a745",
                                "symbol": "diamond",
                            },
                            name="A → B",
                        )
                    )
                    fig.update_layout(
                        title="Fisher Geodesic Path (c₁ channel)",
                        xaxis_title="t ∈ [0,1]",
                        yaxis_title="Value",
                        height=350,
                        margin={"t": 40, "b": 20},
                    )
                    st.plotly_chart(fig, use_container_width=True)

                # Fano-Fisher duality check
                st.markdown("**Fano-Fisher Duality** (T19): h″(c) = −g_F(c)")
                c_check = np.linspace(0.05, 0.95, 50)
                duality_data = []
                for cv in c_check:
                    ff = verify_fano_fisher_duality(float(cv))
                    duality_data.append(
                        {
                            "c": float(cv),
                            "h_pp": ff.h_double_prime,
                            "neg_gF": ff.neg_g_fisher,
                            "rel_err": ff.relative_error,
                        }
                    )

                fig2 = go.Figure()
                fig2.add_trace(
                    go.Scatter(
                        x=[d["c"] for d in duality_data],
                        y=[d["h_pp"] for d in duality_data],
                        mode="lines",
                        name="h″(c)",
                        line={"color": "#007bff", "width": 2},
                    )
                )
                fig2.add_trace(
                    go.Scatter(
                        x=[d["c"] for d in duality_data],
                        y=[d["neg_gF"] for d in duality_data],
                        mode="markers",
                        name="−g_F(c)",
                        marker={
                            "size": 4,
                            "color": "#dc3545",
                        },
                    )
                )
                fig2.update_layout(
                    title="Fano-Fisher Duality Verification",
                    xaxis_title="c",
                    yaxis_title="Curvature",
                    height=320,
                    margin={"t": 40, "b": 20},
                )
                st.plotly_chart(fig2, use_container_width=True)

            except Exception as e:
                st.error(f"Computation error: {e}")

    # ── Tab 6: Universality Class ─────────────────────────────────
    with tab6:
        st.subheader("🌡️ Universality Class (Partition Function)")
        st.markdown(
            "**Central charge**: c_eff = 1/p = 1/3  \n"
            "**Critical exponents**: ν=1/3, γ=1/3, η=1, α=0, β=5/6, δ=7/5  \n"
            "**Scaling relations**: Rushbrooke ✓  Widom ✓  Hyperscaling ✓"
        )

        uc1, uc2 = st.columns(2)
        with uc1:
            beta_u = st.number_input(
                "β (inverse temperature)",
                0.1,
                200.0,
                10.0,
                0.5,
                key="univ_beta",
            )
        with uc2:
            p_exp = st.number_input("p (drift exponent)", 2, 6, 3, key="univ_p")

        if st.button(
            "Compute Universality Class",
            key="univ_compute",
            type="primary",
        ):
            try:
                from closures.rcft.universality_class import (
                    compute_central_charge,
                    compute_critical_exponents,
                    compute_partition_function,
                    verify_scaling_relations,
                )

                pf = compute_partition_function(beta_u, p=p_exp)
                r = pf._asdict()

                rc1, rc2, rc3, rc4 = st.columns(4)
                with rc1:
                    st.metric("Z(β)", f"{r['Z']:.6f}")
                with rc2:
                    st.metric("Free energy F", f"{r['free_energy']:.4f}")
                with rc3:
                    st.metric(
                        "Internal energy U",
                        f"{r['internal_energy']:.4f}",
                    )
                with rc4:
                    st.metric(
                        "Specific heat C_V",
                        f"{r['specific_heat']:.4f}",
                    )

                mc1, mc2, mc3 = st.columns(3)
                with mc1:
                    st.metric("⟨ω⟩", f"{r['mean_omega']:.6f}")
                with mc2:
                    st.metric("Var(ω)", f"{r['var_omega']:.8f}")
                with mc3:
                    st.metric(
                        "χ (susceptibility)",
                        f"{r['susceptibility']:.6f}",
                    )

                # Central charge
                cc = compute_central_charge(beta_high=max(50.0, beta_u * 5), p=p_exp)
                st.markdown(
                    f"**Central charge**: c_eff = 1/p = {cc.c_eff:.4f}, "
                    f"C_V measured = {cc.C_V_measured:.4f}, "
                    f"relative error = {cc.relative_error:.2e}"
                )

                # Critical exponents table
                ce = compute_critical_exponents(p=p_exp)
                exp_data = [
                    {
                        "Exponent": "ν",
                        "Value": f"{ce.nu:.4f}",
                        "Formula": "1/p",
                    },
                    {
                        "Exponent": "γ",
                        "Value": f"{ce.gamma:.4f}",
                        "Formula": "(p−2)/p",
                    },
                    {
                        "Exponent": "η",
                        "Value": f"{ce.eta:.4f}",
                        "Formula": "4−p",
                    },
                    {
                        "Exponent": "α",
                        "Value": f"{ce.alpha:.4f}",
                        "Formula": "0",
                    },
                    {
                        "Exponent": "β",
                        "Value": f"{ce.beta_exp:.4f}",
                        "Formula": "(p+2)/(2p)",
                    },
                    {
                        "Exponent": "δ",
                        "Value": f"{ce.delta:.4f}",
                        "Formula": "(3p−2)/(p+2)",
                    },
                    {
                        "Exponent": "d_eff",
                        "Value": f"{ce.d_eff:.1f}",
                        "Formula": "2p",
                    },
                ]
                st.dataframe(
                    pd.DataFrame(exp_data),
                    use_container_width=True,
                    hide_index=True,
                )

                # Scaling relations
                sr = verify_scaling_relations(p=p_exp)
                sr_data = [
                    {
                        "Relation": s.name,
                        "LHS": f"{s.lhs:.6f}",
                        "RHS": f"{s.rhs:.6f}",
                        "Status": "✅" if s.satisfied else "❌",
                    }
                    for s in sr
                ]
                st.dataframe(
                    pd.DataFrame(sr_data),
                    use_container_width=True,
                    hide_index=True,
                )

                # Thermodynamic sweep over β
                beta_range = np.logspace(np.log10(0.5), np.log10(200), 60)
                thermo = []
                for b in beta_range:
                    try:
                        pf_b = compute_partition_function(float(b), p=p_exp)
                        thermo.append(
                            {
                                "beta": float(b),
                                "C_V": pf_b.specific_heat,
                                "mean_omega": pf_b.mean_omega,
                                "chi": pf_b.susceptibility,
                            }
                        )
                    except Exception:
                        pass

                if thermo:
                    fig = go.Figure()
                    fig.add_trace(
                        go.Scatter(
                            x=[d["beta"] for d in thermo],
                            y=[d["C_V"] for d in thermo],
                            mode="lines",
                            name="C_V",
                            line={"color": "#dc3545", "width": 2},
                        )
                    )
                    fig.add_hline(
                        y=1.0 / p_exp,
                        line_dash="dash",
                        line_color="#28a745",
                        annotation_text=f"c_eff = 1/{p_exp}",
                    )
                    fig.update_layout(
                        title="Specific Heat vs β",
                        xaxis_title="β",
                        xaxis_type="log",
                        yaxis_title="C_V",
                        height=350,
                        margin={"t": 40, "b": 20},
                    )
                    st.plotly_chart(fig, use_container_width=True)

            except Exception as e:
                st.error(f"Computation error: {e}")

    # ── Tab 7: Collapse Grammar ───────────────────────────────────
    with tab7:
        st.subheader("🔤 Collapse Grammar (Transfer Matrix)")
        st.markdown(
            "Metropolis dynamics under Γ(ω) at inverse temperature β.  \n"
            "**Spectral gap** Δ controls mixing time. "
            "**Entropy rate** h classifies complexity."
        )

        gc1, gc2 = st.columns(2)
        with gc1:
            beta_g = st.number_input(
                "β (inverse temperature)",
                0.1,
                100.0,
                5.0,
                0.5,
                key="gram_beta",
            )
        with gc2:
            seed_g = st.number_input("Random seed", 0, 99999, 42, key="gram_seed")

        if st.button("Compute Grammar", key="gram_compute", type="primary"):
            try:
                from closures.rcft.collapse_grammar import (
                    compute_grammar_entropy,
                    compute_transfer_matrix,
                )

                tm = compute_transfer_matrix(beta_g, seed=int(seed_g))
                ge = compute_grammar_entropy(tm.T)
                r_tm = tm._asdict()
                r_ge = ge._asdict()

                rc1, rc2, rc3, rc4 = st.columns(4)
                with rc1:
                    st.metric(
                        "Spectral Gap Δ",
                        f"{r_tm['spectral_gap']:.4f}",
                    )
                with rc2:
                    st.metric(
                        "Mixing Time τ",
                        f"{r_tm['mixing_time']:.2f}",
                    )
                with rc3:
                    st.metric(
                        "Entropy Rate h",
                        f"{r_ge['entropy_rate']:.4f} bits",
                    )
                with rc4:
                    cc = r_ge["complexity_class"]
                    cc_color = {
                        "FROZEN": "🟢",
                        "ORDERED": "🟡",
                        "COMPLEX": "🟠",
                    }.get(cc, "🔴")
                    st.metric("Class", f"{cc_color} {cc}")

                # Stationary distribution
                pi_stat = r_tm["stationary"]
                labels = ["STABLE", "WATCH", "COLLAPSE"]
                sd1, sd2, sd3 = st.columns(3)
                with sd1:
                    st.metric(
                        f"π({labels[0]})",
                        f"{float(pi_stat[0]):.4f}",
                    )
                with sd2:
                    st.metric(
                        f"π({labels[1]})",
                        f"{float(pi_stat[1]):.4f}",
                    )
                with sd3:
                    st.metric(
                        f"π({labels[2]})",
                        f"{float(pi_stat[2]):.4f}",
                    )

                # Transfer matrix heatmap
                T_matrix = r_tm["T"]
                fig = go.Figure(
                    go.Heatmap(
                        z=T_matrix.tolist(),
                        x=labels,
                        y=labels,
                        colorscale="Viridis",
                        text=[[f"{v:.3f}" for v in row] for row in T_matrix.tolist()],
                        texttemplate="%{text}",
                        textfont={"size": 14},
                        colorbar={"title": "P"},
                    )
                )
                fig.update_layout(
                    title=f"Transfer Matrix T (β = {beta_g})",
                    xaxis_title="From",
                    yaxis_title="To",
                    height=350,
                    margin={"t": 40, "b": 20},
                )
                st.plotly_chart(fig, use_container_width=True)

                # Grammar phase diagram over β
                st.markdown("**Grammar Phase Diagram**")
                beta_sweep = np.logspace(np.log10(0.5), np.log10(50), 30)
                phase_data: list[dict[str, object]] = []
                for b in beta_sweep:
                    try:
                        _tm = compute_transfer_matrix(float(b), seed=int(seed_g))
                        _ge = compute_grammar_entropy(_tm.T)
                        phase_data.append(
                            {
                                "beta": float(b),
                                "h_norm": _ge.normalized_entropy,
                                "gap": _tm.spectral_gap,
                                "class": _ge.complexity_class,
                            }
                        )
                    except Exception:
                        pass

                if phase_data:
                    fig2 = go.Figure()
                    fig2.add_trace(
                        go.Scatter(
                            x=[d["beta"] for d in phase_data],
                            y=[d["h_norm"] for d in phase_data],
                            mode="lines+markers",
                            name="h / h_max",
                            line={
                                "color": "#dc3545",
                                "width": 2,
                            },
                            marker={"size": 5},
                        )
                    )
                    fig2.add_trace(
                        go.Scatter(
                            x=[d["beta"] for d in phase_data],
                            y=[d["gap"] for d in phase_data],
                            mode="lines+markers",
                            name="Spectral Gap Δ",
                            line={
                                "color": "#007bff",
                                "width": 2,
                            },
                            marker={"size": 5},
                        )
                    )
                    # Region boundaries
                    fig2.add_hline(
                        y=0.2,
                        line_dash="dot",
                        line_color="#28a745",
                        annotation_text="FROZEN/ORDERED",
                    )
                    fig2.add_hline(
                        y=0.5,
                        line_dash="dot",
                        line_color="#ffc107",
                        annotation_text="ORDERED/COMPLEX",
                    )
                    fig2.add_hline(
                        y=0.8,
                        line_dash="dot",
                        line_color="#dc3545",
                        annotation_text="COMPLEX/CHAOTIC",
                    )
                    fig2.update_layout(
                        title="Grammar Phase Diagram",
                        xaxis_title="β",
                        xaxis_type="log",
                        yaxis_title="Value",
                        height=380,
                        margin={"t": 40, "b": 20},
                    )
                    st.plotly_chart(fig2, use_container_width=True)

            except Exception as e:
                st.error(f"Computation error: {e}")


# ══════════════════════════════════════════════════════════════════
#  ATOMIC PHYSICS PAGE
# ══════════════════════════════════════════════════════════════════


def render_atomic_physics_page() -> None:
    """Render interactive Atomic Physics domain page with 6 closures."""
    if st is None:
        return
    if go is None or pd is None or np is None:
        st.error(
            "Dashboard dependencies (plotly, pandas, numpy) are required for this page. Install with: `pip install plotly pandas numpy`"
        )
        return

    _ensure_closures_path()

    st.title("⚛️ Atomic Physics Domain")
    st.caption(
        "ATOM.INTSTACK.v1 — Ionization, spectral lines, electron config, fine structure, selection rules, field effects"
    )

    with st.expander("📖 Domain Overview", expanded=False):
        st.markdown(
            """
        The **Atomic Physics** domain maps atomic structure observables into
        UMCP contract space.  Each closure validates fundamental atomic
        principles against reference data (NIST ASD, CODATA 2022).

        | Closure | Principle | Key Observable |
        |---------|-----------|---------------|
        | Ionization Energy | Hydrogen-like + Slater screening | IE₁ deviation |
        | Spectral Lines | Rydberg formula | Wavelength precision |
        | Electron Config | Aufbau principle + Hund's rules | Shell completeness |
        | Fine Structure | Dirac relativistic correction (Zα)² | Energy splitting |
        | Selection Rules | E1: Δl=±1, Δm=0,±1, Δj=0,±1 | Rule compliance |
        | Zeeman/Stark | External field perturbation | Level splitting |
        """
        )

    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(
        [
            "⚡ Ionization Energy",
            "🌈 Spectral Lines",
            "🔘 Electron Config",
            "🔬 Fine Structure",
            "📏 Selection Rules",
            "🧲 Zeeman & Stark",
        ]
    )

    # ── Tab 1: Ionization Energy ──────────────────────────────────
    with tab1:
        st.subheader("⚡ Ionization Energy (Hydrogen-like + Screening)")
        st.markdown("**Model**: IE = 13.6 eV · Z_eff² / n_eff²  — Slater screening reduces Z_eff.")

        preset_col, _ = st.columns([1, 2])
        with preset_col:
            ip = st.selectbox(
                "Element preset",
                [
                    "Custom",
                    "H – Hydrogen (Z=1)",
                    "He – Helium (Z=2)",
                    "Li – Lithium (Z=3)",
                    "C – Carbon (Z=6)",
                    "N – Nitrogen (Z=7)",
                    "O – Oxygen (Z=8)",
                    "Ne – Neon (Z=10)",
                    "Na – Sodium (Z=11)",
                    "Si – Silicon (Z=14)",
                    "Ar – Argon (Z=18)",
                    "Ca – Calcium (Z=20)",
                    "Fe – Iron (Z=26)",
                    "Cu – Copper (Z=29)",
                    "Kr – Krypton (Z=36)",
                    "Ag – Silver (Z=47)",
                    "Au – Gold (Z=79)",
                    "U – Uranium (Z=92)",
                ],
                key="atom_ie_preset",
                help="Pick an element or enter Z manually",
            )
        presets_ie = {
            "H – Hydrogen (Z=1)": 1,
            "He – Helium (Z=2)": 2,
            "Li – Lithium (Z=3)": 3,
            "C – Carbon (Z=6)": 6,
            "N – Nitrogen (Z=7)": 7,
            "O – Oxygen (Z=8)": 8,
            "Ne – Neon (Z=10)": 10,
            "Na – Sodium (Z=11)": 11,
            "Si – Silicon (Z=14)": 14,
            "Ar – Argon (Z=18)": 18,
            "Ca – Calcium (Z=20)": 20,
            "Fe – Iron (Z=26)": 26,
            "Cu – Copper (Z=29)": 29,
            "Kr – Krypton (Z=36)": 36,
            "Ag – Silver (Z=47)": 47,
            "Au – Gold (Z=79)": 79,
            "U – Uranium (Z=92)": 92,
        }
        _lk_ie = "_last_atom_ie"
        if ip != "Custom" and st.session_state.get(_lk_ie) != ip:
            st.session_state["atom_z_ie"] = presets_ie[ip]
        st.session_state[_lk_ie] = ip
        _z = presets_ie.get(ip, 1)
        z_val = st.number_input("Z (atomic number)", 1, 118, _z, key="atom_z_ie", help="Atomic number (1–118)")

        if st.button("Compute Ionization Energy", key="atom_ie", type="primary"):
            try:
                from closures.atomic_physics.ionization_energy import (
                    compute_ionization,
                )

                result = compute_ionization(z_val)
                r = result._asdict()
                regime = r["regime"]
                regime_color = {
                    "Precise": "🟢",
                    "Approximate": "🟡",
                    "Screened": "🟠",
                }.get(regime, "🔴")

                rc1, rc2, rc3, rc4 = st.columns(4)
                with rc1:
                    st.metric("IE predicted (eV)", f"{r['IE_predicted_eV']:.3f}")
                with rc2:
                    st.metric("IE measured (eV)", f"{r['IE_measured_eV']:.3f}")
                with rc3:
                    st.metric("ω_eff", f"{r['omega_eff']:.4f}")
                with rc4:
                    st.metric("Regime", f"{regime_color} {regime}")

                mc1, mc2, mc3 = st.columns(3)
                with mc1:
                    st.metric("Z_eff (Slater)", f"{r['Z_eff']:.3f}")
                with mc2:
                    st.metric("n_eff", f"{r['n_eff']:.3f}")
                with mc3:
                    st.metric("Ψ_IE", f"{r['Psi_IE']:.4f}")

                # IE trend across elements
                z_range = list(range(1, min(37, max(z_val + 5, 37))))
                ie_data: list[dict[str, float]] = []
                for _zz in z_range:
                    try:
                        _r = compute_ionization(_zz)
                        ie_data.append(
                            {
                                "Z": _zz,
                                "IE_pred": _r.IE_predicted_eV,
                                "IE_meas": _r.IE_measured_eV,
                            }
                        )
                    except Exception:
                        pass

                if ie_data:
                    fig = go.Figure()
                    fig.add_trace(
                        go.Scatter(
                            x=[d["Z"] for d in ie_data],
                            y=[d["IE_meas"] for d in ie_data],
                            mode="lines+markers",
                            name="NIST measured",
                            marker={"size": 5, "color": "#007bff"},
                            line={"width": 2},
                        )
                    )
                    fig.add_trace(
                        go.Scatter(
                            x=[d["Z"] for d in ie_data],
                            y=[d["IE_pred"] for d in ie_data],
                            mode="lines",
                            name="Predicted",
                            line={
                                "color": "#dc3545",
                                "dash": "dash",
                                "width": 1.5,
                            },
                        )
                    )
                    fig.add_trace(
                        go.Scatter(
                            x=[z_val],
                            y=[r["IE_measured_eV"]],
                            mode="markers",
                            name=f"Z={z_val}",
                            marker={
                                "size": 12,
                                "color": "red",
                                "symbol": "star",
                            },
                        )
                    )
                    fig.update_layout(
                        title="First Ionization Energy Across Elements",
                        xaxis_title="Atomic Number Z",
                        yaxis_title="IE₁ (eV)",
                        height=380,
                        margin={"t": 40, "b": 20},
                    )
                    st.plotly_chart(fig, use_container_width=True)
            except Exception as e:
                st.error(f"Computation error: {e}")

    # ── Tab 2: Spectral Lines ─────────────────────────────────────
    with tab2:
        st.subheader("🌈 Spectral Lines (Rydberg Formula)")
        st.markdown("**Rydberg**: 1/λ = R∞ Z²(1/n₁² − 1/n₂²).  Series: Lyman (UV), Balmer (vis), Paschen (IR).")

        preset_col2, _ = st.columns([1, 2])
        with preset_col2:
            sp = st.selectbox(
                "Series preset",
                [
                    "Custom",
                    "Lyman series (UV, n₁=1)",
                    "Balmer series (visible, n₁=2)",
                    "Paschen series (IR, n₁=3)",
                    "Brackett series (far-IR, n₁=4)",
                    "Pfund series (n₁=5)",
                    "Balmer-α (Hα 656 nm, n=3→2)",
                    "Lyman-β (n=3→1)",
                    "He⁺ Lyman-α (Z=2, n=2→1)",
                    "He⁺ Balmer (Z=2, n=4→2)",
                    "Li²⁺ Lyman (Z=3, n=2→1)",
                ],
                key="atom_spec_preset",
            )
        presets_spec = {
            "Lyman series (UV, n₁=1)": (1, 1, 4),
            "Balmer series (visible, n₁=2)": (1, 2, 6),
            "Paschen series (IR, n₁=3)": (1, 3, 6),
            "Brackett series (far-IR, n₁=4)": (1, 4, 7),
            "Pfund series (n₁=5)": (1, 5, 8),
            "Balmer-α (Hα 656 nm, n=3→2)": (1, 2, 3),
            "Lyman-β (n=3→1)": (1, 1, 3),
            "He⁺ Lyman-α (Z=2, n=2→1)": (2, 1, 2),
            "He⁺ Balmer (Z=2, n=4→2)": (2, 2, 4),
            "Li²⁺ Lyman (Z=3, n=2→1)": (3, 1, 2),
        }
        _lk_sp = "_last_atom_spec"
        if sp != "Custom" and st.session_state.get(_lk_sp) != sp:
            _sv = presets_spec[sp]
            st.session_state["atom_z_spec"] = _sv[0]
            st.session_state["atom_n1"] = _sv[1]
            st.session_state["atom_n2"] = _sv[2]
        st.session_state[_lk_sp] = sp
        _z_s, _n1, _n2 = presets_spec.get(sp, (1, 2, 3))

        c1, c2, c3 = st.columns(3)
        with c1:
            z_spec = st.number_input("Z", 1, 118, _z_s, key="atom_z_spec")
        with c2:
            n_lower = st.number_input("n₁ (lower)", 1, 10, _n1, key="atom_n1")
        with c3:
            n_upper = st.number_input("n₂ (upper)", 2, 20, _n2, key="atom_n2")

        if st.button("Compute Spectral Series", key="atom_spec", type="primary"):
            try:
                from closures.atomic_physics.spectral_lines import (
                    compute_series,
                )

                series = compute_series(  # type: ignore[arg-type]
                    z_spec, n_lower, min(n_upper + 3, 12)
                )

                if series:
                    df = pd.DataFrame(series)
                    display_cols = [
                        "n_lower",
                        "n_upper",
                        "lambda_predicted_nm",
                        "energy_eV",
                        "series_name",
                        "regime",
                    ]
                    st.dataframe(
                        df[display_cols],
                        use_container_width=True,
                        hide_index=True,
                    )

                    # Spectrum visualisation
                    fig = go.Figure()
                    colors_map = {
                        "Lyman": "#9b59b6",
                        "Balmer": "#e74c3c",
                        "Paschen": "#e67e22",
                        "Brackett": "#2ecc71",
                    }
                    for row in series:
                        lam = row["lambda_predicted_nm"]
                        sname = row["series_name"]
                        color = colors_map.get(sname, "#3498db")
                        fig.add_trace(
                            go.Scatter(
                                x=[lam, lam],
                                y=[0, 1],
                                mode="lines",
                                line={"color": color, "width": 3},
                                name=f"n={row['n_upper']}→{row['n_lower']} ({lam:.1f} nm)",
                                showlegend=True,
                            )
                        )

                    fig.update_layout(
                        title=f"Emission Spectrum — Z={z_spec}",
                        xaxis_title="Wavelength (nm)",
                        yaxis={"visible": False},
                        height=300,
                        margin={"t": 40, "b": 20},
                    )
                    st.plotly_chart(fig, use_container_width=True)

                    # Energy level diagram
                    fig2 = go.Figure()
                    levels_shown = sorted(set([n_lower] + [r_row["n_upper"] for r_row in series]))
                    for n_lev in levels_shown:
                        e_lev = -13.6 * z_spec**2 / n_lev**2
                        fig2.add_trace(
                            go.Scatter(
                                x=[0, 1],
                                y=[e_lev, e_lev],
                                mode="lines",
                                line={"color": "#333", "width": 2},
                                name=f"n={n_lev} ({e_lev:.3f} eV)",
                            )
                        )
                        fig2.add_annotation(
                            x=1.1,
                            y=e_lev,
                            text=f"n={n_lev}",
                            showarrow=False,
                        )

                    fig2.update_layout(
                        title="Energy Level Diagram",
                        xaxis={
                            "visible": False,
                            "range": [-0.2, 1.5],
                        },
                        yaxis_title="Energy (eV)",
                        height=350,
                        margin={"t": 40, "b": 20},
                    )
                    st.plotly_chart(fig2, use_container_width=True)

            except Exception as e:
                st.error(f"Computation error: {e}")

    # ── Tab 3: Electron Configuration ─────────────────────────────
    with tab3:
        st.subheader("🔘 Electron Configuration (Aufbau Principle)")
        st.markdown(
            "Noble gas configurations (closed shells) are **collapse attractors** "
            "— they have maximum shell completeness (F_eff → 1)."
        )

        preset_col3, _ = st.columns([1, 2])
        with preset_col3:
            ec_p = st.selectbox(
                "Element preset",
                [
                    "Custom",
                    "H – Hydrogen (Z=1)",
                    "He – Noble gas (Z=2)",
                    "C – Carbon (Z=6)",
                    "N – Half-filled 2p (Z=7)",
                    "Ne – Noble gas (Z=10)",
                    "Na – Alkali metal (Z=11)",
                    "Ar – Noble gas (Z=18)",
                    "Cr – Anomalous 3d⁵4s¹ (Z=24)",
                    "Fe – Iron (Z=26)",
                    "Cu – Anomalous 3d¹⁰4s¹ (Z=29)",
                    "Kr – Noble gas (Z=36)",
                    "Ag – Anomalous 4d¹⁰5s¹ (Z=47)",
                    "Au – Anomalous 5d¹⁰6s¹ (Z=79)",
                    "U – Uranium (Z=92)",
                ],
                key="atom_config_preset",
            )
        presets_config = {
            "H – Hydrogen (Z=1)": 1,
            "He – Noble gas (Z=2)": 2,
            "C – Carbon (Z=6)": 6,
            "N – Half-filled 2p (Z=7)": 7,
            "Ne – Noble gas (Z=10)": 10,
            "Na – Alkali metal (Z=11)": 11,
            "Ar – Noble gas (Z=18)": 18,
            "Cr – Anomalous 3d⁵4s¹ (Z=24)": 24,
            "Fe – Iron (Z=26)": 26,
            "Cu – Anomalous 3d¹⁰4s¹ (Z=29)": 29,
            "Kr – Noble gas (Z=36)": 36,
            "Ag – Anomalous 4d¹⁰5s¹ (Z=47)": 47,
            "Au – Anomalous 5d¹⁰6s¹ (Z=79)": 79,
            "U – Uranium (Z=92)": 92,
        }
        _lk_ec = "_last_atom_config"
        if ec_p != "Custom" and st.session_state.get(_lk_ec) != ec_p:
            st.session_state["atom_z_config"] = presets_config[ec_p]
        st.session_state[_lk_ec] = ec_p
        _z_c = presets_config.get(ec_p, 26)
        z_config = st.number_input("Z (atomic number)", 1, 118, _z_c, key="atom_z_config")

        if st.button("Compute Configuration", key="atom_config", type="primary"):
            try:
                from closures.atomic_physics.electron_config import (
                    compute_electron_config,
                )

                result = compute_electron_config(z_config)
                r = result._asdict()
                regime = r["regime"]
                regime_color = {
                    "ClosedShell": "🟢",
                    "NearClosed": "🟢",
                    "HalfFilled": "🟡",
                }.get(regime, "🟠")

                st.markdown(f"### Configuration: `{r['configuration']}`")
                if r.get("noble_gas_core"):
                    st.caption(f"Noble gas core: {r['noble_gas_core']}")

                rc1, rc2, rc3, rc4 = st.columns(4)
                with rc1:
                    st.metric("Valence e⁻", r["valence_electrons"])
                with rc2:
                    st.metric(
                        "Shell Completeness",
                        f"{r['shell_completeness']:.3f}",
                    )
                with rc3:
                    st.metric("Block", r["group_block"])
                with rc4:
                    st.metric("Regime", f"{regime_color} {regime}")

                mc1, mc2, mc3 = st.columns(3)
                with mc1:
                    st.metric("Period", r["period"])
                with mc2:
                    st.metric("ω_eff", f"{r['omega_eff']:.4f}")
                with mc3:
                    st.metric("F_eff", f"{r['F_eff']:.4f}")

                # Shell completeness across elements
                z_range = list(range(1, min(z_config + 20, 119)))
                comp_data: list[dict[str, object]] = []
                for _zz in z_range:
                    try:
                        _r = compute_electron_config(_zz)
                        comp_data.append(
                            {
                                "Z": _zz,
                                "completeness": _r.shell_completeness,
                                "regime": _r.regime,
                            }
                        )
                    except Exception:
                        pass

                if comp_data:
                    fig = go.Figure()
                    colors = [
                        (
                            "#28a745"
                            if d["regime"] == "ClosedShell"
                            else (
                                "#ffc107"
                                if d["regime"] == "HalfFilled"
                                else ("#007bff" if d["regime"] == "NearClosed" else "#6c757d")
                            )
                        )
                        for d in comp_data
                    ]
                    fig.add_trace(
                        go.Bar(
                            x=[d["Z"] for d in comp_data],
                            y=[d["completeness"] for d in comp_data],
                            marker_color=colors,
                            name="Shell Completeness",
                        )
                    )
                    fig.add_trace(
                        go.Scatter(
                            x=[z_config],
                            y=[r["shell_completeness"]],
                            mode="markers",
                            marker={
                                "size": 14,
                                "color": "red",
                                "symbol": "star",
                            },
                            name=f"Z={z_config}",
                        )
                    )
                    fig.update_layout(
                        title="Shell Completeness Across Elements",
                        xaxis_title="Z",
                        yaxis_title="Completeness",
                        height=350,
                        margin={"t": 40, "b": 20},
                    )
                    st.plotly_chart(fig, use_container_width=True)

            except Exception as e:
                st.error(f"Computation error: {e}")

    # ── Tab 4: Fine Structure ─────────────────────────────────────
    with tab4:
        st.subheader("🔬 Fine Structure (Relativistic Correction)")
        st.markdown(
            "The relativistic parameter (Zα)² determines the regime: NonRelativistic → Relativistic → HeavyAtom."
        )

        preset_col4, _ = st.columns([1, 2])
        with preset_col4:
            fs_p = st.selectbox(
                "State preset",
                [
                    "Custom",
                    "H 2p₃/₂ (n=2, l=1, j=3/2)",
                    "H 2p₁/₂ (n=2, l=1, j=1/2)",
                    "H 2s₁/₂ (n=2, l=0, j=1/2)",
                    "H 3d₅/₂ (n=3, l=2, j=5/2)",
                    "Na 3p₃/₂ – D-line (Z=11)",
                    "He⁺ 2p₃/₂ (Z=2)",
                    "Li 2p₁/₂ (Z=3)",
                    "Cs 6p₃/₂ (Z=55)",
                    "U 2p₃/₂ – heavy atom (Z=92)",
                ],
                key="atom_fs_preset",
            )
        presets_fs: dict[str, tuple[int, int, int, float]] = {
            "H 2p₃/₂ (n=2, l=1, j=3/2)": (1, 2, 1, 1.5),
            "H 2p₁/₂ (n=2, l=1, j=1/2)": (1, 2, 1, 0.5),
            "H 2s₁/₂ (n=2, l=0, j=1/2)": (1, 2, 0, 0.5),
            "H 3d₅/₂ (n=3, l=2, j=5/2)": (1, 3, 2, 2.5),
            "Na 3p₃/₂ – D-line (Z=11)": (11, 3, 1, 1.5),
            "He⁺ 2p₃/₂ (Z=2)": (2, 2, 1, 1.5),
            "Li 2p₁/₂ (Z=3)": (3, 2, 1, 0.5),
            "Cs 6p₃/₂ (Z=55)": (55, 6, 1, 1.5),
            "U 2p₃/₂ – heavy atom (Z=92)": (92, 2, 1, 1.5),
        }
        _lk_fs = "_last_atom_fs"
        if fs_p != "Custom" and st.session_state.get(_lk_fs) != fs_p:
            _fv = presets_fs[fs_p]
            st.session_state["atom_z_fs"] = _fv[0]
            st.session_state["atom_n_fs"] = _fv[1]
            st.session_state["atom_l_fs"] = _fv[2]
            st.session_state["atom_j_fs"] = _fv[3]
        st.session_state[_lk_fs] = fs_p

        c1, c2, c3, c4 = st.columns(4)
        with c1:
            z_fs = st.number_input("Z", 1, 118, 1, key="atom_z_fs")
        with c2:
            n_fs = st.number_input("n", 1, 10, 2, key="atom_n_fs")
        with c3:
            l_fs = st.number_input("l", 0, min(n_fs - 1, 6), 1, key="atom_l_fs")
        with c4:
            j_options: list[float] = [l_fs - 0.5, l_fs + 0.5] if l_fs > 0 else [0.5]
            j_fs = st.selectbox("j", j_options, key="atom_j_fs")

        if st.button("Compute Fine Structure", key="atom_fs", type="primary"):
            try:
                from closures.atomic_physics.fine_structure import (
                    compute_fine_structure,
                )

                result = compute_fine_structure(z_fs, n_fs, l_fs, j_fs)
                r = result._asdict()
                regime = r["regime"]
                regime_color = {
                    "NonRelativistic": "🟢",
                    "Relativistic": "🟡",
                }.get(regime, "🔴")

                rc1, rc2, rc3, rc4 = st.columns(4)
                with rc1:
                    st.metric("E_n (eV)", f"{r['E_n_eV']:.4f}")
                with rc2:
                    st.metric("ΔE_fine (eV)", f"{r['E_fine_eV']:.8f}")
                with rc3:
                    st.metric("(Zα)²", f"{r['Z_alpha_squared']:.6f}")
                with rc4:
                    st.metric("Regime", f"{regime_color} {regime}")

                mc1, mc2, mc3 = st.columns(3)
                with mc1:
                    st.metric("Lamb shift (eV)", f"{r['E_lamb_eV']:.10f}")
                with mc2:
                    st.metric("j-splitting (eV)", f"{r['splitting_eV']:.8f}")
                with mc3:
                    st.metric("ω_eff", f"{r['omega_eff']:.6f}")

                # (Zα)² vs Z
                z_range = list(range(1, 93))
                za_data = [{"Z": _zz, "Za_sq": (_zz / 137.036) ** 2} for _zz in z_range]

                fig = go.Figure()
                fig.add_trace(
                    go.Scatter(
                        x=[d["Z"] for d in za_data],
                        y=[d["Za_sq"] for d in za_data],
                        mode="lines",
                        name="(Zα)²",
                        line={"color": "#007bff", "width": 2},
                    )
                )
                fig.add_hline(
                    y=0.01,
                    line_dash="dash",
                    line_color="#28a745",
                    annotation_text="NonRelativistic boundary",
                )
                fig.add_hline(
                    y=0.1,
                    line_dash="dash",
                    line_color="#dc3545",
                    annotation_text="HeavyAtom boundary",
                )
                fig.add_trace(
                    go.Scatter(
                        x=[z_fs],
                        y=[r["Z_alpha_squared"]],
                        mode="markers",
                        marker={
                            "size": 12,
                            "color": "red",
                            "symbol": "star",
                        },
                        name=f"Z={z_fs}",
                    )
                )
                fig.update_layout(
                    title="Relativistic Parameter (Zα)² Across Elements",
                    xaxis_title="Z",
                    yaxis_title="(Zα)²",
                    yaxis_type="log",
                    height=350,
                    margin={"t": 40, "b": 20},
                )
                st.plotly_chart(fig, use_container_width=True)
            except Exception as e:
                st.error(f"Computation error: {e}")

    # ── Tab 5: Selection Rules ────────────────────────────────────
    with tab5:
        st.subheader("📏 Selection Rules (E1 Dipole Transitions)")
        st.markdown("**E1 rules**: Δl=±1, Δm_l=0/±1, Δj=0/±1 (j=0→0 forbidden), Δs=0, parity change.")

        preset_col5, _ = st.columns([1, 2])
        with preset_col5:
            sr_p = st.selectbox(
                "Transition preset",
                [
                    "Custom",
                    "Lyman-α: 2p → 1s (allowed)",
                    "Balmer-α: 3d → 2p (allowed)",
                    "Balmer-β: 4d → 2p (allowed)",
                    "Na D₁: 3p → 3s (allowed)",
                    "σ⁺: 2p(m=1) → 1s (allowed)",
                    "Forbidden: 2s → 1s (Δl=0)",
                    "Forbidden: 3s → 2s (Δl=0)",
                    "Forbidden: 3d → 1s (Δl=2)",
                ],
                key="atom_sel_preset",
            )
        # Each preset: (n_i, l_i, ml_i, n_f, l_f, ml_f)
        presets_sel: dict[str, tuple[int, int, int, int, int, int]] = {
            "Lyman-α: 2p → 1s (allowed)": (2, 1, 0, 1, 0, 0),
            "Balmer-α: 3d → 2p (allowed)": (3, 2, 0, 2, 1, 0),
            "Balmer-β: 4d → 2p (allowed)": (4, 2, 0, 2, 1, 0),
            "Na D₁: 3p → 3s (allowed)": (3, 1, 0, 3, 0, 0),
            "σ⁺: 2p(m=1) → 1s (allowed)": (2, 1, 1, 1, 0, 0),
            "Forbidden: 2s → 1s (Δl=0)": (2, 0, 0, 1, 0, 0),
            "Forbidden: 3s → 2s (Δl=0)": (3, 0, 0, 2, 0, 0),
            "Forbidden: 3d → 1s (Δl=2)": (3, 2, 0, 1, 0, 0),
        }
        _lk_sr = "_last_atom_sel"
        if sr_p != "Custom" and st.session_state.get(_lk_sr) != sr_p:
            _srv = presets_sel[sr_p]
            st.session_state["atom_ni"] = _srv[0]
            st.session_state["atom_li"] = _srv[1]
            st.session_state["atom_mli"] = _srv[2]
            st.session_state["atom_nf"] = _srv[3]
            st.session_state["atom_lf"] = _srv[4]
            st.session_state["atom_mlf"] = _srv[5]
        st.session_state[_lk_sr] = sr_p

        st.markdown("**Initial state**")
        ic1, ic2, ic3, _ = st.columns(4)
        with ic1:
            n_i = st.number_input("n_i", 1, 10, 2, key="atom_ni")
        with ic2:
            l_i = st.number_input("l_i", 0, min(n_i - 1, 6), 1, key="atom_li")
        with ic3:
            ml_i = st.number_input("m_l_i", -l_i, l_i, 0, key="atom_mli")
        j_i_sel = l_i + 0.5

        st.markdown("**Final state**")
        fc1, fc2, fc3, _ = st.columns(4)
        with fc1:
            n_f = st.number_input("n_f", 1, 10, 1, key="atom_nf")
        with fc2:
            l_f = st.number_input("l_f", 0, min(n_f - 1, 6), 0, key="atom_lf")
        with fc3:
            ml_f = st.number_input("m_l_f", -max(l_f, 1), max(l_f, 1), 0, key="atom_mlf")
        j_f_sel = l_f + 0.5

        if st.button("Check Selection Rules", key="atom_sel", type="primary"):
            try:
                from closures.atomic_physics.selection_rules import (
                    compute_selection_rules,
                )

                result = compute_selection_rules(
                    n_i,
                    l_i,
                    ml_i,
                    0.5,
                    j_i_sel,
                    n_f,
                    l_f,
                    ml_f,
                    0.5,
                    j_f_sel,
                )
                r = result._asdict()
                regime = r["regime"]
                regime_color = {
                    "Allowed": "🟢",
                    "ForbiddenWeak": "🟡",
                }.get(regime, "🔴")

                rc1, rc2, rc3, rc4 = st.columns(4)
                with rc1:
                    st.metric("Transition", r["transition_type"])
                with rc2:
                    st.metric(
                        "Rules Met",
                        f"{r['rules_satisfied']}/{r['rules_total']}",
                    )
                with rc3:
                    st.metric("ω_eff", f"{r['omega_eff']:.4f}")
                with rc4:
                    st.metric("Regime", f"{regime_color} {regime}")

                rules_data = [
                    {
                        "Rule": "Δl = ±1",
                        "Value": f"Δl = {r['delta_l']}",
                        "Status": "✅" if r["l_rule_ok"] else "❌",
                    },
                    {
                        "Rule": "Δm_l = 0,±1",
                        "Value": f"Δm = {r['delta_ml']}",
                        "Status": "✅" if r["ml_rule_ok"] else "❌",
                    },
                    {
                        "Rule": "Δj = 0,±1",
                        "Value": f"Δj = {r['delta_j']}",
                        "Status": "✅" if r["j_rule_ok"] else "❌",
                    },
                    {
                        "Rule": "Δs = 0",
                        "Value": f"Δs = {r['delta_s']}",
                        "Status": "✅" if r["s_rule_ok"] else "❌",
                    },
                    {
                        "Rule": "Parity change",
                        "Value": str(r["parity_change"]),
                        "Status": "✅" if r["parity_rule_ok"] else "❌",
                    },
                ]
                st.dataframe(
                    pd.DataFrame(rules_data),
                    use_container_width=True,
                    hide_index=True,
                )

            except Exception as e:
                st.error(f"Computation error: {e}")

    # ── Tab 6: Zeeman & Stark ─────────────────────────────────────
    with tab6:
        st.subheader("🧲 Zeeman & Stark Effects")
        st.markdown("**Zeeman**: ΔE = m_j · g_J · μ_B · B  **Stark**: ΔE = −½ α_D E²")

        preset_col6, _ = st.columns([1, 2])
        with preset_col6:
            zs_p = st.selectbox(
                "Scenario preset",
                [
                    "Custom",
                    "H 2p in 1 T (weak Zeeman)",
                    "H 2p in 10 T (strong Zeeman)",
                    "Na D-line in 0.5 T (Z=11)",
                    "Cs 6p in 0.1 T (Z=55)",
                    "Stark: H n=2 in 10⁶ V/m",
                    "Combined: B=1 T + E=10⁵ V/m",
                ],
                key="atom_zs_preset",
            )
        # Each preset: (Z, n, l, B_tesla, E_Vm)
        presets_zs: dict[str, tuple[int, int, int, float, float]] = {
            "H 2p in 1 T (weak Zeeman)": (1, 2, 1, 1.0, 0.0),
            "H 2p in 10 T (strong Zeeman)": (1, 2, 1, 10.0, 0.0),
            "Na D-line in 0.5 T (Z=11)": (11, 3, 1, 0.5, 0.0),
            "Cs 6p in 0.1 T (Z=55)": (55, 6, 1, 0.1, 0.0),
            "Stark: H n=2 in 10⁶ V/m": (1, 2, 1, 0.0, 1e6),
            "Combined: B=1 T + E=10⁵ V/m": (1, 2, 1, 1.0, 1e5),
        }
        _lk_zs = "_last_atom_zs"
        if zs_p != "Custom" and st.session_state.get(_lk_zs) != zs_p:
            _zsv = presets_zs[zs_p]
            st.session_state["atom_z_zs"] = _zsv[0]
            st.session_state["atom_n_zs"] = _zsv[1]
            st.session_state["atom_l_zs"] = _zsv[2]
            st.session_state["atom_b_zs"] = _zsv[3]
            st.session_state["atom_e_zs"] = _zsv[4]
        st.session_state[_lk_zs] = zs_p

        c1, c2, c3 = st.columns(3)
        with c1:
            z_zs = st.number_input("Z", 1, 118, 1, key="atom_z_zs")
            n_zs = st.number_input("n", 1, 10, 2, key="atom_n_zs")
        with c2:
            l_zs = st.number_input("l", 0, min(n_zs - 1, 6), 1, key="atom_l_zs")
            j_zs_opts = [l_zs + 0.5] if l_zs == 0 else [l_zs - 0.5, l_zs + 0.5]
            j_zs = st.selectbox("j", j_zs_opts, key="atom_j_zs")
        with c3:
            mj_range = [x * 0.5 for x in range(int(-2 * j_zs), int(2 * j_zs) + 1)]
            mj_zs = st.selectbox(
                "m_j",
                mj_range,
                index=len(mj_range) // 2,
                key="atom_mj_zs",
            )

        fc1, fc2 = st.columns(2)
        with fc1:
            b_field = st.number_input("B (Tesla)", 0.0, 100.0, 1.0, 0.1, key="atom_b_zs")
        with fc2:
            e_field = st.number_input("E (V/m)", 0.0, 1e8, 0.0, 1e4, key="atom_e_zs")

        if st.button("Compute Field Effects", key="atom_zs", type="primary"):
            try:
                from closures.atomic_physics.zeeman_stark import (
                    compute_zeeman_stark,
                )

                result = compute_zeeman_stark(
                    z_zs,
                    n_zs,
                    l_zs,
                    0.5,
                    j_zs,
                    mj_zs,
                    B_tesla=b_field,
                    E_field_Vm=e_field,
                )
                r = result._asdict()
                regime = r["regime"]
                regime_color = {
                    "Weak": "🟢",
                    "Moderate": "🟡",
                }.get(regime, "🔴")

                rc1, rc2, rc3, rc4 = st.columns(4)
                with rc1:
                    st.metric(
                        "ΔE_Zeeman (eV)",
                        f"{r['delta_E_zeeman_eV']:.8f}",
                    )
                with rc2:
                    st.metric(
                        "ΔE_Stark (eV)",
                        f"{r['delta_E_stark_eV']:.8f}",
                    )
                with rc3:
                    st.metric("g_J (Landé)", f"{r['g_lande']:.4f}")
                with rc4:
                    st.metric("Regime", f"{regime_color} {regime}")

                mc1, mc2, mc3 = st.columns(3)
                with mc1:
                    st.metric("E_n (eV)", f"{r['E_n_eV']:.4f}")
                with mc2:
                    st.metric(
                        "ΔE_total (eV)",
                        f"{r['delta_E_total_eV']:.8f}",
                    )
                with mc3:
                    st.metric("Zeeman sub-levels", r["n_zeeman_levels"])

                # Zeeman splitting diagram for all m_j values
                if b_field > 0:
                    mj_all = [x * 0.5 for x in range(int(-2 * j_zs), int(2 * j_zs) + 1)]
                    fig = go.Figure()
                    for mj_v in mj_all:
                        r_v = compute_zeeman_stark(
                            z_zs,
                            n_zs,
                            l_zs,
                            0.5,
                            j_zs,
                            mj_v,
                            B_tesla=b_field,
                        )
                        # Unperturbed
                        fig.add_trace(
                            go.Scatter(
                                x=[0, 0.4],
                                y=[r_v.E_n_eV, r_v.E_n_eV],
                                mode="lines",
                                line={"color": "#333", "width": 2},
                                showlegend=False,
                            )
                        )
                        # Perturbed
                        e_p = r_v.E_n_eV + r_v.delta_E_zeeman_eV
                        fig.add_trace(
                            go.Scatter(
                                x=[0.6, 1],
                                y=[e_p, e_p],
                                mode="lines",
                                line={
                                    "color": "#007bff",
                                    "width": 2,
                                },
                                name=f"m_j = {mj_v:+.1f}",
                            )
                        )
                        # Connector
                        fig.add_trace(
                            go.Scatter(
                                x=[0.4, 0.6],
                                y=[r_v.E_n_eV, e_p],
                                mode="lines",
                                line={
                                    "color": "#ccc",
                                    "width": 1,
                                    "dash": "dot",
                                },
                                showlegend=False,
                            )
                        )

                    fig.update_layout(
                        title=f"Zeeman Splitting at B = {b_field} T",
                        xaxis={
                            "visible": False,
                            "range": [-0.1, 1.2],
                        },
                        yaxis_title="Energy (eV)",
                        height=400,
                        margin={"t": 40, "b": 20},
                    )
                    st.plotly_chart(fig, use_container_width=True)

            except Exception as e:
                st.error(f"Computation error: {e}")


# ══════════════════════════════════════════════════════════════════
#  STANDARD MODEL COMPARISON PAGE
# ══════════════════════════════════════════════════════════════════


def render_standard_model_page() -> None:
    """Render interactive Standard Model comparison page with 5 closures."""
    if st is None:
        return
    if go is None or pd is None or np is None:
        st.error(
            "Dashboard dependencies (plotly, pandas, numpy) are required for this page. Install with: `pip install plotly pandas numpy`"
        )
        return

    _ensure_closures_path()

    st.title("🔬 Standard Model Comparison")
    st.caption("SM.INTSTACK.v1 — Particle catalog, coupling constants, cross sections, Higgs mechanism, CKM mixing")

    with st.expander("📖 Domain Overview", expanded=False):
        st.markdown(
            """
        The **Standard Model** domain maps particle physics observables
        into UMCP contract space.

        | Closure | Principle | Key Observable |
        |---------|-----------|---------------|
        | Particle Catalog | 17-particle SM table | Mass/charge/spin |
        | Coupling Constants | 1-loop RGE: α_s(Q²) | Running drift |
        | Cross Sections | R-ratio: σ(e⁺e⁻→had)/σ(μμ) | QCD validation |
        | Symmetry Breaking | Higgs VEV, Yukawa | Mass prediction |
        | CKM Mixing | Wolfenstein parametrization | Unitarity deficit |
        """
        )

    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        [
            "📋 Particle Catalog",
            "📉 Running Couplings",
            "📊 Cross Sections",
            "⚡ Higgs Mechanism",
            "🔀 CKM Mixing",
        ]
    )

    # ── Tab 1: Particle Catalog ───────────────────────────────────
    with tab1:
        st.subheader("📋 Standard Model Particle Catalog")
        st.markdown(
            "All 17 fundamental particles (PDG 2024). "
            "Mass, charge, spin embedded into UMCP coordinates c₁,c₂,c₃ ∈ [0,1]."
        )

        try:
            from closures.standard_model.particle_catalog import (
                list_particles,
                particle_table,
            )

            cat_filter = st.selectbox(
                "Filter by category",
                [
                    "All",
                    "Quark",
                    "Lepton",
                    "GaugeBoson",
                    "ScalarBoson",
                ],
                key="sm_cat_filter",
                help="Filter particles by SM category",
            )

            particles = particle_table()
            if cat_filter != "All":
                particles = [p for p in particles if p["category"] == cat_filter]

            display_cols = [
                "symbol",
                "name",
                "category",
                "mass_GeV",
                "charge_e",
                "spin",
                "generation",
                "c1",
                "c2",
                "c3",
                "omega",
                "F",
                "regime",
            ]
            df = pd.DataFrame(particles)
            if not df.empty:
                st.dataframe(
                    df[display_cols],
                    use_container_width=True,
                    hide_index=True,
                )

            # Mass spectrum
            all_particles = particle_table()
            masses = [p for p in all_particles if p["mass_GeV"] > 0]
            if masses:
                import math as _math

                fig = go.Figure()
                cat_colors = {
                    "Quark": "#e74c3c",
                    "Lepton": "#3498db",
                    "GaugeBoson": "#2ecc71",
                    "ScalarBoson": "#f39c12",
                }
                for cat in cat_colors:
                    cat_p = [p for p in masses if p["category"] == cat]
                    if cat_p:
                        fig.add_trace(
                            go.Scatter(
                                x=[p["symbol"] for p in cat_p],
                                y=[_math.log10(p["mass_GeV"]) for p in cat_p],
                                mode="markers+text",
                                marker={
                                    "size": 12,
                                    "color": cat_colors[cat],
                                },
                                text=[p["symbol"] for p in cat_p],
                                textposition="top center",
                                name=cat,
                            )
                        )

                fig.update_layout(
                    title="SM Mass Spectrum (log₁₀ scale)",
                    xaxis_title="Particle",
                    yaxis_title="log₁₀(m / GeV)",
                    height=450,
                    margin={"t": 40, "b": 20},
                )
                st.plotly_chart(fig, use_container_width=True)

            # Radar chart
            st.markdown("**UMCP Coordinate Embedding**")
            radar_particles = list_particles()[:6]
            if radar_particles:
                fig2 = go.Figure()
                categories = [
                    "c₁ (mass)",
                    "c₂ (charge)",
                    "c₃ (spin)",
                    "F (stability)",
                    "c₁ (mass)",
                ]
                for p in radar_particles:
                    values = [p.c1, p.c2, p.c3, p.F, p.c1]
                    fig2.add_trace(
                        go.Scatterpolar(
                            r=values,
                            theta=categories,
                            fill="toself",
                            name=f"{p.symbol} ({p.name})",
                            opacity=0.6,
                        )
                    )
                fig2.update_layout(
                    polar={
                        "radialaxis": {
                            "visible": True,
                            "range": [0, 1],
                        }
                    },
                    title="Particle Embedding Radar",
                    height=400,
                )
                st.plotly_chart(fig2, use_container_width=True)

        except Exception as e:
            st.error(f"Computation error: {e}")

    # ── Tab 2: Running Couplings ──────────────────────────────────
    with tab2:
        st.subheader("📉 Running Coupling Constants (1-loop RGE)")
        st.markdown(
            "**Asymptotic freedom**: α_s(Q) decreases at high energy.  \n"
            "**QED screening**: α_em(Q) increases at high energy."
        )

        preset_col_c, _ = st.columns([1, 2])
        with preset_col_c:
            cp_p = st.selectbox(
                "Energy range preset",
                [
                    "Custom",
                    "QCD region (1–10 GeV)",
                    "Charm → bottom (1–5 GeV)",
                    "Z-pole region (50–150 GeV)",
                    "LHC range (10–14000 GeV)",
                    "Full survey (0.5–100k GeV)",
                    "Grand unification (100–10⁶ GeV)",
                ],
                key="sm_coupling_preset",
            )
        presets_coup: dict[str, tuple[float, float]] = {
            "QCD region (1–10 GeV)": (1.0, 10.0),
            "Charm → bottom (1–5 GeV)": (1.0, 5.0),
            "Z-pole region (50–150 GeV)": (50.0, 150.0),
            "LHC range (10–14000 GeV)": (10.0, 14000.0),
            "Full survey (0.5–100k GeV)": (0.5, 1e5),
            "Grand unification (100–10⁶ GeV)": (100.0, 1e6),
        }
        _lk_cp = "_last_sm_coupling"
        if cp_p != "Custom" and st.session_state.get(_lk_cp) != cp_p:
            _cpv = presets_coup[cp_p]
            st.session_state["sm_qmin"] = _cpv[0]
            st.session_state["sm_qmax"] = _cpv[1]
        st.session_state[_lk_cp] = cp_p
        _qd = presets_coup.get(cp_p, (1.0, 1000.0))

        c1, c2 = st.columns(2)
        with c1:
            q_min = st.number_input("Q_min (GeV)", 0.5, 1e4, _qd[0], key="sm_qmin")
        with c2:
            q_max = st.number_input("Q_max (GeV)", 10.0, 1e6, _qd[1], key="sm_qmax")

        if st.button("Compute Running Couplings", key="sm_coupling", type="primary"):
            try:
                from closures.standard_model.coupling_constants import (
                    ALPHA_S_MZ,
                    M_Z_GEV,
                    compute_running_coupling,
                )

                q_values = np.logspace(np.log10(q_min), np.log10(q_max), 100)
                results = []
                for q in q_values:
                    rr = compute_running_coupling(float(q))
                    results.append(rr._asdict())

                df = pd.DataFrame(results)

                # Summary at landmark scales
                summary_scales = [1.0, 2.0, 10.0, 91.2, 500.0, 1000.0]
                summary_data = []
                for q in summary_scales:
                    if q_min <= q <= q_max:
                        rr = compute_running_coupling(q)
                        summary_data.append(
                            {
                                "Q (GeV)": q,
                                "α_s": f"{rr.alpha_s:.4f}",
                                "α_em": f"{rr.alpha_em:.6f}",
                                "n_f": rr.n_flavors,
                                "ω_eff": f"{rr.omega_eff:.4f}",
                                "Regime": rr.regime,
                            }
                        )
                if summary_data:
                    st.dataframe(
                        pd.DataFrame(summary_data),
                        use_container_width=True,
                        hide_index=True,
                    )

                # α_s running plot
                fig = go.Figure()
                fig.add_trace(
                    go.Scatter(
                        x=df["Q_GeV"].tolist(),
                        y=df["alpha_s"].tolist(),
                        mode="lines",
                        name="α_s(Q)",
                        line={"color": "#dc3545", "width": 2},
                    )
                )
                fig.add_trace(
                    go.Scatter(
                        x=df["Q_GeV"].tolist(),
                        y=(df["alpha_em"] * 100).tolist(),
                        mode="lines",
                        name="α_em(Q) × 100",
                        line={"color": "#007bff", "width": 2},
                    )
                )
                fig.add_hline(
                    y=ALPHA_S_MZ,
                    line_dash="dash",
                    line_color="#28a745",
                    annotation_text=f"α_s(M_Z) = {ALPHA_S_MZ}",
                )
                fig.add_vline(
                    x=M_Z_GEV,
                    line_dash="dot",
                    line_color="#6c757d",
                    annotation_text=f"M_Z = {M_Z_GEV}",
                )
                fig.update_layout(
                    title="Running Coupling Constants",
                    xaxis_title="Q (GeV)",
                    xaxis_type="log",
                    yaxis_title="Coupling strength",
                    height=400,
                    margin={"t": 40, "b": 20},
                )
                st.plotly_chart(fig, use_container_width=True)

                # Unification proximity
                uni_data: list[dict[str, float]] = []
                q_wide = np.logspace(0, 6, 200)
                for q in q_wide:
                    rr = compute_running_coupling(float(q))
                    uni_data.append(
                        {
                            "Q": float(q),
                            "proximity": rr.unification_proximity,
                        }
                    )

                fig2 = go.Figure()
                fig2.add_trace(
                    go.Scatter(
                        x=[d["Q"] for d in uni_data],
                        y=[d["proximity"] for d in uni_data],
                        mode="lines",
                        name="Unification Proximity",
                        line={"color": "#9b59b6", "width": 2},
                        fill="tozeroy",
                        fillcolor="rgba(155,89,182,0.1)",
                    )
                )
                fig2.update_layout(
                    title="Coupling Unification Proximity",
                    xaxis_title="Q (GeV)",
                    xaxis_type="log",
                    yaxis_title="Proximity [0,1]",
                    height=300,
                    margin={"t": 40, "b": 20},
                )
                st.plotly_chart(fig2, use_container_width=True)

            except Exception as e:
                st.error(f"Computation error: {e}")

    # ── Tab 3: Cross Sections ─────────────────────────────────────
    with tab3:
        st.subheader("📊 e⁺e⁻ → Hadrons & R-ratio")
        st.markdown("R = σ(e⁺e⁻→had) / σ(e⁺e⁻→μ⁺μ⁻) = N_c Σ Q_f² · (1 + α_s/π + …)")

        preset_col_xs, _ = st.columns([1, 2])
        with preset_col_xs:
            xs_p = st.selectbox(
                "Energy preset",
                [
                    "Custom",
                    "Low energy (2.0 GeV)",
                    "J/ψ resonance (3.10 GeV)",
                    "τ threshold (3.56 GeV)",
                    "Υ(1S) resonance (9.46 GeV)",
                    "B-factory (10.58 GeV)",
                    "Z-pole (91.2 GeV)",
                    "W⁺W⁻ threshold (161 GeV)",
                    "LEP-II (200 GeV)",
                ],
                key="sm_xs_preset",
            )
        presets_xs: dict[str, float] = {
            "Low energy (2.0 GeV)": 2.0,
            "J/ψ resonance (3.10 GeV)": 3.10,
            "τ threshold (3.56 GeV)": 3.56,
            "Υ(1S) resonance (9.46 GeV)": 9.46,
            "B-factory (10.58 GeV)": 10.58,
            "Z-pole (91.2 GeV)": 91.2,
            "W⁺W⁻ threshold (161 GeV)": 161.0,
            "LEP-II (200 GeV)": 200.0,
        }
        _lk_xs = "_last_sm_xs"
        if xs_p != "Custom" and st.session_state.get(_lk_xs) != xs_p:
            st.session_state["sm_sqrts"] = presets_xs[xs_p]
        st.session_state[_lk_xs] = xs_p
        _sqd = presets_xs.get(xs_p, 91.2)

        sqrt_s = st.number_input("√s (GeV)", 1.0, 500.0, _sqd, 0.1, key="sm_sqrts")

        if st.button("Compute Cross Section", key="sm_xsec", type="primary"):
            try:
                from closures.standard_model.cross_sections import (
                    R_EXPERIMENTAL,
                    compute_cross_section,
                )

                result = compute_cross_section(sqrt_s)
                r = result._asdict()
                regime = r["regime"]
                regime_color = {
                    "Validated": "🟢",
                    "Tension": "🟡",
                }.get(regime, "🔴")

                rc1, rc2, rc3, rc4 = st.columns(4)
                with rc1:
                    st.metric("R (tree)", f"{r['R_predicted']:.4f}")
                with rc2:
                    st.metric("R (QCD)", f"{r['R_QCD_corrected']:.4f}")
                with rc3:
                    st.metric("σ_point (pb)", f"{r['sigma_point_pb']:.2f}")
                with rc4:
                    st.metric("Regime", f"{regime_color} {regime}")

                mc1, mc2, mc3, mc4 = st.columns(4)
                with mc1:
                    st.metric("N_c (colors)", r["n_colors"])
                with mc2:
                    st.metric("n_f (flavors)", r["n_active_flavors"])
                with mc3:
                    st.metric("Σ Q_f²", f"{r['sum_Qf_squared']:.4f}")
                with mc4:
                    st.metric("α_s at √s", f"{r['alpha_s_at_s']:.4f}")

                # R-ratio vs √s
                s_range = np.logspace(np.log10(1.5), np.log10(300), 200)
                r_data: list[dict[str, float]] = []
                for s_val in s_range:
                    try:
                        _r = compute_cross_section(float(s_val))
                        r_data.append(
                            {
                                "sqrt_s": float(s_val),
                                "R_tree": _r.R_predicted,
                                "R_QCD": _r.R_QCD_corrected,
                            }
                        )
                    except Exception:
                        pass

                if r_data:
                    fig = go.Figure()
                    fig.add_trace(
                        go.Scatter(
                            x=[d["sqrt_s"] for d in r_data],
                            y=[d["R_QCD"] for d in r_data],
                            mode="lines",
                            name="R (QCD)",
                            line={
                                "color": "#007bff",
                                "width": 2,
                            },
                        )
                    )
                    fig.add_trace(
                        go.Scatter(
                            x=[d["sqrt_s"] for d in r_data],
                            y=[d["R_tree"] for d in r_data],
                            mode="lines",
                            name="R (tree)",
                            line={
                                "color": "#dc3545",
                                "width": 1.5,
                                "dash": "dash",
                            },
                        )
                    )

                    for name, (s_exp, r_exp) in R_EXPERIMENTAL.items():
                        fig.add_trace(
                            go.Scatter(
                                x=[s_exp],
                                y=[r_exp],
                                mode="markers",
                                marker={
                                    "size": 10,
                                    "color": "#28a745",
                                    "symbol": "diamond",
                                },
                                name=f"{name} (exp)",
                            )
                        )

                    thresholds = [
                        (3.0, "cc̄"),
                        (10.0, "bb̄"),
                    ]
                    for s_th, label in thresholds:
                        fig.add_vline(
                            x=s_th,
                            line_dash="dot",
                            line_color="#ffc107",
                            annotation_text=label,
                            annotation_position="top right",
                        )

                    fig.update_layout(
                        title="R-ratio vs √s",
                        xaxis_title="√s (GeV)",
                        xaxis_type="log",
                        yaxis_title="R",
                        height=450,
                        margin={"t": 40, "b": 20},
                    )
                    st.plotly_chart(fig, use_container_width=True)

            except Exception as e:
                st.error(f"Computation error: {e}")

    # ── Tab 4: Higgs Mechanism ────────────────────────────────────
    with tab4:
        st.subheader("⚡ Higgs Mechanism & EWSB")
        st.markdown("V(φ) = μ²|φ|² + λ|φ|⁴  →  v ≈ 246.22 GeV  →  m_f = y_f v/√2,  M_W = g₂v/2,  M_Z = v√(g₁²+g₂²)/2")

        preset_col_h, _ = st.columns([1, 2])
        with preset_col_h:
            hg_p = st.selectbox(
                "Scenario preset",
                [
                    "Custom",
                    "SM measured (PDG 2024)",
                    "Heavy Higgs (m_H = 150 GeV)",
                    "Light Higgs (m_H = 100 GeV)",
                    "High VEV (v = 260 GeV)",
                    "Low VEV (v = 230 GeV)",
                    "Pre-discovery prediction (m_H = 115)",
                ],
                key="sm_higgs_preset",
            )
        presets_higgs: dict[str, tuple[float, float]] = {
            "SM measured (PDG 2024)": (246.22, 125.25),
            "Heavy Higgs (m_H = 150 GeV)": (246.22, 150.0),
            "Light Higgs (m_H = 100 GeV)": (246.22, 100.0),
            "High VEV (v = 260 GeV)": (260.0, 125.25),
            "Low VEV (v = 230 GeV)": (230.0, 125.25),
            "Pre-discovery prediction (m_H = 115)": (246.22, 115.0),
        }
        _lk_hg = "_last_sm_higgs"
        if hg_p != "Custom" and st.session_state.get(_lk_hg) != hg_p:
            _hv = presets_higgs[hg_p]
            st.session_state["sm_vev"] = _hv[0]
            st.session_state["sm_mh"] = _hv[1]
        st.session_state[_lk_hg] = hg_p
        _hd = presets_higgs.get(hg_p, (246.22, 125.25))

        c1, c2 = st.columns(2)
        with c1:
            v_input = st.number_input(
                "VEV (GeV)",
                200.0,
                300.0,
                _hd[0],
                0.01,
                key="sm_vev",
            )
        with c2:
            mh_input = st.number_input(
                "m_H (GeV)",
                100.0,
                200.0,
                _hd[1],
                0.01,
                key="sm_mh",
            )

        if st.button("Compute Higgs Mechanism", key="sm_higgs", type="primary"):
            try:
                from closures.standard_model.symmetry_breaking import (
                    M_W_MEASURED,
                    M_Z_MEASURED,
                    compute_higgs_mechanism,
                )

                result = compute_higgs_mechanism(v_input, mh_input)
                r = result._asdict()
                regime = r["regime"]
                regime_color = {
                    "Consistent": "🟢",
                    "Tension": "🟡",
                }.get(regime, "🔴")

                rc1, rc2, rc3, rc4 = st.columns(4)
                with rc1:
                    st.metric("VEV (GeV)", f"{r['v_GeV']:.2f}")
                with rc2:
                    st.metric("λ (quartic)", f"{r['lambda_quartic']:.6f}")
                with rc3:
                    st.metric("μ² (GeV²)", f"{r['mu_squared']:.2f}")
                with rc4:
                    st.metric("Regime", f"{regime_color} {regime}")

                mc1, mc2 = st.columns(2)
                with mc1:
                    st.metric(
                        "M_W predicted",
                        f"{r['m_W_predicted']:.3f} GeV",
                        f"meas: {M_W_MEASURED}",
                    )
                with mc2:
                    st.metric(
                        "M_Z predicted",
                        f"{r['m_Z_predicted']:.3f} GeV",
                        f"meas: {M_Z_MEASURED}",
                    )

                # Yukawa chart
                import math as _math

                yukawas = r["yukawa_couplings"]
                sorted_y = sorted(yukawas.items(), key=lambda x: -x[1])
                fig = go.Figure()
                fig.add_trace(
                    go.Bar(
                        x=[name for name, _ in sorted_y],
                        y=[_math.log10(y) if y > 0 else -10 for _, y in sorted_y],
                        marker_color=[
                            (
                                "#dc3545"
                                if name
                                in [
                                    "top",
                                    "bottom",
                                    "charm",
                                    "strange",
                                    "up",
                                    "down",
                                ]
                                else "#007bff"
                            )
                            for name, _ in sorted_y
                        ],
                        text=[f"{y:.2e}" for _, y in sorted_y],
                        textposition="outside",
                    )
                )
                fig.update_layout(
                    title="Yukawa Couplings (log₁₀ scale)",
                    xaxis_title="Fermion",
                    yaxis_title="log₁₀(y_f)",
                    height=400,
                    margin={"t": 40, "b": 20},
                )
                st.plotly_chart(fig, use_container_width=True)

                # Higgs potential
                phi_range = np.linspace(-300, 300, 500)
                lam = r["lambda_quartic"]
                mu_sq = r["mu_squared"]
                V = mu_sq * (phi_range**2) / (r["v_GeV"] ** 2) + lam * (phi_range**4) / (r["v_GeV"] ** 4)
                V = V / 1e6  # scale for display

                fig2 = go.Figure()
                fig2.add_trace(
                    go.Scatter(
                        x=phi_range.tolist(),
                        y=V.tolist(),
                        mode="lines",
                        name="V(φ)",
                        line={"color": "#9b59b6", "width": 2},
                    )
                )
                fig2.add_vline(
                    x=r["v_GeV"],
                    line_dash="dash",
                    line_color="#28a745",
                    annotation_text=f"v = {r['v_GeV']:.1f} GeV",
                )
                fig2.add_vline(
                    x=-r["v_GeV"],
                    line_dash="dash",
                    line_color="#28a745",
                )
                fig2.update_layout(
                    title="Higgs Potential (Mexican Hat)",
                    xaxis_title="φ (GeV)",
                    yaxis_title="V(φ) (arb. units)",
                    height=350,
                    margin={"t": 40, "b": 20},
                )
                st.plotly_chart(fig2, use_container_width=True)

            except Exception as e:
                st.error(f"Computation error: {e}")

    # ── Tab 5: CKM Mixing ────────────────────────────────────────
    with tab5:
        st.subheader("🔀 CKM Quark Mixing Matrix")
        st.markdown(
            "**Wolfenstein**: λ ≈ 0.2265, A ≈ 0.790, ρ̄ ≈ 0.141, η̄ ≈ 0.357  \n"
            "**Jarlskog**: J ≈ 3.08 × 10⁻⁵ (CP violation)"
        )

        preset_col_ckm, _ = st.columns([1, 2])
        with preset_col_ckm:
            ckm_p = st.selectbox(
                "Parameter set",
                [
                    "Custom",
                    "PDG 2024 central values",
                    "PDG 2020 values",
                    "Enhanced CP violation",
                    "No CP violation (η̄ = 0)",
                    "Cabibbo limit (A = 0)",
                    "Large mixing (λ = 0.30)",
                ],
                key="sm_ckm_preset",
            )
        presets_ckm: dict[str, tuple[float, float, float, float]] = {
            "PDG 2024 central values": (0.22650, 0.790, 0.141, 0.357),
            "PDG 2020 values": (0.22500, 0.826, 0.159, 0.348),
            "Enhanced CP violation": (0.22650, 0.790, 0.200, 0.400),
            "No CP violation (η̄ = 0)": (0.22650, 0.790, 0.141, 0.000),
            "Cabibbo limit (A = 0)": (0.22650, 0.001, 0.001, 0.001),
            "Large mixing (λ = 0.30)": (0.300, 0.790, 0.141, 0.357),
        }
        _lk_ckm = "_last_sm_ckm"
        if ckm_p != "Custom" and st.session_state.get(_lk_ckm) != ckm_p:
            _cv = presets_ckm[ckm_p]
            st.session_state["sm_lam"] = _cv[0]
            st.session_state["sm_a"] = _cv[1]
            st.session_state["sm_rho"] = _cv[2]
            st.session_state["sm_eta"] = _cv[3]
        st.session_state[_lk_ckm] = ckm_p
        _cd = presets_ckm.get(ckm_p, (0.22650, 0.790, 0.141, 0.357))

        c1, c2 = st.columns(2)
        with c1:
            lam_w = st.number_input(
                "λ_W",
                0.1,
                0.5,
                _cd[0],
                0.0001,
                key="sm_lam",
                format="%.5f",
            )
            rho_bar = st.number_input(
                "ρ̄",
                0.0,
                1.0,
                _cd[2],
                0.001,
                key="sm_rho",
                format="%.3f",
            )
        with c2:
            a_w = st.number_input(
                "A",
                0.1,
                2.0,
                _cd[1],
                0.001,
                key="sm_a",
                format="%.3f",
            )
            eta_bar = st.number_input(
                "η̄",
                0.0,
                1.0,
                _cd[3],
                0.001,
                key="sm_eta",
                format="%.3f",
            )

        if st.button("Compute CKM Matrix", key="sm_ckm", type="primary"):
            try:
                from closures.standard_model.ckm_mixing import (
                    compute_ckm_mixing,
                )

                result = compute_ckm_mixing(lam_w, a_w, rho_bar, eta_bar)
                r = result._asdict()
                regime = r["regime"]
                regime_color = {
                    "Unitary": "🟢",
                    "Tension": "🟡",
                }.get(regime, "🔴")

                # Display matrix
                st.markdown("**|V_CKM| matrix:**")
                labels_r = ["u", "c", "t"]
                labels_c = ["d", "s", "b"]
                matrix_df = pd.DataFrame(
                    r["V_matrix"],
                    index=labels_r,
                    columns=labels_c,
                )
                st.dataframe(matrix_df, use_container_width=True)

                rc1, rc2, rc3, rc4 = st.columns(4)
                with rc1:
                    st.metric("J_CP", f"{r['J_CP']:.8f}")
                with rc2:
                    st.metric(
                        "Row 1 unitarity",
                        f"{r['unitarity_row1']:.6f}",
                    )
                with rc3:
                    st.metric("ω_eff", f"{r['omega_eff']:.6f}")
                with rc4:
                    st.metric("Regime", f"{regime_color} {regime}")

                angles = r["triangle_angles"]
                st.markdown(
                    f"**Unitarity Triangle**: α = {angles['alpha_deg']:.1f}°, "
                    f"β = {angles['beta_deg']:.1f}°, "
                    f"γ = {angles['gamma_deg']:.1f}°"
                )

                # Triangle visualisation
                fig = go.Figure()
                fig.add_trace(
                    go.Scatter(
                        x=[0, 1, rho_bar, 0],
                        y=[0, 0, eta_bar, 0],
                        mode="lines+markers",
                        fill="toself",
                        fillcolor="rgba(0,123,255,0.1)",
                        line={"color": "#007bff", "width": 2},
                        marker={"size": 8},
                        name="Unitarity Triangle",
                    )
                )
                fig.add_annotation(x=0, y=-0.03, text="(0,0)", showarrow=False)
                fig.add_annotation(x=1, y=-0.03, text="(1,0)", showarrow=False)
                fig.add_annotation(
                    x=rho_bar,
                    y=eta_bar + 0.03,
                    text=f"(ρ̄,η̄)=({rho_bar:.3f},{eta_bar:.3f})",
                    showarrow=False,
                )
                fig.add_annotation(
                    x=rho_bar,
                    y=eta_bar * 0.7,
                    text=f"α={angles['alpha_deg']:.0f}°",
                    showarrow=False,
                )
                fig.add_annotation(
                    x=0.85,
                    y=0.03,
                    text=f"β={angles['beta_deg']:.0f}°",
                    showarrow=False,
                )
                fig.add_annotation(
                    x=0.15,
                    y=0.03,
                    text=f"γ={angles['gamma_deg']:.0f}°",
                    showarrow=False,
                )
                fig.update_layout(
                    title="CKM Unitarity Triangle",
                    xaxis_title="ρ̄",
                    yaxis_title="η̄",
                    xaxis={"range": [-0.1, 1.2]},
                    yaxis={"range": [-0.1, 0.5]},
                    height=400,
                    margin={"t": 40, "b": 20},
                    yaxis_scaleanchor="x",
                )
                st.plotly_chart(fig, use_container_width=True)

                # CKM heatmap
                fig2 = go.Figure(
                    go.Heatmap(
                        z=r["V_matrix"],
                        x=labels_c,
                        y=labels_r,
                        colorscale="Blues",
                        text=[[f"{v:.4f}" for v in row] for row in r["V_matrix"]],
                        texttemplate="%{text}",
                        textfont={"size": 14},
                        colorbar={"title": "|V_ij|"},
                    )
                )
                fig2.update_layout(
                    title="CKM Matrix Heatmap",
                    height=300,
                    margin={"t": 40, "b": 20},
                )
                st.plotly_chart(fig2, use_container_width=True)

            except Exception as e:
                st.error(f"Computation error: {e}")


# ═══════════════════════════════════════════════════════════════════════════════
# Materials Science Domain Page
# ═══════════════════════════════════════════════════════════════════════════════


def render_materials_science_page() -> None:
    """Render interactive Materials Science domain page with 8 closures + element database."""
    if st is None:
        return
    if go is None or pd is None or np is None:
        st.error(
            "Dashboard dependencies (plotly, pandas, numpy) are required for this page. Install with: `pip install plotly pandas numpy`"
        )
        return

    _ensure_closures_path()

    st.title("🧱 Materials Science Domain")
    st.caption(
        "MATL.INTSTACK.v1 — Cohesive energy, band structure, phase transitions, "
        "elastic moduli, Debye thermal, magnetism, superconductivity, surface catalysis"
    )

    with st.expander("📖 Domain Overview", expanded=False):
        st.markdown(
            """
        The **Materials Science** domain bridges atomic-scale observables into bulk
        material properties through the RCFT universality framework. Each closure
        derives independently from Axiom-0: collective material phases emerge as
        collapse of individual atomic observables into bulk structure.

        | Closure | Physics | Key Observable |
        |---------|---------|---------------|
        | Cohesive Energy | Madelung-Born-Mayer binding | E_coh (eV/atom) |
        | Band Structure | Bloch periodicity + RCFT gap | Band gap E_g (eV) |
        | Phase Transition | RCFT critical exponents | Order parameter φ(T) |
        | Elastic Moduli | Interatomic potential curvature | K, G, E (GPa) |
        | Debye Thermal | RCFT partition → Debye model | C_V, Θ_D (K) |
        | Magnetic Properties | Weiss field + RCFT β,γ | μ_eff, T_ordering |
        | BCS Superconductivity | RCFT partition condensation | T_c (K), Δ₀ (meV) |
        | Surface Catalysis | Broken-bond + d-band theory | γ (J/m²), E_ads |
        """
        )

    tab_names = [
        "⚡ Cohesive Energy",
        "📊 Band Structure",
        "🔥 Phase Transitions",
        "🔩 Elastic Moduli",
        "🌡️ Debye Thermal",
        "🧲 Magnetism",
        "❄️ Superconductivity",
        "🧪 Surface Catalysis",
    ]
    matl_tabs = st.tabs(tab_names)

    # ── Common element presets (symbol → Z) ──
    _ELEMENT_PRESETS: dict[str, tuple[str, int]] = {
        "Al – Aluminium": ("Al", 13),
        "Fe – Iron": ("Fe", 26),
        "Cu – Copper": ("Cu", 29),
        "Si – Silicon": ("Si", 14),
        "Au – Gold": ("Au", 79),
        "Ni – Nickel": ("Ni", 28),
        "Ti – Titanium": ("Ti", 22),
        "W – Tungsten": ("W", 74),
        "Ag – Silver": ("Ag", 47),
        "Nb – Niobium": ("Nb", 41),
        "Pb – Lead": ("Pb", 82),
        "C – Carbon": ("C", 6),
        "Cr – Chromium": ("Cr", 24),
        "Co – Cobalt": ("Co", 27),
    }

    # ── Tab 1: Cohesive Energy ─────────────────────────────────────
    with matl_tabs[0]:
        st.subheader("⚡ Cohesive Energy")
        st.markdown(
            "**Model**: Madelung-Born-Mayer (ionic), Wigner-Seitz (metallic), "
            "overlap integrals (covalent). Derives bulk binding from atomic potentials."
        )

        c1, _c2 = st.columns([1, 2])
        with c1:
            coh_preset = st.selectbox(
                "Element",
                list(_ELEMENT_PRESETS.keys()),
                key="matl_coh_preset",
                help="Select element for cohesive energy calc",
            )
        coh_sym, coh_Z = _ELEMENT_PRESETS.get(coh_preset, ("Fe", 26))

        if st.button("Compute Cohesive Energy", key="matl_coh_btn", type="primary"):
            try:
                from closures.materials_science.cohesive_energy import (
                    compute_cohesive_energy,
                )

                result = compute_cohesive_energy(coh_Z, symbol=coh_sym)
                r = result._asdict()
                regime = r["regime"]
                regime_icon = {"Strong_Bond": "🟢", "Moderate_Bond": "🟡", "Weak_Bond": "🟠"}.get(regime, "🔴")

                rc = st.columns(4)
                with rc[0]:
                    st.metric("E_coh predicted (eV)", f"{r['E_coh_eV']:.3f}")
                with rc[1]:
                    st.metric("E_coh measured (eV)", f"{r['E_coh_measured_eV']:.3f}")
                with rc[2]:
                    st.metric("ω_eff", f"{r['omega_eff']:.4f}")
                with rc[3]:
                    st.metric("Regime", f"{regime_icon} {regime}")

                mc = st.columns(4)
                with mc[0]:
                    st.metric("Bond Type", r["bond_type"])
                with mc[1]:
                    st.metric("Madelung α", f"{r['madelung_constant']:.4f}")
                with mc[2]:
                    st.metric("r₀ (Å)", f"{r['r0_A']:.3f}")
                with mc[3]:
                    st.metric("F_eff", f"{r['F_eff']:.4f}")

                # Batch scan for comparison
                from closures.materials_science.cohesive_energy import REFERENCE_COHESIVE
                from closures.materials_science.element_database import ELEMENTS_BY_SYMBOL

                if REFERENCE_COHESIVE:
                    batch_data = []
                    for sym in list(REFERENCE_COHESIVE.keys())[:20]:
                        try:
                            el = ELEMENTS_BY_SYMBOL.get(sym)
                            if el is None:
                                continue
                            br = compute_cohesive_energy(el.Z, symbol=sym)._asdict()
                            batch_data.append(
                                {
                                    "Element": sym,
                                    "E_coh_pred": br["E_coh_eV"],
                                    "E_coh_meas": br["E_coh_measured_eV"],
                                    "ω_eff": br["omega_eff"],
                                    "Bond": br["bond_type"],
                                    "Regime": br["regime"],
                                }
                            )
                        except Exception:
                            pass
                    if batch_data:
                        df_coh = pd.DataFrame(batch_data)
                        st.dataframe(df_coh, use_container_width=True, hide_index=True)

                        fig = go.Figure()
                        fig.add_trace(
                            go.Bar(
                                x=df_coh["Element"], y=df_coh["E_coh_pred"], name="Predicted", marker_color="#1f77b4"
                            )
                        )
                        fig.add_trace(
                            go.Bar(x=df_coh["Element"], y=df_coh["E_coh_meas"], name="Measured", marker_color="#ff7f0e")
                        )
                        fig.update_layout(
                            title="Cohesive Energy: Predicted vs Measured",
                            xaxis_title="Element",
                            yaxis_title="E_coh (eV/atom)",
                            barmode="group",
                            height=400,
                        )
                        st.plotly_chart(fig, use_container_width=True)
            except Exception as e:
                st.error(f"Cohesive energy error: {e}")

    # ── Tab 2: Band Structure ──────────────────────────────────────
    with matl_tabs[1]:
        st.subheader("📊 Band Structure")
        st.markdown(
            "**Model**: Electron config + Bloch periodicity → band gap. "
            "RCFT interpretation: gap = Fisher geodesic distance × energy scale."
        )

        c1, _c2 = st.columns([1, 2])
        with c1:
            band_preset = st.selectbox("Element", list(_ELEMENT_PRESETS.keys()), key="matl_band_preset")
        band_sym, band_Z = _ELEMENT_PRESETS.get(band_preset, ("Si", 14))

        if st.button("Compute Band Structure", key="matl_band_btn", type="primary"):
            try:
                from closures.materials_science.band_structure import (
                    compute_band_structure,
                )

                result = compute_band_structure(band_Z, symbol=band_sym)
                r = result._asdict()
                regime = r["regime"]
                regime_icon = {"Precise": "🟢", "Moderate": "🟡", "Approximate": "🟠"}.get(regime, "🔴")

                rc = st.columns(4)
                with rc[0]:
                    st.metric("E_g predicted (eV)", f"{r['E_g_eV']:.3f}")
                with rc[1]:
                    st.metric("E_g measured (eV)", f"{r['E_g_measured_eV']:.3f}")
                with rc[2]:
                    st.metric("Band Character", r["band_character"])
                with rc[3]:
                    st.metric("Regime", f"{regime_icon} {regime}")

                mc = st.columns(3)
                with mc[0]:
                    st.metric("ω_eff", f"{r['omega_eff']:.4f}")
                with mc[1]:
                    st.metric("F_eff", f"{r['F_eff']:.4f}")
                with mc[2]:
                    st.metric("RCFT Fisher distance", f"{r.get('rcft_fisher_distance', 0):.4f}")

                # Batch comparison
                from closures.materials_science.band_structure import REFERENCE_GAPS
                from closures.materials_science.element_database import ELEMENTS_BY_SYMBOL

                if REFERENCE_GAPS:
                    batch_data = []
                    for sym in list(REFERENCE_GAPS.keys())[:20]:
                        try:
                            el = ELEMENTS_BY_SYMBOL.get(sym)
                            if el is None:
                                continue
                            br = compute_band_structure(el.Z, symbol=sym)._asdict()
                            batch_data.append(
                                {
                                    "Element": sym,
                                    "E_g (eV)": br["E_g_eV"],
                                    "E_g meas (eV)": br["E_g_measured_eV"],
                                    "Character": br["band_character"],
                                    "ω_eff": br["omega_eff"],
                                    "Regime": br["regime"],
                                }
                            )
                        except Exception:
                            pass
                    if batch_data:
                        df_band = pd.DataFrame(batch_data)
                        st.dataframe(df_band, use_container_width=True, hide_index=True)

                        # Color by band character
                        char_colors = {
                            "Metal": "#1f77b4",
                            "Semimetal": "#2ca02c",
                            "Semiconductor": "#ff7f0e",
                            "Insulator": "#d62728",
                        }
                        fig = go.Figure()
                        for char, color in char_colors.items():
                            sub = df_band[df_band["Character"] == char]
                            if not sub.empty:
                                fig.add_trace(
                                    go.Bar(x=sub["Element"], y=sub["E_g (eV)"], name=char, marker_color=color)
                                )
                        fig.update_layout(
                            title="Band Gap by Element",
                            xaxis_title="Element",
                            yaxis_title="E_g (eV)",
                            height=400,
                        )
                        st.plotly_chart(fig, use_container_width=True)
            except Exception as e:
                st.error(f"Band structure error: {e}")

    # ── Tab 3: Phase Transitions ───────────────────────────────────
    with matl_tabs[2]:
        st.subheader("🔥 Phase Transitions")
        st.markdown(
            "**Model**: RCFT critical exponents (ν, γ, α, β) govern order parameter, "
            "susceptibility, and correlation length near T_c."
        )

        pt_presets = {
            "Custom": ("", 1043.0),
            "Fe (Curie)": ("Fe", 1043.0),
            "Ni (Curie)": ("Ni", 631.0),
            "Co (Curie)": ("Co", 1388.0),
            "Gd (Curie)": ("Gd", 292.5),
            "Cr (Néel)": ("Cr", 311.0),
            "MnO (Néel)": ("MnO", 116.0),
        }
        pt_sel = st.selectbox("Material preset", list(pt_presets.keys()), key="matl_pt_preset")
        pt_sym, pt_tc = pt_presets.get(pt_sel, ("", 1043.0))

        pt_cols = st.columns(3)
        with pt_cols[0]:
            pt_T = st.slider("Temperature T (K)", 1.0, 2000.0, pt_tc * 0.8, 1.0, key="matl_pt_T")
        with pt_cols[1]:
            pt_Tc = st.number_input("T_c (K)", 1.0, 5000.0, pt_tc, key="matl_pt_Tc")
        with pt_cols[2]:
            pt_type = st.selectbox(
                "Transition type", ["Magnetic", "Structural", "Superconducting", "Displacive"], key="matl_pt_type"
            )

        if st.button("Compute Phase Transition", key="matl_pt_btn", type="primary"):
            try:
                from closures.materials_science.phase_transition import (
                    compute_phase_transition,
                    scan_phase_diagram,
                )

                result = compute_phase_transition(pt_T, pt_Tc, material_key=pt_sym, transition_type=pt_type)
                r = result._asdict()
                regime = r["regime"]
                regime_icon = {"Ordered": "🟢", "Critical": "🟡", "Fluctuation": "🟠", "Disordered": "🔴"}.get(
                    regime, "⚪"
                )

                rc = st.columns(4)
                with rc[0]:
                    st.metric("Order Parameter φ", f"{r['order_parameter']:.4f}")
                with rc[1]:
                    st.metric("Susceptibility χ", f"{r['susceptibility']:.4f}")
                with rc[2]:
                    st.metric("ω_eff", f"{r['omega_eff']:.4f}")
                with rc[3]:
                    st.metric("Regime", f"{regime_icon} {regime}")

                mc = st.columns(4)
                with mc[0]:
                    st.metric("ν (corr. length)", f"{r['nu']:.4f}")
                with mc[1]:
                    st.metric("γ (suscept.)", f"{r['gamma']:.4f}")
                with mc[2]:
                    st.metric("β (order param.)", f"{r['beta_exp']:.4f}")
                with mc[3]:
                    st.metric("c_eff (RCFT)", f"{r['c_eff']:.4f}")

                # Phase diagram scan
                scan = scan_phase_diagram(pt_Tc, n_points=80, transition_type=pt_type)
                T_arr = [s.T_K for s in scan]
                phi_arr = [s.order_parameter for s in scan]
                chi_arr = [s.susceptibility for s in scan]
                omega_arr = [s.omega_eff for s in scan]

                fig = go.Figure()
                fig.add_trace(go.Scatter(x=T_arr, y=phi_arr, mode="lines", name="φ(T)", line={"width": 2}))
                fig.add_trace(
                    go.Scatter(
                        x=T_arr, y=chi_arr, mode="lines", name="χ(T)", yaxis="y2", line={"width": 2, "dash": "dash"}
                    )
                )
                fig.add_vline(x=pt_Tc, line_dash="dash", line_color="red", annotation_text="T_c")
                fig.update_layout(
                    title=f"Phase Diagram — T_c = {pt_Tc:.0f} K | {pt_type}",
                    xaxis_title="T (K)",
                    yaxis_title="Order Parameter φ",
                    yaxis2={"title": "Susceptibility χ", "overlaying": "y", "side": "right"},
                    height=400,
                )
                st.plotly_chart(fig, use_container_width=True)

                # ω trajectory
                fig2 = go.Figure()
                fig2.add_trace(
                    go.Scatter(
                        x=T_arr, y=omega_arr, mode="lines", name="ω_eff(T)", line={"color": "#d62728", "width": 2}
                    )
                )
                fig2.add_vline(x=pt_Tc, line_dash="dash", line_color="gray", annotation_text="T_c")
                fig2.update_layout(
                    title="Drift ω_eff vs Temperature",
                    xaxis_title="T (K)",
                    yaxis_title="ω_eff",
                    height=300,
                )
                st.plotly_chart(fig2, use_container_width=True)
            except Exception as e:
                st.error(f"Phase transition error: {e}")

    # ── Tab 4: Elastic Moduli ──────────────────────────────────────
    with matl_tabs[3]:
        st.subheader("🔩 Elastic Moduli")
        st.markdown(
            "**Model**: Interatomic potential curvature → bulk modulus K, shear modulus G, "
            "Young's modulus E. Voigt-Reuss-Hill averaging."
        )

        c1, _c2 = st.columns([1, 2])
        with c1:
            el_preset = st.selectbox("Element", list(_ELEMENT_PRESETS.keys()), key="matl_el_preset")
        el_sym, el_Z = _ELEMENT_PRESETS.get(el_preset, ("Fe", 26))

        if st.button("Compute Elastic Moduli", key="matl_el_btn", type="primary"):
            try:
                # Need cohesive energy first
                from closures.materials_science.cohesive_energy import (
                    compute_cohesive_energy,
                )
                from closures.materials_science.elastic_moduli import (
                    REFERENCE_K,
                    compute_elastic_moduli,
                )

                sym = el_sym if el_sym else "Fe"
                coh = compute_cohesive_energy(el_Z, symbol=sym)
                result = compute_elastic_moduli(coh.E_coh_eV, coh.r0_A, symbol=sym)
                r = result._asdict()
                regime = r["regime"]
                regime_icon = {"Stiff": "🟢", "Moderate": "🟡", "Compliant": "🟠"}.get(regime, "🔴")

                rc = st.columns(4)
                with rc[0]:
                    st.metric("K (GPa)", f"{r['K_GPa']:.1f}")
                with rc[1]:
                    st.metric("G (GPa)", f"{r['G_GPa']:.1f}")
                with rc[2]:
                    st.metric("E (GPa)", f"{r['E_GPa']:.1f}")
                with rc[3]:
                    st.metric("Regime", f"{regime_icon} {regime}")

                mc = st.columns(4)
                with mc[0]:
                    st.metric("ν (Poisson)", f"{r['nu_poisson']:.3f}")
                with mc[1]:
                    st.metric("K_meas (GPa)", f"{r['K_measured_GPa']:.1f}" if r["K_measured_GPa"] else "N/A")
                with mc[2]:
                    st.metric("ω_eff", f"{r['omega_eff']:.4f}")
                with mc[3]:
                    st.metric("F_eff", f"{r['F_eff']:.4f}")

                # Batch
                if REFERENCE_K:
                    from closures.materials_science.element_database import (
                        ELEMENTS_BY_SYMBOL as _EL_BY_SYM_EL,
                    )

                    batch_data = []
                    for sym_b in list(REFERENCE_K.keys())[:20]:
                        try:
                            el_db = _EL_BY_SYM_EL.get(sym_b)
                            if el_db is None:
                                continue
                            coh_b = compute_cohesive_energy(el_db.Z, symbol=sym_b)
                            el_b = compute_elastic_moduli(coh_b.E_coh_eV, coh_b.r0_A, symbol=sym_b)._asdict()
                            batch_data.append(
                                {
                                    "Element": sym_b,
                                    "K_pred (GPa)": el_b["K_GPa"],
                                    "K_meas (GPa)": el_b["K_measured_GPa"] or 0,
                                    "G (GPa)": el_b["G_GPa"],
                                    "E (GPa)": el_b["E_GPa"],
                                    "ω_eff": el_b["omega_eff"],
                                    "Regime": el_b["regime"],
                                }
                            )
                        except Exception:
                            pass
                    if batch_data:
                        df_el = pd.DataFrame(batch_data)
                        st.dataframe(df_el, use_container_width=True, hide_index=True)

                        fig = go.Figure()
                        fig.add_trace(
                            go.Bar(
                                x=df_el["Element"], y=df_el["K_pred (GPa)"], name="K predicted", marker_color="#1f77b4"
                            )
                        )
                        fig.add_trace(
                            go.Bar(
                                x=df_el["Element"], y=df_el["K_meas (GPa)"], name="K measured", marker_color="#ff7f0e"
                            )
                        )
                        fig.update_layout(
                            title="Bulk Modulus: Predicted vs Measured",
                            xaxis_title="Element",
                            yaxis_title="K (GPa)",
                            barmode="group",
                            height=400,
                        )
                        st.plotly_chart(fig, use_container_width=True)
            except Exception as e:
                st.error(f"Elastic moduli error: {e}")

    # ── Tab 5: Debye Thermal ───────────────────────────────────────
    with matl_tabs[4]:
        st.subheader("🌡️ Debye Thermal Properties")
        st.markdown(
            "**Model**: RCFT partition function → Debye model. "
            "Heat capacity C_V, thermal energy U, entropy S at temperature T."
        )

        deb_presets = {
            "Custom": ("", 300.0, 428.0),
            "Al": ("Al", 300.0, 428.0),
            "Fe": ("Fe", 300.0, 470.0),
            "Cu": ("Cu", 300.0, 343.0),
            "Au": ("Au", 300.0, 165.0),
            "Si": ("Si", 300.0, 645.0),
            "Nb": ("Nb", 300.0, 275.0),
            "W": ("W", 300.0, 400.0),
        }
        deb_sel = st.selectbox("Element preset", list(deb_presets.keys()), key="matl_deb_preset")
        deb_sym, deb_T, deb_Theta = deb_presets.get(deb_sel, ("", 300.0, 428.0))

        deb_cols = st.columns(2)
        with deb_cols[0]:
            deb_T_val = st.slider("Temperature T (K)", 1.0, 2000.0, deb_T, 1.0, key="matl_deb_T")
        with deb_cols[1]:
            deb_Theta_val = st.number_input("Θ_D (K)", 10.0, 3000.0, deb_Theta, key="matl_deb_Theta")

        if st.button("Compute Debye Thermal", key="matl_deb_btn", type="primary"):
            try:
                from closures.materials_science.debye_thermal import compute_debye_thermal

                result = compute_debye_thermal(deb_T_val, symbol=deb_sym if deb_sym else "", Theta_D_K=deb_Theta_val)
                r = result._asdict()
                regime = r["regime"]
                regime_icon = {"Quantum": "🔵", "Intermediate": "🟡", "Classical": "🟢"}.get(regime, "⚪")

                rc = st.columns(4)
                with rc[0]:
                    st.metric("C_V (J/mol·K)", f"{r['C_V_J_mol_K']:.3f}")
                with rc[1]:
                    st.metric("T/Θ_D", f"{r['T_over_Theta']:.3f}")
                with rc[2]:
                    st.metric("ω_eff", f"{r['omega_eff']:.4f}")
                with rc[3]:
                    st.metric("Regime", f"{regime_icon} {regime}")

                mc = st.columns(3)
                with mc[0]:
                    st.metric("U (J/mol)", f"{r['U_J_mol']:.1f}")
                with mc[1]:
                    st.metric("S (J/mol·K)", f"{r['S_J_mol_K']:.3f}")
                with mc[2]:
                    st.metric("v_sound (m/s)", f"{r['v_sound_ms']:.0f}")

                # Temperature scan
                T_scan = np.linspace(1.0, 2.0 * deb_Theta_val, 80)
                cv_data = []
                for T_i in T_scan:
                    try:
                        ri = compute_debye_thermal(float(T_i), Theta_D_K=deb_Theta_val)
                        cv_data.append(
                            {"T": float(T_i), "C_V": ri.C_V_J_mol_K, "ω_eff": ri.omega_eff, "Regime": ri.regime}
                        )
                    except Exception:
                        pass
                if cv_data:
                    df_cv = pd.DataFrame(cv_data)
                    fig = go.Figure()
                    fig.add_trace(
                        go.Scatter(
                            x=df_cv["T"],
                            y=df_cv["C_V"],
                            mode="lines",
                            name="C_V(T)",
                            line={"color": "#1f77b4", "width": 2},
                        )
                    )
                    fig.add_hline(y=24.94, line_dash="dash", line_color="gray", annotation_text="3R (Dulong-Petit)")
                    fig.add_vline(x=deb_Theta_val, line_dash="dash", line_color="red", annotation_text="Θ_D")
                    fig.update_layout(
                        title=f"Heat Capacity vs Temperature — Θ_D = {deb_Theta_val:.0f} K",
                        xaxis_title="T (K)",
                        yaxis_title="C_V (J/mol·K)",
                        height=400,
                    )
                    st.plotly_chart(fig, use_container_width=True)
            except Exception as e:
                st.error(f"Debye thermal error: {e}")

    # ── Tab 6: Magnetic Properties ─────────────────────────────────
    with matl_tabs[5]:
        st.subheader("🧲 Magnetic Properties")
        st.markdown("**Model**: Zeeman/Stark → bulk magnetism via Weiss molecular field + RCFT β,γ exponents.")

        mag_presets = {
            "Custom": (26, "Fe", 300.0),
            "Fe": (26, "Fe", 300.0),
            "Co": (27, "Co", 300.0),
            "Ni": (28, "Ni", 300.0),
            "Gd": (64, "Gd", 300.0),
            "Cr": (24, "Cr", 300.0),
            "Mn": (25, "Mn", 300.0),
        }
        mag_sel = st.selectbox("Element preset", list(mag_presets.keys()), key="matl_mag_preset")
        mag_Z, mag_sym, mag_T = mag_presets.get(mag_sel, (26, "Fe", 300.0))

        mag_cols = st.columns(3)
        with mag_cols[0]:
            mag_Z_val = st.number_input("Z", 1, 118, mag_Z, key="matl_mag_Z")
        with mag_cols[1]:
            mag_T_val = st.slider("Temperature (K)", 1.0, 2000.0, mag_T, 1.0, key="matl_mag_T")
        with mag_cols[2]:
            mag_B = st.slider("B field (T)", 0.0, 10.0, 0.0, 0.1, key="matl_mag_B")

        if st.button("Compute Magnetic Properties", key="matl_mag_btn", type="primary"):
            try:
                from closures.materials_science.magnetic_properties import (
                    compute_magnetic_properties,
                )

                result = compute_magnetic_properties(mag_Z_val, symbol=mag_sym, T_K=mag_T_val, B_tesla=mag_B)
                r = result._asdict()
                regime = r["regime"]
                regime_icon = {"Ordered": "🟢", "Moderate": "🟡", "Disordered": "🟠"}.get(regime, "🔴")

                rc = st.columns(4)
                with rc[0]:
                    st.metric("μ_eff (μ_B)", f"{r['mu_eff_B']:.3f}")
                with rc[1]:
                    st.metric("Magnetic Class", r["magnetic_class"])
                with rc[2]:
                    st.metric("T_ordering (K)", f"{r['T_ordering_K']:.1f}" if r["T_ordering_K"] else "N/A")
                with rc[3]:
                    st.metric("Regime", f"{regime_icon} {regime}")

                mc = st.columns(4)
                with mc[0]:
                    st.metric("M (μ_B)", f"{r['M_total_B']:.4f}")
                with mc[1]:
                    st.metric("χ_SI", f"{r['chi_SI']:.4e}")
                with mc[2]:
                    st.metric("ω_eff", f"{r['omega_eff']:.4f}")
                with mc[3]:
                    st.metric("F_eff", f"{r['F_eff']:.4f}")
            except Exception as e:
                st.error(f"Magnetic properties error: {e}")

    # ── Tab 7: Superconductivity ───────────────────────────────────
    with matl_tabs[6]:
        st.subheader("❄️ BCS Superconductivity")
        st.markdown(
            "**Model**: McMillan T_c from Debye temperature Θ_D and electron-phonon coupling λ_ep. "
            "BCS gap Δ₀, coherence length ξ₀, penetration depth λ_L."
        )

        sc_presets: dict[str, tuple[str, float, float]] = {
            "Custom": ("", 275.0, 0.82),
            "Nb": ("Nb", 275.0, 0.82),
            "Pb": ("Pb", 105.0, 1.55),
            "Al": ("Al", 428.0, 0.43),
            "Sn": ("Sn", 200.0, 0.72),
            "V": ("V", 380.0, 0.60),
            "MgB₂": ("MgB2", 700.0, 1.00),
        }
        sc_sel = st.selectbox("Material", list(sc_presets.keys()), key="matl_sc_preset")
        sc_sym, sc_Theta, sc_lambda = sc_presets.get(sc_sel, ("", 275.0, 0.82))

        sc_cols = st.columns(3)
        with sc_cols[0]:
            sc_Theta_val = st.number_input("Θ_D (K)", 10.0, 3000.0, sc_Theta, key="matl_sc_Theta")
        with sc_cols[1]:
            sc_lambda_val = st.slider("λ_ep", 0.1, 3.0, sc_lambda, 0.01, key="matl_sc_lambda")
        with sc_cols[2]:
            sc_mustar = st.slider("μ*", 0.05, 0.25, 0.13, 0.01, key="matl_sc_mustar")

        if st.button("Compute BCS", key="matl_sc_btn", type="primary"):
            try:
                from closures.materials_science.bcs_superconductivity import (
                    compute_bcs_superconductivity,
                )

                result = compute_bcs_superconductivity(
                    sc_Theta_val, sc_lambda_val, mu_star=sc_mustar, symbol=sc_sym if sc_sym else ""
                )
                r = result._asdict()
                regime = r["regime"]
                regime_icon = {"Precise": "🟢", "Moderate": "🟡", "Approximate": "🟠"}.get(regime, "🔴")

                rc = st.columns(4)
                with rc[0]:
                    st.metric("T_c predicted (K)", f"{r['T_c_K']:.3f}")
                with rc[1]:
                    st.metric("T_c measured (K)", f"{r['T_c_measured_K']:.3f}" if r["T_c_measured_K"] else "N/A")
                with rc[2]:
                    st.metric("SC Type", r["sc_type"])
                with rc[3]:
                    st.metric("Regime", f"{regime_icon} {regime}")

                mc = st.columns(4)
                with mc[0]:
                    st.metric("Δ₀ (meV)", f"{r['Delta_0_meV']:.3f}")
                with mc[1]:
                    st.metric("ξ₀ (nm)", f"{r['xi_0_nm']:.2f}")
                with mc[2]:
                    st.metric("λ_L (nm)", f"{r['lambda_L_nm']:.2f}")
                with mc[3]:
                    st.metric("κ_GL", f"{r['kappa_GL']:.3f}")

                ec = st.columns(3)
                with ec[0]:
                    st.metric("BCS ratio 2Δ₀/kT_c", f"{r['BCS_ratio']:.3f}")
                with ec[1]:
                    st.metric("ω_eff", f"{r['omega_eff']:.4f}")
                with ec[2]:
                    st.metric("F_eff", f"{r['F_eff']:.4f}")
            except Exception as e:
                st.error(f"BCS superconductivity error: {e}")

    # ── Tab 8: Surface Catalysis ───────────────────────────────────
    with matl_tabs[7]:
        st.subheader("🧪 Surface Catalysis")
        st.markdown(
            "**Model**: Broken-bond model for surface energy γ, d-band theory for adsorption, "
            "BEP (Brønsted-Evans-Polanyi) relation for barrier estimation."
        )

        c1, _c2 = st.columns([1, 2])
        with c1:
            surf_preset = st.selectbox("Element", list(_ELEMENT_PRESETS.keys()), key="matl_surf_preset")
        surf_sym, surf_Z = _ELEMENT_PRESETS.get(surf_preset, ("Fe", 26))

        if st.button("Compute Surface Catalysis", key="matl_surf_btn", type="primary"):
            try:
                from closures.materials_science.cohesive_energy import (
                    compute_cohesive_energy,
                )
                from closures.materials_science.surface_catalysis import (
                    REFERENCE_SURFACE,
                    compute_surface_catalysis,
                )

                sym = surf_sym if surf_sym else "Fe"
                coh = compute_cohesive_energy(surf_Z, symbol=sym)
                result = compute_surface_catalysis(coh.E_coh_eV, symbol=sym, r0_A=coh.r0_A)
                r = result._asdict()
                regime = r["regime"]
                regime_icon = {"Noble": "🟢", "Active": "🟡", "Reactive": "🟠"}.get(regime, "🔴")

                rc = st.columns(4)
                with rc[0]:
                    st.metric("γ (J/m²)", f"{r['gamma_J_m2']:.4f}")
                with rc[1]:
                    st.metric("Catalytic Class", r["catalytic_class"])
                with rc[2]:
                    st.metric("ω_eff", f"{r['omega_eff']:.4f}")
                with rc[3]:
                    st.metric("Regime", f"{regime_icon} {regime}")

                mc = st.columns(4)
                with mc[0]:
                    st.metric("E_ads (eV)", f"{r['E_ads_eV']:.3f}")
                with mc[1]:
                    st.metric("BEP barrier (eV)", f"{r['BEP_barrier_eV']:.3f}")
                with mc[2]:
                    st.metric("E_vacancy (eV)", f"{r['E_vacancy_eV']:.3f}")
                with mc[3]:
                    st.metric("d-band center (eV)", f"{r['d_band_center_eV']:.3f}" if r["d_band_center_eV"] else "N/A")

                # Volcano plot from reference data
                if REFERENCE_SURFACE:
                    from closures.materials_science.element_database import (
                        ELEMENTS_BY_SYMBOL as _EL_BY_SYM_SURF,
                    )

                    vol_data = []
                    for sym_v, _ref_v in list(REFERENCE_SURFACE.items())[:20]:
                        try:
                            el_v = _EL_BY_SYM_SURF.get(sym_v)
                            if el_v is None:
                                continue
                            coh_v = compute_cohesive_energy(el_v.Z, symbol=sym_v)
                            sr = compute_surface_catalysis(coh_v.E_coh_eV, symbol=sym_v, r0_A=coh_v.r0_A)._asdict()
                            vol_data.append(
                                {
                                    "Element": sym_v,
                                    "E_ads": sr["E_ads_eV"],
                                    "BEP_barrier": sr["BEP_barrier_eV"],
                                    "γ": sr["gamma_J_m2"],
                                    "Catalytic": sr["catalytic_class"],
                                }
                            )
                        except Exception:
                            pass
                    if vol_data:
                        df_vol = pd.DataFrame(vol_data)
                        fig = go.Figure()
                        fig.add_trace(
                            go.Scatter(
                                x=df_vol["E_ads"],
                                y=df_vol["BEP_barrier"],
                                mode="markers+text",
                                text=df_vol["Element"],
                                textposition="top center",
                                marker={
                                    "size": 10,
                                    "color": df_vol["γ"],
                                    "colorscale": "Viridis",
                                    "colorbar": {"title": "γ (J/m²)"},
                                },
                            )
                        )
                        fig.update_layout(
                            title="Volcano Plot: BEP Barrier vs Adsorption Energy",
                            xaxis_title="E_ads (eV)",
                            yaxis_title="BEP Barrier (eV)",
                            height=450,
                        )
                        st.plotly_chart(fig, use_container_width=True)
            except Exception as e:
                st.error(f"Surface catalysis error: {e}")


# ═══════════════════════════════════════════════════════════════════════════════
# Security Domain Page
# ═══════════════════════════════════════════════════════════════════════════════


def render_security_page() -> None:
    """Render interactive Security domain page with trust fidelity, threat classification, and more."""
    if st is None:
        return
    if go is None or pd is None or np is None:
        st.error(
            "Dashboard dependencies (plotly, pandas, numpy) are required for this page. Install with: `pip install plotly pandas numpy`"
        )
        return

    _ensure_closures_path()

    st.title("🛡️ Security Domain")
    st.caption(
        "SECURITY.INTSTACK.v1 — Trust fidelity, threat classification, anomaly return, "
        "behavior profiling, privacy audit, reputation analysis"
    )

    with st.expander("📖 Domain Overview", expanded=False):
        st.markdown(
            """
        The **Security** domain applies UMCP architecture to security validation.
        Axiom-0 translation: *"What survives validation is trusted."*

        | Tier | Component | Role |
        |------|-----------|------|
        | Tier-0 | Frozen security policy | Contracts, closures, frozen thresholds |
        | Tier-1 | Trust kernel | T, θ, H, D, σ, TIC, τ_A — deterministic |
        | Tier-2 | Diagnostics | Threat classification, reputation, privacy audit |

        **Tier-1 Invariants**:
        - **T** = Trust Fidelity (analog of F) — weighted security signals
        - **θ** = Threat Drift (analog of ω) — θ = 1 − T
        - **T + θ = 1** — duality identity holds exactly
        - **TIC** = Trust Integrity Composite (analog of IC)
        - **τ_A** = Anomaly Return Time (analog of τ_R)
        """
        )

    tab_names = [
        "🔒 Trust Fidelity",
        "⚠️ Threat Classifier",
        "📊 Security Validator",
        "📈 Anomaly Return",
        "👤 Behavior Profiler",
        "🔐 Privacy Auditor",
    ]
    sec_tabs = st.tabs(tab_names)

    # ── Tab 1: Trust Fidelity ──────────────────────────────────────
    with sec_tabs[0]:
        st.subheader("🔒 Trust Fidelity (Tier-1 Kernel)")
        st.markdown(
            "**T = Σ wᵢ · sᵢ** — weighted sum of security signals. "
            "θ = 1 − T (threat drift). Duality: T + θ = 1 exactly."
        )

        st.markdown("#### Configure Security Signals")
        sig_names = ["Authentication", "Encryption", "Access Control", "Network Integrity", "Behavior Score"]

        sig_cols = st.columns(len(sig_names))
        signals = []
        for i, name in enumerate(sig_names):
            with sig_cols[i]:
                s = st.slider(
                    name,
                    0.0,
                    1.0,
                    0.9 - i * 0.05,
                    0.01,
                    key=f"sec_sig_{i}",
                    help=f"{name} signal strength (0=fail, 1=pass)",
                )
                signals.append(s)

        st.markdown("#### Signal Weights")
        w_cols = st.columns(len(sig_names))
        weights_raw = []
        for i, name in enumerate(sig_names):
            with w_cols[i]:
                w = st.number_input(
                    f"w_{name[:4]}",
                    0.0,
                    1.0,
                    1.0 / len(sig_names),
                    0.01,
                    key=f"sec_w_{i}",
                    help=f"Weight for {name} signal",
                )
                weights_raw.append(w)

        if st.button("Compute Trust Fidelity", key="sec_tf_btn", type="primary"):
            try:
                from closures.security.trust_fidelity import (
                    classify_trust_status,
                    compute_trust_fidelity,
                )

                sig_arr = np.array(signals)
                w_arr = np.array(weights_raw)
                w_sum = w_arr.sum()
                if w_sum > 0:
                    w_arr = w_arr / w_sum  # Normalize

                result = compute_trust_fidelity(sig_arr, w_arr)
                T_val = result["T"]
                theta_val = result["theta"]
                status = classify_trust_status(T_val, 1)

                status_icons = {"TRUSTED": "🟢", "SUSPICIOUS": "🟡", "BLOCKED": "🔴", "NON_EVALUABLE": "⚪"}

                rc = st.columns(4)
                with rc[0]:
                    st.metric("T (Trust Fidelity)", f"{T_val:.4f}")
                with rc[1]:
                    st.metric("θ (Threat Drift)", f"{theta_val:.4f}")
                with rc[2]:
                    st.metric("T + θ", f"{T_val + theta_val:.6f}")
                with rc[3]:
                    st.metric("Status", f"{status_icons.get(status, '⚪')} {status}")

                # Per-signal contribution chart
                contribs = result["signal_contributions"]
                fig = go.Figure()
                fig.add_trace(
                    go.Bar(
                        x=sig_names,
                        y=contribs,
                        marker_color=["#2ca02c" if s > 0.7 else "#ff7f0e" if s > 0.4 else "#d62728" for s in signals],
                        text=[f"{c:.3f}" for c in contribs],
                        textposition="auto",
                    )
                )
                fig.update_layout(
                    title="Per-Signal Contribution to Trust Fidelity",
                    xaxis_title="Signal",
                    yaxis_title="w_i · s_i",
                    height=350,
                )
                st.plotly_chart(fig, use_container_width=True)

                # Gauge chart for T
                fig_gauge = go.Figure(
                    go.Indicator(
                        mode="gauge+number+delta",
                        value=T_val,
                        title={"text": "Trust Fidelity T"},
                        delta={"reference": 0.8, "increasing": {"color": "green"}, "decreasing": {"color": "red"}},
                        gauge={
                            "axis": {"range": [0, 1]},
                            "bar": {"color": "#1f77b4"},
                            "steps": [
                                {"range": [0, 0.4], "color": "#ffcccc"},
                                {"range": [0.4, 0.8], "color": "#ffffcc"},
                                {"range": [0.8, 1.0], "color": "#ccffcc"},
                            ],
                            "threshold": {"line": {"color": "red", "width": 4}, "thickness": 0.75, "value": 0.8},
                        },
                    )
                )
                fig_gauge.update_layout(height=300)
                st.plotly_chart(fig_gauge, use_container_width=True)
            except Exception as e:
                st.error(f"Trust fidelity error: {e}")

    # ── Tab 2: Threat Classifier ───────────────────────────────────
    with sec_tabs[1]:
        st.subheader("⚠️ Threat Classification (Tier-2 Diagnostic)")
        st.markdown(
            "Classifies security state using Tier-1 invariants (T, θ, H, D, σ, TIC, τ_A). "
            "Diagnostics inform but cannot override gates."
        )

        tc_cols = st.columns(4)
        with tc_cols[0]:
            tc_T = st.slider("T (Trust)", 0.0, 1.0, 0.85, 0.01, key="sec_tc_T")
        with tc_cols[1]:
            tc_H = st.slider("H (Entropy)", 0.0, 1.0, 0.3, 0.01, key="sec_tc_H")
        with tc_cols[2]:
            tc_D = st.slider("D (Deviation)", 0.0, 1.0, 0.1, 0.01, key="sec_tc_D")
        with tc_cols[3]:
            tc_sigma = st.slider("σ (Dispersion)", 0.0, 1.0, 0.15, 0.01, key="sec_tc_sigma")

        tc_cols2 = st.columns(3)
        with tc_cols2[0]:
            tc_TIC = st.slider("TIC", 0.0, 1.0, 0.75, 0.01, key="sec_tc_TIC")
        with tc_cols2[1]:
            tc_tau_A = st.number_input("τ_A", 0, 100, 2, key="sec_tc_tauA")
        with tc_cols2[2]:
            tc_hist_len = st.slider("T history length", 3, 20, 5, key="sec_tc_hist")

        if st.button("Classify Threat", key="sec_tc_btn", type="primary"):
            try:
                from closures.security.threat_classifier import classify_threat

                theta_val = 1.0 - tc_T
                T_history = [tc_T + np.random.normal(0, 0.02) for _ in range(tc_hist_len)]

                result = classify_threat(
                    T=tc_T,
                    theta=theta_val,
                    H=tc_H,
                    D=tc_D,
                    sigma=tc_sigma,
                    TIC=tc_TIC,
                    tau_A=tc_tau_A,
                    T_history=T_history,
                )

                threat_icons = {
                    "BENIGN": "🟢",
                    "TRANSIENT_ANOMALY": "🟡",
                    "PERSISTENT_THREAT": "🟠",
                    "ATTACK_IN_PROGRESS": "🔴",
                    "RECOVERY": "🔵",
                    "UNKNOWN": "⚪",
                }
                sev_icons = {"LOW": "🟢", "MEDIUM": "🟡", "HIGH": "🟠", "CRITICAL": "🔴"}

                rc = st.columns(4)
                with rc[0]:
                    tt = result.threat_type.name if hasattr(result.threat_type, "name") else str(result.threat_type)
                    st.metric("Threat Type", f"{threat_icons.get(tt, '⚪')} {tt}")
                with rc[1]:
                    st.metric("Confidence", f"{result.confidence:.3f}")
                with rc[2]:
                    sev = result.severity if isinstance(result.severity, str) else str(result.severity)
                    st.metric("Severity", f"{sev_icons.get(sev, '⚪')} {sev}")
                with rc[3]:
                    st.metric("Invariants Used", str(len(result.invariants_used)))

                if result.recommendations:
                    st.markdown("**Recommendations:**")
                    for rec in result.recommendations:
                        st.markdown(f"- {rec}")

                # Radar chart of invariants
                inv_names = ["T", "1−θ", "1−H", "1−D", "1−σ", "TIC"]
                inv_values = [tc_T, tc_T, 1 - tc_H, 1 - tc_D, 1 - tc_sigma, tc_TIC]
                inv_values.append(inv_values[0])  # Close polygon
                inv_names_closed = [*inv_names, inv_names[0]]

                fig = go.Figure()
                fig.add_trace(
                    go.Scatterpolar(
                        r=inv_values,
                        theta=inv_names_closed,
                        fill="toself",
                        fillcolor="rgba(31,119,180,0.2)",
                        line={"color": "#1f77b4", "width": 2},
                        name="Security State",
                    )
                )
                fig.update_layout(
                    polar={"radialaxis": {"visible": True, "range": [0, 1]}},
                    title="Security Invariants Radar",
                    height=400,
                )
                st.plotly_chart(fig, use_container_width=True)
            except Exception as e:
                st.error(f"Threat classification error: {e}")

    # ── Tab 3: Security Validator ──────────────────────────────────
    with sec_tabs[2]:
        st.subheader("📊 Full Security Validation")
        st.markdown("Orchestrates Tier-0 → Tier-1 → Tier-2 pipeline: frozen policy → trust kernel → threat diagnostic.")

        sv_cols = st.columns(5)
        with sv_cols[0]:
            sv_n = st.number_input("Number of signals", 3, 10, 5, key="sec_sv_n")
        with sv_cols[1]:
            sv_base = st.slider("Base signal value", 0.0, 1.0, 0.85, 0.01, key="sec_sv_base")
        with sv_cols[2]:
            sv_noise = st.slider("Signal noise σ", 0.0, 0.3, 0.05, 0.01, key="sec_sv_noise")
        with sv_cols[3]:
            sv_tau = st.number_input("τ_A", 0, 100, 3, key="sec_sv_tau")
        with sv_cols[4]:
            sv_hist = st.number_input("History length", 3, 50, 10, key="sec_sv_hist")

        if st.button("Run Full Validation", key="sec_sv_btn", type="primary"):
            try:
                from closures.security.trust_fidelity import (
                    classify_trust_status,
                    compute_trust_fidelity,
                )

                signals_arr = np.clip(np.random.normal(sv_base, sv_noise, sv_n), 0, 1)
                weights_arr = np.ones(sv_n) / sv_n

                result = compute_trust_fidelity(signals_arr, weights_arr)
                T_val = result["T"]
                status = classify_trust_status(T_val, sv_tau)

                st.markdown(f"### Result: **{status}**")

                rc = st.columns(3)
                with rc[0]:
                    st.metric("T", f"{T_val:.4f}")
                with rc[1]:
                    st.metric("θ", f"{result['theta']:.4f}")
                with rc[2]:
                    st.metric("Status", status)

                # Time-series simulation
                from closures.security.trust_fidelity import (
                    compute_trust_fidelity_series,
                )

                series = np.clip(np.random.normal(sv_base, sv_noise, (sv_hist, sv_n)), 0, 1)
                ts_results = compute_trust_fidelity_series(series, weights_arr)

                T_series = [r["T"] for r in ts_results]
                theta_series = [r["theta"] for r in ts_results]
                t_axis = list(range(1, sv_hist + 1))

                fig = go.Figure()
                fig.add_trace(
                    go.Scatter(
                        x=t_axis, y=T_series, mode="lines+markers", name="T(t)", line={"color": "#2ca02c", "width": 2}
                    )
                )
                fig.add_trace(
                    go.Scatter(
                        x=t_axis,
                        y=theta_series,
                        mode="lines+markers",
                        name="θ(t)",
                        line={"color": "#d62728", "width": 2},
                    )
                )
                fig.add_hline(y=0.8, line_dash="dash", line_color="green", annotation_text="Trusted threshold")
                fig.add_hline(y=0.4, line_dash="dash", line_color="orange", annotation_text="Suspicious threshold")
                fig.update_layout(
                    title="Trust/Threat Evolution Over Time",
                    xaxis_title="Time Step",
                    yaxis_title="Value",
                    height=400,
                )
                st.plotly_chart(fig, use_container_width=True)

                # Signal heatmap
                fig2 = go.Figure(
                    go.Heatmap(
                        z=series.T,
                        x=[f"t={t}" for t in t_axis],
                        y=[f"Signal {i + 1}" for i in range(sv_n)],
                        colorscale="RdYlGn",
                        zmin=0,
                        zmax=1,
                        colorbar={"title": "Signal Value"},
                    )
                )
                fig2.update_layout(
                    title="Signal Heatmap Over Time",
                    height=300,
                )
                st.plotly_chart(fig2, use_container_width=True)
            except Exception as e:
                st.error(f"Security validation error: {e}")

    # ── Tab 4: Anomaly Return ──────────────────────────────────────
    with sec_tabs[3]:
        st.subheader("📈 Anomaly Return (τ_A)")
        st.markdown(
            "Measures re-entry delay after anomaly detection. If τ_A = INF_ANOMALY, no trust credit is granted."
        )

        ar_cols = st.columns(3)
        with ar_cols[0]:
            ar_n = st.number_input("Series length", 10, 200, 50, key="sec_ar_n")
        with ar_cols[1]:
            ar_base = st.slider("Baseline T", 0.0, 1.0, 0.85, 0.01, key="sec_ar_base")
        with ar_cols[2]:
            ar_anomaly_at = st.slider("Anomaly at step", 5, 45, 20, key="sec_ar_anom")

        if st.button("Simulate Anomaly Return", key="sec_ar_btn", type="primary"):
            try:
                from closures.security.anomaly_return import (
                    compute_anomaly_return_series,
                    detect_anomaly_events,
                )

                # Generate synthetic multi-signal history with a dip
                n_signals = 5
                t_series_2d = np.ones((ar_n, n_signals)) * ar_base
                # Inject anomaly dip into all signals
                dip_start = min(ar_anomaly_at, ar_n - 5)
                dip_width = min(8, ar_n - dip_start)
                for si in range(n_signals):
                    t_series_2d[dip_start : dip_start + dip_width, si] = np.clip(
                        ar_base * 0.3 + np.linspace(0, ar_base * 0.7, dip_width), 0, 1
                    )

                # Compute τ_A for each timestep, then detect events
                tau_series = compute_anomaly_return_series(t_series_2d)
                events = detect_anomaly_events(tau_series)

                # Plot trust fidelity (mean across signals per timestep)
                t_mean = np.mean(t_series_2d, axis=1)
                fig = go.Figure()
                fig.add_trace(
                    go.Scatter(y=t_mean.tolist(), mode="lines", name="T̄(t)", line={"color": "#1f77b4", "width": 2})
                )
                fig.add_hline(y=ar_base * 0.7, line_dash="dash", line_color="red", annotation_text="Anomaly threshold")

                for ev in events:
                    ev_start = ev.get("start", 0)
                    ev_end = ev.get("end", ev_start + ev.get("duration", 1))
                    if ev_end is None:
                        ev_end = ar_n
                    fig.add_vrect(
                        x0=ev_start,
                        x1=ev_end,
                        fillcolor="red",
                        opacity=0.15,
                        line_width=0,
                    )

                fig.update_layout(
                    title="Trust Series with Anomaly Detection",
                    xaxis_title="Time Step",
                    yaxis_title="T̄",
                    height=400,
                )
                st.plotly_chart(fig, use_container_width=True)

                if events:
                    st.dataframe(pd.DataFrame(events), use_container_width=True, hide_index=True)
                else:
                    st.info("No anomaly events detected in this simulation.")
            except Exception as e:
                st.error(f"Anomaly return error: {e}")

    # ── Tab 5: Behavior Profiler ───────────────────────────────────
    with sec_tabs[4]:
        st.subheader("👤 Behavior Profiler")
        st.markdown(
            "Establishes baseline behavior profile and detects deviations. "
            "Trend analysis: STABLE, DECLINING, IMPROVING, VOLATILE."
        )

        bp_cols = st.columns(3)
        with bp_cols[0]:
            bp_n = st.number_input("Profile length", 10, 100, 30, key="sec_bp_n")
        with bp_cols[1]:
            bp_base = st.slider("Baseline", 0.0, 1.0, 0.85, 0.01, key="sec_bp_base")
        with bp_cols[2]:
            bp_drift = st.slider("Drift rate", -0.02, 0.02, 0.0, 0.001, key="sec_bp_drift")

        if st.button("Profile Behavior", key="sec_bp_btn", type="primary"):
            try:
                from closures.security.behavior_profiler import (
                    analyze_trend,
                    compute_baseline_profile,
                    compute_deviation,
                )

                # Simulate multi-signal behavioral data: shape (T, n_signals)
                n_sig = 5
                baseline_data = np.clip(
                    np.array(
                        [
                            [bp_base + bp_drift * i + np.random.normal(0, 0.03) for _ in range(n_sig)]
                            for i in range(bp_n)
                        ]
                    ),
                    0,
                    1,
                )

                # compute_baseline_profile takes ndarray shape (T, n)
                profile = compute_baseline_profile(baseline_data)

                # analyze_trend takes 1D ndarray, returns (BehaviorTrend, stats_dict)
                trust_series = np.mean(baseline_data, axis=1)
                trend, _trend_stats = analyze_trend(trust_series)

                trend_name = trend.value if hasattr(trend, "value") else str(trend)
                trend_icon = {
                    "STABLE": "🟢",
                    "DECLINING": "🔴",
                    "IMPROVING": "🟢",
                    "VOLATILE": "🟡",
                    "UNKNOWN": "⚪",
                }.get(trend_name, "⚪")

                rc = st.columns(4)
                with rc[0]:
                    mean_val = float(np.mean(profile.mean))
                    st.metric("Baseline Mean", f"{mean_val:.4f}")
                with rc[1]:
                    std_val = float(np.mean(profile.std))
                    st.metric("Baseline Std", f"{std_val:.4f}")
                with rc[2]:
                    st.metric("Trend", f"{trend_icon} {trend_name}")
                with rc[3]:
                    # compute_deviation takes (ndarray shape (n,), BehaviorProfile)
                    latest_dev = compute_deviation(baseline_data[-1], profile)
                    st.metric("Current Deviation", f"{latest_dev.deviation_score:.4f}")

                fig = go.Figure()
                fig.add_trace(
                    go.Scatter(
                        y=trust_series.tolist(),
                        mode="lines+markers",
                        name="Mean Trust Signal",
                        line={"width": 2},
                    )
                )
                fig.add_hline(y=mean_val, line_dash="dash", line_color="green", annotation_text="Baseline Mean")
                fig.add_hline(
                    y=mean_val - 2 * std_val,
                    line_dash="dot",
                    line_color="orange",
                    annotation_text="−2σ",
                )
                fig.add_hline(
                    y=mean_val + 2 * std_val,
                    line_dash="dot",
                    line_color="orange",
                    annotation_text="+2σ",
                )
                fig.update_layout(
                    title="Behavior Profile Over Time",
                    xaxis_title="Time Step",
                    yaxis_title="Behavior Score",
                    height=400,
                )
                st.plotly_chart(fig, use_container_width=True)
            except Exception as e:
                st.error(f"Behavior profiler error: {e}")

    # ── Tab 6: Privacy Auditor ─────────────────────────────────────
    with sec_tabs[5]:
        st.subheader("🔐 Privacy Auditor")
        st.markdown(
            "Detects PII (Personally Identifiable Information) and privacy violations. "
            "Severity levels: LOW, MEDIUM, HIGH, CRITICAL."
        )

        sample_texts = {
            "Clean text": "The weather forecast for tomorrow shows partly cloudy skies with temperatures around 72°F.",
            "Email + Phone": "Contact John Doe at john.doe@email.com or call 555-123-4567 for details.",
            "SSN + Address": "SSN: 123-45-6789. Address: 123 Main St, Springfield, IL 62704.",
            "Credit Card": "Payment: Visa 4111-1111-1111-1111, exp 12/25, CVV 123.",
            "Mixed PII": "Patient Jane Smith (DOB: 03/15/1990, SSN: 987-65-4321) visited on 2024-01-15.",
        }
        pa_sel = st.selectbox("Sample text", list(sample_texts.keys()), key="sec_pa_sample")
        pa_text = st.text_area("Text to audit", sample_texts.get(pa_sel, ""), height=100, key="sec_pa_text")

        if st.button("Audit Privacy", key="sec_pa_btn", type="primary"):
            try:
                from closures.security.privacy_auditor import detect_pii

                pii_findings = detect_pii(pa_text)

                if pii_findings:
                    sev_counts: dict[str, int] = {}
                    pii_data = []
                    for finding in pii_findings:
                        # PIIMatch is a dataclass — use vars() for dict conversion
                        f_dict = {
                            "pii_type": finding.pii_type,
                            "value_masked": finding.value_masked,
                            "location": finding.location,
                            "severity": finding.severity.value
                            if hasattr(finding.severity, "value")
                            else str(finding.severity),
                        }
                        pii_data.append(f_dict)
                        sev_str = f_dict["severity"]
                        sev_counts[sev_str] = sev_counts.get(sev_str, 0) + 1

                    st.warning(f"⚠️ Found {len(pii_findings)} PII instance(s)")

                    rc = st.columns(4)
                    for i, (sev, cnt) in enumerate(sev_counts.items()):
                        with rc[i % 4]:
                            st.metric(sev, cnt)

                    st.dataframe(pd.DataFrame(pii_data), use_container_width=True, hide_index=True)

                    # Severity distribution pie chart
                    if sev_counts:
                        sev_colors = {
                            "LOW": "#2ca02c",
                            "MODERATE": "#ff7f0e",
                            "HIGH": "#d62728",
                            "CRITICAL": "#7b2d8e",
                        }
                        fig = go.Figure(
                            go.Pie(
                                labels=list(sev_counts.keys()),
                                values=list(sev_counts.values()),
                                marker={"colors": [sev_colors.get(s, "#999") for s in sev_counts]},
                                hole=0.4,
                            )
                        )
                        fig.update_layout(title="PII Severity Distribution", height=350)
                        st.plotly_chart(fig, use_container_width=True)
                else:
                    st.success("✅ No PII detected — text is clean.")
            except Exception as e:
                st.error(f"Privacy audit error: {e}")
