from __future__ import annotations

from typing import Optional

from services import migration_service, notice_repository, validation_service
from services.dataStructure.notice import Notice
from services.notice_repository import FileFingerprint


class ExternalChangeError(Exception):
    pass


class SaveBlockedError(Exception):
    def __init__(self, results: dict[str, validation_service.ValidationResult]):
        self.results = results
        super().__init__("Existem avisos inválidos; corrija antes de salvar")


class AppState:
    def __init__(self) -> None:
        self.notices: list[Notice] = []
        self.fingerprint: Optional[FileFingerprint] = None
        self.dirty: bool = False
        self.load_error: Optional[str] = None

    def load(self) -> None:
        self.notices, self.fingerprint = notice_repository.load_notices()
        self.dirty = False
        self.load_error = None

    def validate_all(self) -> dict[str, validation_service.ValidationResult]:
        return validation_service.validate_all(self.notices)

    def validate_one(self, notice: Notice) -> validation_service.ValidationResult:
        return validation_service.validate_notice(notice, all_notices=self.notices)

    def validate_candidate(self, notice: Notice, index: Optional[int]) -> validation_service.ValidationResult:
        working = list(self.notices)
        if index is None:
            working.append(notice)
        else:
            working[index] = notice
        return validation_service.validate_notice(notice, all_notices=working)

    def _mark_dirty(self) -> None:
        self.dirty = True

    def apply_notice(self, notice: Notice, index: Optional[int]) -> None:
        if index is None:
            self.notices.append(notice)
        else:
            self.notices[index] = notice
        self._mark_dirty()

    def duplicate_notice(self, index: int, new_id: str) -> Notice:
        clone = self.notices[index].duplicate(new_id)
        self.notices.insert(index + 1, clone)
        self._mark_dirty()
        return clone

    def set_active(self, index: int, active: bool) -> None:
        self.notices[index].ativo = active
        self._mark_dirty()

    def update_notice_lesson_id(self, index: int, lesson_id: str) -> None:
        self.notices[index].lesson_id = lesson_id
        self._mark_dirty()

    def delete_notice(self, index: int) -> None:
        del self.notices[index]
        self._mark_dirty()

    def move_up(self, index: int) -> None:
        if index <= 0:
            return
        self.notices[index - 1], self.notices[index] = self.notices[index], self.notices[index - 1]
        self._mark_dirty()

    def move_down(self, index: int) -> None:
        if index >= len(self.notices) - 1:
            return
        self.notices[index + 1], self.notices[index] = self.notices[index], self.notices[index + 1]
        self._mark_dirty()

    def sort_by_publicacao(self) -> None:
        self.notices.sort(key=lambda notice: notice.data_publicacao or "")
        self._mark_dirty()

    def sort_by_prioridade(self) -> None:
        self.notices.sort(key=lambda notice: -(notice.prioridade or 0))
        self._mark_dirty()

    def migrate_to_static_link(self, index: int, static_link: str) -> None:
        self.notices[index] = migration_service.migrate_to_static_link(self.notices[index], static_link)
        self._mark_dirty()

    def migrate_to_lesson_reference(self, index: int, module_id: str, lesson_id: str, link_type: str) -> None:
        self.notices[index] = migration_service.migrate_to_lesson_reference(
            self.notices[index], module_id, lesson_id, link_type
        )
        self._mark_dirty()

    def legacy_report(self) -> list[migration_service.LegacyRecord]:
        return migration_service.build_legacy_report(self.notices)

    def save(self) -> None:
        results = self.validate_all()
        if validation_service.has_blocking_errors(results):
            raise SaveBlockedError(results)
        if self.fingerprint is not None and notice_repository.has_changed_externally(self.fingerprint):
            raise ExternalChangeError(
                "assets/data/avisos.json foi alterado fora do editor desde o último carregamento."
            )
        self.fingerprint = notice_repository.save_notices(self.notices)
        self.dirty = False

    def save_overriding_external_change(self) -> None:
        results = self.validate_all()
        if validation_service.has_blocking_errors(results):
            raise SaveBlockedError(results)
        self.fingerprint = notice_repository.save_notices(self.notices)
        self.dirty = False


__all__ = ["AppState", "ExternalChangeError", "SaveBlockedError"]
