from datetime import datetime, timedelta, timezone
from decimal import Decimal
from types import SimpleNamespace

from src.transaction_risk_api.rules import (
    check_cumulative_cap,
    check_large_amount,
    check_large_and_fast,
    check_rapid_withdrawals,
    check_unusual_hours,
    check_very_fast,
    evaluate_transaction,
)


def make_transaction(
    amount=Decimal("5000"),
    transaction_type="withdrawal",
    timestamp=None,
):
    if timestamp is None:
        timestamp = datetime(2026, 11, 17, 12, 0, tzinfo=timezone.utc)

    return SimpleNamespace(
        amount=amount,
        transaction_type=transaction_type,
        timestamp=timestamp,
    )


def test_large_amount_rule():
    transaction = make_transaction(amount=Decimal("150000"))

    result = check_large_amount(transaction)

    assert result is not None
    assert result["rule"] == "large_amount"


def test_rapid_withdrawals_rule():
    now = datetime(2026, 11, 17, 12, 0, 10, tzinfo=timezone.utc)

    transaction = make_transaction(timestamp=now)

    earlier = make_transaction(
        timestamp=now - timedelta(seconds=5)
    )

    result = check_rapid_withdrawals(transaction, [earlier])

    assert result is not None
    assert result["rule"] == "rapid_withdrawals"


def test_very_fast_withdrawals_rule():
    now = datetime(2026, 11, 17, 12, 0, 10, tzinfo=timezone.utc)

    transaction = make_transaction(timestamp=now)

    earlier = [
        make_transaction(timestamp=now - timedelta(seconds=seconds))
        for seconds in [1, 2, 3, 4]
    ]

    result = check_very_fast(transaction, earlier)

    assert result is not None
    assert result["rule"] == "very_fast"


def test_large_and_fast_rule():
    now = datetime(2026, 11, 17, 12, 0, 10, tzinfo=timezone.utc)

    transaction = make_transaction(
        amount=Decimal("150000"),
        timestamp=now,
    )

    earlier = make_transaction(
        amount=Decimal("120000"),
        timestamp=now - timedelta(seconds=5),
    )

    result = check_large_and_fast(transaction, [earlier])

    assert result is not None
    assert result["rule"] == "large_and_fast"


def test_cumulative_cap_rule():
    now = datetime(2026, 11, 17, 12, 0, tzinfo=timezone.utc)

    transaction = make_transaction(
        amount=Decimal("100000"),
        timestamp=now,
    )

    earlier = make_transaction(
        amount=Decimal("100000"),
        timestamp=now - timedelta(minutes=10),
    )

    result = check_cumulative_cap(transaction, [earlier])

    assert result is not None
    assert result["rule"] == "cumulative_cap"


def test_unusual_hours_rule():
    transaction = make_transaction(
        timestamp=datetime(
            2026, 11, 17, 2, 0, tzinfo=timezone.utc
        )
    )

    result = check_unusual_hours(transaction)

    assert result is not None
    assert result["rule"] == "unusual_hours"


def test_deposit_does_not_trigger_withdrawal_rules():
    transaction = make_transaction(
        amount=Decimal("150000"),
        transaction_type="deposit",
    )

    assert check_large_amount(transaction) is None
    assert check_rapid_withdrawals(transaction, []) is None
    assert check_very_fast(transaction, []) is None
    assert check_large_and_fast(transaction, []) is None
    assert check_cumulative_cap(transaction, []) is None


def test_very_fast_withdrawals_produce_high_risk():
    now = datetime(2026, 11, 17, 12, 0, 10, tzinfo=timezone.utc)

    transaction = make_transaction(timestamp=now)

    earlier = [
        make_transaction(timestamp=now - timedelta(seconds=seconds))
        for seconds in [1, 2, 3, 4]
    ]

    flagged, risk_level, flags = evaluate_transaction(
        transaction, earlier
    )

    assert flagged is True
    assert risk_level == "HIGH"
    assert any(flag["rule"] == "very_fast" for flag in flags)
