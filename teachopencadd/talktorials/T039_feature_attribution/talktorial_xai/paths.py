"""Canonical talktorial paths, resolved relative to the talktorial folder."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

DATA = ROOT / "data"
DATA_RAW = DATA / "raw"
DATA_PROCESSED = DATA / "processed"
IMAGES = ROOT / "images"

__all__ = ["ROOT", "DATA", "DATA_RAW", "DATA_PROCESSED", "IMAGES"]
