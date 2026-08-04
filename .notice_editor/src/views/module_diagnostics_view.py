from __future__ import annotations

import flet as ft

from services import module_repository, reference_service, validation_service


class ModuleDiagnosticsView:
    def __init__(self, main_view) -> None:
        self.main_view = main_view
        self.content_column = ft.Column([], spacing=10, scroll=ft.ScrollMode.AUTO)
        self.dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Diagnóstico geral de módulos"),
            content=ft.Container(content=self.content_column, width=640, height=460),
            actions=[ft.TextButton("Fechar", on_click=self._on_close)],
        )

    def open(self) -> None:
        self.refresh()
        self.main_view.page.show_dialog(self.dialog)

    def refresh(self) -> None:
        rows: list[ft.Control] = []

        structural = module_repository.diagnose_index_files()
        if structural["missing_files"]:
            rows.append(
                self._section(
                    "Entradas do índice sem arquivo",
                    [f"dataFile ausente: {name}" for name in structural["missing_files"]],
                    ft.Colors.RED_700,
                )
            )
        if structural["orphan_files"]:
            rows.append(
                self._section(
                    "Arquivos não listados no índice", structural["orphan_files"], ft.Colors.AMBER_700
                )
            )

        module_issues: list[str] = []
        for summary in module_repository.list_modules():
            try:
                module = module_repository.get_module(summary.id)
            except module_repository.ModuleRepositoryError as exc:
                module_issues.append(f"{summary.id}: {exc}")
                continue
            result = validation_service.validate_module(module)
            for issue in result.errors:
                module_issues.append(f"{module.id} — {issue.field}: {issue.message}")
            for issue in result.warnings:
                module_issues.append(f"{module.id} — {issue.field}: {issue.message} (aviso)")
        if module_issues:
            rows.append(self._section("Módulos e aulas com problemas", module_issues, ft.Colors.RED_700))

        broken = reference_service.find_broken_notice_references(self.main_view.state.notices)
        if broken:
            rows.append(
                self._section(
                    "Avisos com referência quebrada",
                    [f"{item.notice.id} ({item.module_id}/{item.lesson_id}): {item.reason}" for item in broken],
                    ft.Colors.RED_700,
                )
            )

        if not rows:
            rows.append(ft.Text("Nenhuma inconsistência encontrada.", color=ft.Colors.GREEN_700))

        self.content_column.controls = rows

    def _section(self, title: str, lines: list[str], color: str) -> ft.Control:
        return ft.Column(
            [
                ft.Text(f"{title} ({len(lines)})", weight=ft.FontWeight.BOLD, size=13),
                *[ft.Text(f"• {line}", size=12, color=color) for line in lines],
                ft.Divider(),
            ],
            spacing=2,
        )

    def _on_close(self, e: ft.Event) -> None:
        self.main_view.page.pop_dialog()


__all__ = ["ModuleDiagnosticsView"]
