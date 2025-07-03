import allure
import pytest
import requests


@allure.feature("Test Ping")
@allure.story("Test connection")
def test_ping(api_client,generate_random_booking_data):
    json_data = generate_random_booking_data
    json_create_booking = api_client.create_booking(json_data)

    booking = json_create_booking["booking"]
    assert booking["firstname"] == json_data["firstname"], "firstname не совпал с ожидаемым"
    assert booking["lastname"] == json_data["lastname"], "lastname не совпал с ожидаемым"
    assert booking["totalprice"] == json_data["totalprice"], "totalprice не совпал с ожидаемым"
    assert booking["depositpaid"] == json_data["depositpaid"], "depositpaid не совпал с ожидаемым"
    assert booking["bookingdates"] == json_data["bookingdates"], "bookingdates не совпал с ожидаемым"
    assert booking["additionalneeds"] == json_data["additionalneeds"], "additionalneeds не совпал с ожидаемым"


@allure.feature("Test Ping")
@allure.story("Test server unavailable")
def test_server_unavailable(api_client, mocker,generate_random_booking_data):
    json_data = generate_random_booking_data
    mocker.patch.object(api_client.session, 'post', side_effect=Exception("Server unavailable"))
    with pytest.raises(Exception, match="Server unavailable"):
        api_client.create_booking(json_data)

# @allure.feature("Test wrong HTTP method")
# @allure.story("Test wrong HTTP method")
# def test_ping_returns_405_method_not_allowed(api_client, mocker,generate_random_booking_data):
#     json_data = generate_random_booking_data
#     mock_response = mocker.Mock()
#     mock_response.json.return_value = {
#     "bookingid": 1,
#     "booking": {
#         "firstname": "Jim",
#         "lastname": "Brown",
#         "totalprice": 111,
#         "depositpaid": True,
#         "bookingdates": {
#             "checkin": "2018-01-01",
#             "checkout": "2019-01-01"
#         },
#         "additionalneeds": "Breakfast"
#     }
# }
#     mocker.patch.object(api_client.session, 'post', return_value=mock_response)
#     with (pytest.raises(AssertionError, match="firstname не совпал с ожидаемым")):
#         api_client.create_booking(json_data)