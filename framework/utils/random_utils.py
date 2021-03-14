import random
import string
from ..logger import logger


class RandomUtils:

    @staticmethod
    def get_random_text(length: int):
        random_text = "".join([random.choice(string.ascii_letters) for i in range(length)])
        logger.info(f'Getting random text "{random_text}"')
        return random_text

    @staticmethod
    def get_random_number(length: int):
        random_number = int("".join([random.choice(string.digits) for i in range(length)]))
        logger.info(f'Getting random number "{random_number}"')
        return random_number
