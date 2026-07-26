from __future__ import annotations

import flet as ft

from services.dataStructure.lesson import Lesson


class LessonPreviewView:
    def __init__(self) -> None:
        self._title = ft.Text("", size=16, weight=ft.FontWeight.BOLD)
        self._dates = ft.Text("", size=12, color=ft.Colors.ON_SURFACE_VARIANT)
        self._links = ft.Column([], spacing=2)
        self._materials = ft.Column([], spacing=2)
        self._references = ft.Column([], spacing=2)
        self._empty_state = ft.Text("Nenhuma aula selecionada.", color=ft.Colors.ON_SURFACE_VARIANT)
        self._body = ft.Column([self._title, self._dates, self._links, self._materials, self._references], spacing=6, visible=False)

        self.container = ft.Container(
            content=ft.Column([ft.Text("Resumo da aula", weight=ft.FontWeight.BOLD), self._empty_state, self._body]),
            padding=16,
            border=ft.Border.all(width=1, color=ft.Colors.OUTLINE),
            border_radius=8,
        )

    def clear(self) -> None:
        self._empty_state.visible = True
        self._body.visible = False

    def render(self, lesson: Lesson, reference_count: int) -> None:
        self._empty_state.visible = False
        self._body.visible = True

        self._title.value = f"Aula {lesson.numero} — {lesson.titulo or '(sem título)'}"
        if lesson.data_inicio and lesson.data_fim:
            self._dates.value = f"{lesson.data_inicio}  →  {lesson.data_fim}"
        else:
            self._dates.value = "Sem data definida"

        link_rows = []
        for link_type, value in (("teams", lesson.links.teams), ("youtubeLive", lesson.links.youtube_live), ("youtubeRecorded", lesson.links.youtube_recorded)):
            status = value if value else "não definido"
            color = ft.Colors.GREEN_700 if value else ft.Colors.GREY_600
            link_rows.append(ft.Text(f"{link_type}: {status}", size=12, color=color))
        self._links.controls = link_rows

        total_materials = len(lesson.materials.professor) + len(lesson.materials.replacement_courses)
        self._materials.controls = [ft.Text(f"Materiais: {total_materials} item(ns)", size=12)]

        self._references.controls = [
            ft.Text(
                f"{reference_count} aviso(s) referenciam esta aula" if reference_count else "Nenhum aviso referencia esta aula",
                size=12,
                color=ft.Colors.AMBER_700 if reference_count else ft.Colors.ON_SURFACE_VARIANT,
            )
        ]


__all__ = ["LessonPreviewView"]
