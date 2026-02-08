from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas import schemas
from app.models.database_models import Customer
from app.services.churn_service import ChurnPredictionService
from app.services.clv_service import CLVService
from app.services.anomaly_service import AnomalyDetectionService

router = APIRouter()
churn_service = ChurnPredictionService()
clv_service = CLVService()
anomaly_service = AnomalyDetectionService()


@router.post("/predict", response_model=schemas.ChurnPredictionResponse)
def predict_churn(
    request: schemas.ChurnPredictionRequest,
    db: Session = Depends(get_db)
):
    """
    Predict churn probability for a customer using ensemble ML model
    Returns XGBoost, Neural Network, and ensemble scores with SHAP explanations
    """
    try:
        result = churn_service.predict_churn(db, request.customer_id)
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/predict/batch")
def predict_churn_batch(
    customer_ids: List[int],
    db: Session = Depends(get_db)
):
    """
    Predict churn for multiple customers in batch
    """
    try:
        results = churn_service.predict_batch(db, customer_ids)
        return {"predictions": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/high-risk", response_model=List[schemas.Customer])
def get_high_risk_customers(
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Get customers with high churn risk
    """
    try:
        customers = churn_service.get_high_risk_customers(db, limit)
        return customers
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/clv/predict", response_model=schemas.CLVPredictionResponse)
def predict_clv(
    request: schemas.CLVPredictionRequest,
    db: Session = Depends(get_db)
):
    """
    Predict Customer Lifetime Value for a customer
    """
    try:
        result = clv_service.predict_clv(db, request.customer_id)
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/anomaly/detect", response_model=schemas.AnomalyDetectionResponse)
def detect_anomalies(
    customer_id: int,
    db: Session = Depends(get_db)
):
    """
    Detect anomalies in customer behavior
    """
    try:
        result = anomaly_service.detect_anomalies(db, customer_id)
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
