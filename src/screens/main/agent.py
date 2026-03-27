"""AI агент - чат с ассистентом."""
import flet as ft

def agent_screen(page: ft.Page) -> ft.View:
    """Экран AI-агента."""
    chat_column = ft.Column(spacing=12, height=400, scroll=ft.ScrollMode.AUTO)
    message_input = ft.TextField(
        hint_text="Ask AI assistant...",
        expand=True,
        border_radius=12,
        filled=True,
        multiline=True,
        min_lines=1,
        max_lines=3,
    )

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
                alignment=ft.Alignment(-0.7, 0),
            )
        )
        message_input.value = ""
        page.update()

    send_button = ft.Container(
        content=ft.Icon(ft.Icons.SEND, size=18),
        bgcolor="#7C5CFF",
        border_radius=16,
        width=40,
        height=40,
        alignment=ft.Alignment.CENTER,
        on_click=send_message,
    )

    content = ft.Container(
        expand=True,
        padding=40,
        content=ft.Column(
            controls=[
                ft.Text("AI Assistant", size=24, weight=ft.FontWeight.BOLD),
                ft.Container(height=16),
                chat_column,
                ft.Container(height=16),
                ft.Row([message_input, send_button], spacing=12),
            ],
            spacing=16,
        ),
    )

    return ft.View(route="/agent", controls=[content])
