"""
Тесты валидации данных и схем.
UI-тесты ограничены в Flet без полноценного запуска приложения.
"""
import sys

sys.path.insert(0, "src")

from schemas import (
    validate_note,
    validate_task,
    validate_user_email,
    validate_user_name,
    validate_user_password,
)


def test_user_name_validation_empty():
    validated, error = validate_user_name("")
    assert error is not None


def test_user_name_validation_valid():
    validated, error = validate_user_name("Иван")
    assert error is None
    assert validated == "Иван"


def test_user_name_validation_special_chars():
    validated, error = validate_user_name("Test@123")
    assert error is not None


def test_user_name_validation_underscore():
    validated, error = validate_user_name("Anna_Maria")
    assert error is None


def test_user_name_validation_backtick():
    validated, error = validate_user_name("O`Brien")
    assert error is None


def test_user_name_validation_too_long():
    validated, error = validate_user_name("A" * 26)
    assert error is not None


def test_user_name_validation_with_spaces():
    validated, error = validate_user_name("Иван Петров")
    assert error is None


def test_user_email_validation_valid():
    validated, error = validate_user_email("Alice@Example.com")
    assert error is None
    assert validated == "alice@example.com"


def test_user_email_validation_invalid():
    validated, error = validate_user_email("alice-at-example.com")
    assert validated is None
    assert error is not None


def test_user_password_validation_valid():
    validated, error = validate_user_password("strongpass123")
    assert error is None
    assert validated == "strongpass123"


def test_user_password_validation_too_short():
    validated, error = validate_user_password("short")
    assert validated is None
    assert error is not None


def test_task_validation():
    task_data, error = validate_task("Test Task", "Description")
    assert error is None
    assert task_data["title"] == "Test Task"


def test_task_validation_empty_title():
    task_data, error = validate_task("")
    assert error is not None


def test_note_validation():
    content, error = validate_note("Test note content")
    assert error is None
    assert content == "Test note content"


def test_note_validation_empty():
    content, error = validate_note("")
    assert error is not None
