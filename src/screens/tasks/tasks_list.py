"""Список задач."""
import flet as ft

from components import create_empty_state, create_task_card
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
from database import get_tasks
from screens.tasks.task_form import CATEGORY_OPTIONS, STATUS_OPTIONS, task_form_dialog
from utils.session import get_current_user_id


def _current_filters(page: ft.Page) -> tuple[str, str | None, str | None]:
    search_query = (page.task_search.value or "").strip()
    status = page.task_status.value if getattr(page, "task_status", None) else "all"
    category = page.task_category.value if getattr(page, "task_category", None) else "all"
    return (
        search_query,
        None if status == "all" else status,
        None if category == "all" else category,
    )


def _filter_tasks(
    tasks: list[dict],
    *,
    search_query: str = "",
    status_filter: str | None = None,
    category_filter: str | None = None,
) -> list[dict]:
    filtered_tasks = tasks

    if search_query:
        search_lower = search_query.lower()
        filtered_tasks = [
            task
            for task in filtered_tasks
            if search_lower in task.get("title", "").lower()
            or search_lower in task.get("description", "").lower()
        ]

    if status_filter:
        filtered_tasks = [task for task in filtered_tasks if task.get("status") == status_filter]

    if category_filter:
        filtered_tasks = [task for task in filtered_tasks if task.get("category") == category_filter]

    return filtered_tasks


def _update_stats(page: ft.Page, tasks: list[dict], filtered_tasks: list[dict]) -> None:
    page.task_total_stat.value = str(len(tasks))
    page.task_filtered_stat.value = str(len(filtered_tasks))
    page.task_completed_stat.value = str(
        len([task for task in tasks if task.get("status") == "completed"])
    )


def _load_tasks(
    page: ft.Page,
    tasks_list: ft.Column,
    user_id: int | None,
    *,
    search_query: str = "",
    status_filter: str | None = None,
    category_filter: str | None = None,
    update_page: bool = True,
) -> None:
    """Загружает задачи из БД с фильтрацией."""
    tasks_list.controls.clear()
    tasks = get_tasks(user_id) if user_id is not None else []
    filtered_tasks = _filter_tasks(
        tasks,
        search_query=search_query,
        status_filter=status_filter,
        category_filter=category_filter,
    )
    _update_stats(page, tasks, filtered_tasks)

    if not filtered_tasks:
        message = "No tasks found" if search_query or status_filter or category_filter else "No tasks yet"
        tasks_list.controls.append(create_empty_state(ft.Icons.TASK_ALT, message))
    else:
        for task in filtered_tasks:
            tasks_list.controls.append(
                create_task_card(task, lambda current_task: open_edit_dialog(page, current_task, user_id))
            )

    if update_page:
        page.update()


def _reload_tasks(page: ft.Page, user_id: int | None, update_page: bool = True) -> None:
    search_query, status_filter, category_filter = _current_filters(page)
    _load_tasks(
        page,
        page.tasks_list,
        user_id,
        search_query=search_query,
        status_filter=status_filter,
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


def open_edit_dialog(page: ft.Page, task: dict, user_id: int | None) -> None:
    """Открывает диалог редактирования задачи."""
    if user_id is None:
        return

    task_form_dialog(
        page,
        task_id=task["id"],
        user_id=user_id,
        on_save=lambda: _reload_tasks(page, user_id),
    )


def open_add_dialog(page: ft.Page, user_id: int | None) -> None:
    """Открывает диалог создания задачи."""
    if user_id is None:
        return

    task_form_dialog(
        page,
        task_id=None,
        user_id=user_id,
        on_save=lambda: _reload_tasks(page, user_id),
    )


def tasks_screen(page: ft.Page) -> ft.View:
    """Экран задач пользователя."""
    user_id = get_current_user_id(page)
    tasks_list = ft.Column(spacing=14, scroll=ft.ScrollMode.AUTO, expand=True)
    page.tasks_list = tasks_list
    page.task_total_stat = ft.Text("0", size=FONT_SIZE_XL, weight=ft.FontWeight.BOLD, color=COLOR_TEXT_PRIMARY)
    page.task_filtered_stat = ft.Text("0", size=FONT_SIZE_XL, weight=ft.FontWeight.BOLD, color=COLOR_TEXT_PRIMARY)
    page.task_completed_stat = ft.Text("0", size=FONT_SIZE_XL, weight=ft.FontWeight.BOLD, color=COLOR_TEXT_PRIMARY)

    page.task_search = ft.TextField(
        hint_text="Search tasks...",
        prefix_icon=ft.Icons.SEARCH,
        border_radius=12,
        filled=True,
        bgcolor=COLOR_INPUT_BG,
        color=COLOR_TEXT_PRIMARY,
        expand=True,
        on_change=lambda e: _reload_tasks(page, user_id),
    )
    page.task_status = ft.Dropdown(
        options=[ft.dropdown.Option(key="all", text="All Statuses")] + [
            ft.dropdown.Option(key=value, text=label) for value, label in STATUS_OPTIONS
        ],
        value="all",
        border_radius=12,
        filled=True,
        bgcolor=COLOR_INPUT_BG,
        color=COLOR_TEXT_PRIMARY,
        width=220,
        on_select=lambda e: _reload_tasks(page, user_id),
    )
    page.task_category = ft.Dropdown(
        options=[ft.dropdown.Option(key="all", text="All Categories")] + [
            ft.dropdown.Option(key=value, text=label) for value, label in CATEGORY_OPTIONS
        ],
        value="all",
        border_radius=12,
        filled=True,
        bgcolor=COLOR_INPUT_BG,
        color=COLOR_TEXT_PRIMARY,
        width=220,
        on_select=lambda e: _reload_tasks(page, user_id),
    )

    _load_tasks(page, tasks_list, user_id, update_page=False)

    title_block = ft.Column(
        controls=[
            ft.Text("Tasks", size=FONT_SIZE_XL, weight=ft.FontWeight.BOLD, color=COLOR_TEXT_PRIMARY),
            ft.Text(
                "Track, filter and update your current work without leaving the flow.",
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
                ft.Text("Add Task", color="#0B0F14", weight=ft.FontWeight.BOLD),
            ],
            spacing=8,
            tight=True,
        ),
        on_click=lambda e: open_add_dialog(page, user_id),
    )

    filters_row = ft.Row(
        controls=[page.task_search, page.task_status, page.task_category],
        spacing=12,
        wrap=True,
    )
    stats_row = ft.Row(
        controls=[
            _stat_card("Total", page.task_total_stat),
            _stat_card("Visible", page.task_filtered_stat),
            _stat_card("Completed", page.task_completed_stat),
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
        content=tasks_list,
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

    return ft.View(route="/tasks", controls=[content])
