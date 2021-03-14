from .elements.label import Label


class BasePage:
    def __init__(self, locator=None):
        self.locator = locator

    def is_page_open(self):
        return Label(self.locator).find_element().is_displayed()
