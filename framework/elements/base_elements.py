from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from ..utils.json_utils import JsonUtils
from ..logger import logger
from ..singleton_driver import SingleDriver


explicitly_wait = JsonUtils('config.json').get_data('explicitly_wait')


class BaseElement:
    def __init__(self, locator=None):
        self.locator = locator
        self.browser = SingleDriver().get_driver()
        self.wait = WebDriverWait(self.browser, explicitly_wait)

    def find_element(self):
        logger.info(f'Finding element with locator: "{self.locator[1]}"')
        return self.wait.until(EC.presence_of_element_located(self.locator))

    def get_text(self):
        logger.info(f'Getting text from element with locator: "{self.locator[1]}"')
        return self.find_element().text
