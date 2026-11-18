import pytest
from fastapi.testclient import TestClient

from src.transaction_risk_api import api
from src.transaction_risk_api.main import app
from src.transaction_risk_api.state import clear_history


@pytest.fixture
def client(monkeypatch):
    clear_history()

    monkeypatch.setattr(
        api,
        "convert_to_base",
        lambda amount, currency: amount,
    )

    with TestClient(app) as test_client:
        yield test_client

    clear_history()


def test_health_endpoint(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_rules_endpoint(client):
    response = client.get("/rules")

    assert response.status_code == 200

    data = response.json()

    assert data["base_currency"] == "NGN"
    assert data["timezone"] == "Africa/Lagos"
    assert "large_amount_threshold" in data["rules"]


def test_evaluate_transaction_endpoint(client):
    transaction = {
        "transaction_id": "TX001",
        "account_id": "ACC001",
        "amount": "5000",
        "currency": "NGN",
        "transaction_type": "deposit",
        "timestamp": "2026-11-17T10:00:00+00:00",
    }

    response = client.post(
        "/transactions/evaluate",
        json=transaction,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["transaction_id"] == "TX001"
    assert data["account_id"] == "ACC001"
    assert data["risk_level"] == "LOW"
    assert data["flagged"] is False


def test_invalid_transaction_is_rejected(client):
    transaction = {
        "transaction_id": "TX002",
        "account_id": "ACC001",
        "amount": "-500",
        "currency": "NGN",
        "transaction_type": "withdrawal",
        "timestamp": "2026-11-17T10:00:00+00:00",
    }

    response = client.post(
        "/transactions/evaluate",
        json=transaction,
    )

    assert response.status_code == 422


def test_batch_evaluation_endpoint(client):
    batch = {
        "transactions": [
            {
                "transaction_id": "TX003",
                "account_id": "ACC001",
                "amount": "5000",
                "currency": "NGN",
                "transaction_type": "deposit",
                "timestamp": "2026-11-17T10:00:00+00:00",
            },
            {
                "transaction_id": "TX004",
                "account_id": "ACC002",
                "amount": "7000",
                "currency": "NGN",
                "transaction_type": "deposit",
                "timestamp": "2026-11-17T10:05:00+00:00",
            },
        ]
    }

    response = client.post(
        "/transactions/evaluate/batch",
        json=batch,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["total"] == 2
    assert data["successful"] == 2
    assert data["failed"] == 0
