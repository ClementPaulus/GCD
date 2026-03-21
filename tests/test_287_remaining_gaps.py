"""Tests for coverage gaps in seam_optimized, compute_utils, logging_utils, measurement_engine.

Targets uncovered branches across these four modules.
"""

from __future__ import annotations

import json
import math
from typing import Any

import numpy as np
import pytest

from umcp.compute_utils import (
    batch_validate_outputs,
    clip_coordinates,
    normalize_weights,
    prune_zero_weights,
    validate_inputs,
)
from umcp.logging_utils import (
    HealthCheck,
    JsonFormatter,
    PerformanceMetrics,
    StructuredLogger,
    get_logger,
)
from umcp.measurement_engine import (
    EmbeddingConfig,
    EmbeddingSpec,
    EmbeddingStrategy,
    EngineResult,
    InvariantRow,
    MeasurementEngine,
    TraceRow,
    safe_tau_R,
    tau_R_display,
)
from umcp.seam_optimized import (
    ResidualBoundCalculator,
    SeamCompositionAnalyzer,
    create_seam_chain,
    validate_seam_residuals,
)

# =====================================================================
# SeamCompositionAnalyzer
# =====================================================================


class TestSeamCompositionAnalyzer:
    def test_validate_empty_chain(self) -> None:
        chain = create_seam_chain()
        result = SeamCompositionAnalyzer.validate_composition_law(chain, 0, 10)
        assert not result["valid"]
        assert "Empty chain" in result["reason"]

    def test_validate_no_seams_in_range(self) -> None:
        chain = create_seam_chain()
        chain.add_seam(0, 1, -0.1, -0.15, 1.0, R=0.01)
        result = SeamCompositionAnalyzer.validate_composition_law(chain, 100, 200)
        assert not result["valid"]

    def test_validate_composition_law(self) -> None:
        chain = create_seam_chain()
        chain.add_seam(0, 1, -0.10, -0.15, 1.0, R=0.01)
        chain.add_seam(1, 2, -0.15, -0.20, 1.0, R=0.01)
        chain.add_seam(2, 3, -0.20, -0.25, 1.0, R=0.01)
        result = SeamCompositionAnalyzer.validate_composition_law(chain, 0, 3)
        assert result["valid"]
        assert abs(result["composed_total"] - result["direct_total"]) < 1e-9

    def test_analyze_residual_pattern_empty(self) -> None:
        result = SeamCompositionAnalyzer.analyze_residual_pattern([])
        assert not result["valid"]

    def test_analyze_residual_pattern_short(self) -> None:
        result = SeamCompositionAnalyzer.analyze_residual_pattern([0.01, -0.01, 0.005])
        assert result["valid"]
        assert result["count"] == 3

    def test_analyze_residual_pattern_long(self) -> None:
        rng = np.random.default_rng(42)
        residuals = rng.normal(0, 0.01, 50).tolist()
        result = SeamCompositionAnalyzer.analyze_residual_pattern(residuals)
        assert result["valid"]
        assert result["is_sublinear"]
        assert "is_centered" in result


class TestResidualBoundCalculator:
    def test_compute_residual_sensitivity(self) -> None:
        sens = ResidualBoundCalculator.compute_residual_sensitivity(
            tau_R=5.0, R=0.01, D_omega=0.1, D_C=0.05, delta_kappa_ledger=-0.1
        )
        assert sens["ds_dR"] == 5.0
        assert sens["ds_dtau_R"] == 0.01
        assert sens["ds_dD_omega"] == -1.0
        assert sens["ds_dD_C"] == -1.0
        assert sens["ds_dkappa_ledger"] == -1.0


class TestSeamAccumulatorExtra:
    def test_get_metrics_empty(self) -> None:
        chain = create_seam_chain()
        m = chain.get_metrics()
        assert m.total_seams == 0
        assert m.is_returning is False

    def test_growth_exponent_short(self) -> None:
        chain = create_seam_chain()
        for i in range(5):
            chain.add_seam(i, i + 1, -0.1 * i, -0.1 * (i + 1), 1.0, R=0.01)
        assert chain._compute_growth_exponent() == 0.0

    def test_validate_seam_residuals_short(self) -> None:
        assert validate_seam_residuals([0.01, 0.02]) is True

    def test_validate_seam_residuals_bounded(self) -> None:
        rng = np.random.default_rng(42)
        residuals = rng.normal(0, 0.001, 50).tolist()
        assert validate_seam_residuals(residuals) is True


# =====================================================================
# compute_utils
# =====================================================================


class TestComputeUtilsGaps:
    def test_validate_inputs_negative_weights(self) -> None:
        c = np.array([0.5, 0.5])
        w = np.array([-0.5, 1.5])
        result = validate_inputs(c, w)
        assert not result["valid"]
        assert "negative" in str(result["errors"])

    def test_validate_inputs_nan_coords(self) -> None:
        c = np.array([0.5, np.nan])
        w = np.array([0.5, 0.5])
        result = validate_inputs(c, w)
        assert not result["valid"]
        assert "NaN" in str(result["errors"])

    def test_validate_inputs_inf_weights(self) -> None:
        c = np.array([0.5, 0.5])
        w = np.array([0.5, np.inf])
        result = validate_inputs(c, w)
        assert not result["valid"]

    def test_validate_inputs_dim_mismatch(self) -> None:
        c = np.array([0.5, 0.5, 0.5])
        w = np.array([0.5, 0.5])
        result = validate_inputs(c, w)
        assert not result["valid"]
        assert "mismatch" in str(result["errors"])

    def test_validate_inputs_out_of_range(self) -> None:
        c = np.array([0.5, 1.5])
        w = np.array([0.5, 0.5])
        result = validate_inputs(c, w)
        assert not result["valid"]
        assert "outside" in str(result["errors"])

    def test_validate_inputs_valid(self) -> None:
        c = np.array([0.5, 0.8])
        w = np.array([0.5, 0.5])
        result = validate_inputs(c, w)
        assert result["valid"]
        assert result["errors"] == ""

    def test_batch_validate_outputs(self) -> None:
        outputs = np.array(
            [
                [0.9, 0.1, 0.1, 0.85, -0.16],
                [0.5, 0.5, 0.5, 0.45, -0.8],
                [1.1, -0.1, 0.0, 0.5, -0.5],  # F > 1, omega < 0 → invalid
            ]
        )
        valid = batch_validate_outputs(outputs)
        assert valid[0]
        assert not valid[2]

    def test_prune_zero_weights_all_zero(self) -> None:
        c = np.array([0.5, 0.5])
        w = np.array([0.0, 0.0])
        with pytest.raises(ValueError, match="All weights"):
            prune_zero_weights(c, w)

    def test_prune_zero_weights_partial(self) -> None:
        c = np.array([0.9, 0.5, 0.7])
        w = np.array([0.5, 0.0, 0.5])
        result = prune_zero_weights(c, w)
        assert result.n_active == 2
        assert 1 in result.pruned_indices

    def test_normalize_weights_negative(self) -> None:
        w = np.array([-0.5, 1.5])
        with pytest.raises(ValueError, match="non-negative"):
            normalize_weights(w)

    def test_clip_coordinates_with_weights(self) -> None:
        c = np.array([0.5, -0.1, 1.2])
        w = np.array([1 / 3, 1 / 3, 1 / 3])
        result = clip_coordinates(c, w=w)
        assert result.clip_count == 2
        assert len(result.oor_indices) == 2


# =====================================================================
# logging_utils
# =====================================================================


class TestLoggingUtilsGaps:
    def test_json_formatter(self) -> None:
        import logging

        formatter = JsonFormatter()
        record = logging.LogRecord(
            name="test",
            level=logging.INFO,
            pathname="",
            lineno=0,
            msg="test message",
            args=(),
            exc_info=None,
        )
        output = formatter.format(record)
        data = json.loads(output)
        assert data["message"] == "test message"
        assert data["level"] == "INFO"

    def test_json_formatter_with_context(self) -> None:
        import logging

        formatter = JsonFormatter()
        record = logging.LogRecord(
            name="test",
            level=logging.WARNING,
            pathname="",
            lineno=0,
            msg="ctx msg",
            args=(),
            exc_info=None,
        )
        record.context = {"key": "value"}  # type: ignore[attr-defined]
        output = formatter.format(record)
        data = json.loads(output)
        assert data["context"]["key"] == "value"

    def test_structured_logger_json_output(self) -> None:
        logger = StructuredLogger(name="test_json", json_output=True, level=10)
        # Should not raise
        logger.debug("debug msg")
        logger.info("info msg")
        logger.warning("warn msg")
        logger.error("error msg")
        logger.critical("critical msg")

    def test_operation_context_success(self) -> None:
        logger = StructuredLogger(name="test_op", level=10)
        with logger.operation("test_op") as metrics:
            pass  # do nothing
        assert metrics.duration_ms is not None
        assert metrics.duration_ms >= 0

    def test_operation_context_failure(self) -> None:
        logger = StructuredLogger(name="test_op_fail", level=10)
        with pytest.raises(ValueError, match="boom"), logger.operation("failing_op") as metrics:
            raise ValueError("boom")
        assert metrics.duration_ms is not None

    def test_performance_metrics_to_dict_no_memory(self) -> None:
        m = PerformanceMetrics(operation="test")
        m.finish()
        d = m.to_dict()
        assert d["operation"] == "test"
        assert d["duration_ms"] is not None
        assert "memory_mb" not in d  # not set

    def test_health_check(self, tmp_path: Any) -> None:
        # Create required dirs
        (tmp_path / "schemas").mkdir()
        (tmp_path / "contracts").mkdir()
        (tmp_path / "closures").mkdir()
        # Create a schema file
        (tmp_path / "schemas" / "test.json").write_text("{}")

        health = HealthCheck.check(tmp_path)
        assert health["status"] == "healthy"
        assert health["checks"]["dir_schemas"]["status"] == "pass"

    def test_health_check_missing_dirs(self, tmp_path: Any) -> None:
        health = HealthCheck.check(tmp_path)
        assert health["status"] == "unhealthy"

    def test_get_logger_singleton(self) -> None:
        import umcp.logging_utils as lu

        lu._default_logger = None
        logger1 = get_logger()
        logger2 = get_logger()
        assert logger1 is logger2
        lu._default_logger = None  # cleanup


# =====================================================================
# measurement_engine
# =====================================================================


class TestMeasurementEngineGaps:
    def test_from_array_1d(self) -> None:
        engine = MeasurementEngine()
        data = np.array([0.1, 0.5, 0.9])
        result = engine.from_array(data)
        assert result.n_dims == 1
        assert result.n_timesteps == 3

    def test_from_array_2d(self) -> None:
        engine = MeasurementEngine()
        data = np.array([[0.9, 0.8], [0.85, 0.75], [0.7, 0.6]])
        result = engine.from_array(data, weights=[0.6, 0.4])
        assert result.n_dims == 2
        assert result.n_timesteps == 3

    def test_from_array_with_nan(self) -> None:
        engine = MeasurementEngine()
        data = np.array([[0.9, np.nan], [0.8, 0.7]])
        result = engine.from_array(data)
        assert result.n_timesteps == 2
        # NaN imputed to column mean

    def test_embedding_zscore_sigmoid(self) -> None:
        engine = MeasurementEngine()
        config = EmbeddingConfig(
            default_strategy=EmbeddingStrategy.ZSCORE_SIGMOID,
        )
        data = np.array([[10.0, 20.0], [30.0, 40.0], [50.0, 60.0]])
        result = engine.from_array(data, embedding=config)
        assert result.n_timesteps == 3
        # Sigmoid output should be in [0,1]
        coords = result.coordinates_array
        assert np.all(coords >= 0) and np.all(coords <= 1)

    def test_embedding_max_norm(self) -> None:
        engine = MeasurementEngine()
        config = EmbeddingConfig(
            default_strategy=EmbeddingStrategy.MAX_NORM,
        )
        data = np.array([[5.0, 10.0], [3.0, 8.0]])
        result = engine.from_array(data, embedding=config)
        assert result.n_timesteps == 2

    def test_embedding_linear_scale(self) -> None:
        engine = MeasurementEngine()
        config = EmbeddingConfig(
            specs=[
                EmbeddingSpec(strategy=EmbeddingStrategy.LINEAR_SCALE, input_range=(0.0, 100.0)),
                EmbeddingSpec(strategy=EmbeddingStrategy.LINEAR_SCALE, input_range=(0.0, 50.0)),
            ],
        )
        data = np.array([[50.0, 25.0], [75.0, 37.5]])
        result = engine.from_array(data, embedding=config)
        assert result.n_timesteps == 2

    def test_embedding_constant_column(self) -> None:
        """Constant column → embedded as 0.5."""
        engine = MeasurementEngine()
        data = np.array([[5.0, 5.0], [5.0, 5.0], [5.0, 5.0]])
        result = engine.from_array(data)
        # MIN_MAX with zero range → 0.5
        coords = result.coordinates_array
        assert np.allclose(coords, 0.5, atol=0.01)

    def test_from_csv(self, tmp_path: Any) -> None:
        csv_file = tmp_path / "data.csv"
        csv_file.write_text("t,a,b\n0,0.9,0.8\n1,0.7,0.6\n2,0.5,0.4\n")
        engine = MeasurementEngine()
        result = engine.from_csv(csv_file)
        assert result.n_dims == 2
        assert result.n_timesteps == 3

    def test_from_csv_no_t_column(self, tmp_path: Any) -> None:
        csv_file = tmp_path / "data.csv"
        csv_file.write_text("x,y\n0.9,0.8\n0.7,0.6\n")
        engine = MeasurementEngine()
        result = engine.from_csv(csv_file)
        assert result.n_dims == 2

    def test_write_psi_csv(self, tmp_path: Any) -> None:
        engine = MeasurementEngine()
        data = np.array([[0.9, 0.8], [0.7, 0.6]])
        result = engine.from_array(data)
        out = tmp_path / "psi.csv"
        engine.write_psi_csv(result, out)
        assert out.exists()

    def test_write_invariants_json(self, tmp_path: Any) -> None:
        engine = MeasurementEngine()
        data = np.array([[0.9, 0.8], [0.7, 0.6]])
        result = engine.from_array(data)
        out = tmp_path / "invariants.json"
        engine.write_invariants_json(result, out)
        assert out.exists()
        inv = json.loads(out.read_text())
        assert "rows" in inv

    def test_generate_casepack(self, tmp_path: Any) -> None:
        engine = MeasurementEngine()
        data = np.array([[0.9, 0.8], [0.7, 0.6]])
        result = engine.from_array(data)
        cp_dir = tmp_path / "test_casepack"
        engine.generate_casepack(result, cp_dir, title="Test")
        assert (cp_dir / "manifest.json").exists()
        assert (cp_dir / "expected" / "psi.csv").exists()
        assert (cp_dir / "expected" / "invariants.json").exists()

    def test_engine_result_properties(self) -> None:
        engine = MeasurementEngine()
        data = np.array([[0.9, 0.8], [0.7, 0.6], [0.5, 0.4]])
        result = engine.from_array(data)
        assert len(result.regimes) == 3
        assert result.final_regime in {"STABLE", "WATCH", "COLLAPSE", "CRITICAL"}
        assert result.coordinates_array.shape == (3, 2)
        s = result.summary()
        assert "n_timesteps" in s
        assert "regime_counts" in s

    def test_weight_mismatch(self) -> None:
        engine = MeasurementEngine()
        data = np.array([[0.9, 0.8]])
        with pytest.raises(ValueError, match="mismatch"):
            engine.from_array(data, weights=[0.5])

    def test_write_psi_empty_trace(self, tmp_path: Any) -> None:
        result = EngineResult(
            trace=[],
            invariants=[],
            weights=[],
            n_dims=0,
            n_timesteps=0,
            embedding_config=EmbeddingConfig(),
        )
        with pytest.raises(ValueError, match="empty"):
            MeasurementEngine.write_psi_csv(result, tmp_path / "empty.csv")


# =====================================================================
# safe_tau_R and tau_R_display
# =====================================================================


class TestTauRHelpers:
    def test_safe_tau_R_none(self) -> None:
        assert math.isinf(safe_tau_R(None))

    def test_safe_tau_R_inf_rec(self) -> None:
        assert math.isinf(safe_tau_R("INF_REC"))

    def test_safe_tau_R_float_inf(self) -> None:
        assert math.isinf(safe_tau_R(float("inf")))

    def test_safe_tau_R_nan(self) -> None:
        assert math.isinf(safe_tau_R(float("nan")))

    def test_safe_tau_R_numeric(self) -> None:
        assert safe_tau_R(5) == 5.0
        assert safe_tau_R(3.14) == 3.14

    def test_safe_tau_R_string_infinity(self) -> None:
        assert math.isinf(safe_tau_R("∞"))
        assert math.isinf(safe_tau_R("infinity"))
        assert math.isinf(safe_tau_R("NONE"))
        assert math.isinf(safe_tau_R(""))

    def test_safe_tau_R_invalid_string(self) -> None:
        assert math.isinf(safe_tau_R("not_a_number"))

    def test_tau_R_display_inf(self) -> None:
        assert tau_R_display(float("inf")) == "INF_REC"

    def test_tau_R_display_numeric(self) -> None:
        assert tau_R_display(5) == "5"
        assert tau_R_display(3.14) == "3.14"

    def test_tau_R_display_none(self) -> None:
        assert tau_R_display(None) == "INF_REC"


# =====================================================================
# InvariantRow
# =====================================================================


class TestInvariantRow:
    def test_to_dict_finite(self) -> None:
        row = InvariantRow(
            t=0,
            omega=0.1,
            F=0.9,
            S=0.2,
            C=0.1,
            tau_R=5.0,
            kappa=-0.1,
            IC=0.9,
            regime="STABLE",
            critical_overlay=False,
        )
        d = row.to_dict()
        assert d["tau_R"] == 5.0
        assert d["regime"]["label"] == "Stable"

    def test_to_dict_inf(self) -> None:
        row = InvariantRow(
            t=0,
            omega=0.5,
            F=0.5,
            S=0.6,
            C=0.5,
            tau_R=float("inf"),
            kappa=-0.7,
            IC=0.5,
            regime="COLLAPSE",
            critical_overlay=False,
        )
        d = row.to_dict()
        assert d["tau_R"] == "INF_REC"


# =====================================================================
# TraceRow
# =====================================================================


class TestTraceRow:
    def test_to_csv_wide_dict(self) -> None:
        row = TraceRow(t=0, c=[0.9, 0.8], oor=[False, False], miss=[False, False])
        d = row.to_csv_wide_dict()
        assert d["t"] == 0
        assert d["c_1"] == 0.9
        assert d["c_2"] == 0.8
        assert not d["oor_1"]
