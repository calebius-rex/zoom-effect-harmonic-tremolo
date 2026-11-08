"""Minimal compatibility layer for the Harmonic scaffold build."""

from __future__ import annotations

from pathlib import Path


class LinkerConfig:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


def params_from_manifest(params):
    return params


def link(cfg):
    out = Path(cfg.output_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(b"stub-zdl")
    return out
