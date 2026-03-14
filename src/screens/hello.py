import flet as ft


def hello_screen(page: ft.Page) -> ft.View:
    # Intro screen: ask for a user name and then navigate to home.
    message = ft.Text(
        "Enter your name to continue",
        size=16,
        color=ft.Colors.GREY_700,
    )

    user_name = ft.TextField(
        label="Your name",
        width=320,
        autofocus=True,
    )

    async def continue_click(e):
        # Validate the input, save it in session storage, then navigate.
        name = user_name.value.strip()

        if not name:
            message.value = "Please enter your name"
            message.color = ft.Colors.RED_600
            page.update()
            return

        page.session.store.set("user_name", name)
        message.value = f"Welcome, {name}!"
        message.color = ft.Colors.GREY_700
        page.update()
        await page.push_route("/home")

    user_name.on_submit = continue_click

    heading = ft.Text(
        "Welcome to QWorkspaces!",
        size=30,
        weight=ft.FontWeight.BOLD,
        text_align=ft.TextAlign.CENTER,
    )

    subtitle = ft.Text(
        "A small start screen built with Flet",
        size=14,
        color=ft.Colors.GREY_600,
        text_align=ft.TextAlign.CENTER,
    )

    submit_button = ft.Button(
        "Continue",
        on_click=continue_click,
    )

    return ft.View(
        route="/",
        controls=[
            ft.Container(
                expand=True,
                alignment=ft.Alignment(0, 0),
                content=ft.Column(
                    controls=[
                        heading,
                        subtitle,
                        user_name,
                        submit_button,
                        message,
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=16,
                    tight=True,
                ),
            )
        ],
    )
