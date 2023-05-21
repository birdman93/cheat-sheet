import json


# На этой странице описаны все фильтры, которые используются в запросах.

# Все функции, кроме generate_filter, возвращают conditions в виде словарей, поэтому их можно вызывать, отдавая
# аргументом другие подобные функции для конструирования составных условий.


def generate_filter(conditions: dict) -> json:
    """
    Единственная функция в файле, возвращающая json, а не словарь. Все остальные функции нужны, для конструирования
    условий, а эта всегда будет финализирующей, т.к. превратит словарь с условиями в json для добавления в тело запроса
    """
    filter = json.dumps(conditions, ensure_ascii=False)
    return filter

def regex_condition(value: str = None):
    condition = {"$regex": f"{value}", "$options": "i"}
    return condition


def in_condition(values: list = None) -> dict:
    condition = {"$in": values}
    return condition


def nin_condition(values: list = None) -> dict:
    condition = {"$nin": values}
    return condition


def eq_condition(value: str = None) -> dict:
    condition = {"$eq": value}
    return condition


def exists_condition() -> dict:
    condition = {"$exists": True, "$nin": [None, "null", ""]}
    return condition


def non_exists_condition(path: str) -> dict:
    condition_1 = {"$eq": None}
    condition_2 = {"$exists": False}
    condition = {"$or": [{path: condition_1}, {path: condition_2}]}
    return condition


def elem_match_condition(id: str = None, value: dict = None) -> dict:
    if value:
        return {"$elemMatch": {"id": id, "value": value}}
    return {"$elemMatch": {"id": id}}


def not_condition(condition: dict = None) -> dict:
    condition = {"$not": condition}
    return condition


def and_condition(*conditions) -> dict:
    conditions = list(conditions)
    condition = {"$and": conditions}
    return condition


def or_condition(*conditions) -> dict:
    conditions = list(conditions)
    condition = {"$or": conditions}
    return condition


def equal_filter(path: str = None, value: str = None) -> json:
    condition = {path: eq_condition(value=value)}
    return condition


def equal_filter_with_id(path: str = None, id: str = None, value: str = None) -> json:
    condition = {path: elem_match_condition(id=id, value=eq_condition(value=value))}
    return condition


def contain_filter(path: str = None, values: list = None) -> json:
    condition = {path: in_condition(values)}
    return condition


def contain_filter_with_id(path: str = None, id: str = None, values: list = None) -> json:
    condition = {path: elem_match_condition(id=id, value=in_condition(values))}
    return condition


def non_contain_filter(path: str = None, values: list = None) -> json:
    condition = {path: nin_condition(values)}
    return condition


def non_contain_filter_with_id(path: str = None, id: str = None, values: list = None) -> json:
    condition = {path: elem_match_condition(id=id, value=nin_condition(values))}
    return condition


def have_value_filter(path: str = None) -> json:
    condition = {path: exists_condition()}
    return condition


def have_value_filter_with_id(path: str = None, id: str = None) -> json:
    condition_1 = {path: not_condition(elem_match_condition(id=id, value={"$type": 10}))}
    condition_2 = {path: elem_match_condition(id=id, value=exists_condition())}
    conditions = and_condition(condition_1, condition_2)
    return conditions


def non_have_value_filter(path: str = None) -> json:
    condition = non_exists_condition(path)
    return condition


def non_have_value_filter_with_id(path: str = None, id: str = None) -> json:
    condition_1 = {path: not_condition(elem_match_condition(id=id))}
    condition_2 = {path: elem_match_condition(id=id, value={"$size": 0})}
    conditions = or_condition(condition_1, condition_2)
    return conditions
