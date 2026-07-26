from __future__ import annotations

from datetime import datetime
from typing import Optional

import flet as ft

from services.generic.values.constants import DATE_OFFSET_OPTIONS, DEFAULT_DATE_OFFSET


def info_row(control: ft.Control, explanation: str, required: bool = False) -> ft.Row:
    marker: list[ft.Control] = []
    if required:
        marker.append(ft.Text("*", color=ft.Colors.BLUE, weight=ft.FontWeight.BOLD, size=16))
    return ft.Row(
        [
            ft.Container(content=control, expand=True),
            *marker,
            ft.Icon(ft.Icons.INFO_OUTLINE, tooltip=explanation, size=18, color=ft.Colors.ON_SURFACE_VARIANT),
            ft.Container(width=16),
        ],
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=6,
    )


class DateTimeInput:
    """Campo composto data + hora + fuso; produz/consome uma string ISO 8601 com offset."""

    def __init__(self, label: str) -> None:
        self.date_field = ft.TextField(label=label, hint_text="dd/mm/aaaa", width=190)
        self.time_field = ft.TextField(label="hora", hint_text="hh:mm", width=90)
        self.offset_dropdown = ft.Dropdown(
            label="fuso",
            value=DEFAULT_DATE_OFFSET,
            options=[ft.DropdownOption(key=value, text=value) for value in DATE_OFFSET_OPTIONS],
            width=125,
        )
        self.control = ft.Row([self.date_field, self.time_field, self.offset_dropdown], spacing=8)

    def get_iso(self) -> Optional[str]:
        date_raw = (self.date_field.value or "").strip()
        if not date_raw:
            return None
        time_raw = (self.time_field.value or "").strip() or "00:00"
        offset = self.offset_dropdown.value or DEFAULT_DATE_OFFSET
        try:
            day_str, month_str, year_str = date_raw.split("/")
            hour_str, minute_str = time_raw.split(":")
            day, month, year = int(day_str), int(month_str), int(year_str)
            hour, minute = int(hour_str), int(minute_str)
            return f"{year:04d}-{month:02d}-{day:02d}T{hour:02d}:{minute:02d}:00{offset}"
        except ValueError:
            # Mantém o texto bruto: validation_service rejeita, o usuário vê o erro
            # em vez do formulário "engolir" silenciosamente uma data malformada.
            return f"{date_raw}T{time_raw}{offset}"

    def set_iso(self, value: Optional[str]) -> None:
        if not value:
            self.date_field.value = ""
            self.time_field.value = ""
            self.offset_dropdown.value = DEFAULT_DATE_OFFSET
            return
        try:
            parsed = datetime.fromisoformat(value)
        except ValueError:
            self.date_field.value = value
            self.time_field.value = ""
            return

        self.date_field.value = f"{parsed.day:02d}/{parsed.month:02d}/{parsed.year:04d}"
        self.time_field.value = f"{parsed.hour:02d}:{parsed.minute:02d}"

        offset_text = DEFAULT_DATE_OFFSET
        utc_offset = parsed.utcoffset()
        if utc_offset is not None:
            total_minutes = int(utc_offset.total_seconds() // 60)
            sign = "+" if total_minutes >= 0 else "-"
            total_minutes = abs(total_minutes)
            offset_text = f"{sign}{total_minutes // 60:02d}:{total_minutes % 60:02d}"
        if offset_text not in DATE_OFFSET_OPTIONS:
            self.offset_dropdown.options.append(ft.DropdownOption(key=offset_text, text=offset_text))
        self.offset_dropdown.value = offset_text


__all__ = ["info_row", "DateTimeInput"]
