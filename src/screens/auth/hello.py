"""Приветственный экран / вход."""
import sys
from pathlib import Path

import flet as ft


# Добавляем src в sys.path для корректных импортов
src_path = Path(__file__).resolve().parent.parent.parent
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

from config import (
    CARD_BORDER_RADIUS,
    COLOR_ACCENT,
    COLOR_BG_PRIMARY,
    COLOR_BG_SECONDARY,
    COLOR_CARD_BG,
    COLOR_TEXT_ERROR,
    COLOR_TEXT_PRIMARY,
    COLOR_TEXT_SECONDARY,
    COLOR_TEXT_SUCCESS,
    FONT_SIZE_BASE,
    FONT_SIZE_SM,
    FONT_SIZE_XL,
    SPACING_SM,
)
from database import authenticate_user, get_user_by_id, register_user, start_user_session
from schemas import validate_user_email, validate_user_name, validate_user_password
from utils.session import set_current_user


def hello_screen(page: ft.Page) -> ft.View:
    """Экран регистрации и входа."""
    is_register_mode = {"value": False}

    message = ft.Text(
        "Sign in to continue",
        size=FONT_SIZE_SM,
        color=COLOR_TEXT_SECONDARY,
        text_align=ft.TextAlign.CENTER,
    )

    heading = ft.Text(
        "Welcome to QWorkspaces!",
        size=FONT_SIZE_XL,
        weight=ft.FontWeight.BOLD,
        color=COLOR_TEXT_PRIMARY,
        text_align=ft.TextAlign.CENTER,
    )

    subtitle = ft.Text(
        "Your personal AI-powered workspace",
        size=FONT_SIZE_BASE,
        color=COLOR_TEXT_SECONDARY,
        text_align=ft.TextAlign.CENTER,
    )

    user_name = ft.TextField(
        label="Login",
        width=320,
        visible=False,
        border_radius=CARD_BORDER_RADIUS,
        filled=True,
        bgcolor=COLOR_CARD_BG,
        color=COLOR_TEXT_PRIMARY,
    )

    email_field = ft.TextField(
        label="Email",
        width=320,
        keyboard_type=ft.KeyboardType.EMAIL,
        autofocus=True,
        border_radius=CARD_BORDER_RADIUS,
        filled=True,
        bgcolor=COLOR_CARD_BG,
        color=COLOR_TEXT_PRIMARY,
    )

    password_field = ft.TextField(
        label="Password",
        width=320,
        password=True,
        can_reveal_password=True,
        border_radius=CARD_BORDER_RADIUS,
        filled=True,
        bgcolor=COLOR_CARD_BG,
        color=COLOR_TEXT_PRIMARY,
    )

    confirm_password_field = ft.TextField(
        label="Confirm password",
        width=320,
        visible=False,
        password=True,
        can_reveal_password=True,
        border_radius=CARD_BORDER_RADIUS,
        filled=True,
        bgcolor=COLOR_CARD_BG,
        color=COLOR_TEXT_PRIMARY,
    )

    submit_button = ft.Button(
        "Sign in",
        width=320,
        bgcolor=COLOR_ACCENT,
        color=COLOR_TEXT_PRIMARY,
    )

    switch_mode_button = ft.TextButton("Create account")

    def set_mode(register_mode: bool, update_page: bool = True) -> None:
        is_register_mode["value"] = register_mode
        user_name.visible = register_mode
        confirm_password_field.visible = register_mode
        submit_button.content = "Create account" if register_mode else "Sign in"
        message.value = "Create a new account" if register_mode else "Sign in to continue"
        message.color = COLOR_TEXT_SECONDARY
        subtitle.value = (
            "Create your personal workspace account"
            if register_mode
            else "Your personal AI-powered workspace"
        )
        switch_mode_button.content = (
            "Already have an account? Sign in"
            if register_mode
            else "Don't have an account? Create one"
        )
        if update_page:
            page.update()

    def complete_auth(user: dict) -> None:
        set_current_user(page, user["id"], user["login"])
        start_user_session(user["id"])
        message.value = f"Welcome, {user['login']}!"
        message.color = COLOR_TEXT_SUCCESS
        page.go("/home")

    def submit_auth(e) -> None:
        email = (email_field.value or "").strip()
        password = password_field.value or ""

        normalized_email, email_error = validate_user_email(email)
        if email_error:
            message.value = email_error
            message.color = COLOR_TEXT_ERROR
            page.update()
            return

        validated_password, password_error = validate_user_password(password)
        if password_error:
            message.value = password_error
            message.color = COLOR_TEXT_ERROR
            page.update()
            return

        if is_register_mode["value"]:
            login_value = (user_name.value or "").strip()
            validated_name, name_error = validate_user_name(login_value)
            if name_error:
                message.value = name_error
                message.color = COLOR_TEXT_ERROR
                page.update()
                return

            if validated_password != (confirm_password_field.value or ""):
                message.value = "Passwords do not match"
                message.color = COLOR_TEXT_ERROR
                page.update()
                return

            try:
                user_id = register_user(
                    login=validated_name,
                    email=normalized_email,
                    password=validated_password,
                )
            except ValueError as error:
                message.value = str(error)
                message.color = COLOR_TEXT_ERROR
                page.update()
                return

            user = get_user_by_id(user_id)
            if user is None:
                message.value = "Unable to create account"
                message.color = COLOR_TEXT_ERROR
                page.update()
                return

            complete_auth(user)
            return

        user = authenticate_user(normalized_email, validated_password)
        if user is None:
            message.value = "Invalid email or password"
            message.color = COLOR_TEXT_ERROR
            page.update()
            return

        complete_auth(user)

    submit_button.on_click = submit_auth
    password_field.on_submit = submit_auth
    switch_mode_button.on_click = lambda e: set_mode(not is_register_mode["value"])

    card = ft.Container(
        width=420,
        padding=32,
        bgcolor=COLOR_BG_SECONDARY,
        border_radius=CARD_BORDER_RADIUS,
        content=ft.Column(
            controls=[
                ft.Icon(ft.Icons.WORKSPACE_PREMIUM, size=48, color=COLOR_ACCENT),
                ft.Container(height=8),
                heading,
                subtitle,
                ft.Container(height=24),
                user_name,
                email_field,
                password_field,
                confirm_password_field,
                ft.Container(height=8),
                submit_button,
                switch_mode_button,
                message,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=SPACING_SM,
            tight=True,
        ),
    )

    set_mode(False, update_page=False)

    return ft.View(
        route="/",
        bgcolor=COLOR_BG_PRIMARY,
        padding=0,
        spacing=0,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        controls=[card],
    )
