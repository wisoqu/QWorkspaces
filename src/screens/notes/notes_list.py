"""Список заметок."""
import flet as ft

from components import create_empty_state, create_note_card
from config import (
    CARD_BORDER_RADIUS,
    COLOR_ACCENT,
    COLOR_BG_SECONDARY,
    COLOR_CARD_BG,
    COLOR_DIVIDER,
    COLOR_INPUT_BG,
    COLOR_TEXT_PRIMARY,
    COLOR_TEXT_SECONDARY,
    FONT_SIZE_BASE,
    FONT_SIZE_SM,
    FONT_SIZE_XL,
    PAGE_PADDING,
    SPACING_MD,
)
from database import get_notes
from screens.notes.note_form import note_form_dialog
from screens.tasks.task_form import CATEGORY_OPTIONS
from utils.session import get_current_user_id


def _current_filters(page: ft.Page) -> tuple[str, str | None]:
    search_query = (page.note_search.value or "").strip()
    category = page.note_category.value if getattr(page, "note_category", None) else "all"
    return search_query, None if category == "all" else category


def _filter_notes(
    notes: list[dict],
    *,
    search_query: str = "",
    category_filter: str | None = None,
) -> list[dict]:
    filtered_notes = notes

    if search_query:
        search_lower = search_query.lower()
        filtered_notes = [
            note
            for note in filtered_notes
            if search_lower in note.get("title", "").lower()
            or search_lower in note.get("content", "").lower()
        ]

    if category_filter:
        filtered_notes = [note for note in filtered_notes if note.get("category") == category_filter]

    return filtered_notes


def _update_stats(page: ft.Page, notes: list[dict], filtered_notes: list[dict]) -> None:
    page.note_total_stat.value = str(len(notes))
    page.note_filtered_stat.value = str(len(filtered_notes))
    page.note_long_stat.value = str(
        len([note for note in notes if len((note.get("content") or "").strip()) >= 120])
    )


def _load_notes(
    page: ft.Page,
    notes_list: ft.Column,
    user_id: int | None,
    *,
    search_query: str = "",
    category_filter: str | None = None,
    update_page: bool = True,
) -> None:
    """Загружает заметки из БД с фильтрацией."""
    notes_list.controls.clear()
    notes = get_notes(user_id) if user_id is not None else []
    filtered_notes = _filter_notes(
        notes,
        search_query=search_query,
        category_filter=category_filter,
    )
    _update_stats(page, notes, filtered_notes)

    if not filtered_notes:
        message = "No notes found" if search_query or category_filter else "No notes yet"
        notes_list.controls.append(create_empty_state(ft.Icons.NOTE, message))
    else:
        for note in filtered_notes:
            notes_list.controls.append(
                create_note_card(note, lambda current_note: open_edit_dialog(page, current_note, user_id))
            )

    if update_page:
        page.update()


def _reload_notes(page: ft.Page, user_id: int | None, update_page: bool = True) -> None:
    search_query, category_filter = _current_filters(page)
    _load_notes(
        page,
        page.notes_list,
        user_id,
        search_query=search_query,
        category_filter=category_filter,
        update_page=update_page,
    )


def _stat_card(label: str, value_control: ft.Text) -> ft.Container:
    return ft.Container(
        bgcolor=COLOR_BG_SECONDARY,
        border_radius=CARD_BORDER_RADIUS,
        border=ft.Border.all(1, COLOR_DIVIDER),
        padding=14,
        content=ft.Column(
            controls=[
                ft.Text(label, size=FONT_SIZE_SM, color=COLOR_TEXT_SECONDARY),
                value_control,
            ],
            spacing=6,
        ),
    )


def open_edit_dialog(page: ft.Page, note: dict, user_id: int | None) -> None:
    """Открывает диалог редактирования заметки."""
    if user_id is None:
        return

    note_form_dialog(
        page,
        note_id=note["id"],
        user_id=user_id,
        on_save=lambda: _reload_notes(page, user_id),
    )


def open_add_dialog(page: ft.Page, user_id: int | None) -> None:
    """Открывает диалог создания заметки."""
    if user_id is None:
        return

    note_form_dialog(
        page,
        note_id=None,
        user_id=user_id,
        on_save=lambda: _reload_notes(page, user_id),
    )


def notes_screen(page: ft.Page) -> ft.View:
    """Экран заметок пользователя."""
    user_id = get_current_user_id(page)
    notes_list = ft.Column(spacing=14, scroll=ft.ScrollMode.AUTO, expand=True)
    page.notes_list = notes_list
    page.note_total_stat = ft.Text("0", size=FONT_SIZE_XL, weight=ft.FontWeight.BOLD, color=COLOR_TEXT_PRIMARY)
    page.note_filtered_stat = ft.Text("0", size=FONT_SIZE_XL, weight=ft.FontWeight.BOLD, color=COLOR_TEXT_PRIMARY)
    page.note_long_stat = ft.Text("0", size=FONT_SIZE_XL, weight=ft.FontWeight.BOLD, color=COLOR_TEXT_PRIMARY)

    page.note_search = ft.TextField(
        hint_text="Search notes...",
        prefix_icon=ft.Icons.SEARCH,
        border_radius=12,
        filled=True,
        bgcolor=COLOR_INPUT_BG,
        color=COLOR_TEXT_PRIMARY,
        expand=True,
        on_change=lambda e: _reload_notes(page, user_id),
    )
    page.note_category = ft.Dropdown(
        options=[ft.dropdown.Option(key="all", text="All Categories")] + [
            ft.dropdown.Option(key=value, text=label) for value, label in CATEGORY_OPTIONS
        ],
        value="all",
        border_radius=12,
        filled=True,
        bgcolor=COLOR_INPUT_BG,
        color=COLOR_TEXT_PRIMARY,
        width=220,
        on_select=lambda e: _reload_notes(page, user_id),
    )

    _load_notes(page, notes_list, user_id, update_page=False)

    title_block = ft.Column(
        controls=[
            ft.Text("Notes", size=FONT_SIZE_XL, weight=ft.FontWeight.BOLD, color=COLOR_TEXT_PRIMARY),
            ft.Text(
                "Keep context, ideas and references in one searchable archive.",
                size=FONT_SIZE_BASE,
                color=COLOR_TEXT_SECONDARY,
            ),
        ],
        spacing=6,
    )
    add_button = ft.Container(
        bgcolor=COLOR_ACCENT,
        border_radius=16,
        padding=14,
        content=ft.Row(
            controls=[
                ft.Icon(ft.Icons.ADD, size=18, color="#0B0F14"),
                ft.Text("Add Note", color="#0B0F14", weight=ft.FontWeight.BOLD),
            ],
            spacing=8,
            tight=True,
        ),
        on_click=lambda e: open_add_dialog(page, user_id),
    )

    filters_row = ft.Row(
        controls=[page.note_search, page.note_category],
        spacing=12,
        wrap=True,
    )
    stats_row = ft.Row(
        controls=[
            _stat_card("Total", page.note_total_stat),
            _stat_card("Visible", page.note_filtered_stat),
            _stat_card("Long-form", page.note_long_stat),
        ],
        spacing=SPACING_MD,
        wrap=True,
    )
    list_shell = ft.Container(
        expand=True,
        bgcolor=COLOR_CARD_BG,
        border_radius=CARD_BORDER_RADIUS,
        border=ft.Border.all(1, COLOR_DIVIDER),
        padding=18,
        content=notes_list,
    )

    content = ft.Container(
        expand=True,
        padding=PAGE_PADDING,
        content=ft.Column(
            controls=[
                ft.Row(
                    controls=[title_block, add_button],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                filters_row,
                stats_row,
                list_shell,
            ],
            spacing=18,
            expand=True,
        ),
    )

    return ft.View(route="/notes", controls=[content])
