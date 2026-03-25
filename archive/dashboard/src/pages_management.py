"""
Management dashboard pages: Notifications, Bookmarks, API Integration.
"""
# pyright: reportUnknownMemberType=false
# pyright: reportUnknownVariableType=false
# pyright: reportUnknownArgumentType=false
# pyright: reportOptionalMemberAccess=false
# pyright: reportMissingTypeStubs=false

from __future__ import annotations

import json
from datetime import datetime

from umcp.dashboard._deps import pd, st
from umcp.dashboard._utils import (
    classify_regime,
    detect_anomalies,
    load_ledger,
)


def render_notifications_page() -> None:
    """Render the notification and alerts page."""
    if st is None:
        return

    st.title("🔔 Notifications & Alerts")
    st.caption("Configure alerts for regime changes and anomalies")

    # Initialize notification settings
    if "notifications" not in st.session_state:
        st.session_state.notifications = {
            "enabled": True,
            "regime_change": True,
            "anomaly_detected": True,
            "validation_failed": True,
            "threshold_omega_low": 0.1,
            "threshold_omega_high": 0.9,
            "alert_log": [],
        }

    # ========== Alert Configuration ==========
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("⚙️ Alert Settings")

        with st.container(border=True):
            st.session_state.notifications["enabled"] = st.toggle(
                "Enable Notifications",
                value=st.session_state.notifications["enabled"],
                help="Master switch for all alert types",
            )

            st.markdown("**Alert Types:**")
            st.session_state.notifications["regime_change"] = st.checkbox(
                "🌡️ Regime Changes",
                value=st.session_state.notifications["regime_change"],
                help="Alert when regime transitions (STABLE→WATCH, WATCH→COLLAPSE, etc.)",
            )
            st.session_state.notifications["anomaly_detected"] = st.checkbox(
                "⚠️ Anomaly Detection",
                value=st.session_state.notifications["anomaly_detected"],
                help="Alert when statistical anomalies are detected",
            )
            st.session_state.notifications["validation_failed"] = st.checkbox(
                "❌ Validation Failures",
                value=st.session_state.notifications["validation_failed"],
                help="Alert when validation returns NONCONFORMANT",
            )

            st.markdown("**Thresholds:**")
            st.session_state.notifications["threshold_omega_low"] = st.slider(
                "ω Low Threshold (COLLAPSE)",
                0.0,
                0.3,
                st.session_state.notifications["threshold_omega_low"],
                0.01,
                help="Alert when ω drops below this value",
            )
            st.session_state.notifications["threshold_omega_high"] = st.slider(
                "ω High Threshold (COLLAPSE)",
                0.7,
                1.0,
                st.session_state.notifications["threshold_omega_high"],
                0.01,
                help="Alert when ω exceeds this value",
            )

    with col2:
        st.subheader("🔍 Current State Check")

        if st.button("🔄 Check for Alerts Now", use_container_width=True):
            df = load_ledger()
            alerts = []

            if not df.empty:
                latest = df.iloc[-1]

                # Check omega thresholds
                if "omega" in df.columns:
                    omega = latest["omega"]
                    low_thresh = st.session_state.notifications["threshold_omega_low"]
                    high_thresh = st.session_state.notifications["threshold_omega_high"]

                    if omega < low_thresh:
                        alerts.append(
                            {
                                "type": "CRITICAL",
                                "message": f"ω below threshold: {omega:.4f} < {low_thresh}",
                                "timestamp": datetime.now().isoformat(),
                            }
                        )
                    elif omega > high_thresh:
                        alerts.append(
                            {
                                "type": "CRITICAL",
                                "message": f"ω above threshold: {omega:.4f} > {high_thresh}",
                                "timestamp": datetime.now().isoformat(),
                            }
                        )

                # Check regime transitions
                if len(df) >= 2 and "omega" in df.columns:
                    prev = df.iloc[-2]
                    current_regime = classify_regime(latest.get("omega", 0.5), latest.get("seam_residual", 0))
                    prev_regime = classify_regime(prev.get("omega", 0.5), prev.get("seam_residual", 0))

                    if current_regime != prev_regime:
                        alerts.append(
                            {
                                "type": "WARNING",
                                "message": f"Regime changed: {prev_regime} → {current_regime}",
                                "timestamp": datetime.now().isoformat(),
                            }
                        )

                # Check validation status
                if "run_status" in df.columns and latest["run_status"] == "NONCONFORMANT":
                    alerts.append(
                        {
                            "type": "ERROR",
                            "message": "Latest validation NONCONFORMANT",
                            "timestamp": datetime.now().isoformat(),
                        }
                    )

                # Anomaly check
                if "omega" in df.columns and len(df) > 5:
                    anomalies = detect_anomalies(df["omega"])
                    if anomalies.iloc[-1]:
                        alerts.append(
                            {
                                "type": "WARNING",
                                "message": f"Statistical anomaly detected in ω: {latest['omega']:.4f}",
                                "timestamp": datetime.now().isoformat(),
                            }
                        )

            # Display and log alerts
            if alerts:
                st.session_state.notifications["alert_log"].extend(alerts)
                for alert in alerts:
                    if alert["type"] == "CRITICAL":
                        st.error(f"🚨 **CRITICAL:** {alert['message']}")
                    elif alert["type"] == "ERROR":
                        st.error(f"❌ **ERROR:** {alert['message']}")
                    elif alert["type"] == "WARNING":
                        st.warning(f"⚠️ **WARNING:** {alert['message']}")
                    else:
                        st.info(f"ℹ️ **INFO:** {alert['message']}")
            else:
                st.success("✅ No alerts - system operating normally")

    # ========== Alert Log ==========
    st.divider()
    st.subheader("📜 Alert History")

    alert_log = st.session_state.notifications.get("alert_log", [])
    if alert_log:
        # Show last 20 alerts
        for alert in reversed(alert_log[-20:]):
            icon = (
                "🚨"
                if alert["type"] == "CRITICAL"
                else "⚠️"
                if alert["type"] == "WARNING"
                else "❌"
                if alert["type"] == "ERROR"
                else "ℹ️"
            )
            st.markdown(f"{icon} **{alert['type']}** — {alert['message']} @ {alert['timestamp'][:19]}")

        if st.button("🗑️ Clear Alert History"):
            st.session_state.notifications["alert_log"] = []
            st.rerun()
    else:
        st.info("No alerts recorded yet.")


def render_bookmarks_page() -> None:
    """Render the bookmarks page for saving interesting states."""
    if st is None or pd is None:
        return

    st.title("🔖 Bookmarks")
    st.caption("Save and revisit interesting states and configurations")

    # Initialize bookmarks
    if "bookmarks" not in st.session_state:
        st.session_state.bookmarks = []

    # ========== Add Bookmark ==========
    st.subheader("➕ Save Current State")

    with st.form("add_bookmark"):
        col1, col2 = st.columns(2)

        with col1:
            bookmark_name = st.text_input(
                "Bookmark Name", placeholder="e.g., 'Stable regime baseline'", help="Short descriptive name"
            )
            bookmark_type = st.selectbox(
                "Bookmark Type",
                ["Ledger Snapshot", "Configuration", "Audit Run", "Custom Note"],
                help="What kind of state to capture",
            )

        with col2:
            bookmark_tags = st.text_input("Tags (comma-separated)", placeholder="stable, baseline, v1.5")
            bookmark_notes = st.text_area("Notes", placeholder="Add any notes about this bookmark...")

        submitted = st.form_submit_button("🔖 Save Bookmark", use_container_width=True)

        if submitted and bookmark_name:
            # Capture current state
            df = load_ledger()
            snapshot = {}

            if bookmark_type == "Ledger Snapshot" and not df.empty:
                latest = df.iloc[-1].to_dict()
                # Convert numpy/pandas types to native Python
                snapshot = {
                    k: (float(v) if hasattr(v, "item") else str(v) if hasattr(v, "isoformat") else v)
                    for k, v in latest.items()
                    if pd.notna(v)
                }
            elif bookmark_type == "Audit Run" and "audit_log" in st.session_state and st.session_state.audit_log:
                snapshot = st.session_state.audit_log[-1]
            elif bookmark_type == "Configuration":
                snapshot = {
                    "auto_refresh": st.session_state.get("auto_refresh", False),
                    "refresh_interval": st.session_state.get("refresh_interval", 30),
                    "show_advanced": st.session_state.get("show_advanced", False),
                    "compact_mode": st.session_state.get("compact_mode", False),
                    "theme": st.session_state.get("theme", "Default"),
                }

            bookmark = {
                "id": len(st.session_state.bookmarks) + 1,
                "name": bookmark_name,
                "type": bookmark_type,
                "tags": [t.strip() for t in bookmark_tags.split(",") if t.strip()],
                "notes": bookmark_notes,
                "snapshot": snapshot,
                "created_at": datetime.now().isoformat(),
            }

            st.session_state.bookmarks.append(bookmark)
            st.success(f"✅ Bookmark '{bookmark_name}' saved!")
            st.rerun()

    st.divider()

    # ========== View Bookmarks ==========
    st.subheader("📚 Saved Bookmarks")

    if not st.session_state.bookmarks:
        st.info("No bookmarks saved yet. Create your first bookmark above!")
    else:
        # Filter by type
        types = list({b["type"] for b in st.session_state.bookmarks})
        type_filter = st.selectbox("Filter by Type", ["All", *types], help="Show only this bookmark type")

        filtered = st.session_state.bookmarks
        if type_filter != "All":
            filtered = [b for b in filtered if b["type"] == type_filter]

        # Display bookmarks
        for _i, bookmark in enumerate(reversed(filtered)):
            with st.expander(f"🔖 {bookmark['name']} ({bookmark['type']}) — {bookmark['created_at'][:10]}"):
                col1, col2 = st.columns([3, 1])

                with col1:
                    if bookmark["tags"]:
                        st.markdown("**Tags:** " + ", ".join([f"`{t}`" for t in bookmark["tags"]]))
                    if bookmark["notes"]:
                        st.markdown(f"**Notes:** {bookmark['notes']}")

                    st.markdown("**Snapshot:**")
                    st.json(bookmark["snapshot"])

                with col2:
                    if st.button("🗑️ Delete", key=f"del_bm_{bookmark['id']}"):
                        st.session_state.bookmarks = [
                            b for b in st.session_state.bookmarks if b["id"] != bookmark["id"]
                        ]
                        st.rerun()

                    # Export single bookmark
                    st.download_button(
                        label="📥 Export",
                        data=json.dumps(bookmark, indent=2, default=str),
                        file_name=f"bookmark_{bookmark['id']}.json",
                        mime="application/json",
                        key=f"export_bm_{bookmark['id']}",
                    )

        # Export all bookmarks
        st.divider()
        col1, col2 = st.columns(2)
        with col1:
            st.download_button(
                label="📥 Export All Bookmarks",
                data=json.dumps(st.session_state.bookmarks, indent=2, default=str),
                file_name=f"umcp_bookmarks_{datetime.now().strftime('%Y%m%d')}.json",
                mime="application/json",
                use_container_width=True,
            )
        with col2:
            if st.button("🗑️ Clear All Bookmarks", use_container_width=True):
                st.session_state.bookmarks = []
                st.rerun()


# ============================================================================
# Medium-term Expansions - Time Series, Custom Formulas, Batch, API
# ============================================================================


def render_api_integration_page() -> None:
    """Render the API integration page with endpoint reference, example payloads, and live testing."""
    if st is None:
        return

    st.title("🔌 API Integration")
    st.caption("64 REST endpoints · Kernel computation · Domain closures · Live testing")

    # Initialize API settings
    if "api_settings" not in st.session_state:
        st.session_state.api_settings = {
            "url": "http://localhost:8000",
            "connected": False,
            "last_sync": None,
            "auto_sync": False,
        }

    # ========== Quick Reference ==========
    st.markdown("""
    The UMCP REST API exposes the full kernel, validation engine, and all 18 domain
    closures over HTTP. Start it with:

    ```bash
    uvicorn umcp.api_umcp:app --reload --host 0.0.0.0 --port 8000
    ```

    **OpenAPI docs**: `http://localhost:8000/docs` (Swagger UI) ·
    `http://localhost:8000/redoc` (ReDoc)

    **Auth**: Read/compute endpoints are public. Admin endpoints require
    `X-API-Key` header (set `UMCP_ADMIN_KEY` env var). Use `UMCP_DEV_MODE=1` for development.
    """)

    st.divider()

    # ========== Connection Settings ==========
    st.subheader("⚙️ Connection")

    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        api_url = st.text_input(
            "API URL",
            value=st.session_state.api_settings["url"],
            placeholder="http://localhost:8000",
            help="Base URL of the UMCP REST API",
        )
        st.session_state.api_settings["url"] = api_url
    with col2:
        if st.button("🔗 Test Connection", use_container_width=True):
            try:
                import urllib.error
                import urllib.request

                with urllib.request.urlopen(f"{api_url}/health", timeout=5) as response:
                    data = json.loads(response.read().decode())
                    st.session_state.api_settings["connected"] = True
                    st.success(f"✅ Connected! Status: {data.get('status', 'OK')}")
            except urllib.error.URLError as e:
                st.session_state.api_settings["connected"] = False
                st.error(f"❌ Connection failed: {e.reason}")
            except Exception as e:
                st.session_state.api_settings["connected"] = False
                st.error(f"❌ Error: {e}")
    with col3:
        status = "🟢 Connected" if st.session_state.api_settings["connected"] else "🔴 Disconnected"
        st.markdown(f"**{status}**")

    st.divider()

    # ========== Endpoint Reference ==========
    st.subheader("📡 Endpoint Reference (64 endpoints)")

    endpoint_groups = {
        "System": [
            ("GET", "/health", "System health, metrics, domain count"),
            ("GET", "/version", "API and validator version info"),
            ("GET", "/metrics", "Operational metrics and request stats"),
        ],
        "Kernel (Core)": [
            ("POST", "/kernel/compute", "Compute kernel invariants (F, ω, S, C, κ, IC)"),
            ("POST", "/kernel/batch", "Batch kernel computation (multiple traces)"),
            ("POST", "/kernel/budget", "Verify seam budget identity (Γ, D_C, Δκ)"),
            ("POST", "/kernel/spine", "Full spine evaluation (Contract → Stance)"),
        ],
        "Validation": [
            ("POST", "/validate", "Validate a casepack or repository"),
            ("GET", "/casepacks", "List available casepacks"),
            ("GET", "/casepacks/{id}", "Get casepack details"),
            ("POST", "/casepacks/{id}/run", "Run a casepack validation"),
        ],
        "Ledger & Contracts": [
            ("GET", "/ledger", "Query the return log ledger"),
            ("GET", "/contracts", "List available contracts"),
            ("GET", "/closures", "List registered closures"),
        ],
        "Analysis": [
            ("POST", "/regime/classify", "Classify regime from invariants"),
            ("POST", "/analysis/timeseries", "Time series analysis of traces"),
            ("POST", "/analysis/statistics", "Statistical summary of traces"),
            ("POST", "/analysis/correlation", "Cross-channel correlation analysis"),
            ("GET", "/analysis/ledger", "Ledger analytics and trends"),
        ],
        "Conversion": [
            ("POST", "/convert/measurements", "Unit conversion (SI aware)"),
            ("POST", "/convert/embed", "Embed raw values into [0,1] trace"),
        ],
        "Uncertainty": [
            ("POST", "/uncertainty/propagate", "Propagate measurement uncertainty"),
        ],
        "Calculator": [
            ("POST", "/calculate", "Universal kernel calculator"),
        ],
        "Outputs": [
            ("GET", "/badge/status.svg", "Status badge (SVG)"),
            ("GET", "/badge/regime.svg", "Regime badge (SVG)"),
            ("GET", "/output/ascii/gauge", "ASCII gauge visualization"),
            ("GET", "/output/ascii/sparkline", "ASCII sparkline of ω history"),
            ("GET", "/output/markdown/report", "Markdown validation report"),
            ("GET", "/output/mermaid/regime", "Mermaid regime diagram"),
            ("GET", "/output/html/card", "HTML card widget"),
            ("GET", "/output/latex/invariants", "LaTeX invariant equations"),
            ("GET", "/output/junit", "JUnit XML test report"),
            ("GET", "/output/jsonld", "JSON-LD linked data output"),
        ],
        "Standard Model": [
            ("GET", "/sm/particles", "31-particle catalog with kernel data"),
            ("GET", "/sm/theorems", "10 proven theorems (74/74 subtests)"),
        ],
        "Domains": [
            ("GET", "/domains", "List all 18 UMCP domains with metadata"),
            ("GET", "/canon", "Canon anchors across all domains"),
            ("GET", "/canon/{domain}", "Domain-specific canon anchors"),
            ("GET", "/atomic/elements", "118-element periodic kernel data"),
            ("GET", "/evolution/organisms", "40-organism evolution kernel"),
            ("POST", "/finance/embed", "Finance portfolio embedding"),
        ],
        "Astronomy": [
            ("POST", "/astro/luminosity", "Stellar luminosity closure"),
            ("POST", "/astro/distance", "Distance modulus closure"),
            ("POST", "/astro/spectral", "Spectral classification"),
            ("POST", "/astro/evolution", "Stellar evolution closure"),
            ("POST", "/astro/orbital", "Orbital mechanics closure"),
            ("POST", "/astro/dynamics", "Galactic dynamics closure"),
        ],
        "Nuclear Physics": [
            ("POST", "/nuclear/binding", "Bethe-Weizsäcker binding energy"),
            ("POST", "/nuclear/alpha-decay", "Alpha decay closure"),
            ("POST", "/nuclear/shell", "Nuclear shell model"),
            ("POST", "/nuclear/fissility", "Fissility parameter"),
            ("POST", "/nuclear/decay-chain", "Decay chain analysis"),
            ("POST", "/nuclear/double-sided", "Double-sided nuclear analysis"),
        ],
        "Quantum Mechanics": [
            ("POST", "/qm/collapse", "Wavefunction collapse closure"),
            ("POST", "/qm/entanglement", "Entanglement closure"),
            ("POST", "/qm/tunneling", "Tunneling closure"),
            ("POST", "/qm/harmonic-oscillator", "Harmonic oscillator closure"),
            ("POST", "/qm/spin", "Spin measurement closure"),
            ("POST", "/qm/uncertainty", "Uncertainty relation closure"),
        ],
        "WEYL Cosmology": [
            ("GET", "/weyl/background", "FLRW background cosmology"),
            ("GET", "/weyl/sigma", "σ₈ clustering amplitude"),
            ("GET", "/weyl/des-y3", "DES Year 3 data"),
            ("GET", "/weyl/umcp-mapping", "WEYL-to-UMCP mapping"),
        ],
    }

    if pd is not None:
        for group_name, endpoints in endpoint_groups.items():
            with st.expander(f"**{group_name}** ({len(endpoints)} endpoints)", expanded=False):
                rows = [{"Method": m, "Path": p, "Description": d} for m, p, d in endpoints]
                st.dataframe(
                    pd.DataFrame(rows),
                    use_container_width=True,
                    hide_index=True,
                    column_config={
                        "Method": st.column_config.TextColumn(width="small"),
                        "Path": st.column_config.TextColumn(width="medium"),
                    },
                )
    else:
        for group_name, endpoints in endpoint_groups.items():
            with st.expander(f"**{group_name}** ({len(endpoints)})", expanded=False):
                for method, path, desc in endpoints:
                    st.markdown(f"- **{method}** `{path}` — {desc}")

    st.divider()

    # ========== Example Payloads ==========
    st.subheader("📋 Example Payloads")

    example_tabs = st.tabs(
        [
            "Kernel Compute",
            "Batch Compute",
            "Spine Evaluation",
            "Regime Classify",
            "Validate",
        ]
    )

    with example_tabs[0]:
        st.markdown("**POST `/kernel/compute`** — Compute kernel invariants from a trace vector")
        st.code(
            """{
    "coordinates": [0.85, 0.72, 0.91, 0.68, 0.77, 0.83],
    "weights": [0.167, 0.167, 0.167, 0.167, 0.166, 0.166],
    "epsilon": 1e-8
}""",
            language="json",
        )
        st.markdown("**Response:**")
        st.code(
            """{
    "F": 0.793333,
    "omega": 0.206667,
    "S": 0.389012,
    "C": 0.148533,
    "kappa": -0.247821,
    "IC": 0.780512,
    "heterogeneity_gap": 0.012821,
    "regime": "WATCH",
    "identities": {
        "duality_residual": 0.0,
        "integrity_bound_holds": true,
        "log_integrity_residual": 0.0
    }
}""",
            language="json",
        )

    with example_tabs[1]:
        st.markdown("**POST `/kernel/batch`** — Multiple trace vectors in one call")
        st.code(
            """{
    "traces": [
        {"coordinates": [0.95, 0.92, 0.97, 0.91], "weights": [0.25, 0.25, 0.25, 0.25]},
        {"coordinates": [0.45, 0.42, 0.48, 0.40], "weights": [0.25, 0.25, 0.25, 0.25]},
        {"coordinates": [0.12, 0.08, 0.15, 0.05], "weights": [0.25, 0.25, 0.25, 0.25]}
    ],
    "epsilon": 1e-8
}""",
            language="json",
        )
        st.markdown("Returns an array of kernel outputs — one per trace.")

    with example_tabs[2]:
        st.markdown("**POST `/kernel/spine`** — Full spine traversal (Contract → Stance)")
        st.code(
            """{
    "coordinates": [0.85, 0.72, 0.91, 0.68],
    "weights": [0.25, 0.25, 0.25, 0.25],
    "contract": {
        "epsilon": 1e-8,
        "p_exponent": 3,
        "alpha": 1.0,
        "tol_seam": 0.005
    }
}""",
            language="json",
        )
        st.markdown(
            "Returns all five spine stops: contract echo, kernel invariants, "
            "regime gates (4 individual checks), seam budget (Γ, D_C, Δκ), and final stance."
        )

    with example_tabs[3]:
        st.markdown("**POST `/regime/classify`** — Classify regime from pre-computed invariants")
        st.code(
            """{
    "omega": 0.15,
    "F": 0.85,
    "S": 0.42,
    "C": 0.28
}""",
            language="json",
        )
        st.markdown("**Response:**")
        st.code(
            """{
    "regime": "WATCH",
    "gates": {
        "omega_gate": false,
        "F_gate": false,
        "S_gate": false,
        "C_gate": false
    },
    "critical": false,
    "classification_reason": "omega in [0.038, 0.30)"
}""",
            language="json",
        )

    with example_tabs[4]:
        st.markdown("**POST `/validate`** — Validate a casepack")
        st.code(
            """{
    "target": "casepacks/hello_world",
    "strict": false,
    "verbose": false
}""",
            language="json",
        )
        st.markdown("**Response:**")
        st.code(
            """{
    "run_status": "CONFORMANT",
    "target_path": "casepacks/hello_world",
    "summary": {
        "counts": {"errors": 0, "warnings": 0, "targets_total": 1}
    },
    "timestamp": "2026-03-12T10:42:00Z"
}""",
            language="json",
        )

    st.divider()

    # ========== Live Testing ==========
    st.subheader("🧪 Live Endpoint Testing")

    if not st.session_state.api_settings["connected"]:
        st.warning("Connect to the API above to test endpoints live.")
    else:
        tabs = st.tabs(["🏥 Health", "📒 Ledger", "📦 Casepacks", "✅ Validate", "⚙️ Kernel"])

        with tabs[0]:
            st.markdown("### Health Check")
            if st.button("🔄 Fetch Health", key="api_health"):
                try:
                    import urllib.request

                    with urllib.request.urlopen(f"{api_url}/health", timeout=5) as response:
                        data = json.loads(response.read().decode())
                        st.json(data)
                except Exception as e:
                    st.error(f"❌ Error: {e}")

        with tabs[1]:
            st.markdown("### Ledger Data")
            limit = st.slider("Limit", 5, 100, 20, key="api_ledger_limit", help="Max ledger rows to fetch")
            if st.button("🔄 Fetch Ledger", key="api_ledger"):
                try:
                    import urllib.request

                    with urllib.request.urlopen(f"{api_url}/ledger?limit={limit}", timeout=10) as response:
                        data = json.loads(response.read().decode())
                        if isinstance(data, list) and pd is not None:
                            df = pd.DataFrame(data)
                            st.dataframe(df, use_container_width=True)
                        else:
                            st.json(data)
                except Exception as e:
                    st.error(f"❌ Error: {e}")

        with tabs[2]:
            st.markdown("### Casepacks")
            if st.button("🔄 Fetch Casepacks", key="api_casepacks"):
                try:
                    import urllib.request

                    with urllib.request.urlopen(f"{api_url}/casepacks", timeout=10) as response:
                        data = json.loads(response.read().decode())
                        st.json(data)
                except Exception as e:
                    st.error(f"❌ Error: {e}")

        with tabs[3]:
            st.markdown("### Validate via API")
            target = st.text_input("Target Path", value=".", key="api_validate_target")
            if st.button("🚀 Validate", key="api_validate"):
                try:
                    import urllib.request

                    req_data = json.dumps({"target": target}).encode()
                    req = urllib.request.Request(
                        f"{api_url}/validate",
                        data=req_data,
                        headers={"Content-Type": "application/json"},
                        method="POST",
                    )

                    with urllib.request.urlopen(req, timeout=60) as response:
                        data = json.loads(response.read().decode())

                        if data.get("run_status") == "CONFORMANT":
                            st.success("✅ CONFORMANT")
                        else:
                            st.error("❌ NONCONFORMANT")

                        st.json(data)
                except Exception as e:
                    st.error(f"❌ Error: {e}")

        with tabs[4]:
            st.markdown("### Kernel Compute")
            kernel_input = st.text_area(
                "Request Body (JSON)",
                value='{\n    "coordinates": [0.85, 0.72, 0.91, 0.68],\n    "weights": [0.25, 0.25, 0.25, 0.25]\n}',
                height=120,
                key="api_kernel_input",
            )
            if st.button("⚙️ Compute Kernel", key="api_kernel_compute"):
                try:
                    import urllib.request

                    req_data = kernel_input.encode()
                    req = urllib.request.Request(
                        f"{api_url}/kernel/compute",
                        data=req_data,
                        headers={"Content-Type": "application/json"},
                        method="POST",
                    )

                    with urllib.request.urlopen(req, timeout=10) as response:
                        data = json.loads(response.read().decode())
                        st.json(data)
                except json.JSONDecodeError:
                    st.error("❌ Invalid JSON in request body")
                except Exception as e:
                    st.error(f"❌ Error: {e}")

    st.divider()

    # ========== Auto-Sync ==========
    st.subheader("🔄 Auto-Sync")

    st.session_state.api_settings["auto_sync"] = st.toggle(
        "Enable Auto-Sync",
        value=st.session_state.api_settings["auto_sync"],
        help="Automatically sync data from API at regular intervals",
    )

    if st.session_state.api_settings["auto_sync"]:
        sync_interval = st.slider("Sync Interval (seconds)", 10, 120, 30)
        st.info(f"💡 Auto-sync will fetch data every {sync_interval} seconds when enabled.")

        if st.session_state.api_settings.get("last_sync"):
            st.caption(f"Last sync: {st.session_state.api_settings['last_sync']}")


# ============================================================================
# Precision Verification Page
# ============================================================================
