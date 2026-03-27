"""
Тесты CRUD операций для задач и заметок.
"""
import sys
from pathlib import Path
from uuid import uuid4

import pytest

sys.path.insert(0, "src")

from database.storage import (
    clear_active_session,
    create_note,
    create_task,
    create_user,
    delete_note,
    delete_task,
    get_note,
    get_notes,
    get_task,
    get_tasks,
    initialize_database,
    save_active_session,
    update_note,
    update_task,
)


@pytest.fixture
def test_db(monkeypatch):
    """Фикстура для изолированной БД."""
    temp_dir = (Path("tests/.tmp") / uuid4().hex).resolve()
    temp_dir.mkdir(parents=True, exist_ok=True)
    database_path = temp_dir / "test_qworkspaces.db"
    monkeypatch.setenv("QWORKSPACES_DB_PATH", str(database_path))
    
    initialize_database()
    
    # Создаем тестового пользователя
    user_id = create_user(login="testuser", email="test@test.com", password_hash="hash")
    save_active_session(user_id, "token")
    
    yield {"db_path": database_path, "user_id": user_id}
    
    # Cleanup
    import shutil
    shutil.rmtree(temp_dir, ignore_errors=True)


class TestTasks:
    """Тесты для задач."""

    def test_create_task(self, test_db):
        """Создание задачи."""
        task_id = create_task(
            user_id=test_db["user_id"],
            title="Test Task",
            description="Test Description",
            category="work",
        )
        
        assert task_id > 0

    def test_get_tasks(self, test_db):
        """Получение списка задач."""
        create_task(test_db["user_id"], "Task 1", "Desc 1", "work")
        create_task(test_db["user_id"], "Task 2", "Desc 2", "hobby")
        
        tasks = get_tasks(test_db["user_id"])
        
        assert len(tasks) == 2
        assert tasks[0]["title"] == "Task 2"  # ORDER BY created_at DESC

    def test_get_task(self, test_db):
        """Получение одной задачи."""
        task_id = create_task(test_db["user_id"], "Single Task", "Desc", "home")
        
        task = get_task(task_id, test_db["user_id"])
        
        assert task is not None
        assert task["title"] == "Single Task"

    def test_update_task(self, test_db):
        """Обновление задачи."""
        task_id = create_task(test_db["user_id"], "Old Title", "Old Desc", "work")
        
        update_task(task_id, test_db["user_id"], title="New Title", status="completed")
        
        task = get_task(task_id, test_db["user_id"])
        assert task["title"] == "New Title"
        assert task["status"] == "completed"

    def test_delete_task_soft(self, test_db):
        """Soft delete задачи."""
        task_id = create_task(test_db["user_id"], "To Delete", "Desc", "work")
        
        delete_task(task_id, test_db["user_id"])
        
        task = get_task(task_id, test_db["user_id"])
        assert task is None  # Не возвращается в get_task
        
        # Но в БД есть с is_deleted=1
        tasks_all = get_tasks(test_db["user_id"], include_deleted=True)
        assert len(tasks_all) == 1
        assert tasks_all[0]["is_deleted"] == 1

    def test_delete_task_hard(self, test_db):
        """Hard delete задачи."""
        task_id = create_task(test_db["user_id"], "To Delete Hard", "Desc", "work")
        
        delete_task(task_id, test_db["user_id"], hard=True)
        
        tasks = get_tasks(test_db["user_id"], include_deleted=True)
        assert len(tasks) == 0


class TestNotes:
    """Тесты для заметок."""

    def test_create_note(self, test_db):
        """Создание заметки."""
        note_id = create_note(
            user_id=test_db["user_id"],
            title="Test Note",
            content="Test Content",
            category="personal",
        )
        
        assert note_id > 0

    def test_get_notes(self, test_db):
        """Получение списка заметок."""
        create_note(test_db["user_id"], "Note 1", "Content 1", "work")
        create_note(test_db["user_id"], "Note 2", "Content 2", "hobby")
        
        notes = get_notes(test_db["user_id"])
        
        assert len(notes) == 2
        assert notes[0]["title"] == "Note 2"  # ORDER BY created_at DESC

    def test_get_note(self, test_db):
        """Получение одной заметки."""
        note_id = create_note(test_db["user_id"], "Single Note", "Content", "home")
        
        note = get_note(note_id, test_db["user_id"])
        
        assert note is not None
        assert note["title"] == "Single Note"

    def test_update_note(self, test_db):
        """Обновление заметки."""
        note_id = create_note(test_db["user_id"], "Old Title", "Old Content", "work")
        
        update_note(note_id, test_db["user_id"], title="New Title", category="personal")
        
        note = get_note(note_id, test_db["user_id"])
        assert note["title"] == "New Title"
        assert note["category"] == "personal"

    def test_delete_note_soft(self, test_db):
        """Soft delete заметки."""
        note_id = create_note(test_db["user_id"], "To Delete", "Content", "work")
        
        delete_note(note_id, test_db["user_id"])
        
        note = get_note(note_id, test_db["user_id"])
        assert note is None  # Не возвращается в get_note

    def test_delete_note_hard(self, test_db):
        """Hard delete заметки."""
        note_id = create_note(test_db["user_id"], "To Delete Hard", "Content", "work")
        
        delete_note(note_id, test_db["user_id"], hard=True)
        
        notes = get_notes(test_db["user_id"], include_deleted=True)
        assert len(notes) == 0
