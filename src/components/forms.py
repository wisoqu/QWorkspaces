"""Базовые компоненты для форм."""
import flet as ft
import sys
from pathlib import Path

# Добавляем src в sys.path для корректных импортов
src_path = Path(__file__).resolve().parent.parent
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

from config import (
    COLOR_TEXT_PRIMARY,
    COLOR_TEXT_SECONDARY,
    COLOR_TEXT_ERROR,
    COLOR_ACCENT,
    COLOR_INPUT_BG,
    FONT_SIZE_LG,
    FONT_SIZE_BASE,
    FONT_SIZE_SM,
    CARD_BORDER_RADIUS,
    INPUT_BORDER_RADIUS,
    SPACING_MD,
)


def create_text_field(
    label: str,
    value: str = "",
    hint_text: str = "",
    multiline: bool = False,
    min_lines: int = 1,
    max_lines: int = 1,
    expand: bool = True,
) -> ft.TextField:
    """Создает стандартное текстовое поле."""
    return ft.TextField(
        label=label,
        value=value,
        hint_text=hint_text,
        border_radius=INPUT_BORDER_RADIUS,
        filled=True,
        bgcolor=COLOR_INPUT_BG,
        color=COLOR_TEXT_PRIMARY,
        multiline=multiline,
        min_lines=min_lines,
        max_lines=max_lines,
        expand=expand,
    )


def create_dropdown(
    label: str,
    options: list[tuple[str, str]],
    value: str = "",
    expand: bool = True,
) -> ft.Dropdown:
    """
    Создает стандартный выпадающий список.

    Args:
        label: Заголовок поля
        options: Список кортежей (value, display_text)
        value: Текущее значение
        expand: Растягивать ли поле
    """
    return ft.Dropdown(
        label=label,
        value=value,
        options=[ft.dropdown.Option(key=val, text=text) for val, text in options],
        border_radius=INPUT_BORDER_RADIUS,
        filled=True,
        bgcolor=COLOR_INPUT_BG,
        color=COLOR_TEXT_PRIMARY,
        expand=expand,
    )


def create_error_text(message: str = "") -> ft.Text:
    """Создает текст ошибки."""
    return ft.Text(message, color=COLOR_TEXT_ERROR, size=FONT_SIZE_SM)


def create_form_dialog(
    page: ft.Page,
    title: str,
    content_controls: list,
    actions: list,
) -> ft.AlertDialog:
    """
    Создает стандартный диалог формы.

    Args:
        page: Страница
        title: Заголовок диалога
        content_controls: Список элементов контента
        actions: Список кнопок действий
    """
    return ft.AlertDialog(
        open=True,
        modal=True,
        title=ft.Text(title, size=FONT_SIZE_LG, weight=ft.FontWeight.BOLD),
        content=ft.Column(
            controls=content_controls,
            spacing=SPACING_MD,
            tight=True,
        ),
        actions=actions,
        actions_alignment=ft.MainAxisAlignment.END,
    )


def create_cancel_button(on_click: callable) -> ft.TextButton:
    """Создает кнопку отмены."""
    return ft.TextButton("Cancel", on_click=on_click)


def create_save_button(on_click: callable) -> ft.TextButton:
    """Создает кнопку сохранения."""
    return ft.TextButton("Save", on_click=on_click)


def create_delete_button(on_click: callable) -> ft.TextButton:
    """Создает кнопку удаления."""
    return ft.TextButton("Delete", on_click=on_click)
