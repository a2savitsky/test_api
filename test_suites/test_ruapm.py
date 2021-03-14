import pytest
from ..framework.utils.random_utils import RandomUtils
from ..framework.browser import Browser
from ..pages.user_page import UserPage
from ..ruapm_utils.ruapm_api_utils import RuapmApi

ruapm_api = RuapmApi()

login_max_length = 50
login_min_length = 3
passwd_max_length = 25
passwd_min_length = 5
contact_max_length = 25
contact_min_length = 1


@pytest.mark.parametrize('login, passwd', [
    (RandomUtils.get_random_text(login_min_length), RandomUtils.get_random_text(passwd_min_length)),
    (RandomUtils.get_random_text(login_max_length), RandomUtils.get_random_text(passwd_min_length))])
def test_user_name_on_page_is_correct(login, passwd, browser):
    ruapm_api.registration(login, passwd, 201)
    Browser.open_url(ruapm_api.URL + "session/" + ruapm_api.get_ssid(login, passwd))
    user_page = UserPage()
    assert user_page.is_page_open() is True, 'User page is not open'
    user_page.is_user_name_correct(login)


@pytest.mark.parametrize('login, passwd', [
    (RandomUtils.get_random_text(login_min_length), RandomUtils.get_random_text(passwd_max_length)),
    (RandomUtils.get_random_text(login_max_length), RandomUtils.get_random_text(passwd_min_length))])
def test_registration_new_user_with_valid_cred(login, passwd):
    response = ruapm_api.registration(login, passwd, 201)
    assert response['success'] is True, 'Response came with error'
    assert response['result']['user']['login'] == login, "Login in the response doesn't match with expected"


@pytest.mark.parametrize('login, passwd', [
    (RandomUtils.get_random_text(login_min_length), RandomUtils.get_random_text(passwd_min_length))])
def test_registration_user_which_already_exist(login, passwd):
    ruapm_api.registration(login, passwd, 201)
    response = ruapm_api.registration(login, RandomUtils.get_random_text(passwd_min_length), 400)
    assert response['success'] is False, 'Response came with success'
    assert response['error'] == 'User already exist', 'Error field is not as expected'


@pytest.mark.parametrize('login, passwd', [
    (RandomUtils.get_random_text(login_min_length - 1), RandomUtils.get_random_text(passwd_max_length)),
    (RandomUtils.get_random_text(login_max_length + 1), RandomUtils.get_random_text(passwd_min_length)),
    (RandomUtils.get_random_text(login_min_length), RandomUtils.get_random_text(passwd_max_length + 1)),
    (RandomUtils.get_random_text(login_max_length), RandomUtils.get_random_text(passwd_min_length - 1))])
def test_registration_new_user_with_no_valid_cred(login, passwd):
    response = ruapm_api.registration(login, passwd, 400)
    assert response['success'] is False, 'Response came with success'
    assert response['error'].startswith("Invalid field"), 'Error field is not as expected'


@pytest.mark.parametrize('login, passwd', [
    (RandomUtils.get_random_text(login_min_length), RandomUtils.get_random_text(passwd_max_length))])
def test_authorisation_with_valid_cred(login, passwd):
    ruapm_api.registration(login, passwd, 201)
    response = ruapm_api.authorisation(login, passwd, 200)
    assert response['success'] is True, 'Response came with error'
    assert response['result']['user']['login'] == login, "Login in the response doesn't match with expected"


@pytest.mark.parametrize('login, passwd', [
    (RandomUtils.get_random_text(login_min_length), RandomUtils.get_random_text(passwd_max_length))])
def test_authorisation_with_invalid_login(login, passwd):
    ruapm_api.registration(login, passwd, 201)
    response = ruapm_api.authorisation(login + "a", passwd, 200)  # статус код должен быть 400, но возв-т 200
    assert response['success'] is False, 'Response came with success'
    assert response['error'] == 'User not found', 'Error field is not as expected'


@pytest.mark.parametrize('login, passwd', [
    (RandomUtils.get_random_text(login_min_length), RandomUtils.get_random_text(passwd_min_length))])
def test_authorisation_with_invalid_password(login, passwd):
    ruapm_api.registration(login, passwd, 201)
    response = ruapm_api.authorisation(login, passwd + "a", 200)  # статус код должен быть 400, но возв-т 200
    assert response['success'] is False, 'Response came with success'
    assert response['error'] == 'Incorrect password', 'Error field is not as expected'


@pytest.mark.parametrize('login, passwd', [
    (RandomUtils.get_random_text(login_max_length), RandomUtils.get_random_text(passwd_min_length))])
def test_get_user_data(login, passwd):
    ruapm_api.registration(login, passwd, 201)
    response = ruapm_api.get_user(ruapm_api.get_ssid(login, passwd), 200)
    assert response['success'] is True, 'Response came with error'
    assert response['result']['user']['login'] == login, "Login in the response doesn't match with expected"
    assert len(response['result']['user']['contacts']) == 0, "List of contacts is not empty"


@pytest.mark.parametrize('login, passwd, contact_type, contact', [
    (RandomUtils.get_random_text(login_max_length), RandomUtils.get_random_text(passwd_min_length),
     "email", RandomUtils.get_random_text(contact_max_length)),
    (RandomUtils.get_random_text(login_max_length), RandomUtils.get_random_text(passwd_min_length),
     "phone", RandomUtils.get_random_text(contact_min_length))])
def test_add_user_valid_contact(login, passwd, contact_type, contact):
    ruapm_api.registration(login, passwd, 201)
    response = ruapm_api.add_user_contact(ruapm_api.get_ssid(login, passwd), contact_type, contact, 200)
    assert response['success'] is True, 'Response came with error'
    assert response['result']['user']['contacts'][0]['type'] == contact_type, \
        "Type of contact in the response doesn't match with expected"
    assert response['result']['user']['contacts'][0]['content'] == contact, \
        "Contact in the response doesn't match with expected"


@pytest.mark.parametrize('login, passwd, contact_type, contact', [
    (RandomUtils.get_random_text(login_max_length), RandomUtils.get_random_text(passwd_min_length),
     "email", RandomUtils.get_random_text(contact_max_length + 1)),
    (RandomUtils.get_random_text(login_max_length), RandomUtils.get_random_text(passwd_min_length),
     "phone", RandomUtils.get_random_text(contact_min_length - 1)),
    (RandomUtils.get_random_text(login_max_length), RandomUtils.get_random_text(passwd_min_length),
     "e-mail", RandomUtils.get_random_text(contact_max_length)),
    (RandomUtils.get_random_text(login_max_length), RandomUtils.get_random_text(passwd_min_length),
     "phon", RandomUtils.get_random_text(contact_min_length))])
def test_add_user_invalid_contact(login, passwd, contact_type, contact):
    ruapm_api.registration(login, passwd, 201)
    response = ruapm_api.add_user_contact(ruapm_api.get_ssid(login, passwd), contact_type, contact, 400)
    assert response['success'] is False, 'Response came with success'
    assert response['error'].startswith("Invalid field"), 'Error field is not as expected'


@pytest.mark.parametrize('login, passwd, contact_type, contact', [
    (RandomUtils.get_random_text(login_max_length), RandomUtils.get_random_text(passwd_min_length),
     "email", RandomUtils.get_random_text(contact_max_length)),
    (RandomUtils.get_random_text(login_max_length), RandomUtils.get_random_text(passwd_min_length),
     "phone", RandomUtils.get_random_text(contact_min_length))])
def test_add_user_contact_which_already_exist(login, passwd, contact_type, contact):
    ruapm_api.registration(login, passwd, 201)
    ruapm_api.add_user_contact(ruapm_api.get_ssid(login, passwd), contact_type, contact, 200)
    response = ruapm_api.add_user_contact(ruapm_api.get_ssid(login, passwd), contact_type, contact, 400)
    assert response['success'] is False, 'Response came with success'
    assert response['error'] == 'Contact already exist', 'Error field is not as expected'


@pytest.mark.parametrize('login, passwd, contact_type, contact', [
    (RandomUtils.get_random_text(login_max_length), RandomUtils.get_random_text(passwd_min_length),
     "email", RandomUtils.get_random_text(contact_max_length))])
def test_delete_user_contact(login, passwd, contact_type, contact):
    ruapm_api.registration(login, passwd, 201)
    contact_id = ruapm_api.add_user_contact(ruapm_api.get_ssid(login, passwd),
                                            contact_type, contact, 200)['result']['user']['contacts'][0]['id']
    response = ruapm_api.delete_user_contact(ruapm_api.get_ssid(login, passwd), contact_id, 200)
    assert response['success'] is True, 'Response came with error'
    assert len(response['result']['user']['contacts']) == 0, "List of contacts is not empty"


@pytest.mark.parametrize('login, passwd, contact_type, contact', [
    (RandomUtils.get_random_text(login_max_length), RandomUtils.get_random_text(passwd_min_length),
     "email", RandomUtils.get_random_text(contact_max_length))])
def test_delete_user_contact_which_not_exist(login, passwd, contact_type, contact):
    ruapm_api.registration(login, passwd, 201)
    contact_id = ruapm_api.add_user_contact(ruapm_api.get_ssid(login, passwd),
                                            contact_type, contact, 200)['result']['user']['contacts'][0]['id']
    response = ruapm_api.delete_user_contact(ruapm_api.get_ssid(login, passwd), contact_id + 1, 400)
    assert response['success'] is False, 'Response came with success'
    assert response['error'] == 'Nothing to remove', 'Error field is not as expected'
