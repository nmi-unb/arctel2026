from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from .LessonLinks import LessonLinks
from .lesson_materials import LessonMaterials

_KNOWN_LESSON_KEYS = {"numero", "titulo", "dataInicio", "dataFim", "links", "materials"}


@dataclass(frozen=True)
class Lesson:
    numero: int
    titulo: str
    data_inicio: Optional[str]
    data_fim: Optional[str]
    links: LessonLinks
    materials: LessonMaterials
    extra_fields: dict = field(default_factory=dict)

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
            materials=LessonMaterials.from_dict(data.get("materials") or {}),
            extra_fields={key: value for key, value in data.items() if key not in _KNOWN_LESSON_KEYS},
        )

    def to_dict(self) -> dict:
        result = {
            "numero": self.numero,
            "titulo": self.titulo,
            "dataInicio": self.data_inicio,
            "dataFim": self.data_fim,
            "links": self.links.to_dict(),
            "materials": self.materials.to_dict(),
        }
        result.update(self.extra_fields)
        return result


__all__ = ["Lesson"]
