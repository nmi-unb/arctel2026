from __future__ import annotations

import flet as ft

from views import confirmation_dialog


class LessonListView:
    def __init__(self, module_view) -> None:
        self.module_view = module_view

        self.new_button = ft.FilledButton("Aula", icon=ft.Icons.ADD, on_click=self._on_new_click)
        self.sort_numero_button = ft.OutlinedButton("Ordenar por número", on_click=self._on_sort_numero_click)
        self.sort_data_button = ft.OutlinedButton("Ordenar por data", on_click=self._on_sort_data_click)

        self.rows_column = ft.Column([], spacing=6, scroll=ft.ScrollMode.AUTO, expand=True)

        self.container = ft.Column(
            [
                ft.Row([ft.Text("Aulas", weight=ft.FontWeight.BOLD, size=13), ft.Container(expand=True), self.new_button]),
                ft.Column([self.sort_numero_button, self.sort_data_button], spacing=6),
                ft.Divider(),
                self.rows_column,
            ],
            expand=True,
            spacing=8,
        )

    def refresh(self) -> None:
        module_state = self.module_view.main_view.module_state
        module_id = module_state.selected_module_id
        module = module_state.get_module(module_id) if module_id else None
        if module is None:
            self.rows_column.controls = [ft.Text("Selecione um módulo.", color=ft.Colors.ON_SURFACE_VARIANT)]
            return
        if not module.lessons:
            self.rows_column.controls = [ft.Text("Nenhuma aula cadastrada.", color=ft.Colors.ON_SURFACE_VARIANT)]
            return

        total = len(module.lessons)
        rows: list[ft.Control] = []
        for index, lesson in enumerate(module.lessons):
            is_selected = module_state.selected_lesson_numero == lesson.numero
            rows.append(self._build_row(lesson, index, total, is_selected))
        self.rows_column.controls = rows

    def _build_row(self, lesson, index: int, total: int, is_selected: bool) -> ft.Control:
        header = ft.Row(
            [
                ft.Text(f"Aula {lesson.numero}", weight=ft.FontWeight.BOLD, expand=True),
            ],
            spacing=8,
        )
        actions = ft.Row(
            [
                ft.IconButton(ft.Icons.EDIT, tooltip="Editar", on_click=lambda e, n=lesson.numero: self.module_view.select_lesson(n)),
                ft.IconButton(
                    ft.Icons.CONTENT_COPY,
                    tooltip="Duplicar",
                    on_click=lambda e, n=lesson.numero: self.module_view.duplicate_lesson(n),
                ),
                ft.IconButton(
                    ft.Icons.ARROW_UPWARD,
                    tooltip="Mover para cima",
                    disabled=index == 0,
                    on_click=lambda e, n=lesson.numero: self.module_view.move_lesson(n, -1),
                ),
                ft.IconButton(
                    ft.Icons.ARROW_DOWNWARD,
                    tooltip="Mover para baixo",
                    disabled=index == total - 1,
                    on_click=lambda e, n=lesson.numero: self.module_view.move_lesson(n, 1),
                ),
                ft.IconButton(
                    ft.Icons.DELETE,
                    tooltip="Remover",
                    icon_color=ft.Colors.RED_700,
                    on_click=lambda e, n=lesson.numero: self.module_view.request_remove_lesson(n),
                ),
            ],
            spacing=0,
        )
        return ft.Container(
            content=ft.Column([header, ft.Text(lesson.titulo, size=12, color=ft.Colors.ON_SURFACE_VARIANT), actions], spacing=2),
            padding=8,
            border=ft.Border.all(width=2 if is_selected else 1, color=ft.Colors.PRIMARY if is_selected else ft.Colors.OUTLINE),
            border_radius=6,
            bgcolor=ft.Colors.PRIMARY_CONTAINER if is_selected else None,
        )

    def _on_new_click(self, e: ft.Event) -> None:
        self.module_view.create_lesson()

    def _on_sort_numero_click(self, e: ft.Event) -> None:
        module_id = self.module_view.main_view.module_state.selected_module_id
        if not module_id:
            return
        confirmation_dialog.show_confirmation(
            self.module_view.main_view.page,
            title="Ordenar aulas por número",
            message="Isso substituirá a ordem física atual do array 'lessons' em memória. A ordem só é gravada após \"Salvar módulo\". Deseja continuar?",
            on_confirm=lambda: self.module_view.sort_lessons_by_numero(),
            confirm_label="Ordenar",
        )

    def _on_sort_data_click(self, e: ft.Event) -> None:
        module_id = self.module_view.main_view.module_state.selected_module_id
        if not module_id:
            return
        confirmation_dialog.show_confirmation(
            self.module_view.main_view.page,
            title="Ordenar aulas por data",
            message="Isso substituirá a ordem física atual do array 'lessons' em memória. A ordem só é gravada após \"Salvar módulo\". Deseja continuar?",
            on_confirm=lambda: self.module_view.sort_lessons_by_data(),
            confirm_label="Ordenar",
        )


__all__ = ["LessonListView"]
