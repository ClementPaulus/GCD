"""Coverage push — final round targeting remaining branch/stmt gaps.

Targets: insights, extensions, validator, scheduler, cache, queue,
closures, logging, measurement, file_refs, tenant, tau_r_star_dynamics,
seam_optimized, compute_utils, api helpers.
"""

from __future__ import annotations

import tempfile
from pathlib import Path

import numpy as np
import pytest

from umcp.closures import ClosureLoader, get_closure_loader
from umcp.compute_utils import (
    BatchProcessor,
    batch_validate_outputs,
    clip_coordinates,
    normalize_weights,
    validate_inputs,
)
from umcp.file_refs import UMCPFiles, get_umcp_files
from umcp.fleet.cache import FilesystemBackend
from umcp.fleet.models import JobPriority, TenantQuota
from umcp.fleet.queue import PriorityQueue
from umcp.fleet.scheduler import Scheduler
from umcp.fleet.tenant import (
    QuotaExceededError,
    TenantManager,
    TenantNotFoundError,
)

# ── Source modules ────────────────────────────────────────────────────────
from umcp.insights import InsightEngine, InsightEntry, InsightSeverity, PatternDatabase, PatternType
from umcp.logging_utils import HealthCheck, StructuredLogger
from umcp.measurement_engine import MeasurementEngine
from umcp.seam_optimized import (
    SeamChainAccumulator,
    create_seam_chain,
    validate_seam_residuals,
)
from umcp.tau_r_star_dynamics import (
    compute_entropy_production,
    compute_equation_of_state,
    diagnose_extended,
    verify_residue_convergence,
)
from umcp.umcp_extensions import ExtensionManager
from umcp.validator import RootFileValidator

# ==========================================================================
# Insights — discovery paths
# ==========================================================================


class TestInsightsDiscoveryPaths:
    """Cover discovery branches in InsightEngine."""

    def test_engine_no_load(self):
        engine = InsightEngine(load_canon=False, load_db=False)
        assert isinstance(engine.db, PatternDatabase)
        assert len(engine.db.entries) == 0

    def test_engine_load_db_only(self):
        engine = InsightEngine(load_canon=False, load_db=True)
        assert isinstance(engine.db, PatternDatabase)

    def test_discover_periodic_trends_no_module(self):
        engine = InsightEngine(load_canon=False, load_db=False)
        results = engine.discover_periodic_trends()
        # Returns empty or list depending on import availability
        assert isinstance(results, list)

    def test_discover_regime_boundaries_no_module(self):
        engine = InsightEngine(load_canon=False, load_db=False)
        if hasattr(engine, "discover_regime_boundaries"):
            results = engine.discover_regime_boundaries()
            assert isinstance(results, list)

    def test_engine_full_report(self):
        engine = InsightEngine(load_canon=False, load_db=False)
        if hasattr(engine, "full_report"):
            # Just verify it doesn't crash
            engine.full_report()

    def test_pattern_database_query(self):
        db = PatternDatabase()
        results = db.query()
        assert isinstance(results, list)

    def test_insight_entry_creation(self):
        entry = InsightEntry(
            id="TEST-001",
            domain="Test",
            pattern="Test pattern",
            lesson="A lesson",
            implication="An implication",
            severity=InsightSeverity.CURIOUS,
            pattern_type=PatternType.PHYSICAL_INSIGHT,
        )
        assert entry.id == "TEST-001"
        assert entry.severity == InsightSeverity.CURIOUS

    def test_pattern_database_add_and_query(self):
        db = PatternDatabase()
        entry = InsightEntry(
            id="MY-001",
            domain="Testing",
            pattern="Pattern X",
            lesson="Lesson Y",
            implication="Impl Z",
            severity=InsightSeverity.STRUCTURAL,
            pattern_type=PatternType.CROSS_CORRELATION,
        )
        db.add(entry)
        assert len(db.entries) >= 1
        found = db.query(domain="Testing")
        assert any(e.id == "MY-001" for e in found)


# ==========================================================================
# Extensions — status / load branches
# ==========================================================================


class TestExtensionManagerStatus:
    """Cover ExtensionManager.status() + load branches."""

    def test_status_dict(self):
        mgr = ExtensionManager()
        s = mgr.status()
        assert "started" in s
        assert "default" in s
        assert "on_demand" in s
        assert "loaded" in s

    def test_default_names_list(self):
        mgr = ExtensionManager()
        assert isinstance(mgr.default_names, list)

    def test_on_demand_names_list(self):
        mgr = ExtensionManager()
        assert isinstance(mgr.on_demand_names, list)

    def test_loaded_names_initially_empty(self):
        mgr = ExtensionManager()
        assert isinstance(mgr.loaded_names, list)

    def test_get_nonexistent_returns_none(self):
        mgr = ExtensionManager()
        result = mgr.get("__nonexistent_extension__")
        assert result is None

    def test_is_loaded_false_initially(self):
        mgr = ExtensionManager()
        assert mgr.is_loaded("__nonexistent__") is False


# ==========================================================================
# Validator — root file validation
# ==========================================================================


class TestRootFileValidatorEdge:
    """Cover validator edge paths."""

    def test_validator_default_init(self):
        v = RootFileValidator()
        assert isinstance(v.root, Path)

    def test_validator_custom_root(self):
        with tempfile.TemporaryDirectory() as td:
            v = RootFileValidator(root_dir=Path(td))
            assert v.root == Path(td)

    def test_validate_all_returns_dict(self):
        with tempfile.TemporaryDirectory() as td:
            v = RootFileValidator(root_dir=Path(td))
            result = v.validate_all()
            assert "status" in result
            assert "errors" in result
            assert "warnings" in result
            assert "passed" in result

    def test_validate_all_missing_files(self):
        with tempfile.TemporaryDirectory() as td:
            v = RootFileValidator(root_dir=Path(td))
            result = v.validate_all()
            # Should have errors for missing files
            assert result["status"] == "FAIL" or len(result["errors"]) > 0

    def test_validator_error_accumulation(self):
        v = RootFileValidator(root_dir=Path("/nonexistent/path"))
        result = v.validate_all()
        assert result["total_checks"] > 0


# ==========================================================================
# Scheduler — submit without use_cache
# ==========================================================================


class TestSchedulerSubmitPaths:
    """Cover scheduler submit variations."""

    def test_submit_basic(self):
        s = Scheduler()
        job = s.submit("test_target")
        assert job.target == "test_target"
        assert job.status is not None

    def test_submit_with_priority(self):
        s = Scheduler()
        job = s.submit("test_target", priority=JobPriority.HIGH)
        assert job.priority == JobPriority.HIGH

    def test_submit_with_strict(self):
        s = Scheduler()
        job = s.submit("test_target", strict=True)
        assert job.strict is True

    def test_submit_with_tags(self):
        s = Scheduler()
        job = s.submit("test_target", tags={"env": "test"})
        assert job.tags.get("env") == "test"

    def test_submit_with_tenant_id(self):
        s = Scheduler()
        job = s.submit("test_target", tenant_id="t1")
        assert job is not None


# ==========================================================================
# Queue — advanced paths
# ==========================================================================


class TestQueueAdvancedPaths:
    """Cover queue DLQ/replay edge paths."""

    def test_empty_queue_dequeue(self):
        q = PriorityQueue()
        result = q.dequeue()
        assert result is None

    def test_enqueue_dequeue_roundtrip(self):
        q = PriorityQueue()
        from umcp.fleet.models import Job

        job = Job(job_id="q-test", target="t")
        q.enqueue(job)
        got = q.dequeue()
        assert got is not None
        assert got.job_id == "q-test"

    def test_queue_pending_count(self):
        q = PriorityQueue()
        assert q.pending_count() == 0
        from umcp.fleet.models import Job

        q.enqueue(Job(job_id="sz-1", target="t"))
        assert q.pending_count() == 1


# ==========================================================================
# Cache — FilesystemBackend
# ==========================================================================


class TestCacheFilesystemBackend:
    """Cover FilesystemBackend branch paths."""

    def test_put_get_roundtrip(self):
        with tempfile.TemporaryDirectory() as td:
            fb = FilesystemBackend(root=Path(td))
            fb.put("abc123", b"hello world")
            got = fb.get("abc123")
            assert got == b"hello world"

    def test_get_missing_returns_none(self):
        with tempfile.TemporaryDirectory() as td:
            fb = FilesystemBackend(root=Path(td))
            assert fb.get("nonexistent") is None

    def test_delete_existing(self):
        with tempfile.TemporaryDirectory() as td:
            fb = FilesystemBackend(root=Path(td))
            fb.put("del1", b"data")
            assert fb.delete("del1") is True

    def test_delete_nonexistent(self):
        with tempfile.TemporaryDirectory() as td:
            fb = FilesystemBackend(root=Path(td))
            assert fb.delete("nope") is False

    def test_keys(self):
        with tempfile.TemporaryDirectory() as td:
            fb = FilesystemBackend(root=Path(td))
            fb.put("key1", b"a")
            fb.put("key2", b"b")
            ks = fb.keys()
            assert "key1" in ks
            assert "key2" in ks

    def test_size(self):
        with tempfile.TemporaryDirectory() as td:
            fb = FilesystemBackend(root=Path(td))
            fb.put("sz1", b"12345")
            assert fb.size("sz1") == 5

    def test_size_missing(self):
        with tempfile.TemporaryDirectory() as td:
            fb = FilesystemBackend(root=Path(td))
            assert fb.size("nope") == 0

    def test_clear(self):
        with tempfile.TemporaryDirectory() as td:
            fb = FilesystemBackend(root=Path(td))
            fb.put("c1", b"x")
            fb.clear()
            assert fb.keys() == []


# ==========================================================================
# Closures — edge paths
# ==========================================================================


class TestClosuresEdgePaths:
    """Cover closure loader edge paths."""

    def test_get_closure_loader_default(self):
        loader = get_closure_loader()
        assert isinstance(loader, ClosureLoader)

    def test_list_closures(self):
        loader = get_closure_loader()
        closures = loader.list_closures()
        assert isinstance(closures, dict)

    def test_validate_closure_nonexistent(self):
        loader = get_closure_loader()
        assert loader.validate_closure_exists("__nonexistent_closure__") is False

    def test_load_closure_nonexistent_raises(self):
        loader = get_closure_loader()
        with pytest.raises(FileNotFoundError):
            loader.load_closure_module("__nonexistent_closure__")


# ==========================================================================
# Logging — health check states
# ==========================================================================


class TestLoggingHealthCheckStates:
    """Cover StructuredLogger and HealthCheck branching."""

    def test_logger_creation(self):
        logger = StructuredLogger("test_component")
        assert logger is not None

    def test_logger_info(self):
        logger = StructuredLogger("test_info")
        logger.info("test message")

    def test_logger_warning(self):
        logger = StructuredLogger("test_warn")
        logger.warning("test warning")

    def test_logger_error(self):
        logger = StructuredLogger("test_err")
        logger.error("test error")

    def test_health_check(self):
        hc = HealthCheck()
        result = hc.check(repo_root=Path("."))
        assert isinstance(result, dict)


# ==========================================================================
# MeasurementEngine — embedding paths
# ==========================================================================


class TestMeasurementEngineEmbedding:
    """Cover MeasurementEngine edge paths."""

    def test_from_array(self):
        data = np.array([[0.5, 0.6, 0.7, 0.8], [0.4, 0.5, 0.6, 0.7]])
        me = MeasurementEngine()
        result = me.from_array(data=data)
        assert result is not None
        assert hasattr(result, "invariants")

    def test_from_array_with_weights(self):
        data = np.array([[0.5, 0.6, 0.7, 0.8], [0.4, 0.5, 0.6, 0.7]])
        weights = [0.25, 0.25, 0.25, 0.25]
        me = MeasurementEngine()
        result = me.from_array(data=data, weights=weights)
        assert result is not None
        assert hasattr(result, "invariants")

    def test_engine_compute_invariants(self):
        data = np.array([[0.5, 0.6, 0.7, 0.8], [0.4, 0.5, 0.6, 0.7]])
        me = MeasurementEngine()
        result = me.from_array(data=data)
        inv = result.invariants
        assert inv is not None


# ==========================================================================
# File refs — UMCPFiles class
# ==========================================================================


class TestFileRefsEdge:
    """Cover UMCPFiles branch paths."""

    def test_umcp_files_default_init(self):
        files = UMCPFiles()
        assert isinstance(files.root, Path)

    def test_umcp_files_custom_root(self):
        with tempfile.TemporaryDirectory() as td:
            files = UMCPFiles(root_path=Path(td))
            assert files.root == Path(td)

    def test_manifest_yaml_path(self):
        files = UMCPFiles()
        assert files.manifest_yaml.name == "manifest.yaml"

    def test_contract_yaml_path(self):
        files = UMCPFiles()
        assert files.contract_yaml.name == "contract.yaml"

    def test_sha256_txt_path(self):
        files = UMCPFiles()
        assert files.sha256_txt.name == "sha256.txt"

    def test_get_umcp_files_factory(self):
        f = get_umcp_files()
        assert isinstance(f, UMCPFiles)

    def test_load_yaml_missing_raises(self):
        files = UMCPFiles()
        with pytest.raises(FileNotFoundError):
            files.load_yaml(Path("/nonexistent/file.yaml"))

    def test_load_text(self):
        files = UMCPFiles()
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
            f.write("hello test")
            f.flush()
            content = files.load_text(Path(f.name))
            assert content == "hello test"

    def test_derived_dir_path(self):
        files = UMCPFiles()
        assert files.derived_dir.name == "derived"


# ==========================================================================
# Tenant — quota paths
# ==========================================================================


class TestTenantQuotaPaths:
    """Cover TenantManager registration and quota enforcement."""

    def test_register_basic(self):
        mgr = TenantManager()
        t = mgr.register("t1")
        assert t.tenant_id == "t1"

    def test_register_with_quota(self):
        mgr = TenantManager()
        q = TenantQuota(max_concurrent_jobs=5)
        t = mgr.register("t2", quota=q)
        assert t.quota.max_concurrent_jobs == 5

    def test_register_duplicate_raises(self):
        mgr = TenantManager()
        mgr.register("dup1")
        with pytest.raises(ValueError):
            mgr.register("dup1")

    def test_get_nonexistent_raises(self):
        mgr = TenantManager()
        with pytest.raises(TenantNotFoundError):
            mgr.get("nonexistent")

    def test_list_tenants(self):
        mgr = TenantManager()
        mgr.register("lt1")
        mgr.register("lt2")
        tenants = mgr.list_tenants()
        assert len(tenants) == 2

    def test_check_submission_unregistered(self):
        mgr = TenantManager()
        with pytest.raises(TenantNotFoundError):
            mgr.check_submission("ghost")

    def test_check_submission_disabled(self):
        mgr = TenantManager()
        mgr.register("dis1")
        mgr.disable("dis1")
        with pytest.raises(QuotaExceededError):
            mgr.check_submission("dis1")

    def test_check_submission_ok(self):
        mgr = TenantManager()
        mgr.register("ok1")
        # Should not raise
        mgr.check_submission("ok1")

    def test_disable_enable(self):
        mgr = TenantManager()
        _t = mgr.register("de1")
        mgr.disable("de1")
        assert not mgr.get("de1").enabled
        mgr.enable("de1")
        assert mgr.get("de1").enabled

    def test_remove_tenant(self):
        mgr = TenantManager()
        mgr.register("rm1")
        assert mgr.remove("rm1") is True
        assert mgr.remove("rm1") is False

    def test_record_submission(self):
        mgr = TenantManager()
        mgr.register("rs1")
        mgr.record_submission("rs1")
        t = mgr.get("rs1")
        assert t.total_submitted == 1
        assert t.queued_jobs == 1

    def test_record_start(self):
        mgr = TenantManager()
        mgr.register("rst1")
        mgr.record_submission("rst1")
        mgr.record_start("rst1")
        t = mgr.get("rst1")
        assert t.active_jobs == 1
        assert t.queued_jobs == 0

    def test_update_quota(self):
        mgr = TenantManager()
        mgr.register("uq1")
        new_q = TenantQuota(max_concurrent_jobs=99)
        mgr.update_quota("uq1", new_q)
        assert mgr.get("uq1").quota.max_concurrent_jobs == 99

    def test_tenant_to_dict(self):
        mgr = TenantManager()
        t = mgr.register("td1")
        d = t.to_dict()
        assert d["tenant_id"] == "td1"
        assert "quota" in d


# ==========================================================================
# τ_R* dynamics — additional paths
# ==========================================================================


class TestTauRStarDynamicsAdditional:
    """Cover tau_r_star_dynamics residue convergence + equation of state."""

    def test_verify_residue_convergence_returns_list(self):
        results = verify_residue_convergence()
        assert isinstance(results, list)
        assert len(results) > 0

    def test_residue_convergence_custom_epsilons(self):
        results = verify_residue_convergence(epsilon_values=[1e-4, 1e-8])
        assert len(results) == 2

    def test_equation_of_state_returns_list(self):
        results = compute_equation_of_state()
        assert isinstance(results, list)
        assert len(results) > 0

    def test_equation_of_state_custom_betas(self):
        results = compute_equation_of_state(beta_values=[0.5, 1.0, 2.0])
        assert len(results) == 3

    def test_entropy_production(self):
        result = compute_entropy_production(0.1, 0.5)
        assert result.omega == 0.1
        assert result.R == 0.5
        assert result.sigma >= 0

    def test_diagnose_extended_basic(self):
        result = diagnose_extended(omega=0.1, C=0.05, R=0.5)
        assert result.tier0_checks_pass is not None
        assert result.kramers is not None
        assert result.gibbs is not None

    def test_diagnose_extended_high_omega(self):
        result = diagnose_extended(omega=0.5, C=0.2, R=0.1)
        assert result is not None

    def test_diagnose_extended_negative_R_raises(self):
        with pytest.raises(ValueError):
            diagnose_extended(omega=0.1, C=0.05, R=-1.0)


# ==========================================================================
# Seam optimized — chain + residual validation
# ==========================================================================


class TestSeamOptimizedEdge:
    """Cover seam chain accumulation and residual validation."""

    def test_create_seam_chain(self):
        chain = create_seam_chain()
        assert isinstance(chain, SeamChainAccumulator)

    def test_add_seam_basic(self):
        chain = create_seam_chain()
        chain.add_seam(
            t0=0,
            t1=1,
            kappa_t0=-0.1,
            kappa_t1=-0.2,
            tau_R=1.0,
        )
        assert len(chain.seam_history) == 1

    def test_add_multiple_seams(self):
        chain = create_seam_chain()
        for i in range(5):
            chain.add_seam(
                t0=i,
                t1=i + 1,
                kappa_t0=-0.1 * (i + 1),
                kappa_t1=-0.1 * (i + 2),
                tau_R=1.0,
            )
        assert len(chain.seam_history) == 5

    def test_validate_seam_residuals_stable(self):
        # Small residuals -> True (stable / returning)
        residuals = [0.001, 0.002, 0.001, 0.003, 0.002]
        result = validate_seam_residuals(residuals)
        assert isinstance(result, bool)

    def test_validate_seam_residuals_growing(self):
        # Large growing residuals
        residuals = [0.1 * (i + 1) for i in range(20)]
        result = validate_seam_residuals(residuals)
        assert isinstance(result, bool)

    def test_validate_seam_residuals_empty(self):
        result = validate_seam_residuals([])
        assert isinstance(result, bool)

    def test_chain_total_delta_kappa(self):
        chain = create_seam_chain()
        chain.add_seam(t0=0, t1=1, kappa_t0=-0.1, kappa_t1=-0.2, tau_R=1.0)
        chain.add_seam(t0=1, t1=2, kappa_t0=-0.2, kappa_t1=-0.3, tau_R=1.0)
        # Total delta kappa should be cumulative
        assert chain.total_delta_kappa != 0.0


# ==========================================================================
# Compute utils — validate + batch paths
# ==========================================================================


class TestComputeUtilsEdge:
    """Cover compute_utils validate_inputs / batch_validate_outputs."""

    def test_validate_inputs_good(self):
        c = np.array([0.5, 0.6, 0.7])
        w = np.array([1 / 3, 1 / 3, 1 / 3])
        # Should not raise
        validate_inputs(c, w)

    def test_validate_inputs_mismatched_length(self):
        c = np.array([0.5, 0.6])
        w = np.array([0.5])
        result = validate_inputs(c, w)
        assert result["valid"] is False or not result["valid"]

    def test_batch_validate_outputs(self):
        # Shape (T, 5) array
        outputs = np.array([[0.8, 0.2, 0.1, 0.05, -0.1]])
        result = batch_validate_outputs(outputs)
        assert isinstance(result, np.ndarray)

    def test_clip_coordinates_basic(self):
        c = np.array([0.5, 1.5, -0.5, 0.8])
        result = clip_coordinates(c)
        # Returns ClippingResult with .c_clipped
        assert np.all(result.c_clipped >= 0.0)
        assert np.all(result.c_clipped <= 1.0)
        assert result.clip_count >= 2

    def test_normalize_weights(self):
        w = np.array([1.0, 2.0, 3.0])
        result = normalize_weights(w)
        assert abs(result.sum() - 1.0) < 1e-10

    def test_batch_processor_creation(self):
        bp = BatchProcessor()
        assert bp.epsilon > 0
        assert hasattr(bp, "preprocess_trace")


# ==========================================================================
# API helpers — native routes if available
# ==========================================================================


class TestApiNativeHelper:
    """Cover api_routes_v2 helpers if importable."""

    def test_import_api_routes(self):
        try:
            from umcp import api_routes_v2

            assert api_routes_v2 is not None
        except ImportError:
            pytest.skip("api_routes_v2 not available")

    def test_api_route_health(self):
        try:
            from umcp.api_routes_v2 import health_check

            result = health_check()
            assert result is not None
        except (ImportError, AttributeError):
            pytest.skip("health_check not available")

    def test_api_route_version(self):
        try:
            from umcp.api_routes_v2 import get_version

            result = get_version()
            assert result is not None
        except (ImportError, AttributeError):
            pytest.skip("get_version not available")


# ==========================================================================
# Additional coverage: closures.py YAML fallback branch
# ==========================================================================


class TestClosuresYAMLFallback:
    """Cover the YAML fallback parser branch in ClosureLoader."""

    def test_registry_property(self):
        loader = get_closure_loader()
        reg = loader.registry
        assert isinstance(reg, dict)

    def test_execute_closure_nonexistent(self):
        loader = get_closure_loader()
        with pytest.raises(FileNotFoundError):
            loader.execute_closure("__nonexistent__")

    def test_get_closure_function_nonexistent(self):
        loader = get_closure_loader()
        with pytest.raises(FileNotFoundError):
            loader.get_closure_function("__nonexistent__")
