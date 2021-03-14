import requests


class APIUtils:

    def __init__(self, url):
        self._url = url

    def _post(self, path="", data=None, json=None, headers=None, exp_status_code=None):
        response = requests.post(url=self._url + path, data=data, json=json, headers=headers)
        if exp_status_code is not None:
            self.__check_status_code(response, exp_status_code)
        return response.json()

    def _get(self, path="", params=None, headers=None, exp_status_code=None):
        response = requests.get(url=self._url + path, params=params, headers=headers)
        if exp_status_code is not None:
            self.__check_status_code(response, exp_status_code)
        return response.json()

    def _delete(self, path="", params=None, headers=None, exp_status_code=None):
        response = requests.delete(url=self._url + path, params=params, headers=headers)
        if exp_status_code is not None:
            self.__check_status_code(response, exp_status_code)
        return response.json()

    @staticmethod
    def __check_status_code(response, exp_status_code):
        assert response.status_code == exp_status_code, f'Expected status code is: {exp_status_code}, but actual: {response.status_code}'
