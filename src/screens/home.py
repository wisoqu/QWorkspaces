import flet as ft


def home_screen(page: ft.Page) -> ft.View:
    user_name = page.session.store.get("user_name") or "Guest"

    note_input = ft.TextField(label="New note", width=300)
    notes_column = ft.Column(spacing=10)

    def add_note(e):
        text = note_input.value.strip()

        if not text:
            return

        notes_column.controls.append(ft.Text(text))
        note_input.value = ""
        page.update()

    sidebar = ft.Container(
        width=260,
        bgcolor=ft.Colors.BLUE_GREY_700,
        padding=20,
        content=ft.Column(
            controls=[
                ft.Text(
                    f"{user_name}'s space",
                    size=22,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.WHITE
                ),
                ft.Divider(color=ft.Colors.WHITE24),
                ft.Text("Sidebar",
                        color=ft.Colors.WHITE70,
                        ),
            ],
            spacing=20,
            alignment=ft.MainAxisAlignment.START,
        ),
    )

    main_content = ft.Container(
        expand=True,
        bgcolor=ft.Colors.BLACK12,
        padding=30,
        content=ft.Column(
            controls=[
                ft.Text(
                    "Main content",
                    size=28,
                    weight=ft.FontWeight.BOLD,
                ),
                ft.Text(
                    "Your personal tasks here...",
                    size=16,
                ),
                ft.Row(
                    controls=[
                        note_input,
                        ft.Button("Add", on_click=add_note),
                    ]
                ),
                notes_column,
            ],
            spacing=16,
            alignment=ft.MainAxisAlignment.START,
        ),
    )

    return ft.View(
        route="/home",
        controls=[
            ft.Row(
                controls=[
                    sidebar,
                    main_content,
                ],
                spacing=0,
                expand=True,
            )
        ],
    )
