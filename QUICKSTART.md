# ChurnGuard AI - Quick Start Guide

## Getting Started in 5 Minutes

### Option 1: Using Docker (Recommended)

1. **Clone and Start**
```bash
git clone https://github.com/Soham-Alhat-StdId/ChurnGuard-AI.git
cd ChurnGuard-AI
docker-compose up -d
```

2. **Generate Sample Data**
```bash
docker-compose exec backend python scripts/generate_sample_data.py
```

3. **Access the Application**
- Frontend: http://localhost:3000
- API Docs: http://localhost:8000/docs

### Option 2: Local Development

#### Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

#### Frontend
```bash
cd frontend
npm install
npm start
```

## Basic Usage

### 1. View Dashboard
Navigate to http://localhost:3000 to see:
- Total customers and risk distribution
- Average churn probability
- Customer lifetime value metrics
- Campaign performance
- High-risk customers list

### 2. Predict Churn
Click on any customer to get:
- Churn probability (0-100%)
- Risk level (low/medium/high)
- Ensemble model scores (XGBoost + NN)
- SHAP explainability showing why

### 3. Create Automated Campaigns
```bash
curl -X POST http://localhost:8000/api/v1/campaigns/automated/high-risk
```

This automatically creates personalized retention campaigns for high-risk customers.

## API Examples

### Predict Churn
```bash
curl -X POST http://localhost:8000/api/v1/predictions/predict \
  -H "Content-Type: application/json" \
  -d '{"customer_id": 1}'
```

### Get High-Risk Customers
```bash
curl http://localhost:8000/api/v1/predictions/high-risk?limit=10
```

### Predict CLV
```bash
curl -X POST http://localhost:8000/api/v1/predictions/clv/predict \
  -H "Content-Type: application/json" \
  -d '{"customer_id": 1}'
```

## Integration Examples

### Shopify Integration
```python
from app.integrations.ecommerce import ShopifyIntegration

shopify = ShopifyIntegration(
    api_key="your_key",
    api_secret="your_secret",
    shop_domain="your-store.myshopify.com"
)

customers = await shopify.get_customers()
```

### WooCommerce Integration
```python
from app.integrations.ecommerce import WooCommerceIntegration

woo = WooCommerceIntegration(
    api_key="your_key",
    api_secret="your_secret",
    store_url="https://your-store.com"
)

customers = await woo.get_customers()
```

## Key Features to Try

1. **Multi-Modal Prediction**: The system analyzes transactions, behavior, and engagement
2. **SHAP Explainability**: See exactly why a customer is at risk
3. **Automated Campaigns**: Set up once, runs automatically
4. **CLV Forecasting**: Identify high-value customers to retain
5. **Anomaly Detection**: Catch unusual behavior early

## Troubleshooting

**Database connection issues?**
- Check that PostgreSQL is running on port 5432
- Verify DATABASE_URL in .env file

**Frontend can't connect to backend?**
- Ensure backend is running on port 8000
- Check REACT_APP_API_URL in frontend/.env

**No predictions showing?**
- Run the sample data generation script
- Make sure ML models are initialized (happens automatically on first run)

## Next Steps

1. Import your real customer data via API
2. Set up Shopify/WooCommerce integration
3. Configure email (SendGrid) and SMS (Twilio) credentials
4. Customize campaign templates
5. Monitor retention metrics on dashboard

For detailed documentation, see README.md
