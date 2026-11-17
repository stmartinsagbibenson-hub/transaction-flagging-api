# Transaction Risk Flagging API

## Project Overview
A Python FastAPI application that evaluates financial transactions and identifies potentially suspicious activities using predefined risk rules.

## Features
- Evaluate individual transactions.
- Evaluate batches of transactions.
- Validate transaction data.
- Convert foreign currencies to NGN.
- Detect unusually large withdrawals.
- Detect rapid and very fast withdrawals.
- Detect repeated large withdrawals.
- Monitor cumulative withdrawal amounts.
- Detect unusual transaction hours.
- Return risk levels and explanations.

## Technologies
- Python 3.14
- FastAPI
- Pydantic
- HTTPX
- Pytest
- Ruff

## Installation

Create a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -e ".[dev]"
```

## Run the Application

```bash
uvicorn src.transaction_risk_api.main:app --reload
```

API documentation:

http://127.0.0.1:8000/docs

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | /health | Health check |
| GET | /rules | View risk rules |
| POST | /transactions/evaluate | Evaluate one transaction |
| POST | /transactions/evaluate/batch | Evaluate multiple transactions |

## Run Tests

```bash
python -m pytest -v
```

Check code:

```bash
ruff check .
ruff format --check .
```

## Documentation

- `docs/atm_withdrawal_flowchart.md`
- `docs/atm_withdrawal_pseudocode.md`

## Limitations

This is an educational fraud-detection simulation. It is not a production banking system. Transaction history is held in application memory and is not persistent.

