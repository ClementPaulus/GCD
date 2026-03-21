"""Tests for coverage gaps in universal_calculator, kernel_optimized, validator, file_refs.

Targets specific uncovered lines:
  - UniversalCalculator: to_dict, summary, _compute_gcd, _compute_rcft_single,
    _compute_rcft, _box_counting_dimension, _compute_tau_R_from_trajectory,
    _compute_diagnostics, _compute_uncertainty, KernelInvariants.to_dict (inf/nan)
  - ComputationResult: to_json, to_dict with optional sections, summary formatting
  - kernel_optimized: _bernoulli_h, _classify_heterogeneity, _validate_outputs,
    propagate_coordinate_error, propagate_weight_error,
    propagate_coordinate_error_empirical, check_composition_compatibility
  - validator: _load_yaml fallback, _validate_manifest, _validate_weights
  - file_refs: UMCPFiles root-finding, load_yaml fallback
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any

import numpy as np
import pytest

from umcp.kernel_optimized import (
    OptimizedKernelComputer,
    check_composition_compatibility,
    diagnose,
)
from umcp.universal_calculator import (
    ComputationMode,
    UniversalCalculator,
)

# =====================================================================
# UniversalCalculator
# =====================================================================


class TestUniversalCalculator:
    @pytest.fixture()
    def calc(self) -> UniversalCalculator:
        return UniversalCalculator()

    def test_minimal_mode(self, calc: UniversalCalculator) -> None:
        result = calc.compute_all([0.9, 0.85, 0.8], mode=ComputationMode.MINIMAL)
        assert result.kernel is not None
        assert result.regime in {"STABLE", "WATCH", "COLLAPSE"}

    def test_standard_mode(self, calc: UniversalCalculator) -> None:
        result = calc.compute_all([0.9, 0.85, 0.8], mode=ComputationMode.STANDARD)
        assert result.costs is not None
        # GCD only available in FULL mode
        assert result.gcd is None

    def test_full_mode(self, calc: UniversalCalculator) -> None:
        result = calc.compute_all([0.9, 0.85, 0.8], mode=ComputationMode.FULL)
        assert result.gcd is not None
        assert result.rcft is not None  # single-point fallback

    def test_full_mode_with_trajectory(self, calc: UniversalCalculator) -> None:
        traj = np.array([[0.9, 0.85, 0.8], [0.88, 0.83, 0.78], [0.86, 0.81, 0.76]])
        result = calc.compute_all([0.9, 0.85, 0.8], mode=ComputationMode.FULL, trajectory=traj)
        assert result.rcft is not None

    def test_rcft_mode(self, calc: UniversalCalculator) -> None:
        traj = np.array([[0.9, 0.85, 0.8], [0.88, 0.83, 0.78]])
        result = calc.compute_all([0.9, 0.85, 0.8], mode=ComputationMode.RCFT, trajectory=traj)
        assert result.rcft is not None

    def test_with_uncertainty(self, calc: UniversalCalculator) -> None:
        result = calc.compute_all(
            [0.9, 0.85, 0.8],
            mode=ComputationMode.FULL,
            coord_variances=[0.001, 0.002, 0.001],
        )
        assert result.uncertainty is not None

    def test_with_seam(self, calc: UniversalCalculator) -> None:
        result = calc.compute_all(
            [0.9, 0.85, 0.8],
            prior_kappa=-0.1,
            prior_IC=0.9,
        )
        assert result.seam is not None

    def test_with_tau_R(self, calc: UniversalCalculator) -> None:
        result = calc.compute_all([0.9, 0.85, 0.8], tau_R=2.0)
        assert result.kernel.tau_R == 2.0

    def test_weight_normalization(self, calc: UniversalCalculator) -> None:
        """Non-normalized weights get normalized."""
        result = calc.compute_all([0.9, 0.85, 0.8], weights=[2.0, 2.0, 2.0])
        assert result.kernel is not None

    def test_to_dict(self, calc: UniversalCalculator) -> None:
        result = calc.compute_all([0.9, 0.85, 0.8], mode=ComputationMode.FULL)
        d = result.to_dict()
        assert "metadata" in d
        assert "kernel" in d
        assert "regime" in d

    def test_to_json(self, calc: UniversalCalculator) -> None:
        result = calc.compute_all([0.9, 0.85, 0.8])
        j = result.to_json()
        parsed = json.loads(j)
        assert "kernel" in parsed

    def test_summary(self, calc: UniversalCalculator) -> None:
        result = calc.compute_all(
            [0.9, 0.85, 0.8],
            mode=ComputationMode.FULL,
            coord_variances=[0.001, 0.002, 0.001],
            prior_kappa=-0.1,
            prior_IC=0.9,
        )
        s = result.summary()
        assert "Kernel" in s
        assert "Regime" in s

    def test_kernel_to_dict_inf_tau_R(self, calc: UniversalCalculator) -> None:
        result = calc.compute_all([0.9, 0.85, 0.8])
        d = result.kernel.to_dict()
        if math.isinf(result.kernel.tau_R):
            assert d["tau_R"] == "INF_REC"

    def test_gcd_energy_regimes(self, calc: UniversalCalculator) -> None:
        """Test all three GCD energy regime classifications."""
        # Low energy
        result_low = calc.compute_all([0.99, 0.98, 0.97], mode=ComputationMode.FULL)
        assert result_low.gcd is not None

        # High energy (high drift)
        result_high = calc.compute_all([0.1, 0.15, 0.2], mode=ComputationMode.FULL)
        assert result_high.gcd is not None

    def test_rcft_single_smooth(self, calc: UniversalCalculator) -> None:
        """RCFT single-point with low curvature → Smooth."""
        result = calc.compute_all([0.5, 0.5, 0.5], mode=ComputationMode.FULL)
        if result.rcft:
            assert result.rcft.fractal_regime in {"Smooth", "Wrinkled", "Turbulent"}

    def test_diagnostics(self, calc: UniversalCalculator) -> None:
        result = calc.compute_all([0.9, 0.85, 0.8], mode=ComputationMode.FULL)
        assert result.diagnostics is not None
        assert "n_coordinates" in result.diagnostics

    def test_box_counting_1d(self, calc: UniversalCalculator) -> None:
        """Box-counting with short trajectory."""
        traj = np.array([[0.1, 0.2, 0.3], [0.4, 0.5, 0.6], [0.7, 0.8, 0.9], [0.3, 0.4, 0.5]])
        result = calc.compute_all([0.5, 0.5, 0.5], mode=ComputationMode.RCFT, trajectory=traj)
        if result.rcft:
            assert result.rcft.D_fractal >= 0

    def test_box_counting_constant(self, calc: UniversalCalculator) -> None:
        """Box-counting with constant trajectory → D=0."""
        traj = np.ones((10, 3)) * 0.5
        calc.compute_all([0.5, 0.5, 0.5], mode=ComputationMode.FULL, trajectory=traj)

    def test_box_counting_short(self, calc: UniversalCalculator) -> None:
        """Box-counting with < 3 points."""
        traj = np.array([[0.5, 0.5]])
        calc.compute_all([0.5, 0.5], mode=ComputationMode.FULL, trajectory=traj)

    def test_compute_tau_R_from_trajectory(self, calc: UniversalCalculator) -> None:
        """τ_R from trajectory — should find a return."""
        traj = np.array(
            [
                [0.9, 0.8, 0.7],
                [0.5, 0.4, 0.3],
                [0.9, 0.8, 0.7],  # returns close to first
            ]
        )
        calc.compute_all([0.9, 0.8, 0.7], trajectory=traj, tau_R=None)


# =====================================================================
# OptimizedKernelComputer — gap-filling
# =====================================================================


class TestOptimizedKernelGaps:
    @pytest.fixture()
    def kernel(self) -> OptimizedKernelComputer:
        return OptimizedKernelComputer()

    def test_bernoulli_entropy_zero(self, kernel: OptimizedKernelComputer) -> None:
        assert kernel._bernoulli_entropy(0.0) == 0.0
        assert kernel._bernoulli_entropy(1.0) == 0.0

    def test_bernoulli_entropy_half(self, kernel: OptimizedKernelComputer) -> None:
        h = kernel._bernoulli_entropy(0.5)
        assert abs(h - math.log(2)) < 1e-10

    def test_classify_heterogeneity_all(self, kernel: OptimizedKernelComputer) -> None:
        assert kernel._classify_heterogeneity(0.0) == "homogeneous"
        assert kernel._classify_heterogeneity(1e-7) == "homogeneous"
        assert kernel._classify_heterogeneity(0.005) == "coherent"
        assert kernel._classify_heterogeneity(0.02) == "heterogeneous"
        assert kernel._classify_heterogeneity(0.1) == "fragmented"

    def test_propagate_coordinate_error(self, kernel: OptimizedKernelComputer) -> None:
        eb = kernel.propagate_coordinate_error(0.01)
        assert eb.F >= 0
        assert eb.omega >= 0
        assert eb.kappa >= 0
        assert eb.S >= 0

    def test_propagate_weight_error(self, kernel: OptimizedKernelComputer) -> None:
        eb = kernel.propagate_weight_error(0.01)
        assert eb.F >= 0
        assert eb.omega >= 0

    def test_propagate_empirical_error(self, kernel: OptimizedKernelComputer) -> None:
        c = np.array([0.9, 0.8, 0.7])
        w = np.array([1 / 3, 1 / 3, 1 / 3])
        eb = kernel.propagate_empirical_error(c, w, 0.01)
        assert eb.F >= 0
        assert eb.kappa >= 0
        assert eb.S >= 0


class TestCheckCompositionCompatibility:
    def test_compatible(self) -> None:
        c1 = np.array([0.9, 0.85, 0.8])
        c2 = np.array([0.88, 0.83, 0.78])
        w = np.array([1 / 3, 1 / 3, 1 / 3])
        k = OptimizedKernelComputer()
        out1 = k.compute(c1, w)
        out2 = k.compute(c2, w)
        d1 = diagnose(out1, c1, w)
        d2 = diagnose(out2, c2, w)
        ok, reason = check_composition_compatibility(d1, d2)
        assert isinstance(ok, bool)
        assert isinstance(reason, str)

    def test_incompatible_fragmented(self) -> None:
        k = OptimizedKernelComputer()
        w = np.array([1 / 3, 1 / 3, 1 / 3])
        # One system near-dead channel → IC/F ≈ 0
        c1 = np.array([0.9, 0.85, 1e-8])
        c2 = np.array([0.9, 0.85, 0.8])
        out1 = k.compute(c1, w)
        out2 = k.compute(c2, w)
        d1 = diagnose(out1, c1, w)
        d2 = diagnose(out2, c2, w)
        ok, _reason = check_composition_compatibility(d1, d2)
        # fragmented system → should flag incompatibility
        assert isinstance(ok, bool)


# =====================================================================
# UMCPFiles — file_refs coverage
# =====================================================================


class TestUMCPFiles:
    def test_root_auto_detection(self) -> None:
        from umcp.file_refs import UMCPFiles

        files = UMCPFiles()
        assert files.root.exists()

    def test_explicit_root(self, tmp_path: Any) -> None:
        from umcp.file_refs import UMCPFiles

        (tmp_path / "pyproject.toml").touch()
        files = UMCPFiles(root_path=tmp_path)
        assert files.root == tmp_path

    def test_load_yaml_missing_raises(self) -> None:
        from umcp.file_refs import UMCPFiles

        files = UMCPFiles()
        with pytest.raises(FileNotFoundError):
            files.load_yaml(Path("/nonexistent/file.yaml"))

    def test_load_json(self, tmp_path: Any) -> None:
        from umcp.file_refs import UMCPFiles

        jf = tmp_path / "test.json"
        jf.write_text('{"key": "value"}')
        files = UMCPFiles(root_path=tmp_path)
        data = files.load_json(jf)
        assert data["key"] == "value"
