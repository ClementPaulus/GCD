"""
Headless Contract Gateway (HCG) — Decentralized Publishing Engine

Extends the spine into the deployment phase:
    Contract → Canon → Closures → Integrity Ledger → Stance → **Publish**

The HCG reads frozen validation data (ledger, casepacks, canon anchors,
kernel invariants) and emits deterministic static site content.  By the time
a web page is generated, every Stance and IC number is already frozen —
computation is separated from rendering.

Architecture:
    extractor      — reads ledger + casepacks + canon → unified SiteData
    rosetta_gen    — translates kernel invariants → constrained prose via lenses
    domain_config  — routes TARGET_DOMAIN env var to the correct closure subset
    webhook        — fires rebuild triggers on CONFORMANT weld events
    builder        — orchestrates extract → generate → emit static content
    isolator       — scaffolds standalone Astro projects per domain (fleet mode)
    trigger        — bridges validation pipeline → webhook orchestrator

Usage:
    from umcp.hcg import build_site, extract_domain_data, SiteData

    data = extract_domain_data("finance")
    build_site(data, output_dir="web/dist/finance")
"""

from __future__ import annotations

from umcp.hcg.builder import build_site
from umcp.hcg.domain_config import DomainConfig, get_domain_config, list_domains
from umcp.hcg.extractor import (
    EntityInfo,
    SiteData,
    TheoremInfo,
    extract_domain_data,
    scan_closure_entities,
    scan_closure_theorems,
)
from umcp.hcg.isolator import IsolatedSite, isolate_all, isolate_domain
from umcp.hcg.trigger import LedgerWatcher, TriggerEvent, ValidationTrigger

__all__ = [
    "DomainConfig",
    "EntityInfo",
    "IsolatedSite",
    "LedgerWatcher",
    "SiteData",
    "TheoremInfo",
    "TriggerEvent",
    "ValidationTrigger",
    "build_site",
    "extract_domain_data",
    "get_domain_config",
    "isolate_all",
    "isolate_domain",
    "list_domains",
    "scan_closure_entities",
    "scan_closure_theorems",
]
