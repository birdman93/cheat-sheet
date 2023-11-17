import pickle


def cache_results(func):
    """
    Декоратор для кэширования результатов выполнения функций (т.е. сокращаем число вызовов функции с одинаковыми
    входными данными)
    """

    cache = {}

    def wrapper(*args, **kwargs):
        key = (func.__name__, pickle.dumps(args), pickle.dumps(kwargs))

        if key in cache:
            return cache[key]
        else:
            result = func(*args, **kwargs)
            cache[key] = result
            return result

    return wrapper