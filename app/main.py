from fastapi import FastAPI
from app.models.transaction import TransactionRequest, RiskResponse
from app.services.risk_engine import FraudRiskEngine
from app.db.repository import get_repository
from app.config import settings

app = FastAPI(title=settings.app_name, version="1.0.0")
risk_engine = FraudRiskEngine()
repository = get_repository()


@app.get("/health")
def health():
    return {"status": "UP", "service": settings.app_name}


@app.post("/api/v1/transactions/score", response_model=RiskResponse)
def score_transaction(transaction: TransactionRequest):
    recent_transactions = repository.find_by_customer(transaction.customer_id)
    response = risk_engine.score(transaction, recent_transactions)

    record = transaction.model_dump()
    record.update(response.model_dump())
    repository.save(record)
    return response


@app.get("/api/v1/transactions")
def get_transactions():
    return repository.find_all()
