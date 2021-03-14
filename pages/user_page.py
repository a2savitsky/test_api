from selenium.webdriver.common.by import By
from ..framework.base_page import BasePage
from ..framework.elements.label import Label


class UserPage(BasePage):
    PAGE_LOCATOR = (By.XPATH, '//table')
    USER_LABEL_LOCATOR_1 = (By.XPATH, '//h1/span[@class="username"]')
    USER_LABEL_LOCATOR_2 = (By.XPATH, '//h2/span[@class="username"]')

    def __init__(self):
        super().__init__(locator=self.PAGE_LOCATOR)

    def is_user_name_correct(self, expected_user_name):
        actual_user_name_1 = Label(self.USER_LABEL_LOCATOR_1).get_text()
        actual_user_name_2 = Label(self.USER_LABEL_LOCATOR_2).get_text()
        assert expected_user_name == actual_user_name_1, f"Expected user name is: {expected_user_name}, but actual: {actual_user_name_1}"
        assert expected_user_name == actual_user_name_2, f"Expected user name is: {expected_user_name}, but actual: {actual_user_name_2}"
