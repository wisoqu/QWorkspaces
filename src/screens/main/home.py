"""Главная страница с чатом ИИ и сводкой дел."""
import flet as ft

from _imports import *  # noqa: F401,F403
from database import get_notes, get_tasks
from utils.session import get_current_user_id, get_current_user_name


def home_screen(page: ft.Page) -> ft.View:
    """Главная страница."""
    user_name = get_current_user_name(page)
    user_id = get_current_user_id(page)
    recent_tasks = get_tasks(user_id)[:3] if user_id is not None else []
    recent_notes = get_notes(user_id)[:3] if user_id is not None else []

    def send_message(e):
        text = message_input.value.strip()
        if not text:
            return
        chat_column.controls.append(
            ft.Container(
                content=ft.Text(text, size=14),
                bgcolor="#7C5CFF",
                border_radius=16,
                padding=12,
            )
        )
        message_input.value = ""
        page.update()

    # AI чат
    chat_column = ft.Column(spacing=12, height=250, scroll=ft.ScrollMode.AUTO)
    message_input = ft.TextField(
        hint_text="Ask AI assistant...",
        expand=True,
        border_radius=12,
        filled=True,
        multiline=True,
        min_lines=1,
        max_lines=3,
    )
    send_button = ft.Container(
        content=ft.Icon(ft.Icons.SEND, size=18),
        bgcolor="#7C5CFF",
        border_radius=16,
        width=40,
        height=40,
        alignment=ft.Alignment.CENTER,
        on_click=send_message,
    )

    # Карточки
    def create_card(title, items, icon):
        content_items = items or [{"title": "Nothing here yet"}]
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Row([ft.Icon(icon, size=20), ft.Text(title, size=16, weight=ft.FontWeight.BOLD)], spacing=8),
                    ft.Divider(),
                    *(ft.Text(item.get("title", str(item)), size=14) for item in content_items),
                ],
                spacing=8,
            ),
            padding=16,
            border_radius=16,
        )

    tasks_card = create_card("Tasks", recent_tasks, ft.Icons.TASK_ALT)
    notes_card = create_card("Notes", recent_notes, ft.Icons.NOTE)

    content = ft.Container(
        expand=True,
        padding=40,
        content=ft.Column(
            controls=[
                ft.Text(f"Good day, {user_name}!", size=24, weight=ft.FontWeight.BOLD),
                ft.Text("Here's what's happening today", size=16),
                ft.Container(height=24),
                ft.Row([tasks_card, notes_card], spacing=16),
                ft.Container(height=24),
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Row([ft.Icon(ft.Icons.SMART_TOY), ft.Text("AI Assistant", size=16, weight=ft.FontWeight.BOLD)], spacing=8),
                            chat_column,
                            ft.Row([message_input, send_button], spacing=12),
                        ],
                        spacing=12,
                    ),
                    padding=16,
                    border_radius=16,
                ),
            ],
            spacing=16,
        ),
    )

    return ft.View(route="/home", controls=[content])
