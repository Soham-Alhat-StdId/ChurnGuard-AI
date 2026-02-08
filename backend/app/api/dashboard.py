from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db
from app.schemas import schemas
from app.models.database_models import Customer, Campaign

router = APIRouter()


@router.get("/", response_model=schemas.DashboardMetrics)
def get_dashboard_metrics(
    db: Session = Depends(get_db)
):
    """
    Get dashboard metrics and KPIs
    """
    # Count customers by risk level
    total_customers = db.query(func.count(Customer.id)).scalar()
    high_risk = db.query(func.count(Customer.id)).filter(
        Customer.churn_risk_level == 'high'
    ).scalar()
    medium_risk = db.query(func.count(Customer.id)).filter(
        Customer.churn_risk_level == 'medium'
    ).scalar()
    low_risk = db.query(func.count(Customer.id)).filter(
        Customer.churn_risk_level == 'low'
    ).scalar()
    
    # Average churn probability
    avg_churn = db.query(func.avg(Customer.churn_probability)).filter(
        Customer.churn_probability.isnot(None)
    ).scalar() or 0.0
    
    # Average CLV
    avg_clv = db.query(func.avg(Customer.predicted_clv)).filter(
        Customer.predicted_clv.isnot(None)
    ).scalar() or 0.0
    
    # Campaign metrics
    total_campaigns = db.query(func.count(Campaign.id)).scalar()
    successful_campaigns = db.query(func.count(Campaign.id)).filter(
        Campaign.status == 'delivered'
    ).scalar()
    
    campaign_success_rate = (
        (successful_campaigns / total_campaigns * 100) 
        if total_campaigns > 0 else 0.0
    )
    
    # Estimated metrics (in production, these would be calculated from actual data)
    retention_lift = 12.5  # 12.5% retention lift
    roi = 4.5  # 4.5x ROI
    
    return {
        'total_customers': total_customers or 0,
        'high_risk_customers': high_risk or 0,
        'medium_risk_customers': medium_risk or 0,
        'low_risk_customers': low_risk or 0,
        'avg_churn_probability': float(avg_churn),
        'avg_clv': float(avg_clv),
        'total_campaigns_sent': total_campaigns or 0,
        'campaign_success_rate': campaign_success_rate,
        'retention_lift': retention_lift,
        'roi': roi
    }
