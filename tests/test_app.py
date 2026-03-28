"""
Интеграционные тесты приложения.
Проверяют импорты и базовый дымовой сценарий роутинга.
"""
import shutil
import sys
from pathlib import Path
from uuid import uuid4

sys.path.insert(0, "src")


class FakeSessionStore:
    def __init__(self):
        self._data = {}

    def get(self, key, default=None):
        return self._data.get(key, default)

    def set(self, key, value):
        self._data[key] = value

    def remove(self, key):
        self._data.pop(key, None)


class FakeSession:
    def __init__(self):
        self.store = FakeSessionStore()


class FakePage:
    def __init__(self):
        self.session = FakeSession()
        self.route = ""
        self.views = []
        self.on_route_change = None
        self.on_view_pop = None
        self.dialog = None
        self.title = None
        self.theme_mode = None
        self.bgcolor = None
        self.padding = None
        self.updated = False
        self.update_calls = 0

    def update(self):
        self.updated = True
        self.update_calls += 1

    def go(self, route):
        self.route = route
        if self.on_route_change:
            self.on_route_change(type("RouteChangeEvent", (), {"route": route})())

    def show_dialog(self, dialog):
        self.dialog = dialog
        dialog.open = True

    def pop_dialog(self):
        if self.dialog is not None:
            self.dialog.open = False

    def close_dialog(self):
        self.pop_dialog()


class ReadOnlyRoutePage:
    def __init__(self):
        self.session = FakeSession()
        self._route = ""
        self.views = []
        self.on_route_change = None
        self.on_view_pop = None
        self.dialog = None
        self.title = None
        self.theme_mode = None
        self.bgcolor = None
        self.padding = None
        self.updated = False
        self.update_calls = 0

    @property
    def route(self):
        return self._route

    def update(self):
        self.updated = True
        self.update_calls += 1

    def go(self, route):
        self._route = route
        if self.on_route_change:
            self.on_route_change(type("RouteChangeEvent", (), {"route": route})())

    def show_dialog(self, dialog):
        self.dialog = dialog
        dialog.open = True

    def pop_dialog(self):
        if self.dialog is not None:
            self.dialog.open = False


class TestAppImports:
    def test_import_main(self):
        from src import main

        assert main is not None

    def test_import_config(self):
        from src import config

        assert config.PAGE_TITLE == "QWorkspaces"

    def test_import_schemas(self):
        from src import schemas

        assert schemas.UserName is not None

    def test_import_database(self):
        from src.database import create_user, get_user_by_email

        assert create_user is not None
        assert get_user_by_email is not None

    def test_import_components(self):
        from src.components import create_empty_state, create_note_card, create_task_card

        assert create_task_card is not None
        assert create_note_card is not None
        assert create_empty_state is not None

    def test_import_utils(self):
        from src.utils import get_current_user_id, get_current_user_name

        assert get_current_user_id is not None
        assert get_current_user_name is not None


class TestScreensImports:
    def test_import_hello_screen(self):
        from src.screens.auth.hello import hello_screen

        assert hello_screen is not None

    def test_import_home_screen(self):
        from src.screens.main.home import home_screen

        assert home_screen is not None

    def test_import_tasks_screen(self):
        from src.screens.tasks.tasks_list import tasks_screen

        assert tasks_screen is not None

    def test_import_notes_screen(self):
        from src.screens.notes.notes_list import notes_screen

        assert notes_screen is not None

    def test_import_agent_screen(self):
        from src.screens.main.agent import agent_screen

        assert agent_screen is not None

    def test_import_calendar_screen(self):
        from src.screens.calendar.calendar import calendar_screen

        assert calendar_screen is not None


class TestFormsImports:
    def test_import_task_form(self):
        from src.screens.tasks.task_form import task_form_dialog

        assert task_form_dialog is not None

    def test_import_note_form(self):
        from src.screens.notes.note_form import note_form_dialog

        assert note_form_dialog is not None

    def test_task_form_opens_dialog(self, monkeypatch):
        temp_dir = (Path("tests/.tmp") / uuid4().hex).resolve()
        temp_dir.mkdir(parents=True, exist_ok=True)
        monkeypatch.setenv("QWORKSPACES_DB_PATH", str(temp_dir / "app.db"))

        from src.database import create_user, initialize_database
        from src.screens.tasks.task_form import task_form_dialog

        try:
            initialize_database()
            user_id = create_user(email="task@example.com", password_hash="hash")
            page = FakePage()

            task_form_dialog(page, task_id=None, user_id=user_id, on_save=lambda: None)

            assert page.dialog is not None
            assert page.dialog.open is True
        finally:
            shutil.rmtree(temp_dir, ignore_errors=True)

    def test_note_form_opens_dialog(self, monkeypatch):
        temp_dir = (Path("tests/.tmp") / uuid4().hex).resolve()
        temp_dir.mkdir(parents=True, exist_ok=True)
        monkeypatch.setenv("QWORKSPACES_DB_PATH", str(temp_dir / "app.db"))

        from src.database import create_user, initialize_database
        from src.screens.notes.note_form import note_form_dialog

        try:
            initialize_database()
            user_id = create_user(email="note@example.com", password_hash="hash")
            page = FakePage()

            note_form_dialog(page, note_id=None, user_id=user_id, on_save=lambda: None)

            assert page.dialog is not None
            assert page.dialog.open is True
        finally:
            shutil.rmtree(temp_dir, ignore_errors=True)


class TestAppStartup:
    def test_main_function_exists(self):
        from src.main import main

        assert callable(main)

    def test_ft_run_exists(self):
        import flet as ft

        assert hasattr(ft, "run")

    def test_hello_screen_does_not_update_page_during_build(self):
        from src.screens.auth.hello import hello_screen

        page = FakePage()
        view = hello_screen(page)

        assert view.route == "/"
        assert page.update_calls == 0

    def test_tasks_screen_does_not_update_page_during_build(self):
        from src.screens.tasks.tasks_list import tasks_screen

        page = FakePage()
        view = tasks_screen(page)

        assert view.route == "/tasks"
        assert page.update_calls == 0

    def test_notes_screen_does_not_update_page_during_build(self):
        from src.screens.notes.notes_list import notes_screen

        page = FakePage()
        view = notes_screen(page)

        assert view.route == "/notes"
        assert page.update_calls == 0

    def test_main_builds_login_view_without_session(self, monkeypatch):
        temp_dir = (Path("tests/.tmp") / uuid4().hex).resolve()
        temp_dir.mkdir(parents=True, exist_ok=True)
        monkeypatch.setenv("QWORKSPACES_DB_PATH", str(temp_dir / "app.db"))

        from src.main import main

        try:
            page = FakePage()
            main(page)

            assert len(page.views) == 1
            assert page.views[0].route == "/"
        finally:
            shutil.rmtree(temp_dir, ignore_errors=True)

    def test_main_restores_persistent_session_and_redirects_home(self, monkeypatch):
        temp_dir = (Path("tests/.tmp") / uuid4().hex).resolve()
        temp_dir.mkdir(parents=True, exist_ok=True)
        monkeypatch.setenv("QWORKSPACES_DB_PATH", str(temp_dir / "app.db"))

        import flet as ft
        from src.database import create_user, initialize_database, save_active_session
        from src.main import main

        try:
            initialize_database()
            user_id = create_user(
                email="alice@example.com",
                password_hash="hash",
            )
            save_active_session(user_id, "token-123")

            page = FakePage()
            page.route = "/"  # Имитируем начальную маршрутизацию
            main(page)

            assert page.route == "/home"
            assert len(page.views) == 1
            assert page.views[0].route == "/home"
            assert not isinstance(page.views[0].controls[0].controls[1], ft.View)
            assert page.session.store.get("user_id") == user_id
            assert page.session.store.get("user_name") == "alice@example.com"
        finally:
            shutil.rmtree(temp_dir, ignore_errors=True)

    def test_main_restores_session_with_read_only_route_page(self, monkeypatch):
        temp_dir = (Path("tests/.tmp") / uuid4().hex).resolve()
        temp_dir.mkdir(parents=True, exist_ok=True)
        monkeypatch.setenv("QWORKSPACES_DB_PATH", str(temp_dir / "app.db"))

        from src.database import create_user, initialize_database, save_active_session
        from src.main import main

        try:
            initialize_database()
            user_id = create_user(
                email="readonly@example.com",
                password_hash="hash",
            )
            save_active_session(user_id, "token-456")

            page = ReadOnlyRoutePage()
            main(page)

            assert page.route == "/home"
            assert len(page.views) == 1
            assert page.views[0].route == "/home"
            assert page.session.store.get("user_id") == user_id
        finally:
            shutil.rmtree(temp_dir, ignore_errors=True)
