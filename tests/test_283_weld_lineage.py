"""Tests for umcp.weld_lineage — edition identity, SS1m receipts, weld lineage.

Covers:
  - EditionIdentity construction & fields
  - compute_extended_triad() deterministic checksums
  - verify_extended_triad() pass and fail
  - SS1mReceipt: compact(), to_dict(), chk, str
  - compute_ss1m_receipt()
  - WeldAnchor construction
  - WeldLineage: __post_init__ (auto timestamp), to_dict()
  - create_weld(): passing, failing residual, failing identity
"""

from __future__ import annotations

import math

import pytest

from umcp.ss1m_triad import EditionTriad
from umcp.weld_lineage import (
    EditionIdentity,
    SS1mReceipt,
    WeldAnchor,
    WeldLineage,
    compute_extended_triad,
    compute_ss1m_receipt,
    create_weld,
    verify_extended_triad,
)

# Reference EID from the paper
PAPER_EID = EditionIdentity(pages=34, equations=52, figures=3, tables=6, listings=4, boxes=9, references=12)


def _make_anchor(eid: EditionIdentity | None = None, canon: str = "test") -> WeldAnchor:
    """Helper to build a WeldAnchor."""
    eid = eid or PAPER_EID
    triad = compute_extended_triad(eid)
    return WeldAnchor(
        eid=eid,
        triad=triad,
        canon_ref=canon,
        artifact_sha256="a" * 64,
        timestamp_utc="2025-01-01T00:00:00Z",
    )


class TestEditionIdentity:
    def test_fields(self) -> None:
        eid = PAPER_EID
        assert eid.pages == 34
        assert eid.equations == 52
        assert eid.figures == 3
        assert eid.tables == 6
        assert eid.listings == 4
        assert eid.boxes == 9
        assert eid.references == 12

    def test_is_namedtuple(self) -> None:
        assert len(PAPER_EID) == 7
        assert PAPER_EID._fields == (
            "pages",
            "equations",
            "figures",
            "tables",
            "listings",
            "boxes",
            "references",
        )


class TestComputeExtendedTriad:
    def test_deterministic(self) -> None:
        t1 = compute_extended_triad(PAPER_EID)
        t2 = compute_extended_triad(PAPER_EID)
        assert t1 == t2

    def test_c1_is_sum_mod_97(self) -> None:
        t = compute_extended_triad(PAPER_EID)
        expected = sum(PAPER_EID) % 97
        assert t.c1 == expected

    def test_different_eids_differ(self) -> None:
        eid2 = EditionIdentity(1, 2, 3, 4, 5, 6, 7)
        t1 = compute_extended_triad(PAPER_EID)
        t2 = compute_extended_triad(eid2)
        assert t1 != t2

    def test_returns_edition_triad(self) -> None:
        t = compute_extended_triad(PAPER_EID)
        assert isinstance(t, EditionTriad)


class TestVerifyExtendedTriad:
    def test_pass(self) -> None:
        triad = compute_extended_triad(PAPER_EID)
        assert verify_extended_triad(PAPER_EID, triad) is True

    def test_fail(self) -> None:
        wrong = EditionTriad(c1=0, c2=0, c3=0)
        assert verify_extended_triad(PAPER_EID, wrong) is False


class TestSS1mReceipt:
    @pytest.fixture()
    def receipt(self) -> SS1mReceipt:
        return compute_ss1m_receipt(PAPER_EID, delta_kappa=0.5, ir=1.7, M0=205, M1=120)

    def test_chk_list(self, receipt: SS1mReceipt) -> None:
        assert isinstance(receipt.chk, list)
        assert len(receipt.chk) == 3

    def test_compact_contains_eid(self, receipt: SS1mReceipt) -> None:
        s = receipt.compact()
        assert "SS1m(EID)" in s
        assert "P=34" in s
        assert "Eq=52" in s

    def test_str_is_compact(self, receipt: SS1mReceipt) -> None:
        assert str(receipt) == receipt.compact()

    def test_to_dict_keys(self, receipt: SS1mReceipt) -> None:
        d = receipt.to_dict()
        assert "eid" in d
        assert "delta_kappa" in d
        assert "ir" in d
        assert "M0" in d
        assert "M1" in d
        assert "triad" in d
        assert d["eid"]["pages"] == 34
        assert d["M0"] == 205

    def test_to_dict_triad_has_compact(self, receipt: SS1mReceipt) -> None:
        d = receipt.to_dict()
        assert "compact" in d["triad"]


class TestWeldAnchor:
    def test_construction(self) -> None:
        anchor = _make_anchor()
        assert anchor.canon_ref == "test"
        assert len(anchor.artifact_sha256) == 64

    def test_eid_accessible(self) -> None:
        anchor = _make_anchor()
        assert anchor.eid.pages == 34


class TestWeldLineage:
    def test_auto_timestamp(self) -> None:
        """__post_init__ sets created_utc if empty."""
        pre = _make_anchor(canon="pre")
        post = _make_anchor(canon="post")
        weld = WeldLineage(
            weld_id="W-TEST",
            pre_anchor=pre,
            post_anchor=post,
            delta_kappa=0.1,
            ir=1.1,
            residual=0.001,
            seam_pass=True,
        )
        assert weld.created_utc != ""
        assert "T" in weld.created_utc  # ISO format

    def test_explicit_timestamp(self) -> None:
        pre = _make_anchor()
        post = _make_anchor()
        weld = WeldLineage(
            weld_id="W-TEST",
            pre_anchor=pre,
            post_anchor=post,
            delta_kappa=0.1,
            ir=1.1,
            residual=0.001,
            seam_pass=True,
            created_utc="2025-06-01T00:00:00Z",
        )
        assert weld.created_utc == "2025-06-01T00:00:00Z"

    def test_to_dict(self) -> None:
        pre = _make_anchor(canon="pre")
        post = _make_anchor(canon="post")
        weld = WeldLineage(
            weld_id="W-TEST",
            pre_anchor=pre,
            post_anchor=post,
            delta_kappa=0.1,
            ir=1.1,
            residual=0.001,
            seam_pass=True,
            failures=("test failure",),
        )
        d = weld.to_dict()
        assert d["weld_id"] == "W-TEST"
        assert d["pre_anchor"]["canon_ref"] == "pre"
        assert d["post_anchor"]["canon_ref"] == "post"
        assert d["seam_pass"] is True
        assert d["failures"] == ["test failure"]
        assert "eid" in d["pre_anchor"]
        assert "triad" in d["pre_anchor"]

    def test_failures_tuple(self) -> None:
        pre = _make_anchor()
        post = _make_anchor()
        weld = WeldLineage(
            weld_id="W-TEST",
            pre_anchor=pre,
            post_anchor=post,
            delta_kappa=0.1,
            ir=1.1,
            residual=0.001,
            seam_pass=False,
            failures=("err1", "err2"),
        )
        assert len(weld.failures) == 2


class TestCreateWeld:
    def test_passing_weld(self) -> None:
        pre = _make_anchor()
        post = _make_anchor()
        dk = 0.1
        ir = math.exp(dk)
        weld = create_weld("W-PASS", pre, post, delta_kappa=dk, ir=ir, residual=0.001)
        assert weld.seam_pass is True
        assert len(weld.failures) == 0

    def test_failing_residual(self) -> None:
        pre = _make_anchor()
        post = _make_anchor()
        weld = create_weld("W-FAIL-R", pre, post, delta_kappa=0.1, ir=math.exp(0.1), residual=1.0)
        assert weld.seam_pass is False
        assert any("tol_seam" in f for f in weld.failures)

    def test_failing_identity(self) -> None:
        pre = _make_anchor()
        post = _make_anchor()
        # ir != exp(delta_kappa)
        weld = create_weld("W-FAIL-I", pre, post, delta_kappa=0.1, ir=999.0, residual=0.001)
        assert weld.seam_pass is False
        assert any("exp(Δκ)" in f for f in weld.failures)

    def test_both_failures(self) -> None:
        pre = _make_anchor()
        post = _make_anchor()
        weld = create_weld("W-BOTH", pre, post, delta_kappa=0.1, ir=999.0, residual=1.0)
        assert weld.seam_pass is False
        assert len(weld.failures) == 2
