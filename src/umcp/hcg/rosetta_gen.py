"""
Rosetta Markdown Generator — Math → Constrained Prose via Lenses.

Reads kernel invariants (F, ω, S, C, κ, IC) and regime classification,
then generates prose-first markdown using the Quinque Verba (five words)
mapped through the Rosetta lens system.

The words are programmatically tethered to the math — no external LLM
prompt-drift.  The prose returns to the contract.

Usage:
    from umcp.hcg.rosetta_gen import generate_domain_markdown
    from umcp.hcg.extractor import extract_domain_data

    data = extract_domain_data("finance")
    md = generate_domain_markdown(data, lens="Policy")
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from umcp.hcg.extractor import KernelSnapshot, SiteData


# ---------------------------------------------------------------------------
# Rosetta lens table — maps the five words across 6 lenses
# ---------------------------------------------------------------------------

ROSETTA_LENSES: dict[str, dict[str, str]] = {
    "Epistemology": {
        "drift": "Change in belief or evidence",
        "fidelity": "Retained warrant",
        "roughness": "Inference friction",
        "return": "Justified re-entry",
        "integrity": "Coherence of the epistemic position",
    },
    "Ontology": {
        "drift": "State transition",
        "fidelity": "Conserved properties",
        "roughness": "Heterogeneity at interface seams",
        "return": "Restored coherence",
        "integrity": "Structural persistence under change",
    },
    "Phenomenology": {
        "drift": "Perceived shift",
        "fidelity": "Stable features",
        "roughness": "Distress, bias, or effort",
        "return": "Coping or repair that holds",
        "integrity": "Experiential coherence",
    },
    "History": {
        "drift": "Periodization — what shifted",
        "fidelity": "Continuity — what endures",
        "roughness": "Rupture or confound",
        "return": "Restitution or reconciliation",
        "integrity": "Narrative coherence across epochs",
    },
    "Policy": {
        "drift": "Regime shift",
        "fidelity": "Compliance and mandate persistence",
        "roughness": "Friction, cost, or externality",
        "return": "Reinstatement or acceptance",
        "integrity": "Institutional coherence",
    },
    "Semiotics": {
        "drift": "Sign drift — departure from referent",
        "fidelity": "Ground persistence — convention that survived",
        "roughness": "Translation friction — meaning loss across contexts",
        "return": "Interpretant closure — sign chain returns to grounded meaning",
        "integrity": "Semiotic coherence across sign chains",
    },
}


# ---------------------------------------------------------------------------
# Regime descriptions — prose templates keyed by regime × lens
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class RegimeDescription:
    """Prose template for a regime within a lens."""

    drift_sentence: str
    fidelity_sentence: str
    roughness_sentence: str
    return_sentence: str
    verdict: str


def _describe_regime(
    regime: str,
    lens: str,
    snap: KernelSnapshot,
) -> RegimeDescription:
    """Generate constrained prose description from regime + invariants."""
    lens_words = ROSETTA_LENSES.get(lens, ROSETTA_LENSES["Ontology"])
    omega_pct = f"{snap.omega * 100:.1f}%"
    f_pct = f"{snap.F * 100:.1f}%"
    ic_pct = f"{snap.IC * 100:.1f}%"
    gap_pct = f"{snap.heterogeneity_gap * 100:.1f}%"

    if regime == "STABLE":
        return RegimeDescription(
            drift_sentence=(f"{lens_words['drift']} is minimal: ω = {omega_pct} drift from the contract."),
            fidelity_sentence=(
                f"{lens_words['fidelity']} holds at F = {f_pct} — the system retains almost all structure."
            ),
            roughness_sentence=(f"{lens_words['roughness']} is contained: C = {snap.C:.3f}, S = {snap.S:.3f}."),
            return_sentence=(
                f"{lens_words['return']} is confirmed — the system maintains IC = {ic_pct} composite integrity."
            ),
            verdict=(
                f"**Stance: STABLE** — {lens_words['integrity']} is verified. "
                f"The heterogeneity gap Δ = {gap_pct} indicates coherent structure."
            ),
        )
    elif regime == "WATCH":
        return RegimeDescription(
            drift_sentence=(f"{lens_words['drift']} is measurable: ω = {omega_pct} departure from the contract."),
            fidelity_sentence=(
                f"{lens_words['fidelity']} remains at F = {f_pct}, but not all stability gates are satisfied."
            ),
            roughness_sentence=(
                f"{lens_words['roughness']} is elevated: "
                f"C = {snap.C:.3f}, S = {snap.S:.3f}. "
                f"Some channels show heterogeneity."
            ),
            return_sentence=(f"{lens_words['return']} is plausible — IC = {ic_pct}, gap = {gap_pct}."),
            verdict=(
                f"**Stance: WATCH** — {lens_words['integrity']} is under observation. "
                f"Gates are not fully satisfied; monitoring continues."
            ),
        )
    else:  # COLLAPSE
        return RegimeDescription(
            drift_sentence=(f"{lens_words['drift']} is significant: ω = {omega_pct} collapse proximity."),
            fidelity_sentence=(f"{lens_words['fidelity']} is at F = {f_pct}. Substantial structure has been lost."),
            roughness_sentence=(
                f"{lens_words['roughness']} dominates: "
                f"C = {snap.C:.3f}, S = {snap.S:.3f}. "
                f"Channel heterogeneity is severe."
            ),
            return_sentence=(
                f"{lens_words['return']} requires demonstration — "
                f"IC = {ic_pct}, gap = {gap_pct}. "
                f"Return is not yet established."
            ),
            verdict=(
                f"**Stance: COLLAPSE** — {lens_words['integrity']} requires re-entry. "
                f"Collapse is generative; only what returns is real."
            ),
        )


# ---------------------------------------------------------------------------
# Markdown generators
# ---------------------------------------------------------------------------


def _generate_invariants_table(snap: KernelSnapshot) -> str:
    """Render the kernel invariants as a markdown table."""
    return f"""| Symbol | Name | Value |
|--------|------|-------|
| **F** | Fidelity | {snap.F:.6f} |
| **ω** | Drift | {snap.omega:.6f} |
| **S** | Bernoulli Field Entropy | {snap.S:.6f} |
| **C** | Curvature | {snap.C:.6f} |
| **κ** | Log-Integrity | {snap.kappa:.6f} |
| **IC** | Composite Integrity | {snap.IC:.6f} |
| **Δ** | Heterogeneity Gap | {snap.heterogeneity_gap:.6f} |
| — | Regime | **{snap.regime}** |"""


def generate_domain_markdown(
    data: SiteData,
    lens: str = "Ontology",
) -> str:
    """Generate full markdown content for one domain site.

    The output is a complete markdown document suitable for a static site
    generator (Astro, Hugo, Next.js).  All prose is derived from the
    frozen kernel invariants through the Rosetta lens — no prompt drift.
    """
    sections: list[str] = []

    # --- Hero ---
    sections.append(f"# {data.domain_display}\n")
    if data.anchors:
        sections.append(f"> *{data.anchors.hierarchy}*\n")
    sections.append("> **Axiom-0**: *Collapse is generative; only what returns is real.*\n")

    # --- Kernel Invariants ---
    sections.append("## Current Kernel State\n")
    if data.latest_snapshot:
        sections.append(_generate_invariants_table(data.latest_snapshot))
        sections.append("")

        # --- Five-Word Canon (Rosetta) ---
        sections.append(f"## Canon — {lens} Lens\n")
        desc = _describe_regime(
            data.latest_snapshot.regime,
            lens,
            data.latest_snapshot,
        )
        sections.append(f"**Drift**: {desc.drift_sentence}\n")
        sections.append(f"**Fidelity**: {desc.fidelity_sentence}\n")
        sections.append(f"**Roughness**: {desc.roughness_sentence}\n")
        sections.append(f"**Return**: {desc.return_sentence}\n")
        sections.append(f"{desc.verdict}\n")
    else:
        sections.append("*No CONFORMANT ledger entry available yet.*\n")

    # --- Channels ---
    if data.anchors and data.anchors.channels:
        sections.append("## Channels\n")
        channels = data.anchors.channels
        if isinstance(channels, dict):
            # Grouped channels: {"group_name": [items...], ...}
            for group_name, items in channels.items():
                sections.append(f"### {group_name.replace('_', ' ').title()}\n")
                if isinstance(items, list):
                    for item in items:
                        if isinstance(item, dict):
                            sections.append(f"- **{item.get('name', '—')}**: {item.get('definition', '—')}")
                        else:
                            sections.append(f"- {item}")
                sections.append("")
        elif isinstance(channels, list):
            sections.append("| Channel | Weight | Definition |")
            sections.append("|---------|--------|------------|")
            for ch in channels:
                if isinstance(ch, dict):
                    name = ch.get("name", "—")
                    weight = ch.get("weight", "—")
                    defn = ch.get("definition", "—")
                    sections.append(f"| {name} | {weight} | {defn} |")
                else:
                    sections.append(f"| {ch} | — | — |")
            sections.append("")

    # --- Anchors ---
    if data.anchors and data.anchors.anchors:
        sections.append("## Regime Anchors\n")
        for anchor_id, anchor_data in data.anchors.anchors.items():
            if isinstance(anchor_data, dict):
                name = anchor_data.get("name", anchor_id)
                regime = anchor_data.get("regime", "—")
                sections.append(f"- **{anchor_id}**: {name} → *{regime}*")
            else:
                sections.append(f"- **{anchor_id}**: {anchor_data}")
        sections.append("")

    # --- Closure Modules ---
    if data.closure_modules:
        sections.append("## Closure Modules\n")
        sections.append(f"**{len(data.closure_modules)}** modules")
        if data.theorem_count > 0:
            sections.append(f" · **~{data.theorem_count}** theorem references")
        if data.entity_count > 0:
            sections.append(f" · **~{data.entity_count}** entities")
        sections.append("\n")
        for mod in data.closure_modules:
            sections.append(f"- `{mod}`")
        sections.append("")

    # --- Casepacks ---
    if data.casepacks:
        sections.append("## Casepacks\n")
        for cp in data.casepacks:
            sections.append(f"### {cp.name}\n")
            if cp.description:
                sections.append(f"{cp.description}\n")
            sections.append(f"- **Contract**: `{cp.contract_ref}`")
            sections.append(f"- **Path**: `{cp.path}`")
            sections.append(f"- **Status**: {cp.status}")
            sections.append("")

    # --- Ledger Summary ---
    sections.append("## Validation Ledger Summary\n")
    total = len(data.ledger_rows)
    conformant = sum(1 for r in data.ledger_rows if r.run_status == "CONFORMANT")
    sections.append(f"- **Total entries**: {total}")
    sections.append(f"- **CONFORMANT**: {conformant}")
    sections.append(
        f"- **Conformance rate**: {conformant / total * 100:.1f}%" if total > 0 else "- **Conformance rate**: N/A"
    )
    sections.append("")

    # --- Spine ---
    sections.append("## The Spine\n")
    sections.append("```")
    sections.append("CONTRACT → CANON → CLOSURES → INTEGRITY LEDGER → STANCE → PUBLISH")
    sections.append("(freeze)   (tell)   (publish)   (reconcile)        (read)   (emit)")
    sections.append("```\n")
    sections.append(
        "Every page on this site is the final stop of the spine. "
        "The computation is frozen; the rendering reads the verdict.\n"
    )

    # --- Footer ---
    sections.append("---\n")
    sections.append(
        f"*Generated by the Headless Contract Gateway (HCG) · Domain: {data.domain} · Lens: {lens} · UMCP v2.2.5*\n"
    )

    return "\n".join(sections)


def generate_index_markdown(domains: list[SiteData]) -> str:
    """Generate the root index page listing all domain sites."""
    lines: list[str] = []
    lines.append("# GCD Kernel — Domain Network\n")
    lines.append("> *Collapse is generative; only what returns is real.*\n")
    lines.append("## Autonomous Domain Sites\n")
    lines.append("| Domain | Regime | F | IC | Δ | Modules |")
    lines.append("|--------|--------|---|----|----|---------|")

    for d in domains:
        snap = d.latest_snapshot
        if snap:
            lines.append(
                f"| [{d.domain_display}](/{d.domain}/) "
                f"| {snap.regime} "
                f"| {snap.F:.3f} "
                f"| {snap.IC:.3f} "
                f"| {snap.heterogeneity_gap:.3f} "
                f"| {len(d.closure_modules)} |"
            )
        else:
            lines.append(f"| [{d.domain_display}](/{d.domain}/) | — | — | — | — | {len(d.closure_modules)} |")

    lines.append("")
    lines.append("---\n")
    lines.append("*Generated by the Headless Contract Gateway (HCG) · UMCP v2.2.5*\n")
    return "\n".join(lines)
