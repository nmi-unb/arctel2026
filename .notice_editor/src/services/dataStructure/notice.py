from __future__ import annotations

from dataclasses import dataclass, replace
from typing import Optional

from ..generic.values.constants import (
    LINK_SOURCE_LEGACY,
    LINK_SOURCE_LESSON,
    LINK_SOURCE_LIVE,
    LINK_SOURCE_NONE,
    LINK_SOURCE_STATIC,
)

_FIELD_ORDER = (
    "id",
    "titulo",
    "mensagem",
    "tipo",
    "dataPublicacao",
    "dataInicio",
    "dataFim",
    "moduleId",
    "lessonId",
    "linkType",
    "staticLink",
    "url",
    "textoLink",
    "prioridade",
    "ativo",
    "arquivarApos",
    "exibirLinkAPartirDe",
)


@dataclass
class Notice:
    id: str
    titulo: str
    mensagem: str
    tipo: str
    data_publicacao: str
    ativo: bool
    data_inicio: Optional[str] = None
    data_fim: Optional[str] = None
    module_id: Optional[str] = None
    lesson_id: Optional[str] = None
    link_type: Optional[str] = None
    static_link: Optional[str] = None
    live_link_teams: Optional[str] = None
    live_link_youtube_live: Optional[str] = None
    url: Optional[str] = None
    texto_link: Optional[str] = None
    prioridade: Optional[int] = None
    arquivar_apos: Optional[str] = None
    exibir_link_a_partir_de: Optional[str] = None

    @property
    def is_lesson_notice(self) -> bool:
        return self.data_inicio is not None and self.data_fim is not None

    @property
    def link_source(self) -> str:
        if self.url:
            return LINK_SOURCE_LEGACY
        if self.static_link:
            return LINK_SOURCE_STATIC
        if self.live_link_teams or self.live_link_youtube_live:
            return LINK_SOURCE_LIVE
        if self.module_id or self.lesson_id or self.link_type:
            return LINK_SOURCE_LESSON
        return LINK_SOURCE_NONE

    def duplicate(self, new_id: str) -> "Notice":
        return replace(self, id=new_id)

    @classmethod
    def from_dict(cls, data: dict) -> "Notice":
        live_links = data.get("liveLinks") or {}
        return cls(
            id=data["id"],
            titulo=data.get("titulo", ""),
            mensagem=data.get("mensagem", ""),
            tipo=data.get("tipo", ""),
            data_publicacao=data.get("dataPublicacao", ""),
            ativo=bool(data.get("ativo", True)),
            data_inicio=data.get("dataInicio"),
            data_fim=data.get("dataFim"),
            module_id=data.get("moduleId"),
            lesson_id=data.get("lessonId"),
            link_type=data.get("linkType"),
            static_link=data.get("staticLink"),
            live_link_teams=live_links.get("teams"),
            live_link_youtube_live=live_links.get("youtubeLive"),
            url=data.get("url"),
            texto_link=data.get("textoLink"),
            prioridade=data.get("prioridade"),
            arquivar_apos=data.get("arquivarApos"),
            exibir_link_a_partir_de=data.get("exibirLinkAPartirDe"),
        )

    def to_dict(self) -> dict:
        raw = {
            "id": self.id,
            "titulo": self.titulo,
            "mensagem": self.mensagem,
            "tipo": self.tipo,
            "dataPublicacao": self.data_publicacao,
            "dataInicio": self.data_inicio,
            "dataFim": self.data_fim,
            "moduleId": self.module_id,
            "lessonId": self.lesson_id,
            "linkType": self.link_type,
            "staticLink": self.static_link,
            "url": self.url,
            "textoLink": self.texto_link,
            "prioridade": self.prioridade,
            "ativo": self.ativo,
            "arquivarApos": self.arquivar_apos,
            "exibirLinkAPartirDe": self.exibir_link_a_partir_de,
        }
        result = {key: raw[key] for key in _FIELD_ORDER if raw[key] is not None}
        if self.live_link_teams or self.live_link_youtube_live:
            result["liveLinks"] = {
                "teams": self.live_link_teams,
                "youtubeLive": self.live_link_youtube_live,
            }
        return result


__all__ = ["Notice"]
