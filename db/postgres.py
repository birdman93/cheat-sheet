import psycopg2
from psycopg2._psycopg import connection


# переменные
current_connections: list[connection] = []  # активное подключение к базе данных


# структуры данных
class QueryResult:
    """
    Результат запроса к БД
    """

    def __init__(self) -> None:
        self.rowcount: int = 0
        """кол-во строк полученных/обработанных по запросу"""

        self.first_row: dict = {}
        """результаты первой строки"""

        self.rows: list[dict] = []
        """вывод запроса (каждая строка словарь имя_столбца:значение)"""


# функции
def new_database_connection(host: str = None,
                            port: str = None,
                            user: str = None,
                            password: str = None,
                            database_name: str = None) -> connection:
    """
    Устанавливает подключение к БД, согласно конфигу
    """
    db_conn = psycopg2.connect(host=host,
                               port=port,
                               user=user,
                               password=password,
                               database=database_name)

    return db_conn


def find_conn(host: str = None,
              port: str = None,
              user: str = None,
              password: str = None,
              database_name: str = None) -> connection:
    """
    Проверяет наличие активного подключения к конкретной бд
    """

    selected_conn: connection = None

    for conn in current_connections:
        if conn.info.dbname == database_name:
            selected_conn = conn
            break

    if selected_conn is not None:

        try:
            cursor = selected_conn.cursor()
            cursor.execute("SELECT 1")

        except psycopg2.OperationalError:
            current_connections.remove(selected_conn)
            selected_conn = new_database_connection(host=host,
                                                    port=port,
                                                    user=user,
                                                    password=password,
                                                    database_name=database_name)
            current_connections.append(selected_conn)

    else:
        selected_conn = new_database_connection(host=host,
                                                port=port,
                                                user=user,
                                                password=password,
                                                database_name=database_name)
        current_connections.append(selected_conn)

    return selected_conn


def select_query(text_query: str,
                 host: str = None,
                 port: str = None,
                 user: str = None,
                 password: str = None,
                 database_name: str = None) -> QueryResult:
    """
    Выполняет запрос и возвращает результат
        text_query - текст запроса
        database_name - имя БД, в которую будем делать запрос
    """

    conn = find_conn(
        host=host,
        port=port,
        user=user,
        password=password,
        database_name=database_name
    )

    res = QueryResult()

    with conn.cursor() as cursor:
        cursor.execute(text_query)

        # названия колонок
        clmn_names = [column[0] for column in cursor.description]

        # результаты
        res_values = cursor.fetchall()

        try:
            # первая строка
            res.first_row = (dict(zip(clmn_names, res_values[0])))

        except IndexError:
            res.first_row = {}

        # общая длина
        res.rowcount = len(res_values)

        # все результаты
        for row in res_values:
            res.rows.append(dict(zip(clmn_names, row)))

    return res


def crud_query(text_query: str,
               host: str = None,
               port: str = None,
               user: str = None,
               password: str = None,
               database_name: str = None) -> int:
    """
    Создает / обновляет / удаляет данные по запросу, возвращает кол-во обновленных строк
        text_query: str, текст запроса
        database_name: str имя БД в которую будем делать запрос
    """

    conn = find_conn(
        host=host,
        port=port,
        user=user,
        password=password,
        database_name=database_name
    )

    with conn.cursor() as cursor:
        cursor.execute(text_query)

        rowcount = cursor.rowcount

        conn.commit()

    return rowcount
