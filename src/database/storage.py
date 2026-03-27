import hashlib
import hmac
import os
import secrets
import sqlite3
from datetime import datetime, timezone
from pathlib import Path


DATABASE_FILE_NAME = "qworkspaces.db"
PASSWORD_HASH_ALGORITHM = "pbkdf2_sha256"
PASSWORD_HASH_ITERATIONS = 100_000


def get_database_path() -> Path:
    env_path = os.getenv("QWORKSPACES_DB_PATH")
    if env_path:
        return Path(env_path).expanduser().resolve()

    return Path(__file__).resolve().parent / "data" / DATABASE_FILE_NAME


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _normalize_email(email: str) -> str:
    return email.strip().lower()


def _row_to_dict(row: sqlite3.Row | None) -> dict | None:
    if row is None:
        return None

    return dict(row)


def get_connection() -> sqlite3.Connection:
    database_path = get_database_path()
    database_path.parent.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(database_path)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def initialize_database() -> Path:
    with get_connection() as connection:
        connection.executescript(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                login TEXT NOT NULL COLLATE NOCASE UNIQUE,
                email TEXT COLLATE NOCASE UNIQUE,
                password_hash TEXT NOT NULL,
                role TEXT NOT NULL DEFAULT 'free',
                subscription_plan TEXT NOT NULL DEFAULT 'free',
                company_name TEXT,
                is_active INTEGER NOT NULL DEFAULT 1,
                is_deleted INTEGER NOT NULL DEFAULT 0,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                last_login_at TEXT,
                deleted_at TEXT
            );

            CREATE TABLE IF NOT EXISTS app_session (
                id INTEGER PRIMARY KEY CHECK (id = 1),
                user_id INTEGER,
                session_token TEXT NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                expires_at TEXT,
                FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE SET NULL
            );

            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                title TEXT NOT NULL,
                description TEXT,
                category TEXT NOT NULL DEFAULT 'other',
                deadline TEXT,
                status TEXT NOT NULL DEFAULT 'pending',
                is_deleted INTEGER NOT NULL DEFAULT 0,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                deleted_at TEXT,
                FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
            );

            CREATE TABLE IF NOT EXISTS notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                title TEXT NOT NULL,
                content TEXT,
                category TEXT NOT NULL DEFAULT 'other',
                is_deleted INTEGER NOT NULL DEFAULT 0,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                deleted_at TEXT,
                FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
            );
            """
        )

    return get_database_path()


def create_user(
    login: str,
    password_hash: str,
    email: str | None = None,
    role: str = "free",
    subscription_plan: str = "free",
    company_name: str | None = None,
) -> int:
    now = _utc_now()
    normalized_login = login.strip()
    normalized_email = _normalize_email(email) if email else None

    with get_connection() as connection:
        try:
            cursor = connection.execute(
                """
                INSERT INTO users (
                    login,
                    email,
                    password_hash,
                    role,
                    subscription_plan,
                    company_name,
                    created_at,
                    updated_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    normalized_login,
                    normalized_email,
                    password_hash,
                    role,
                    subscription_plan,
                    company_name.strip() if company_name else None,
                    now,
                    now,
                ),
            )
        except sqlite3.IntegrityError as error:
            message = str(error).lower()
            if "users.login" in message:
                raise ValueError("User with this login already exists.") from error
            if "users.email" in message:
                raise ValueError("User with this email already exists.") from error
            raise

    return int(cursor.lastrowid)


def hash_password(password: str) -> str:
    salt = secrets.token_hex(16)
    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        bytes.fromhex(salt),
        PASSWORD_HASH_ITERATIONS,
    ).hex()
    return f"{PASSWORD_HASH_ALGORITHM}${PASSWORD_HASH_ITERATIONS}${salt}${password_hash}"


def verify_password(password: str, stored_password_hash: str) -> bool:
    try:
        algorithm, iterations, salt, password_hash = stored_password_hash.split("$", 3)
    except ValueError:
        return False

    if algorithm != PASSWORD_HASH_ALGORITHM:
        return False

    calculated_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        bytes.fromhex(salt),
        int(iterations),
    ).hex()
    return hmac.compare_digest(password_hash, calculated_hash)


def register_user(
    login: str,
    email: str,
    password: str,
    role: str = "free",
    subscription_plan: str = "free",
    company_name: str | None = None,
) -> int:
    return create_user(
        login=login,
        email=email,
        password_hash=hash_password(password),
        role=role,
        subscription_plan=subscription_plan,
        company_name=company_name,
    )


def get_user_by_login(login: str) -> dict | None:
    with get_connection() as connection:
        row = connection.execute(
            "SELECT * FROM users WHERE login = ? AND is_deleted = 0",
            (login.strip(),),
        ).fetchone()

    return _row_to_dict(row)


def get_user_by_email(email: str) -> dict | None:
    with get_connection() as connection:
        row = connection.execute(
            "SELECT * FROM users WHERE email = ? AND is_deleted = 0",
            (_normalize_email(email),),
        ).fetchone()

    return _row_to_dict(row)


def authenticate_user(email: str, password: str) -> dict | None:
    user = get_user_by_email(email)
    if not user:
        return None

    if not user["is_active"] or user["is_deleted"]:
        return None

    if not verify_password(password, user["password_hash"]):
        return None

    update_last_login(user["id"])
    return get_user_by_id(user["id"])


def get_user_by_id(user_id: int) -> dict | None:
    with get_connection() as connection:
        row = connection.execute(
            "SELECT * FROM users WHERE id = ? AND is_deleted = 0",
            (user_id,),
        ).fetchone()

    return _row_to_dict(row)


def update_last_login(user_id: int) -> None:
    now = _utc_now()

    with get_connection() as connection:
        connection.execute(
            """
            UPDATE users
            SET last_login_at = ?, updated_at = ?
            WHERE id = ? AND is_deleted = 0
            """,
            (now, now, user_id),
        )


def soft_delete_user(user_id: int) -> None:
    now = _utc_now()

    with get_connection() as connection:
        connection.execute(
            """
            UPDATE users
            SET is_active = 0,
                is_deleted = 1,
                deleted_at = ?,
                updated_at = ?
            WHERE id = ? AND is_deleted = 0
            """,
            (now, now, user_id),
        )
        connection.execute(
            "UPDATE app_session SET user_id = NULL, updated_at = ? WHERE user_id = ?",
            (now, user_id),
        )


def save_active_session(
    user_id: int,
    session_token: str,
    expires_at: str | None = None,
) -> None:
    now = _utc_now()

    with get_connection() as connection:
        connection.execute(
            """
            INSERT INTO app_session (
                id,
                user_id,
                session_token,
                created_at,
                updated_at,
                expires_at
            )
            VALUES (1, ?, ?, ?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET
                user_id = excluded.user_id,
                session_token = excluded.session_token,
                updated_at = excluded.updated_at,
                expires_at = excluded.expires_at
            """,
            (user_id, session_token, now, now, expires_at),
        )


def start_user_session(user_id: int) -> str:
    session_token = secrets.token_urlsafe(32)
    save_active_session(user_id=user_id, session_token=session_token)
    return session_token


def get_active_session() -> dict | None:
    with get_connection() as connection:
        row = connection.execute(
            """
            SELECT
                app_session.id,
                app_session.user_id,
                app_session.session_token,
                app_session.created_at,
                app_session.updated_at,
                app_session.expires_at,
                users.login,
                users.email,
                users.role,
                users.subscription_plan,
                users.company_name
            FROM app_session
            LEFT JOIN users ON users.id = app_session.user_id
            WHERE app_session.id = 1
            """
        ).fetchone()

    return _row_to_dict(row)


def clear_active_session() -> None:
    with get_connection() as connection:
        connection.execute("DELETE FROM app_session WHERE id = 1")


# ==================== TASKS ====================

def create_task(
    user_id: int,
    title: str,
    description: str = "",
    category: str = "other",
    deadline: str | None = None,
    status: str = "pending",
) -> int:
    now = _utc_now()

    with get_connection() as connection:
        cursor = connection.execute(
            """
            INSERT INTO tasks (
                user_id, title, description, category, deadline, status,
                created_at, updated_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                user_id,
                title.strip(),
                description.strip(),
                category,
                deadline,
                status,
                now,
                now,
            ),
        )

    return int(cursor.lastrowid)


def get_tasks(user_id: int, include_deleted: bool = False) -> list[dict]:
    query = "SELECT * FROM tasks WHERE user_id = ?"
    if not include_deleted:
        query += " AND is_deleted = 0"
    query += " ORDER BY created_at DESC"

    with get_connection() as connection:
        rows = connection.execute(query, (user_id,)).fetchall()

    return [_row_to_dict(row) for row in rows]


def get_task(task_id: int, user_id: int) -> dict | None:
    with get_connection() as connection:
        row = connection.execute(
            "SELECT * FROM tasks WHERE id = ? AND user_id = ? AND is_deleted = 0",
            (task_id, user_id),
        ).fetchone()

    return _row_to_dict(row)


def update_task(
    task_id: int,
    user_id: int,
    title: str | None = None,
    description: str | None = None,
    category: str | None = None,
    deadline: str | None = None,
    status: str | None = None,
) -> None:
    now = _utc_now()
    updates = []
    values = []

    if title is not None:
        updates.append("title = ?")
        values.append(title.strip())
    if description is not None:
        updates.append("description = ?")
        values.append(description.strip())
    if category is not None:
        updates.append("category = ?")
        values.append(category)
    if deadline is not None:
        updates.append("deadline = ?")
        values.append(deadline)
    if status is not None:
        updates.append("status = ?")
        values.append(status)

    if not updates:
        return

    updates.append("updated_at = ?")
    values.append(now)
    values.append(task_id)
    values.append(user_id)

    with get_connection() as connection:
        connection.execute(
            f"UPDATE tasks SET {', '.join(updates)} WHERE id = ? AND user_id = ?",
            values,
        )


def delete_task(task_id: int, user_id: int, hard: bool = False) -> None:
    now = _utc_now()

    with get_connection() as connection:
        if hard:
            connection.execute(
                "DELETE FROM tasks WHERE id = ? AND user_id = ?",
                (task_id, user_id),
            )
        else:
            connection.execute(
                """
                UPDATE tasks
                SET is_deleted = 1, deleted_at = ?, updated_at = ?
                WHERE id = ? AND user_id = ? AND is_deleted = 0
                """,
                (now, now, task_id, user_id),
            )


# ==================== NOTES ====================

def create_note(
    user_id: int,
    title: str,
    content: str = "",
    category: str = "other",
) -> int:
    now = _utc_now()

    with get_connection() as connection:
        cursor = connection.execute(
            """
            INSERT INTO notes (user_id, title, content, category, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (user_id, title.strip(), content.strip(), category, now, now),
        )

    return int(cursor.lastrowid)


def get_notes(user_id: int, include_deleted: bool = False) -> list[dict]:
    query = "SELECT * FROM notes WHERE user_id = ?"
    if not include_deleted:
        query += " AND is_deleted = 0"
    query += " ORDER BY created_at DESC"

    with get_connection() as connection:
        rows = connection.execute(query, (user_id,)).fetchall()

    return [_row_to_dict(row) for row in rows]


def get_note(note_id: int, user_id: int) -> dict | None:
    with get_connection() as connection:
        row = connection.execute(
            "SELECT * FROM notes WHERE id = ? AND user_id = ? AND is_deleted = 0",
            (note_id, user_id),
        ).fetchone()

    return _row_to_dict(row)


def update_note(
    note_id: int,
    user_id: int,
    title: str | None = None,
    content: str | None = None,
    category: str | None = None,
) -> None:
    now = _utc_now()
    updates = []
    values = []

    if title is not None:
        updates.append("title = ?")
        values.append(title.strip())
    if content is not None:
        updates.append("content = ?")
        values.append(content.strip())
    if category is not None:
        updates.append("category = ?")
        values.append(category)

    if not updates:
        return

    updates.append("updated_at = ?")
    values.append(now)
    values.append(note_id)
    values.append(user_id)

    with get_connection() as connection:
        connection.execute(
            f"UPDATE notes SET {', '.join(updates)} WHERE id = ? AND user_id = ?",
            values,
        )


def delete_note(note_id: int, user_id: int, hard: bool = False) -> None:
    now = _utc_now()

    with get_connection() as connection:
        if hard:
            connection.execute(
                "DELETE FROM notes WHERE id = ? AND user_id = ?",
                (note_id, user_id),
            )
        else:
            connection.execute(
                """
                UPDATE notes
                SET is_deleted = 1, deleted_at = ?, updated_at = ?
                WHERE id = ? AND user_id = ? AND is_deleted = 0
                """,
                (now, now, note_id, user_id),
            )
