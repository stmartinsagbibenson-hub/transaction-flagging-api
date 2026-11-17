from decimal import Decimal
from unittest.mock import Mock

import httpx
import pytest

from src.transaction_risk_api import exchange_rates


def test_same_currency_does_not_call_api(monkeypatch):
    mock_get = Mock()

    monkeypatch.setattr(exchange_rates.httpx, "get", mock_get)

    result = exchange_rates.convert_to_base(
        Decimal("5000"), "NGN"
    )

    assert result == Decimal("5000")
    mock_get.assert_not_called()


def test_foreign_currency_conversion(monkeypatch):
    mock_response = Mock()
    mock_response.raise_for_status.return_value = None

    mock_response.json.return_value = {
        "date": "2026-11-17",
        "base": "USD",
        "quote": "NGN",
        "rate": 1500,
    }

    mock_get = Mock(return_value=mock_response)

    monkeypatch.setattr(exchange_rates.httpx, "get", mock_get)

    result = exchange_rates.convert_to_base(
        Decimal("10"), "USD"
    )

    assert result == Decimal("15000")


def test_exchange_rate_service_error(monkeypatch):
    mock_get = Mock(
        side_effect=httpx.TimeoutException("Request timed out")
    )

    monkeypatch.setattr(exchange_rates.httpx, "get", mock_get)

    with pytest.raises(exchange_rates.ExchangeRateError):
        exchange_rates.convert_to_base(
            Decimal("10"), "USD"
        )


def test_missing_exchange_rate(monkeypatch):
    mock_response = Mock()
    mock_response.raise_for_status.return_value = None
    mock_response.json.return_value = {
        "date": "2026-11-17",
        "base": "USD",
        "quote": "EUR",
        "rate": 0.92,
    }

    monkeypatch.setattr(
        exchange_rates.httpx,
        "get",
        Mock(return_value=mock_response),
    )

    with pytest.raises(exchange_rates.ExchangeRateError):
        exchange_rates.convert_to_base(
            Decimal("10"), "USD"
        )
