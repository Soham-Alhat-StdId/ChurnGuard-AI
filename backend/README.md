# ChurnGuard AI Backend

This directory contains the backend API for ChurnGuard AI.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set environment variables (create a `.env` file):
```
DATABASE_URL=postgresql://user:password@localhost:5432/churnguard_db
REDIS_HOST=localhost
REDIS_PORT=6379
```

3. Run the application:
```bash
uvicorn app.main:app --reload
```

## API Documentation

Once running, access the interactive API documentation at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Endpoints

### Predictions
- `POST /api/v1/predictions/predict` - Predict churn for a customer
- `POST /api/v1/predictions/predict/batch` - Batch prediction
- `GET /api/v1/predictions/high-risk` - Get high-risk customers
- `POST /api/v1/predictions/clv/predict` - Predict CLV
- `POST /api/v1/predictions/anomaly/detect` - Detect anomalies

### Customers
- `POST /api/v1/customers/` - Create customer
- `GET /api/v1/customers/{id}` - Get customer
- `GET /api/v1/customers/` - List customers
- `PUT /api/v1/customers/{id}` - Update customer
- `DELETE /api/v1/customers/{id}` - Delete customer

### Campaigns
- `POST /api/v1/campaigns/` - Create campaign
- `POST /api/v1/campaigns/{id}/send` - Send campaign
- `POST /api/v1/campaigns/automated/high-risk` - Auto-create campaigns

### Dashboard
- `GET /api/v1/dashboard/` - Get dashboard metrics
