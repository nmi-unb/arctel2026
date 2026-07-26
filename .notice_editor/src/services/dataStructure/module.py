from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Optional

from .lesson import Lesson

_MODULE_ID_PATTERN = re.compile(r"^modulo-(\d+)$")
_LESSON_ID_PATTERN = re.compile(r"^aula-(\d+)$")
_KNOWN_MODULE_KEYS = {"modulo", "titulo", "lessons"}
_KNOWN_SUMMARY_KEYS = {"id", "number", "title", "dataFile", "active"}


def parse_module_number(module_id: str) -> int:
    match = _MODULE_ID_PATTERN.match(module_id or "")
    if not match:
        raise ValueError(f"moduleId inválido: {module_id!r}")
    return int(match.group(1))


def parse_lesson_number(lesson_id: str) -> int:
    match = _LESSON_ID_PATTERN.match(lesson_id or "")
    if not match:
        raise ValueError(f"lessonId inválido: {lesson_id!r}")
    return int(match.group(1))


def build_lesson_id(numero: int) -> str:
    return f"aula-{numero}"


def build_module_id(number: int) -> str:
    return f"modulo-{number}"


@dataclass(frozen=True)
class ModuleSummary:
    id: str
    number: int
    title: str
    data_file: str
    active: bool
    extra_fields: dict = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: dict) -> "ModuleSummary":
        return cls(
            id=data["id"],
            number=int(data["number"]),
            title=data.get("title", ""),
            data_file=data["dataFile"],
            active=bool(data.get("active", True)),
            extra_fields={key: value for key, value in data.items() if key not in _KNOWN_SUMMARY_KEYS},
        )

    def to_dict(self) -> dict:
        result = {
            "id": self.id,
            "number": self.number,
            "title": self.title,
            "dataFile": self.data_file,
            "active": self.active,
        }
        result.update(self.extra_fields)
        return result


@dataclass(frozen=True)
class Module:
    id: str
    number: int
    title: str
    lessons: tuple[Lesson, ...]
    extra_fields: dict = field(default_factory=dict)

    def lesson(self, numero: int) -> Optional[Lesson]:
        return next((item for item in self.lessons if item.numero == numero), None)

    @classmethod
    def from_dict(cls, module_id: str, data: dict) -> "Module":
        lessons = tuple(Lesson.from_dict(item) for item in data.get("lessons", []))
        return cls(
            id=module_id,
            number=int(data.get("modulo", 0)),
            title=data.get("titulo", ""),
            lessons=lessons,
            extra_fields={key: value for key, value in data.items() if key not in _KNOWN_MODULE_KEYS},
        )

    def to_dict(self) -> dict:
        result = {
            "modulo": self.number,
            "titulo": self.title,
            "lessons": [lesson.to_dict() for lesson in self.lessons],
        }
        result.update(self.extra_fields)
        return result


__all__ = [
    "Module",
    "ModuleSummary",
    "parse_module_number",
    "parse_lesson_number",
    "build_lesson_id",
    "build_module_id",
]
