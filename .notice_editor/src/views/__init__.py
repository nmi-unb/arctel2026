# .notice_editor/src/views/__init__.py

_EXPORTS = {
    "DiagnosticsView": (".diagnostics_view", "DiagnosticsView"),
    "MainView": (".main_view", "MainView"),
    "NoticeFormView": (".notice_form", "NoticeFormView"),
    "NoticeListView": (".notice_list", "NoticeListView"),
    "NoticePreviewView": (".notice_preview", "NoticePreviewView"),
    "build_main_view": (".main_view", "build_main_view"),
    "confirm_delete": (".confirmation_dialog", "confirm_delete"),
    "confirm_discard_edit": (".confirmation_dialog", "confirm_discard_edit"),
    "confirm_external_change": (".confirmation_dialog", "confirm_external_change"),
    "confirm_id_change": (".confirmation_dialog", "confirm_id_change"),
    "confirm_reload": (".confirmation_dialog", "confirm_reload"),
    "confirm_save": (".confirmation_dialog", "confirm_save"),
    "confirm_sort": (".confirmation_dialog", "confirm_sort"),
    "resolve_notice_link_preview": (".notice_preview", "resolve_notice_link_preview"),
    "show_confirmation": (".confirmation_dialog", "show_confirmation"),
    "show_message": (".confirmation_dialog", "show_message"),
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
