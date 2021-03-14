from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from .utils.json_utils import JsonUtils
from os.path import abspath
from selenium.webdriver.support.events import EventFiringWebDriver
from .logger import MyListener

data = JsonUtils('config.json')
br_name = data.get_data('browser')
lang = data.get_data('lang')
downloads_path = abspath(data.get_data('downloads_path'))


class SingleDriver:
    instance = None

    @classmethod
    def get_driver(cls):
        if cls.instance is None:
            if br_name == "firefox":
                profile = webdriver.FirefoxProfile()
                profile.set_preference("browser.download.folderList", 2)
                profile.set_preference('intl.accept_languages', f'{lang}')
                profile.set_preference('browser.helperApps.neverAsk.saveToDisk', "application/octet-stream,text/csv")
                profile.set_preference("browser.download.manager.showWhenStarting", False)
                profile.set_preference("browser.download.dir", f'{downloads_path}')
                cls.instance = webdriver.Firefox(executable_path=GeckoDriverManager().install(), firefox_profile=profile)
            elif br_name == "chrome":
                options = webdriver.ChromeOptions()
                prefs = {'safebrowsing.enabled': 'false', 'intl.accept_languages': f'{lang}',
                         'download.default_directory': f'{downloads_path}'}
                options.add_experimental_option("prefs", prefs)
                cls.instance = EventFiringWebDriver(webdriver.Chrome(ChromeDriverManager().install(), options=options),
                                                    MyListener())
            else:
                raise Exception('Name of browser is incorrect!')
        return cls.instance

    @classmethod
    def del_driver(cls):
        cls.instance = None
