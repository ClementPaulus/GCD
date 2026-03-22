"""
Static Site Builder — Orchestrates extract → generate → emit.

The builder reads frozen validation data through the extractor, generates
markdown through the Rosetta generator, and emits static content ready for
an SSG framework (Astro, Hugo, Next.js) to compile into HTML.

The builder can operate in two modes:
    1. Single domain:  TARGET_DOMAIN=finance → builds only the finance site
    2. Full network:   No TARGET_DOMAIN → builds all 20 domain sites + index

Usage:
    # Python API
    from umcp.hcg.builder import build_site, build_all_sites

    build_site(domain="finance", output_dir=Path("web/src/content/finance"))
    build_all_sites(output_dir=Path("web/src/content"))

    # CLI
    python -m umcp.hcg.builder --domain finance --output web/src/content
    python -m umcp.hcg.builder --all --output web/src/content
"""

from __future__ import annotations

import argparse
import json
import logging
import sys
from pathlib import Path
from typing import Any

from umcp.hcg.domain_config import DomainConfig, get_domain_config, list_domains
from umcp.hcg.extractor import SiteData, extract_domain_data
from umcp.hcg.rosetta_gen import generate_domain_markdown, generate_index_markdown

logger = logging.getLogger(__name__)


def _write_frontmatter(
    path: Path,
    frontmatter: dict[str, Any],
    body: str,
) -> None:
    """Write a markdown file with YAML frontmatter."""
    path.parent.mkdir(parents=True, exist_ok=True)

    lines: list[str] = ["---"]
    for key, value in frontmatter.items():
        if isinstance(value, bool):
            lines.append(f"{key}: {'true' if value else 'false'}")
        elif isinstance(value, str):
            # Quote strings with special chars
            if any(c in value for c in ":#{}[]|>&*!%@`"):
                lines.append(f'{key}: "{value}"')
            else:
                lines.append(f"{key}: {value}")
        elif isinstance(value, list):
            lines.append(f"{key}:")
            for item in value:
                lines.append(f"  - {item}")
        else:
            lines.append(f"{key}: {value}")
    lines.append("---")
    lines.append("")
    lines.append(body)

    path.write_text("\n".join(lines), encoding="utf-8")
    logger.info("Wrote %s (%d bytes)", path, path.stat().st_size)


def _emit_domain_data_json(
    data: SiteData,
    output_dir: Path,
) -> None:
    """Emit domain data as JSON for client-side rendering."""
    json_dir = output_dir / "_data"
    json_dir.mkdir(parents=True, exist_ok=True)

    # Kernel snapshot
    snap_data: dict[str, Any] = {}
    if data.latest_snapshot:
        snap_data = {
            "F": data.latest_snapshot.F,
            "omega": data.latest_snapshot.omega,
            "S": data.latest_snapshot.S,
            "C": data.latest_snapshot.C,
            "kappa": data.latest_snapshot.kappa,
            "IC": data.latest_snapshot.IC,
            "regime": data.latest_snapshot.regime,
            "heterogeneity_gap": data.latest_snapshot.heterogeneity_gap,
        }

    domain_json = {
        "domain": data.domain,
        "display_name": data.domain_display,
        "kernel": snap_data,
        "closure_modules": data.closure_modules,
        "theorem_count": data.theorem_count,
        "entity_count": data.entity_count,
        "casepack_count": len(data.casepacks),
        "ledger_total": len(data.ledger_rows),
        "ledger_conformant": sum(1 for r in data.ledger_rows if r.run_status == "CONFORMANT"),
        "metadata": {
            k: v
            for k, v in data.metadata.items()
            if k != "repo_root"  # Don't leak filesystem paths
        },
    }

    out = json_dir / f"{data.domain}.json"
    out.write_text(json.dumps(domain_json, indent=2), encoding="utf-8")
    logger.info("Wrote %s", out)


def build_site(
    domain: str | None = None,
    output_dir: Path | str | None = None,
    lens: str | None = None,
    root: Path | None = None,
) -> SiteData:
    """Build static content for one domain.

    Parameters
    ----------
    domain : str, optional
        Domain slug (e.g. "finance").  Falls back to TARGET_DOMAIN env.
    output_dir : Path, optional
        Where to write content.  Defaults to web/src/content/<domain>.
    lens : str, optional
        Rosetta lens to use.  Falls back to domain config default.
    root : Path, optional
        Repository root.  Auto-detected if omitted.

    Returns
    -------
    SiteData
        The extracted data used for the build.
    """
    config: DomainConfig = get_domain_config(domain)
    domain = config.slug

    if lens is None:
        lens = config.default_lens

    if output_dir is None:
        from umcp.hcg.extractor import _repo_root

        output_dir = _repo_root() / "web" / "src" / "content" / domain
    else:
        output_dir = Path(output_dir) / domain

    logger.info("Building site for domain=%s lens=%s → %s", domain, lens, output_dir)

    # Extract
    data = extract_domain_data(domain, root)

    # Generate markdown
    body = generate_domain_markdown(data, lens=lens)

    # Emit main page
    frontmatter = {
        "title": config.display_name,
        "description": config.tagline,
        "domain": domain,
        "lens": lens,
        "regime": data.latest_snapshot.regime if data.latest_snapshot else "UNKNOWN",
        "layout": "../../layouts/DomainLayout.astro",
        "primaryColor": config.primary_color,
        "accentColor": config.accent_color,
        "icon": config.icon,
    }
    _write_frontmatter(output_dir / "index.md", frontmatter, body)

    # Emit data JSON
    _emit_domain_data_json(data, output_dir)

    # Emit per-casepack pages
    for cp in data.casepacks:
        cp_body = f"# {cp.name}\n\n{cp.description}\n\n"
        cp_body += f"- **Contract**: `{cp.contract_ref}`\n"
        cp_body += f"- **Status**: {cp.status}\n"
        cp_fm = {
            "title": cp.name,
            "description": cp.description or f"Casepack: {cp.name}",
            "layout": "../../../layouts/CasepackLayout.astro",
        }
        _write_frontmatter(
            output_dir / "casepacks" / f"{cp.name}.md",
            cp_fm,
            cp_body,
        )

    logger.info(
        "Domain %s: %d modules, %d casepacks, regime=%s",
        domain,
        len(data.closure_modules),
        len(data.casepacks),
        data.latest_snapshot.regime if data.latest_snapshot else "N/A",
    )

    return data


def build_all_sites(
    output_dir: Path | str | None = None,
    root: Path | None = None,
) -> list[SiteData]:
    """Build static content for all 20 domains + root index.

    Returns list of SiteData for all domains.
    """
    if output_dir is None:
        from umcp.hcg.extractor import _repo_root

        output_dir = _repo_root() / "web" / "src" / "content"
    else:
        output_dir = Path(output_dir)

    all_data: list[SiteData] = []
    domains = list_domains()

    for domain in domains:
        try:
            data = build_site(domain=domain, output_dir=output_dir, root=root)
            all_data.append(data)
        except Exception as exc:
            logger.error("Failed to build domain %s: %s", domain, exc)

    # Generate root index
    index_body = generate_index_markdown(all_data)
    _write_frontmatter(
        output_dir / "index.md",
        {
            "title": "GCD Kernel — Domain Network",
            "description": "Autonomous domain sites powered by the Headless Contract Gateway",
            "layout": "../layouts/IndexLayout.astro",
        },
        index_body,
    )

    logger.info("Built %d domain sites + index → %s", len(all_data), output_dir)
    return all_data


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------


def main(argv: list[str] | None = None) -> int:
    """CLI for the HCG builder."""
    parser = argparse.ArgumentParser(
        prog="hcg-builder",
        description="Headless Contract Gateway — Static Site Builder",
    )
    parser.add_argument(
        "--domain",
        "-d",
        help="Build a single domain site (e.g. 'finance')",
    )
    parser.add_argument(
        "--all",
        "-a",
        action="store_true",
        dest="build_all",
        help="Build all 20 domain sites + index",
    )
    parser.add_argument(
        "--output",
        "-o",
        default=None,
        help="Output directory (default: web/src/content)",
    )
    parser.add_argument(
        "--lens",
        "-l",
        default=None,
        help="Rosetta lens (default: domain config default)",
    )
    parser.add_argument(
        "--list-domains",
        action="store_true",
        help="List available domains and exit",
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Enable verbose logging",
    )

    args = parser.parse_args(argv)

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(levelname)s: %(message)s",
    )

    if args.list_domains:
        for d in list_domains():
            config = get_domain_config(d)
            print(f"  {d:30s} {config.display_name}")
        return 0

    output = Path(args.output) if args.output else None

    if args.build_all:
        results = build_all_sites(output_dir=output)
        print(f"\nBuilt {len(results)} domain sites.")
        return 0

    if args.domain:
        build_site(domain=args.domain, output_dir=output, lens=args.lens)
        return 0

    # Default: build from TARGET_DOMAIN env or all
    import os

    if os.environ.get("TARGET_DOMAIN"):
        build_site(output_dir=output, lens=args.lens)
    else:
        results = build_all_sites(output_dir=output)
        print(f"\nBuilt {len(results)} domain sites.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
