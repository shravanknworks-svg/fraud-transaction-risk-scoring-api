from app.models.transaction import TransactionRequest
from app.services.risk_engine import FraudRiskEngine


def test_low_risk_transaction_is_approved():
    engine = FraudRiskEngine()
    txn = TransactionRequest(
        transaction_id="T1",
        customer_id="C1",
        account_id="A1",
        amount=100,
        country="US",
        merchant_category="GROCERY",
        device_id="D1",
    )
    result = engine.score(txn)
    assert result.decision == "APPROVE"
    assert result.risk_score < 40


def test_high_risk_transaction_is_declined():
    engine = FraudRiskEngine()
    txn = TransactionRequest(
        transaction_id="T2",
        customer_id="C1",
        account_id="A1",
        amount=15000,
        country="NG",
        merchant_category="CRYPTO",
    )
    result = engine.score(txn)
    assert result.decision == "DECLINE"
    assert result.risk_score >= 70
