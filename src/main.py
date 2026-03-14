import flet as ft

from screens.hello import hello_screen
from screens.home import home_screen


def main(page: ft.Page):
    # Global page configuration.
    page.title = "QWorkspaces"
    page.padding = 24
    page.theme_mode = ft.ThemeMode.LIGHT

    def route_change(e=None):
        # Rebuild the visible screens when the route changes.
        page.views.clear()
        page.views.append(hello_screen(page))

        if page.route == "/home":
            page.views.append(home_screen(page))

        page.update()

    page.on_route_change = route_change
    route_change()


ft.run(main)
