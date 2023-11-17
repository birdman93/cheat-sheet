import random


def random_num_from_string(input_str: str = None) -> str:
    """Функция принимает на вход строку с диапазонами из чисел (1, 5-10, 15-17) и возвращает рандомное число в виде
    строки"""

    result = []
    ranges = input_str.split(',')
    for item in ranges:
        item = item.strip()
        if '-' in item:
            start, end = list(map(int, item.split('-')))
            result.extend(list(range(start, end + 1)))
            result = list(map(str, result))
        else:
            result.append(item)
    return random.choice(result)
