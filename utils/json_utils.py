import json


def find_value_by_key(data: dict = None, key: str = None) -> dict | None:
    """
    Функция для рекурсивного поиска по ключу в JSON-объекте

    Возвращает:
    - Значение ключа, если он был найден
    - None, если ключ не найден.
    """

    if isinstance(data, dict):
        for k, v in data.items():
            if k == key:
                return v
            elif isinstance(v, (dict, list)):
                result = find_value_by_key(key, v)
                if result is not None:
                    return result

    elif isinstance(data, list):
        for item in data:
            result = find_value_by_key(key, item)
            if result is not None:
                return result

    return None


def find_values_list_by_key(data: dict = None, key: str = None) -> list:
    """
    Функция для рекурсивного поиска значений по ключу в JSON-объекте

    Возвращает:
    - Список значений, соответствующих ключу, если найдены.
    - Пустой список, если ключ не найден.
    """

    results = []

    if isinstance(data, dict):
        if key in data:
            results.append(data[key])

        for value in data.values():
            results.extend(find_values_list_by_key(value, key))

    # Поиск ключа в списке
    if isinstance(data, list):
        for item in data:
            results.extend(find_values_list_by_key(item, key))

    return results


def find_dict_by_value(data: dict = None, key: str = None, value: str = None) -> dict | None:
    """
    Функция для рекурсивного поиска словаря, в котором находится целевое значение, в JSON-объекте

    Возвращает:
    - Словарь с искомым значением
    - None, если значение не найдено или ключ не существует.
    """

    if isinstance(data, dict):
        if key in data and data[key] == value:
            return data

        for val in data.values():
            result = find_dict_by_value(val, key, value)
            if result is not None:
                return result

    if isinstance(data, list):
        for item in data:
            result = find_dict_by_value(item, key, value)
            if result is not None:
                return result

    return None


def remove_dict_with_key_value(data=None, key_to_remove=None, value_to_remove=None):

    if isinstance(data, dict):
        new_dict = data.copy()
        for key, value in data.items():
            if key == key_to_remove and value == value_to_remove:
                del new_dict[key]

            elif isinstance(value, (dict, list)):
                new_dict[key] = remove_dict_with_key_value(value, key_to_remove, value_to_remove)

        return new_dict

    elif isinstance(data, list):
        # Удаляем нужные значения из списка
        new_list = []
        for item in data:
            if not (isinstance(item, (dict, list)) and (
                    key_to_remove in item and item[key_to_remove] == value_to_remove)):
                new_list.append(remove_dict_with_key_value(item, key_to_remove, value_to_remove))

        return new_list

    else:
        return data
