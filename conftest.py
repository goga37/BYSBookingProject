from datetime import datetime, timedelta

import pytest
from faker import Faker

from core.clients.api_client import APIClient


@pytest.fixture(scope='session')
def api_client():
    client = APIClient()
    client.auth()
    return client


@pytest.fixture(scope='session')
def booking_dates():
    today = datetime.date.today()
    checkin_date = today + timedelta(days=10)
    checkout_date = today + timedelta(days=5)

    return {
        "checkin": checkin_date.strftime("%Y-%m-%d"),
        "checkout": checkout_date.strftime("%Y-%m-%d"),
    }


@pytest.fixture(scope='session')
def generate_random_booking_data(booking_dates):
    faker = Faker()
    first_name = faker.first_name()
    last_name = faker.last_name()
    total_price = faker.random_number(digits=3)
    deposit_paid = faker.boolean()
    additional_needs = faker.sentence()

    data = {
        "firstname": first_name,
        "lastname": last_name,
        "totalprice": total_price,
        "depositpaid": deposit_paid,
        "additionalneeds": additional_needs
    }

    return data
