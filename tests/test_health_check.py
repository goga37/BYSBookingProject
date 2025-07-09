import allure
import pytest
import requests


@allure.feature("Test Ping")
@allure.story("Test connection")
def test_ping(api_client):
    status_cod = api_client.ping()
    assert status_cod == 201, f"Expected status 201 but got {status_cod}"

@allure.feature("Test Ping")
@allure.story("Test server unavailable")
def test_server_unavailable(api_client, mocker):
    mocker.patch.object(api_client.session, 'get', side_effect=Exception("Server unavailable"))
    with pytest.raises(Exception, match="Server unavailable"):
        api_client.get_booking_ids()

@allure.feature("Test wrong HTTP method")
@allure.story("Test wrong HTTP method")
def test_ping_returns_405_method_not_allowed(api_client, mocker):
    mock_response = mocker.Mock()
    mock_response.status_code = 405
    mocker.patch.object(api_client.session, 'get', return_value=mock_response)
    with (pytest.raises(AssertionError, match="Expected status 201 but got 405")):
        api_client.ping()

@allure.feature("Test wrong HTTP method")
@allure.story("Not Found")
def test_ping_returns_404_not_found(api_client, mocker):
    mock_response = mocker.Mock()
    mock_response.status_code = 404
    mocker.patch.object(api_client.session, 'get', return_value=mock_response)
    with pytest.raises(AssertionError, match="Expected status 201 but got 404"):
        api_client.ping()

@allure.feature("Test wrong HTTP method")
@allure.story("Unexpected 200 OK when 201 expected")
def test_ping_returns_200_instead_of_201(api_client, mocker):
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mocker.patch.object(api_client.session, 'get', return_value=mock_response)
    with pytest.raises(AssertionError, match="Expected status 201 but got 200"):
        api_client.ping()

@allure.feature("Test wrong HTTP method")
@allure.story("Timeout handling")
def test_ping_timeout_exception(api_client, mocker):
    mocker.patch.object(api_client.session, 'get', side_effect=requests.Timeout)
    with pytest.raises(requests.Timeout):
        api_client.ping()

