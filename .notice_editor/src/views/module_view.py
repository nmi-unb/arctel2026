from __future__ import annotations

import flet as ft

from services import reference_service, validation_service
from services.dataStructure.module import build_lesson_id
from services.module_state import ModuleExternalChangeError, ModuleSaveBlockedError, ModuleStateError
from views import confirmation_dialog
from views.lesson_form import LessonFormView
from views.lesson_list import LessonListView
from views.lesson_preview import LessonPreviewView
from views.module_form import ModuleFormView
from views.module_list import ModuleListView


class ModuleView:
    def __init__(self, main_view) -> None:
        self.main_view = main_view

        self.module_list = ModuleListView(self)
        self.module_form = ModuleFormView(self)
        self.lesson_list = LessonListView(self)
        self.lesson_form = LessonFormView(self)
        self.lesson_preview = LessonPreviewView()

        left = ft.Container(content=self.module_list.container, width=240, padding=12)
        middle = ft.Container(
            content=ft.Column(
                [self.module_form.container, ft.Divider(), self.lesson_list.container], expand=True, spacing=10
            ),
            expand=2,
            padding=12,
        )
        right = ft.Container(
            content=ft.Column(
                [self.lesson_preview.container, ft.Divider(), self.lesson_form.container], expand=True, spacing=10
            ),
            expand=3,
            padding=12,
        )

        self.container = ft.Row([left, ft.VerticalDivider(), middle, ft.VerticalDivider(), right], expand=True)

    # ------------------------------------------------------------ refresh

    def refresh(self) -> None:
        self.module_list.refresh()
        self.lesson_list.refresh()
        self._refresh_lesson_panel()

    def _refresh_lesson_panel(self) -> None:
        module_state = self.main_view.module_state
        module_id = module_state.selected_module_id
        module = module_state.get_module(module_id) if module_id else None
        numero = module_state.selected_lesson_numero
        lesson = module.lesson(numero) if module and numero is not None else None
        if lesson is None:
            self.lesson_preview.clear()
            self.lesson_form.load_lesson(None, None)
            return
        refs = module_state.notices_referencing(self.main_view.state.notices, module_id=module_id, lesson_numero=numero)
        self.lesson_preview.render(lesson, len(refs))
        self.lesson_form.load_lesson(module_id, lesson)

    # ------------------------------------------------------------- guards

    def _guard_lesson_unapplied(self, proceed) -> None:
        if self.lesson_form.has_unapplied_changes():
            confirmation_dialog.confirm_discard_edit(self.main_view.page, on_confirm=proceed)
        else:
            proceed()

    # --------------------------------------------------------- selection

    def select_module(self, module_id: str) -> None:
        def _proceed() -> None:
            module_state = self.main_view.module_state
            if module_state.get_module(module_id) is None:
                module_state.load_module(module_id)
            module_state.select_module(module_id)
            self.module_form.load_module(module_state.get_module(module_id))
            self.refresh()

        self._guard_lesson_unapplied(_proceed)

    def select_lesson(self, numero) -> None:
        def _proceed() -> None:
            self.main_view.module_state.select_lesson(numero)
            self.refresh()

        self._guard_lesson_unapplied(_proceed)

    def cancel_lesson_edit(self) -> None:
        self._refresh_lesson_panel()

    # ------------------------------------------------------- module edit

    def update_title(self, new_title: str) -> None:
        module_state = self.main_view.module_state
        module_id = module_state.selected_module_id
        if module_id is None:
            return
        module_state.update_title(module_id, new_title)
        self.module_form.refresh_status()
        self.module_list.refresh()

    # ------------------------------------------------------- lesson edit

    def validate_lesson_form(self, lesson) -> list[str]:
        result = validation_service.validate_lesson(lesson)
        return [issue.message for issue in result.errors]

    def apply_lesson_from_form(self, lesson) -> None:
        module_id = self.main_view.module_state.selected_module_id
        if module_id is None:
            return
        self.main_view.module_state.update_lesson(module_id, lesson)
        self.module_form.refresh_status()
        self.refresh()

    def create_lesson(self) -> None:
        module_id = self.main_view.module_state.selected_module_id
        if module_id is None:
            return

        def _proceed() -> None:
            lesson = self.main_view.module_state.create_lesson(module_id)
            self.main_view.module_state.select_lesson(lesson.numero)
            self.module_form.refresh_status()
            self.refresh()

        self._guard_lesson_unapplied(_proceed)

    def duplicate_lesson(self, numero: int) -> None:
        module_id = self.main_view.module_state.selected_module_id
        if module_id is None:
            return

        def _proceed() -> None:
            clone = self.main_view.module_state.duplicate_lesson(module_id, numero)
            self.main_view.module_state.select_lesson(clone.numero)
            self.module_form.refresh_status()
            self.refresh()

        self._guard_lesson_unapplied(_proceed)

    def move_lesson(self, numero: int, direction: int) -> None:
        module_id = self.main_view.module_state.selected_module_id
        if module_id is None:
            return
        self.main_view.module_state.move_lesson(module_id, numero, direction)
        self.module_form.refresh_status()
        self.refresh()

    def sort_lessons_by_numero(self) -> None:
        module_id = self.main_view.module_state.selected_module_id
        if module_id is None:
            return
        self.main_view.module_state.sort_lessons_by_numero(module_id)
        self.module_form.refresh_status()
        self.refresh()

    def sort_lessons_by_data(self) -> None:
        module_id = self.main_view.module_state.selected_module_id
        if module_id is None:
            return
        self.main_view.module_state.sort_lessons_by_data(module_id)
        self.module_form.refresh_status()
        self.refresh()

    # ---------------------------------------------------- lesson removal

    def request_remove_lesson(self, numero: int) -> None:
        module_id = self.main_view.module_state.selected_module_id
        if module_id is None:
            return
        impact = reference_service.analyze_lesson_removal(self.main_view.state.notices, module_id, numero)
        if not impact.has_affected:
            self._do_remove_lesson(module_id, numero, deactivate=False)
            return

        lines = [f"{len(impact.affected)} aviso(s) referenciam esta aula:"]
        for ref in impact.affected:
            lines.append(f"  - {ref.id} ({'ativo' if ref.ativo else 'inativo'}): {ref.titulo}")
        message = "\n".join(lines)

        confirmation_dialog.confirm_lesson_removal(
            self.main_view.page,
            message=message,
            on_keep_invalid=lambda: self._do_remove_lesson(module_id, numero, deactivate=False),
            on_deactivate=lambda: self._do_remove_lesson(module_id, numero, deactivate=True),
        )

    def _do_remove_lesson(self, module_id: str, numero: int, *, deactivate: bool) -> None:
        if deactivate:
            lesson_id = build_lesson_id(numero)
            for index, notice in enumerate(self.main_view.state.notices):
                if notice.module_id == module_id and notice.lesson_id == lesson_id and notice.ativo:
                    self.main_view.state.set_active(index, False)
            self.main_view.list_view.refresh()
            self.main_view.refresh_status()

        self.main_view.module_state.remove_lesson(module_id, numero)
        self.module_form.refresh_status()
        self.refresh()

    # ---------------------------------------------------- lesson renumber

    def request_renumber_lesson(self, old_numero: int) -> None:
        module_id = self.main_view.module_state.selected_module_id
        if module_id is None:
            return

        new_numero_field = ft.TextField(
            label="novo número", value=str(old_numero), width=120, keyboard_type=ft.KeyboardType.NUMBER
        )

        def _on_confirm_pick(e: ft.Event) -> None:
            raw = (new_numero_field.value or "").strip()
            if not raw.isdigit():
                return
            self.main_view.page.pop_dialog()
            self._continue_renumber(module_id, old_numero, int(raw))

        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Alterar número da aula"),
            content=ft.Column([ft.Text("Informe o novo número da aula:"), new_numero_field], tight=True),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: self.main_view.page.pop_dialog()),
                ft.FilledButton("Continuar", on_click=_on_confirm_pick),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        self.main_view.page.show_dialog(dialog)

    def _continue_renumber(self, module_id: str, old_numero: int, new_numero: int) -> None:
        if old_numero == new_numero:
            return
        impact = reference_service.analyze_lesson_renumber(self.main_view.state.notices, module_id, old_numero, new_numero)
        if not impact.has_affected:
            self._do_renumber(module_id, old_numero, new_numero, update_notices=False)
            return

        lines = [f"{len(impact.affected)} aviso(s) usam o lessonId antigo ({impact.old_lesson_id}):"]
        for ref in impact.affected:
            lines.append(f"  - {ref.id}: {ref.titulo}")
        message = "\n".join(lines)

        confirmation_dialog.confirm_lesson_renumber(
            self.main_view.page,
            message=message,
            on_lesson_only=lambda: self._do_renumber(module_id, old_numero, new_numero, update_notices=False),
            on_lesson_and_notices=lambda: self._do_renumber(module_id, old_numero, new_numero, update_notices=True),
        )

    def _do_renumber(self, module_id: str, old_numero: int, new_numero: int, *, update_notices: bool) -> None:
        try:
            self.main_view.module_state.renumber_lesson(module_id, old_numero, new_numero)
        except ModuleStateError as exc:
            confirmation_dialog.show_message(self.main_view.page, title="Não foi possível renumerar", message=str(exc))
            return

        if update_notices:
            new_lesson_id = build_lesson_id(new_numero)
            old_lesson_id = build_lesson_id(old_numero)
            for index, notice in enumerate(self.main_view.state.notices):
                if notice.module_id == module_id and notice.lesson_id == old_lesson_id:
                    self.main_view.state.update_notice_lesson_id(index, new_lesson_id)
            self.main_view.list_view.refresh()
            self.main_view.refresh_status()

        self.module_form.refresh_status()
        self.refresh()

    # -------------------------------------------------------------- save

    def request_save_module(self) -> None:
        module_id = self.main_view.module_state.selected_module_id
        if module_id is None:
            return
        confirmation_dialog.confirm_save_module(
            self.main_view.page, module_id=module_id, on_confirm=lambda: self._do_save(module_id)
        )

    def _show_blocked(self, exc: ModuleSaveBlockedError) -> None:
        messages = "\n".join(f"{issue.field}: {issue.message}" for issue in exc.result.errors)
        confirmation_dialog.show_message(
            self.main_view.page, title="Não foi possível salvar", message=f"Módulo inválido:\n{messages}"
        )

    def _on_saved(self, module_id: str) -> None:
        self.module_form.load_module(self.main_view.module_state.get_module(module_id))
        self.module_list.refresh()
        confirmation_dialog.show_message(
            self.main_view.page, title="Salvo", message=f"assets/data/modulos/{module_id}.json atualizado com sucesso."
        )

    def _do_save(self, module_id: str) -> None:
        try:
            self.main_view.module_state.save_module(module_id)
        except ModuleSaveBlockedError as exc:
            self._show_blocked(exc)
            return
        except ModuleExternalChangeError:
            confirmation_dialog.confirm_module_external_change(
                self.main_view.page,
                on_reload=lambda: self._do_reload(module_id),
                on_overwrite=lambda: self._do_save_overriding(module_id),
            )
            return
        self._on_saved(module_id)

    def _do_save_overriding(self, module_id: str) -> None:
        try:
            self.main_view.module_state.save_module_overriding_external_change(module_id)
        except ModuleSaveBlockedError as exc:
            self._show_blocked(exc)
            return
        self._on_saved(module_id)

    def request_reload_module(self) -> None:
        module_id = self.main_view.module_state.selected_module_id
        if module_id is None:
            return
        if self.main_view.module_state.is_dirty(module_id):
            confirmation_dialog.confirm_reload_module(self.main_view.page, on_confirm=lambda: self._do_reload(module_id))
        else:
            self._do_reload(module_id)

    def _do_reload(self, module_id: str) -> None:
        self.main_view.module_state.reload_module(module_id)
        self.main_view.module_state.select_lesson(None)
        self.module_form.load_module(self.main_view.module_state.get_module(module_id))
        self.module_list.refresh()
        self.refresh()


__all__ = ["ModuleView"]
