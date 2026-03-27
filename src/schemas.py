import re
from datetime import datetime
from enum import Enum
from pydantic import BaseModel, field_validator, ValidationError


class TaskCategory(str, Enum):
    """Категории задач."""
    WORK = "work"
    HOBBY = "hobby"
    HOME = "home"
    PERSONAL = "personal"
    OTHER = "other"


class TaskStatus(str, Enum):
    """Статусы задачи."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    OVERDUE = "overdue"


class UserName(BaseModel):
    """Схема валидации имени пользователя."""
    
    name: str

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        value = value.strip()
        
        if len(value) < 1:
            raise ValueError("Имя должно содержать хотя бы 1 символ")
        if len(value) > 25:
            raise ValueError("Имя не должно превышать 25 символов")
        
        pattern = r"^[\w\s`]+$"
        if not re.match(pattern, value, re.UNICODE):
            raise ValueError("Имя содержит недопустимые символы")
        
        return value


class UserEmail(BaseModel):
    """Схема валидации email пользователя."""

    email: str

    @field_validator("email")
    @classmethod
    def validate_email(cls, value: str) -> str:
        value = value.strip().lower()

        if len(value) < 5:
            raise ValueError("Email слишком короткий")

        pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
        if not re.match(pattern, value):
            raise ValueError("Некорректный формат email")

        return value


class UserPassword(BaseModel):
    """Схема валидации пароля пользователя."""

    password: str

    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str) -> str:
        if len(value) < 8:
            raise ValueError("Пароль должен содержать минимум 8 символов")
        if len(value) > 128:
            raise ValueError("Пароль слишком длинный")
        return value


class Task(BaseModel):
    """Схема задачи."""
    
    id: int
    title: str
    description: str = ""
    category: TaskCategory = TaskCategory.OTHER
    deadline: datetime | None = None
    status: TaskStatus = TaskStatus.PENDING
    created_at: datetime = datetime.now()

    @field_validator("title")
    @classmethod
    def validate_title(cls, value: str) -> str:
        value = value.strip()
        
        if len(value) < 1:
            raise ValueError("Заголовок не может быть пустым")
        if len(value) > 100:
            raise ValueError("Заголовок не должен превышать 100 символов")
        
        return value

    @field_validator("description")
    @classmethod
    def validate_description(cls, value: str) -> str:
        if len(value) > 1000:
            raise ValueError("Описание не должно превышать 1000 символов")
        return value


class Note(BaseModel):
    """Схема заметки."""
    
    id: int
    content: str
    created_at: datetime = datetime.now()

    @field_validator("content")
    @classmethod
    def validate_content(cls, value: str) -> str:
        value = value.strip()
        
        if len(value) < 1:
            raise ValueError("Заметка не может быть пустой")
        if len(value) > 5000:
            raise ValueError("Заметка не должна превышать 5000 символов")
        
        return value


def validate_user_name(name: str) -> tuple[str | None, str | None]:
    """
    Валидирует имя пользователя.
    
    Returns:
        (normalized_name, error_message):
        - если успешно: (имя, None)
        - если ошибка: (None, сообщение_об_ошибке)
    """
    try:
        user = UserName(name=name)
        return user.name, None
    except ValidationError as e:
        return None, e.errors()[0]["msg"]


def validate_user_email(email: str) -> tuple[str | None, str | None]:
    """Валидирует email пользователя."""
    try:
        user_email = UserEmail(email=email)
        return user_email.email, None
    except ValidationError as e:
        return None, e.errors()[0]["msg"]


def validate_user_password(password: str) -> tuple[str | None, str | None]:
    """Валидирует пароль пользователя."""
    try:
        user_password = UserPassword(password=password)
        return user_password.password, None
    except ValidationError as e:
        return None, e.errors()[0]["msg"]


def validate_task(title: str, description: str = "") -> tuple[dict | None, str | None]:
    """
    Валидирует задачу.
    
    Returns:
        (task_data, error_message)
    """
    try:
        task = Task(
            id=0,  # Будет заменено на реальный ID
            title=title,
            description=description,
        )
        return {
            "title": task.title,
            "description": task.description,
            "category": task.category.value,
            "status": task.status.value,
        }, None
    except ValidationError as e:
        return None, e.errors()[0]["msg"]


def validate_note(content: str) -> tuple[str | None, str | None]:
    """
    Валидирует заметку.
    
    Returns:
        (content, error_message)
    """
    try:
        note = Note(id=0, content=content)
        return note.content, None
    except ValidationError as e:
        return None, e.errors()[0]["msg"]
