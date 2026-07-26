# .notice_editor/src/services/generic/__init__.py

_EXPORTS = {
    "AVISOS_ID_FORBIDDEN_CHARS": (".values", "AVISOS_ID_FORBIDDEN_CHARS"),
    "DATE_DISPLAY_FORMAT": (".values", "DATE_DISPLAY_FORMAT"),
    "DATE_OFFSET_OPTIONS": (".values", "DATE_OFFSET_OPTIONS"),
    "DEFAULT_DATE_OFFSET": (".values", "DEFAULT_DATE_OFFSET"),
    "DEFAULT_TEXTO_LINK": (".values", "DEFAULT_TEXTO_LINK"),
    "LINK_SOURCE_LABELS": (".values", "LINK_SOURCE_LABELS"),
    "LINK_SOURCE_LEGACY": (".values", "LINK_SOURCE_LEGACY"),
    "LINK_SOURCE_LESSON": (".values", "LINK_SOURCE_LESSON"),
    "LINK_SOURCE_LIVE": (".values", "LINK_SOURCE_LIVE"),
    "LINK_SOURCE_NONE": (".values", "LINK_SOURCE_NONE"),
    "LINK_SOURCE_STATIC": (".values", "LINK_SOURCE_STATIC"),
    "LINK_TYPES": (".values", "LINK_TYPES"),
    "LINK_TYPE_LABELS": (".values", "LINK_TYPE_LABELS"),
    "LIST_FILTERS": (".values", "LIST_FILTERS"),
    "NOTICE_REQUIRED_FIELDS": (".values", "NOTICE_REQUIRED_FIELDS"),
    "NOTICE_TYPES": (".values", "NOTICE_TYPES"),
    "RootNotFoundError": (".paths", "RootNotFoundError"),
    "RootResolution": (".paths", "RootResolution"),
    "TIMEZONE_NAME": (".values", "TIMEZONE_NAME"),
    "get_avisos_path": (".paths", "get_avisos_path"),
    "get_modulo_data_path": (".paths", "get_modulo_data_path"),
    "get_modulos_dir": (".paths", "get_modulos_dir"),
    "get_modulos_index_path": (".paths", "get_modulos_index_path"),
    "get_notice_link_integration_path": (".paths", "get_notice_link_integration_path"),
    "get_project_root": (".paths", "get_project_root"),
    "resolve_project_root": (".paths", "resolve_project_root"),
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
