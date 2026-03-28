"""AI агент - чат с ассистентом."""
import flet as ft

from config import (
    CARD_BORDER_RADIUS,
    COLOR_ACCENT,
    COLOR_BG_PRIMARY,
    COLOR_BG_SECONDARY,
    COLOR_CARD_BG,
    COLOR_DIVIDER,
    COLOR_INPUT_BG,
    COLOR_TEXT_PRIMARY,
    COLOR_TEXT_SECONDARY,
    FONT_SIZE_SM,
    FONT_SIZE_XL,
    PAGE_PADDING,
)

def agent_screen(page: ft.Page) -> ft.View:
    """Экран AI-агента."""
    chat_column = ft.Column(spacing=12, scroll=ft.ScrollMode.AUTO, expand=True)
    message_input = ft.TextField(
        hint_text="Ask AI assistant...",
        expand=True,
        border_radius=12,
        filled=True,
        multiline=True,
        min_lines=1,
        max_lines=3,
        bgcolor=COLOR_INPUT_BG,
        color=COLOR_TEXT_PRIMARY,
    )

    def send_message(e):
        text = message_input.value.strip()
        if not text:
            return
        chat_column.controls.append(
            ft.Row(
                controls=[
                    ft.Container(
                        content=ft.Text(text, size=14, color="#0B0F14"),
                        bgcolor=COLOR_ACCENT,
                        border_radius=16,
                        padding=12,
                    )
                ],
                alignment=ft.MainAxisAlignment.END,
            )
        )
        message_input.value = ""
        page.update()

    send_button = ft.Container(
        content=ft.Icon(ft.Icons.SEND, size=18, color="#0B0F14"),
        bgcolor=COLOR_ACCENT,
        border_radius=16,
        width=40,
        height=40,
        alignment=ft.Alignment.CENTER,
        on_click=send_message,
    )

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
                            ft.Text("AI Assistant", size=FONT_SIZE_XL, weight=ft.FontWeight.BOLD, color=COLOR_TEXT_PRIMARY),
                            ft.Text(
                                "A focused lane for short prompts, drafts and quick thinking.",
                                size=FONT_SIZE_SM,
                                color=COLOR_TEXT_SECONDARY,
                            ),
                        ],
                        spacing=8,
                    ),
                ),
                ft.Container(
                    expand=True,
                    bgcolor=COLOR_CARD_BG,
                    border_radius=CARD_BORDER_RADIUS,
                    border=ft.Border.all(1, COLOR_DIVIDER),
                    padding=18,
                    content=chat_column,
                ),
                ft.Container(
                    bgcolor=COLOR_BG_PRIMARY,
                    border_radius=CARD_BORDER_RADIUS,
                    border=ft.Border.all(1, COLOR_DIVIDER),
                    padding=14,
                    content=ft.Row([message_input, send_button], spacing=12),
                ),
            ],
            spacing=16,
            expand=True,
        ),
    )

    return ft.View(route="/agent", controls=[content])
