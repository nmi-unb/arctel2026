from __future__ import annotations

import json
from typing import Optional

from .dataStructure.lesson import Lesson
from .dataStructure.module import Module, ModuleSummary, parse_lesson_number
from .generic.paths.target import get_modulo_data_path, get_modulos_index_path


class ModuleRepositoryError(Exception):
    pass


_index_cache: Optional[list[ModuleSummary]] = None
_module_cache: dict[str, Module] = {}


def _load_index() -> list[ModuleSummary]:
    path = get_modulos_index_path()
    if not path.is_file():
        raise ModuleRepositoryError(f"Índice de módulos não encontrado: {path}")
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ModuleRepositoryError(f"JSON malformado em {path}: {exc}") from exc
    modules_raw = data.get("modules") if isinstance(data, dict) else None
    if modules_raw is None:
        raise ModuleRepositoryError(f"{path} não contém a chave 'modules'")
    return [ModuleSummary.from_dict(item) for item in modules_raw]


def list_modules(refresh: bool = False) -> list[ModuleSummary]:
    global _index_cache
    if _index_cache is None or refresh:
        _index_cache = _load_index()
    return list(_index_cache)


def get_module(module_id: str, refresh: bool = False) -> Module:
    if not refresh and module_id in _module_cache:
        return _module_cache[module_id]

    summary = next((item for item in list_modules(refresh=refresh) if item.id == module_id), None)
    if summary is None:
        raise ModuleRepositoryError(f"Módulo desconhecido: {module_id!r}")

    path = get_modulo_data_path(summary.data_file)
    if not path.is_file():
        raise ModuleRepositoryError(f"Arquivo do módulo não encontrado: {path}")
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ModuleRepositoryError(f"JSON malformado em {path}: {exc}") from exc

    module = Module.from_dict(module_id, data)
    _module_cache[module_id] = module
    return module


def find_lesson(module_id: str, lesson_id: str) -> Lesson:
    try:
        numero = parse_lesson_number(lesson_id)
    except ValueError as exc:
        raise ModuleRepositoryError(str(exc)) from exc

    module = get_module(module_id)
    lesson = module.lesson(numero)
    if lesson is None:
        raise ModuleRepositoryError(f"Aula {lesson_id!r} não encontrada em {module_id!r}")
    return lesson


def get_lesson_link(module_id: str, lesson_id: str, link_type: str) -> Optional[str]:
    lesson = find_lesson(module_id, lesson_id)
    try:
        return lesson.link_for(link_type)
    except ValueError as exc:
        raise ModuleRepositoryError(str(exc)) from exc


def clear_cache() -> None:
    global _index_cache
    _index_cache = None
    _module_cache.clear()


__all__ = [
    "ModuleRepositoryError",
    "list_modules",
    "get_module",
    "find_lesson",
    "get_lesson_link",
    "clear_cache",
]
