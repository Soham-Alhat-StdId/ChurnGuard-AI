# ChurnGuard AI API Documentation

## Base URL
```
http://localhost:8000/api/v1
```

## Authentication
Currently, the API is open. In production, implement API key authentication.

## Endpoints

### Health Check

#### GET /health
Check API health status

**Response:**
```json
{
  "status": "healthy",
  "version": "1.0.0"
}
```

---

## Predictions

### Predict Churn

#### POST /predictions/predict
Predict churn probability for a customer using ensemble ML model.

**Request Body:**
```json
{
  "customer_id": 1
}
```

**Response:**
```json
{
  "customer_id": 1,
  "xgboost_score": 0.72,
  "nn_score": 0.68,
  "ensemble_score": 0.704,
  "risk_level": "high",
  "shap_values": {
    "days_since_last_order": 0.15,
    "email_open_rate": -0.08,
    "total_orders": -0.12
  },
  "top_features": [
    {
      "feature": "days_since_last_order",
      "shap_value": 0.15,
      "feature_value": 200
    }
  ],
  "prediction_date": "2024-02-08T12:00:00"
}
```

### Batch Predict

#### POST /predictions/predict/batch
Predict churn for multiple customers at once.

**Request Body:**
```json
[1, 2, 3, 4, 5]
```

**Response:**
```json
{
  "predictions": [
    {
      "customer_id": 1,
      "ensemble_score": 0.704,
      "risk_level": "high"
    },
    ...
  ]
}
```

### Get High-Risk Customers

#### GET /predictions/high-risk?limit=100
Get list of customers with high churn risk.

**Query Parameters:**
- `limit` (optional): Number of customers to return (default: 100)

**Response:**
```json
[
  {
    "id": 1,
    "name": "John Smith",
    "email": "john@example.com",
    "churn_probability": 0.85,
    "churn_risk_level": "high",
    "total_spent": 2500.00
  }
]
```

### Predict CLV

#### POST /predictions/clv/predict
Predict Customer Lifetime Value.

**Request Body:**
```json
{
  "customer_id": 1
}
```

**Response:**
```json
{
  "customer_id": 1,
  "predicted_clv": 3500.50,
  "clv_segment": "gold",
  "confidence_interval": {
    "lower": 3200.00,
    "upper": 3800.00,
    "std": 150.25
  }
}
```

### Detect Anomalies

#### POST /predictions/anomaly/detect?customer_id=1
Detect behavioral anomalies for a customer.

**Query Parameters:**
- `customer_id` (required): Customer ID

**Response:**
```json
{
  "customer_id": 1,
  "anomalies": [
    {
      "type": "behavior",
      "description": "Customer has been inactive for over 180 days",
      "severity": "high",
      "feature": "days_since_last_order",
      "value": 200
    }
  ],
  "overall_score": 0.15,
  "is_anomalous": true
}
```

---

## Customers

### List Customers

#### GET /customers?skip=0&limit=100
List all customers with pagination.

**Query Parameters:**
- `skip` (optional): Number of records to skip (default: 0)
- `limit` (optional): Number of records to return (default: 100)

**Response:**
```json
[
  {
    "id": 1,
    "external_id": "CUST-1001",
    "email": "john@example.com",
    "name": "John Smith",
    "total_orders": 15,
    "total_spent": 2500.00,
    "churn_probability": 0.35,
    "created_at": "2024-01-01T00:00:00"
  }
]
```

### Get Customer

#### GET /customers/{customer_id}
Get detailed information about a customer.

**Response:**
```json
{
  "id": 1,
  "external_id": "CUST-1001",
  "email": "john@example.com",
  "name": "John Smith",
  "total_orders": 15,
  "total_spent": 2500.00,
  "avg_order_value": 166.67,
  "days_since_last_order": 30,
  "order_frequency": 2.5,
  "email_open_rate": 0.75,
  "churn_probability": 0.35,
  "churn_risk_level": "low",
  "predicted_clv": 3500.00,
  "created_at": "2024-01-01T00:00:00"
}
```

### Create Customer

#### POST /customers
Create a new customer.

**Request Body:**
```json
{
  "email": "jane@example.com",
  "name": "Jane Doe",
  "external_id": "CUST-1002"
}
```

**Response:**
```json
{
  "id": 2,
  "external_id": "CUST-1002",
  "email": "jane@example.com",
  "name": "Jane Doe",
  "total_orders": 0,
  "total_spent": 0.0,
  "created_at": "2024-02-08T12:00:00"
}
```

### Update Customer

#### PUT /customers/{customer_id}
Update customer information.

**Request Body:**
```json
{
  "name": "Jane Smith",
  "email": "jane.smith@example.com"
}
```

### Create Transaction

#### POST /customers/transactions
Create a new transaction for a customer.

**Request Body:**
```json
{
  "customer_id": 1,
  "external_id": "TXN-1001",
  "amount": 150.00,
  "items_count": 3,
  "discount_amount": 15.00,
  "transaction_date": "2024-02-08T12:00:00",
  "status": "completed"
}
```

---

## Campaigns

### List Campaigns

#### GET /campaigns?skip=0&limit=100
List all campaigns.

**Response:**
```json
[
  {
    "id": 1,
    "customer_id": 1,
    "campaign_type": "email",
    "campaign_name": "Win-back Campaign",
    "status": "sent",
    "sent_at": "2024-02-08T12:00:00",
    "trigger_reason": "high_churn_risk",
    "trigger_score": 0.85
  }
]
```

### Create Campaign

#### POST /campaigns
Create a new campaign.

**Request Body:**
```json
{
  "customer_id": 1,
  "campaign_type": "email",
  "campaign_name": "Special Offer",
  "message_template": "Hi {{name}}, we have a special offer for you!",
  "trigger_reason": "high_churn_risk",
  "trigger_score": 0.85
}
```

### Send Campaign

#### POST /campaigns/{campaign_id}/send
Send a campaign to the customer.

**Response:**
```json
{
  "message": "Campaign sent successfully",
  "campaign_id": 1
}
```

### Create Automated Campaigns

#### POST /campaigns/automated/high-risk
Automatically create campaigns for all high-risk customers.

**Response:**
```json
{
  "message": "Created 15 automated campaigns",
  "campaigns": [...]
}
```

---

## Dashboard

### Get Dashboard Metrics

#### GET /dashboard
Get overall dashboard metrics and KPIs.

**Response:**
```json
{
  "total_customers": 100,
  "high_risk_customers": 15,
  "medium_risk_customers": 35,
  "low_risk_customers": 50,
  "avg_churn_probability": 0.42,
  "avg_clv": 2500.00,
  "total_campaigns_sent": 50,
  "campaign_success_rate": 65.5,
  "retention_lift": 12.5,
  "roi": 4.5
}
```

---

## Error Responses

All endpoints may return error responses:

**404 Not Found:**
```json
{
  "detail": "Customer not found"
}
```

**500 Internal Server Error:**
```json
{
  "detail": "Internal server error message"
}
```

**422 Validation Error:**
```json
{
  "detail": [
    {
      "loc": ["body", "customer_id"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

---

## Rate Limiting
Currently no rate limiting is implemented. In production, implement rate limiting per API key.

## Webhooks
Webhook support coming soon for real-time notifications.

For interactive API documentation, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
