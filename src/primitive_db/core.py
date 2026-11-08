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
    """
    Выводит информацию о таблице
    """
    if table_name not in metadata:
        print(f'Ошибка: Таблица "{table_name}" не существует.')
        return
    _columns = metadata[table_name]["columns"]
    _columns_str = ", ".join(f"{_n}:{_t}" for _n, _t in _columns.items())

    print(f"Таблица: {table_name}")
    print(f"Столбцы: {_columns_str}")
    print(f"Количество записей: {len(table_data)}")


def insert(metadata: dict, table_name: str, values: list[str]) -> list[dict] | None:
    """
    Добавляет новую запись в таблицу
    """
    if table_name not in metadata:
        print(f'Ошибка: Таблица "{table_name}" не существует.')
        return None
    _columns = metadata[table_name]["columns"]
    _data_columns = {k: v for k, v in _columns.items() if k != "ID"}

    if len(values) != len(_data_columns):
        print(f"Некорректное значение: ожидается {len(_data_columns)} значений, получено {len(values)}.") # noqa: E501
        return None

    from .parser import cast_value
    from .utils import load_table_data
    _table_data = load_table_data(table_name)
    _typed_values = {}
    for (_col_name, _col_type), _val in zip(_data_columns.items(), values):
        try:
            _typed_values[_col_name] = cast_value(_val, _col_type)
        except ValueError:
            print(f"Некорректное значение: {_val} для типа {_col_type}.")
            return None

    _new_id = max([_r["ID"] for _r in _table_data], default=0) + 1

    _record = {"ID": _new_id}
    _record.update(_typed_values)
    _table_data.append(_record)

    print(f'Запись с ID={_new_id} успешно добавлена в таблицу "{table_name}".')
    return _table_data


def select(table_data: list[dict], where_clause: dict | None = None) -> list[dict]:
    """
    Возвращает записи, фильтрует по where_clause если задан
    """
    if not where_clause:
        return table_data
    return [_r for _r in table_data if all(_r.get(_k) == _v for _k, 
                                           _v in where_clause.items())]


def update(table_data: list[dict], set_clause: dict, where_clause: dict) -> list[dict]:
    """
    Обновляет записи по where_clause согласно set_clause
    """
    for _record in table_data:
        if all(_record.get(_k) == _v for _k, _v in where_clause.items()):
            _record.update(set_clause)
    return table_data


def delete(table_data: list[dict], where_clause: dict) -> list[dict]:
    """
    Удаляет записи по where_clause
    """
    return [_r for _r in table_data if not all(_r.get(_k) == _v for _k, 
                                               _v in where_clause.items())]
