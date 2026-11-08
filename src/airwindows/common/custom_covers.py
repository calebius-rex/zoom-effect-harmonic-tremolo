"""Minimal custom cover helper for the Harmonic scaffold."""

from __future__ import annotations


def make_cover(name, param_names=None):
    return b"\x00" * 2048
