"""Calendar arithmetic gate. The module carries its own checks; run them here."""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scripts"))

import harptos  # noqa: E402


def test_selftest_passes():
    assert harptos.selftest() == 0


def test_sourced_lane_anchors():
    """The two facts the campaign states. If these drift, the epoch is wrong."""
    assert harptos.Date(1494, "Tarsakh", 30).day_number() == 904
    assert harptos.Date(1494, "Mirtul", 6).day_number() == 911


def test_lanes_cannot_be_summed():
    a = harptos.parse("ARIK:1495.Hammer.07")
    b = harptos.parse("SHIVAN:D911")
    try:
        harptos.delta(a, b)
    except harptos.LaneMismatch:
        return
    raise AssertionError("cross-lane subtraction must be refused")
