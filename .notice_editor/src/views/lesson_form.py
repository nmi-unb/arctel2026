from __future__ import annotations

from typing import Optional

import flet as ft

from services.dataStructure.lesson import Lesson
from services.dataStructure.LessonLinks import LessonLinks
from services.dataStructure.lesson_materials import LessonMaterialItem, LessonMaterials
from services.generic.values.constants import LINK_TYPE_LABELS
from views import confirmation_dialog
from views.form_widgets import DateTimeInput, info_row


class _MaterialItemRow:
    def __init__(self, item: Optional[LessonMaterialItem], on_remove) -> None:
        self.original = item
        self.title_field = ft.TextField(label="title", value=(item.titulo if item else ""), expand=True)
        self.url_field = ft.TextField(label="url", value=(item.url if item and item.url else ""), expand=True)
        self.available_checkbox = ft.Checkbox(label="disponível", value=item.disponivel if item else True)
        self.remove_button = ft.IconButton(ft.Icons.DELETE, tooltip="Remover", icon_color=ft.Colors.RED_700, on_click=lambda e: on_remove(self))
        self.row = ft.Row(
            [self.title_field, self.url_field, self.available_checkbox, self.remove_button],
            spacing=6,
        )

    def to_item(self) -> LessonMaterialItem:
        return LessonMaterialItem(
            titulo=(self.title_field.value or "").strip(),
            url=(self.url_field.value or "").strip() or None,
            disponivel=bool(self.available_checkbox.value),
            extra_fields=self.original.extra_fields if self.original else {},
        )


class _MaterialGroupEditor:
    def __init__(self, label: str) -> None:
        self.label = label
        self._rows: list[_MaterialItemRow] = []
        self.rows_column = ft.Column([], spacing=4)
        self.add_button = ft.TextButton(f"+ Adicionar em {label}", on_click=self._on_add_click)
        self.control = ft.Column([ft.Text(label, size=12, weight=ft.FontWeight.BOLD), self.rows_column, self.add_button], spacing=4)

    def load(self, items: tuple[LessonMaterialItem, ...]) -> None:
        self._rows = [_MaterialItemRow(item, self._on_remove) for item in items]
        self._refresh()

    def _on_add_click(self, e: ft.Event) -> None:
        self._rows.append(_MaterialItemRow(None, self._on_remove))
        self._refresh()

    def _on_remove(self, row: _MaterialItemRow) -> None:
        self._rows.remove(row)
        self._refresh()

    def _refresh(self) -> None:
        self.rows_column.controls = [row.row for row in self._rows]

    def to_items(self) -> tuple[LessonMaterialItem, ...]:
        return tuple(row.to_item() for row in self._rows if row.title_field.value or row.url_field.value)


class LessonFormView:
    def __init__(self, module_view) -> None:
        self.module_view = module_view
        self.module_id: Optional[str] = None
        self.original_lesson: Optional[Lesson] = None

        self.numero_field = ft.TextField(label="numero", read_only=True, width=100)
        self.renumber_button = ft.TextButton("Alterar número...", on_click=self._on_renumber_click)
        self.titulo_field = ft.TextField(label="titulo")
        self.data_inicio_input = DateTimeInput("dataInicio")
        self.data_fim_input = DateTimeInput("dataFim")

        self.link_fields: dict[str, ft.TextField] = {
            link_type: ft.TextField(label=f"links.{link_type} ({label})", hint_text="URL ou vazio para null")
            for link_type, label in LINK_TYPE_LABELS.items()
        }

        self.professor_editor = _MaterialGroupEditor("materials.professor")
        self.replacement_editor = _MaterialGroupEditor("materials.replacementCourses")

        self.error_column = ft.Column([], spacing=2)

        self.apply_button = ft.FilledButton("Aplicar aula", icon=ft.Icons.CHECK_CIRCLE, on_click=self._on_apply_click)
        self.cancel_button = ft.OutlinedButton("Cancelar edição da aula", on_click=self._on_cancel_click)

        scrollable = ft.Column(
            [
                ft.Text("Formulário da aula", weight=ft.FontWeight.BOLD, size=14),
                ft.Row([self.numero_field, self.renumber_button]),
                info_row(self.titulo_field, "Título da aula.", required=True),
                info_row(self.data_inicio_input.control, "Início da aula. Deve estar preenchida junto com dataFim, ou ambas ausentes."),
                info_row(self.data_fim_input.control, "Fim da aula — deve ser posterior ao início."),
                ft.Divider(),
                ft.Text("Links", weight=ft.FontWeight.BOLD, size=13),
                *[info_row(field, f"Link de {link_type}. Campo vazio é salvo como null.") for link_type, field in self.link_fields.items()],
                ft.Divider(),
                ft.Text("Materiais", weight=ft.FontWeight.BOLD, size=13),
                self.professor_editor.control,
                self.replacement_editor.control,
                self.error_column,
            ],
            spacing=8,
            scroll=ft.ScrollMode.AUTO,
            expand=True,
        )
        footer = ft.Row([self.apply_button, self.cancel_button])
        self.container = ft.Column([scrollable, footer], expand=True, spacing=10)

        self.load_lesson(None, None)

    def load_lesson(self, module_id: Optional[str], lesson: Optional[Lesson]) -> None:
        self.module_id = module_id
        self.original_lesson = lesson
        base = lesson or Lesson(
            numero=0, titulo="", data_inicio=None, data_fim=None,
            links=LessonLinks.from_dict({}), materials=LessonMaterials.from_dict({}),
        )
        self.numero_field.value = str(base.numero) if lesson else ""
        self.titulo_field.value = base.titulo
        self.data_inicio_input.set_iso(base.data_inicio)
        self.data_fim_input.set_iso(base.data_fim)
        for link_type, field in self.link_fields.items():
            field.value = base.links.get(link_type) or ""
        self.professor_editor.load(base.materials.professor)
        self.replacement_editor.load(base.materials.replacement_courses)
        self._clear_errors()

    def build_lesson(self) -> Lesson:
        links = LessonLinks(
            teams=(self.link_fields["teams"].value or "").strip() or None,
            youtube_live=(self.link_fields["youtubeLive"].value or "").strip() or None,
            youtube_recorded=(self.link_fields["youtubeRecorded"].value or "").strip() or None,
        )
        materials = LessonMaterials(
            professor=self.professor_editor.to_items(),
            replacement_courses=self.replacement_editor.to_items(),
        )
        return Lesson(
            numero=self.original_lesson.numero if self.original_lesson else 0,
            titulo=(self.titulo_field.value or "").strip(),
            data_inicio=self.data_inicio_input.get_iso(),
            data_fim=self.data_fim_input.get_iso(),
            links=links,
            materials=materials,
            extra_fields=self.original_lesson.extra_fields if self.original_lesson else {},
        )

    def has_unapplied_changes(self) -> bool:
        if self.original_lesson is None:
            return False
        return self.build_lesson() != self.original_lesson

    def _clear_errors(self) -> None:
        self.error_column.controls = []

    def _show_errors(self, messages: list[str]) -> None:
        self.error_column.controls = [ft.Text(f"• {message}", color=ft.Colors.RED_700, size=12) for message in messages]

    def _on_apply_click(self, e: ft.Event) -> None:
        if self.original_lesson is None:
            return
        lesson = self.build_lesson()
        errors = self.module_view.validate_lesson_form(lesson)
        if errors:
            self._show_errors(errors)
            return
        self._clear_errors()
        self.module_view.apply_lesson_from_form(lesson)
        self.original_lesson = lesson

    def _on_cancel_click(self, e: ft.Event) -> None:
        if self.has_unapplied_changes():
            confirmation_dialog.confirm_discard_edit(self.module_view.main_view.page, on_confirm=self.module_view.cancel_lesson_edit)
        else:
            self.module_view.cancel_lesson_edit()

    def _on_renumber_click(self, e: ft.Event) -> None:
        if self.original_lesson is None:
            return
        self.module_view.request_renumber_lesson(self.original_lesson.numero)


__all__ = ["LessonFormView"]
