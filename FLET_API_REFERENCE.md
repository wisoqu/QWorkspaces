# Flet API Reference for QWorkspaces

Version checked locally: `flet 0.83.0`  
Updated: `2026-03-27`

This contract is strict:
- if a method is in `DEPRECATED`, do not use it;
- if a method is not listed in `ALLOWED`, do not assume it exists;
- if a valid new method is confirmed locally, add it explicitly.

## ALLOWED

### Page
- `page.title = value`
- `page.theme_mode = value`
- `page.bgcolor = value`
- `page.padding = value`
- `page.route`
- `page.go("/route")`
- `page.on_route_change = handler`
- `page.on_view_pop = handler`
- `page.views.clear()`
- `page.views.append(view)`
- `page.update()`
- `page.show_dialog(dialog)`
- `page.pop_dialog()`

### Session
- `page.session.get("key")`
- `page.session.set("key", value)`
- `page.session.contains_key("key")`
- `page.session.remove("key")`

### Controls
- `ft.View(...)`
- `ft.Container(...)`
- `ft.Column(...)`
- `ft.Row(...)`
- `ft.Text(...)`
- `ft.Icon(...)`
- `ft.Divider(...)`
- `ft.TextField(...)`
- `ft.Dropdown(...)`
- `ft.dropdown.Option(...)`
- `ft.AlertDialog(...)`
- `ft.Button(...)`
- `ft.TextButton(...)`

### Control properties and enums used in the project
- `control.content = value`
- `control.visible = value`
- `ft.FontWeight.BOLD`
- `ft.TextAlign.CENTER`
- `ft.CrossAxisAlignment.CENTER`
- `ft.MainAxisAlignment.CENTER`
- `ft.ThemeMode.DARK`
- `ft.KeyboardType.EMAIL`
- `ft.Icons.*`
- `ft.Alignment(x, y)`

## DEPRECATED

### Routing and page
- `page.push_route(...)`
- `await page.push_route(...)`
- `page.close_dialog()`
- `page.open(dialog)`
- `page.close()`
- `page.session["key"] = value`
- `del page.session["key"]`
- `"key" in page.session`
- `page.session.get("key", default)`

### Buttons
- `ft.ElevatedButton(...)`
- `ft.Button(text="...")`
- `ft.TextButton(text="...")`
- `button.text = "..."`

### Dropdown and dialogs
- `ft.DropdownOption(...)`
- manual nesting of one `ft.View` inside another `ft.View`

### Risky UI patterns
- calling `page.update()` while a screen is still being built

## Notes

- In this project, button text is passed as the first positional argument or through `content`.
- In this project, dialogs are opened with `page.show_dialog()` and closed with `page.pop_dialog()`.
- In this project, session access is only through `get/set/contains_key/remove`.
