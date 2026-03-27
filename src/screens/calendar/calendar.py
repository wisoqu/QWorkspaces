"""Экран календаря."""
import flet as ft

def calendar_screen(page: ft.Page) -> ft.View:
    """Экран календаря (заглушка)."""
    content = ft.Container(
        expand=True,
        padding=40,
        content=ft.Column(
            controls=[
                ft.Text("Calendar", size=24, weight=ft.FontWeight.BOLD),
                ft.Container(height=24),
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Icon(ft.Icons.CALENDAR_MONTH, size=64),
                            ft.Text("Calendar coming soon...", size=16),
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=16,
                    ),
                    alignment=ft.Alignment.CENTER,
                    expand=True,
                ),
            ],
            spacing=16,
        ),
    )

    return ft.View(route="/calendar", controls=[content])
