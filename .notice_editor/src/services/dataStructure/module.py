from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Optional

from .lesson import Lesson

_MODULE_ID_PATTERN = re.compile(r"^modulo-(\d+)$")
_LESSON_ID_PATTERN = re.compile(r"^aula-(\d+)$")


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

    @classmethod
    def from_dict(cls, data: dict) -> "ModuleSummary":
        return cls(
            id=data["id"],
            number=int(data["number"]),
            title=data.get("title", ""),
            data_file=data["dataFile"],
            active=bool(data.get("active", True)),
        )


@dataclass(frozen=True)
class Module:
    id: str
    number: int
    title: str
    lessons: tuple[Lesson, ...]

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
        )


__all__ = [
    "Module",
    "ModuleSummary",
    "parse_module_number",
    "parse_lesson_number",
    "build_lesson_id",
    "build_module_id",
]
