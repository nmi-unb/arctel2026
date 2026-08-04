from pathlib import Path

from .root import get_project_root


def get_avisos_path() -> Path:
    return get_project_root() / "assets" / "data" / "avisos.json"


def get_modulos_dir() -> Path:
    return get_project_root() / "assets" / "data" / "modulos"


def get_modulos_index_path() -> Path:
    return get_modulos_dir() / "index.json"


def get_modulo_data_path(data_file: str) -> Path:
    return get_modulos_dir() / data_file


def get_notice_link_integration_path() -> Path:
    return get_project_root() / ".docs" / "NOTICE_LINK_INTEGRATION.md"


__all__ = [
    "get_avisos_path",
    "get_modulos_dir",
    "get_modulos_index_path",
    "get_modulo_data_path",
    "get_notice_link_integration_path",
]
