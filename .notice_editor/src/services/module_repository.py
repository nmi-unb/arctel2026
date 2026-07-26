from __future__ import annotations

import json
from typing import Optional

from .dataStructure.lesson import Lesson
from .dataStructure.module import Module, ModuleSummary, parse_lesson_number
from .generic.file_fingerprint import FileFingerprint, read_fingerprint
from .generic.paths.target import get_modulo_data_path, get_modulos_dir, get_modulos_index_path


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


def _get_summary(module_id: str, refresh: bool = False) -> ModuleSummary:
    summary = next((item for item in list_modules(refresh=refresh) if item.id == module_id), None)
    if summary is None:
        raise ModuleRepositoryError(f"Módulo desconhecido: {module_id!r}")
    return summary


def get_module(module_id: str, refresh: bool = False) -> Module:
    if not refresh and module_id in _module_cache:
        return _module_cache[module_id]

    summary = _get_summary(module_id, refresh=refresh)

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


def load_all_modules(refresh: bool = False) -> list[Module]:
    return [get_module(summary.id, refresh=refresh) for summary in list_modules(refresh=refresh)]


def get_module_fingerprint(module_id: str) -> FileFingerprint:
    summary = _get_summary(module_id)
    path = get_modulo_data_path(summary.data_file)
    if not path.is_file():
        raise ModuleRepositoryError(f"Arquivo do módulo não encontrado: {path}")
    return read_fingerprint(path)


def has_module_changed_externally(module_id: str, fingerprint: FileFingerprint) -> bool:
    summary = _get_summary(module_id)
    path = get_modulo_data_path(summary.data_file)
    if not path.is_file():
        return True
    return read_fingerprint(path) != fingerprint


def reload_module(module_id: str) -> Module:
    return get_module(module_id, refresh=True)


def validate_module_file(module_id: str) -> bool:
    try:
        summary = _get_summary(module_id)
    except ModuleRepositoryError:
        return False
    path = get_modulo_data_path(summary.data_file)
    if not path.is_file():
        return False
    try:
        json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return False
    return True


def _update_index_title(module_id: str, new_title: str) -> None:
    global _index_cache
    index_path = get_modulos_index_path()
    try:
        data = json.loads(index_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ModuleRepositoryError(
            f"Falha ao sincronizar title em {index_path}: {exc}"
        ) from exc
    modules_raw = data.get("modules") if isinstance(data, dict) else None
    if modules_raw is None:
        raise ModuleRepositoryError(f"{index_path} não contém a chave 'modules'")

    changed = False
    for entry in modules_raw:
        if entry.get("id") == module_id and entry.get("title") != new_title:
            entry["title"] = new_title
            changed = True
    if not changed:
        return

    text = json.dumps(data, ensure_ascii=False, indent=2) + "\n"
    try:
        index_path.write_text(text, encoding="utf-8")
    except OSError as exc:
        raise ModuleRepositoryError(f"Falha ao gravar {index_path}: {exc}") from exc
    _index_cache = None


def save_module(module: Module, *, sync_index_title: bool = True) -> tuple[Module, FileFingerprint]:
    summary = _get_summary(module.id)
    path = get_modulo_data_path(summary.data_file)
    payload = module.to_dict()
    text = json.dumps(payload, ensure_ascii=False, indent=2) + "\n"
    try:
        path.write_text(text, encoding="utf-8")
    except OSError as exc:
        raise ModuleRepositoryError(f"Falha ao gravar {path}: {exc}") from exc

    try:
        reread_raw = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ModuleRepositoryError(
            f"Arquivo gravado, mas releitura de verificação falhou: {exc}"
        ) from exc
    if not isinstance(reread_raw, dict):
        raise ModuleRepositoryError("Releitura pós-gravação retornou conteúdo inesperado")

    reread_module = Module.from_dict(module.id, reread_raw)
    _module_cache[module.id] = reread_module
    fingerprint = read_fingerprint(path)

    if sync_index_title and summary.title != module.title:
        _update_index_title(module.id, module.title)

    return reread_module, fingerprint


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


def diagnose_index_files() -> dict:
    summaries = list_modules()
    dir_path = get_modulos_dir()
    existing_files = {path.name for path in dir_path.glob("*.json") if path.name != "index.json"}
    referenced_files = {summary.data_file for summary in summaries}

    missing_files = [summary.data_file for summary in summaries if summary.data_file not in existing_files]
    orphan_files = sorted(existing_files - referenced_files)
    return {"missing_files": missing_files, "orphan_files": orphan_files}


def clear_cache() -> None:
    global _index_cache
    _index_cache = None
    _module_cache.clear()


__all__ = [
    "ModuleRepositoryError",
    "list_modules",
    "get_module",
    "load_all_modules",
    "get_module_fingerprint",
    "has_module_changed_externally",
    "reload_module",
    "validate_module_file",
    "save_module",
    "diagnose_index_files",
    "find_lesson",
    "get_lesson_link",
    "clear_cache",
]
