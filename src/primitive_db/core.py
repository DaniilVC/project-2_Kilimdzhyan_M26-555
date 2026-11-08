# src/primitive_db/core.py
SUPPORTED_TYPES = {"int", "str", "bool"}


def create_table(metadata: dict, table_name: str, columns: list[str]) -> dict | None:
    """
    Создаёт таблицу в метаданных
    """
    if table_name in metadata:
        print(f'Ошибка: Таблица "{table_name}" уже существует.')
        return None

    _parsed_columns = {"ID": "int"}

    for _col_def in columns:
        if ":" not in _col_def:
            print(f"Некорректное значение: {_col_def}. Попробуйте снова.")
            return None

        _col_name, _col_type = _col_def.split(":", 1)

        if _col_type not in SUPPORTED_TYPES:
            print(f"Некорректное значение: {_col_type}. Попробуйте снова.")
            return None

        _parsed_columns[_col_name] = _col_type

    metadata[table_name] = {"columns": _parsed_columns}

    _columns_str = ", ".join(f"{_n}:{_t}" for _n, _t in _parsed_columns.items())
    print(f'Таблица "{table_name}" успешно создана со столбцами: {_columns_str}')

    return metadata


def drop_table(metadata: dict, table_name: str) -> dict | None:
    """
    Удаляет таблицу из метаданных
    """
    if table_name not in metadata:
        print(f'Ошибка: Таблица "{table_name}" не существует.')
        return None

    del metadata[table_name]
    print(f'Таблица "{table_name}" успешно удалена.')

    return metadata


def list_tables(metadata: dict) -> None:
    """
    Выводит список всех таблиц
    """
    if not metadata:
        print("Таблицы не найдены.")
        return

    for _table_name in metadata:
        print(f"- {_table_name}")

def info(metadata: dict, table_name: str, table_data: list[dict]) -> None:
    """Выводит информацию о таблице."""
    if table_name not in metadata:
        print(f'Ошибка: Таблица "{table_name}" не существует.')
        return

    _columns = metadata[table_name]["columns"]
    _columns_str = ", ".join(f"{_n}:{_t}" for _n, _t in _columns.items())

    print(f"Таблица: {table_name}")
    print(f"Столбцы: {_columns_str}")
    print(f"Количество записей: {len(table_data)}")

