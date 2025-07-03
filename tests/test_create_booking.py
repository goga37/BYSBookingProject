import allure
import pytest
import requests
from pydantic import ValidationError
from core.models.booking import BookingResponse


@allure.feature("Создание бронирования")
@allure.story("Успешное создание бронирования")
def test_create_bocking(api_client, generate_random_booking_data):
    with allure.step("Отправка запроса на создание бронирования"):
        json_data = generate_random_booking_data
        response = api_client.create_booking(json_data)
        booking = response["booking"]
        try:
            BookingResponse(**response)
        except ValidationError as e:
            raise ValidationError(f'Response validation failed {e}')
    with allure.step("Проверка параметров в ответе на создание бронирования"):
        assert booking["firstname"] == json_data["firstname"], "firstname не совпал с ожидаемым"
        assert booking["lastname"] == json_data["lastname"], "lastname не совпал с ожидаемым"
        assert booking["totalprice"] == json_data["totalprice"], "totalprice не совпал с ожидаемым"
        assert booking["depositpaid"] == json_data["depositpaid"], "depositpaid не совпал с ожидаемым"
        assert booking["bookingdates"] == json_data["bookingdates"], "bookingdates не совпал с ожидаемым"
        assert booking["additionalneeds"] == json_data["additionalneeds"], "additionalneeds не совпал с ожидаемым"


@allure.feature("Создание бронирования")
@allure.story("Создание бронирования без передачи необязательного параметра additionalneeds")
def test_create_booking_without_additionalneeds(api_client, generate_random_booking_data):
    with allure.step("Отправка запроса на создание бронирования"):
        json_data = {
            "firstname": "Sally",
            "lastname": "Brown",
            "totalprice": 111,
            "depositpaid": True,
            "bookingdates": {
                "checkin": "2013-02-23",
                "checkout": "2014-16-23"
            }
        }
        response = api_client.create_booking(json_data)
        booking = response["booking"]
        try:
            BookingResponse(**response)
        except ValidationError as e:
            raise ValidationError(f'Response validation failed {e}')

    with allure.step("Проверка параметров в ответе на создание бронирования"):
        assert booking["firstname"] == json_data["firstname"], "firstname не совпал с ожидаемым"
        assert booking["lastname"] == json_data["lastname"], "lastname не совпал с ожидаемым"
        assert booking["totalprice"] == json_data["totalprice"], "totalprice не совпал с ожидаемым"
        assert booking["depositpaid"] == json_data["depositpaid"], "depositpaid не совпал с ожидаемым"
        assert booking["bookingdates"] == json_data["bookingdates"], "bookingdates не совпал с ожидаемым"


test_data = [
    {
        "lastname": "Brown",
        "totalprice": 111,
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2013-02-23",
            "checkout": "2014-10-23"
        },
        "additionalneeds": "Breakfast"
    },
    {
        "firstname": "Sally",
        "totalprice": 111,
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2013-02-23",
            "checkout": "2014-10-23"
        },
        "additionalneeds": "Breakfast"
    },
    {
        "firstname": "Sally",
        "lastname": "Brown",
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2013-02-23",
            "checkout": "2014-10-23"
        },
        "additionalneeds": "Breakfast"
    },
    {
        "firstname": "Sally",
        "lastname": "Brown",
        "totalprice": 111,
        "bookingdates": {
            "checkin": "2013-02-23",
            "checkout": "2014-10-23"
        },
        "additionalneeds": "Breakfast"
    },
    {
        "firstname": "Sally",
        "lastname": "Brown",
        "totalprice": 111,
        "depositpaid": True,
        "bookingdates": {
            "checkout": "2014-10-23"
        },
        "additionalneeds": "Breakfast"
    },
    {
        "firstname": "Sally",
        "lastname": "Brown",
        "totalprice": 111,
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2013-02-23",
        },
        "additionalneeds": "Breakfast"
    }
]

test_ids = [
    "Missing firstname",
    "Missing lastname",
    "Missing totalprice",
    "Missing depositpaid",
    "Missing bookingdates.checkin",
    "Missing bookingdates.checkout"
]

@pytest.mark.parametrize("json_data", test_data, ids=test_ids)
@allure.feature("Создание бронирования")
@allure.story("Негативные проверки на обязательные параметры")
def test_missing_required_fields(api_client, json_data):
    with allure.step("Отправка запроса и проверка статус-кода ошибки"):
        with pytest.raises(requests.exceptions.HTTPError) as exc_info:
            api_client.create_booking(json_data)
        assert exc_info.value.response.status_code == 500



@allure.feature("Test Ping")
@allure.story("Test server unavailable")
def test_server_unavailable(api_client, mocker, generate_random_booking_data):
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
