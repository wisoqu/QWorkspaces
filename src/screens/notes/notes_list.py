"""Список заметок."""
import flet as ft

from _imports import *  # noqa: F401,F403
from components import create_empty_state, create_note_card
from database import get_notes
from screens.notes.note_form import note_form_dialog
from utils.session import get_current_user_id


def _load_notes(
    page: ft.Page,
    notes_list: ft.Column,
    user_id: int | None,
    update_page: bool = True,
) -> None:
    """Загружает заметки из БД."""
    notes_list.controls.clear()
    notes = get_notes(user_id) if user_id is not None else []

    if not notes:
        notes_list.controls.append(create_empty_state(ft.Icons.NOTE, "No notes yet"))
    else:
        for note in notes:
            notes_list.controls.append(
                create_note_card(note, lambda current_note: open_edit_dialog(page, current_note, user_id))
            )

    if update_page:
        page.update()


def open_edit_dialog(page: ft.Page, note: dict, user_id: int | None) -> None:
    """Открывает диалог редактирования заметки."""
    if user_id is None:
        return

    note_form_dialog(
        page,
        note_id=note["id"],
        user_id=user_id,
        on_save=lambda: _load_notes(page, page.notes_list, user_id),
    )


def open_add_dialog(page: ft.Page, user_id: int | None) -> None:
    """Открывает диалог создания заметки."""
    if user_id is None:
        return

    note_form_dialog(
        page,
        note_id=None,
        user_id=user_id,
        on_save=lambda: _load_notes(page, page.notes_list, user_id),
    )


def notes_screen(page: ft.Page) -> ft.View:
    """Экран заметок пользователя."""
    user_id = get_current_user_id(page)
    notes_list = ft.Column(spacing=12)
    page.notes_list = notes_list

    _load_notes(page, notes_list, user_id, update_page=False)

    title = ft.Text("Notes", size=24, weight=ft.FontWeight.BOLD)
    add_button = ft.Container(
        content=ft.Row([ft.Icon(ft.Icons.ADD, size=20), ft.Text("Add Note")], spacing=8),
        padding=12,
        border_radius=16,
        on_click=lambda e: open_add_dialog(page, user_id),
    )

    content = ft.Container(
        expand=True,
        padding=20,
        content=ft.Column(
            controls=[
                ft.Row([title, add_button], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Container(height=24),
                notes_list,
            ],
            spacing=16,
        ),
    )

    return ft.View(route="/notes", controls=[content])
