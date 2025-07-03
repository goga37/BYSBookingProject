import requests
import os
from dotenv import load_dotenv
from core.settings.environments import Environment
import allure
from core.clients.endpoints import Endpoints
from core.settings.config import AdminCredentials, Timeouts
from requests.auth import HTTPBasicAuth

load_dotenv()
os.environ['ENVIRONMENT'] = 'PROD'

class APIClient:
    def __init__(self):
        environment_str = os.getenv('ENVIRONMENT')
        try:
            environment = Environment[environment_str]
        except KeyError:
            raise KeyError(f"Environment '{environment_str}' not found.")

        self.base_url = self.get_base_url(environment)
        self.session = requests.Session()

    def get_base_url(self, environment: Environment) -> str:
        if environment == Environment.TEST:
            return os.getenv('TEST_BASE_URL')
        elif environment == Environment.PROD:
            return os.getenv('PROD_BASE_URL')
        else:
            raise ValueError(f"Unsupported environment: {environment}")

    def get(self, endpoint, params=None, status_code=200):
        url = self.base_url + endpoint
        response = requests.get(url, headers=self.headers, params=params)
        if status_code:
            assert response.status_code == status_code
        return response.json()

    def post(self, endpoint, data=None, status_code=200):
        url = self.base_url + endpoint
        response = requests.post(url, headers=self.headers, json=data)
        if status_code:
            assert response.status_code == status_code
        return response.json()

    def ping(self):
        with allure.step('Ping api client'):
            url = f"{self.base_url}{Endpoints.PING_ENDPOINT.value}"
            response = self.session.get(url)
            response.raise_for_status()

        with allure.step('Assert status code'):
            assert response.status_code == 201, f"Expected status 201 but got {response.status_code}"
        return response.status_code

    def auth(self):
        with allure.step('Getting auth token'):
            url = f"{self.base_url}{Endpoints.AUTH_ENDPOINT.value}"
            payload = {"username": AdminCredentials.USERNAME.value, "password": AdminCredentials.PASSWORD.value}
            response = self.session.post(url, json=payload, timeout=Timeouts.TIMEOUT.value)
            response.raise_for_status()
        with allure.step('Checking status code'):
            assert response.status_code == 200, f"Expected status 200 but got {response.status_code}"
        token = response.json()['token']
        with allure.step('Updating header with authorization token'):
            self.session.headers.update({'Authorization': f'Bearer {token}'})

    def get_booking_by_id(self, booking_id):
        with allure.step('Returns a specific booking based upon the booking id provided'):
            url = f"{self.base_url}{Endpoints.BOOKING_ENDPOINT.value}/{booking_id}"
            response = self.session.get(url)
            response.raise_for_status()
        with allure.step('Assert status code'):
            assert response.status_code == 200, f"Expected status 200 but got {response.status_code}"
        return response.status_code, response.json()

    def delete_booking(self, booking_id):
        with allure.step('Deleting booking'):
            url = f"{self.base_url}{Endpoints.BOOKING_ENDPOINT.value}/{booking_id}"
            response = self.session.delete(url, auth=HTTPBasicAuth(AdminCredentials.USERNAME.value, AdminCredentials.PASSWORD.value))
            response.raise_for_status()
        with allure.step('Assert status code'):
            assert response.status_code == 201, f"Expected status 201 but got {response.status_code}"
            return response.status_code

    def create_booking(self, json_data):
        with allure.step('Creates a new booking'):
            url = f"{self.base_url}{Endpoints.BOOKING_ENDPOINT.value}"
            response = self.session.post(url, json=json_data)
            response.raise_for_status()

        with allure.step('Assert status code'):
            assert response.status_code in (200, 201), f"Expected status 200 or 201 but got {response.status_code}"
        return response.json()

    def get_booking_ids(self, params=None):
        with allure.step('Getting object with bookings'):
            url = f"{self.base_url}{Endpoints.BOOKING_ENDPOINT.value}"
            response = self.session.get(url, params=params)
            response.raise_for_status()
        with allure.step('Assert status code'):
            assert response.status_code == 200, f"Expected status 200 but got {response.status_code}"
            return response.json()

    def put_booking(self, booking_id, json_data):
        with allure.step('Updating booking'):
            url = f"{self.base_url}{Endpoints.BOOKING_ENDPOINT.value}/{booking_id}"
            response = self.session.put(url, auth=HTTPBasicAuth(AdminCredentials.USERNAME.value, AdminCredentials.PASSWORD.value), json=json_data)
            response.raise_for_status()
        with allure.step('Assert status code'):
            assert response.status_code == 200, f"Expected status 200 but got {response.status_code}"
            return response.json()

    def patch_booking(self, booking_id, json_data):
        with allure.step('Updating booking'):
            url = f"{self.base_url}{Endpoints.BOOKING_ENDPOINT.value}/{booking_id}"
            response = self.session.patch(url, auth=HTTPBasicAuth(AdminCredentials.USERNAME.value, AdminCredentials.PASSWORD.value), json=json_data)
            response.raise_for_status()
        with allure.step('Assert status code'):
            assert response.status_code == 200, f"Expected status 200 but got {response.status_code}"
            return response.json()