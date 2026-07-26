# .notice_editor/src/services/__init__.py

_EXPORTS = {
    "AVISOS_ID_FORBIDDEN_CHARS": (".generic", "AVISOS_ID_FORBIDDEN_CHARS"),
    "DATE_DISPLAY_FORMAT": (".generic", "DATE_DISPLAY_FORMAT"),
    "DATE_OFFSET_OPTIONS": (".generic", "DATE_OFFSET_OPTIONS"),
    "DEFAULT_DATE_OFFSET": (".generic", "DEFAULT_DATE_OFFSET"),
    "DEFAULT_TEXTO_LINK": (".generic", "DEFAULT_TEXTO_LINK"),
    "FileFingerprint": (".notice_repository", "FileFingerprint"),
    "LINK_SOURCE_LABELS": (".generic", "LINK_SOURCE_LABELS"),
    "LINK_SOURCE_LEGACY": (".generic", "LINK_SOURCE_LEGACY"),
    "LINK_SOURCE_LESSON": (".generic", "LINK_SOURCE_LESSON"),
    "LINK_SOURCE_LIVE": (".generic", "LINK_SOURCE_LIVE"),
    "LINK_SOURCE_NONE": (".generic", "LINK_SOURCE_NONE"),
    "LINK_SOURCE_STATIC": (".generic", "LINK_SOURCE_STATIC"),
    "LINK_TYPES": (".generic", "LINK_TYPES"),
    "LINK_TYPE_LABELS": (".generic", "LINK_TYPE_LABELS"),
    "LIST_FILTERS": (".generic", "LIST_FILTERS"),
    "LegacyRecord": (".migration_service", "LegacyRecord"),
    "LegacyReference": (".migration_service", "LegacyReference"),
    "Lesson": (".dataStructure", "Lesson"),
    "LessonLinks": (".dataStructure", "LessonLinks"),
    "Module": (".dataStructure", "Module"),
    "ModuleRepositoryError": (".module_repository", "ModuleRepositoryError"),
    "ModuleSummary": (".dataStructure", "ModuleSummary"),
    "NOTICE_REQUIRED_FIELDS": (".generic", "NOTICE_REQUIRED_FIELDS"),
    "NOTICE_TYPES": (".generic", "NOTICE_TYPES"),
    "Notice": (".dataStructure", "Notice"),
    "NoticeRepositoryError": (".notice_repository", "NoticeRepositoryError"),
    "RootNotFoundError": (".generic", "RootNotFoundError"),
    "RootResolution": (".generic", "RootResolution"),
    "TIMEZONE_NAME": (".generic", "TIMEZONE_NAME"),
    "ValidationIssue": (".validation_service", "ValidationIssue"),
    "ValidationResult": (".validation_service", "ValidationResult"),
    "build_legacy_report": (".migration_service", "build_legacy_report"),
    "build_lesson_id": (".dataStructure", "build_lesson_id"),
    "build_module_id": (".dataStructure", "build_module_id"),
    "clear_cache": (".module_repository", "clear_cache"),
    "find_legacy_notices": (".migration_service", "find_legacy_notices"),
    "find_lesson": (".module_repository", "find_lesson"),
    "get_avisos_path": (".generic", "get_avisos_path"),
    "get_lesson_link": (".module_repository", "get_lesson_link"),
    "get_module": (".module_repository", "get_module"),
    "get_modulo_data_path": (".generic", "get_modulo_data_path"),
    "get_modulos_dir": (".generic", "get_modulos_dir"),
    "get_modulos_index_path": (".generic", "get_modulos_index_path"),
    "get_notice_link_integration_path": (".generic", "get_notice_link_integration_path"),
    "get_project_root": (".generic", "get_project_root"),
    "has_blocking_errors": (".validation_service", "has_blocking_errors"),
    "has_changed_externally": (".notice_repository", "has_changed_externally"),
    "list_modules": (".module_repository", "list_modules"),
    "load_notices": (".notice_repository", "load_notices"),
    "migrate_to_lesson_reference": (".migration_service", "migrate_to_lesson_reference"),
    "migrate_to_static_link": (".migration_service", "migrate_to_static_link"),
    "parse_lesson_number": (".dataStructure", "parse_lesson_number"),
    "parse_module_number": (".dataStructure", "parse_module_number"),
    "resolve_project_root": (".generic", "resolve_project_root"),
    "save_notices": (".notice_repository", "save_notices"),
    "suggest_lesson_reference": (".migration_service", "suggest_lesson_reference"),
    "validate_all": (".validation_service", "validate_all"),
    "validate_notice": (".validation_service", "validate_notice"),
}

__all__ = list(_EXPORTS)


def __getattr__(name: str):
    from importlib import import_module

    if name not in _EXPORTS:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

    module_name, attribute_name = _EXPORTS[name]
    value = getattr(import_module(module_name, __name__), attribute_name)
    globals()[name] = value
    return value


def __dir__():
    return sorted(set(globals()) | set(__all__))
