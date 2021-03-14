from ..framework.utils.api_utils import APIUtils
from ..framework.utils.json_utils import JsonUtils


class RuapmApi(APIUtils):

    URL = JsonUtils('config.json').get_data('url_local')

    def __init__(self):
        super().__init__(url=self.URL)

    def registration(self, username, password, exp_status_code=None):
        data = {"user": {"login": username, "password": password}}
        return self._post(path='api/v1/user/registration', json=data, exp_status_code=exp_status_code)

    def authorisation(self, username, password, exp_status_code=None):
        data = {"user": {"login": username, "password": password}}
        return self._post(path='api/v1/user/login', json=data, exp_status_code=exp_status_code)

    def get_ssid(self, username, password):
        return self.authorisation(username, password, 200)["result"]["ssid"]

    def get_user(self, ssid, exp_status_code=None):
        headers = {"ssid": ssid}
        return self._get(path='api/v1/user', headers=headers, exp_status_code=exp_status_code)

    def add_user_contact(self, ssid, contact_type, contact, exp_status_code=None):
        headers = {"ssid": ssid}
        data = {"contact": {"type": contact_type, "content": contact}}
        return self._post(path='api/v1/user/contact', json=data, headers=headers, exp_status_code=exp_status_code)

    def delete_user_contact(self, ssid, contact_id, exp_status_code=None):
        headers = {"ssid": ssid}
        return self._delete(path=f'api/v1/user/contact/{contact_id}', headers=headers, exp_status_code=exp_status_code)
