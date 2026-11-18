from datetime import datetime, timezone
from fastapi import APIRouter, HTTPException
from pydantic import ValidationError
from .config import get_settings
from .exchange_rates import ExchangeRateError, convert_to_base
from .rules import evaluate_transaction
from .schemas import (
    BatchItemResult,
    BatchRequest,
    BatchResponse,
    Flag,
    TransactionEvaluation,
    TransactionRequest,
)
from .state import get_recent_withdrawals, record_withdrawal

router = APIRouter()


@router.get("/health")
def health():
    settings = get_settings()
    return {"status": "ok", "app": settings["app_name"], "version": "1.0.0"}


@router.get("/rules")
def rules():
    settings = get_settings()
    return {
        "base_currency": settings["base_currency"],
        "timezone": settings["timezone"],
        "rules": {k: v for k, v in settings.items() if k not in ("app_name", "exchange_rate_base_url")},
    }


def run_evaluation(transaction):
    converted = convert_to_base(transaction.amount, transaction.currency)
    naira_transaction = transaction.model_copy(update={"amount": converted})
    recent = get_recent_withdrawals(transaction.account_id, transaction.timestamp)

    flagged, risk_level, flags = evaluate_transaction(naira_transaction, recent)

    if transaction.transaction_type == "withdrawal":
        record_withdrawal(transaction.account_id, naira_transaction)

    return TransactionEvaluation(
        transaction_id=transaction.transaction_id,
        account_id=transaction.account_id,
        amount=transaction.amount,
        currency=transaction.currency,
        risk_level=risk_level,
        flagged=flagged,
        flags=[Flag(**f) for f in flags],
        evaluated_at=datetime.now(timezone.utc),
    )


@router.post("/transactions/evaluate", response_model=TransactionEvaluation)
def evaluate(transaction: TransactionRequest):
    try:
        return run_evaluation(transaction)
    except ExchangeRateError as error:
        raise HTTPException(status_code=503, detail=str(error))


@router.post("/transactions/evaluate/batch", response_model=BatchResponse)
def evaluate_batch(batch: BatchRequest):
    parsed = []
    results = []

    for index, item in enumerate(batch.transactions):
        try:
            parsed.append((index, TransactionRequest(**item)))
        except (ValidationError, TypeError) as error:
            results.append(BatchItemResult(index=index, success=False, error=str(error)))

    parsed.sort(key=lambda pair: pair[1].timestamp)

    for index, transaction in parsed:
        try:
            results.append(BatchItemResult(index=index, success=True, result=run_evaluation(transaction)))
        except ExchangeRateError as error:
            results.append(BatchItemResult(index=index, success=False, error=str(error)))

    results.sort(key=lambda r: r.index)
    successful = sum(1 for r in results if r.success)
    return BatchResponse(total=len(results), successful=successful, failed=len(results) - successful, results=results)