import config
from xml.base_parser import BaseParser
from common.utils.forms.get_object_data import get_random_value, get_data_by_field

import json


class ParserHandler(BaseParser):
    def __init__(self, path_to_xml_file):

        # Наследуемся от BaseParser со всеми базовыми методами для парсинга
        super().__init__(path_to_xml_file)

        # Забираем все xpaths и парсим данные
        self.common_document = self.__parsing(self.__json_reader(
            f'{config.ROOT}/common/utils/semd_parsers/common_document.json'))
        self.common_patient = self.__parsing(self.__json_reader(
             f'{config.ROOT}/common/utils/semd_parsers/common_patient.json'))
        self.common_event = self.__parsing(self.__json_reader(
            f'{config.ROOT}/common/utils/semd_parsers/common_event.json'))
        self.kpis = self.__parsing(self.__json_reader(
            f'{config.ROOT}/common/utils/semd_parsers/kpis.json'))

    @staticmethod
    def __json_reader(path_to_json):
        """Метод для чтения xpaths, собранных в json"""
        with open(path_to_json, encoding='UTF-8') as file:
            result = json.load(fp=file)
        return result

    def __parsing(self, json_data: dict) -> dict:
        """Метод для парсинга данных, полученных из json с xpaths"""
        for key, value in json_data.items():
            result = self._xpaths_handler(json_data[key]['xpath'])
            if result is not None and result:
                json_data[key]['element'], json_data[key]['xpath'] = result
        return json_data

    def replace_element_handler(self, entity_from_json: dict | list = None, value: str | list = None,
                                random_date: str = None, random_datetime: str = None,
                                obj=None):
        """
        Метод, являющийся хабом для всех replace функций - логика завязана на парсинге json-файлов, подмена будет
        срабатывать лишь в том случае, если целевой элемент в СЭМДе был найден
        """

        # Проверяем успешность парсинга
        if entity_from_json.get('element') is not None:

            # Создадим переменную, куда запишем подставляемое значение, чтобы после обратиться к нему из тестов (если
            # будем обращаться к справочнику, то значение перезапишем)
            value_for_check = value

            # Определяем targetPlace
            entity_from_json['targetPlace'] = (str(entity_from_json['xpath']).split('/')[-1].
                                               replace("@", "").replace("()", ""))

            # Определяем родительский элемент(ы)
            parent_element = None
            if isinstance(entity_from_json['element'], dict):
                parent_element = entity_from_json['element'][0].getparent()
            elif isinstance(entity_from_json['element'], list):
                parent_element = [item.getparent() for item in entity_from_json['element']]

            # Если имеем дело с текстом
            if 'text' in entity_from_json['targetPlace']:

                # Если передано значение, но подставляем
                if value_for_check is not None:
                    self._replace_element_text(element=parent_element, value=value_for_check)

                # Если значение НЕ передано, то подставляем displayName - удобно для кпи и пр., чтобы иметь
                # уникальные текстовые значения
                else:
                    self._replace_element_text(element=parent_element, value=entity_from_json['displayName'])

            # Если имеем дело с другими опциями, тогда проверяем тип и выбираем соответствующее значение для
            # подстановки в СЭМД
            else:

                if entity_from_json.get('type') == 'link' and entity_from_json.get('forms') is not None:
                    if value_for_check is None:
                        value_for_check = get_random_value(collection_name=entity_from_json['forms'],
                                                           expected_field=entity_from_json['target_field_from_forms'])

                elif entity_from_json.get('type') == 'digit':
                    pass

                elif entity_from_json.get('type') == 'date':
                    value_for_check = str(random_date)

                elif entity_from_json.get('type') == 'datetime':
                    value_for_check = str(random_datetime)

                self._replace_element_attribute(element=parent_element,
                                                attr=entity_from_json['targetPlace'],
                                                value=value_for_check)

            # Добавляем значение для проверки в тестах в исходную сущность - без интерпретации
            if (entity_from_json.get('interpretation_source') is None
                    and entity_from_json.get('interpretation_target') is None):
                entity_from_json['value_for_check'] = value_for_check
            # Если значение с интерпретацией: в СЭМДе, например, displayName, а в пациента мы записываем id сущности
            else:
                entity_from_json['value_for_check'] = get_data_by_field(
                    collection_name=entity_from_json['forms'],
                    search_field=entity_from_json['interpretation_source'],
                    search_body=value_for_check,
                    returned_entity=entity_from_json['interpretation_target']
                )

    @staticmethod
    def replace_str_handler(semd: str = None, entity_from_json: dict = None, value: str = None) -> str:
        """
        Метод, который принимает уже переделанный в строку СЭМД и выполняем замену целевых значений
        """

        # Проверяем успешность парсинга
        if entity_from_json.get('element') is not None:

            # Создадим переменную, куда запишем подставляемое значение, чтобы после обратиться к нему из тестов
            value_for_check = value

            # Определяем targetPlace
            entity_from_json['targetPlace'] = (str(entity_from_json['xpath']).split('/')[-1].
                                               replace("@", "").replace("()", ""))

            # Определяем родительский элемент, атрибут которого будем заменять
            parent_element = entity_from_json['element'][0].getparent()

            # Если имеем дело с текстом
            if 'text' in entity_from_json['targetPlace']:
                old_value = parent_element.text
                semd = semd.replace(old_value, value_for_check)

            # Если имеем дело с другими опциями
            else:
                old_value = parent_element.get(entity_from_json['targetPlace'])

                # Проверяем, нужно ли обратиться к какому-либо справочнику в Forms (тогда переназначаем value)
                if entity_from_json.get('forms') is not None:

                    # Если мы передаем конкретное значение, то к справочнику обращаться не будем
                    if value_for_check is None:
                        value_for_check = get_random_value(collection_name=entity_from_json['forms'],
                                                           expected_field=entity_from_json['target_field_from_forms'])

                    # Приходится дообрабатывать clinic, который является частью id, чтобы заменить разом везде
                    if '.100.1.1.51' in old_value:
                        old_value = old_value.replace('.100.1.1.51', '')

                semd = semd.replace(old_value, value_for_check)

            # Добавляем подставленное значение в исходную сущность
            entity_from_json['value_for_check'] = value_for_check

        return semd


