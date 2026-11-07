# src/primitive_db/engine.py
import shlex

import prompt

from .core import create_table, drop_table, list_tables
from .utils import load_metadata, save_metadata

DB_META_FILE = "db_meta.json"


def print_help() -> None:
    """Выводит справочную информацию о доступных командах."""
    print("\n***Процесс работы с таблицей***")
    print("Функции:")
    print("<command> create_table <имя_таблицы> <столбец1:тип> <столбец2:тип> .. - создать таблицу") # noqa: E501
    print("<command> list_tables - показать список всех таблиц")
    print("<command> drop_table <имя_таблицы> - удалить таблицу")
    print("\nОбщие команды:")
    print("<command> exit - выход из программы")
    print("<command> help - справочная информация\n")


def run() -> None:
    """
    Основной цикл программы для работы с базой данных
    """
    print("\n***База данных***\n")
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
            case _:
                print(f"Функции {_command} нет. Попробуйте снова.")