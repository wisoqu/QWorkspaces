import shutil
import sys
from pathlib import Path
from uuid import uuid4

import pytest

sys.path.insert(0, "src")

from database.storage import (
    authenticate_user,
    clear_active_session,
    create_user,
    get_active_session,
    get_user_by_email,
    get_user_by_login,
    hash_password,
    initialize_database,
    register_user,
    save_active_session,
    soft_delete_user,
    start_user_session,
    update_last_login,
    verify_password,
)


@pytest.fixture
def isolated_database(monkeypatch):
    temp_dir = (Path("tests/.tmp") / uuid4().hex).resolve()
    temp_dir.mkdir(parents=True, exist_ok=True)
    database_path = temp_dir / "test_qworkspaces.db"
    monkeypatch.setenv("QWORKSPACES_DB_PATH", str(database_path))
    yield database_path
    shutil.rmtree(temp_dir, ignore_errors=True)


def test_initialize_database_creates_file_and_tables(isolated_database):
    database_path = initialize_database()

    assert database_path == isolated_database
    assert database_path.exists()


def test_create_user_and_fetch_by_login(isolated_database):
    initialize_database()

    user_id = create_user(
        login="alice",
        email="alice@example.com",
        password_hash="hashed-password",
    )
    user = get_user_by_login("alice")

    assert user_id > 0
    assert user is not None
    assert user["id"] == user_id
    assert user["email"] == "alice@example.com"
    assert user["role"] == "free"
    assert user["subscription_plan"] == "free"


def test_create_user_rejects_duplicate_login(isolated_database):
    initialize_database()
    create_user(login="alice", email="alice@example.com", password_hash="hash-1")

    with pytest.raises(ValueError, match="login"):
        create_user(login="alice", email="other@example.com", password_hash="hash-2")


def test_save_and_clear_active_session(isolated_database):
    initialize_database()
    user_id = create_user(login="bob", email="bob@example.com", password_hash="hash")

    save_active_session(user_id=user_id, session_token="token-123")
    session = get_active_session()

    assert session is not None
    assert session["user_id"] == user_id
    assert session["login"] == "bob"

    clear_active_session()

    assert get_active_session() is None


def test_soft_delete_user_marks_user_deleted_and_clears_session(isolated_database):
    initialize_database()
    user_id = create_user(login="carol", email="carol@example.com", password_hash="hash")
    save_active_session(user_id=user_id, session_token="token-456")
    update_last_login(user_id)

    soft_delete_user(user_id)
    user = get_user_by_login("carol")
    session = get_active_session()

    assert user is None
    assert session is not None
    assert session["user_id"] is None


def test_hash_password_and_verify_password():
    password_hash = hash_password("strongpass123")

    assert password_hash.startswith("pbkdf2_sha256$")
    assert verify_password("strongpass123", password_hash) is True
    assert verify_password("wrongpass123", password_hash) is False


def test_register_user_hashes_password_and_authenticates(isolated_database):
    initialize_database()

    user_id = register_user(
        login="alice",
        email="Alice@Example.com",
        password="strongpass123",
    )
    stored_user = get_user_by_email("alice@example.com")
    authenticated_user = authenticate_user("alice@example.com", "strongpass123")

    assert user_id > 0
    assert stored_user is not None
    assert stored_user["password_hash"] != "strongpass123"
    assert authenticated_user is not None
    assert authenticated_user["id"] == user_id
    assert authenticated_user["email"] == "alice@example.com"


def test_authenticate_user_rejects_invalid_password(isolated_database):
    initialize_database()
    register_user(login="alice", email="alice@example.com", password="strongpass123")

    assert authenticate_user("alice@example.com", "wrongpass123") is None


def test_start_user_session_saves_active_session(isolated_database):
    initialize_database()
    user_id = create_user(login="bob", email="bob@example.com", password_hash="hash")

    session_token = start_user_session(user_id)
    session = get_active_session()

    assert session_token
    assert session is not None
    assert session["user_id"] == user_id
    assert session["session_token"] == session_token
