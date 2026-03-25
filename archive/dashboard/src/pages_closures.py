"""
UMCP Dashboard — Closure Explorer

Dedicated page for exploring all 15 domain closure families as interactive,
clickable cards. Each domain expands to show every closure with its full
schematic (input → processing → output), docstring, source code, and
spine-position metadata.

Cross-references:
  - closures/registry.yaml (canonical closure list)
  - closures/__init__.py (CLOSURE_DOMAINS constant)
  - src/umcp/dashboard/_utils.py (load_closures helper)
  - KERNEL_SPECIFICATION.md (Tier-1 identities referenced by closures)
"""

from __future__ import annotations

import ast
import textwrap
from pathlib import Path
from typing import Any

from umcp.dashboard._deps import go, st
from umcp.dashboard._utils import (
    format_bytes,
    load_closures,
)

# ── Domain metadata ──────────────────────────────────────────────────────────
# Each domain carries its icon, full name, description, tier, and contract.

DOMAIN_META: dict[str, dict[str, str]] = {
    "GCD": {
        "icon": "🌀",
        "name": "Generative Collapse Dynamics",
        "description": "Core GCD closures: energy potentials, entropic collapse, generative flux, field resonance, momentum flux.",
        "tier": "Tier-2",
        "contract": "GCD.INTSTACK.v1",
        "dir": "gcd",
    },
    "RCFT": {
        "icon": "🔁",
        "name": "Recursive Collapse Field Theory",
        "description": "Fractal dimension, recursive field strength, resonance patterns, attractor basins, active matter, coherence pipelines.",
        "tier": "Tier-2",
        "contract": "RCFT.INTSTACK.v1",
        "dir": "rcft",
    },
    "KIN": {
        "icon": "🏃",
        "name": "Kinematics",
        "description": "Linear & rotational kinematics, energy mechanics, momentum dynamics, phase-space return, kinematic stability.",
        "tier": "Tier-2",
        "contract": "KIN.INTSTACK.v1",
        "dir": "kinematics",
    },
    "WEYL": {
        "icon": "🌌",
        "name": "WEYL Cosmology",
        "description": "Modified gravity: transfer functions, Limber integrals, beyond-Limber corrections, Σ-evolution, boost factors.",
        "tier": "Tier-2",
        "contract": "WEYL.INTSTACK.v1",
        "dir": "weyl",
    },
    "SECURITY": {
        "icon": "🛡️",
        "name": "Security",
        "description": "Trust fidelity, security entropy, trust integrity, anomaly return, threat classification, behavior profiling, privacy audit.",
        "tier": "Tier-2",
        "contract": "SECURITY.INTSTACK.v1",
        "dir": "security",
    },
    "ASTRO": {
        "icon": "🔭",
        "name": "Astronomy",
        "description": "Stellar luminosity, orbital mechanics, spectral analysis, distance ladder, gravitational dynamics, stellar evolution, cosmology.",
        "tier": "Tier-2",
        "contract": "ASTRO.INTSTACK.v1",
        "dir": "astronomy",
    },
    "NUC": {
        "icon": "☢️",
        "name": "Nuclear Physics",
        "description": "Nuclide binding energy, alpha decay, decay chains, fissility, shell structure, double-sided collapse, periodic table.",
        "tier": "Tier-2",
        "contract": "NUC.INTSTACK.v1",
        "dir": "nuclear_physics",
    },
    "QM": {
        "icon": "🔮",
        "name": "Quantum Mechanics",
        "description": "Wavefunction collapse, entanglement, tunneling, harmonic oscillator, spin measurement, uncertainty, TERS near-field, atom-dot.",
        "tier": "Tier-2",
        "contract": "QM.INTSTACK.v1",
        "dir": "quantum_mechanics",
    },
    "FIN": {
        "icon": "💰",
        "name": "Finance",
        "description": "Financial metric embedding: revenue, expenses, margin, cashflow mapped to [0,1]⁴ trace vectors.",
        "tier": "Tier-2",
        "contract": "FINANCE.INTSTACK.v1",
        "dir": "finance",
    },
    "ATOM": {
        "icon": "⚛️",
        "name": "Atomic Physics",
        "description": "118-element periodic kernel, cross-scale nuclear-atomic bridge, ionization energy, spectral lines, Tier-1 proof (10,162 tests).",
        "tier": "Tier-2",
        "contract": "ATOM.INTSTACK.v1",
        "dir": "atomic_physics",
    },
    "MAT": {
        "icon": "🧱",
        "name": "Materials Science",
        "description": "Cohesive energy, phase transitions, elastic moduli, band structure, thermal properties, BCS superconductivity, surface catalysis, 3 databases.",
        "tier": "Tier-2",
        "contract": "MAT.INTSTACK.v1",
        "dir": "materials_science",
    },
    "SM": {
        "icon": "🔬",
        "name": "Standard Model",
        "description": "31-particle subatomic kernel (17 fundamental + 14 composite), 10 proven theorems, CKM/PMNS mixing, running couplings, EWSB.",
        "tier": "Tier-2",
        "contract": "SM.INTSTACK.v1",
        "dir": "standard_model",
    },
    "EVERYDAY": {
        "icon": "🌡️",
        "name": "Everyday Physics",
        "description": "Thermodynamics, electromagnetism, optics, wave phenomena — everyday physics mapped through the kernel.",
        "tier": "Tier-2",
        "contract": "EVERYDAY.INTSTACK.v1",
        "dir": "everyday_physics",
    },
    "EVO": {
        "icon": "🧬",
        "name": "Evolution",
        "description": "40-organism evolution kernel, 10-channel brain kernel, recursive evolution, Axiom-0 instantiation map, deep implications.",
        "tier": "Tier-2",
        "contract": "EVO.INTSTACK.v1",
        "dir": "evolution",
    },
}


# ── Helpers ──────────────────────────────────────────────────────────────────


def _parse_closure_detail(path_str: str) -> dict[str, Any]:
    """Extract detailed metadata from a closure file (docstring, functions, inputs/outputs)."""
    path = Path(path_str)
    detail: dict[str, Any] = {
        "docstring": "",
        "functions": [],
        "imports": [],
    }
    if not path.exists() or path.suffix != ".py":
        return detail

    try:
        source = path.read_text(encoding="utf-8", errors="replace")
        tree = ast.parse(source)
    except (SyntaxError, ValueError):
        return detail

    # Module docstring
    doc = ast.get_docstring(tree)
    if doc:
        detail["docstring"] = doc

    # Public functions with signatures & docstrings
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and not node.name.startswith("_"):
            args = []
            for arg in node.args.args:
                args.append(arg.arg)
            fn_doc = ast.get_docstring(node) or ""
            # Extract return annotation if present
            returns = ""
            if node.returns:
                returns = ast.dump(node.returns)
            detail["functions"].append(
                {
                    "name": node.name,
                    "args": args,
                    "docstring": fn_doc,
                    "line": node.lineno,
                    "returns": returns,
                }
            )

    return detail


def _build_spine_diagram(closure_name: str, inputs: list[str], outputs: list[str]) -> str:
    """Build an ASCII schematic showing the closure's spine position."""
    inp_str = ", ".join(inputs[:6]) if inputs else "raw data"
    if len(inputs) > 6:
        inp_str += f" (+{len(inputs) - 6})"
    out_str = ", ".join(outputs[:6]) if outputs else "invariants"
    if len(outputs) > 6:
        out_str += f" (+{len(outputs) - 6})"

    return textwrap.dedent(f"""\
    ┌─────────────┐     ┌──────────────────┐     ┌───────────────┐     ┌─────────────────┐     ┌────────┐
    │  CONTRACT    │────▶│  CANON           │────▶│  THIS CLOSURE │────▶│ INTEGRITY       │────▶│ STANCE │
    │  (freeze)    │     │  (5 words)       │     │  {closure_name:<13s} │     │ LEDGER          │     │ (read) │
    └─────────────┘     └──────────────────┘     └───────────────┘     └─────────────────┘     └────────┘
                                                   ▲                     │
                                                   │  inputs:            │  outputs:
                                                   │  {inp_str:<20s}     │  {out_str:<20s}
    """)


def _render_domain_card(
    domain_key: str,
    meta: dict[str, str],
    closures_in_domain: list[dict[str, Any]],
) -> None:
    """Render a single domain as an expandable card with all its closures."""
    if st is None:
        return

    py_count = sum(1 for c in closures_in_domain if c["type"] == "python")
    yaml_count = sum(1 for c in closures_in_domain if c["type"] == "yaml")
    total_lines = sum(c.get("lines", 0) for c in closures_in_domain)
    total_size = sum(c.get("size_bytes", 0) for c in closures_in_domain)

    # Domain-level card
    header_label = f"{meta['icon']} {meta['name']}  —  {len(closures_in_domain)} closures"
    with st.expander(header_label, expanded=False):
        # Domain summary bar
        st.markdown(f"*{meta['description']}*")

        mcol1, mcol2, mcol3, mcol4, mcol5 = st.columns(5)
        with mcol1:
            st.metric("🐍 Python", py_count)
        with mcol2:
            st.metric("📄 YAML", yaml_count)
        with mcol3:
            st.metric("📏 Lines", f"{total_lines:,}")
        with mcol4:
            st.metric("💾 Size", format_bytes(total_size))
        with mcol5:
            st.metric("📜 Contract", meta.get("contract", "—"))

        st.divider()

        # Tier & contract info
        st.markdown(
            f"**Tier**: {meta['tier']}  ·  **Contract**: `{meta.get('contract', 'N/A')}`  ·  "
            f"**Directory**: `closures/{meta['dir']}/`"
        )

        st.divider()

        # ── Individual closures ──────────────────────────────────────────
        for closure in closures_in_domain:
            emoji = "🐍" if closure["type"] == "python" else "📄"
            cl_label = f"{emoji}  **{closure['name']}**"

            with st.container(border=True):
                # Header row
                hcol1, hcol2, hcol3 = st.columns([3, 1, 1])
                with hcol1:
                    st.markdown(cl_label)
                with hcol2:
                    st.caption(f"{closure.get('lines', 0):,} lines")
                with hcol3:
                    st.caption(format_bytes(closure.get("size_bytes", 0)))

                # Parse details for Python files
                if closure["type"] == "python":
                    detail = _parse_closure_detail(closure["path"])

                    # Docstring
                    if detail["docstring"]:
                        doc_text = detail["docstring"]
                        if len(doc_text) > 600:
                            doc_text = doc_text[:600] + "…"
                        st.markdown(f"> {doc_text}")

                    # Function signatures (the public API of the closure)
                    if detail["functions"]:
                        st.markdown("**Public Functions:**")
                        for fn in detail["functions"]:
                            args_str = ", ".join(fn["args"])
                            st.code(
                                f"def {fn['name']}({args_str})  # line {fn['line']}",
                                language="python",
                            )
                            if fn["docstring"]:
                                fn_doc = fn["docstring"]
                                if len(fn_doc) > 400:
                                    fn_doc = fn_doc[:400] + "…"
                                st.caption(fn_doc)

                    # Schematic: inputs → closure → outputs
                    if detail["functions"]:
                        main_fn = detail["functions"][0]
                        inputs = [a for a in main_fn["args"] if a != "self"]
                        # Infer outputs from function name
                        st.markdown("**Spine Position (Contract → … → Stance):**")
                        short_name = closure["name"][:13]
                        diagram = _build_spine_diagram(short_name, inputs, [])
                        st.code(diagram, language="text")

                # Full source code (collapsed)
                with st.expander(f"📝 Full Source — {closure['name']}", expanded=False):
                    try:
                        content = Path(closure["path"]).read_text(encoding="utf-8", errors="replace")
                        lang = "python" if closure["type"] == "python" else "yaml"
                        st.code(content, language=lang, line_numbers=True)
                    except Exception as e:
                        st.error(f"Could not read: {e}")


# ── Distribution chart ───────────────────────────────────────────────────────


def _render_distribution_chart(
    domain_counts: dict[str, int],
    domain_lines: dict[str, int],
) -> None:
    """Render a bar chart showing closure counts and lines per domain."""
    if st is None or go is None:
        return

    domains = list(domain_counts.keys())
    counts = [domain_counts[d] for d in domains]
    lines = [domain_lines[d] for d in domains]
    icons = [DOMAIN_META.get(d, {}).get("icon", "📁") for d in domains]
    names = [DOMAIN_META.get(d, {}).get("name", d) for d in domains]
    labels = [f"{ic} {nm}" for ic, nm in zip(icons, names, strict=True)]

    tab1, tab2 = st.tabs(["📊 Closure Count", "📏 Lines of Code"])

    with tab1:
        fig_count = go.Figure(
            data=[
                go.Bar(
                    x=labels,
                    y=counts,
                    marker_color=[
                        "#4CAF50",
                        "#2196F3",
                        "#FF9800",
                        "#9C27B0",
                        "#F44336",
                        "#00BCD4",
                        "#795548",
                        "#E91E63",
                        "#FFEB3B",
                        "#3F51B5",
                        "#8BC34A",
                        "#FF5722",
                        "#607D8B",
                        "#009688",
                    ][: len(domains)],
                    text=counts,
                    textposition="auto",
                )
            ]
        )
        fig_count.update_layout(
            title="Closures per Domain",
            xaxis_title="Domain",
            yaxis_title="Number of Closures",
            height=420,
            margin={"l": 40, "r": 20, "t": 50, "b": 100},
            xaxis_tickangle=-45,
        )
        st.plotly_chart(fig_count, use_container_width=True)

    with tab2:
        fig_lines = go.Figure(
            data=[
                go.Bar(
                    x=labels,
                    y=lines,
                    marker_color=[
                        "#4CAF50",
                        "#2196F3",
                        "#FF9800",
                        "#9C27B0",
                        "#F44336",
                        "#00BCD4",
                        "#795548",
                        "#E91E63",
                        "#FFEB3B",
                        "#3F51B5",
                        "#8BC34A",
                        "#FF5722",
                        "#607D8B",
                        "#009688",
                    ][: len(domains)],
                    text=[f"{ln:,}" for ln in lines],
                    textposition="auto",
                )
            ]
        )
        fig_lines.update_layout(
            title="Lines of Code per Domain",
            xaxis_title="Domain",
            yaxis_title="Lines",
            height=420,
            margin={"l": 40, "r": 20, "t": 50, "b": 100},
            xaxis_tickangle=-45,
        )
        st.plotly_chart(fig_lines, use_container_width=True)


# ── Main page renderer ──────────────────────────────────────────────────────


def render_closure_explorer_page() -> None:
    """Render the full Closure Explorer page — all 15 domains as clickable cards."""
    if st is None:
        return

    st.title("🗂️ Closure Explorer")
    st.caption(
        "All 15 domain closure families  ·  Click any domain to expand  ·  "
        "Full schematics, source code, and spine position for every closure"
    )

    # Load all closures
    closures = load_closures()
    if not closures:
        st.warning("No closures found in `closures/` directory.")
        return

    # Group by domain
    domain_groups: dict[str, list[dict[str, Any]]] = {}
    for c in closures:
        d = c.get("domain", "unknown")
        domain_groups.setdefault(d, []).append(c)

    # ══════════════════════════════════════════════════════════════════════
    #  Summary metrics
    # ══════════════════════════════════════════════════════════════════════
    with st.container(border=True):
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.metric("🌐 Domains", len(domain_groups))
        with col2:
            st.metric("📦 Total Closures", len(closures))
        with col3:
            py_total = sum(1 for c in closures if c["type"] == "python")
            st.metric("🐍 Python", py_total)
        with col4:
            yaml_total = sum(1 for c in closures if c["type"] == "yaml")
            st.metric("📄 YAML", yaml_total)
        with col5:
            total_lines = sum(c.get("lines", 0) for c in closures)
            st.metric("📏 Total Lines", f"{total_lines:,}")

    st.divider()

    # ══════════════════════════════════════════════════════════════════════
    #  The Spine — context for all closures
    # ══════════════════════════════════════════════════════════════════════
    with st.expander("📖 Where Closures Sit in the Spine", expanded=False):
        st.markdown(
            r"""
Every closure occupies the **third stop** of the five-stop spine:

```
CONTRACT → CANON → CLOSURES → INTEGRITY LEDGER → STANCE
(freeze)   (tell)   (publish)   (reconcile)        (read)
```

**Closures** are Tier-2 expansions: they map domain-specific data into
the Tier-1 kernel invariants (F, ω, S, C, κ, IC). They are validated
**through** Tier-0 **against** Tier-1. Each closure publishes thresholds
and their order; no mid-episode edits. Stance *must* change when
thresholds are crossed.

The data flow for any single closure is:

```
Raw Domain Data → [Normalization to [ε, 1-ε]ⁿ] → Trace Vector c
    → Kernel(c, w) → { F, ω, S, C, κ, IC }
    → Regime Gates → Stance (Stable / Watch / Collapse)
```
"""
        )

    st.divider()

    # ══════════════════════════════════════════════════════════════════════
    #  Distribution charts
    # ══════════════════════════════════════════════════════════════════════
    domain_counts = {d: len(cls) for d, cls in domain_groups.items()}
    domain_lines = {d: sum(c.get("lines", 0) for c in cls) for d, cls in domain_groups.items()}

    _render_distribution_chart(domain_counts, domain_lines)

    st.divider()

    # ══════════════════════════════════════════════════════════════════════
    #  Filters
    # ══════════════════════════════════════════════════════════════════════
    fcol1, fcol2 = st.columns(2)
    with fcol1:
        # Domain filter
        domain_options = ["All Domains", *sorted(domain_groups.keys())]
        domain_filter: str = (
            st.selectbox(
                "Filter by Domain",
                domain_options,
                help="Show closures for a specific domain",
            )
            or "All Domains"
        )
    with fcol2:
        search_term = st.text_input(
            "Search closures",
            placeholder="Type to filter by name…",
            help="Filters across all domains",
        )

    st.divider()

    # ══════════════════════════════════════════════════════════════════════
    #  Domain cards — ordered by DOMAIN_META then remaining
    # ══════════════════════════════════════════════════════════════════════
    # Canonical order: iterate DOMAIN_META first, then any unknown domains
    ordered_domains: list[str] = []
    for key in DOMAIN_META:
        if key in domain_groups:
            ordered_domains.append(key)
    for key in sorted(domain_groups.keys()):
        if key not in ordered_domains:
            ordered_domains.append(key)

    rendered_count = 0
    for dkey in ordered_domains:
        if domain_filter != "All Domains" and dkey != domain_filter:
            continue

        group = domain_groups[dkey]

        # Apply search filter within domain
        if search_term:
            group = [c for c in group if search_term.lower() in c["name"].lower()]
            if not group:
                continue

        meta = DOMAIN_META.get(
            dkey,
            {
                "icon": "📁",
                "name": dkey,
                "description": f"Closures in the {dkey} domain.",
                "tier": "Tier-2",
                "contract": "—",
                "dir": dkey.lower(),
            },
        )

        _render_domain_card(dkey, meta, group)
        rendered_count += 1

    if rendered_count == 0:
        st.info("No closures match the current filters.")
