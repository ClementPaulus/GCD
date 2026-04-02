"""Tests for atomic physics theorems (T-AP-1 through T-AP-10).

Validates 118-element periodic kernel structural theorems:
block ordering, period trends, noble gas extrema, magic numbers.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

_WORKSPACE = Path(__file__).resolve().parents[1]
if str(_WORKSPACE) not in sys.path:
    sys.path.insert(0, str(_WORKSPACE))

from closures.atomic_physics.atomic_theorems import (
    _all_results,
    verify_all_theorems,
    verify_t_ap_1,
    verify_t_ap_2,
    verify_t_ap_3,
    verify_t_ap_4,
    verify_t_ap_5,
    verify_t_ap_6,
    verify_t_ap_7,
    verify_t_ap_8,
    verify_t_ap_9,
    verify_t_ap_10,
)


@pytest.fixture(scope="module")
def all_results():
    return _all_results()


class TestTier1Identities:
    """Verify Tier-1 identities hold for all 118 elements."""

    def test_element_count(self, all_results):
        assert len(all_results) == 118

    @pytest.mark.parametrize("idx", range(118))
    def test_duality_identity(self, all_results, idx):
        r = all_results[idx]
        assert abs(r.F + r.omega - 1.0) < 1e-12

    @pytest.mark.parametrize("idx", range(118))
    def test_integrity_bound(self, all_results, idx):
        r = all_results[idx]
        assert r.IC <= r.F + 1e-12

    @pytest.mark.parametrize("idx", range(118))
    def test_log_integrity_relation(self, all_results, idx):
        import math

        r = all_results[idx]
        assert abs(r.IC - math.exp(r.kappa)) < 1e-4


class TestTheorems:
    """Validate all 10 atomic physics theorems."""

    def test_t_ap_1_block_fidelity_ordering(self, all_results):
        assert verify_t_ap_1(all_results)["passed"]

    def test_t_ap_2_noble_gas_ic_maximum(self, all_results):
        assert verify_t_ap_2(all_results)["passed"]

    def test_t_ap_3_alkali_drift_maximum(self, all_results):
        assert verify_t_ap_3(all_results)["passed"]

    def test_t_ap_4_period_trend(self, all_results):
        assert verify_t_ap_4(all_results)["passed"]

    def test_t_ap_5_magic_number_signature(self, all_results):
        assert verify_t_ap_5(all_results)["passed"]

    def test_t_ap_6_heterogeneity_gap_block_separation(self, all_results):
        assert verify_t_ap_6(all_results)["passed"]

    def test_t_ap_7_radioactive_regime(self, all_results):
        assert verify_t_ap_7(all_results)["passed"]

    def test_t_ap_8_lanthanide_contraction(self, all_results):
        assert verify_t_ap_8(all_results)["passed"]

    def test_t_ap_9_electronegativity_correlation(self, all_results):
        assert verify_t_ap_9(all_results)["passed"]

    def test_t_ap_10_category_exhaustive(self, all_results):
        assert verify_t_ap_10(all_results)["passed"]

    def test_all_theorems_pass(self):
        for t in verify_all_theorems():
            assert t["passed"], f"{t['name']} failed: {t}"
