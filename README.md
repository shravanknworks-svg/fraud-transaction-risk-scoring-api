# Fraud Transaction Risk Scoring API

A FinTech-focused Fraud Transaction Risk Scoring API built with Python and FastAPI. This project evaluates financial transactions using rule-based risk scoring and returns fraud decisions such as APPROVE, REVIEW, or DECLINE.

## Features

- REST API for transaction risk scoring
- Rule-based fraud scoring engine
- Risk decisions: APPROVE, REVIEW, DECLINE
- MongoDB repository support
- In-memory mode for easy local testing
- MongoDB indexes for customer, transaction, and risk queries
- Unit tests with Pytest
- Swagger UI documentation

## Tech Stack

- Python
- FastAPI
- MongoDB / PyMongo
- Pydantic
- Pytest
- Uvicorn

## Project Structure

```text
app/
  main.py
  config.py
  models/
  services/
  db/
tests/
requirements.txt
README.md
```

## Run Locally

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open Swagger UI:

```text
http://localhost:8000/docs
```

## Run Tests

```bash
PYTHONPATH=. bittest
```
## Sample Use Case

This project simulates how financial institutions score transactions based on fraud indicators such as transaction amount, location, merchant category, frequency, and customer behavior.

## Sample Request

```json
{
  "transaction_id": "TXN-1001",
  "customer_id": "CUST-501",
  "account_id": "ACC-9001",
  "amount": 12500,
  "currency": "USD",
  "merchant_category": "CRYPTO",
  "country": "NG",
  "channel": "WEB",
  "device_id": null,
  "ip_address": "192.168.1.1"
}
```

## Sample Response

```json
{
  "transaction_id": "TXN-1001",
  "customer_id": "CUST-501",
  "risk_score": 100,
  "decision": "DECLINE",
  "reasons": [
    "High transaction amount >= 10000",
    "High-risk country: NG",
    "High-risk merchant category: CRYPTO",
    "Missing device identifier"
  ]
}
```
## Author
Shravan K Nellutla
