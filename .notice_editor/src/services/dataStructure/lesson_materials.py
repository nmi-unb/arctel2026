from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

_KNOWN_ITEM_KEYS = {"title", "url", "available"}


@dataclass(frozen=True)
class LessonMaterialItem:
    titulo: str
    url: Optional[str]
    disponivel: bool = True
    extra_fields: dict = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: dict) -> "LessonMaterialItem":
        return cls(
            titulo=data.get("title", ""),
            url=data.get("url"),
            disponivel=bool(data.get("available", True)),
            extra_fields={key: value for key, value in data.items() if key not in _KNOWN_ITEM_KEYS},
        )

    def to_dict(self) -> dict:
        result = {"title": self.titulo, "url": self.url}
        if not self.disponivel:
            result["available"] = False
        result.update(self.extra_fields)
        return result


@dataclass(frozen=True)
class LessonMaterials:
    professor: tuple[LessonMaterialItem, ...] = ()
    replacement_courses: tuple[LessonMaterialItem, ...] = ()

    @classmethod
    def from_dict(cls, data: dict) -> "LessonMaterials":
        return cls(
            professor=tuple(LessonMaterialItem.from_dict(item) for item in data.get("professor", [])),
            replacement_courses=tuple(
                LessonMaterialItem.from_dict(item) for item in data.get("replacementCourses", [])
            ),
        )

    def to_dict(self) -> dict:
        return {
            "professor": [item.to_dict() for item in self.professor],
            "replacementCourses": [item.to_dict() for item in self.replacement_courses],
        }


__all__ = ["LessonMaterialItem", "LessonMaterials"]
