from pytest_check import check


@check.check_func
def strings_equals(key: str, a: str, b: str):
    assert a == b, f'У {key} записано неверное значение. Ожидалось: {a} == {b}'


@check.check_func
def string_in_string(key: str, a: str, b: str):
    assert a in b, f'У {key} записано неверное значение. Ожидалось: {a} in {b}'


@check.check_func
def string_in_list(key: str, a: str, b: list):
    assert a in b, f'У {key} записано неверное значение. Ожидалось: {a} in {b}'


@check.check_func
def lists_equals(key: str, a: list, b: list):
    assert a == b, f'У {key} записано неверное значение. Ожидалось: {a} == {b}'


@check.check_func
def set_equals(key: str, a: set, b: set):
    assert a == b, f'У {key} записано неверное значение. Ожидалось: {a} == {b}'


@check.check_func
def set_in_set(key: str, a: set, b: set):
    assert a.issubset(b), f'У {key} записано неверное значение. Ожидалось: {a} in {b}'


@check.check_func
def assert_false(key: str):
    assert False, f'Значение {key} было передано, но его нет в системе'
