def load_local_storage_data(driver, link, path_to_file):
    """
    Загрузка в браузер ранее записанных данных localStorage
    """

    # Открытие приложения
    driver.get(link)

    # Парсинг данных из файла, обновленного при авторизации, и их подгрузка в локал сторедж
    with open(path_to_file, 'r', encoding='UTF-8') as file:
        lines = [i.split('~') for i in file.readlines()]
        for line in lines:
            driver.execute_script(f"localStorage.setItem('{line[0].strip()}', '{line[1].strip()}');")

    # Обновление страницы для перехода в интерфейс авторизованного юзера
    driver.refresh()
