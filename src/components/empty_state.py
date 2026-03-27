"""Переиспользуемые UI-компоненты для пустых состояний."""
import flet as ft
import sys
from pathlib import Path

# Добавляем src в sys.path для корректных импортов
src_path = Path(__file__).resolve().parent.parent
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

from config import (
    COLOR_TEXT_TERTIARY,
    COLOR_TEXT_SECONDARY,
    FONT_SIZE_SM,
)


def create_empty_state(icon: ft.IconData, message: str) -> ft.Container:
    """
    Создает компонент пустого состояния.
    
    Args:
        icon: Иконка для отображения
        message: Текст сообщения
    
    Returns:
        Container с центрированным содержимым
    """
    return ft.Container(
        content=ft.Column(
            controls=[
                ft.Icon(icon, size=48, color=COLOR_TEXT_TERTIARY),
                ft.Text(message, color=COLOR_TEXT_SECONDARY, size=FONT_SIZE_SM),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=8,
        ),
        alignment=ft.Alignment.CENTER,
        expand=True,
        padding=40,
    )
