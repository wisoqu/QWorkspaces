# Flet API Reference для QWorkspaces

**Версия Flet:** 0.82.2  
**Дата обновления:** 2026-03-28  
**Статус:** Актуально для проекта QWorkspaces

---

## 📋 Как использовать этот справочник

Этот файл содержит полную информацию о доступных API Flet 0.82.2 для использования в проекте QWorkspaces.

**Правила:**
- Если метод/свойство есть в `ALLOWED` — можно использовать
- Если в `DEPRECATED` — НЕ использовать
- Если чего-то нет в списке — проверить через `python -c "import flet as ft; print(dir(ft.ControlName))"`

---

## 🔑 Основные контролы для QWorkspaces

### Page

**Методы:**
| Метод | Описание |
|-------|----------|
| `page.add(control)` | Добавить контрол на страницу |
| `page.remove(control)` | Удалить контрол со страницы |
| `page.update()` | Обновить UI |
| `page.go(route)` | Перейти по маршруту |
| `page.show_dialog(dialog)` | Показать диалог |
| `page.pop_dialog()` | Закрыть диалог |
| `page.close_drawer()` | Закрыть drawer |
| `page.close_end_drawer()` | Закрыть end drawer |
| `page.scroll_to(offset=0, duration=0)` | Прокрутка страницы |
| `page.launch_url(url)` | Открыть URL |
| `page.get_control(id)` | Получить контрол по ID |
| `page.pubsub.send_all(message)` | Отправить сообщение всем |
| `page.run_task(task_name, func)` | Запустить задачу |
| `page.run_thread(func)` | Запустить в потоке |
| `page.take_screenshot()` | Сделать скриншот |
| `page.clipboard.set_text(text)` | Копировать в буфер |
| `page.clipboard.get_text()` | Получить из буфера |

**Свойства:**
| Свойство | Тип | Описание |
|----------|-----|----------|
| `page.title` | str | Заголовок окна |
| `page.theme_mode` | ThemeMode | Тема (DARK/LIGHT/SYSTEM) |
| `page.bgcolor` | str/Colors | Цвет фона |
| `page.padding` | int/Padding | Отступы страницы |
| `page.route` | str | Текущий маршрут |
| `page.session` | Session | Хранилище сессии |
| `page.session.store` | Storage | Хранилище данных сессии |
| `page.views` | list | Список представлений |
| `page.controls` | list | Контролы страницы |
| `page.vertical_alignment` | MainAxisAlignment | Вертикальное выравнивание |
| `page.horizontal_alignment` | CrossAxisAlignment | Горизонтальное выравнивание |
| `page.scroll` | ScrollMode | Режим прокрутки |
| `page.spacing` | int | Расстояние между элементами |
| `page.width` | int | Ширина страницы |
| `page.height` | int | Высота страницы |
| `page.visible` | bool | Видимость |
| `page.disabled` | bool | Disabled состояние |
| `page.opacity` | float | Прозрачность (0-1) |
| `page.expand` | bool/int | Растягивание |
| `page.col` | int | Количество колонок (1-12) |
| `page.tooltip` | str | Подсказка |
| `page.data` | Any | Пользовательские данные |
| `page.key` | str | Ключ контрола |
| `page.ref` | Ref | Реф для доступа |
| `page.on_route_change` | callable | Обработчик смены маршрута |
| `page.on_view_pop` | callable | Обработчик pop view |
| `page.on_error` | callable | Обработчик ошибок |
| `page.on_connect` | callable | Обработчик подключения |
| `page.on_disconnect` | callable | Обработчик отключения |
| `page.on_resize` | callable | Обработчик изменения размера |
| `page.on_keyboard_event` | callable | Обработчик клавиатуры |
| `page.appbar` | AppBar | Верхняя панель |
| `page.bottom_appbar` | BottomAppBar | Нижняя панель |
| `page.floating_action_button` | FloatingActionButton | FAB кнопка |
| `page.navigation_bar` | NavigationBar | Навигационная панель |
| `page.drawer` | Drawer | Левая панель |
| `page.end_drawer` | Drawer | Правая панель |
| `page.theme` | Theme | Светлая тема |
| `page.dark_theme` | Theme | Тёмная тема |
| `page.locale_configuration` | LocaleConfiguration | Локаль |

---

### View

**Параметры инициализации:**
- `route: str = ""` — маршрут представления
- `controls: list = []` — список контролов
- `spacing: int = 10` — расстояние между элементами
- `padding: Padding = 0` — отступы
- `bgcolor: str/Colors = None` — цвет фона
- `vertical_alignment: MainAxisAlignment = None` — вертикальное выравнивание
- `horizontal_alignment: CrossAxisAlignment = None` — горизонтальное выравнивание
- `scroll: ScrollMode = None` — режим прокрутки
- `visible: bool = True` — видимость
- `expand: bool/int = False` — растягивание

**Методы:**
- `view.add(control)` — добавить контрол
- `view.remove(control)` — удалить контрол
- `view.controls.clear()` — очистить все контролы
- `view.controls.append(control)` — добавить в конец
- `view.controls.insert(index, control)` — вставить по индексу
- `view.controls.pop()` — удалить последний

**Свойства:**
- `view.route` — маршрут
- `view.controls` — список контролов
- `view.spacing` — spacing
- `view.padding` — padding
- `view.bgcolor` — цвет фона
- `view.visible` — видимость
- `view.expand` — растягивание
- `view.data` — пользовательские данные
- `view.key` — ключ

---

### Container

**Параметры инициализации:**
- `content: Control = None` — содержимое
- `bgcolor: str/Colors = None` — цвет фона
- `border: Border = None` — граница
- `border_radius: int/BorderRadius = 0` — скругление углов
- `padding: Padding = 0` — внутренние отступы
- `margin: Margin = 0` — внешние отступы
- `width: int/float = None` — ширина
- `height: int/float = None` — высота
- `alignment: Alignment = None` — выравнивание контента
- `expand: bool/int = False` — растягивание
- `col: int = 12` — колонки (1-12)
- `visible: bool = True` — видимость
- `disabled: bool = False` — disabled
- `opacity: float = 1.0` — прозрачность
- `tooltip: str = None` — подсказка
- `data: Any = None` — данные
- `key: str = None` — ключ
- `ref: Ref = None` — реф
- `on_click: callable = None` — обработчик клика
- `on_hover: callable = None` — обработчик наведения
- `on_long_press: callable = None` — длинное нажатие
- `on_tap: callable = None` — тап
- `on_pan_update: callable = None` — перетаскивание
- `on_resize: callable = None` — изменение размера
- `shadow: list = []` — тень
- `clip_behavior: ClipBehavior = ClipBehavior.HARD_EDGE` — обрезка
- `ink: bool = False` — ink эффект
- `gradient: Gradient = None` — градиент

**Методы:**
- `container.add(control)` — добавить контрол
- `container.update()` — обновить

---

### Column

**Параметры инициализации:**
- `controls: list = []` — список контролов
- `spacing: int = 10` — расстояние между элементами
- `width: int/float = None` — ширина
- `height: int/float = None` — высота
- `expand: bool/int = False` — растягивание
- `scroll: ScrollMode = ScrollMode.AUTO` — прокрутка
- `horizontal_alignment: CrossAxisAlignment = CrossAxisAlignment.NONE` — выравнивание по горизонтали
- `vertical_alignment: MainAxisAlignment = MainAxisAlignment.NONE` — выравнивание по вертикали
- `wrap: bool = False` — перенос
- `visible: bool = True` — видимость
- `data: Any = None` — данные
- `key: str = None` — ключ

**Методы:**
- `column.add(control)` — добавить контрол
- `column.controls.clear()` — очистить
- `column.controls.append(control)` — добавить в конец
- `column.controls.insert(index, control)` — вставить
- `column.controls.pop()` — удалить последний
- `column.update()` — обновить

---

### Row

**Параметры инициализации:**
- `controls: list = []` — список контролов
- `spacing: int = 10` — расстояние между элементами
- `width: int/float = None` — ширина
- `height: int/float = None` — высота
- `expand: bool/int = False` — растягивание
- `scroll: ScrollMode = ScrollMode.AUTO` — прокрутка
- `horizontal_alignment: MainAxisAlignment = MainAxisAlignment.NONE` — выравнивание по горизонтали
- `vertical_alignment: CrossAxisAlignment = CrossAxisAlignment.NONE` — выравнивание по вертикали
- `wrap: bool = False` — перенос
- `visible: bool = True` — видимость
- `data: Any = None` — данные
- `key: str = None` — ключ

**Методы:**
- `row.add(control)` — добавить контрол
- `row.controls.clear()` — очистить
- `row.controls.append(control)` — добавить в конец
- `row.controls.insert(index, control)` — вставить
- `row.controls.pop()` — удалить последний
- `row.update()` — обновить

---

### Text

**Параметры инициализации:**
- `value: str = ""` — текст (первый позиционный аргумент)
- `size: int/float = None` — размер шрифта
- `color: str/Colors = None` — цвет текста
- `weight: FontWeight = FontWeight.NORMAL` — жирность
- `font_family: str = None` — шрифт
- `text_align: TextAlign = TextAlign.LEFT` — выравнивание
- `text_overflow: TextOverflow = TextOverflow.CLIP` — переполнение
- `max_lines: int = None` — максимум строк
- `selectable: bool = False` — можно выделить
- `italic: bool = False` — курсив
- `no_wrap: bool = False` — без переноса
- `span: bool = False` — span режим
- `visible: bool = True` — видимость
- `data: Any = None` — данные
- `key: str = None` — ключ
- `ref: Ref = None` — реф
- `tooltip: str = None` — подсказка
- `expand: bool/int = False` — растягивание
- `col: int = 12` — колонки
- `opacity: float = 1.0` — прозрачность
- `italic: bool = False` — курсив
- `theme_style: TextThemeStyle = None` — стиль темы
- `text_scale_factor: int/float = 1` — масштаб текста
- `line_height: int/float = 1.2` — высота строки

**Методы:**
- `text.update()` — обновить

---

### Icon

**Параметры инициализации:**
- `name: Icons = None` — иконка (например, `ft.Icons.HOME`)
- `size: int/float = None` — размер
- `color: str/Colors = None` — цвет
- `visible: bool = True` — видимость
- `data: Any = None` — данные
- `key: str = None` — ключ
- `ref: Ref = None` — реф
- `tooltip: str = None` — подсказка
- `expand: bool/int = False` — растягивание
- `col: int = 12` — колонки
- `opacity: float = 1.0` — прозрачность

---

### IconButton

**Параметры инициализации:**
- `icon: Icons = None` — иконка
- `icon_size: int/float = None` — размер иконки
- `icon_color: str/Colors = None` — цвет иконки
- `selected_icon: Icons = None` — иконка для выбранного состояния
- `selected: bool = False` — выбрано
- `toggle_mode: bool = False` — режим переключения
- `bgcolor: str/Colors = None` — цвет фона
- `icon_padding: Padding = 4` — отступы иконки
- `width: int/float = None` — ширина
- `height: int/float = None` — высота
- `visible: bool = True` — видимость
- `disabled: bool = False` — disabled
- `opacity: float = 1.0` — прозрачность
- `tooltip: str = None` — подсказка
- `data: Any = None` — данные
- `key: str = None` — ключ
- `ref: Ref = None` — реф
- `expand: bool/int = False` — растягивание
- `col: int = 12` — колонки
- `on_click: callable = None` — обработчик клика
- `on_hover: callable = None` — обработчик наведения
- `on_focus: callable = None` — обработчик фокуса
- `on_blur: callable = None` — обработчик потери фокуса

---

### TextField

**Параметры инициализации:**
- `value: str = ""` — значение
- `label: str = None` — лейбл
- `hint_text: str = None` — подсказка
- `prefix: Control = None` — префикс контрол
- `suffix: Control = None` — суффикс контрол
- `prefix_icon: Icons = None` — иконка префикса
- `suffix_icon: Icons = None` — иконка суффикса
- `keyboard_type: KeyboardType = KeyboardType.TEXT` — тип клавиатуры
- `password: bool = False` — пароль
- `can_reveal_password: bool = False` — показать пароль
- `multiline: bool = False` — многострочное
- `min_lines: int = 1` — минимум строк
- `max_lines: int = 1` — максимум строк
- `max_length: int = None` — максимум символов
- `width: int/float = None` — ширина
- `height: int/float = None` — высота
- `expand: bool/int = False` — растягивание
- `col: int = 12` — колонки
- `text_size: int/float = None` — размер текста
- `text_align: TextAlign = TextAlign.LEFT` — выравнивание
- `color: str/Colors = None` — цвет текста
- `bgcolor: str/Colors = None` — цвет фона
- `border_radius: int/BorderRadius = 0` — скругление
- `filled: bool = False` — залитый фон
- `fill_color: str/Colors = None` — цвет заполнения
- `hover_color: str/Colors = None` — цвет при наведении
- `focused_border_color: str/Colors = None` — цвет рамки в фокусе
- `focused_border_width: int/float = 2` — ширина рамки в фокусе
- `border_color: str/Colors = None` — цвет рамки
- `border_width: int/float = 1` — ширина рамки
- `content_padding: Padding = None` — отступы контента
- `readonly: bool = False` — только чтение
- `disabled: bool = False` — disabled
- `visible: bool = True` — видимость
- `opacity: float = 1.0` — прозрачность
- `tooltip: str = None` — подсказка
- `data: Any = None` — данные
- `key: str = None` — ключ
- `ref: Ref = None` — реф
- `on_change: callable = None` — при изменении
- `on_submit: callable = None` — при нажатии Enter
- `on_focus: callable = None` — при фокусе
- `on_blur: callable = None` — при потере фокуса
- `on_tap: callable = None` — при тапе
- `autofocus: bool = False` — автофокус
- `shift_key: bool = False` — shift
- `control_key: bool = False` — control
- `alt_key: bool = False` — alt
- `meta_key: bool = False` — meta
- `text_style: TextStyle = None` — стиль текста
- `label_style: TextStyle = None` — стиль лейбла
- `hint_style: TextStyle = None` — стиль подсказки
- `helper_text: str = None` — вспомогательный текст
- `helper_style: TextStyle = None` — стиль вспомогательного текста
- `counter_text: str = None` — текст счётчика
- `counter_style: TextStyle = None` — стиль счётчика
- `error_text: str = None` — текст ошибки
- `error_style: TextStyle = None` — стиль ошибки
- `capitalization: TextCapitalization = TextCapitalization.NONE` — капитализация
- `input_filter: InputFilter = None` — фильтр ввода
- `enable_suggestions: bool = False` — включить подсказки
- `smart_dashes_type: bool = False` — умные кавычки
- `smart_quotes_type: bool = False` — умные тире
- `cursor_color: str/Colors = None` — цвет курсора
- `cursor_width: int/float = 2` — ширина курсора
- `cursor_height: int/float = None` — высота курсора
- `cursor_radius: int/float = None` — радиус курсора
- `cursor_error_color: str/Colors = None` — цвет курсора ошибки
- `selection_color: str/Colors = None` — цвет выделения
- `autocorrect: bool = True` — автокоррекция

---

### Dropdown

**Параметры инициализации:**
- `value: str = None` — текущее значение
- `options: list[DropdownOption] = []` — список опций
- `label: str = None` — лейбл
- `hint: str = None` — подсказка
- `text: str = None` — текст
- `text_align: TextAlign = TextAlign.START` — выравнивание текста
- `width: int/float = None` — ширина
- `height: int/float = None` — высота
- `expand: bool/int = False` — растягивание
- `col: int = 12` — колонки
- `filled: bool = False` — залитый фон
- `bgcolor: str/Colors = None` — цвет фона
- `border_radius: int/BorderRadius = 0` — скругление
- `border: InputBorder = None` — граница
- `border_width: int/float = 1` — ширина границы
- `border_color: str/Colors = None` — цвет границы
- `focused_border_width: int/float = None` — ширина границы в фокусе
- `focused_border_color: str/Colors = None` — цвет границы в фокусе
- `content_padding: Padding = None` — отступы контента
- `dense: bool = False` — плотный режим
- `elevation: int/float = 8` — возвышение
- `enable_filter: bool = False` — включить фильтрацию
- `enable_search: bool = True` — включить поиск
- `editable: bool = False` — редактируемый
- `menu_height: int/float = None` — высота меню
- `menu_width: int/float = None` — ширина меню
- `menu_style: MenuStyle = None` — стиль меню
- `expanded_insets: Padding = None` — отступы раскрытия
- `selected_suffix: Control = None` — суффикс выбранного
- `input_filter: InputFilter = None` — фильтр ввода
- `capitalization: TextCapitalization = None` — капитализация
- `trailing_icon: Icons/Control = None` — иконка справа
- `leading_icon: Icons/Control = None` — иконка слева
- `selected_trailing_icon: Icons/Control = None` — иконка справа для выбранного
- `error_text: str = None` — текст ошибки
- `error_style: TextStyle = None` — стиль ошибки
- `text_size: int/float = None` — размер текста
- `text_style: TextStyle = None` — стиль текста
- `label_style: TextStyle = None` — стиль лейбла
- `hint_style: TextStyle = None` — стиль подсказки
- `helper_text: str = None` — вспомогательный текст
- `helper_style: TextStyle = None` — стиль вспомогательного текста
- `visible: bool = True` — видимость
- `disabled: bool = False` — disabled
- `opacity: float = 1.0` — прозрачность
- `tooltip: str = None` — подсказка
- `data: Any = None` — данные
- `key: str = None` — ключ
- `ref: Ref = None` — реф
- `on_select: callable = None` — при выборе
- `on_text_change: callable = None` — при изменении текста
- `on_focus: callable = None` — при фокусе
- `on_blur: callable = None` — при потере фокуса
- `autofocus: bool = False` — автофокус

**DropdownOption параметры:**
- `key: str` — ключ опции (возвращается в value)
- `label: str` — отображаемый текст
- `disabled: bool = False` — disabled опция

---

### Button

**Параметры инициализации:**
- `text: str = ""` — текст кнопки (первый позиционный аргумент)
- `icon: Icons = None` — иконка
- `bgcolor: str/Colors = None` — цвет фона
- `color: str/Colors = None` — цвет текста
- `disabled_color: str/Colors = None` — цвет когда disabled
- `style: ButtonStyle = None` — стиль
- `width: int/float = None` — ширина
- `height: int/float = None` — высота
- `expand: bool/int = False` — растягивание
- `col: int = 12` — колонки
- `visible: bool = True` — видимость
- `disabled: bool = False` — disabled
- `opacity: float = 1.0` — прозрачность
- `tooltip: str = None` — подсказка
- `data: Any = None` — данные
- `key: str = None` — ключ
- `ref: Ref = None` — реф
- `on_click: callable = None` — обработчик клика
- `on_hover: callable = None` — обработчик наведения
- `on_focus: callable = None` — обработчик фокуса
- `on_blur: callable = None` — обработчик потери фокуса
- `on_long_press: callable = None` — длинное нажатие
- `url: str = None` — URL для перехода
- `url_target: str = None` — цель URL (_blank, _self)

---

### TextButton

**Параметры инициализации:**
- `text: str = ""` — текст кнопки (первый позиционный аргумент)
- `icon: Icons = None` — иконка
- `style: ButtonStyle = None` — стиль
- `width: int/float = None` — ширина
- `height: int/float = None` — высота
- `expand: bool/int = False` — растягивание
- `col: int = 12` — колонки
- `visible: bool = True` — видимость
- `disabled: bool = False` — disabled
- `opacity: float = 1.0` — прозрачность
- `tooltip: str = None` — подсказка
- `data: Any = None` — данные
- `key: str = None` — ключ
- `ref: Ref = None` — реф
- `on_click: callable = None` — обработчик клика
- `on_hover: callable = None` — обработчик наведения
- `on_focus: callable = None` — обработчик фокуса
- `on_blur: callable = None` — обработчик потери фокуса
- `on_long_press: callable = None` — длинное нажатие
- `url: str = None` — URL для перехода
- `url_target: str = None` — цель URL

---

### AlertDialog

**Параметры инициализации:**
- `open: bool = False` — открыт ли диалог
- `modal: bool = False` — модальный
- `title: Control = None` — заголовок
- `content: Control = None` — содержимое
- `actions: list = []` — список кнопок действий
- `actions_alignment: MainAxisAlignment = MainAxisAlignment.NONE` — выравнивание действий
- `actions_overflow_alignment: MainAxisAlignment = MainAxisAlignment.NONE` — выравнивание при переполнении
- `actions_overflow_spacing: int/float = 0` — spacing при переполнении
- `action_button_height: int/float = 48` — высота кнопок действий
- `action_button_min_width: int/float = 64` — мин ширина кнопок
- `action_button_padding: Padding = None` — отступы кнопок
- `button_layout: ButtonLayout = ButtonLayout.ROW` — layout кнопок
- `scrollable: bool = False` — прокручиваемый
- `adaptive: bool = False` — адаптивный
- `bgcolor: str/Colors = None` — цвет фона
- `elevation: int/float = 24` — возвышение
- `shadow_color: str/Colors = Colors.TRANSPARENT` — цвет тени
- `shape: ShapeBorder = None` — форма
- `title_padding: Padding = None` — отступы заголовка
- `content_padding: Padding = None` — отступы контента
- `visible: bool = True` — видимость
- `data: Any = None` — данные
- `key: str = None` — ключ
- `ref: Ref = None` — реф
- `on_dismiss: callable = None` — при закрытии

---

### Chip

**Параметры инициализации:**
- `label: Control = None` — лейбл (текст или контрол)
- `avatar: Control = None` — аватар
- `delete_icon: Icons = None` — иконка удаления
- `selected: bool = False` — выбран
- `disabled: bool = False` — disabled
- `bgcolor: str/Colors = None` — цвет фона
- `selected_color: str/Colors = None` — цвет когда выбран
- `delete_icon_color: str/Colors = None` — цвет иконки удаления
- `label_padding: Padding = None` — отступы лейбла
- `padding: Padding = None` — отступы
- `width: int/float = None` — ширина
- `height: int/float = None` — высота
- `expand: bool/int = False` — растягивание
- `col: int = 12` — колонки
- `visible: bool = True` — видимость
- `opacity: float = 1.0` — прозрачность
- `tooltip: str = None` — подсказка
- `data: Any = None` — данные
- `key: str = None` — ключ
- `ref: Ref = None` — реф
- `on_click: callable = None` — обработчик клика
- `on_hover: callable = None` — обработчик наведения
- `on_focus: callable = None` — обработчик фокуса
- `on_blur: callable = None` — обработчик потери фокуса
- `on_delete: callable = None` — при нажатии на delete

---

### Divider

**Параметры инициализации:**
- `height: int/float = None` — высота
- `thickness: int/float = 1` — толщина линии
- `indent: int/float = 0` — отступ слева
- `end_indent: int/float = 0` — отступ справа
- `color: str/Colors = None` — цвет
- `visible: bool = True` — видимость
- `data: Any = None` — данные
- `key: str = None` — ключ
- `ref: Ref = None` — реф
- `expand: bool/int = False` — растягивание
- `col: int = 12` — колонки
- `opacity: float = 1.0` — прозрачность
- `tooltip: str = None` — подсказка

---

## 🎨 Enums и константы

### FontWeight
- `FontWeight.NORMAL` — нормальный
- `FontWeight.BOLD` — жирный
- `FontWeight.W_100` — 100
- `FontWeight.W_200` — 200
- `FontWeight.W_300` — 300
- `FontWeight.W_400` — 400 (= NORMAL)
- `FontWeight.W_500` — 500
- `FontWeight.W_600` — 600
- `FontWeight.W_700` — 700 (= BOLD)
- `FontWeight.W_800` — 800
- `FontWeight.W_900` — 900

### TextAlign
- `TextAlign.LEFT`
- `TextAlign.RIGHT`
- `TextAlign.CENTER`
- `TextAlign.JUSTIFY`
- `TextAlign.START`
- `TextAlign.END`

### MainAxisAlignment
- `MainAxisAlignment.NONE`
- `MainAxisAlignment.START`
- `MainAxisAlignment.END`
- `MainAxisAlignment.CENTER`
- `MainAxisAlignment.SPACE_BETWEEN`
- `MainAxisAlignment.SPACE_AROUND`
- `MainAxisAlignment.SPACE_EVENLY`

### CrossAxisAlignment
- `CrossAxisAlignment.NONE`
- `CrossAxisAlignment.START`
- `CrossAxisAlignment.END`
- `CrossAxisAlignment.CENTER`
- `CrossAxisAlignment.STRETCH`

### ScrollMode
- `ScrollMode.AUTO`
- `ScrollMode.ALWAYS`
- `ScrollMode.HIDDEN`

### ThemeMode
- `ThemeMode.SYSTEM`
- `ThemeMode.LIGHT`
- `ThemeMode.DARK`

### KeyboardType
- `KeyboardType.TEXT`
- `KeyboardType.EMAIL`
- `KeyboardType.NUMBER`
- `KeyboardType.PHONE`
- `KeyboardType.URL`
- `KeyboardType.PASSWORD`
- `KeyboardType.MULTILINE`
- `KeyboardType.DATETIME`
- `KeyboardType.VISIBLE_PASSWORD`

### ClipBehavior
- `ClipBehavior.NONE`
- `ClipBehavior.HARD_EDGE`
- `ClipBehavior.ANTI_ALIAS`
- `ClipBehavior.ANTI_ALIAS_WITH_SAVE_LAYER`

### Icons (часто используемые в QWorkspaces)
- `ft.Icons.HOME`
- `ft.Icons.TASK_ALT`
- `ft.Icons.NOTE`
- `ft.Icons.NOTES`
- `ft.Icons.CALENDAR_MONTH`
- `ft.Icons.SMART_TOY`
- `ft.Icons.LOGOUT`
- `ft.Icons.SEND`
- `ft.Icons.ADD`
- `ft.Icons.EDIT`
- `ft.Icons.DELETE`
- `ft.Icons.SEARCH`
- `ft.Icons.FILTER_LIST`
- `ft.Icons.CHECK`
- `ft.Icons.CLOSE`
- `ft.Icons.MENU`
- `ft.Icons.ACCOUNT_CIRCLE`
- `ft.Icons.WORKSPACE_PREMIUM`
- `ft.Icons.ARROW_BACK`
- `ft.Icons.MORE_VERT`
- `ft.Icons.SETTINGS`
- `ft.Icons.INFO`
- `ft.Icons.WARNING`
- `ft.Icons.ERROR`
- `ft.Icons.SUCCESS`

---

## 📦 Session API

**Session (page.session):**
- `page.session.store.get(key, default=None)` — получить значение
- `page.session.store.set(key, value)` — установить значение
- `page.session.store.remove(key)` — удалить значение
- `page.session.store.contains_key(key)` — проверить наличие ключа

---

## ⚠️ DEPRECATED (НЕ использовать)

### Routing и Page
- `page.push_route(...)` — использовать `page.go(route)`
- `await page.push_route(...)` — асинхронный API не поддерживается
- `page.close_dialog()` — использовать `page.pop_dialog()`
- `page.open(dialog)` — использовать `page.show_dialog(dialog)`
- `page.close()` — не использовать напрямую

### Session
- `page.session["key"] = value` — использовать `page.session.store.set(key, value)`
- `del page.session["key"]` — использовать `page.session.store.remove(key)`
- `"key" in page.session` — использовать `page.session.store.contains_key(key)`
- `page.session.get("key", default)` — использовать `page.session.store.get(key, default)`

### Buttons
- `ft.ElevatedButton(...)` — использовать `ft.Button(...)` или `ft.FilledButton(...)`
- `ft.Button(text="...")` — использовать позиционный аргумент: `ft.Button("...")`
- `button.text = "..."` — использовать `button.content = "..."`

### Dropdown
- `ft.DropdownOption(...)` — использовать `ft.dropdown.Option(...)`
- `ft.Dropdown(on_change=...)` — использовать `ft.Dropdown(on_select=...)`

### Risky UI patterns
- Вызов `page.update()` во время сборки экрана — использовать `update_page=False` и обновлять после

---

## 💡 Best Practices для QWorkspaces

### 1. Работа с сессией
```python
# Правильно (через utils/session.py):
from utils.session import get_current_user_id, set_current_user

user_id = get_current_user_id(page)
set_current_user(page, user_id, user_name)

# Неправильно (прямой доступ):
user_id = page.session["user_id"]  # DEPRECATED!
```

### 2. Диалоги
```python
# Правильно:
page.show_dialog(dialog)
page.pop_dialog()

# Неправильно:
page.open(dialog)  # DEPRECATED!
page.close_dialog()  # DEPRECATED!
```

### 3. Dropdown
```python
# Правильно:
ft.Dropdown(
    options=[ft.dropdown.Option(key="value", text="Label")],
    on_select=handler,  # НЕ on_change!
)

# Неправильно:
ft.Dropdown(on_change=handler)  # DEPRECATED в 0.82.2!
```

### 4. Кнопки
```python
# Правильно:
ft.Button("Save", on_click=handler)
ft.TextButton("Cancel", on_click=handler)

# Неправильно:
ft.Button(text="Save")  # text= не нужен
ft.ElevatedButton("Save")  # DEPRECATED стиль
```

### 5. Lambda в циклах
```python
# Правильно (capture через default argument):
for item in items:
    controls.append(
        ft.Container(
            on_click=lambda e, i=item: handle_click(i)
        )
    )

# Неправильно (closure problem):
for item in items:
    controls.append(
        ft.Container(
            on_click=lambda e: handle_click(item)  # Все будут с последним item!
        )
    )
```

---

## 🔍 Как проверить API контрола

```bash
# Получить все атрибуты контрола:
python -c "import flet as ft; print(dir(ft.Container))"

# Получить сигнатуру __init__:
python -c "import flet as ft; import inspect; print(inspect.signature(ft.Container.__init__))"

# Получить документацию:
python -c "import flet as ft; help(ft.Container)"
```

---

## 📚 Дополнительные ресурсы

- [Flet Docs](https://flet.dev/docs/)
- [Flet Controls](https://flet.dev/docs/controls/)
- [Flet API Reference](https://flet.dev/docs/api/)
- [GitHub: flet-dev/flet](https://github.com/flet-dev/flet)
