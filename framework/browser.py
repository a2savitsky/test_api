from .singleton_driver import SingleDriver
from .utils.json_utils import JsonUtils
from .logger import logger


class Browser:
    URL = ""
    IMPLICITLY_WAIT = JsonUtils('config.json').get_data('implicitly_wait')

    @staticmethod
    def open_url(url=None):
        if url is None:
            url = Browser.URL
        logger.info(f'Try to open url "{url}"')
        SingleDriver().get_driver().get(url)
        SingleDriver().get_driver().implicitly_wait(Browser.IMPLICITLY_WAIT)

    @staticmethod
    def quit_browser():
        SingleDriver().get_driver().quit()
        SingleDriver().del_driver()
