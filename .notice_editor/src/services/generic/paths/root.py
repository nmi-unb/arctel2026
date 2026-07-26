from dataclasses import dataclass
from pathlib import Path

_ROOT_MARKERS = (
    "tree_focada.txt",
    Path("assets") / "data" / "avisos.json",
    Path("assets") / "data" / "modulos" / "index.json",
)

_cached_root: Path | None = None


def _missing_markers(candidate: Path) -> list[str]:
    missing = []
    for marker in _ROOT_MARKERS:
        if not (candidate / marker).is_file():
            missing.append(str(marker))
    return missing


def _candidate_dirs() -> list[Path]:
    anchors = {Path(__file__).resolve(), Path.cwd().resolve()}
    candidates: list[Path] = []
    seen: set[Path] = set()
    for anchor in anchors:
        for parent in (anchor, *anchor.parents):
            if parent not in seen:
                seen.add(parent)
                candidates.append(parent)
    return candidates


@dataclass(frozen=True)
class RootResolution:
    root: Path | None
    missing_markers: list[str]

    @property
    def found(self) -> bool:
        return self.root is not None


class RootNotFoundError(Exception):
    def __init__(self, missing_markers: list[str]):
        self.missing_markers = missing_markers
        super().__init__(
            "Raiz do repositório não encontrada. Marcadores ausentes: "
            + ", ".join(missing_markers)
        )


def resolve_project_root() -> RootResolution:
    last_missing: list[str] = [str(marker) for marker in _ROOT_MARKERS]
    for candidate in _candidate_dirs():
        missing = _missing_markers(candidate)
        if not missing:
            return RootResolution(root=candidate, missing_markers=[])
        last_missing = missing
    return RootResolution(root=None, missing_markers=last_missing)


def get_project_root() -> Path:
    global _cached_root
    if _cached_root is not None:
        return _cached_root
    resolution = resolve_project_root()
    if resolution.root is None:
        raise RootNotFoundError(resolution.missing_markers)
    _cached_root = resolution.root
    return _cached_root


__all__ = [
    "RootNotFoundError",
    "RootResolution",
    "get_project_root",
    "resolve_project_root",
]
