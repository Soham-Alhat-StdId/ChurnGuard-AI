from typing import Dict
from sqlalchemy.orm import Session
from app.models.database_models import Customer
from app.ml.clv_model import CLVModel
from app.core.config import settings


class CLVService:
    """Service for Customer Lifetime Value prediction"""
    
    def __init__(self):
        self.model = CLVModel(model_path=settings.MODEL_PATH)
    
    def predict_clv(self, db: Session, customer_id: int) -> Dict:
        """
        Predict CLV for a customer
        """
        # Get customer data
        customer = db.query(Customer).filter(Customer.id == customer_id).first()
        if not customer:
            raise ValueError(f"Customer {customer_id} not found")
        
        # Prepare customer features
        customer_data = {
            'total_orders': customer.total_orders,
            'total_spent': customer.total_spent,
            'avg_order_value': customer.avg_order_value,
            'order_frequency': customer.order_frequency,
            'days_since_last_order': customer.days_since_last_order,
            'email_open_rate': customer.email_open_rate,
            'app_sessions': customer.app_sessions
        }
        
        # Get prediction
        predicted_clv, segment, confidence_interval = self.model.predict(customer_data)
        
        # Update customer record
        customer.predicted_clv = predicted_clv
        customer.clv_segment = segment
        
        db.commit()
        db.refresh(customer)
        
        return {
            'customer_id': customer_id,
            'predicted_clv': predicted_clv,
            'clv_segment': segment,
            'confidence_interval': confidence_interval
        }
