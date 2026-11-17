from collections import defaultdict
from datetime import timedelta

withdrawal_history = defaultdict(list)


def get_recent_withdrawals(account_id, now, minutes=60):
    cutoff = now - timedelta(minutes=minutes)
    return [w for w in withdrawal_history[account_id] if w.timestamp >= cutoff]


def record_withdrawal(account_id, transaction):
    withdrawal_history[account_id].append(transaction)


def clear_history():
    withdrawal_history.clear()