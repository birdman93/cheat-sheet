import aerospike
from aerospike import exception as ex


class AerospikeClient:
    """
    Класс для Aerospike, позволяющий работать с его объектами с помощью контекстного менеджера with, дабы закрытие
    соединения выполнялось автоматически
    """

    def __init__(self, config):
        self.config = config
        self.client = None

    def __enter__(self):
        self.client = aerospike.client(self.config).connect()
        print('connected')
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.client:
            self.client.close()

    def create(self, namespace, set_name, key, bins):

        try:
            self.client.put((namespace, set_name, key), bins)

        except ex.RecordExistsError:
            raise ValueError("Запись уже существует")

        except Exception as e:
            raise ValueError(e)

    def read(self, namespace, set_name, key):

        try:
            (key, metadata, record) = self.client.get((namespace, set_name, key))
            return record

        except ex.RecordNotFound:
            return None

        except Exception as e:
            raise ValueError(e)

    def update(self, namespace, set_name, key, bins):

        try:
            self.client.put((namespace, set_name, key), bins)

        except Exception as e:
            raise ValueError({e})

    def delete(self, namespace, set_name, key):

        try:
            self.client.remove((namespace, set_name, key))

        except ex.RecordNotFound:
            raise ValueError("Запись не найдена")

        except Exception as e:
            raise ValueError(e)
