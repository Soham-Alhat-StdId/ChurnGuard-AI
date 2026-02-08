from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, JSON, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class Customer(Base):
    """Customer model"""
    __tablename__ = "customers"
    
    id = Column(Integer, primary_key=True, index=True)
    external_id = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    name = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Customer metrics
    total_orders = Column(Integer, default=0)
    total_spent = Column(Float, default=0.0)
    avg_order_value = Column(Float, default=0.0)
    days_since_last_order = Column(Integer, default=0)
    order_frequency = Column(Float, default=0.0)
    
    # Engagement metrics
    email_open_rate = Column(Float, default=0.0)
    email_click_rate = Column(Float, default=0.0)
    sms_engagement_rate = Column(Float, default=0.0)
    app_sessions = Column(Integer, default=0)
    
    # Churn prediction
    churn_probability = Column(Float, nullable=True)
    churn_risk_level = Column(String, nullable=True)  # low, medium, high
    last_prediction_date = Column(DateTime, nullable=True)
    
    # CLV
    predicted_clv = Column(Float, nullable=True)
    clv_segment = Column(String, nullable=True)
    
    # Relationships
    transactions = relationship("Transaction", back_populates="customer")
    predictions = relationship("ChurnPrediction", back_populates="customer")
    campaigns = relationship("Campaign", back_populates="customer")


class Transaction(Base):
    """Transaction model"""
    __tablename__ = "transactions"
    
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"))
    external_id = Column(String, unique=True, index=True)
    
    amount = Column(Float)
    items_count = Column(Integer)
    discount_amount = Column(Float, default=0.0)
    transaction_date = Column(DateTime)
    status = Column(String)  # completed, pending, cancelled
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    customer = relationship("Customer", back_populates="transactions")


class ChurnPrediction(Base):
    """Churn prediction history"""
    __tablename__ = "churn_predictions"
    
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"))
    
    # Predictions
    xgboost_score = Column(Float)
    nn_score = Column(Float)
    ensemble_score = Column(Float)
    risk_level = Column(String)
    
    # Explainability
    shap_values = Column(JSON)
    top_features = Column(JSON)
    
    # Metadata
    model_version = Column(String)
    prediction_date = Column(DateTime, default=datetime.utcnow)
    
    customer = relationship("Customer", back_populates="predictions")


class Campaign(Base):
    """Automated campaign model"""
    __tablename__ = "campaigns"
    
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"))
    
    campaign_type = Column(String)  # email, sms, push
    campaign_name = Column(String)
    message_template = Column(String)
    
    # Status
    status = Column(String)  # pending, sent, delivered, failed
    sent_at = Column(DateTime, nullable=True)
    delivered_at = Column(DateTime, nullable=True)
    opened_at = Column(DateTime, nullable=True)
    clicked_at = Column(DateTime, nullable=True)
    
    # Trigger
    trigger_reason = Column(String)  # high_churn_risk, inactive, win_back
    trigger_score = Column(Float)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    customer = relationship("Customer", back_populates="campaigns")


class Anomaly(Base):
    """Anomaly detection results"""
    __tablename__ = "anomalies"
    
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"))
    
    anomaly_type = Column(String)  # behavior, transaction, engagement
    anomaly_score = Column(Float)
    description = Column(String)
    
    # Context
    feature_values = Column(JSON)
    expected_range = Column(JSON)
    
    detected_at = Column(DateTime, default=datetime.utcnow)
    resolved = Column(Boolean, default=False)
