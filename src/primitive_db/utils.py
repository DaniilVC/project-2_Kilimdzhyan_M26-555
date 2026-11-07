# src/primitive_db/utils.py
import json


def load_metadata(filepath: str) -> dict:
    """
    Загружает данные из JSON
    """
    try:
        with open(filepath, "r", encoding="utf-8") as _file:
            return json.load(_file)
    except FileNotFoundError:
        return {}


def save_metadata(filepath: str, data: dict) -> None:
    """
    Сохраняет переданные данные в JSON
    """
    with open(filepath, "w", encoding="utf-8") as _file:
        json.dump(data, _file, indent=4, ensure_ascii=False)
