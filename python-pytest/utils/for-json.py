import json


def find_key(key: str = None, json_data: json = None):
    """
    Функция для рекурсивного поиска по ключу в json
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
