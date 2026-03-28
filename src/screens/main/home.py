"""Главная страница с отдельными блоками задач, заметок и панели ассистента."""
import flet as ft

from config import (
    AGENT_PANEL_WIDTH,
    CARD_BORDER_RADIUS,
    COLOR_ACCENT,
    COLOR_BG_PRIMARY,
    COLOR_BG_SECONDARY,
    COLOR_BG_TERTIARY,
    COLOR_CARD_BG,
    COLOR_DIVIDER,
    COLOR_INPUT_BG,
    COLOR_TEXT_PRIMARY,
    COLOR_TEXT_SECONDARY,
    COLOR_TEXT_TERTIARY,
    FONT_SIZE_BASE,
    FONT_SIZE_LG,
    FONT_SIZE_SM,
    FONT_SIZE_XL,
    PAGE_PADDING,
    SPACING_LG,
    SPACING_MD,
    SPACING_SM,
)
from database import get_notes, get_tasks
from utils.session import get_current_user_id, get_current_user_name

TASKS_ACCENT = "#6EA7FF"
NOTES_ACCENT = COLOR_ACCENT


def _section_icon(icon: str, accent_color: str) -> ft.Container:
    return ft.Container(
        width=42,
        height=42,
        border_radius=14,
        bgcolor=f"{accent_color}22",
        alignment=ft.Alignment.CENTER,
        content=ft.Icon(icon, size=20, color=accent_color),
    )


def _section_shell(
    *,
    icon: str,
    title: str,
    subtitle: str,
    accent_color: str,
    body: ft.Control,
    expand: bool = False,
    width: int | None = None,
) -> ft.Container:
    return ft.Container(
        expand=expand,
        width=width,
        padding=22,
        bgcolor=COLOR_CARD_BG,
        border_radius=CARD_BORDER_RADIUS + 2,
        border=ft.Border.all(1, f"{accent_color}55"),
        shadow=[
            ft.BoxShadow(
                blur_radius=18,
                spread_radius=0,
                color="#00000026",
                offset=ft.Offset(0, 8),
            )
        ],
        content=ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        _section_icon(icon, accent_color),
                        ft.Column(
                            controls=[
                                ft.Text(
                                    title,
                                    size=FONT_SIZE_LG,
                                    weight=ft.FontWeight.BOLD,
                                    color=COLOR_TEXT_PRIMARY,
                                ),
                                ft.Text(
                                    subtitle,
                                    size=FONT_SIZE_SM,
                                    color=COLOR_TEXT_SECONDARY,
                                ),
                            ],
                            spacing=2,
                            expand=True,
                        ),
                    ],
                    spacing=12,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                ft.Divider(color=COLOR_DIVIDER, height=1),
                body,
            ],
            spacing=16,
            expand=expand,
        ),
    )


def _summary_chip(label: str, value: int, accent_color: str) -> ft.Container:
    return ft.Container(
        padding=ft.Padding(12, 8, 12, 8),
        border_radius=999,
        bgcolor=COLOR_BG_PRIMARY,
        border=ft.Border.all(1, f"{accent_color}44"),
        content=ft.Row(
            controls=[
                ft.Container(
                    width=8,
                    height=8,
                    border_radius=4,
                    bgcolor=accent_color,
                ),
                ft.Text(label, size=FONT_SIZE_SM, color=COLOR_TEXT_SECONDARY),
                ft.Text(str(value), size=FONT_SIZE_SM, weight=ft.FontWeight.BOLD),
            ],
            spacing=8,
            tight=True,
        ),
    )


def _preview_item(title: str, meta: str, accent_color: str) -> ft.Container:
    return ft.Container(
        padding=16,
        bgcolor=COLOR_BG_PRIMARY,
        border_radius=CARD_BORDER_RADIUS,
        border=ft.Border.all(1, f"{accent_color}33"),
        content=ft.Column(
            controls=[
                ft.Text(
                    title,
                    size=FONT_SIZE_BASE,
                    weight=ft.FontWeight.BOLD,
                    color=COLOR_TEXT_PRIMARY,
                ),
                ft.Text(
                    meta,
                    size=FONT_SIZE_SM,
                    color=COLOR_TEXT_TERTIARY,
                ),
            ],
            spacing=6,
        ),
    )


def _empty_preview(message: str, accent_color: str) -> ft.Container:
    return ft.Container(
        padding=18,
        bgcolor=COLOR_BG_PRIMARY,
        border_radius=CARD_BORDER_RADIUS,
        border=ft.Border.all(1, f"{accent_color}22"),
        content=ft.Text(message, size=FONT_SIZE_SM, color=COLOR_TEXT_TERTIARY),
    )


def _task_meta(task: dict) -> str:
    parts = []
    category = task.get("category")
    status = task.get("status")
    deadline = task.get("deadline")

    if category:
        parts.append(category.capitalize())
    if status:
        parts.append(status.replace("_", " ").capitalize())
    if deadline:
        parts.append(f"Due {deadline[:16]}")

    return " • ".join(parts) if parts else "No details yet"


def _note_meta(note: dict) -> str:
    category = note.get("category")
    content = (note.get("content") or "").strip().replace("\n", " ")
    if content:
        content = content[:90] + ("..." if len(content) > 90 else "")

    parts = []
    if category:
        parts.append(category.capitalize())
    if content:
        parts.append(content)

    return " • ".join(parts) if parts else "No details yet"


def _preview_list(
    items: list[dict],
    *,
    accent_color: str,
    empty_message: str,
    meta_builder,
) -> ft.Column:
    if not items:
        return ft.Column(
            controls=[_empty_preview(empty_message, accent_color)],
            spacing=12,
        )

    return ft.Column(
        controls=[
            _preview_item(
                item.get("title", "Untitled"),
                meta_builder(item),
                accent_color,
            )
            for item in items
        ],
        spacing=12,
    )


def home_screen(page: ft.Page) -> ft.View:
    """Главная страница."""
    user_name = get_current_user_name(page)
    user_id = get_current_user_id(page)
    recent_tasks = get_tasks(user_id)[:3] if user_id is not None else []
    recent_notes = get_notes(user_id)[:3] if user_id is not None else []

    chat_column = ft.Column(
        controls=[
            ft.Container(
                padding=14,
                border_radius=CARD_BORDER_RADIUS,
                border=ft.Border.all(1, f"{COLOR_ACCENT}33"),
                bgcolor=COLOR_BG_TERTIARY,
                content=ft.Text(
                    "Use this side panel to sketch a plan, break a task into steps, or capture a thought before it gets lost.",
                    size=FONT_SIZE_SM,
                    color=COLOR_TEXT_SECONDARY,
                ),
            )
        ],
        spacing=10,
        scroll=ft.ScrollMode.AUTO,
        expand=True,
    )

    message_input = ft.TextField(
        hint_text="Ask for a plan or next step...",
        expand=True,
        border_radius=12,
        filled=True,
        multiline=True,
        min_lines=1,
        max_lines=4,
        bgcolor=COLOR_INPUT_BG,
        color=COLOR_TEXT_PRIMARY,
    )

    def send_message(e):
        text = (message_input.value or "").strip()
        if not text:
            return

        chat_column.controls.append(
            ft.Row(
                controls=[
                    ft.Container(
                        content=ft.Text(text, size=FONT_SIZE_SM, color=COLOR_TEXT_PRIMARY),
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
        content=ft.Icon(ft.Icons.SEND, size=18, color=COLOR_TEXT_PRIMARY),
        bgcolor=COLOR_ACCENT,
        border_radius=16,
        width=46,
        height=46,
        alignment=ft.Alignment.CENTER,
        on_click=send_message,
    )

    overview_section = ft.Container(
        padding=24,
        bgcolor=COLOR_BG_SECONDARY,
        border_radius=CARD_BORDER_RADIUS + 4,
        border=ft.Border.all(1, COLOR_DIVIDER),
        content=ft.Column(
            controls=[
                ft.Text("Workspace overview", size=FONT_SIZE_SM, color=COLOR_TEXT_SECONDARY),
                ft.Text(
                    f"Good day, {user_name}.",
                    size=FONT_SIZE_XL,
                    weight=ft.FontWeight.BOLD,
                    color=COLOR_TEXT_PRIMARY,
                ),
                ft.Text(
                    "The home screen is split into focused blocks so tasks, notes, and quick thinking space are easier to scan.",
                    size=FONT_SIZE_BASE,
                    color=COLOR_TEXT_SECONDARY,
                ),
                ft.Row(
                    controls=[
                        _summary_chip("Tasks", len(recent_tasks), TASKS_ACCENT),
                        _summary_chip("Notes", len(recent_notes), NOTES_ACCENT),
                    ],
                    spacing=12,
                    wrap=True,
                ),
            ],
            spacing=14,
        ),
    )

    tasks_section = _section_shell(
        icon=ft.Icons.TASK_ALT,
        title="Tasks",
        subtitle="Current priorities in a dedicated block",
        accent_color=TASKS_ACCENT,
        body=_preview_list(
            recent_tasks,
            accent_color=TASKS_ACCENT,
            empty_message="No tasks yet.",
            meta_builder=_task_meta,
        ),
    )

    notes_section = _section_shell(
        icon=ft.Icons.NOTE_ALT,
        title="Notes",
        subtitle="Separate space for captured context and ideas",
        accent_color=NOTES_ACCENT,
        body=_preview_list(
            recent_notes,
            accent_color=NOTES_ACCENT,
            empty_message="No notes yet.",
            meta_builder=_note_meta,
        ),
    )

    assistant_panel = _section_shell(
        icon=ft.Icons.SMART_TOY,
        title="Focus lane",
        subtitle="A narrow vertical panel for quick prompts and drafts",
        accent_color=COLOR_ACCENT,
        width=AGENT_PANEL_WIDTH,
        expand=True,
        body=ft.Column(
            controls=[
                ft.Container(
                    expand=True,
                    padding=14,
                    bgcolor=COLOR_BG_PRIMARY,
                    border_radius=CARD_BORDER_RADIUS,
                    border=ft.Border.all(1, f"{COLOR_ACCENT}22"),
                    content=chat_column,
                ),
                ft.Container(
                    padding=12,
                    bgcolor=COLOR_BG_PRIMARY,
                    border_radius=CARD_BORDER_RADIUS,
                    border=ft.Border.all(1, COLOR_DIVIDER),
                    content=ft.Row(
                        controls=[message_input, send_button],
                        spacing=12,
                        vertical_alignment=ft.CrossAxisAlignment.END,
                    ),
                ),
            ],
            spacing=14,
            expand=True,
        ),
    )

    main_column = ft.Column(
        controls=[
            overview_section,
            tasks_section,
            notes_section,
        ],
        spacing=SPACING_LG,
        scroll=ft.ScrollMode.AUTO,
        expand=True,
    )

    content = ft.Container(
        expand=True,
        padding=PAGE_PADDING + 8,
        content=ft.Row(
            controls=[
                main_column,
                assistant_panel,
            ],
            spacing=SPACING_LG,
            expand=True,
            vertical_alignment=ft.CrossAxisAlignment.START,
        ),
    )

    return ft.View(route="/home", controls=[content])
