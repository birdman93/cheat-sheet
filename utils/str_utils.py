import re


def get_funcs_name_from_code(code: str) -> list:
    """
    Функция принимает js-код в виде строки и возвращает массив с названием функций
    """

    matches = re.findall(r'export const (\w+) = {', code)

    return matches
