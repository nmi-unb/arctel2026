from __future__ import annotations

import flet as ft


class ModuleListView:
    def __init__(self, module_view) -> None:
        self.module_view = module_view
        self.rows_column = ft.Column([], spacing=6, scroll=ft.ScrollMode.AUTO, expand=True)
        self.container = ft.Column(
            [ft.Text("Módulos", weight=ft.FontWeight.BOLD, size=13), self.rows_column],
            expand=True,
            spacing=8,
        )

    def refresh(self) -> None:
        state = self.module_view.main_view.module_state
        if state.load_error:
            self.rows_column.controls = [
                ft.Text(f"Erro ao carregar índice: {state.load_error}", color=ft.Colors.RED_700)
            ]
            return

        rows: list[ft.Control] = []
        for summary in state.summaries:
            is_selected = state.selected_module_id == summary.id
            dirty = state.is_dirty(summary.id)
            rows.append(
                ft.Container(
                    content=ft.Row(
                        [
                            ft.Text(f"{summary.number:02d}", width=28),
                            ft.Text(summary.title, expand=True, overflow=ft.TextOverflow.ELLIPSIS),
                            ft.Icon(ft.Icons.EDIT_NOTE, size=16, color=ft.Colors.AMBER_700, visible=dirty, tooltip="alterações não salvas"),
                        ],
                        spacing=6,
                    ),
                    padding=8,
                    border=ft.Border.all(width=2 if is_selected else 1, color=ft.Colors.PRIMARY if is_selected else ft.Colors.OUTLINE),
                    border_radius=6,
                    bgcolor=ft.Colors.PRIMARY_CONTAINER if is_selected else None,
                    on_click=lambda e, module_id=summary.id: self.module_view.select_module(module_id),
                    ink=True,
                )
            )
        self.rows_column.controls = rows or [ft.Text("Nenhum módulo encontrado.", color=ft.Colors.ON_SURFACE_VARIANT)]


__all__ = ["ModuleListView"]
