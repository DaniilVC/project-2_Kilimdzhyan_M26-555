# src/primitive_db/engine.py
import shlex

import prompt
from prettytable import PrettyTable

from .constants import DB_META_FILE
from .core import (
    create_table,
    delete,
    drop_table,
    info,
    insert,
    list_tables,
    select,
    update,
)
from .parser import parse_condition
from .utils import load_metadata, load_table_data, save_metadata, save_table_data


def print_help() -> None:
    """
    Выводит справочную информацию о доступных командах
    """
    print("\n***Операции с данными***\n")
    print("Функции:")
    print("<command> create_table <имя_таблицы> <столбец1:тип> <столбец2:тип> .. - создать таблицу") # noqa: E501
    print("<command> insert into <имя_таблицы> values (<значение1>, <значение2>, ...) - создать запись") # noqa: E501
    print("<command> select from <имя_таблицы> where <столбец> = <значение> - прочитать записи по условию") # noqa: E501
    print("<command> select from <имя_таблицы> - прочитать все записи")
    print("<command> update <имя_таблицы> set <столбец1> = <новое_значение1> where <столбец_условия> = <значение_условия> - обновить запись") # noqa: E501
    print("<command> delete from <имя_таблицы> where <столбец> = <значение> - удалить запись") # noqa: E501
    print("<command> info <имя_таблицы> - вывести информацию о таблице")
    print("<command> list_tables - показать список всех таблиц")
    print("<command> drop_table <имя_таблицы> - удалить таблицу")
    print("\nОбщие команды:")
    print("<command> exit - выход из программы")
    print("<command> help - справочная информация\n")


def _print_table(_columns: list[str], _data: list[dict]) -> None:
    """
    Выводит данные в виде таблицы
    """
    _table = PrettyTable()
    _table.field_names = _columns
    for _row in _data:
        _table.add_row([_row[_col] for _col in _columns])
    print(_table)


def run() -> None:
    """
    Основной цикл программы для работы с базой данных
    """
    print_help()

    while True:
        try:
            _user_input = prompt.string("Введите команду: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nЗавершение работы программы.")
            break

        if not _user_input:
            continue

        _args = shlex.split(_user_input)
        _command = _args[0]

        match _command:
            case "exit":
                break

            case "help":
                print_help()

            case "list_tables":
                _metadata = load_metadata(DB_META_FILE)
                list_tables(_metadata)

            case "create_table":
                if len(_args) < 3:
                    print("Некорректное значение: create_table. Попробуйте снова.")
                    continue
                _table_name = _args[1]
                _columns = _args[2:]
                _metadata = load_metadata(DB_META_FILE)
                _result = create_table(_metadata, _table_name, _columns)
                if _result is not None:
                    save_metadata(DB_META_FILE, _result)

            case "drop_table":
                if len(_args) != 2:
                    print("Некорректное значение: drop_table. Попробуйте снова.")
                    continue
                _table_name = _args[1]
                _metadata = load_metadata(DB_META_FILE)
                _result = drop_table(_metadata, _table_name)
                if _result is not None:
                    save_metadata(DB_META_FILE, _result)

            case "info":
                if len(_args) != 2:
                    print("Некорректное значение: info. Попробуйте снова.")
                    continue
                _table_name = _args[1]
                _metadata = load_metadata(DB_META_FILE)
                if _table_name not in _metadata:
                    print(f'Ошибка: Таблица "{_table_name}" не существует.')
                    continue
                _table_data = load_table_data(_table_name)
                info(_metadata, _table_name, _table_data)

            case "insert":
                # insert into <table> values (v1, v2, ...)
                if len(_args) < 5 or _args[1] != "into" or _args[3] != "values":
                    print("Некорректное значение: insert. Попробуйте снова.")
                    continue
                _table_name = _args[2]
                _values = _args[4:]
                _metadata = load_metadata(DB_META_FILE)
                if _table_name not in _metadata:
                    print(f'Ошибка: Таблица "{_table_name}" не существует.')
                    continue
                _result = insert(_metadata, _table_name, _values)
                if _result is not None:
                    save_table_data(_table_name, _result)

            case "select":
                # select from <table> [where col = val ...]
                if len(_args) < 3 or _args[1] != "from":
                    print("Некорректное значение: select. Попробуйте снова.")
                    continue
                _table_name = _args[2]
                _metadata = load_metadata(DB_META_FILE)
                if _table_name not in _metadata:
                    print(f'Ошибка: Таблица "{_table_name}" не существует.')
                    continue
                _columns = _metadata[_table_name]["columns"]
                _table_data = load_table_data(_table_name)

                if "where" in _args:
                    _where_idx = _args.index("where")
                    _where_tokens = _args[_where_idx + 1:]
                    _where_clause = parse_condition(_where_tokens, _columns)
                    if _where_clause is None:
                        continue
                    _result = select(_table_data, _where_clause)
                else:
                    _result = select(_table_data)

                _print_table(list(_columns.keys()), _result)

            case "update":
                # update <table> set col = val [where col = val ...]
                if len(_args) < 5 or _args[2] != "set":
                    print("Некорректное значение: update. Попробуйте снова.")
                    continue
                _table_name = _args[1]
                _metadata = load_metadata(DB_META_FILE)
                if _table_name not in _metadata:
                    print(f'Ошибка: Таблица "{_table_name}" не существует.')
                    continue
                _columns = _metadata[_table_name]["columns"]
                _table_data = load_table_data(_table_name)

                if "where" not in _args:
                    print("Некорректное значение: update требует условие where. Попробуйте снова.") # noqa: E501
                    continue
                _where_idx = _args.index("where")
                _set_tokens = _args[3:_where_idx]
                _where_tokens = _args[_where_idx + 1:]

                _set_clause = parse_condition(_set_tokens, _columns)
                if _set_clause is None:
                    continue
                _where_clause = parse_condition(_where_tokens, _columns)
                if _where_clause is None:
                    continue

                _result = update(_table_data, _set_clause, _where_clause)
                if _result is not None:
                    save_table_data(_table_name, _result)
                    print(f'Запись в таблице "{_table_name}" успешно обновлена.')

            case "delete":
                # delete from <table> where col = val
                if len(_args) < 5 or _args[1] != "from" or "where" not in _args:
                    print("Некорректное значение: delete. Попробуйте снова.")
                    continue
                _table_name = _args[2]
                _metadata = load_metadata(DB_META_FILE)
                if _table_name not in _metadata:
                    print(f'Ошибка: Таблица "{_table_name}" не существует.')
                    continue
                _columns = _metadata[_table_name]["columns"]
                _table_data = load_table_data(_table_name)

                _where_idx = _args.index("where")
                _where_tokens = _args[_where_idx + 1:]
                _where_clause = parse_condition(_where_tokens, _columns)
                if _where_clause is None:
                    continue

                _result = delete(_table_data, _where_clause)
                if _result is not None:
                    save_table_data(_table_name, _result)
                    print(f'Запись успешно удалена из таблицы "{_table_name}".')

            case _:
                print(f"Функции {_command} нет. Попробуйте снова.")