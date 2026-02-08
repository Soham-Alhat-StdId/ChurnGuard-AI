from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings"""
    
    # API Settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "ChurnGuard AI"
    VERSION: str = "1.0.0"
    
    # Database
    DATABASE_URL: str = "postgresql://churnguard:churnguard@localhost:5432/churnguard_db"
    
    # Redis
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    
    # Kafka
    KAFKA_BOOTSTRAP_SERVERS: str = "localhost:9092"
    KAFKA_TOPIC_PREDICTIONS: str = "churn_predictions"
    KAFKA_TOPIC_CAMPAIGNS: str = "automated_campaigns"
    
    # ML Models
    MODEL_PATH: str = "./models"
    XGBOOST_MODEL_PATH: str = "./models/xgboost_churn_model.pkl"
    NN_MODEL_PATH: str = "./models/nn_churn_model.h5"
    CLV_MODEL_PATH: str = "./models/clv_model.pkl"
    ANOMALY_MODEL_PATH: str = "./models/anomaly_model.pkl"
    
    # Model Thresholds
    CHURN_THRESHOLD: float = 0.5
    HIGH_RISK_THRESHOLD: float = 0.75
    
    # Integrations
    SHOPIFY_API_KEY: Optional[str] = None
    SHOPIFY_API_SECRET: Optional[str] = None
    WOOCOMMERCE_API_KEY: Optional[str] = None
    WOOCOMMERCE_API_SECRET: Optional[str] = None
    
    # Notifications
    SENDGRID_API_KEY: Optional[str] = None
    TWILIO_ACCOUNT_SID: Optional[str] = None
    TWILIO_AUTH_TOKEN: Optional[str] = None
    TWILIO_PHONE_NUMBER: Optional[str] = None
    
    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
