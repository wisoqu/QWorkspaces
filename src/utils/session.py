"""Утилиты для работы с сессией пользователя."""
import flet as ft


def get_current_user_id(page: ft.Page, default: int | None = None) -> int | None:
    """Получить ID текущего пользователя из сессии."""
    user_id = page.session.get("user_id")
    return user_id if user_id is not None else default


def get_current_user_name(page: ft.Page, default: str = "Guest") -> str:
    """Получить имя текущего пользователя из сессии."""
    user_name = page.session.get("user_name")
    return user_name if user_name is not None else default


def set_current_user(page: ft.Page, user_id: int, user_name: str) -> None:
    """Сохранить данные пользователя в сессии."""
    page.session["user_id"] = user_id
    page.session["user_name"] = user_name


def clear_current_user(page: ft.Page) -> None:
    """Очистить данные пользователя из сессии."""
    if "user_id" in page.session:
        del page.session["user_id"]
    if "user_name" in page.session:
        del page.session["user_name"]


def is_authenticated(page: ft.Page) -> bool:
    """Проверить, есть ли пользователь в сессии."""
    return "user_id" in page.session
