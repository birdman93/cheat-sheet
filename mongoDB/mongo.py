from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError, InvalidOperation


current_connection = [] # хранилище доступных подключений


def connect_database_server(server_host: str, server_port: int) -> MongoClient:
    """
    Устанавливает подключение с сервером баз данных MongoDB, где
        server_host: str, адрес сервера базы данных, для подключения
        server_port: int, порт на котором ожидается подключение берет дефолтные данные из конфига
    """

    # проверим нет ли действующих подключений
    while len(current_connection) > 0:

        try:
            current_connection[-1].admin.command('ping')
            conn = current_connection[-1]
            return conn

        except (ServerSelectionTimeoutError, InvalidOperation):
            current_connection.pop(-1)

    # если нет, создадим новое
    else:
        conn = MongoClient(server_host, server_port)

        # проверим что подключение успешно
        try:
            conn.admin.command('ping')

        except ServerSelectionTimeoutError:
            raise ConnectionError(
                f"не удалось подключиться к серверу баз данных. HOST: {server_host}, PORT: {server_port}")

        current_connection.append(conn)
        return conn


def get_list_databases(session: MongoClient) -> list:
    """
    Возвращает массив с названиями найденных БД
    """

    databases = MongoClient.list_database_names(session)
    if not databases:
        print("No databases found")
    else:
        return databases


def get_database(session: MongoClient, database_name: str):
    """
    Находит и возвращает базу данных на сервере, если искомая база данных отсутствует, возвращает ошибку
    """

    if database_name in session.list_database_names():
        database = session[database_name]

        return database

    else:
        raise KeyError(f"""не удалось найти базу данных {database_name} на подключенном сервере, 
                доступные базы данных: {sorted(session.list_database_names())}""")


def get_list_collections(session: MongoClient, database_name: str):
    """
    Находит и возвращает список коллекций БД,
    """

    database = get_database(session, database_name)
    return [item for item in database.list_collections()]


def get_collection(session: MongoClient, database_name: str, collection_name: str):
    """
    Находит и возвращает объект коллекции базы данных, если искомая база коллекция отсутствует, возвращает ошибку
    """

    database = get_database(session=session, database_name=database_name)

    if collection_name in database.list_collection_names():
        collection = database[collection_name]

        return collection

    else:
        raise KeyError(f"""не удалось найти коллекцию {collection_name} в базе данных, 
                доступные коллекции: {sorted(database.list_collection_names())}""")


def find_document(session: MongoClient, database_name: str, collection_name: str, key_to_find: tuple[dict], multiple: bool = False):
    """
    Получает документ из указанной коллекции и возвращает его
    """

    collection = get_collection(session=session, database_name=database_name, collection_name=collection_name)

    if multiple:
        results = collection.find(*key_to_find)
        return [result for result in results]

    else:
        return collection.find_one(*key_to_find)


def drop_document(session: MongoClient, database_name: str, collection_name: str, query_text: tuple[dict], multiple: bool = False):
    """
    Удаляет документ из коллекции
    """

    collection = get_collection(session=session, database_name=database_name, collection_name=collection_name)

    if multiple:
        collection.delete_many(*query_text)

    else:
        collection.delete_one(*query_text)


def drop_collection(session: MongoClient, database_name: str, collection_name: str):
    """
    Удаляет указанную коллекцию из базы данных возвращает словарь с результатом
    """

    database = get_database(session=session, database_name=database_name)
    result = database.drop_collection(collection_name)

    return result


def update_document(session: MongoClient, database_name: str, collection_name: str, query_text: tuple[dict],
                    multiple: bool = False):
    """
    Изменяет документ в соответствии с запросом, где
        query_text: tuple[dict], запрос вида ({'key': 'value'}, {$set: {key: value}})
    """

    collection = get_collection(session=session, database_name=database_name, collection_name=collection_name)

    if multiple:
        collection.update_many(*query_text)

    else:
        collection.update_one(*query_text)


def insert_document(session: MongoClient, database_name: str, collection_name: str, query_text: list[dict],
                    multiple: False):
    """
    Вставляет документ в выбранную коллекцию, где
        query_text: list[dict], запрос вида [{'key': 'value'}]
    """

    collection = get_collection(session=session, database_name=database_name, collection_name=collection_name)

    if multiple:
        collection.insert_many(query_text)

    else:
        collection.insert_one(*query_text)
