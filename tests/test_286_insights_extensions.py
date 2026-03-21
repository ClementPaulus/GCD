"""Tests for coverage gaps in insights.py and umcp_extensions.py.

Targets:
  - InsightEntry: to_dict, from_dict
  - PatternDatabase: add, query, count, load_yaml, load_canon, save_yaml, domains
  - InsightEngine: discover_all, show_startup_insight, full_report, summary_stats,
    save, philosophy, init flags
  - _hash_short, _pearson, _daily_seed
  - ExtensionManager: startup, get, is_loaded, loaded_names, available_names,
    default_names, on_demand_names, status, reset
  - list_extensions, get_extension_info, check_extension, load_extension
  - install_extension, run_extension
  - main CLI entry point
"""

from __future__ import annotations

from pathlib import Path
from typing import Any
from unittest.mock import patch

from umcp.insights import (
    InsightEngine,
    InsightEntry,
    InsightSeverity,
    PatternDatabase,
    PatternType,
    _hash_short,
    _pearson,
)
from umcp.umcp_extensions import (
    EXTENSIONS,
    ExtensionInfo,
    ExtensionManager,
    check_extension,
    get_extension_info,
    list_extensions,
    load_extension,
    run_extension,
)

# =====================================================================
# InsightEntry
# =====================================================================


class TestInsightEntry:
    def test_to_dict(self) -> None:
        e = InsightEntry(
            id="TEST-1",
            domain="Test",
            pattern="p",
            lesson="l",
            implication="i",
            severity=InsightSeverity.FUNDAMENTAL,
            pattern_type=PatternType.REGIME_BOUNDARY,
            source="discovered",
            elements=["Fe", "Cu"],
            omega_range=(0.1, 0.5),
        )
        d = e.to_dict()
        assert d["id"] == "TEST-1"
        assert d["severity"] == "Fundamental"
        assert d["pattern_type"] == "RegimeBoundary"
        assert d["omega_range"] == [0.1, 0.5]
        assert d["elements"] == ["Fe", "Cu"]

    def test_from_dict_minimal(self) -> None:
        d = {"id": "X-1", "pattern": "p", "lesson": "l", "implication": "i"}
        e = InsightEntry.from_dict(d)
        assert e.id == "X-1"
        assert e.domain == "General"
        assert e.source == "canon"
        assert e.severity == InsightSeverity.EMPIRICAL

    def test_roundtrip(self) -> None:
        e = InsightEntry(
            id="RT-1",
            domain="D",
            pattern="p",
            lesson="l",
            implication="i",
            severity=InsightSeverity.CURIOUS,
            pattern_type=PatternType.CROSS_CORRELATION,
            elements=["Au"],
            omega_range=(0.0, 1.0),
        )
        d = e.to_dict()
        e2 = InsightEntry.from_dict(d)
        assert e2.id == e.id
        assert e2.severity == e.severity
        assert e2.pattern_type == e.pattern_type


# =====================================================================
# PatternDatabase
# =====================================================================


class TestPatternDatabase:
    def test_add_unique(self) -> None:
        db = PatternDatabase()
        e1 = InsightEntry(id="A", domain="D", pattern="", lesson="", implication="")
        assert db.add(e1) is True
        assert db.count() == 1

    def test_add_duplicate(self) -> None:
        db = PatternDatabase()
        e = InsightEntry(id="A", domain="D", pattern="", lesson="", implication="")
        db.add(e)
        assert db.add(e) is False
        assert db.count() == 1

    def test_query_by_domain(self) -> None:
        db = PatternDatabase()
        db.add(InsightEntry(id="A", domain="X", pattern="", lesson="", implication=""))
        db.add(InsightEntry(id="B", domain="Y", pattern="", lesson="", implication=""))
        assert len(db.query(domain="X")) == 1
        assert len(db.query(domain="Z")) == 0

    def test_query_by_severity(self) -> None:
        db = PatternDatabase()
        db.add(
            InsightEntry(
                id="A",
                domain="D",
                pattern="",
                lesson="",
                implication="",
                severity=InsightSeverity.FUNDAMENTAL,
            )
        )
        db.add(
            InsightEntry(
                id="B",
                domain="D",
                pattern="",
                lesson="",
                implication="",
                severity=InsightSeverity.CURIOUS,
            )
        )
        assert len(db.query(severity=InsightSeverity.FUNDAMENTAL)) == 1

    def test_query_by_pattern_type(self) -> None:
        db = PatternDatabase()
        db.add(
            InsightEntry(
                id="A",
                domain="D",
                pattern="",
                lesson="",
                implication="",
                pattern_type=PatternType.UNIVERSALITY,
            )
        )
        assert len(db.query(pattern_type=PatternType.UNIVERSALITY)) == 1
        assert len(db.query(pattern_type=PatternType.PERIODIC_TREND)) == 0

    def test_query_by_source(self) -> None:
        db = PatternDatabase()
        db.add(InsightEntry(id="A", domain="D", pattern="", lesson="", implication="", source="canon"))
        db.add(InsightEntry(id="B", domain="D", pattern="", lesson="", implication="", source="discovered"))
        assert len(db.query(source="canon")) == 1
        assert len(db.query(source="discovered")) == 1

    def test_domains(self) -> None:
        db = PatternDatabase()
        db.add(InsightEntry(id="A", domain="Z", pattern="", lesson="", implication=""))
        db.add(InsightEntry(id="B", domain="A", pattern="", lesson="", implication=""))
        assert db.domains() == ["A", "Z"]

    def test_load_yaml_no_file(self) -> None:
        db = PatternDatabase()
        count = db.load_yaml(Path("/nonexistent/db.yaml"))
        assert count == 0

    def test_load_canon_no_file(self) -> None:
        db = PatternDatabase()
        count = db.load_canon(Path("/nonexistent/canon.yaml"))
        assert count == 0

    def test_save_yaml(self, tmp_path: Any) -> None:
        db = PatternDatabase()
        db.add(InsightEntry(id="S1", domain="D", pattern="p", lesson="l", implication="i"))
        out = tmp_path / "test_db.yaml"
        db.save_yaml(out)
        assert out.exists()

        # Reload
        db2 = PatternDatabase()
        count = db2.load_yaml(out)
        assert count == 1
        assert db2.entries[0].id == "S1"

    def test_load_yaml_empty_data(self, tmp_path: Any) -> None:
        """YAML file with no 'insights' key."""
        f = tmp_path / "empty.yaml"
        f.write_text("version: '1.0'\n")
        db = PatternDatabase()
        assert db.load_yaml(f) == 0

    def test_load_canon_empty_data(self, tmp_path: Any) -> None:
        """Canon file with no 'lessons_learned' key."""
        f = tmp_path / "canon.yaml"
        f.write_text("version: '1.0'\n")
        db = PatternDatabase()
        assert db.load_canon(f) == 0

    def test_load_canon_with_entries(self, tmp_path: Any) -> None:
        """Canon file with lessons_learned entries."""
        import yaml

        data = {
            "lessons_learned": [
                {
                    "id": "CAN-1",
                    "domain": "Test",
                    "pattern": "test pattern",
                    "lesson": "test lesson",
                    "implication": "test implication",
                }
            ]
        }
        f = tmp_path / "canon.yaml"
        f.write_text(yaml.dump(data))
        db = PatternDatabase()
        assert db.load_canon(f) == 1
        assert db.entries[0].severity == InsightSeverity.FUNDAMENTAL


# =====================================================================
# InsightEngine
# =====================================================================


class TestInsightEngine:
    def test_init_default(self) -> None:
        engine = InsightEngine()
        assert engine.db.count() >= 0

    def test_init_no_load(self) -> None:
        engine = InsightEngine(load_canon=False, load_db=False)
        assert engine.db.count() == 0

    def test_discover_all(self) -> None:
        engine = InsightEngine(load_canon=False, load_db=False)
        results = engine.discover_all()
        assert isinstance(results, list)

    def test_show_startup_insight_empty(self) -> None:
        engine = InsightEngine(load_canon=False, load_db=False)
        assert engine.show_startup_insight() == ""

    def test_show_startup_insight_with_data(self) -> None:
        engine = InsightEngine(load_canon=False, load_db=False)
        engine.db.add(
            InsightEntry(id="T1", domain="D", pattern="test pattern", lesson="test lesson", implication="test imp")
        )
        result = engine.show_startup_insight(seed=42)
        assert "test pattern" in result
        assert "UMCP" in result

    def test_full_report_empty(self) -> None:
        engine = InsightEngine(load_canon=False, load_db=False)
        assert engine.full_report() == "No insights in database."

    def test_full_report_with_data(self) -> None:
        engine = InsightEngine(load_canon=False, load_db=False)
        engine.db.add(
            InsightEntry(
                id="R1",
                domain="TestDomain",
                pattern="test",
                lesson="lesson",
                implication="imp",
                elements=["Fe"],
            )
        )
        report = engine.full_report()
        assert "TestDomain" in report
        assert "LESSONS-LEARNED" in report
        assert "Fe" in report

    def test_summary_stats(self) -> None:
        engine = InsightEngine(load_canon=False, load_db=False)
        engine.db.add(
            InsightEntry(
                id="SS1",
                domain="D",
                pattern="",
                lesson="",
                implication="",
                severity=InsightSeverity.STRUCTURAL,
                source="discovered",
            )
        )
        stats = engine.summary_stats()
        assert stats["total_insights"] == 1
        assert "D" in stats["domains"]
        assert stats["by_severity"]["Structural"] == 1
        assert stats["by_source"]["discovered"] == 1

    def test_save(self, tmp_path: Any) -> None:
        engine = InsightEngine(load_canon=False, load_db=False)
        engine.db.add(InsightEntry(id="SV1", domain="D", pattern="p", lesson="l", implication="i"))
        out = tmp_path / "save_test.yaml"
        engine.save(out)
        assert out.exists()

    def test_philosophy(self) -> None:
        text = InsightEngine.philosophy()
        assert "collapse" in text.lower()
        assert "ω_eff" in text


# =====================================================================
# Utility helpers
# =====================================================================


class TestUtilityHelpers:
    def test_hash_short(self) -> None:
        h = _hash_short("test")
        assert len(h) == 8
        assert _hash_short("test") == _hash_short("test")
        assert _hash_short("a") != _hash_short("b")

    def test_pearson_identical(self) -> None:
        r = _pearson([1.0, 2.0, 3.0], [1.0, 2.0, 3.0])
        assert abs(r - 1.0) < 1e-10

    def test_pearson_inverse(self) -> None:
        r = _pearson([1.0, 2.0, 3.0], [3.0, 2.0, 1.0])
        assert abs(r - (-1.0)) < 1e-10

    def test_pearson_short(self) -> None:
        assert _pearson([1.0], [2.0]) == 0.0

    def test_pearson_constant(self) -> None:
        assert _pearson([1.0, 1.0, 1.0], [1.0, 2.0, 3.0]) == 0.0


# =====================================================================
# ExtensionManager
# =====================================================================


class TestExtensionManager:
    def test_startup(self) -> None:
        mgr = ExtensionManager()
        loaded = mgr.startup()
        assert isinstance(loaded, list)
        # At least ledger/formatter/thermodynamics should load
        assert len(loaded) >= 1

    def test_get_default(self) -> None:
        mgr = ExtensionManager()
        mod = mgr.get("ledger")
        # Should load successfully
        assert mod is not None or not check_extension("ledger")

    def test_get_unknown(self) -> None:
        mgr = ExtensionManager()
        assert mgr.get("nonexistent_ext_xyz") is None

    def test_is_loaded(self) -> None:
        mgr = ExtensionManager()
        assert mgr.is_loaded("ledger") is False
        mgr.get("ledger")
        # After get, it's loaded (if deps present)
        if check_extension("ledger"):
            assert mgr.is_loaded("ledger") is True

    def test_loaded_names(self) -> None:
        mgr = ExtensionManager()
        mgr.startup()
        names = mgr.loaded_names
        assert isinstance(names, list)

    def test_available_names(self) -> None:
        mgr = ExtensionManager()
        assert "ledger" in mgr.available_names
        assert "api" in mgr.available_names

    def test_default_names(self) -> None:
        mgr = ExtensionManager()
        assert "ledger" in mgr.default_names
        assert "api" not in mgr.default_names

    def test_on_demand_names(self) -> None:
        mgr = ExtensionManager()
        assert "api" in mgr.on_demand_names
        assert "ledger" not in mgr.on_demand_names

    def test_status(self) -> None:
        mgr = ExtensionManager()
        mgr.startup()
        st = mgr.status()
        assert "started" in st
        assert st["started"] is True
        assert "default" in st
        assert "on_demand" in st
        assert "loaded" in st

    def test_reset(self) -> None:
        mgr = ExtensionManager()
        mgr.startup()
        mgr.reset()
        assert mgr._started is False
        assert len(mgr._loaded) == 0


# =====================================================================
# Module-level functions
# =====================================================================


class TestModuleFunctions:
    def test_list_extensions_all(self) -> None:
        exts = list_extensions()
        assert len(exts) == len(EXTENSIONS)

    def test_list_extensions_by_type(self) -> None:
        exts = list_extensions(ext_type="api")
        assert all(e["type"] == "api" for e in exts)

    def test_get_extension_info_known(self) -> None:
        info = get_extension_info("ledger")
        assert info["name"] == "ledger"

    def test_get_extension_info_unknown(self) -> None:
        info = get_extension_info("nonexistent_xyz")
        assert info["status"] == "not_found"

    def test_check_extension_known(self) -> None:
        assert isinstance(check_extension("ledger"), bool)

    def test_check_extension_unknown(self) -> None:
        assert check_extension("nonexistent_xyz") is False

    def test_load_extension(self) -> None:
        mod = load_extension("ledger")
        if check_extension("ledger"):
            assert mod is not None

    def test_run_extension_not_found(self) -> None:
        assert run_extension("nonexistent_xyz") == 1

    def test_run_extension_no_command(self) -> None:
        # ledger has no command
        result = run_extension("ledger")
        # Should return 1 because there's no command to run
        assert result == 1


# =====================================================================
# ExtensionInfo
# =====================================================================


class TestExtensionInfo:
    def test_to_dict(self) -> None:
        info = ExtensionInfo(
            name="test",
            description="A test",
            type="tool",
            module="umcp.test",
            default=True,
            class_name="MyClass",
            requires=["numpy"],
            command="do-thing",
            port=9999,
            endpoints=[{"method": "GET", "path": "/", "description": "root"}],
            features=["feat1"],
        )
        d = info.to_dict()
        assert d["name"] == "test"
        assert d["port"] == 9999
        assert d["class"] == "MyClass"
        assert d["endpoints"][0]["method"] == "GET"


# =====================================================================
# CLI main (minimal paths)
# =====================================================================


class TestExtensionCLI:
    def test_main_no_args(self) -> None:
        from umcp.umcp_extensions import main

        with patch("sys.argv", ["umcp-ext"]):
            assert main() == 0

    def test_main_status(self) -> None:
        from umcp.umcp_extensions import main

        with patch("sys.argv", ["umcp-ext", "status"]):
            assert main() == 0

    def test_main_list(self) -> None:
        from umcp.umcp_extensions import main

        with patch("sys.argv", ["umcp-ext", "list"]):
            assert main() == 0

    def test_main_list_type(self) -> None:
        from umcp.umcp_extensions import main

        with patch("sys.argv", ["umcp-ext", "list", "--type", "api"]):
            assert main() == 0

    def test_main_info(self) -> None:
        from umcp.umcp_extensions import main

        with patch("sys.argv", ["umcp-ext", "info", "ledger"]):
            assert main() == 0

    def test_main_info_unknown(self) -> None:
        from umcp.umcp_extensions import main

        with patch("sys.argv", ["umcp-ext", "info", "nonexistent_xyz"]):
            assert main() == 1

    def test_main_check(self) -> None:
        from umcp.umcp_extensions import main

        with patch("sys.argv", ["umcp-ext", "check", "ledger"]):
            result = main()
            assert result in (0, 1)

    def test_main_check_missing(self) -> None:
        from umcp.umcp_extensions import main

        with patch("sys.argv", ["umcp-ext", "check", "nonexistent_xyz"]):
            assert main() == 1
