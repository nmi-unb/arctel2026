from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from .LessonLinks import LessonLinks


@dataclass(frozen=True)
class Lesson:
    numero: int
    titulo: str
    data_inicio: Optional[str]
    data_fim: Optional[str]
    links: LessonLinks

    def link_for(self, link_type: str) -> Optional[str]:
        return self.links.get(link_type)

    @classmethod
    def from_dict(cls, data: dict) -> "Lesson":
        return cls(
            numero=int(data["numero"]),
            titulo=data.get("titulo", ""),
            data_inicio=data.get("dataInicio"),
            data_fim=data.get("dataFim"),
            links=LessonLinks.from_dict(data.get("links") or {}),
        )


__all__ = ["Lesson"]
