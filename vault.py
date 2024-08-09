import hvac
import urllib3

import config


class Vault:

    def __init__(self, username: str = None, password: str = None):

        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        self.host = config.vault_host
        self.client = None

        self.token = self.auth(username=username, password=password)

    def auth(self, username: str = None, password: str = None):

        self.client = hvac.Client(url=self.host, verify=False)
        login_response = self.client.auth.ldap.login(username, password)

        if not self.client.is_authenticated():
            raise Exception("Не удалось авторизоваться в Vault")

        return login_response['auth']['client_token']

    def get_secret_value(self, path: str, secret: str):
        try:
            vault_dir = self.client.read(path)
        except Exception:
            raise ConnectionError(f'Нет прав для чтения: {path}')

        if vault_dir:
            password = vault_dir['data'].get(secret)
            if not password:
                raise ValueError(f'Секрет ({secret}) не найден по указанному пути: {path}')
            return password
        else:
            raise ValueError(f'Путь ({path}) не существует')
        