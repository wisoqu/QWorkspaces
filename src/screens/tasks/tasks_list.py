"""Список задач."""
import flet as ft

from _imports import *  # noqa: F401,F403
from components import create_empty_state, create_task_card
from database import get_tasks
from screens.tasks.task_form import task_form_dialog
from utils.session import get_current_user_id


def _load_tasks(
    page: ft.Page,
    tasks_list: ft.Column,
    user_id: int | None,
    update_page: bool = True,
) -> None:
    """Загружает задачи из БД."""
    tasks_list.controls.clear()
    tasks = get_tasks(user_id) if user_id is not None else []

    if not tasks:
        tasks_list.controls.append(create_empty_state(ft.Icons.TASK_ALT, "No tasks yet"))
    else:
        for task in tasks:
            tasks_list.controls.append(
                create_task_card(task, lambda current_task: open_edit_dialog(page, current_task, user_id))
            )

    if update_page:
        page.update()


def open_edit_dialog(page: ft.Page, task: dict, user_id: int | None) -> None:
    """Открывает диалог редактирования задачи."""
    if user_id is None:
        return

    task_form_dialog(
        page,
        task_id=task["id"],
        user_id=user_id,
        on_save=lambda: _load_tasks(page, page.tasks_list, user_id),
    )


def open_add_dialog(page: ft.Page, user_id: int | None) -> None:
    """Открывает диалог создания задачи."""
    if user_id is None:
        return

    task_form_dialog(
        page,
        task_id=None,
        user_id=user_id,
        on_save=lambda: _load_tasks(page, page.tasks_list, user_id),
    )


def tasks_screen(page: ft.Page) -> ft.View:
    """Экран задач пользователя."""
    user_id = get_current_user_id(page)
    tasks_list = ft.Column(spacing=12)
    page.tasks_list = tasks_list

    _load_tasks(page, tasks_list, user_id, update_page=False)

    title = ft.Text("Tasks", size=24, weight=ft.FontWeight.BOLD)
    add_button = ft.Container(
        content=ft.Row([ft.Icon(ft.Icons.ADD, size=20), ft.Text("Add Task")], spacing=8),
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
                tasks_list,
            ],
            spacing=16,
        ),
    )

    return ft.View(route="/tasks", controls=[content])
