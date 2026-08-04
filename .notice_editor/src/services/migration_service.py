from __future__ import annotations

from dataclasses import dataclass, replace
from typing import Optional

from . import module_repository
from .dataStructure.module import build_lesson_id
from .dataStructure.notice import Notice
from .generic.values.constants import LINK_TYPES


@dataclass(frozen=True)
class LegacyReference:
    module_id: str
    lesson_id: str
    link_type: str


@dataclass(frozen=True)
class LegacyRecord:
    notice: Notice
    suggested_reference: Optional[LegacyReference]


def find_legacy_notices(notices: list[Notice]) -> list[Notice]:
    return [notice for notice in notices if notice.url]


def suggest_lesson_reference(url: str) -> Optional[LegacyReference]:
    for summary in module_repository.list_modules():
        try:
            module = module_repository.get_module(summary.id)
        except module_repository.ModuleRepositoryError:
            continue
        for lesson in module.lessons:
            for link_type in LINK_TYPES:
                if lesson.link_for(link_type) == url:
                    return LegacyReference(
                        module_id=summary.id,
                        lesson_id=build_lesson_id(lesson.numero),
                        link_type=link_type,
                    )
    return None


def build_legacy_report(notices: list[Notice]) -> list[LegacyRecord]:
    legacy = find_legacy_notices(notices)
    return [
        LegacyRecord(notice=notice, suggested_reference=suggest_lesson_reference(notice.url))
        for notice in legacy
    ]


def migrate_to_static_link(notice: Notice, static_link: str) -> Notice:
    return replace(notice, url=None, static_link=static_link, module_id=None, lesson_id=None, link_type=None)


def migrate_to_lesson_reference(notice: Notice, module_id: str, lesson_id: str, link_type: str) -> Notice:
    module_repository.get_lesson_link(module_id, lesson_id, link_type)
    return replace(notice, url=None, static_link=None, module_id=module_id, lesson_id=lesson_id, link_type=link_type)


__all__ = [
    "LegacyReference",
    "LegacyRecord",
    "find_legacy_notices",
    "suggest_lesson_reference",
    "build_legacy_report",
    "migrate_to_static_link",
    "migrate_to_lesson_reference",
]
