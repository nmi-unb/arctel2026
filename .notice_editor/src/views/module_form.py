from __future__ import annotations

from typing import Optional

import flet as ft

from services.dataStructure.module import Module


class ModuleFormView:
    def __init__(self, module_view) -> None:
        self.module_view = module_view
        self._module: Optional[Module] = None

        self.numero_field = ft.TextField(label="modulo", read_only=True, width=100)
        self.titulo_field = ft.TextField(label="titulo", expand=True, on_change=self._on_titulo_change)
        self.save_button = ft.FilledButton("Salvar módulo", icon=ft.Icons.SAVE, on_click=self._on_save_click)
        self.reload_button = ft.OutlinedButton("Recarregar módulo", icon=ft.Icons.REFRESH, on_click=self._on_reload_click)
        self.status_text = ft.Text("", size=13)

        self.container = ft.Column(
            [
                ft.Row([self.numero_field, ft.Container(content=self.titulo_field, expand=True)]),
                self.status_text,
                ft.Row([self.save_button, self.reload_button]),
            ],
            spacing=8,
        )
        self.load_module(None)

    def load_module(self, module: Optional[Module]) -> None:
        self._module = module
        if module is None:
            self.numero_field.value = ""
            self.titulo_field.value = ""
            self.status_text.value = "Nenhum módulo selecionado."
            self.status_text.color = ft.Colors.ON_SURFACE_VARIANT
            return
        self.numero_field.value = str(module.number)
        self.titulo_field.value = module.title
        self.refresh_status()

    def refresh_status(self) -> None:
        if self._module is None:
            return
        module_state = self.module_view.main_view.module_state
        if module_state.is_dirty(self._module.id):
            self.status_text.value = f"Módulo {self._module.number}: alterações não salvas"
            self.status_text.color = ft.Colors.AMBER_700
        else:
            self.status_text.value = f"Módulo {self._module.number}: salvo"
            self.status_text.color = ft.Colors.ON_SURFACE_VARIANT

    def _on_titulo_change(self, e: ft.Event) -> None:
        if self._module is None:
            return
        self.module_view.update_title(self.titulo_field.value or "")

    def _on_save_click(self, e: ft.Event) -> None:
        self.module_view.request_save_module()

    def _on_reload_click(self, e: ft.Event) -> None:
        self.module_view.request_reload_module()


__all__ = ["ModuleFormView"]
