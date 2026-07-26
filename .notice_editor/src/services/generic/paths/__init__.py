# .notice_editor/src/services/generic/paths/__init__.py

_EXPORTS = {
    "RootNotFoundError": (".root", "RootNotFoundError"),
    "RootResolution": (".root", "RootResolution"),
    "get_avisos_path": (".target", "get_avisos_path"),
    "get_modulo_data_path": (".target", "get_modulo_data_path"),
    "get_modulos_dir": (".target", "get_modulos_dir"),
    "get_modulos_index_path": (".target", "get_modulos_index_path"),
    "get_notice_link_integration_path": (".target", "get_notice_link_integration_path"),
    "get_project_root": (".root", "get_project_root"),
    "resolve_project_root": (".root", "resolve_project_root"),
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
