import json


def find_value_by_key(key: str = None, json_data: json = None) -> dict | None:
    """
    Функция для рекурсивного поиска по ключу в JSON-объекте

    Возвращает:
    - Значение ключа, если он был найден
    - None, если ключ не найден.
    """

    if isinstance(json_data, dict):
        for k, v in json_data.items():
            if k == key:
                return v
            elif isinstance(v, (dict, list)):
                result = find_value_by_key(key, v)
                if result is not None:
                    return result

    elif isinstance(json_data, list):
        for item in json_data:
            result = find_value_by_key(key, item)
            if result is not None:
                return result

    return None


def find_value_list_by_key(json_obj: json = None, key: str = None) -> list:
    """
    Функция для рекурсивного поиска значений по ключу в JSON-объекте

    Возвращает:
    - Список значений, соответствующих ключу, если найдены.
    - Пустой список, если ключ не найден.
    """

    results = []

    # Проверка, является ли json_obj словарем
    if isinstance(json_obj, dict):
        # Поиск ключа в текущем словаре
        if key in json_obj:
            results.append(json_obj[key])

        # Поиск ключа во всех значениях словаря
        for value in json_obj.values():
            results.extend(find_value_list_by_key(value, key))

    # Поиск ключа в списке
    if isinstance(json_obj, list):
        for item in json_obj:
            results.extend(find_value_list_by_key(item, key))

    return results


def find_dict_with_value(json_obj: json = None, key: str = None, value: str = None) -> dict | None:
    """
    Функция для рекурсивного поиска словаря, в котором находится целевое значение, в JSON-объекте

    Возвращает:
    - Словарь с искомым значением
    - None, если значение не найдено или ключ не существует.
    """

    # Проверка, является ли json_obj словарем
    if isinstance(json_obj, dict):
        # Проверка наличия ключа в текущем словаре
        if key in json_obj and json_obj[key] == value:
            return json_obj

        # Поиск значения во всех значениях словаря
        for val in json_obj.values():
            result = find_dict_with_value(val, key, value)
            if result is not None:
                return result

    # Поиск значения в списке
    if isinstance(json_obj, list):
        for item in json_obj:
            result = find_dict_with_value(item, key, value)
            if result is not None:
                return result

    return None

