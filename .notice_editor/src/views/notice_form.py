from __future__ import annotations

import re
from typing import Optional

import flet as ft

from services import module_repository
from services.dataStructure.notice import Notice
from services.generic.values.constants import (
    DEFAULT_TEXTO_LINK,
    LINK_SOURCE_LABELS,
    LINK_SOURCE_LEGACY,
    LINK_SOURCE_LESSON,
    LINK_SOURCE_NONE,
    LINK_SOURCE_STATIC,
    LINK_TYPE_LABELS,
    NOTICE_TYPES,
)
from views import confirmation_dialog

_SLUG_PATTERN = re.compile(r"[^a-z0-9]+")


def _slugify(text: str) -> str:
    slug = _SLUG_PATTERN.sub("-", text.lower()).strip("-")
    return slug or "aviso"


def _group(title: str, controls: list[ft.Control]) -> ft.Column:
    return ft.Column(
        [ft.Text(title, weight=ft.FontWeight.BOLD, size=13), *controls, ft.Divider()],
        spacing=8,
    )


class NoticeFormView:
    def __init__(self, main_view) -> None:
        self.main_view = main_view
        self.editing_index: Optional[int] = None
        self.original_notice: Optional[Notice] = None
        self._current_source = LINK_SOURCE_NONE

        # Identificação
        self.id_field = ft.TextField(label="id")
        self.suggest_id_button = ft.TextButton(
            "Sugerir id a partir do título", on_click=self._on_suggest_id
        )

        # Conteúdo
        self.titulo_field = ft.TextField(label="titulo")
        self.mensagem_field = ft.TextField(label="mensagem", multiline=True, min_lines=3, max_lines=6)
        self.texto_link_field = ft.TextField(label="textoLink (opcional)", hint_text=DEFAULT_TEXTO_LINK)

        # Classificação
        self.tipo_dropdown = ft.Dropdown(
            label="tipo",
            options=[ft.DropdownOption(key=tipo, text=tipo) for tipo in NOTICE_TYPES],
        )
        self.prioridade_field = ft.TextField(
            label="prioridade (opcional)", keyboard_type=ft.KeyboardType.NUMBER
        )
        self.ativo_checkbox = ft.Checkbox(label="ativo", value=True)

        # Agendamento
        self.data_publicacao_field = ft.TextField(
            label="dataPublicacao", hint_text="2026-08-21T08:00:00-03:00"
        )
        self.data_inicio_field = ft.TextField(
            label="dataInicio (opcional, aula)", hint_text="2026-08-21T08:00:00-03:00"
        )
        self.data_fim_field = ft.TextField(
            label="dataFim (opcional, aula)", hint_text="2026-08-21T10:00:00-03:00"
        )

        # Fonte do link
        self._radio_legacy = ft.Radio(value=LINK_SOURCE_LEGACY, label=LINK_SOURCE_LABELS[LINK_SOURCE_LEGACY])
        self.link_source_radio = ft.RadioGroup(
            content=ft.Column(
                [
                    ft.Radio(value=LINK_SOURCE_NONE, label=LINK_SOURCE_LABELS[LINK_SOURCE_NONE]),
                    ft.Radio(value=LINK_SOURCE_LESSON, label=LINK_SOURCE_LABELS[LINK_SOURCE_LESSON]),
                    ft.Radio(value=LINK_SOURCE_STATIC, label=LINK_SOURCE_LABELS[LINK_SOURCE_STATIC]),
                    self._radio_legacy,
                ]
            ),
            value=LINK_SOURCE_NONE,
            on_change=self._on_link_source_change,
        )

        self.module_dropdown = ft.Dropdown(label="Módulo", on_select=self._on_module_change)
        self.lesson_dropdown = ft.Dropdown(label="Aula", on_select=self._on_lesson_change, disabled=True)
        self.link_type_dropdown = ft.Dropdown(
            label="Tipo de link",
            options=[ft.DropdownOption(key=key, text=label) for key, label in LINK_TYPE_LABELS.items()],
            on_select=self._on_link_type_change,
            disabled=True,
        )
        self.link_availability_text = ft.Text("", size=12)
        self.lesson_group = ft.Column(
            [self.module_dropdown, self.lesson_dropdown, self.link_type_dropdown, self.link_availability_text],
            visible=False,
        )

        self.static_link_field = ft.TextField(label="staticLink", hint_text="#modulos")
        self.static_group = ft.Column([self.static_link_field], visible=False)

        self.legacy_url_field = ft.TextField(label="url (legado)", read_only=True)
        self.legacy_group = ft.Column(
            [
                ft.Text(
                    "Formato legado — migre para referência de aula ou link estático "
                    "no diagnóstico de URLs legadas.",
                    size=11,
                    color=ft.Colors.AMBER_700,
                ),
                self.legacy_url_field,
            ],
            visible=False,
        )

        # Arquivamento
        self.arquivar_apos_field = ft.TextField(label="arquivarApos (opcional)")
        self.exibir_link_field = ft.TextField(label="exibirLinkAPartirDe (opcional)")

        self.error_column = ft.Column([], spacing=2)
        self.warning_column = ft.Column([], spacing=2)

        self.apply_button = ft.FilledButton("Aplicar", icon=ft.Icons.CHECK_CIRCLE, on_click=self._on_apply_click)
        self.cancel_button = ft.OutlinedButton("Cancelar edição", on_click=self._on_cancel_click)
        self.clear_button = ft.TextButton("Limpar formulário", on_click=self._on_clear_click)

        self.container = ft.Column(
            [
                ft.Text("Formulário de edição", weight=ft.FontWeight.BOLD, size=15),
                _group("Identificação", [self.id_field, self.suggest_id_button]),
                _group("Conteúdo", [self.titulo_field, self.mensagem_field, self.texto_link_field]),
                _group("Classificação", [self.tipo_dropdown, self.prioridade_field, self.ativo_checkbox]),
                _group(
                    "Agendamento",
                    [self.data_publicacao_field, self.data_inicio_field, self.data_fim_field],
                ),
                _group(
                    "Fonte do link",
                    [self.link_source_radio, self.lesson_group, self.static_group, self.legacy_group],
                ),
                _group("Arquivamento", [self.arquivar_apos_field, self.exibir_link_field]),
                self.error_column,
                self.warning_column,
                ft.Row([self.apply_button, self.cancel_button, self.clear_button]),
            ],
            spacing=10,
            scroll=ft.ScrollMode.AUTO,
        )

        self._populate_module_options()
        self.load_notice(None, None)

    # ------------------------------------------------------------------ load

    def load_notice(self, notice: Optional[Notice], index: Optional[int]) -> None:
        self.editing_index = index
        self.original_notice = notice
        is_new = notice is None
        base = notice or Notice(
            id="", titulo="", mensagem="", tipo=NOTICE_TYPES[0], data_publicacao="", ativo=True
        )

        self.id_field.value = base.id
        self.titulo_field.value = base.titulo
        self.mensagem_field.value = base.mensagem
        self.texto_link_field.value = base.texto_link or ""
        self.tipo_dropdown.value = base.tipo
        self.prioridade_field.value = "" if base.prioridade is None else str(base.prioridade)
        self.ativo_checkbox.value = base.ativo
        self.data_publicacao_field.value = base.data_publicacao
        self.data_inicio_field.value = base.data_inicio or ""
        self.data_fim_field.value = base.data_fim or ""
        self.arquivar_apos_field.value = base.arquivar_apos or ""
        self.exibir_link_field.value = base.exibir_link_a_partir_de or ""

        self.legacy_url_field.value = base.url or ""
        self.static_link_field.value = base.static_link or ""
        self._radio_legacy.disabled = not bool(base.url)

        self.module_dropdown.value = base.module_id
        if base.module_id:
            self._populate_lesson_options(base.module_id)
        else:
            self.lesson_dropdown.options = []
            self.lesson_dropdown.disabled = True
        self.lesson_dropdown.value = base.lesson_id
        self.link_type_dropdown.value = base.link_type
        self.link_type_dropdown.disabled = not bool(base.module_id)

        self._current_source = base.link_source
        self.link_source_radio.value = self._current_source
        self._apply_source_visibility()
        self._update_link_availability()
        self._clear_messages()
        _ = is_new  # reserved for future new-record-only affordances

    # ---------------------------------------------------------- populate ui

    def _populate_module_options(self) -> None:
        self.module_dropdown.options = [
            ft.DropdownOption(key=summary.id, text=f"{summary.number:02d} — {summary.title}")
            for summary in module_repository.list_modules()
        ]

    def _populate_lesson_options(self, module_id: str) -> None:
        try:
            module = module_repository.get_module(module_id)
        except module_repository.ModuleRepositoryError:
            self.lesson_dropdown.options = []
            self.lesson_dropdown.disabled = True
            return
        self.lesson_dropdown.options = [
            ft.DropdownOption(key=f"aula-{lesson.numero}", text=f"Aula {lesson.numero} — {lesson.titulo}")
            for lesson in module.lessons
        ]
        self.lesson_dropdown.disabled = False

    def _apply_source_visibility(self) -> None:
        source = self.link_source_radio.value
        self.lesson_group.visible = source == LINK_SOURCE_LESSON
        self.static_group.visible = source == LINK_SOURCE_STATIC
        self.legacy_group.visible = source == LINK_SOURCE_LEGACY

    def _update_link_availability(self) -> None:
        module_id = self.module_dropdown.value
        lesson_id = self.lesson_dropdown.value
        link_type = self.link_type_dropdown.value
        if not (module_id and lesson_id and link_type):
            self.link_availability_text.value = ""
            return
        try:
            link = module_repository.get_lesson_link(module_id, lesson_id, link_type)
        except module_repository.ModuleRepositoryError as exc:
            self.link_availability_text.value = f"Referência inválida: {exc}"
            self.link_availability_text.color = ft.Colors.RED_700
            return
        if link is None:
            self.link_availability_text.value = "Link ainda não definido — o aviso será exibido sem botão."
            self.link_availability_text.color = ft.Colors.AMBER_700
        else:
            self.link_availability_text.value = "Link disponível."
            self.link_availability_text.color = ft.Colors.GREEN_700

    # -------------------------------------------------------------- events

    def _on_module_change(self, e: ft.Event) -> None:
        self.lesson_dropdown.value = None
        self._populate_lesson_options(self.module_dropdown.value)
        self.link_type_dropdown.disabled = not bool(self.module_dropdown.value)
        self._update_link_availability()

    def _on_lesson_change(self, e: ft.Event) -> None:
        self._update_link_availability()

    def _on_link_type_change(self, e: ft.Event) -> None:
        self._update_link_availability()

    def _source_has_data(self, source: str) -> bool:
        if source == LINK_SOURCE_LESSON:
            return bool(self.module_dropdown.value or self.lesson_dropdown.value or self.link_type_dropdown.value)
        if source == LINK_SOURCE_STATIC:
            return bool(self.static_link_field.value)
        if source == LINK_SOURCE_LEGACY:
            return bool(self.legacy_url_field.value)
        return False

    def _clear_source_fields(self, source: str) -> None:
        if source == LINK_SOURCE_LESSON:
            self.module_dropdown.value = None
            self.lesson_dropdown.value = None
            self.lesson_dropdown.options = []
            self.lesson_dropdown.disabled = True
            self.link_type_dropdown.value = None
            self.link_type_dropdown.disabled = True
        elif source == LINK_SOURCE_STATIC:
            self.static_link_field.value = ""
        elif source == LINK_SOURCE_LEGACY:
            self.legacy_url_field.value = ""

    def _on_link_source_change(self, e: ft.Event) -> None:
        new_source = self.link_source_radio.value
        old_source = self._current_source
        if old_source == new_source:
            return

        def _commit() -> None:
            self._clear_source_fields(old_source)
            self._current_source = new_source
            self._apply_source_visibility()
            self._update_link_availability()

        if self._source_has_data(old_source):
            def _on_cancel() -> None:
                self.link_source_radio.value = old_source
                self._apply_source_visibility()

            confirmation_dialog.show_confirmation(
                self.main_view.page,
                title="Trocar fonte do link",
                message="Isso limpará os campos preenchidos da fonte atual. Continuar?",
                on_confirm=_commit,
                on_cancel=_on_cancel,
                confirm_label="Trocar",
                cancel_label="Cancelar",
            )
        else:
            _commit()

    def _on_suggest_id(self, e: ft.Event) -> None:
        if self.titulo_field.value:
            self.id_field.value = _slugify(self.titulo_field.value)

    def build_notice(self) -> Notice:
        source = self.link_source_radio.value
        module_id = lesson_id = link_type = static_link = url = None
        if source == LINK_SOURCE_LESSON:
            module_id = self.module_dropdown.value or None
            lesson_id = self.lesson_dropdown.value or None
            link_type = self.link_type_dropdown.value or None
        elif source == LINK_SOURCE_STATIC:
            static_link = (self.static_link_field.value or "").strip() or None
        elif source == LINK_SOURCE_LEGACY:
            url = (self.legacy_url_field.value or "").strip() or None

        prioridade_raw = (self.prioridade_field.value or "").strip()
        prioridade = int(prioridade_raw) if prioridade_raw else None

        return Notice(
            id=(self.id_field.value or "").strip(),
            titulo=(self.titulo_field.value or "").strip(),
            mensagem=(self.mensagem_field.value or "").strip(),
            tipo=self.tipo_dropdown.value or "",
            data_publicacao=(self.data_publicacao_field.value or "").strip(),
            ativo=bool(self.ativo_checkbox.value),
            data_inicio=(self.data_inicio_field.value or "").strip() or None,
            data_fim=(self.data_fim_field.value or "").strip() or None,
            module_id=module_id,
            lesson_id=lesson_id,
            link_type=link_type,
            static_link=static_link,
            url=url,
            texto_link=(self.texto_link_field.value or "").strip() or None,
            prioridade=prioridade,
            arquivar_apos=(self.arquivar_apos_field.value or "").strip() or None,
            exibir_link_a_partir_de=(self.exibir_link_field.value or "").strip() or None,
        )

    def _show_errors(self, messages: list[str]) -> None:
        self.error_column.controls = [
            ft.Text(f"• {message}", color=ft.Colors.RED_700, size=12) for message in messages
        ]

    def _show_warnings(self, messages: list[str]) -> None:
        self.warning_column.controls = [
            ft.Text(f"• {message}", color=ft.Colors.AMBER_700, size=12) for message in messages
        ]

    def _clear_messages(self) -> None:
        self.error_column.controls = []
        self.warning_column.controls = []

    def _on_apply_click(self, e: ft.Event) -> None:
        try:
            notice = self.build_notice()
        except ValueError:
            self._show_errors(["prioridade deve ser um número inteiro"])
            return

        if self.original_notice is not None and self.original_notice.id and notice.id != self.original_notice.id:
            def _proceed() -> None:
                self._commit_apply(notice)

            confirmation_dialog.confirm_id_change(self.main_view.page, on_confirm=_proceed)
            return

        self._commit_apply(notice)

    def _commit_apply(self, notice: Notice) -> None:
        result = self.main_view.state.validate_candidate(notice, self.editing_index)
        if not result.is_valid:
            self._show_errors([issue.message for issue in result.errors])
            return
        self._show_warnings([issue.message for issue in result.warnings])
        self.main_view.apply_notice_from_form(notice, self.editing_index)
        if self.editing_index is None:
            self.editing_index = len(self.main_view.state.notices) - 1
        self.original_notice = notice

    def has_unapplied_changes(self) -> bool:
        try:
            draft = self.build_notice()
        except ValueError:
            return True
        baseline = self.original_notice or Notice(
            id="", titulo="", mensagem="", tipo=NOTICE_TYPES[0], data_publicacao="", ativo=True
        )
        return draft != baseline

    def _on_cancel_click(self, e: ft.Event) -> None:
        if self.has_unapplied_changes():
            confirmation_dialog.confirm_discard_edit(
                self.main_view.page, on_confirm=self.main_view.cancel_edit
            )
        else:
            self.main_view.cancel_edit()

    def _on_clear_click(self, e: ft.Event) -> None:
        self.load_notice(None, None)


__all__ = ["NoticeFormView"]
