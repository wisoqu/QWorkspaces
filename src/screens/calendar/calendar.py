"""Экран календаря."""
import flet as ft

from config import (
    CARD_BORDER_RADIUS,
    COLOR_ACCENT,
    COLOR_BG_SECONDARY,
    COLOR_CARD_BG,
    COLOR_DIVIDER,
    COLOR_STATUS_URGENT,
    COLOR_TEXT_PRIMARY,
    COLOR_TEXT_SECONDARY,
    FONT_SIZE_BASE,
    FONT_SIZE_SM,
    FONT_SIZE_XL,
    PAGE_PADDING,
)
from database import get_tasks
from utils.session import get_current_user_id


def _agenda_card(task: dict, accent_color: str) -> ft.Container:
    deadline = task.get("deadline") or "No deadline"
    return ft.Container(
        bgcolor=COLOR_CARD_BG,
        border_radius=CARD_BORDER_RADIUS,
        border=ft.Border.all(1, f"{accent_color}44"),
        padding=16,
        content=ft.Column(
            controls=[
                ft.Text(task.get("title", "Untitled"), size=FONT_SIZE_BASE, weight=ft.FontWeight.BOLD, color=COLOR_TEXT_PRIMARY),
                ft.Text(
                    f"{task.get('category', 'other').capitalize()} • {task.get('status', 'pending').replace('_', ' ')}",
                    size=FONT_SIZE_SM,
                    color=COLOR_TEXT_SECONDARY,
                ),
                ft.Text(deadline[:16], size=FONT_SIZE_SM, color=accent_color),
            ],
            spacing=6,
        ),
    )


def calendar_screen(page: ft.Page) -> ft.View:
    """Экран календаря с задачами по дедлайнам."""
    user_id = get_current_user_id(page)
    tasks = get_tasks(user_id) if user_id is not None else []
    scheduled_tasks = [task for task in tasks if task.get("deadline")]
    scheduled_tasks.sort(key=lambda task: task["deadline"])
    overdue_tasks = [task for task in scheduled_tasks if task.get("status") == "overdue"]

    if scheduled_tasks:
        agenda_controls = [
            _agenda_card(task, COLOR_STATUS_URGENT if task.get("status") == "overdue" else COLOR_ACCENT)
            for task in scheduled_tasks
        ]
    else:
        agenda_controls = [
            ft.Container(
                bgcolor=COLOR_CARD_BG,
                border_radius=CARD_BORDER_RADIUS,
                border=ft.Border.all(1, COLOR_DIVIDER),
                padding=24,
                content=ft.Column(
                    controls=[
                        ft.Icon(ft.Icons.CALENDAR_MONTH, size=56, color=COLOR_ACCENT),
                        ft.Text("No scheduled tasks yet", size=FONT_SIZE_BASE, weight=ft.FontWeight.BOLD, color=COLOR_TEXT_PRIMARY),
                        ft.Text(
                            "Add a deadline to any task and it will appear here as a lightweight agenda.",
                            size=FONT_SIZE_SM,
                            color=COLOR_TEXT_SECONDARY,
                            text_align=ft.TextAlign.CENTER,
                        ),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=12,
                ),
            )
        ]

    content = ft.Container(
        expand=True,
        padding=PAGE_PADDING,
        content=ft.Column(
            controls=[
                ft.Container(
                    bgcolor=COLOR_BG_SECONDARY,
                    border_radius=CARD_BORDER_RADIUS,
                    border=ft.Border.all(1, COLOR_DIVIDER),
                    padding=24,
                    content=ft.Column(
                        controls=[
                            ft.Text("Calendar", size=FONT_SIZE_XL, weight=ft.FontWeight.BOLD, color=COLOR_TEXT_PRIMARY),
                            ft.Text(
                                f"Upcoming scheduled tasks: {len(scheduled_tasks)} • Overdue: {len(overdue_tasks)}",
                                size=FONT_SIZE_SM,
                                color=COLOR_TEXT_SECONDARY,
                            ),
                        ],
                        spacing=8,
                    )
                ),
                ft.Column(controls=agenda_controls, spacing=14, scroll=ft.ScrollMode.AUTO, expand=True),
            ],
            spacing=16,
            expand=True,
        ),
    )

    return ft.View(route="/calendar", controls=[content])
