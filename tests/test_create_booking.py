import allure
import pytest
import requests


@allure.feature("Test Ping")
@allure.story("Test connection")
def test_ping(api_client,generate_random_booking_data):
    json_data = generate_random_booking_data
    json_create_booking = api_client.create_booking(json_data)
    assert json_create_booking["firstname"] == json_data["firstname"], "firstname не совпал с ожидаемым"
    assert json_create_booking["lastname"] == json_data["lastname"], "lastname не совпал с ожидаемым"
    assert json_create_booking["totalprice"] == json_data["totalprice"], "totalprice не совпал с ожидаемым"
    assert json_create_booking["depositpaid"] == json_data["depositpaid"], "depositpaid не совпал с ожидаемым"
    assert json_create_booking["bookingdates"] == json_data["bookingdates"], "bookingdates не совпал с ожидаемым"
    assert json_create_booking["additionalneeds"] == json_data["additionalneeds"], "additionalneeds не совпал с ожидаемым"


@allure.feature("Test Ping")
@allure.story("Test server unavailable")
def test_server_unavailable(api_client, mocker):
    mocker.patch.object(api_client.session, 'get', side_effect=Exception("Server unavailable"))
    with pytest.raises(Exception, match="Server unavailable"):
        api_client.get_booking_ids()