# src/primitive_db/decorators.py
import time

import prompt


def handle_db_errors(func):
    """
    Декоратор для централизованной обработки ошибок БД
    """
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except FileNotFoundError:
            print("Ошибка: Файл данных не найден. Возможно, база данных не инициализирована.") # noqa: E501
        except KeyError as e:
            print(f"Ошибка: Таблица или столбец {e} не найден.")
        except ValueError as e:
            print(f"Ошибка валидации: {e}")
        except Exception as e:
            print(f"Произошла непредвиденная ошибка: {e}")
        return None
    return wrapper


def confirm_action(action_name):
    """
    Декоратор-фабрика для запроса подтверждения опасных операций
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            _answer = prompt.string(f'Вы уверены, что хотите выполнить "{action_name}"? [y/n]: ').strip().lower() # noqa: E501
            if _answer != "y":
                print("Операция отменена.")
                return None
            return func(*args, **kwargs)
        return wrapper
    return decorator


def log_time(func):
    """
    Декоратор для замера времени выполнения функции
    """
    def wrapper(*args, **kwargs):
        _start = time.monotonic()
        _result = func(*args, **kwargs)
        _elapsed = time.monotonic() - _start
        print(f"Функция {func.__name__} выполнилась за {_elapsed:.3f} секунд.")
        return _result
    return wrapper


def create_cacher():
    """
    Функция с замыканием для кэширования результатов
    """
    _cache = {}
    
    def cache_result(key, value_func):
        if key in _cache:
            return _cache[key]
        _result = value_func()
        _cache[key] = _result
        return _result
    
    def clear():
        _cache.clear()
    
    cache_result.clear = clear
    return cache_result