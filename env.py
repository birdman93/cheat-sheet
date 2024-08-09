from dotenv import load_dotenv
import os


class Env:

    def __init__(self):

        # Загрузка переменных окружения из файла .env
        load_dotenv()

    @staticmethod
    def get_env_data_by_name(name: str):

        # Получаем целевую сущность по названию
        entity = os.getenv(name)

        return entity
