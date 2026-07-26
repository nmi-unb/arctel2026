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
    LINK_SOURCE_LIVE,
    LINK_SOURCE_NONE,
    LINK_SOURCE_STATIC,
    LINK_TYPE_LABELS,
    NOTICE_TYPES,
)
from views import confirmation_dialog
from views.form_widgets import DateTimeInput as _DateTimeInput
from views.form_widgets import info_row as _info

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
        self.data_publicacao_input = _DateTimeInput("dataPublicacao")
        self.data_inicio_input = _DateTimeInput("dataInicio (aula)")
        self.data_fim_input = _DateTimeInput("dataFim (aula)")

        # Fonte do link
        self._radio_legacy = ft.Radio(value=LINK_SOURCE_LEGACY, label=LINK_SOURCE_LABELS[LINK_SOURCE_LEGACY])
        self.link_source_radio = ft.RadioGroup(
            content=ft.Column(
                [
                    ft.Radio(value=LINK_SOURCE_NONE, label=LINK_SOURCE_LABELS[LINK_SOURCE_NONE]),
                    ft.Radio(value=LINK_SOURCE_LESSON, label=LINK_SOURCE_LABELS[LINK_SOURCE_LESSON]),
                    ft.Radio(value=LINK_SOURCE_STATIC, label=LINK_SOURCE_LABELS[LINK_SOURCE_STATIC]),
                    ft.Radio(value=LINK_SOURCE_LIVE, label=LINK_SOURCE_LABELS[LINK_SOURCE_LIVE]),
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

        self.live_teams_field = ft.TextField(label="liveLinks.teams (opcional)", hint_text="https://teams...")
        self.live_youtube_field = ft.TextField(
            label="liveLinks.youtubeLive (opcional)", hint_text="https://youtube.com/watch?v=..."
        )
        self.live_group = ft.Column([self.live_teams_field, self.live_youtube_field], visible=False)

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
        self.arquivar_apos_input = _DateTimeInput("arquivarApos")
        self.exibir_link_input = _DateTimeInput("exibirLinkAPartirDe")

        self.error_column = ft.Column([], spacing=2)
        self.warning_column = ft.Column([], spacing=2)

        self.apply_button = ft.FilledButton("Aplicar", icon=ft.Icons.CHECK_CIRCLE, on_click=self._on_apply_click)
        self.cancel_button = ft.OutlinedButton("Cancelar edição", on_click=self._on_cancel_click)
        self.clear_button = ft.TextButton("Limpar formulário", on_click=self._on_clear_click)

        scrollable = ft.Column(
            [
                ft.Text("Formulário de edição", weight=ft.FontWeight.BOLD, size=15),
                _group(
                    "Identificação",
                    [
                        _info(
                            self.id_field,
                            "Identificador único e estável do aviso, usado para detectar duplicados. "
                            "Evite espaços.",
                            required=True,
                        ),
                        self.suggest_id_button,
                    ],
                ),
                _group(
                    "Conteúdo",
                    [
                        _info(
                            self.titulo_field,
                            "Título em destaque, mostrado no quadro de avisos do site.",
                            required=True,
                        ),
                        _info(
                            self.mensagem_field,
                            "Texto do aviso (sem HTML), exibido abaixo do título.",
                            required=True,
                        ),
                        _info(
                            self.texto_link_field,
                            "Texto do botão de ação (ex.: 'Entrar na aula'). Se vazio, usa "
                            f"'{DEFAULT_TEXTO_LINK}'.",
                        ),
                    ],
                ),
                _group(
                    "Classificação",
                    [
                        _info(
                            self.tipo_dropdown,
                            "Define o selo (badge) exibido: confirmação, ao vivo, alteração, alerta, "
                            "material ou encerrado.",
                            required=True,
                        ),
                        _info(
                            self.prioridade_field,
                            "Número usado para desempate quando 2+ avisos disputam o destaque principal "
                            "— o maior vence.",
                        ),
                        _info(
                            self.ativo_checkbox,
                            "Se desmarcado, o aviso some do destaque/aula do site e vai para o histórico "
                            "— não é excluído, pode reativar depois.",
                        ),
                    ],
                ),
                _group(
                    "Agendamento",
                    [
                        _info(
                            self.data_publicacao_input.control,
                            "Data/hora consideradas a publicação — define a ordem no histórico e o "
                            "desempate de prioridade. Use o fuso -03:00 (Brasília), salvo exceção.",
                            required=True,
                        ),
                        _info(
                            self.data_inicio_input.control,
                            "Início da aula. Preencha junto com 'dataFim' para o site tratar este aviso "
                            "como aula com horário (mostra coluna própria 'Ao vivo'/'Aula programada').",
                        ),
                        _info(self.data_fim_input.control, "Fim da aula — deve ser posterior ao início."),
                    ],
                ),
                _group(
                    "Fonte do link",
                    [
                        _info(
                            self.link_source_radio,
                            "Escolha no máximo uma origem para o botão do aviso: aula cadastrada num "
                            "módulo, link fixo, transmissão ao vivo avulsa (Teams + YouTube) ou o "
                            "formato legado (url).",
                        ),
                        self.lesson_group,
                        self.static_group,
                        self.live_group,
                        self.legacy_group,
                    ],
                ),
                _group(
                    "Arquivamento",
                    [
                        _info(
                            self.arquivar_apos_input.control,
                            "Após esta data/hora, o aviso passa automaticamente para o histórico do site.",
                        ),
                        _info(
                            self.exibir_link_input.control,
                            "Antes desta data/hora, o(s) botão(ões) de link ficam ocultos/indisponíveis, "
                            "mesmo que o link já exista.",
                        ),
                    ],
                ),
                self.error_column,
                self.warning_column,
            ],
            spacing=10,
            scroll=ft.ScrollMode.AUTO,
            expand=True,
        )

        footer = ft.Container(
            content=ft.Row([self.apply_button, self.cancel_button, self.clear_button]),
            padding=ft.Padding.only(top=10, left=0, right=0, bottom=0),
            border=ft.Border.only(top=ft.BorderSide(width=1, color=ft.Colors.OUTLINE_VARIANT)),
        )

        scrollable_container = ft.Container(content=scrollable, padding=ft.Padding.only(right=16), expand=True)
        self.container = ft.Column([scrollable_container, footer], expand=True, spacing=10)

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
        self.data_publicacao_input.set_iso(base.data_publicacao or None)
        self.data_inicio_input.set_iso(base.data_inicio)
        self.data_fim_input.set_iso(base.data_fim)
        self.arquivar_apos_input.set_iso(base.arquivar_apos)
        self.exibir_link_input.set_iso(base.exibir_link_a_partir_de)

        self.legacy_url_field.value = base.url or ""
        self.static_link_field.value = base.static_link or ""
        self.live_teams_field.value = base.live_link_teams or ""
        self.live_youtube_field.value = base.live_link_youtube_live or ""
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
        self.live_group.visible = source == LINK_SOURCE_LIVE
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
        if source == LINK_SOURCE_LIVE:
            return bool(self.live_teams_field.value or self.live_youtube_field.value)
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
        elif source == LINK_SOURCE_LIVE:
            self.live_teams_field.value = ""
            self.live_youtube_field.value = ""
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
        live_teams = live_youtube = None
        if source == LINK_SOURCE_LESSON:
            module_id = self.module_dropdown.value or None
            lesson_id = self.lesson_dropdown.value or None
            link_type = self.link_type_dropdown.value or None
        elif source == LINK_SOURCE_STATIC:
            static_link = (self.static_link_field.value or "").strip() or None
        elif source == LINK_SOURCE_LIVE:
            live_teams = (self.live_teams_field.value or "").strip() or None
            live_youtube = (self.live_youtube_field.value or "").strip() or None
        elif source == LINK_SOURCE_LEGACY:
            url = (self.legacy_url_field.value or "").strip() or None

        prioridade_raw = (self.prioridade_field.value or "").strip()
        prioridade = int(prioridade_raw) if prioridade_raw else None

        return Notice(
            id=(self.id_field.value or "").strip(),
            titulo=(self.titulo_field.value or "").strip(),
            mensagem=(self.mensagem_field.value or "").strip(),
            tipo=self.tipo_dropdown.value or "",
            data_publicacao=self.data_publicacao_input.get_iso() or "",
            ativo=bool(self.ativo_checkbox.value),
            data_inicio=self.data_inicio_input.get_iso(),
            data_fim=self.data_fim_input.get_iso(),
            module_id=module_id,
            lesson_id=lesson_id,
            link_type=link_type,
            static_link=static_link,
            live_link_teams=live_teams,
            live_link_youtube_live=live_youtube,
            url=url,
            texto_link=(self.texto_link_field.value or "").strip() or None,
            prioridade=prioridade,
            arquivar_apos=self.arquivar_apos_input.get_iso(),
            exibir_link_a_partir_de=self.exibir_link_input.get_iso(),
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
