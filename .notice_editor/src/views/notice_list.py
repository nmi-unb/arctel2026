from __future__ import annotations

import flet as ft

from services.dataStructure.notice import Notice
from services.generic.values.constants import LINK_SOURCE_LEGACY, LINK_SOURCE_NONE, LIST_FILTERS
from services.validation_service import ValidationResult


class NoticeListView:
    def __init__(self, main_view) -> None:
        self.main_view = main_view

        self.filter_dropdown = ft.Dropdown(
            label="Filtro",
            value="Todos",
            options=[ft.DropdownOption(key=name, text=name) for name in LIST_FILTERS],
            on_select=self._on_filter_change,
        )
        self.new_button = ft.FilledButton("Novo aviso", icon=ft.Icons.ADD, on_click=self._on_new_click)
        self.sort_publicacao_button = ft.OutlinedButton(
            "Ordenar por publicação", on_click=self._on_sort_publicacao_click
        )
        self.sort_prioridade_button = ft.OutlinedButton(
            "Ordenar por prioridade", on_click=self._on_sort_prioridade_click
        )
        self.rows_column = ft.Column([], spacing=6, scroll=ft.ScrollMode.AUTO, expand=True)

        self.container = ft.Column(
            [
                ft.Row([self.filter_dropdown, self.new_button]),
                ft.Column([self.sort_publicacao_button, self.sort_prioridade_button], spacing=6),
                ft.Divider(),
                self.rows_column,
            ],
            expand=True,
        )

    def refresh(self) -> None:
        notices = self.main_view.state.notices
        results = self.main_view.state.validate_all()
        total = len(notices)
        visible = [
            (index, notice)
            for index, notice in enumerate(notices)
            if self._matches_filter(notice)
        ]
        if not visible:
            self.rows_column.controls = [
                ft.Text("Nenhum aviso corresponde ao filtro selecionado.", color=ft.Colors.ON_SURFACE_VARIANT)
            ]
            return
        self.rows_column.controls = [
            self._build_row(index, notice, results.get(notice.id), total)
            for index, notice in visible
        ]

    def _matches_filter(self, notice: Notice) -> bool:
        current = self.filter_dropdown.value
        if current == "Ativos":
            return notice.ativo
        if current == "Histórico":
            return not notice.ativo
        if current == "Aulas":
            return notice.is_lesson_notice
        if current == "Informativos":
            return not notice.is_lesson_notice
        if current == "Com link":
            return notice.link_source != LINK_SOURCE_NONE
        if current == "Sem link":
            return notice.link_source == LINK_SOURCE_NONE
        if current == "Legados":
            return notice.link_source == LINK_SOURCE_LEGACY
        return True

    def _build_row(
        self, index: int, notice: Notice, result: ValidationResult | None, total: int
    ) -> ft.Control:
        is_selected = self.main_view.form.editing_index == index
        status_icon = (
            ft.Icon(ft.Icons.CHECK_CIRCLE, color=ft.Colors.GREEN_700, size=16)
            if notice.ativo
            else ft.Icon(ft.Icons.HISTORY, color=ft.Colors.GREY_600, size=16)
        )
        badges: list[ft.Control] = []
        if result is not None and not result.is_valid:
            badges.append(ft.Icon(ft.Icons.WARNING_AMBER, color=ft.Colors.RED_700, size=16, tooltip="Aviso inválido"))
        if notice.link_source == LINK_SOURCE_LEGACY:
            badges.append(ft.Text("legado", size=10, color=ft.Colors.AMBER_700))

        header = ft.Row(
            [
                ft.Text(str(index + 1), width=28),
                status_icon,
                ft.Text(notice.titulo or "(sem título)", weight=ft.FontWeight.BOLD, expand=True),
                *badges,
            ],
            spacing=8,
        )

        actions = ft.Row(
            [
                ft.IconButton(
                    ft.Icons.EDIT, tooltip="Editar", on_click=lambda e, i=index: self.main_view.start_edit(i)
                ),
                ft.IconButton(
                    ft.Icons.CONTENT_COPY,
                    tooltip="Duplicar",
                    on_click=lambda e, i=index: self.main_view.duplicate_notice(i),
                ),
                ft.IconButton(
                    ft.Icons.VISIBILITY_OFF if notice.ativo else ft.Icons.VISIBILITY,
                    tooltip="Desativar" if notice.ativo else "Reativar",
                    on_click=lambda e, i=index: self.main_view.toggle_active(i),
                ),
                ft.IconButton(
                    ft.Icons.ARROW_UPWARD,
                    tooltip="Mover para cima",
                    disabled=index == 0,
                    on_click=lambda e, i=index: self.main_view.move_notice(i, -1),
                ),
                ft.IconButton(
                    ft.Icons.ARROW_DOWNWARD,
                    tooltip="Mover para baixo",
                    disabled=index == total - 1,
                    on_click=lambda e, i=index: self.main_view.move_notice(i, 1),
                ),
                ft.IconButton(
                    ft.Icons.DELETE,
                    tooltip="Excluir definitivamente",
                    icon_color=ft.Colors.RED_700,
                    on_click=lambda e, i=index: self.main_view.request_delete(i),
                ),
            ],
            spacing=0,
        )

        return ft.Container(
            content=ft.Column([header, actions], spacing=2),
            padding=8,
            border=ft.Border.all(width=2 if is_selected else 1, color=ft.Colors.PRIMARY if is_selected else ft.Colors.OUTLINE),
            border_radius=6,
            bgcolor=ft.Colors.PRIMARY_CONTAINER if is_selected else None,
        )

    def _on_filter_change(self, e: ft.Event) -> None:
        self.refresh()

    def _on_new_click(self, e: ft.Event) -> None:
        self.main_view.start_new()

    def _on_sort_publicacao_click(self, e: ft.Event) -> None:
        self.main_view.request_sort_publicacao()

    def _on_sort_prioridade_click(self, e: ft.Event) -> None:
        self.main_view.request_sort_prioridade()


__all__ = ["NoticeListView"]
