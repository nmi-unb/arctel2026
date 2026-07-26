from __future__ import annotations

from dataclasses import replace
from typing import Optional

from . import module_repository, reference_service, validation_service
from .dataStructure.lesson import Lesson
from .dataStructure.LessonLinks import LessonLinks
from .dataStructure.lesson_materials import LessonMaterials
from .dataStructure.module import Module, ModuleSummary, build_lesson_id
from .dataStructure.notice import Notice
from .generic.file_fingerprint import FileFingerprint


def _next_lesson_number(module: Module) -> int:
    used = {lesson.numero for lesson in module.lessons}
    candidate = 1
    while candidate in used:
        candidate += 1
    return candidate


class ModuleStateError(Exception):
    pass


class ModuleExternalChangeError(Exception):
    pass


class ModuleSaveBlockedError(Exception):
    def __init__(self, result: validation_service.ValidationResult):
        self.result = result
        super().__init__("Módulo inválido; corrija antes de salvar")


class ModuleState:
    def __init__(self) -> None:
        self.summaries: list[ModuleSummary] = []
        self.load_error: Optional[str] = None
        self.selected_module_id: Optional[str] = None
        self.selected_lesson_numero: Optional[int] = None
        self._modules: dict[str, Module] = {}
        self._fingerprints: dict[str, FileFingerprint] = {}
        self._dirty: dict[str, bool] = {}

    # ------------------------------------------------------------- loading

    def load_index(self) -> None:
        try:
            self.summaries = module_repository.list_modules(refresh=True)
            self.load_error = None
        except module_repository.ModuleRepositoryError as exc:
            self.summaries = []
            self.load_error = str(exc)

    def load_module(self, module_id: str) -> Module:
        module = module_repository.get_module(module_id, refresh=True)
        self._modules[module_id] = module
        self._fingerprints[module_id] = module_repository.get_module_fingerprint(module_id)
        self._dirty[module_id] = False
        return module

    def reload_module(self, module_id: str) -> Module:
        return self.load_module(module_id)

    def get_module(self, module_id: str) -> Optional[Module]:
        return self._modules.get(module_id)

    # -------------------------------------------------------------- state

    def select_module(self, module_id: Optional[str]) -> None:
        self.selected_module_id = module_id
        self.selected_lesson_numero = None

    def select_lesson(self, numero: Optional[int]) -> None:
        self.selected_lesson_numero = numero

    def is_dirty(self, module_id: str) -> bool:
        return self._dirty.get(module_id, False)

    def any_dirty(self) -> bool:
        return any(self._dirty.values())

    def dirty_module_ids(self) -> list[str]:
        return [module_id for module_id, dirty in self._dirty.items() if dirty]

    def apply_module(self, module: Module) -> None:
        self._modules[module.id] = module
        self._dirty[module.id] = True

    def _require_module(self, module_id: str) -> Module:
        module = self._modules.get(module_id)
        if module is None:
            raise ModuleStateError(f"Módulo não carregado: {module_id!r}")
        return module

    def _apply_lessons(self, module_id: str, lessons: tuple[Lesson, ...]) -> None:
        module = self._require_module(module_id)
        self.apply_module(replace(module, lessons=lessons))

    # ------------------------------------------------------- module editing

    def update_title(self, module_id: str, new_title: str) -> None:
        module = self._require_module(module_id)
        self.apply_module(replace(module, title=new_title))

    # ------------------------------------------------------- lesson editing

    def create_lesson(self, module_id: str) -> Lesson:
        module = self._require_module(module_id)
        numero = _next_lesson_number(module)
        lesson = Lesson(
            numero=numero,
            titulo=f"Aula {numero}",
            data_inicio=None,
            data_fim=None,
            links=LessonLinks.from_dict({}),
            materials=LessonMaterials.from_dict({}),
        )
        self._apply_lessons(module_id, module.lessons + (lesson,))
        return lesson

    def duplicate_lesson(self, module_id: str, numero: int) -> Lesson:
        module = self._require_module(module_id)
        original = module.lesson(numero)
        if original is None:
            raise ModuleStateError(f"Aula {numero} não encontrada em {module_id!r}")
        new_numero = _next_lesson_number(module)
        clone = replace(
            original,
            numero=new_numero,
            titulo=f"{original.titulo} (cópia)",
            data_inicio=None,
            data_fim=None,
            links=LessonLinks.from_dict({}),
        )
        position = module.lessons.index(original)
        lessons = module.lessons[: position + 1] + (clone,) + module.lessons[position + 1 :]
        self._apply_lessons(module_id, lessons)
        return clone

    def update_lesson(self, module_id: str, lesson: Lesson) -> None:
        module = self._require_module(module_id)
        lessons = tuple(lesson if item.numero == lesson.numero else item for item in module.lessons)
        self._apply_lessons(module_id, lessons)

    def remove_lesson(self, module_id: str, numero: int) -> None:
        module = self._require_module(module_id)
        lessons = tuple(item for item in module.lessons if item.numero != numero)
        self._apply_lessons(module_id, lessons)
        if self.selected_lesson_numero == numero:
            self.selected_lesson_numero = None

    def move_lesson(self, module_id: str, numero: int, direction: int) -> None:
        module = self._require_module(module_id)
        lessons = list(module.lessons)
        index = next((i for i, item in enumerate(lessons) if item.numero == numero), None)
        if index is None:
            raise ModuleStateError(f"Aula {numero} não encontrada em {module_id!r}")
        target = index + direction
        if target < 0 or target >= len(lessons):
            return
        lessons[index], lessons[target] = lessons[target], lessons[index]
        self._apply_lessons(module_id, tuple(lessons))

    def sort_lessons_by_numero(self, module_id: str) -> None:
        module = self._require_module(module_id)
        lessons = tuple(sorted(module.lessons, key=lambda item: item.numero))
        self._apply_lessons(module_id, lessons)

    def sort_lessons_by_data(self, module_id: str) -> None:
        module = self._require_module(module_id)
        lessons = tuple(sorted(module.lessons, key=lambda item: item.data_inicio or ""))
        self._apply_lessons(module_id, lessons)

    def renumber_lesson(self, module_id: str, old_numero: int, new_numero: int) -> Lesson:
        module = self._require_module(module_id)
        original = module.lesson(old_numero)
        if original is None:
            raise ModuleStateError(f"Aula {old_numero} não encontrada em {module_id!r}")
        if old_numero == new_numero:
            return original
        if module.lesson(new_numero) is not None:
            raise ModuleStateError(f"Já existe aula com número {new_numero} em {module_id!r}")

        renumbered = replace(original, numero=new_numero)
        lessons = tuple(renumbered if item.numero == old_numero else item for item in module.lessons)
        self._apply_lessons(module_id, lessons)
        if self.selected_lesson_numero == old_numero:
            self.selected_lesson_numero = new_numero
        return renumbered

    # ---------------------------------------------------------- validation

    def validate_module(self, module: Module) -> validation_service.ValidationResult:
        return validation_service.validate_module(module)

    # -------------------------------------------------------------- save

    def _write(self, module_id: str) -> Module:
        module = self._modules.get(module_id)
        if module is None:
            raise ModuleStateError(f"Módulo não carregado: {module_id!r}")
        reread_module, new_fingerprint = module_repository.save_module(module)
        self._modules[module_id] = reread_module
        self._fingerprints[module_id] = new_fingerprint
        self._dirty[module_id] = False
        return reread_module

    def save_module(self, module_id: str) -> Module:
        module = self._modules.get(module_id)
        if module is None:
            raise ModuleStateError(f"Módulo não carregado: {module_id!r}")

        result = validation_service.validate_module(module)
        if not result.is_valid:
            raise ModuleSaveBlockedError(result)

        fingerprint = self._fingerprints.get(module_id)
        if fingerprint is not None and module_repository.has_module_changed_externally(module_id, fingerprint):
            raise ModuleExternalChangeError(
                f"O arquivo do módulo {module_id!r} foi alterado fora do editor desde o último carregamento."
            )

        return self._write(module_id)

    def save_module_overriding_external_change(self, module_id: str) -> Module:
        module = self._modules.get(module_id)
        if module is None:
            raise ModuleStateError(f"Módulo não carregado: {module_id!r}")
        result = validation_service.validate_module(module)
        if not result.is_valid:
            raise ModuleSaveBlockedError(result)
        return self._write(module_id)

    # -------------------------------------------------------- cross-refs

    def notices_referencing(
        self, notices: list[Notice], module_id: Optional[str] = None, lesson_numero: Optional[int] = None
    ) -> list[reference_service.NoticeReference]:
        module_id = module_id or self.selected_module_id
        if module_id is None:
            return []
        if lesson_numero is None:
            return reference_service.notices_for_module(notices, module_id)
        lesson_id = build_lesson_id(lesson_numero)
        return reference_service.notices_for_lesson(notices, module_id, lesson_id)


__all__ = [
    "ModuleState",
    "ModuleStateError",
    "ModuleExternalChangeError",
    "ModuleSaveBlockedError",
]
