def get_settings():
    return {
        "app_name": "Transaction Risk Flagging API",
        "timezone": "Africa/Lagos",
        "base_currency": "NGN",
        "large_amount_threshold": 100000,
        "rapid_withdrawal_limit": 2,
        "rapid_withdrawal_window_seconds": 20,
        "very_fast_withdrawal_limit": 5,
        "very_fast_withdrawal_window_seconds": 10,
        "unusual_hours_start": "00:00",
        "unusual_hours_end": "05:00",
        "cumulative_cap_amount": 200000,
        "cumulative_cap_window_minutes": 60,
        "exchange_rate_base_url": "https://api.frankfurter.dev",
    } 