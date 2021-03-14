import logging
from selenium.webdriver.support.events import AbstractEventListener


class Logger:

    def __init__(self, logger):
        self.logger = logging.getLogger(logger)
        self.logger.setLevel(logging.DEBUG)
        fh = logging.FileHandler('./log_file.log')
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
        self.logger.addHandler(fh)

    def get_logger(self):
        return self.logger


logger = Logger('MyLogger').get_logger()


class MyListener(AbstractEventListener):

    def on_exception(self, exception, driver):
        logger.error(f'Exception {exception} is appear')

    def before_quit(self, driver):
        logger.info("Test is quitting")

    def after_quit(self, driver):
        logger.info("Test quit")
