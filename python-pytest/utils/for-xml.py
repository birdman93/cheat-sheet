import xml.etree.ElementTree as ET


class BaseParser:
    """
    Базовый класс для работы с xml файлами, в котором инициализуруем ElementTree, а также объявляем словарь с
    пространством имен
    """
    def __init__(self, path_to_xml_file: str):
        self.__ET = ET
        self.semd_name = path_to_xml_file
        self.__tree = self.__ET.parse(path_to_xml_file)
        self.__namespaces = {
            'key_1': 'value_1',
            'key_2': 'value_2'
        }

    def _find_element(self, xpath: str) -> ET.Element:
        """Возвращает ET-элемент по xpath"""
        return self.__tree.find(xpath, self.__namespaces)

    def _find_all_elements(self, xpath: str) -> list[ET.Element]:
        """Возвращает список ET-элементов по xpath"""
        return self.__tree.findall(xpath, self.__namespaces)

    @staticmethod
    def replace_element_text(element: ET.Element, value: str):
        """Заменяет текст тэга элемента"""
        element.text = value

    @staticmethod
    def replace_element_attribute(element: ET.Element, attr: str, value: str):
        """Заменяет значение атрибута у переданного элемента"""
        element.set(attr, value)

    @staticmethod
    def replace_texts_in_list_elements(list_elements: list[ET.Element], list_values: list[str]):
        """Заменяет текст тэгов у массива элементов"""
        # Проверяем валидность переданных данных
        if list_values:
            if len(list_elements) != len(list_values):
                raise AttributeError('Переданы списки с разной длиной')
            # Выполняем замену
            if list_values is not None:
                for i in range(len(list_elements)):
                    list_elements[i].text = list_values[i]
        else:
            raise ValueError(f"В качестве тестовых данных сгенерировано значение None")

    @staticmethod
    def replace_attributes_in_list_elements(list_elements: list[ET.Element], attr: str, list_values: list[str]):
        """Заменяет значение атрибута у массива элементов"""
        # Проверяем валидность переданных данных
        if list_values:
            if len(list_elements) != len(list_values):
                raise AttributeError(f'Переданы списки с разной длиной: {list_elements} vs {list_values}')
            # Выполняем замену
            if list_values is not None:
                for i in range(len(list_elements)):
                    list_elements[i].set(attr, list_values[i])
        else:
            raise ValueError(f"В качестве тестовых данных сгенерировано значение None: {list_elements}")

    def xml_to_string(self):
        return self.__ET.tostring(self.__tree.getroot(), encoding='utf-8', method='xml').decode('utf-8')
