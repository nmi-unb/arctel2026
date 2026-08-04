from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class FileFingerprint:
    mtime_ns: int
    size: int


def read_fingerprint(path: Path) -> FileFingerprint:
    stat = path.stat()
    return FileFingerprint(mtime_ns=stat.st_mtime_ns, size=stat.st_size)


__all__ = ["FileFingerprint", "read_fingerprint"]
