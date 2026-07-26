# ignore file
import flet as ft
from views.main_view import build_main_view


def main(page: ft.Page) -> None:
    page.title = "Notice Editor — avisos.json (FASE 1)"
    page.padding = 0
    build_main_view(page)


if __name__ == "__main__":
    ft.app(main)
