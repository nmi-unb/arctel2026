from __future__ import annotations

import flet as ft


class DiagnosticsView:
    def __init__(self, main_view) -> None:
        self.main_view = main_view
        self.content_column = ft.Column([], spacing=10, scroll=ft.ScrollMode.AUTO)
        self.dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Diagnóstico e migração de URLs legadas"),
            content=ft.Container(content=self.content_column, width=560, height=420),
            actions=[ft.TextButton("Fechar", on_click=self._on_close)],
        )

    def open(self) -> None:
        self.refresh()
        self.main_view.page.show_dialog(self.dialog)

    def refresh(self) -> None:
        report = self.main_view.state.legacy_report()
        if not report:
            self.content_column.controls = [ft.Text("Nenhum registro legado encontrado.")]
            return

        notices = self.main_view.state.notices
        rows: list[ft.Control] = [ft.Text(f"{len(report)} registro(s) legado(s) encontrados.")]
        for record in report:
            notice = record.notice
            index = next(i for i, item in enumerate(notices) if item is notice)
            suggestion = record.suggested_reference

            static_field = ft.TextField(label="staticLink", hint_text="#modulos", width=220)

            def _migrate_static(e: ft.Event, i: int = index, field: ft.TextField = static_field) -> None:
                value = (field.value or "").strip()
                if not value:
                    return
                self.main_view.migrate_legacy_to_static(i, value)
                self.refresh()

            def _migrate_lesson(e: ft.Event, i: int = index, s=suggestion) -> None:
                if s is None:
                    return
                self.main_view.migrate_legacy_to_lesson(i, s.module_id, s.lesson_id, s.link_type)
                self.refresh()

            if suggestion is not None:
                suggestion_text = f"Sugestão automática: {suggestion.module_id} / {suggestion.lesson_id} / {suggestion.link_type}"
                suggestion_color = ft.Colors.GREEN_700
            else:
                suggestion_text = "Nenhuma correspondência automática encontrada nos módulos."
                suggestion_color = ft.Colors.AMBER_700

            rows.append(
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Text(f"{notice.id} — {notice.titulo}", weight=ft.FontWeight.BOLD),
                            ft.Text(f"url atual: {notice.url}", size=11, color=ft.Colors.ON_SURFACE_VARIANT),
                            ft.Text(suggestion_text, size=11, color=suggestion_color),
                            ft.Row(
                                [
                                    ft.FilledButton(
                                        "Migrar para referência de aula",
                                        disabled=suggestion is None,
                                        on_click=_migrate_lesson,
                                    ),
                                    static_field,
                                    ft.OutlinedButton("Migrar para link estático", on_click=_migrate_static),
                                ],
                                wrap=True,
                            ),
                        ],
                        spacing=4,
                    ),
                    padding=8,
                    border=ft.Border.all(width=1, color=ft.Colors.OUTLINE),
                    border_radius=6,
                )
            )
        self.content_column.controls = rows

    def _on_close(self, e: ft.Event) -> None:
        self.main_view.page.pop_dialog()


__all__ = ["DiagnosticsView"]
