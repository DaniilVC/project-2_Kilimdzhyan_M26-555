SUPPORTED_TYPES = {"int", "str", "bool"}


def cast_value(_value: str, _type: str):
    """
    Приводит строку к нужному типу
    """
    if _type == "int":
        return int(_value)
    if _type == "str":
        return _value
    if _type == "bool":
        return _value.lower() in ("true", "1")
    raise ValueError(f"Неизвестный тип: {_type}")


def parse_condition(tokens: list[str], columns: dict) -> dict | None:
    """
    Парсит условие вида 'age = 28' в словарь
    Возвращает словарь {'age': 28'} 
    """
    if len(tokens) % 3 != 0:
        print("Некорректное условие: ожидается формат 'столбец = значение'.")
        return None

    _result = {}
    for _i in range(0, len(tokens), 3):
        _col_name = tokens[_i]
        _operator = tokens[_i + 1]
        _value = tokens[_i + 2]

        if _operator != "=":
            print(f"Некорректный оператор: {_operator}. Поддерживается только '='.")
            return None

        if _col_name not in columns:
            print(f"Некорректное значение: столбец '{_col_name}' не существует.")
            return None

        _col_type = columns[_col_name]
        try:
            _result[_col_name] = cast_value(_value, _col_type)
        except ValueError:
            print(f"Некорректное значение: {_value} для типа {_col_type}.")
            return None

    return _result