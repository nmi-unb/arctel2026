# .notice_editor/src/services/dataStructure/__init__.py

_EXPORTS = {
    "Lesson": (".lesson", "Lesson"),
    "LessonLinks": (".LessonLinks", "LessonLinks"),
    "Module": (".module", "Module"),
    "ModuleSummary": (".module", "ModuleSummary"),
    "Notice": (".notice", "Notice"),
    "build_lesson_id": (".module", "build_lesson_id"),
    "build_module_id": (".module", "build_module_id"),
    "parse_lesson_number": (".module", "parse_lesson_number"),
    "parse_module_number": (".module", "parse_module_number"),
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
