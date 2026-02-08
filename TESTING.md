# Testing Guide for ChurnGuard AI

## Overview
This guide covers how to test the ChurnGuard AI platform.

## Prerequisites
- Backend server running on http://localhost:8000
- Frontend running on http://localhost:3000 (optional)
- Sample data loaded

## 1. Manual API Testing

### Using curl

#### Health Check
```bash
curl http://localhost:8000/health
```

#### Create a Customer
```bash
curl -X POST http://localhost:8000/api/v1/customers \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "name": "Test User",
    "external_id": "TEST-001"
  }'
```

#### Predict Churn
```bash
curl -X POST http://localhost:8000/api/v1/predictions/predict \
  -H "Content-Type: application/json" \
  -d '{"customer_id": 1}'
```

#### Get Dashboard Metrics
```bash
curl http://localhost:8000/api/v1/dashboard
```

### Using the Demo Script

Run the automated demo:
```bash
cd scripts
python demo.py
```

This will:
1. Check API health
2. Create a sample customer
3. Add a transaction
4. Predict churn with SHAP explanations
5. Predict CLV
6. Detect anomalies
7. Create an automated campaign
8. Display dashboard metrics

## 2. Frontend Testing

### Dashboard Page
1. Navigate to http://localhost:3000
2. Verify metrics display:
   - Total customers count
   - Risk level distribution
   - Average churn probability
   - Average CLV
   - Retention lift and ROI
3. Check high-risk customers table

### Customers Page
1. Navigate to http://localhost:3000/customers
2. Verify customer list displays
3. Click "Predict" button on a customer
4. Verify prediction panel shows:
   - Ensemble score with risk level
   - XGBoost and NN model scores
   - SHAP explainability with top features

## 3. Integration Testing

### Shopify Integration Test
```python
import asyncio
from backend.app.integrations.ecommerce import ShopifyIntegration

async def test_shopify():
    shopify = ShopifyIntegration(
        api_key="your_key",
        api_secret="your_secret",
        shop_domain="your-store.myshopify.com"
    )
    
    customers = await shopify.get_customers()
    print(f"Fetched {len(customers)} customers")

asyncio.run(test_shopify())
```

### WooCommerce Integration Test
```python
import asyncio
from backend.app.integrations.ecommerce import WooCommerceIntegration

async def test_woocommerce():
    woo = WooCommerceIntegration(
        api_key="your_key",
        api_secret="your_secret",
        store_url="https://your-store.com"
    )
    
    customers = await woo.get_customers()
    print(f"Fetched {len(customers)} customers")

asyncio.run(test_woocommerce())
```

## 4. ML Model Testing

### Test Churn Model
```python
from backend.app.ml.churn_model import ChurnPredictionModel

model = ChurnPredictionModel()

customer_data = {
    'total_orders': 5,
    'total_spent': 500.0,
    'avg_order_value': 100.0,
    'days_since_last_order': 200,
    'order_frequency': 0.5,
    'email_open_rate': 0.2,
    'email_click_rate': 0.1,
    'sms_engagement_rate': 0.3,
    'app_sessions': 5
}

xgb_score, nn_score, ensemble_score = model.predict(customer_data)
risk_level = model.get_risk_level(ensemble_score)
explanation = model.explain_prediction(customer_data)

print(f"Ensemble Score: {ensemble_score:.2%}")
print(f"Risk Level: {risk_level}")
print(f"Top Features: {explanation['top_features'][:3]}")
```

### Test CLV Model
```python
from backend.app.ml.clv_model import CLVModel

model = CLVModel()

customer_data = {
    'total_orders': 10,
    'total_spent': 1000.0,
    'avg_order_value': 100.0,
    'order_frequency': 2.0,
    'days_since_last_order': 30,
    'email_open_rate': 0.7,
    'app_sessions': 20
}

predicted_clv, segment, confidence = model.predict(customer_data)

print(f"Predicted CLV: ${predicted_clv:.2f}")
print(f"Segment: {segment}")
print(f"Confidence Interval: ${confidence['lower']:.2f} - ${confidence['upper']:.2f}")
```

### Test Anomaly Detector
```python
from backend.app.ml.anomaly_detector import AnomalyDetector

detector = AnomalyDetector()

customer_data = {
    'total_orders': 2,
    'total_spent': 100.0,
    'avg_order_value': 50.0,
    'days_since_last_order': 250,
    'order_frequency': 0.2,
    'email_open_rate': 0.05,
    'email_click_rate': 0.01,
    'sms_engagement_rate': 0.1,
    'app_sessions': 1
}

result = detector.detect(customer_data)

print(f"Is Anomalous: {result['is_anomalous']}")
print(f"Anomalies Found: {len(result['anomalies'])}")
for anomaly in result['anomalies']:
    print(f"  - {anomaly['description']}")
```

## 5. Performance Testing

### Load Test with Apache Bench
```bash
# Install Apache Bench
sudo apt-get install apache2-utils

# Test prediction endpoint
ab -n 1000 -c 10 -p payload.json -T application/json \
  http://localhost:8000/api/v1/predictions/predict
```

payload.json:
```json
{"customer_id": 1}
```

### Expected Performance
- Single prediction: < 100ms
- Batch prediction (10 customers): < 500ms
- Dashboard metrics: < 50ms

## 6. Docker Testing

### Test with Docker Compose
```bash
# Start all services
docker-compose up -d

# Check service health
docker-compose ps

# View logs
docker-compose logs backend
docker-compose logs frontend

# Test backend
curl http://localhost:8000/health

# Test frontend
curl http://localhost:3000

# Stop services
docker-compose down
```

## 7. Database Testing

### Verify Database Schema
```bash
docker-compose exec postgres psql -U churnguard -d churnguard_db

# List tables
\dt

# Check customers table
SELECT COUNT(*) FROM customers;

# Check predictions table
SELECT COUNT(*) FROM churn_predictions;

# Exit
\q
```

## 8. Common Issues and Solutions

### Issue: API not responding
**Solution**: Check if backend is running:
```bash
ps aux | grep uvicorn
```

### Issue: Frontend can't connect to API
**Solution**: Check REACT_APP_API_URL in frontend/.env:
```bash
echo "REACT_APP_API_URL=http://localhost:8000/api/v1" > frontend/.env
```

### Issue: Database connection failed
**Solution**: Ensure PostgreSQL is running:
```bash
docker-compose ps postgres
```

### Issue: ML models not loading
**Solution**: Models are created automatically on first run. Check logs:
```bash
docker-compose logs backend | grep -i model
```

## 9. Automated Testing

### Run Backend Tests
```bash
cd backend
pytest tests/ -v
```

### Run Frontend Tests
```bash
cd frontend
npm test
```

## 10. Validation Checklist

- [ ] API health check passes
- [ ] Can create customers via API
- [ ] Can create transactions via API
- [ ] Churn prediction returns valid scores (0-1)
- [ ] SHAP values are provided in predictions
- [ ] CLV prediction returns positive values
- [ ] Anomaly detection identifies issues
- [ ] Dashboard displays correct metrics
- [ ] Frontend loads without errors
- [ ] Customer list displays in UI
- [ ] Prediction panel shows results
- [ ] Can create campaigns via API
- [ ] Docker Compose starts all services
- [ ] Database tables are created

## Success Criteria

✅ All API endpoints respond with 200 status
✅ ML predictions complete in < 100ms
✅ Frontend loads and displays data
✅ SHAP explanations are provided
✅ No errors in backend/frontend logs
✅ Database operations succeed
✅ Docker services run successfully

For issues or questions, check the main README.md or API_DOCUMENTATION.md
