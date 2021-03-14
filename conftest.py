import pytest
from .framework.browser import Browser


@pytest.fixture()
def browser():
    yield
    Browser.quit_browser()
