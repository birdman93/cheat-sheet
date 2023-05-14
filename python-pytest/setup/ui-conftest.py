import pytest
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from selenium import webdriver


def pytest_addoption(parser):
    """
    Создание параметров запуска тестов, управлять которыми нужно из консоли
    """

    parser.addoption('--browser_name',
                     action='store',
                     default='chrome',
                     help='choose browser: chrome or firefox',
                     choices=('chrome', 'firefox'))

    parser.addoption('--window_size',
                     action='store',
                     default='1920,1080',
                     help='choose browser: chrome or firefox',
                     choices=('3840,2160',
                              '2560,1440', '2048,1152',
                              '1920,1080', '1920,1440', '1920,1200',
                              '1680,1050', '1680,900',
                              '1440,1050', '1440,900',
                              '1280,1024', '1280,960', '1280,800', '1280,768', '1280,720', '1280,600'))

    parser.addoption('--headless',
                     action='store',
                     default='true',
                     help='choose browser: chrome or firefox',
                     choices=('true', 'false'))


@pytest.fixture(scope="module", autouse=True)
def setup_module(request):

    # Сюда пишем то, что должно выполниться перед всеми тестами в этом файле

    # Определяем название браузера из параметров запуска
    request.keywords['browser_name'] = request.config.getoption('browser_name')
    request.keywords['window_size'] = request.config.getoption('window_size')
    request.keywords['headless'] = request.config.getoption('headless')

    yield

    # Сюда пишем то, что должно выполниться после всех тестов в этом файле


@pytest.fixture(scope='function')
def browser(request):

    browser_name = request.keywords['browser_name']
    window_size = request.keywords['window_size']

    browser = None
    if browser_name == 'chrome':

        options = webdriver.ChromeOptions()
        options.add_argument("--no-sandbox")
        options.add_argument(f"--window-size={window_size}")
        if request.keywords['headless'] == 'true':
            options.add_argument("-headless")

        options.set_capability("loggingPrefs", {'performance': 'ALL'})

        browser = webdriver.Chrome(executable_path=ChromeDriverManager().install(), options=options)

    elif browser_name == 'firefox':

        options = webdriver.FirefoxOptions()
        options.add_argument(f"--width={window_size.split(',')[0]}")
        options.add_argument(f"--height={window_size.split(',')[1]}")
        if request.keywords['headless'] == 'true':
            options.add_argument("-headless")

        browser = webdriver.Firefox(executable_path=GeckoDriverManager().install(), options=options)

    else:
        raise pytest.UsageError('-- choose browser name and get as param')

    browser.implicitly_wait(10)

    yield browser

    browser.quit()
