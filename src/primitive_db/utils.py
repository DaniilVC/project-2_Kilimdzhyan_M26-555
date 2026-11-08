# src/primitive_db/utils.py
import json
import os

DATA_DIR = "data"


def load_metadata(filepath: str) -> dict:
    """
    Загружает данные из JSON-файла
    """
    try:
        with open(filepath, "r", encoding="utf-8") as _file:
            return json.load(_file)
    except FileNotFoundError:
        return {}


def save_metadata(filepath: str, data: dict) -> None:
    """
    Сохраняет переданные данные в JSON-файл
    """
    with open(filepath, "w", encoding="utf-8") as _file:
        json.dump(data, _file, indent=4, ensure_ascii=False)


def _get_table_filepath(table_name: str) -> str:
    """
    Возвращает путь к файлу данных таблицы
    """
    os.makedirs(DATA_DIR, exist_ok=True)
    return os.path.join(DATA_DIR, f"{table_name}.json")


def load_table_data(table_name: str) -> list[dict]:
    """
    Загружает данные таблицы из JSON-файла
    """
    _filepath = _get_table_filepath(table_name)
    try:
        with open(_filepath, "r", encoding="utf-8") as _file:
            return json.load(_file)
    except FileNotFoundError:
        return []


def save_table_data(table_name: str, data: list[dict]) -> None:
    """
    Сохраняет данные таблицы в JSON-файл
    """
    _filepath = _get_table_filepath(table_name)
    with open(_filepath, "w", encoding="utf-8") as _file:
        json.dump(data, _file, indent=4, ensure_ascii=False)
