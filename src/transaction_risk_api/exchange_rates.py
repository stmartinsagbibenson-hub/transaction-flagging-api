from decimal import Decimal
import httpx
from .config import get_settings

class ExchangeRateError(Exception):
    pass

def convert_to_base(amount, currency):
    settings = get_settings()
    base = settings["base_currency"]

    if currency == base:
        return amount

    url = f"{settings['exchange_rate_base_url']}/v2/rate/{currency}/{base}"
    try:
        response = httpx.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
    except (httpx.HTTPError, ValueError):
        raise ExchangeRateError("Exchange rate service is unavailable.")

    rate = find_rate(data, base)
    if rate is None:
        raise ExchangeRateError(f"No exchange rate found for {currency} to {base}.")

    return amount * Decimal(str(rate))


def find_rate(data, base):
    if isinstance(data, list):
        for item in data:
            if item.get("quote") == base:
                return item.get("rate")

    elif isinstance(data, dict):
        if data.get("quote") == base:
            return data.get("rate")

        return data.get("rates", {}).get(base)

    return None