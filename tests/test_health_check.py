import allure


@allure.feature("Test Ping")
@allure.story("Test connection")
def test_ping(api_client):
    status_cod = api_client.ping()
    assert status_cod == 201, f"Expected status 201 but got {status_cod}"