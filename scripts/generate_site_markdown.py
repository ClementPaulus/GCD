#!/usr/bin/env python3
"""
Generate static site markdown from frozen validation data.

This is the CLI entry point for the HCG pipeline:
    Contract → Canon → Closures → Integrity Ledger → Stance → **Publish**

Usage:
    # Generate all 20 domain sites
    python scripts/generate_site_markdown.py

    # Generate a single domain
    python scripts/generate_site_markdown.py --domain finance

    # Generate with a specific Rosetta lens
    python scripts/generate_site_markdown.py --domain consciousness_coherence --lens Phenomenology

    # List available domains
    python scripts/generate_site_markdown.py --list
"""

from __future__ import annotations

import sys
from pathlib import Path

# Ensure src/ is on the path
_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_root / "src"))

from umcp.hcg.builder import main

if __name__ == "__main__":
    sys.exit(main())
