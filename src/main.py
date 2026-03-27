"""Точка входа приложения."""
import sys
from pathlib import Path

import flet as ft


# Добавляем src в sys.path для корректных импортов
src_path = Path(__file__).resolve().parent
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

from config import (
    COLOR_ACCENT,
    COLOR_BG_PRIMARY,
    COLOR_DIVIDER,
    COLOR_SIDEBAR_BG,
    COLOR_TEXT_PRIMARY,
    COLOR_TEXT_SECONDARY,
    FONT_SIZE_BASE,
    PAGE_TITLE,
    SIDEBAR_WIDTH,
    THEME_MODE,
)
from database import clear_active_session, get_active_session, initialize_database
from screens.auth.hello import hello_screen
from screens.calendar.calendar import calendar_screen
from screens.main.agent import agent_screen
from screens.main.home import home_screen
from screens.notes.notes_list import notes_screen
from screens.tasks.tasks_list import tasks_screen
from utils.session import (
    clear_current_user,
    get_current_user_name,
    is_authenticated,
    set_current_user,
)


def main(page: ft.Page):
    """Основная функция приложения."""
    initialize_database()

    page.title = PAGE_TITLE
    page.theme_mode = THEME_MODE
    page.bgcolor = COLOR_BG_PRIMARY
    page.padding = 0

    protected_routes = {
        "/home": home_screen,
        "/tasks": tasks_screen,
        "/notes": notes_screen,
        "/calendar": calendar_screen,
        "/agent": agent_screen,
    }

    def restore_user_from_persistent_session() -> bool:
        if is_authenticated(page):
            return True

        active_session = get_active_session()
        if not active_session or active_session["user_id"] is None:
            clear_current_user(page)
            return False

        user_name = active_session.get("login") or active_session.get("email") or "User"
        set_current_user(page, active_session["user_id"], user_name)
        return True

    def logout_click(e):
        clear_active_session()
        clear_current_user(page)
        page.go("/")

    def navigate_to(route: str):
        page.go(route)

    def create_sidebar_item(icon, label, route):
        """Создает элемент навигации sidebar."""
        is_active = page.route == route
        color = COLOR_ACCENT if is_active else COLOR_TEXT_SECONDARY

        return ft.Container(
            content=ft.Row(
                controls=[
                    ft.Icon(icon, color=color, size=20),
                    ft.Text(label, size=FONT_SIZE_BASE, color=color),
                ],
                spacing=12,
            ),
            padding=12,
            border_radius=8,
            on_click=lambda e: navigate_to(route),
        )

    def build_authenticated_view(route: str) -> ft.View:
        """Собирает основную оболочку приложения."""
        user_name = get_current_user_name(page)
        screen_handler = protected_routes.get(route, home_screen)
        screen_view = screen_handler(page)
        if len(screen_view.controls) == 1:
            content = screen_view.controls[0]
        else:
            content = ft.Column(
                controls=screen_view.controls,
                expand=True,
                spacing=0,
            )

        sidebar = ft.Container(
            width=SIDEBAR_WIDTH,
            bgcolor=COLOR_SIDEBAR_BG,
            padding=20,
            content=ft.Column(
                controls=[
                    ft.Text(
                        f"{user_name}'s space",
                        size=FONT_SIZE_BASE,
                        weight=ft.FontWeight.BOLD,
                        color=COLOR_TEXT_PRIMARY,
                    ),
                    ft.Divider(color=COLOR_DIVIDER, height=1),
                    ft.Container(height=16),
                    create_sidebar_item(ft.Icons.HOME, "Home", "/home"),
                    create_sidebar_item(ft.Icons.TASK_ALT, "Tasks", "/tasks"),
                    create_sidebar_item(ft.Icons.NOTE, "Notes", "/notes"),
                    create_sidebar_item(ft.Icons.CALENDAR_MONTH, "Calendar", "/calendar"),
                    create_sidebar_item(ft.Icons.SMART_TOY, "AI Agent", "/agent"),
                    ft.Container(expand=True),
                    ft.TextButton("Logout", icon=ft.Icons.LOGOUT, on_click=logout_click),
                ],
                spacing=4,
                expand=True,
            ),
        )

        return ft.View(
            route=route,
            controls=[
                ft.Row(
                    controls=[sidebar, content],
                    spacing=0,
                    expand=True,
                )
            ],
        )

    def route_change(e):
        """Обработчик изменения маршрута."""
        authenticated = restore_user_from_persistent_session()
        current_route = page.route or "/"
        target_route = current_route

        if not authenticated:
            target_route = "/"
        elif current_route == "/":
            target_route = "/home"
        elif current_route not in protected_routes:
            target_route = "/home"

        if target_route != current_route:
            page.go(target_route)
            return

        page.views.clear()

        if target_route == "/":
            page.views.append(hello_screen(page))
        else:
            page.views.append(build_authenticated_view(target_route))

        page.update()

    def view_pop(e):
        if is_authenticated(page):
            page.go("/home")
        else:
            page.go("/")

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route or "/")


if __name__ == "__main__":
    ft.run(main)
