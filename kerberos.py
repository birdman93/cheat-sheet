import subprocess
import logging


class Kerberos:

    def __init__(self, user, keytab_path):
        self.user = user
        self.keytab_path = keytab_path
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

    def kinit(self):
        kinit_command = f'kinit -kt {self.keytab_path} {self.user}'
        try:
            self.logger.info(f'Выполнение команды kinit -kt {self.keytab_path} {self.user}')
            subprocess.check_output(kinit_command, shell=True, universal_newlines=True)
            self.logger.info('Kerberos ticket успешно получен')
        except subprocess.CalledProcessError as error:
            raise RuntimeError(f'Ошибка при получении Kerberos ticket: {error.output}')

    def kdestroy(self):
        try:
            self.logger.info('Выполнение команды kdestroy')
            subprocess.check_output('kdestroy', shell=True, universal_newlines=True)
            self.logger.info('Kerberos ticket успешно уничтожен')
        except subprocess.CalledProcessError as error:
            raise RuntimeError(f'Ошибка при уничтожении Kerberos ticket: {error.output}')

    def __enter__(self):
        self.kinit()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.kdestroy()
