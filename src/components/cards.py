"""Компоненты карточек для задач и заметок."""
import flet as ft
import sys
from pathlib import Path

# Добавляем src в sys.path для корректных импортов
src_path = Path(__file__).resolve().parent.parent
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

from config import (
    COLOR_BG_SECONDARY,
    COLOR_CARD_BG,
    COLOR_TEXT_PRIMARY,
    COLOR_TEXT_SECONDARY,
    COLOR_TEXT_TERTIARY,
    COLOR_STATUS_URGENT,
    COLOR_STATUS_NORMAL,
    FONT_SIZE_BASE,
    FONT_SIZE_SM,
    FONT_SIZE_XS,
    CARD_PADDING,
    CARD_BORDER_RADIUS,
)


def create_task_card(
    task: dict,
    on_edit: callable,
) -> ft.Container:
    """
    Создает карточку задачи.
    
    Args:
        task: Словарь с данными задачи
        on_edit: Callback при клике на редактирование
    """
    # Определяем цвет статуса
    status_color = COLOR_STATUS_NORMAL
    if task["status"] == "overdue":
        status_color = COLOR_STATUS_URGENT

    # Формируем описание дедлайна
    deadline_text = f"Deadline: {task['deadline'][:16]}" if task.get("deadline") else "No deadline"

    # Обрезаем описание если длинное
    description = task.get("description", "")
    if len(description) > 100:
        description = description[:100] + "..."

    return ft.Container(
        content=ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.Container(
                            width=8,
                            height=8,
                            border_radius=2,
                            bgcolor=status_color,
                        ),
                        ft.Text(
                            task["title"],
                            size=FONT_SIZE_BASE,
                            weight=ft.FontWeight.BOLD,
                            color=COLOR_TEXT_PRIMARY,
                            expand=True,
                        ),
                        ft.IconButton(
                            ft.Icons.EDIT,
                            icon_size=18,
                            icon_color=COLOR_TEXT_SECONDARY,
                            on_click=lambda e: on_edit(task),
                        ),
                    ],
                    spacing=8,
                ),
                ft.Text(description, size=FONT_SIZE_SM, color=COLOR_TEXT_TERTIARY),
                ft.Row(
                    controls=[
                        ft.Chip(
                            ft.Text(task.get("category", "other"), size=FONT_SIZE_XS, color=COLOR_TEXT_PRIMARY),
                            bgcolor=COLOR_BG_SECONDARY,
                            label_padding=8,
                        ),
                        ft.Text(deadline_text, size=FONT_SIZE_XS, color=COLOR_TEXT_TERTIARY),
                    ],
                    spacing=8,
                ),
            ],
            spacing=8,
        ),
        bgcolor=COLOR_CARD_BG,
        border_radius=CARD_BORDER_RADIUS,
        padding=CARD_PADDING,
    )


def create_note_card(
    note: dict,
    on_edit: callable,
) -> ft.Container:
    """
    Создает карточку заметки.
    
    Args:
        note: Словарь с данными заметки
        on_edit: Callback при клике на редактирование
    """
    # Обрезаем контент если длинный
    content = note.get("content", "")
    if len(content) > 150:
        content = content[:150] + "..."

    return ft.Container(
        content=ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.Text(
                            note["title"],
                            size=FONT_SIZE_BASE,
                            weight=ft.FontWeight.BOLD,
                            color=COLOR_TEXT_PRIMARY,
                            expand=True,
                        ),
                        ft.IconButton(
                            ft.Icons.EDIT,
                            icon_size=18,
                            icon_color=COLOR_TEXT_SECONDARY,
                            on_click=lambda e: on_edit(note),
                        ),
                    ],
                    spacing=8,
                ),
                ft.Text(content, size=FONT_SIZE_SM, color=COLOR_TEXT_TERTIARY),
                ft.Chip(
                    ft.Text(note.get("category", "other"), size=FONT_SIZE_XS, color=COLOR_TEXT_PRIMARY),
                    bgcolor=COLOR_BG_SECONDARY,
                    label_padding=8,
                ),
            ],
            spacing=8,
        ),
        bgcolor=COLOR_CARD_BG,
        border_radius=CARD_BORDER_RADIUS,
        padding=CARD_PADDING,
    )
