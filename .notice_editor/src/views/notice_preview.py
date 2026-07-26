from __future__ import annotations

from typing import Optional

import flet as ft

from services import module_repository
from services.dataStructure.notice import Notice
from services.generic.values.constants import DEFAULT_TEXTO_LINK

TITULO_WARN_LENGTH = 70
MENSAGEM_WARN_LENGTH = 220

_BADGE_COLORS = {
    "confirmacao": ft.Colors.BLUE,
    "ao_vivo": ft.Colors.RED_700,
    "alteracao": ft.Colors.AMBER_700,
    "alerta": ft.Colors.ORANGE,
    "material": ft.Colors.GREEN_700,
    "encerrado": ft.Colors.GREY_600,
}


def resolve_notice_link_preview(notice: Notice) -> tuple[Optional[str], str]:
    if notice.url:
        return notice.url, "URL legada (migração pendente)"
    if notice.static_link:
        return notice.static_link, "link estático"
    if notice.module_id and notice.lesson_id and notice.link_type:
        try:
            link = module_repository.get_lesson_link(notice.module_id, notice.lesson_id, notice.link_type)
        except module_repository.ModuleRepositoryError as exc:
            return None, f"referência inválida: {exc}"
        if link is None:
            return None, "referência válida, mas o link ainda não foi definido no módulo"
        return link, "referência de aula"
    return None, "sem fonte de link (aviso informativo)"


class NoticePreviewView:
    def __init__(self) -> None:
        self._badge = ft.Container(
            content=ft.Text("", color=ft.Colors.WHITE, size=12, weight=ft.FontWeight.BOLD),
            padding=ft.Padding.symmetric(horizontal=10, vertical=4),
            border_radius=999,
            visible=False,
        )
        self._title = ft.Text("", size=16, weight=ft.FontWeight.BOLD)
        self._message = ft.Text("", size=13)
        self._dates = ft.Text("", size=12, color=ft.Colors.ON_SURFACE_VARIANT)
        self._link_row = ft.Row([], spacing=6)
        self._warnings = ft.Column([], spacing=2)
        self._empty_state = ft.Text(
            "Nenhum aviso selecionado para pré-visualização.", color=ft.Colors.ON_SURFACE_VARIANT
        )
        self._body = ft.Column(
            [self._badge, self._title, self._message, self._dates, self._link_row, self._warnings],
            spacing=6,
            visible=False,
        )

        self.container = ft.Container(
            content=ft.Column([ft.Text("Pré-visualização", weight=ft.FontWeight.BOLD), self._empty_state, self._body]),
            padding=16,
            border=ft.Border.all(width=1, color=ft.Colors.OUTLINE),
            border_radius=8,
        )

    def clear(self) -> None:
        self._empty_state.visible = True
        self._body.visible = False

    def render(self, notice: Notice) -> None:
        self._empty_state.visible = False
        self._body.visible = True

        self._badge.visible = True
        self._badge.bgcolor = _BADGE_COLORS.get(notice.tipo, ft.Colors.GREY_600)
        self._badge.content.value = notice.tipo or "sem tipo"

        self._title.value = notice.titulo or "(sem título)"
        self._message.value = notice.mensagem or "(sem mensagem)"

        if notice.data_inicio and notice.data_fim:
            self._dates.value = f"{notice.data_inicio}  →  {notice.data_fim}"
        else:
            self._dates.value = f"Publicado em {notice.data_publicacao}" if notice.data_publicacao else ""

        link, status = resolve_notice_link_preview(notice)
        self._link_row.controls = []
        if link:
            texto = notice.texto_link or DEFAULT_TEXTO_LINK
            self._link_row.controls.append(
                ft.ElevatedButton(texto, icon=ft.Icons.LINK, disabled=True)
            )
            self._link_row.controls.append(ft.Text(f"({status})", size=11, color=ft.Colors.ON_SURFACE_VARIANT))
        else:
            self._link_row.controls.append(
                ft.Row(
                    [ft.Icon(ft.Icons.LINK_OFF, size=16, color=ft.Colors.GREY_600), ft.Text(f"Botão oculto — {status}", size=12, color=ft.Colors.GREY_600)]
                )
            )

        warnings: list[str] = []
        if len(notice.titulo) > TITULO_WARN_LENGTH:
            warnings.append("Título longo — pode quebrar o layout do card.")
        if len(notice.mensagem) > MENSAGEM_WARN_LENGTH:
            warnings.append("Mensagem extensa — considere resumir.")
        if link and not notice.texto_link:
            warnings.append(f"Sem textoLink definido — usará o padrão \"{DEFAULT_TEXTO_LINK}\".")
        if notice.data_inicio and notice.data_fim and notice.data_fim <= notice.data_inicio:
            warnings.append("dataFim não é posterior a dataInicio.")
        if not notice.ativo:
            warnings.append("Aviso inativo — não aparece no site (vai para o histórico).")

        self._warnings.controls = [
            ft.Row([ft.Icon(ft.Icons.WARNING_AMBER, size=14, color=ft.Colors.AMBER_700), ft.Text(text, size=12)])
            for text in warnings
        ]


__all__ = ["NoticePreviewView", "resolve_notice_link_preview"]
