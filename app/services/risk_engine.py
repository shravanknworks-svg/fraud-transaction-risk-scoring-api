from datetime import datetime, timedelta
from app.models.transaction import TransactionRequest, RiskDecision, RiskResponse


class FraudRiskEngine:
    """Simple rules-based fraud risk engine for demo/interview portfolio use."""

    HIGH_RISK_COUNTRIES = {"NG", "RU", "KP", "IR"}
    HIGH_RISK_MERCHANTS = {"CRYPTO", "GAMBLING", "WIRE_TRANSFER"}

    def score(self, transaction: TransactionRequest, recent_customer_transactions: list[dict] | None = None) -> RiskResponse:
        score = 0
        reasons: list[str] = []
        recent_customer_transactions = recent_customer_transactions or []

        if transaction.amount >= 10000:
            score += 40
            reasons.append("High transaction amount >= 10000")
        elif transaction.amount >= 5000:
            score += 25
            reasons.append("Elevated transaction amount >= 5000")

        if transaction.country.upper() in self.HIGH_RISK_COUNTRIES:
            score += 30
            reasons.append(f"High-risk country: {transaction.country}")

        if transaction.merchant_category.upper() in self.HIGH_RISK_MERCHANTS:
            score += 25
            reasons.append(f"High-risk merchant category: {transaction.merchant_category}")

        one_hour_ago = datetime.utcnow() - timedelta(hours=1)
        recent_count = sum(
            1 for t in recent_customer_transactions
            if t.get("transaction_time") and t["transaction_time"] >= one_hour_ago
        )
        if recent_count >= 5:
            score += 20
            reasons.append("High transaction velocity: 5+ transactions in the last hour")

        if not transaction.device_id:
            score += 10
            reasons.append("Missing device identifier")

        score = min(score, 100)
        if score >= 70:
            decision = RiskDecision.DECLINE
        elif score >= 40:
            decision = RiskDecision.REVIEW
        else:
            decision = RiskDecision.APPROVE
            if not reasons:
                reasons.append("No major fraud indicators detected")

        return RiskResponse(
            transaction_id=transaction.transaction_id,
            customer_id=transaction.customer_id,
            risk_score=score,
            decision=decision,
            reasons=reasons,
            evaluated_at=datetime.utcnow(),
        )
