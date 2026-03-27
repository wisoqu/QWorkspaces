"""
Модуль для настройки импортов.
Подключать в начале каждого файла который находится в подпапках.
"""
import sys
from pathlib import Path

# Добавляем src в sys.path для корректных импортов
src_path = Path(__file__).resolve().parent.parent
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))
