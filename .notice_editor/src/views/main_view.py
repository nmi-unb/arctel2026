from __future__ import annotations

import flet as ft

from app_state import AppState, ExternalChangeError, SaveBlockedError
from services.notice_repository import NoticeRepositoryError
from views import confirmation_dialog
from views.diagnostics_view import DiagnosticsView
from views.notice_form import NoticeFormView
from views.notice_list import NoticeListView
from views.notice_preview import NoticePreviewView


class MainView:
    def __init__(self, page: ft.Page) -> None:
        self.page = page
        self.state = AppState()

        self.list_view = NoticeListView(self)
        self.form = NoticeFormView(self)
        self.preview = NoticePreviewView()
        self.diagnostics = DiagnosticsView(self)

        self.status_text = ft.Text("", size=12)
        self.save_button = ft.FilledButton("Salvar arquivo", icon=ft.Icons.SAVE, on_click=self._on_save_click)
        self.reload_button = ft.OutlinedButton(
            "Recarregar", icon=ft.Icons.REFRESH, on_click=self._on_reload_click
        )
        self.diagnostics_button = ft.TextButton(
            "Diagnóstico de URLs legadas", on_click=lambda e: self.diagnostics.open()
        )

        self._list_expanded = True
        self.toggle_list_button = ft.IconButton(
            ft.Icons.MENU_OPEN,
            tooltip="Recolher lista de avisos",
            on_click=self._on_toggle_list_click,
        )

        self._build_layout()
        self._initial_load()

    # ------------------------------------------------------------- layout

    def _build_layout(self) -> None:
        header = ft.Container(
            content=ft.Row(
                [
                    self.toggle_list_button,
                    ft.Container(expand=True),
                    self.status_text,
                    self.diagnostics_button,
                    self.reload_button,
                    self.save_button,
                ]
            ),
            padding=ft.Padding.only(top=5, left=12, right=12, bottom=8),
        )
        self.list_container = ft.Container(content=self.list_view.container, width=320, padding=12)
        body = ft.Row(
            [
                self.list_container,
                ft.VerticalDivider(),
                ft.Container(content=self.form.container, expand=1, padding=12),
                ft.VerticalDivider(),
                ft.Container(content=self.preview.container, expand=1, padding=12),
            ],
            expand=True,
        )
        self.page.add(ft.Column([header, ft.Divider(), body], expand=True))

    def _on_toggle_list_click(self, e: ft.Event) -> None:
        self._list_expanded = not self._list_expanded
        self.list_container.visible = self._list_expanded
        self.toggle_list_button.icon = ft.Icons.MENU_OPEN if self._list_expanded else ft.Icons.MENU
        self.toggle_list_button.tooltip = (
            "Recolher lista de avisos" if self._list_expanded else "Expandir lista de avisos"
        )

    def _initial_load(self) -> None:
        try:
            self.state.load()
        except NoticeRepositoryError as exc:
            self.status_text.value = f"Erro ao carregar avisos.json: {exc}"
            self.status_text.color = ft.Colors.RED_700
            return
        self._refresh_status()
        self.list_view.refresh()

    def _refresh_status(self) -> None:
        suffix = " — alterações não salvas" if self.state.dirty else ""
        self.status_text.value = f"{len(self.state.notices)} avisos carregados{suffix}"
        self.status_text.color = ft.Colors.AMBER_700 if self.state.dirty else ft.Colors.ON_SURFACE_VARIANT

    # --------------------------------------------------------- form guard

    def _guard_unapplied(self, proceed) -> None:
        if self.form.has_unapplied_changes():
            confirmation_dialog.confirm_discard_edit(self.page, on_confirm=proceed)
        else:
            proceed()

    # --------------------------------------------------- list/form actions

    def start_new(self) -> None:
        def _proceed() -> None:
            self.form.load_notice(None, None)
            self.preview.clear()
            self.list_view.refresh()

        self._guard_unapplied(_proceed)

    def start_edit(self, index: int) -> None:
        def _proceed() -> None:
            notice = self.state.notices[index]
            self.form.load_notice(notice, index)
            self.preview.render(notice)
            self.list_view.refresh()

        self._guard_unapplied(_proceed)

    def cancel_edit(self) -> None:
        self.form.load_notice(None, None)
        self.preview.clear()
        self.list_view.refresh()

    def apply_notice_from_form(self, notice, index) -> None:
        self.state.apply_notice(notice, index)
        self._refresh_status()
        self.list_view.refresh()
        self.preview.render(notice)

    def duplicate_notice(self, index: int) -> None:
        original = self.state.notices[index]
        existing_ids = {notice.id for notice in self.state.notices}
        base_new_id = f"{original.id}-copia"
        new_id = base_new_id
        counter = 2
        while new_id in existing_ids:
            new_id = f"{base_new_id}-{counter}"
            counter += 1
        clone = self.state.duplicate_notice(index, new_id)
        self._refresh_status()
        self.form.load_notice(clone, index + 1)
        self.preview.render(clone)
        self.list_view.refresh()

    def toggle_active(self, index: int) -> None:
        notice = self.state.notices[index]
        self.state.set_active(index, not notice.ativo)
        self._refresh_status()
        if self.form.editing_index == index:
            self.form.load_notice(self.state.notices[index], index)
            self.preview.render(self.state.notices[index])
        self.list_view.refresh()

    def move_notice(self, index: int, direction: int) -> None:
        if direction < 0:
            self.state.move_up(index)
        else:
            self.state.move_down(index)

        if self.form.editing_index == index:
            self.form.editing_index = index + direction
        elif self.form.editing_index == index + direction:
            self.form.editing_index = index

        self._refresh_status()
        self.list_view.refresh()

    def request_delete(self, index: int) -> None:
        notice = self.state.notices[index]

        def _confirm() -> None:
            self.state.delete_notice(index)
            if self.form.editing_index == index:
                self.form.load_notice(None, None)
                self.preview.clear()
            elif self.form.editing_index is not None and self.form.editing_index > index:
                self.form.editing_index -= 1
            self._refresh_status()
            self.list_view.refresh()

        confirmation_dialog.confirm_delete(self.page, notice_id=notice.id, on_confirm=_confirm)

    def request_sort_publicacao(self) -> None:
        def _confirm() -> None:
            self.state.sort_by_publicacao()
            self.form.load_notice(None, None)
            self.preview.clear()
            self._refresh_status()
            self.list_view.refresh()

        confirmation_dialog.confirm_sort(self.page, label="Ordenar por publicação", on_confirm=_confirm)

    def request_sort_prioridade(self) -> None:
        def _confirm() -> None:
            self.state.sort_by_prioridade()
            self.form.load_notice(None, None)
            self.preview.clear()
            self._refresh_status()
            self.list_view.refresh()

        confirmation_dialog.confirm_sort(self.page, label="Ordenar por prioridade", on_confirm=_confirm)

    # -------------------------------------------------------- diagnostics

    def migrate_legacy_to_static(self, index: int, static_link: str) -> None:
        self.state.migrate_to_static_link(index, static_link)
        self._refresh_status()
        if self.form.editing_index == index:
            self.form.load_notice(self.state.notices[index], index)
            self.preview.render(self.state.notices[index])
        self.list_view.refresh()

    def migrate_legacy_to_lesson(self, index: int, module_id: str, lesson_id: str, link_type: str) -> None:
        self.state.migrate_to_lesson_reference(index, module_id, lesson_id, link_type)
        self._refresh_status()
        if self.form.editing_index == index:
            self.form.load_notice(self.state.notices[index], index)
            self.preview.render(self.state.notices[index])
        self.list_view.refresh()

    # ------------------------------------------------------------- reload

    def _on_reload_click(self, e: ft.Event) -> None:
        def _do_reload() -> None:
            try:
                self.state.load()
            except NoticeRepositoryError as exc:
                confirmation_dialog.show_message(self.page, title="Erro ao recarregar", message=str(exc))
                return
            self.form.load_notice(None, None)
            self.preview.clear()
            self._refresh_status()
            self.list_view.refresh()

        if self.state.dirty:
            confirmation_dialog.confirm_reload(self.page, on_confirm=_do_reload)
        else:
            _do_reload()

    # --------------------------------------------------------------- save

    def _on_save_click(self, e: ft.Event) -> None:
        def _do_save() -> None:
            try:
                self.state.save()
            except SaveBlockedError as exc:
                self._show_save_blocked(exc)
                return
            except ExternalChangeError:
                self._handle_external_change()
                return
            except NoticeRepositoryError as exc:
                confirmation_dialog.show_message(self.page, title="Erro ao salvar", message=str(exc))
                return
            self._refresh_status()
            confirmation_dialog.show_message(
                self.page, title="Salvo", message="assets/data/avisos.json atualizado com sucesso."
            )

        confirmation_dialog.confirm_save(self.page, on_confirm=_do_save)

    def _show_save_blocked(self, exc: SaveBlockedError) -> None:
        messages = [
            f"{notice_id}: {issue.message}"
            for notice_id, result in exc.results.items()
            if not result.is_valid
            for issue in result.errors
        ]
        confirmation_dialog.show_message(
            self.page,
            title="Não foi possível salvar",
            message="Existem avisos inválidos:\n" + "\n".join(messages),
        )

    def _handle_external_change(self) -> None:
        def _reload() -> None:
            self.state.load()
            self.form.load_notice(None, None)
            self.preview.clear()
            self._refresh_status()
            self.list_view.refresh()

        def _overwrite() -> None:
            try:
                self.state.save_overriding_external_change()
            except SaveBlockedError as exc:
                self._show_save_blocked(exc)
                return
            self._refresh_status()
            confirmation_dialog.show_message(
                self.page, title="Salvo", message="assets/data/avisos.json atualizado com sucesso."
            )

        confirmation_dialog.confirm_external_change(self.page, on_reload=_reload, on_overwrite=_overwrite)


def build_main_view(page: ft.Page) -> MainView:
    return MainView(page)


__all__ = ["MainView", "build_main_view"]
