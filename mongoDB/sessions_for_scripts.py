import pymongo
import time


def script_for_mongo(db_host: str,
                     db_port: int,
                     db_prefix: str,
                     db_name: str,
                     collection_name: str,
                     query: dict):

    # Открытие соединения с MongoDB
    with pymongo.MongoClient(f"mongodb://{db_host}:{db_port}/") as client:

        # Соединение с Монгой живет около 30 минут, поэтому следует следить за временем и обновлять сессию
        session = client.start_session()
        session_start_session = time.time()

        # Определяем целевые БД и коллекцию
        db = client[f'{db_prefix}_{db_name}']
        collection = db[collection_name]

        # Установка тайм-аута в 600 секунд (если коллекция большая)
        timeout_ms = 600000

        # Поиск документов, удовлетворяющих условиям (если коллекция большая, нужен параметр no_cursor_timeout,
        # иначе будут падения по таймауту)
        mongo_docs = collection.find(query, no_cursor_timeout=True).max_time_ms(max_time_ms=timeout_ms)

        # Получение документов по одному
        try:
            while True:

                # Рефрешим сессию в монге каждые 25 минут (если работаем с апи, то тут же можем обновлять токен)
                if time.time() - session_start_session > 25 * 60:
                    session.end_session()
                    session = client.start_session()
                    session_start_session = time.time()
                    print("Сессия обновлена", flush=True)

                mongo_doc = mongo_docs.next()

                # Core-логика скрипта тут

        except StopIteration:
            mongo_docs.close()
