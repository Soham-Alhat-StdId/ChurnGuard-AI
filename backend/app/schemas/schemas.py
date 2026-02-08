from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List, Dict
from datetime import datetime


class CustomerBase(BaseModel):
    """Base customer schema"""
    email: EmailStr
    name: str
    external_id: Optional[str] = None


class CustomerCreate(CustomerBase):
    """Schema for creating customer"""
    pass


class CustomerUpdate(BaseModel):
    """Schema for updating customer"""
    name: Optional[str] = None
    email: Optional[EmailStr] = None


class CustomerMetrics(BaseModel):
    """Customer metrics schema"""
    total_orders: int
    total_spent: float
    avg_order_value: float
    days_since_last_order: int
    order_frequency: float
    email_open_rate: float
    email_click_rate: float
    sms_engagement_rate: float
    app_sessions: int


class Customer(CustomerBase):
    """Full customer schema"""
    id: int
    created_at: datetime
    updated_at: datetime
    
    # Metrics
    total_orders: int
    total_spent: float
    avg_order_value: float
    days_since_last_order: int
    order_frequency: float
    email_open_rate: float
    email_click_rate: float
    sms_engagement_rate: float
    app_sessions: int
    
    # Predictions
    churn_probability: Optional[float] = None
    churn_risk_level: Optional[str] = None
    last_prediction_date: Optional[datetime] = None
    predicted_clv: Optional[float] = None
    clv_segment: Optional[str] = None
    
    class Config:
        from_attributes = True


class ChurnPredictionRequest(BaseModel):
    """Request for churn prediction"""
    customer_id: int
    features: Optional[Dict] = None


class ChurnPredictionResponse(BaseModel):
    """Response for churn prediction"""
    customer_id: int
    xgboost_score: float
    nn_score: float
    ensemble_score: float
    risk_level: str
    shap_values: Dict
    top_features: List[Dict]
    prediction_date: datetime
    
    class Config:
        from_attributes = True


class CLVPredictionRequest(BaseModel):
    """Request for CLV prediction"""
    customer_id: int


class CLVPredictionResponse(BaseModel):
    """Response for CLV prediction"""
    customer_id: int
    predicted_clv: float
    clv_segment: str
    confidence_interval: Dict[str, float]


class CampaignCreate(BaseModel):
    """Schema for creating campaign"""
    customer_id: int
    campaign_type: str  # email, sms, push
    campaign_name: str
    message_template: str
    trigger_reason: str
    trigger_score: Optional[float] = None


class Campaign(BaseModel):
    """Full campaign schema"""
    id: int
    customer_id: int
    campaign_type: str
    campaign_name: str
    message_template: str
    status: str
    sent_at: Optional[datetime] = None
    delivered_at: Optional[datetime] = None
    opened_at: Optional[datetime] = None
    clicked_at: Optional[datetime] = None
    trigger_reason: str
    trigger_score: Optional[float] = None
    created_at: datetime
    
    class Config:
        from_attributes = True


class TransactionCreate(BaseModel):
    """Schema for creating transaction"""
    customer_id: int
    external_id: str
    amount: float
    items_count: int
    discount_amount: float = 0.0
    transaction_date: datetime
    status: str = "completed"


class Transaction(TransactionCreate):
    """Full transaction schema"""
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class AnomalyDetectionResponse(BaseModel):
    """Response for anomaly detection"""
    customer_id: int
    anomalies: List[Dict]
    overall_score: float
    is_anomalous: bool


class DashboardMetrics(BaseModel):
    """Dashboard metrics response"""
    total_customers: int
    high_risk_customers: int
    medium_risk_customers: int
    low_risk_customers: int
    avg_churn_probability: float
    avg_clv: float
    total_campaigns_sent: int
    campaign_success_rate: float
    retention_lift: float
    roi: float
