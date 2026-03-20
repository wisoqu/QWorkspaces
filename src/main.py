import flet as ft

from screens.hello import hello_screen
from screens.home import home_screen


def main(page: ft.Page):
    page.title = "QWorkspaces"
    page.padding = 24
    page.theme_mode = ft.ThemeMode.DARK

    def route_change(e=None):
        page.views.clear()
        page.views.append(hello_screen(page))

        if page.route == "/home": 
            page.views.append(home_screen(page))

        page.update()

    page.on_route_change = route_change
    route_change()


ft.run(main)
