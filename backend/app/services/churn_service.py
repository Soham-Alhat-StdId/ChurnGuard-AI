from typing import Optional, Dict
from datetime import datetime
from sqlalchemy.orm import Session
from app.models.database_models import Customer, ChurnPrediction, Campaign
from app.ml.churn_model import ChurnPredictionModel
from app.core.config import settings


class ChurnPredictionService:
    """Service for churn prediction operations"""
    
    def __init__(self):
        self.model = ChurnPredictionModel(model_path=settings.MODEL_PATH)
    
    def predict_churn(self, db: Session, customer_id: int) -> Dict:
        """
        Predict churn for a customer and save to database
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
        
        # Get predictions
        xgb_score, nn_score, ensemble_score = self.model.predict(customer_data)
        risk_level = self.model.get_risk_level(ensemble_score)
        
        # Get explanation
        explanation = self.model.explain_prediction(customer_data)
        
        # Update customer record
        customer.churn_probability = ensemble_score
        customer.churn_risk_level = risk_level
        customer.last_prediction_date = datetime.utcnow()
        
        # Save prediction to history
        prediction = ChurnPrediction(
            customer_id=customer_id,
            xgboost_score=xgb_score,
            nn_score=nn_score,
            ensemble_score=ensemble_score,
            risk_level=risk_level,
            shap_values=explanation['shap_values'],
            top_features=explanation['top_features'],
            model_version="1.0.0",
            prediction_date=datetime.utcnow()
        )
        
        db.add(prediction)
        db.commit()
        db.refresh(prediction)
        
        return {
            'customer_id': customer_id,
            'xgboost_score': xgb_score,
            'nn_score': nn_score,
            'ensemble_score': ensemble_score,
            'risk_level': risk_level,
            'shap_values': explanation['shap_values'],
            'top_features': explanation['top_features'],
            'prediction_date': prediction.prediction_date
        }
    
    def predict_batch(self, db: Session, customer_ids: list) -> list:
        """Predict churn for multiple customers"""
        results = []
        for customer_id in customer_ids:
            try:
                result = self.predict_churn(db, customer_id)
                results.append(result)
            except Exception as e:
                results.append({
                    'customer_id': customer_id,
                    'error': str(e)
                })
        
        return results
    
    def get_high_risk_customers(self, db: Session, limit: int = 100) -> list:
        """Get customers with high churn risk"""
        customers = db.query(Customer).filter(
            Customer.churn_risk_level == 'high'
        ).order_by(Customer.churn_probability.desc()).limit(limit).all()
        
        return customers
