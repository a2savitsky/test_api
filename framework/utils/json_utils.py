import json
from ..logger import logger


class JsonUtils:
    def __init__(self, file):
        self.file = file

    def get_data(self, key):
        logger.info(f'Reading "{key}" from json file')
        with open(self.file, 'r', encoding='utf8') as f:
            data = json.load(f)
        return data[key]

    @staticmethod
    def convert_string_to_json(string):
        return json.loads(string)
