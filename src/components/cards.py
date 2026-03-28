"""Компоненты карточек для задач и заметок."""
import flet as ft

from config import (
    COLOR_ACCENT,
    COLOR_BG_SECONDARY,
    COLOR_DIVIDER,
    COLOR_CARD_BG,
    COLOR_TEXT_PRIMARY,
    COLOR_TEXT_SECONDARY,
    COLOR_TEXT_TERTIARY,
    COLOR_STATUS_INFO,
    COLOR_STATUS_URGENT,
    COLOR_STATUS_NORMAL,
    COLOR_STATUS_WARNING,
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
    elif task["status"] == "in_progress":
        status_color = COLOR_STATUS_INFO
    elif task["status"] == "completed":
        status_color = COLOR_STATUS_NORMAL
    else:
        status_color = COLOR_STATUS_WARNING

    # Формируем описание дедлайна
    deadline_text = f"Deadline: {task['deadline'][:16]}" if task.get("deadline") else "No deadline"

    # Обрезаем описание если длинное
    description = task.get("description", "")
    if len(description) > 100:
        description = description[:100] + "..."

    return ft.Container(
        border=ft.Border.all(1, COLOR_DIVIDER),
        shadow=[
            ft.BoxShadow(
                blur_radius=18,
                spread_radius=0,
                color="#00000022",
                offset=ft.Offset(0, 10),
            )
        ],
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
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                ft.Text(description, size=FONT_SIZE_SM, color=COLOR_TEXT_TERTIARY),
                ft.Row(
                    controls=[
                        ft.Chip(
                            ft.Text(task.get("category", "other"), size=FONT_SIZE_XS, color=COLOR_TEXT_PRIMARY),
                            bgcolor=COLOR_BG_SECONDARY,
                            label_padding=8,
                        ),
                        ft.Chip(
                            ft.Text(task.get("status", "pending").replace("_", " "), size=FONT_SIZE_XS, color=COLOR_TEXT_PRIMARY),
                            bgcolor=f"{status_color}22",
                            label_padding=8,
                        ),
                        ft.Text(deadline_text, size=FONT_SIZE_XS, color=COLOR_TEXT_TERTIARY),
                    ],
                    spacing=8,
                    wrap=True,
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
        border=ft.Border.all(1, COLOR_DIVIDER),
        shadow=[
            ft.BoxShadow(
                blur_radius=18,
                spread_radius=0,
                color="#00000022",
                offset=ft.Offset(0, 10),
            )
        ],
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
                            icon_color=COLOR_ACCENT,
                            on_click=lambda e: on_edit(note),
                        ),
                    ],
                    spacing=8,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
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
