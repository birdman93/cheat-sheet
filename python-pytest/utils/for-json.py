import json


def find_key(key: str = None, json_data: json = None) -> dict | None:
    """
    Функция для рекурсивного поиска по ключу в json

    Возвращает:
    - Значение ключа, если он был найден
    - None, если ключ не найден.
    """

    if isinstance(json_data, dict):
        for k, v in json_data.items():
            if k == key:
                return v
            elif isinstance(v, (dict, list)):
                result = find_key(key, v)
                if result is not None:
                    return result

    elif isinstance(json_data, list):
        for item in json_data:
            result = find_key(key, item)
            if result is not None:
                return result

    return None


def get_dict_with_value_from_json(json_obj: json = None, key: str = None, value: str = None) -> dict | None:
    """
    Функция для поиска значения и возвращения словаря, в котором находится найденное значение.

    Возвращает:
    - Словарь, в котором найдено значение.
    - None, если значение не найдено или ключ не существует.
    """
    # Проверка, является ли json_obj словарем
    if isinstance(json_obj, dict):
        # Проверка наличия ключа в текущем словаре
        if key in json_obj and json_obj[key] == value:
            return json_obj

        # Поиск значения во всех значениях словаря
        for val in json_obj.values():
            result = get_dict_with_value_from_json(val, key, value)
            if result is not None:
                return result

    # Поиск значения в списке
    if isinstance(json_obj, list):
        for item in json_obj:
            result = get_dict_with_value_from_json(item, key, value)
            if result is not None:
                return result

    return None
