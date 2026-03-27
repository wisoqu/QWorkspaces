"""Форма задачи."""
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
from database import create_task, delete_task, get_task, update_task
from schemas import validate_task


CATEGORY_OPTIONS = [
    ("work", "Work"),
    ("hobby", "Hobby"),
    ("home", "Home"),
    ("personal", "Personal"),
    ("other", "Other"),
]
STATUS_OPTIONS = [
    ("pending", "Pending"),
    ("in_progress", "In Progress"),
    ("completed", "Completed"),
    ("overdue", "Overdue"),
]


def task_form_dialog(page: ft.Page, task_id: int | None = None, user_id: int = 1, on_save: callable = None):
    """Диалог создания/редактирования задачи."""
    existing_task = get_task(task_id, user_id) if task_id else None
    task = existing_task or {}

    title_field = create_text_field(label="Title", value=task.get("title", ""))
    description_field = create_text_field(
        label="Description",
        value=task.get("description", ""),
        multiline=True,
        min_lines=3,
        max_lines=5,
    )
    category_dropdown = create_dropdown(
        label="Category",
        options=CATEGORY_OPTIONS,
        value=task.get("category", "other"),
    )
    deadline_field = create_text_field(
        label="Deadline (YYYY-MM-DD HH:MM)",
        value=task.get("deadline", "")[:16] if task.get("deadline") else "",
        hint_text="2026-03-30 18:00",
    )
    status_dropdown = create_dropdown(
        label="Status",
        options=STATUS_OPTIONS,
        value=task.get("status", "pending"),
    )
    error_text = create_error_text()

    def close_dialog(e):
        page.pop_dialog()

    def save_click(e):
        title = title_field.value.strip()
        description = description_field.value.strip()
        category = category_dropdown.value
        deadline = deadline_field.value.strip() or None
        status = status_dropdown.value

        _, error = validate_task(title, description)
        if error:
            error_text.value = error
            page.update()
            return

        if task_id:
            update_task(
                task_id=task_id,
                user_id=user_id,
                title=title,
                description=description,
                category=category,
                deadline=deadline,
                status=status,
            )
        else:
            create_task(
                user_id=user_id,
                title=title,
                description=description,
                category=category,
                deadline=deadline,
                status=status,
            )

        close_dialog(None)
        if on_save:
            on_save()

    def delete_click(e):
        if task_id:
            delete_task(task_id, user_id)
            close_dialog(None)
            if on_save:
                on_save()

    buttons = [create_cancel_button(close_dialog), create_save_button(save_click)]
    if task_id:
        buttons.insert(1, create_delete_button(delete_click))

    dialog = create_form_dialog(
        page=page,
        title="Edit Task" if task_id else "New Task",
        content_controls=[
            title_field,
            description_field,
            category_dropdown,
            deadline_field,
            status_dropdown,
            error_text,
        ],
        actions=buttons,
    )

    page.open(dialog)
