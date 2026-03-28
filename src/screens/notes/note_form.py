"""Форма заметки."""
import flet as ft

from components import (
    create_cancel_button,
    create_delete_button,
    create_dropdown,
    create_error_text,
    create_form_dialog,
    create_save_button,
    create_text_field,
)
from database import create_note, delete_note, get_note, update_note
from schemas import validate_note
from screens.tasks.task_form import CATEGORY_OPTIONS


def note_form_dialog(page: ft.Page, note_id: int | None, user_id: int, on_save: callable) -> None:
    """Диалог создания/редактирования заметки."""
    existing_note = get_note(note_id, user_id) if note_id else None
    note = existing_note or {}

    title_field = create_text_field(label="Title", value=note.get("title", ""))
    content_field = create_text_field(
        label="Content",
        value=note.get("content", ""),
        multiline=True,
        min_lines=8,
        max_lines=12,
    )
    category_dropdown = create_dropdown(
        label="Category",
        options=CATEGORY_OPTIONS,
        value=note.get("category", "other"),
    )
    error_text = create_error_text()

    def close_dialog(e):
        page.pop_dialog()

    def save_click(e):
        title = title_field.value.strip()
        content = content_field.value.strip()
        category = category_dropdown.value

        # Валидируем title отдельно
        if not title:
            error_text.value = "Title cannot be empty"
            page.update()
            return

        # Валидируем заметку через schema
        _, error = validate_note(content)
        if error:
            error_text.value = error
            page.update()
            return

        if note_id:
            update_note(note_id=note_id, user_id=user_id, title=title, content=content, category=category)
        else:
            create_note(user_id=user_id, title=title, content=content, category=category)

        close_dialog(None)
        if on_save:
            on_save()

    def delete_click(e):
        if note_id:
            delete_note(note_id, user_id)
            close_dialog(None)
            if on_save:
                on_save()

    buttons = [create_cancel_button(close_dialog), create_save_button(save_click)]
    if note_id:
        buttons.insert(1, create_delete_button(delete_click))

    dialog = create_form_dialog(
        page=page,
        title="Edit Note" if note_id else "New Note",
        content_controls=[title_field, content_field, category_dropdown, error_text],
        actions=buttons,
    )

    page.show_dialog(dialog)
