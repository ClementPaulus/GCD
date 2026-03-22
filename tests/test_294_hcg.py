"""
Tests for the Headless Contract Gateway (HCG) pipeline.

Validates the full flow:
    extractor → rosetta_gen → domain_config → webhook → builder

All tests use frozen validation data — no kernel computation happens here.
"""

from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import patch

import pytest

from umcp.hcg.domain_config import DomainConfig, get_domain_config, list_domains
from umcp.hcg.extractor import (
    DomainAnchors,
    KernelSnapshot,
    LedgerRow,
    SiteData,
    _safe_float,
    extract_domain_data,
    read_ledger,
)
from umcp.hcg.rosetta_gen import (
    ROSETTA_LENSES,
    generate_domain_markdown,
    generate_index_markdown,
)
from umcp.hcg.webhook import WebhookOrchestrator, WebhookTarget

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture()
def repo_root() -> Path:
    """Return the repository root."""
    p = Path(__file__).resolve().parent.parent
    assert (p / "pyproject.toml").exists(), f"Not a repo root: {p}"
    return p


@pytest.fixture()
def sample_snapshot() -> KernelSnapshot:
    """A STABLE kernel snapshot for testing."""
    return KernelSnapshot(
        F=0.95,
        omega=0.05,
        S=0.10,
        C=0.08,
        kappa=-0.0513,
        IC=0.95,
        regime="STABLE",
        heterogeneity_gap=0.0,
    )


@pytest.fixture()
def sample_site_data(sample_snapshot: KernelSnapshot) -> SiteData:
    """A minimal SiteData for testing."""
    return SiteData(
        domain="finance",
        domain_display="Finance",
        anchors=DomainAnchors(
            domain_id="UMCP.CANON.FINANCE.v1",
            domain_name="Finance",
            version="1.0.0",
            hierarchy="GCD > FINANCE (Tier-2)",
            channels=[
                {"name": "revenue_performance", "weight": 0.30, "definition": "revenue / target"},
                {"name": "expense_control", "weight": 0.25, "definition": "budget / expenses"},
            ],
            anchors={
                "FIN-A1": {"name": "Strong quarter", "regime": "Stable"},
                "FIN-A2": {"name": "Revenue miss", "regime": "Watch"},
            },
            raw={},
        ),
        ledger_rows=[
            LedgerRow(
                timestamp="2026-03-22T00:00:00Z",
                run_status="CONFORMANT",
                F=0.95,
                omega=0.05,
                kappa=-0.0513,
                IC=0.95,
                C=0.08,
                S=0.10,
                tau_R="",
                delta_kappa="",
                chain_hash="abc123",
            ),
        ],
        latest_snapshot=sample_snapshot,
        casepacks=[],
        contract={"id": "FINANCE.INTSTACK.v1"},
        closure_modules=["volatility_surface"],
        theorem_count=6,
        entity_count=12,
        metadata={"domain_count": 20},
    )


# ---------------------------------------------------------------------------
# Domain Config
# ---------------------------------------------------------------------------


class TestDomainConfig:
    """Tests for domain_config.py."""

    def test_list_domains_returns_20(self) -> None:
        domains = list_domains()
        assert len(domains) == 20

    def test_all_domains_have_configs(self) -> None:
        for d in list_domains():
            config = get_domain_config(d)
            assert isinstance(config, DomainConfig)
            assert config.slug == d
            assert config.display_name
            assert config.tagline
            assert config.anchor_prefix

    def test_get_domain_config_unknown_raises(self) -> None:
        with pytest.raises(ValueError, match="Unknown domain"):
            get_domain_config("nonexistent_domain")

    def test_get_domain_config_env_fallback(self) -> None:
        with patch.dict("os.environ", {"TARGET_DOMAIN": "finance"}):
            config = get_domain_config()
            assert config.slug == "finance"

    def test_gcd_is_primary(self) -> None:
        config = get_domain_config("gcd")
        assert config.display_name == "Generative Collapse Dynamics"
        assert config.default_lens == "Epistemology"

    @pytest.mark.parametrize("domain", list_domains())
    def test_each_domain_has_valid_color(self, domain: str) -> None:
        config = get_domain_config(domain)
        assert config.primary_color.startswith("#")
        assert config.accent_color.startswith("#")

    @pytest.mark.parametrize("domain", list_domains())
    def test_each_domain_has_rosetta_lens(self, domain: str) -> None:
        config = get_domain_config(domain)
        assert config.default_lens in ROSETTA_LENSES


# ---------------------------------------------------------------------------
# Extractor
# ---------------------------------------------------------------------------


class TestExtractor:
    """Tests for extractor.py."""

    def test_safe_float_normal(self) -> None:
        assert _safe_float("3.14") == 3.14

    def test_safe_float_empty(self) -> None:
        assert _safe_float("") == 0.0

    def test_safe_float_invalid(self) -> None:
        assert _safe_float("abc") == 0.0

    def test_safe_float_custom_default(self) -> None:
        assert _safe_float("", default=-1.0) == -1.0

    def test_read_ledger_from_repo(self, repo_root: Path) -> None:
        rows = read_ledger(repo_root)
        assert len(rows) > 0
        for row in rows:
            assert isinstance(row, LedgerRow)
            assert row.run_status in ("CONFORMANT", "NONCONFORMANT", "NON_EVALUABLE")

    def test_extract_domain_data_gcd(self, repo_root: Path) -> None:
        data = extract_domain_data("gcd", repo_root)
        assert isinstance(data, SiteData)
        assert data.domain == "gcd"
        assert data.domain_display == "Generative Collapse Dynamics"
        assert len(data.ledger_rows) > 0

    def test_extract_domain_data_finance(self, repo_root: Path) -> None:
        data = extract_domain_data("finance", repo_root)
        assert data.domain == "finance"
        assert data.domain_display == "Finance"
        # Finance has closure modules
        assert len(data.closure_modules) >= 1

    @pytest.mark.parametrize("domain", list_domains())
    def test_extract_every_domain(self, repo_root: Path, domain: str) -> None:
        """Verify extraction works for all 20 domains without error."""
        data = extract_domain_data(domain, repo_root)
        assert isinstance(data, SiteData)
        assert data.domain == domain

    def test_latest_snapshot_is_conformant(self, repo_root: Path) -> None:
        data = extract_domain_data("gcd", repo_root)
        if data.latest_snapshot:
            assert isinstance(data.latest_snapshot, KernelSnapshot)
            assert data.latest_snapshot.regime in ("STABLE", "WATCH", "COLLAPSE")
            # Duality identity
            assert abs(data.latest_snapshot.F + data.latest_snapshot.omega - 1.0) < 1e-6

    def test_ledger_row_types(self) -> None:
        row = LedgerRow(
            timestamp="2026-01-01T00:00:00Z",
            run_status="CONFORMANT",
            F=0.95,
            omega=0.05,
            kappa=-0.05,
            IC=0.95,
            C=0.01,
            S=0.01,
            tau_R="",
            delta_kappa="",
            chain_hash="abc",
        )
        assert row.F + row.omega == pytest.approx(1.0)


# ---------------------------------------------------------------------------
# Rosetta Generator
# ---------------------------------------------------------------------------


class TestRosettaGenerator:
    """Tests for rosetta_gen.py."""

    def test_rosetta_has_six_lenses(self) -> None:
        assert len(ROSETTA_LENSES) == 6
        expected = {"Epistemology", "Ontology", "Phenomenology", "History", "Policy", "Semiotics"}
        assert set(ROSETTA_LENSES.keys()) == expected

    def test_each_lens_has_five_words(self) -> None:
        for lens_name, lens in ROSETTA_LENSES.items():
            assert "drift" in lens, f"{lens_name} missing 'drift'"
            assert "fidelity" in lens, f"{lens_name} missing 'fidelity'"
            assert "roughness" in lens, f"{lens_name} missing 'roughness'"
            assert "return" in lens, f"{lens_name} missing 'return'"
            assert "integrity" in lens, f"{lens_name} missing 'integrity'"

    def test_generate_domain_markdown(self, sample_site_data: SiteData) -> None:
        md = generate_domain_markdown(sample_site_data, lens="Policy")
        assert "# Finance" in md
        assert "STABLE" in md
        assert "Axiom-0" in md
        assert "F" in md and "ω" in md
        # Rosetta lens words should appear
        assert "Regime shift" in md or "Compliance" in md

    @pytest.mark.parametrize("lens", list(ROSETTA_LENSES.keys()))
    def test_generate_all_lenses(self, sample_site_data: SiteData, lens: str) -> None:
        md = generate_domain_markdown(sample_site_data, lens=lens)
        assert len(md) > 100
        assert "# Finance" in md

    def test_generate_without_snapshot(self, sample_site_data: SiteData) -> None:
        data = SiteData(
            domain="test",
            domain_display="Test Domain",
            anchors=None,
            ledger_rows=[],
            latest_snapshot=None,
            casepacks=[],
            contract=None,
            closure_modules=[],
            theorem_count=0,
            entity_count=0,
        )
        md = generate_domain_markdown(data)
        assert "No CONFORMANT" in md

    def test_generate_index_markdown(self, sample_site_data: SiteData) -> None:
        md = generate_index_markdown([sample_site_data])
        assert "Domain Network" in md
        assert "Finance" in md

    def test_spine_appears_in_output(self, sample_site_data: SiteData) -> None:
        md = generate_domain_markdown(sample_site_data)
        assert "CONTRACT" in md and "PUBLISH" in md

    def test_regime_watch(self) -> None:
        snap = KernelSnapshot(
            F=0.85,
            omega=0.15,
            S=0.20,
            C=0.20,
            kappa=-0.16,
            IC=0.85,
            regime="WATCH",
            heterogeneity_gap=0.0,
        )
        data = SiteData(
            domain="test",
            domain_display="Test",
            anchors=None,
            ledger_rows=[],
            latest_snapshot=snap,
            casepacks=[],
            contract=None,
            closure_modules=[],
            theorem_count=0,
            entity_count=0,
        )
        md = generate_domain_markdown(data)
        assert "WATCH" in md

    def test_regime_collapse(self) -> None:
        snap = KernelSnapshot(
            F=0.50,
            omega=0.50,
            S=0.69,
            C=0.50,
            kappa=-0.69,
            IC=0.50,
            regime="COLLAPSE",
            heterogeneity_gap=0.0,
        )
        data = SiteData(
            domain="test",
            domain_display="Test",
            anchors=None,
            ledger_rows=[],
            latest_snapshot=snap,
            casepacks=[],
            contract=None,
            closure_modules=[],
            theorem_count=0,
            entity_count=0,
        )
        md = generate_domain_markdown(data)
        assert "COLLAPSE" in md
        assert "only what returns is real" in md


# ---------------------------------------------------------------------------
# Webhook Orchestrator
# ---------------------------------------------------------------------------


class TestWebhookOrchestrator:
    """Tests for webhook.py."""

    def test_add_target(self) -> None:
        orch = WebhookOrchestrator()
        orch.add_target(WebhookTarget(name="test", url="https://example.com/hook"))
        assert len(orch.targets) == 1
        assert orch.targets[0].name == "test"

    def test_fire_dry_run(self) -> None:
        orch = WebhookOrchestrator()
        orch.add_target(WebhookTarget(name="test", url="https://example.com/hook", domains=["finance"]))
        results = orch.fire("finance", dry_run=True)
        assert len(results) == 1
        assert results[0].success is True
        assert results[0].status_code == 0

    def test_fire_no_matching_targets(self) -> None:
        orch = WebhookOrchestrator()
        orch.add_target(WebhookTarget(name="finance-only", url="https://example.com/hook", domains=["finance"]))
        results = orch.fire("astronomy")
        assert len(results) == 0

    def test_fire_all_domains_target(self) -> None:
        orch = WebhookOrchestrator()
        orch.add_target(WebhookTarget(name="all", url="https://example.com/hook", domains=[]))
        results = orch.fire("finance", dry_run=True)
        assert len(results) == 1

    def test_disabled_target_skipped(self) -> None:
        orch = WebhookOrchestrator()
        orch.add_target(WebhookTarget(name="disabled", url="https://example.com/hook", enabled=False))
        results = orch.fire("finance", dry_run=True)
        assert len(results) == 0

    def test_add_target_from_env(self) -> None:
        env = {
            "HCG_WEBHOOK_VERCEL_URL": "https://api.vercel.com/deploy/xxx",
            "HCG_WEBHOOK_VERCEL_KIND": "vercel",
            "HCG_WEBHOOK_VERCEL_DOMAINS": "finance,astronomy",
            "HCG_WEBHOOK_VERCEL_TOKEN": "secret123",
        }
        with patch.dict("os.environ", env, clear=False):
            orch = WebhookOrchestrator()
            orch.add_target_from_env()
            assert len(orch.targets) == 1
            t = orch.targets[0]
            assert t.name == "vercel"
            assert t.kind == "vercel"
            assert t.domains == ["finance", "astronomy"]
            assert "Authorization" in t.headers

    def test_github_payload_format(self) -> None:
        orch = WebhookOrchestrator()
        payload = orch._build_github_payload("finance", {"IC": 0.95})
        assert payload["event_type"] == "hcg-rebuild-finance"
        assert payload["client_payload"]["domain"] == "finance"
        assert payload["client_payload"]["data"]["IC"] == 0.95


# ---------------------------------------------------------------------------
# Builder
# ---------------------------------------------------------------------------


class TestBuilder:
    """Tests for builder.py."""

    def test_build_site_creates_files(self, repo_root: Path, tmp_path: Path) -> None:
        from umcp.hcg.builder import build_site

        data = build_site(domain="gcd", output_dir=tmp_path, root=repo_root)
        assert isinstance(data, SiteData)
        assert (tmp_path / "gcd" / "index.md").exists()

        content = (tmp_path / "gcd" / "index.md").read_text()
        assert "---" in content  # Frontmatter present
        assert "Generative Collapse Dynamics" in content

    def test_build_site_emits_json(self, repo_root: Path, tmp_path: Path) -> None:
        from umcp.hcg.builder import build_site

        build_site(domain="finance", output_dir=tmp_path, root=repo_root)
        json_path = tmp_path / "finance" / "_data" / "finance.json"
        assert json_path.exists()

        data = json.loads(json_path.read_text())
        assert data["domain"] == "finance"
        assert "kernel" in data
        # No filesystem paths leaked
        assert "repo_root" not in data.get("metadata", {})

    def test_build_all_sites(self, repo_root: Path, tmp_path: Path) -> None:
        from umcp.hcg.builder import build_all_sites

        results = build_all_sites(output_dir=tmp_path, root=repo_root)
        assert len(results) == 20

        # Root index exists
        assert (tmp_path / "index.md").exists()

        # Each domain has its own directory
        for data in results:
            assert (tmp_path / data.domain / "index.md").exists()

    def test_build_site_frontmatter_regime(self, repo_root: Path, tmp_path: Path) -> None:
        from umcp.hcg.builder import build_site

        build_site(domain="gcd", output_dir=tmp_path, root=repo_root)
        content = (tmp_path / "gcd" / "index.md").read_text()

        # Check frontmatter contains regime
        lines = content.split("\n")
        assert lines[0] == "---"
        # Find regime in frontmatter
        in_frontmatter = False
        for line in lines:
            if line == "---":
                in_frontmatter = not in_frontmatter
                continue
            if in_frontmatter and line.startswith("regime:"):
                regime = line.split(":")[1].strip()
                assert regime in ("STABLE", "WATCH", "COLLAPSE", "UNKNOWN")
                break

    def test_cli_list_domains(self) -> None:
        from umcp.hcg.builder import main

        # --list-domains should exit 0
        result = main(["--list-domains"])
        assert result == 0
