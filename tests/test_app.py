import pytest
from unittest.mock import patch
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    return app.test_client()


def test_create_loan_application_bad_request_email(client):
    payload = {
        "full_name": "Test User",
        "email": "testexample.com",  # not email
        "phone": "1234567890",
        "ssn": "123456789",
        "address_line_1": "123 Main St",
        "address_line_2": None,
        "city": "NYC",
        "state": "NY",
        "zip_code": "10001",
        "requested_amount_cents": 40000000,
    }

    with patch("app.db.session.add"), patch("app.db.session.commit"):

        response = client.post("/v1/loan_applications", json=payload)

    assert response.status_code == 400
    json_response = response.get_json()

    assert json_response["error"] == "Validation failed"
    assert "Not a valid email address." in str(json_response["message"])


@pytest.mark.parametrize(
    "scenario, requested_amount_cents",
    [
        ("less than $10,000", 500_000),
        ("greater than $50,000", 10_000_000_000_000),
    ],
)
def test_create_loan_application_scenario_1(client, scenario, requested_amount_cents):
    """
    If the loan amount requested is less than $10,000 or greater than $50,000, deny the application
    """
    payload = {
        "full_name": "Test User",
        "email": "test@example.com",
        "phone": "1234567890",
        "ssn": "123456789",
        "address_line_1": "123 Main St",
        "address_line_2": None,
        "city": "NYC",
        "state": "NY",
        "zip_code": "10001",
        "requested_amount_cents": requested_amount_cents,
    }

    with patch("app.random.randint", return_value=5), patch(
        "app.db.session.add"
    ), patch("app.db.session.commit"):

        response = client.post("/v1/loan_applications", json=payload)

    assert response.status_code == 201
    data = response.get_json()["data"]

    assert data["open_credit_lines"] == 5
    assert data["status"] == "rejected"
    assert data["term_months"] is None
    assert data["interest_rate_bps"] is None


def test_create_loan_application_scenario_2(client):
    """
    If the number of credit lines open is <10, a 36-month term and 10% interest applies
    """
    payload = {
        "full_name": "Test User",
        "email": "test@example.com",
        "phone": "1234567890",
        "ssn": "123456789",
        "address_line_1": "123 Main St",
        "address_line_2": None,
        "city": "NYC",
        "state": "NY",
        "zip_code": "10001",
        "requested_amount_cents": 2_000_000,
    }

    with patch("app.random.randint", return_value=5), patch(
        "app.db.session.add"
    ), patch("app.db.session.commit"):

        response = client.post("/v1/loan_applications", json=payload)

    assert response.status_code == 201
    data = response.get_json()["data"]

    assert data["open_credit_lines"] == 5
    assert data["status"] == "approved"
    assert data["term_months"] == 36
    assert data["interest_rate_bps"] == 1000


def test_create_loan_application_scenario_3(client):
    """
    If the number of credit lines open is <=50 and >=10, a 24-month term and 20% interest applies
    """
    payload = {
        "full_name": "Test User",
        "email": "test@example.com",
        "phone": "1234567890",
        "ssn": "123456789",
        "address_line_1": "123 Main St",
        "address_line_2": None,
        "city": "NYC",
        "state": "NY",
        "zip_code": "10001",
        "requested_amount_cents": 2_000_000,
    }

    with patch("app.random.randint", return_value=15), patch(
        "app.db.session.add"
    ), patch("app.db.session.commit"):

        response = client.post("/v1/loan_applications", json=payload)

    assert response.status_code == 201
    data = response.get_json()["data"]

    assert data["open_credit_lines"] == 15
    assert data["status"] == "approved"
    assert data["term_months"] == 24
    assert data["interest_rate_bps"] == 2000


def test_create_loan_application_scenario_4(client):
    """
    If the number of credit lines is >50, deny the application
    """
    payload = {
        "full_name": "Test User",
        "email": "test@example.com",
        "phone": "1234567890",
        "ssn": "123456789",
        "address_line_1": "123 Main St",
        "address_line_2": None,
        "city": "NYC",
        "state": "NY",
        "zip_code": "10001",
        "requested_amount_cents": 2_000_000,
    }

    with patch("app.random.randint", return_value=51), patch(
        "app.db.session.add"
    ), patch("app.db.session.commit"):

        response = client.post("/v1/loan_applications", json=payload)

    assert response.status_code == 201
    data = response.get_json()["data"]

    assert data["open_credit_lines"] == 51
    assert data["status"] == "rejected"
    assert data["term_months"] is None
    assert data["interest_rate_bps"] is None
