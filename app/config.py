from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Fraud Transaction Risk Scoring API"
    mongodb_uri: str = "mongodb://localhost:27017"
    mongodb_db: str = "fraud_risk_db"
    use_in_memory_db: bool = True

    class Config:
        env_file = ".env"


settings = Settings()
