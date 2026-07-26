from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from . import module_repository
from .dataStructure.module import build_lesson_id, parse_lesson_number
from .dataStructure.notice import Notice
from .generic.values.constants import LINK_TYPES


@dataclass(frozen=True)
class NoticeReference:
    id: str
    titulo: str
    ativo: bool
    link_type: Optional[str]


def _to_reference(notice: Notice) -> NoticeReference:
    return NoticeReference(id=notice.id, titulo=notice.titulo, ativo=notice.ativo, link_type=notice.link_type)


def notices_for_module(notices: list[Notice], module_id: str) -> list[NoticeReference]:
    return [_to_reference(notice) for notice in notices if notice.module_id == module_id]


def notices_for_lesson(notices: list[Notice], module_id: str, lesson_id: str) -> list[NoticeReference]:
    return [
        _to_reference(notice)
        for notice in notices
        if notice.module_id == module_id and notice.lesson_id == lesson_id
    ]


@dataclass(frozen=True)
class LessonImpact:
    module_id: str
    lesson_id: str
    affected: tuple[NoticeReference, ...]

    @property
    def has_affected(self) -> bool:
        return len(self.affected) > 0


def analyze_lesson_removal(notices: list[Notice], module_id: str, numero: int) -> LessonImpact:
    lesson_id = build_lesson_id(numero)
    affected = tuple(notices_for_lesson(notices, module_id, lesson_id))
    return LessonImpact(module_id=module_id, lesson_id=lesson_id, affected=affected)


@dataclass(frozen=True)
class LessonRenumberImpact:
    module_id: str
    old_lesson_id: str
    new_lesson_id: str
    affected: tuple[NoticeReference, ...]

    @property
    def has_affected(self) -> bool:
        return len(self.affected) > 0


def analyze_lesson_renumber(
    notices: list[Notice], module_id: str, old_numero: int, new_numero: int
) -> LessonRenumberImpact:
    old_lesson_id = build_lesson_id(old_numero)
    new_lesson_id = build_lesson_id(new_numero)
    affected = tuple(notices_for_lesson(notices, module_id, old_lesson_id))
    return LessonRenumberImpact(
        module_id=module_id, old_lesson_id=old_lesson_id, new_lesson_id=new_lesson_id, affected=affected
    )


@dataclass(frozen=True)
class BrokenNoticeReference:
    notice: NoticeReference
    module_id: Optional[str]
    lesson_id: Optional[str]
    reason: str


def find_broken_notice_references(notices: list[Notice]) -> list[BrokenNoticeReference]:
    broken: list[BrokenNoticeReference] = []
    for notice in notices:
        if not (notice.module_id or notice.lesson_id or notice.link_type):
            continue
        reference = _to_reference(notice)

        if not notice.module_id:
            broken.append(BrokenNoticeReference(reference, notice.module_id, notice.lesson_id, "moduleId ausente"))
            continue
        if not notice.lesson_id:
            broken.append(BrokenNoticeReference(reference, notice.module_id, notice.lesson_id, "lessonId ausente"))
            continue
        if notice.link_type not in LINK_TYPES:
            broken.append(
                BrokenNoticeReference(
                    reference, notice.module_id, notice.lesson_id, f"linkType inválido: {notice.link_type!r}"
                )
            )
            continue

        try:
            module = module_repository.get_module(notice.module_id)
        except module_repository.ModuleRepositoryError:
            broken.append(BrokenNoticeReference(reference, notice.module_id, notice.lesson_id, "módulo inexistente"))
            continue

        try:
            numero = parse_lesson_number(notice.lesson_id)
        except ValueError:
            broken.append(BrokenNoticeReference(reference, notice.module_id, notice.lesson_id, "lessonId inválido"))
            continue

        lesson = module.lesson(numero)
        if lesson is None:
            broken.append(BrokenNoticeReference(reference, notice.module_id, notice.lesson_id, "aula inexistente"))
            continue

        if lesson.link_for(notice.link_type) is None:
            broken.append(
                BrokenNoticeReference(
                    reference, notice.module_id, notice.lesson_id, "link ainda não definido para este linkType"
                )
            )

    return broken


__all__ = [
    "NoticeReference",
    "LessonImpact",
    "LessonRenumberImpact",
    "BrokenNoticeReference",
    "notices_for_module",
    "notices_for_lesson",
    "analyze_lesson_removal",
    "analyze_lesson_renumber",
    "find_broken_notice_references",
]
