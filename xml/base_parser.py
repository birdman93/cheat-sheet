# import xml.etree.ElementTree as ET
import lxml.etree as ET

class BaseParser:
    """
    Базовый класс для работы с xml-файлами, в котором инициализуруем ElementTree, а также объявляем словарь с
    пространством имен
    """
    def __init__(self, path_to_xml_file: str):
        self.__ET = ET
        self.semd_name = path_to_xml_file
        self.__tree = self.__ET.parse(path_to_xml_file)
        self.namespaces = {
            'key_1': 'value_1',
            'key_2': 'value_2'
        }

        for key, value in self.namespaces.items():
            ET.register_namespace(key, value)

    def _find_element(self, xpath: str) -> ET.Element:
        """Возвращает ET-элемент по xpath"""
        return self.__tree.find(xpath, self.namespaces)

    def _find_all_elements(self, xpath: str) -> list[ET.Element]:
        """Возвращает список ET-элементов по xpath"""
        return self.__tree.findall(xpath, self.namespaces)

    def _xpath(self, xpath: str) -> list[ET.Element]:
        """Возвращает список значений по xpath"""
        return self.__tree.xpath(xpath, namespaces=self.namespaces)

    def _xpaths_handler(self, xpaths: list):
        """Принимает список xpaths, возвращает список значений по первому результативному xpath (и сам xpath)"""
        for xpath in xpaths:
            result = self._xpath(xpath)
            if result:
                return result, xpath
            else:
                continue
        return None

    @staticmethod
    def _replace_element_text(element=None, value=None):
        """Заменяет текст тэга элемента"""

        if not isinstance(element, list):
            if element is not None:
                element.text = value

        else:
            if element is not None:
                if isinstance(value, str):
                    for i in range(len(element)):
                        element[i].text = value
                if isinstance(value, list):
                    for i in range(len(element)):
                        element[i].text = value[i]

    @staticmethod
    def _replace_element_attribute(element=None, attr=None, value=None):
        """Заменяет значение атрибута у переданного элемента/элементов"""

        if not isinstance(element, list):
            if element is not None:
                element.set(attr, value)

        else:
            if element is not None:
                if isinstance(value, str):
                    for i in range(len(element)):
                        element[i].set(attr, value)
                if isinstance(value, list):
                    for i in range(len(element)):
                        element[i].set(attr, value[i])

    def xml_to_string(self):
        return self.__ET.tostring(self.__tree.getroot(), encoding='utf-8', method='xml').decode('utf-8')
