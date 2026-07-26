from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from . import module_repository
from .dataStructure.lesson import Lesson
from .dataStructure.lesson_materials import LessonMaterials
from .dataStructure.module import Module, parse_module_number
from .dataStructure.LessonLinks import LessonLinks
from .dataStructure.notice import Notice
from .generic.values.constants import LINK_TYPES, NOTICE_TYPES


@dataclass(frozen=True)
class ValidationIssue:
    field: str
    message: str


@dataclass
class ValidationResult:
    errors: list[ValidationIssue] = field(default_factory=list)
    warnings: list[ValidationIssue] = field(default_factory=list)

    @property
    def is_valid(self) -> bool:
        return not self.errors


def _parse_iso(value: Optional[str]) -> Optional[datetime]:
    if not value:
        return None
    try:
        return datetime.fromisoformat(value)
    except ValueError:
        return None


def validate_notice(notice: Notice, *, all_notices: Optional[list[Notice]] = None) -> ValidationResult:
    errors: list[ValidationIssue] = []
    warnings: list[ValidationIssue] = []

    if not notice.id:
        errors.append(ValidationIssue("id", "id é obrigatório"))
    if not notice.titulo:
        errors.append(ValidationIssue("titulo", "titulo é obrigatório"))
    if not notice.mensagem:
        errors.append(ValidationIssue("mensagem", "mensagem é obrigatório"))
    if notice.tipo not in NOTICE_TYPES:
        errors.append(ValidationIssue("tipo", f"tipo inválido: {notice.tipo!r}"))
    if not notice.data_publicacao or _parse_iso(notice.data_publicacao) is None:
        errors.append(ValidationIssue("dataPublicacao", "dataPublicacao ausente ou inválida"))

    has_inicio = notice.data_inicio is not None
    has_fim = notice.data_fim is not None
    inicio_dt = _parse_iso(notice.data_inicio)
    fim_dt = _parse_iso(notice.data_fim)
    if has_inicio != has_fim:
        errors.append(
            ValidationIssue(
                "dataInicio/dataFim", "dataInicio e dataFim devem estar ambas preenchidas ou ambas ausentes"
            )
        )
    elif has_inicio and has_fim:
        if inicio_dt is None or fim_dt is None:
            errors.append(ValidationIssue("dataInicio/dataFim", "data inválida"))
        elif fim_dt <= inicio_dt:
            errors.append(ValidationIssue("dataFim", "dataFim deve ser posterior a dataInicio"))

    for name, value in (
        ("arquivarApos", notice.arquivar_apos),
        ("exibirLinkAPartirDe", notice.exibir_link_a_partir_de),
    ):
        if value is not None and _parse_iso(value) is None:
            errors.append(ValidationIssue(name, f"{name} inválida"))

    sources_present = sum(
        1
        for present in (
            bool(notice.module_id or notice.lesson_id or notice.link_type),
            bool(notice.static_link),
            bool(notice.live_link_teams or notice.live_link_youtube_live),
            bool(notice.url),
        )
        if present
    )
    if sources_present > 1:
        errors.append(
            ValidationIssue(
                "linkSource",
                "apenas uma fonte de link é permitida: referência de aula, staticLink, liveLinks ou url",
            )
        )

    if notice.module_id or notice.lesson_id or notice.link_type:
        missing = [
            name
            for name, value in (
                ("moduleId", notice.module_id),
                ("lessonId", notice.lesson_id),
                ("linkType", notice.link_type),
            )
            if not value
        ]
        if missing:
            errors.append(
                ValidationIssue(
                    "lessonReference", f"campos ausentes para referência de aula: {', '.join(missing)}"
                )
            )
        elif notice.link_type not in LINK_TYPES:
            errors.append(ValidationIssue("linkType", f"linkType inválido: {notice.link_type!r}"))
        else:
            try:
                link_value = module_repository.get_lesson_link(
                    notice.module_id, notice.lesson_id, notice.link_type
                )
            except module_repository.ModuleRepositoryError as exc:
                errors.append(ValidationIssue("moduleId/lessonId", str(exc)))
            else:
                if link_value is None:
                    warnings.append(
                        ValidationIssue(
                            "link", "link ainda não definido — aviso será exibido sem botão"
                        )
                    )

    if all_notices is not None and notice.id:
        duplicates = [item for item in all_notices if item is not notice and item.id == notice.id]
        if duplicates:
            errors.append(ValidationIssue("id", f"id duplicado: {notice.id}"))

    if notice.arquivar_apos and fim_dt is not None:
        arquivar_dt = _parse_iso(notice.arquivar_apos)
        if arquivar_dt is not None and arquivar_dt < fim_dt:
            warnings.append(ValidationIssue("arquivarApos", "arquivarApos é anterior ao término da aula"))

    if notice.exibir_link_a_partir_de and fim_dt is not None:
        exibir_dt = _parse_iso(notice.exibir_link_a_partir_de)
        if exibir_dt is not None and exibir_dt > fim_dt:
            warnings.append(
                ValidationIssue("exibirLinkAPartirDe", "exibirLinkAPartirDe é posterior ao término da aula")
            )

    if notice.data_publicacao and notice.arquivar_apos:
        publicacao_dt = _parse_iso(notice.data_publicacao)
        arquivar_dt = _parse_iso(notice.arquivar_apos)
        if publicacao_dt is not None and arquivar_dt is not None and publicacao_dt > arquivar_dt:
            warnings.append(
                ValidationIssue("dataPublicacao", "dataPublicacao é posterior ao arquivamento")
            )

    return ValidationResult(errors=errors, warnings=warnings)


def validate_all(notices: list[Notice]) -> dict[str, ValidationResult]:
    return {notice.id: validate_notice(notice, all_notices=notices) for notice in notices}


def has_blocking_errors(results: dict[str, ValidationResult]) -> bool:
    return any(not result.is_valid for result in results.values())


def validate_lesson_links(links: LessonLinks) -> ValidationResult:
    errors: list[ValidationIssue] = []
    for link_type in LINK_TYPES:
        value = links.get(link_type)
        if value is None:
            continue
        if not isinstance(value, str):
            errors.append(ValidationIssue(f"links.{link_type}", "valor deve ser uma URL (string) ou null"))
        elif value == "":
            errors.append(ValidationIssue(f"links.{link_type}", "string vazia não é permitida; use null"))
    return ValidationResult(errors=errors)


def validate_lesson_materials(materials: LessonMaterials) -> ValidationResult:
    errors: list[ValidationIssue] = []
    groups = (("materials.professor", materials.professor), ("materials.replacementCourses", materials.replacement_courses))
    for field_name, items in groups:
        for position, item in enumerate(items):
            if not item.titulo:
                errors.append(ValidationIssue(field_name, f"item {position}: title é obrigatório"))
            if item.url is not None and not isinstance(item.url, str):
                errors.append(ValidationIssue(field_name, f"item {position}: url deve ser string ou null"))
    return ValidationResult(errors=errors)


def validate_lesson(lesson: Lesson) -> ValidationResult:
    errors: list[ValidationIssue] = []
    warnings: list[ValidationIssue] = []

    if not lesson.titulo:
        errors.append(ValidationIssue("titulo", "titulo da aula é obrigatório"))

    has_inicio = lesson.data_inicio is not None
    has_fim = lesson.data_fim is not None
    inicio_dt = _parse_iso(lesson.data_inicio)
    fim_dt = _parse_iso(lesson.data_fim)
    if has_inicio != has_fim:
        errors.append(ValidationIssue("dataInicio/dataFim", "dataInicio e dataFim devem estar ambas preenchidas ou ambas ausentes"))
    elif has_inicio and has_fim:
        if inicio_dt is None or fim_dt is None:
            errors.append(ValidationIssue("dataInicio/dataFim", "data inválida"))
        elif fim_dt <= inicio_dt:
            errors.append(ValidationIssue("dataFim", "dataFim deve ser posterior a dataInicio"))

    links_result = validate_lesson_links(lesson.links)
    errors.extend(links_result.errors)
    warnings.extend(links_result.warnings)

    materials_result = validate_lesson_materials(lesson.materials)
    errors.extend(materials_result.errors)
    warnings.extend(materials_result.warnings)

    return ValidationResult(errors=errors, warnings=warnings)


def validate_module(module: Module) -> ValidationResult:
    errors: list[ValidationIssue] = []
    warnings: list[ValidationIssue] = []

    try:
        expected_number = parse_module_number(module.id)
    except ValueError as exc:
        errors.append(ValidationIssue("id", str(exc)))
        expected_number = None
    if expected_number is not None and module.number != expected_number:
        errors.append(
            ValidationIssue("modulo", f"número do módulo ({module.number}) não corresponde ao id ({module.id!r})")
        )

    if not module.title:
        errors.append(ValidationIssue("titulo", "titulo é obrigatório"))

    seen_numeros: set[int] = set()
    for lesson in module.lessons:
        lesson_result = validate_lesson(lesson)
        errors.extend(
            ValidationIssue(f"aula {lesson.numero}: {issue.field}", issue.message) for issue in lesson_result.errors
        )
        warnings.extend(
            ValidationIssue(f"aula {lesson.numero}: {issue.field}", issue.message) for issue in lesson_result.warnings
        )
        if lesson.numero in seen_numeros:
            errors.append(ValidationIssue("lessons", f"número de aula duplicado: {lesson.numero}"))
        seen_numeros.add(lesson.numero)

    return ValidationResult(errors=errors, warnings=warnings)


__all__ = [
    "ValidationIssue",
    "ValidationResult",
    "validate_notice",
    "validate_all",
    "has_blocking_errors",
    "validate_lesson_links",
    "validate_lesson_materials",
    "validate_lesson",
    "validate_module",
]
