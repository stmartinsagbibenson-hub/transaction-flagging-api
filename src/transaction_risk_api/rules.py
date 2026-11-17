from datetime import timedelta

from .config import get_settings


def check_unusual_hours(transaction):
    settings = get_settings()
    start = int(settings["unusual_hours_start"].split(":")[0])
    end = int(settings["unusual_hours_end"].split(":")[0])
    hour = transaction.timestamp.hour

    if start <= hour < end:
        return {
            "rule": "unusual_hours",
            "reason": f"Transaction made at {hour}:00, inside the unusual hours window.",
        }
    return None


def check_rapid_withdrawals(transaction, recent_withdrawals):
    settings = get_settings()
    limit = settings["rapid_withdrawal_limit"]
    window = timedelta(seconds=settings["rapid_withdrawal_window_seconds"])

    if transaction.transaction_type != "withdrawal":
        return None

    count = 1
    for earlier in recent_withdrawals:
        gap = transaction.timestamp - earlier.timestamp
        if timedelta(0) <= gap <= window:
            count += 1

    if count >= limit:
        return {
            "rule": "rapid_withdrawals",
            "reason": f"{count} withdrawals within {window.seconds} seconds.",
        }
    return None


def check_large_and_fast(transaction, recent_withdrawals):
    settings = get_settings()
    threshold = settings["large_amount_threshold"]
    window = timedelta(seconds=settings["very_fast_withdrawal_window_seconds"])

    if transaction.transaction_type != "withdrawal":
        return None
    if transaction.amount < threshold:
        return None

    for earlier in recent_withdrawals:
        gap = transaction.timestamp - earlier.timestamp
        if timedelta(0) <= gap <= window and earlier.amount >= threshold:
            return {
                "rule": "large_and_fast",
                "reason": f"Two large withdrawals within {window.seconds} seconds.",
            }
    return None


def check_cumulative_cap(transaction, recent_withdrawals):
    settings = get_settings()
    cap = settings["cumulative_cap_amount"]
    window = timedelta(minutes=settings["cumulative_cap_window_minutes"])

    if transaction.transaction_type != "withdrawal":
        return None

    total = transaction.amount
    for earlier in recent_withdrawals:
        gap = transaction.timestamp - earlier.timestamp
        if timedelta(0) <= gap <= window:
            total += earlier.amount

    if total >= cap:
        return {
            "rule": "cumulative_cap",
            "reason": f"{total} withdrawn within {settings['cumulative_cap_window_minutes']} minutes.",
        }
    return None


def check_very_fast(transaction, recent_withdrawals):
    settings = get_settings()
    limit = settings["very_fast_withdrawal_limit"]
    window = timedelta(seconds=settings["very_fast_withdrawal_window_seconds"])

    if transaction.transaction_type != "withdrawal":
        return None

    count = 1
    for earlier in recent_withdrawals:
        gap = transaction.timestamp - earlier.timestamp
        if timedelta(0) <= gap <= window:
            count += 1

    if count >= limit:
        return {
            "rule": "very_fast",
            "reason": f"{count} withdrawals within {window.seconds} seconds.",
        }
    return None


def check_large_amount(transaction):
    settings = get_settings()
    if transaction.transaction_type == "withdrawal" and transaction.amount >= settings["large_amount_threshold"]:
        return {
            "rule": "large_amount",
            "reason": f"Amount {transaction.amount} is at or above the large amount threshold.",
        }
    return None


def evaluate_transaction(transaction, recent_withdrawals):
    hard_flags = [
        check_very_fast(transaction, recent_withdrawals),
        check_large_and_fast(transaction, recent_withdrawals),
    ]
    hard_flags = [f for f in hard_flags if f]

    soft_flags = [
        check_large_amount(transaction),
        check_unusual_hours(transaction),
        check_rapid_withdrawals(transaction, recent_withdrawals),
        check_cumulative_cap(transaction, recent_withdrawals),
    ]
    soft_flags = [f for f in soft_flags if f]

    all_flags = hard_flags + soft_flags
    flagged = len(hard_flags) > 0 or len(soft_flags) >= 3

    if flagged:
        risk_level = "HIGH"
    elif len(soft_flags) == 2:
        risk_level = "MEDIUM"
    else:
        risk_level = "LOW"

    return flagged, risk_level, all_flags