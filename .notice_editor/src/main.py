# ignore file
import flet as ft
from views.main_view import build_main_view


def main(page: ft.Page) -> None:
    page.title = "Notice Editor — avisos.json (FASE 1)"
    page.padding = 0
    # Força claro: no tema escuro (auto-detectado do SO), o contraste padrão de
    # borda dos campos de formulário ficou baixo demais nesta versão do Flet.
    page.theme_mode = ft.ThemeMode.LIGHT
    build_main_view(page)


if __name__ == "__main__":
    ft.run(main)
