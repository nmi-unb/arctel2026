from __future__ import annotations

from typing import Callable

import flet as ft

SAVE_CONFIRMATION_MESSAGE = (
    "Esta ação sobrescreverá assets/data/avisos.json.\n\n"
    "Antes de continuar, recomenda-se criar um commit com o estado atual do "
    "repositório, para que seja possível restaurá-lo posteriormente.\n\n"
    "Deseja realmente salvar as alterações?"
)


def _close(page: ft.Page) -> None:
    page.pop_dialog()


def show_confirmation(
    page: ft.Page,
    *,
    title: str,
    message: str,
    on_confirm: Callable[[], None],
    confirm_label: str = "Confirmar",
    cancel_label: str = "Cancelar",
    danger: bool = False,
    on_cancel: Callable[[], None] | None = None,
) -> None:
    def _on_confirm(e: ft.Event) -> None:
        _close(page)
        on_confirm()

    def _on_cancel(e: ft.Event) -> None:
        _close(page)
        if on_cancel is not None:
            on_cancel()

    dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text(title),
        content=ft.Text(message),
        actions=[
            ft.TextButton(cancel_label, on_click=_on_cancel),
            ft.FilledButton(
                confirm_label,
                on_click=_on_confirm,
                style=ft.ButtonStyle(bgcolor=ft.Colors.RED_700 if danger else None),
            ),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )
    page.show_dialog(dialog)


def show_message(page: ft.Page, *, title: str, message: str) -> None:
    def _on_close(e: ft.Event) -> None:
        _close(page)

    dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text(title),
        content=ft.Text(message),
        actions=[ft.TextButton("Fechar", on_click=_on_close)],
        actions_alignment=ft.MainAxisAlignment.END,
    )
    page.show_dialog(dialog)


def confirm_save(page: ft.Page, on_confirm: Callable[[], None]) -> None:
    show_confirmation(
        page,
        title="Salvar alterações",
        message=SAVE_CONFIRMATION_MESSAGE,
        on_confirm=on_confirm,
        confirm_label="Salvar mesmo assim",
        cancel_label="Cancelar",
    )


def confirm_delete(page: ft.Page, *, notice_id: str, on_confirm: Callable[[], None]) -> None:
    show_confirmation(
        page,
        title="Excluir aviso definitivamente",
        message=(
            f"O aviso \"{notice_id}\" será removido do arquivo em memória.\n"
            "A remoção só é gravada em assets/data/avisos.json após \"Salvar arquivo\".\n"
            "Recomenda-se criar um commit antes de salvar."
        ),
        on_confirm=on_confirm,
        confirm_label="Excluir",
        cancel_label="Cancelar",
        danger=True,
    )


def confirm_reload(page: ft.Page, on_confirm: Callable[[], None]) -> None:
    show_confirmation(
        page,
        title="Recarregar arquivo",
        message=(
            "Há alterações não salvas. Recarregar assets/data/avisos.json descartará "
            "essas alterações em memória. Deseja continuar?"
        ),
        on_confirm=on_confirm,
        confirm_label="Recarregar mesmo assim",
        cancel_label="Cancelar",
        danger=True,
    )


def confirm_discard_edit(page: ft.Page, on_confirm: Callable[[], None]) -> None:
    show_confirmation(
        page,
        title="Descartar edição",
        message="O formulário tem alterações não aplicadas. Deseja descartá-las?",
        on_confirm=on_confirm,
        confirm_label="Descartar",
        cancel_label="Continuar editando",
        danger=True,
    )


def confirm_id_change(page: ft.Page, on_confirm: Callable[[], None]) -> None:
    show_confirmation(
        page,
        title="Alterar id já salvo",
        message=(
            "Este aviso já possui um id salvo. Alterá-lo pode quebrar referências externas. "
            "Deseja realmente alterar o id?"
        ),
        on_confirm=on_confirm,
        confirm_label="Alterar id",
        cancel_label="Cancelar",
        danger=True,
    )


def confirm_sort(page: ft.Page, *, label: str, on_confirm: Callable[[], None]) -> None:
    show_confirmation(
        page,
        title="Ordenar avisos",
        message=(
            f"{label} substituirá a ordem física atual do array em memória. "
            "A ordem só é gravada após \"Salvar arquivo\". Deseja continuar?"
        ),
        on_confirm=on_confirm,
        confirm_label="Ordenar",
        cancel_label="Cancelar",
    )


def confirm_external_change(
    page: ft.Page,
    *,
    on_reload: Callable[[], None],
    on_overwrite: Callable[[], None],
) -> None:
    def _on_reload(e: ft.Event) -> None:
        _close(page)
        on_reload()

    def _on_overwrite(e: ft.Event) -> None:
        _close(page)
        on_overwrite()

    def _on_cancel(e: ft.Event) -> None:
        _close(page)

    dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("Arquivo alterado externamente"),
        content=ft.Text(
            "assets/data/avisos.json foi alterado fora deste editor desde o último "
            "carregamento. Salvar agora poderá substituir essas alterações externas."
        ),
        actions=[
            ft.TextButton("Cancelar", on_click=_on_cancel),
            ft.TextButton("Recarregar e perder edições locais", on_click=_on_reload),
            ft.FilledButton(
                "Salvar mesmo assim",
                on_click=_on_overwrite,
                style=ft.ButtonStyle(bgcolor=ft.Colors.RED_700),
            ),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )
    page.show_dialog(dialog)


__all__ = [
    "show_confirmation",
    "show_message",
    "confirm_save",
    "confirm_delete",
    "confirm_reload",
    "confirm_discard_edit",
    "confirm_id_change",
    "confirm_sort",
    "confirm_external_change",
]
