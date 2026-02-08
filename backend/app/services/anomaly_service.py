from typing import Dict, List
from sqlalchemy.orm import Session
from app.models.database_models import Customer, Anomaly
from app.ml.anomaly_detector import AnomalyDetector
from app.core.config import settings
from datetime import datetime


class AnomalyDetectionService:
    """Service for anomaly detection"""
    
    def __init__(self):
        self.detector = AnomalyDetector(model_path=settings.MODEL_PATH)
    
    def detect_anomalies(self, db: Session, customer_id: int) -> Dict:
        """
        Detect anomalies for a customer
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
            'days_since_last_order': customer.days_since_last_order,
            'order_frequency': customer.order_frequency,
            'email_open_rate': customer.email_open_rate,
            'email_click_rate': customer.email_click_rate,
            'sms_engagement_rate': customer.sms_engagement_rate,
            'app_sessions': customer.app_sessions
        }
        
        # Detect anomalies
        result = self.detector.detect(customer_data)
        
        # Save anomalies to database
        if result['is_anomalous'] and result['anomalies']:
            for anomaly in result['anomalies']:
                anomaly_record = Anomaly(
                    customer_id=customer_id,
                    anomaly_type=anomaly['type'],
                    anomaly_score=result['anomaly_score'],
                    description=anomaly['description'],
                    feature_values={
                        'feature': anomaly['feature'],
                        'value': anomaly['value'],
                        'severity': anomaly['severity']
                    },
                    expected_range={},
                    detected_at=datetime.utcnow(),
                    resolved=False
                )
                db.add(anomaly_record)
        
        db.commit()
        
        return {
            'customer_id': customer_id,
            'anomalies': result['anomalies'],
            'overall_score': result['anomaly_score'],
            'is_anomalous': result['is_anomalous']
        }
