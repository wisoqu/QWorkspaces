"""Утилиты для работы с сессией пользователя."""
from typing import Any, Protocol

import flet as ft


class SessionStoreProtocol(Protocol):
    def get(self, key: str) -> Any:
        ...

    def set(self, key: str, value: Any) -> None:
        ...

    def remove(self, key: str) -> None:
        ...


def _get_session_store(page: ft.Page) -> SessionStoreProtocol:
    """Вернуть хранилище данных сессии для текущей версии Flet."""
    session = page.session
    return getattr(session, "store", session)


def get_current_user_id(page: ft.Page, default: int | None = None) -> int | None:
    """Получить ID текущего пользователя из сессии."""
    user_id = _get_session_store(page).get("user_id")
    return user_id if user_id is not None else default


def get_current_user_name(page: ft.Page, default: str = "Guest") -> str:
    """Получить имя текущего пользователя из сессии."""
    user_name = _get_session_store(page).get("user_name")
    return user_name if user_name is not None else default


def set_current_user(page: ft.Page, user_id: int, user_name: str) -> None:
    """Сохранить данные пользователя в сессии."""
    session_store = _get_session_store(page)
    session_store.set("user_id", user_id)
    session_store.set("user_name", user_name)


def clear_current_user(page: ft.Page) -> None:
    """Очистить данные пользователя из сессии."""
    session_store = _get_session_store(page)
    for key in ("user_id", "user_name"):
        if session_store.get(key) is not None:
            session_store.remove(key)


def is_authenticated(page: ft.Page) -> bool:
    """Проверить, есть ли пользователь в сессии."""
    return _get_session_store(page).get("user_id") is not None
