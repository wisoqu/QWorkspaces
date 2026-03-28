"""Переиспользуемые UI-компоненты для пустых состояний."""
import flet as ft

from config import (
    CARD_BORDER_RADIUS,
    COLOR_CARD_BG,
    COLOR_DIVIDER,
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
        bgcolor=COLOR_CARD_BG,
        border_radius=CARD_BORDER_RADIUS,
        border=ft.Border.all(1, COLOR_DIVIDER),
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
