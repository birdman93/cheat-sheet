def get_session_storage_data(driver, session_storage_path, token_path):
    """
    Записываем в файл данные из sessionStorage
    """

    data = dict(driver.execute_script("return window.sessionStorage;"))

    # Clearing the file
    with open(session_storage_path, 'w', encoding='UTF-8') as file:
        pass

    # Writing data to a file
    for key, value in data.items():
        with open(session_storage_path, 'a', encoding='UTF-8') as file:
            if key not in ['clear', 'getItem', 'key', 'length', 'removeItem', 'setItem']:
                print(f"{key}~{value}", file=file)

    with open(session_storage_path, 'r', encoding='UTF-8') as file:
        lines = [i.split('~') for i in file.readlines()]

        for line in lines:
            if ('"credentialType":"IdToken"' in line[1]) and ('secret' in line[1]):

                data = line[1].replace('{', '').replace('}', '')

                for item in data.split(','):
                    if 'secret' in item:
                        item = item.split(':')
                        token = item[1].replace('"', '')
                        break

                with open(token_path, 'w', encoding='UTF-8') as file2:
                    print(token, file=file2)
                return token


def load_session_storage_data(driver, link, session_storage_path):
    """
    Загрузка в браузер ранее записанных данных sessionStorage
    """

    driver.get(link)

    with open(session_storage_path, 'r', encoding='UTF-8') as file:
        lines = [i.split('~') for i in file.readlines()]
        for line in lines:
            driver.execute_script(f"sessionStorage.setItem('{line[0].strip()}', '{line[1].strip()}');")

    driver.get(link)
