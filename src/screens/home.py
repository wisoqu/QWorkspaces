import flet as ft


def home_screen(page: ft.Page) -> ft.View:
    user_name = page.session.store.get("user_name") or "Guest"

    title = ft.Text(
        f"Hello, {user_name}!",
        size=30,
        weight=ft.FontWeight.BOLD,
        text_align=ft.TextAlign.CENTER,
    )

    subtitle = ft.Text(
        "This is the first version of your Todo home screen.",
        size=16,
        color=ft.Colors.GREY_700,
        text_align=ft.TextAlign.CENTER,
    )

    task_input = ft.TextField(
        label="Add a new task",
        hint_text="For example: Finish the first Flet screen",
        expand=True,
    )

    tasks_column = ft.Column(spacing=10)
    empty_state = ft.Text(
        "No tasks yet. Add your first one above.",
        size=14,
        color=ft.Colors.GREY_600,
        text_align=ft.TextAlign.CENTER,
    )

    def save_tasks(task_titles: list[str]):
        page.session.store.set("tasks", task_titles)

    def render_tasks():
        task_titles = page.session.store.get("tasks") or []
        tasks_column.controls.clear()

        for task_title in task_titles:
            tasks_column.controls.append(
                ft.Container(
                    padding=12,
                    border_radius=12,
                    bgcolor=ft.Colors.BLUE_GREY_50,
                    content=ft.Row(
                        controls=[
                            ft.Icon(ft.Icons.RADIO_BUTTON_UNCHECKED, size=18),
                            ft.Text(task_title, expand=True),
                        ],
                        spacing=12,
                    ),
                )
            )

        empty_state.visible = len(task_titles) == 0

    def add_task(e):
        title = task_input.value.strip()

        if not title:
            task_input.error_text = "Please enter a task title"
            page.update()
            return

        stored_tasks = page.session.store.get("tasks") or []
        stored_tasks.append(title)

        save_tasks(stored_tasks)
        render_tasks()

        task_input.error_text = None
        task_input.value = ""
        page.update()

    async def go_back(e):
        await page.push_route("/")

    task_input.on_submit = add_task

    add_task_button = ft.Button(
        "Add task",
        icon=ft.Icons.ADD,
        on_click=add_task,
    )

    back_button = ft.Button(
        "Back",
        icon=ft.Icons.ARROW_BACK,
        on_click=go_back,
    )

    hint_card = ft.Container(
        padding=16,
        border_radius=16,
        bgcolor=ft.Colors.AMBER_50,
        content=ft.Column(
            controls=[
                ft.Text("MVP direction", weight=ft.FontWeight.BOLD),
                ft.Text(
                    "Next we can add completion, deletion, and simple filtering.",
                    color=ft.Colors.GREY_800,
                ),
            ],
            spacing=8,
            tight=True,
        ),
    )

    render_tasks()

    return ft.View(
        route="/home",
        controls=[
            ft.Container(
                expand=True,
                padding=8,
                content=ft.Column(
                    controls=[
                        back_button,
                        title,
                        subtitle,
                        ft.Row(
                            controls=[
                                task_input,
                                add_task_button,
                            ],
                            spacing=12,
                        ),
                        hint_card,
                        empty_state,
                        tasks_column,
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
                    spacing=20,
                ),
            )
        ],
    )
