# .notice_editor/src/services/generic/values/__init__.py

_EXPORTS = {
    "AVISOS_ID_FORBIDDEN_CHARS": (".constants", "AVISOS_ID_FORBIDDEN_CHARS"),
    "DATE_DISPLAY_FORMAT": (".constants", "DATE_DISPLAY_FORMAT"),
    "DATE_OFFSET_OPTIONS": (".constants", "DATE_OFFSET_OPTIONS"),
    "DEFAULT_DATE_OFFSET": (".constants", "DEFAULT_DATE_OFFSET"),
    "DEFAULT_TEXTO_LINK": (".constants", "DEFAULT_TEXTO_LINK"),
    "LINK_SOURCE_LABELS": (".constants", "LINK_SOURCE_LABELS"),
    "LINK_SOURCE_LEGACY": (".constants", "LINK_SOURCE_LEGACY"),
    "LINK_SOURCE_LESSON": (".constants", "LINK_SOURCE_LESSON"),
    "LINK_SOURCE_LIVE": (".constants", "LINK_SOURCE_LIVE"),
    "LINK_SOURCE_NONE": (".constants", "LINK_SOURCE_NONE"),
    "LINK_SOURCE_STATIC": (".constants", "LINK_SOURCE_STATIC"),
    "LINK_TYPES": (".constants", "LINK_TYPES"),
    "LINK_TYPE_LABELS": (".constants", "LINK_TYPE_LABELS"),
    "LIST_FILTERS": (".constants", "LIST_FILTERS"),
    "NOTICE_REQUIRED_FIELDS": (".constants", "NOTICE_REQUIRED_FIELDS"),
    "NOTICE_TYPES": (".constants", "NOTICE_TYPES"),
    "TIMEZONE_NAME": (".constants", "TIMEZONE_NAME"),
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
