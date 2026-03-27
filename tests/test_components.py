"""Тесты для компонентов и утилит."""
import shutil
import sys
from pathlib import Path
from uuid import uuid4

import pytest

sys.path.insert(0, "src")

from database.storage import initialize_database
from utils.session import (
    clear_current_user,
    get_current_user_id,
    get_current_user_name,
    is_authenticated,
    set_current_user,
)


class FakeSession:
    """Фейковая сессия для тестов."""

    def __init__(self):
        self._data = {}

    def get(self, key):
        return self._data.get(key)

    def set(self, key, value):
        self._data[key] = value

    def contains_key(self, key):
        return key in self._data

    def remove(self, key):
        self._data.pop(key, None)


class FakePage:
    """Фейковая страница для тестов."""

    def __init__(self):
        self.session = FakeSession()


@pytest.fixture
def test_db(monkeypatch):
    """Фикстура для изолированной БД."""
    temp_dir = (Path("tests/.tmp") / uuid4().hex).resolve()
    temp_dir.mkdir(parents=True, exist_ok=True)
    database_path = temp_dir / "test_qworkspaces.db"
    monkeypatch.setenv("QWORKSPACES_DB_PATH", str(database_path))

    initialize_database()

    yield {"db_path": database_path}

    shutil.rmtree(temp_dir, ignore_errors=True)


class TestSessionUtils:
    """Тесты утилит сессии."""

    def test_set_current_user(self, test_db):
        page = FakePage()
        set_current_user(page, 42, "TestUser")

        assert page.session.get("user_id") == 42
        assert page.session.get("user_name") == "TestUser"

    def test_get_current_user_id(self, test_db):
        page = FakePage()
        page.session.set("user_id", 123)

        assert get_current_user_id(page) == 123

    def test_get_current_user_id_default(self, test_db):
        page = FakePage()

        assert get_current_user_id(page, default=999) == 999

    def test_get_current_user_name(self, test_db):
        page = FakePage()
        page.session.set("user_name", "Alice")

        assert get_current_user_name(page) == "Alice"

    def test_get_current_user_name_default(self, test_db):
        page = FakePage()

        assert get_current_user_name(page, default="Guest") == "Guest"

    def test_clear_current_user(self, test_db):
        page = FakePage()
        set_current_user(page, 42, "TestUser")

        clear_current_user(page)

        assert page.session.get("user_id") is None
        assert page.session.get("user_name") is None

    def test_is_authenticated(self, test_db):
        page = FakePage()

        assert is_authenticated(page) is False
        set_current_user(page, 42, "TestUser")
        assert is_authenticated(page) is True


class TestComponents:
    """Тесты компонентов."""

    def test_create_empty_state(self, test_db):
        from src.components.empty_state import create_empty_state
        import flet as ft

        component = create_empty_state(ft.Icons.TASK_ALT, "No tasks")

        assert isinstance(component, ft.Container)
        assert component.expand is True

    def test_create_text_field(self, test_db):
        from src.components.forms import create_text_field

        field = create_text_field(label="Test", value="Value")

        assert field.label == "Test"
        assert field.value == "Value"

    def test_create_dropdown(self, test_db):
        from src.components.forms import create_dropdown

        options = [("work", "Work"), ("home", "Home")]
        dropdown = create_dropdown(label="Category", options=options, value="work")

        assert dropdown.label == "Category"
        assert dropdown.value == "work"
        assert len(dropdown.options) == 2

    def test_create_error_text(self, test_db):
        from src.components.forms import create_error_text

        error = create_error_text("Something went wrong")

        assert error.value == "Something went wrong"

    def test_create_buttons(self, test_db):
        from src.components.forms import (
            create_cancel_button,
            create_delete_button,
            create_save_button,
        )

        def dummy_callback(e):
            return None

        cancel = create_cancel_button(dummy_callback)
        save = create_save_button(dummy_callback)
        delete = create_delete_button(dummy_callback)

        assert cancel.content == "Cancel"
        assert save.content == "Save"
        assert delete.content == "Delete"
