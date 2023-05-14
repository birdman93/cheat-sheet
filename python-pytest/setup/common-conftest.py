import pytest
import importlib


def pytest_addoption(parser):
    """
    Создание параметров запуска тестов, управлять которыми нужно из консоли
    """

    pass # см. ui-conftest.py


# = = = = = = = = = = = =
# инициализация параметров для data_driven_testing

def pytest_generate_tests(metafunc):
    """
    Магическая функция pytest, при инициализации фикстур, смотрит есть ли у теста фикстуры,
    начинающиеся с data_, если находит - импортирует фикстуру как пакет
    """
    for fixture in metafunc.fixturenames:
        if fixture.startswith('data_'):
            # передаем название параметра в функцию, которая парсит файл
            tests = load_tests(fixture)
            metafunc.parametrize(fixture, tests)


def load_tests(name_of_data_file):
    """
    Передаем название файла с тестовыми данными как модуль python. Параметры:
        name_of_data_file название файла(должно начинаться с data_, будет импортирован как пакет
    """
    tests_module = importlib.import_module(f'tests.test_parameters.{name_of_data_file}')
    # все параметры в тестовом файле передаются из list test_data
    for param in tests_module.test_data:
        yield param
