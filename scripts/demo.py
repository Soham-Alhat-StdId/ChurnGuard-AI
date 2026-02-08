"""
Demo script to showcase ChurnGuard AI capabilities
Run this after starting the backend server
"""

import requests
import json
import time
from datetime import datetime

API_BASE_URL = "http://localhost:8000/api/v1"


def print_section(title):
    """Print a section header"""
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60 + "\n")


def test_health_check():
    """Test API health"""
    print_section("1. Health Check")
    response = requests.get(f"{API_BASE_URL.replace('/api/v1', '')}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.status_code == 200


def create_sample_customer():
    """Create a sample customer"""
    print_section("2. Create Sample Customer")
    
    customer_data = {
        "email": "demo.customer@example.com",
        "name": "Demo Customer",
        "external_id": "DEMO-001"
    }
    
    response = requests.post(f"{API_BASE_URL}/customers", json=customer_data)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        customer = response.json()
        print(f"Created customer: {json.dumps(customer, indent=2, default=str)}")
        return customer['id']
    else:
        print(f"Error: {response.text}")
        return None


def add_transaction(customer_id):
    """Add a transaction for the customer"""
    print_section("3. Add Transaction")
    
    transaction_data = {
        "customer_id": customer_id,
        "external_id": f"TXN-DEMO-{int(time.time())}",
        "amount": 150.00,
        "items_count": 3,
        "discount_amount": 15.00,
        "transaction_date": datetime.utcnow().isoformat(),
        "status": "completed"
    }
    
    response = requests.post(f"{API_BASE_URL}/customers/transactions", json=transaction_data)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        transaction = response.json()
        print(f"Created transaction: {json.dumps(transaction, indent=2, default=str)}")
        return True
    else:
        print(f"Error: {response.text}")
        return False


def predict_churn(customer_id):
    """Predict churn for a customer"""
    print_section("4. Predict Churn (Ensemble ML)")
    
    prediction_data = {
        "customer_id": customer_id
    }
    
    response = requests.post(f"{API_BASE_URL}/predictions/predict", json=prediction_data)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        prediction = response.json()
        print(f"\n📊 Churn Prediction Results:")
        print(f"   XGBoost Score:    {prediction['xgboost_score']:.2%}")
        print(f"   Neural Net Score: {prediction['nn_score']:.2%}")
        print(f"   Ensemble Score:   {prediction['ensemble_score']:.2%}")
        print(f"   Risk Level:       {prediction['risk_level'].upper()}")
        
        print(f"\n🔍 Top Contributing Factors (SHAP):")
        for i, feature in enumerate(prediction['top_features'][:3], 1):
            print(f"   {i}. {feature['feature']}: {feature['shap_value']:.4f}")
        
        return prediction
    else:
        print(f"Error: {response.text}")
        return None


def predict_clv(customer_id):
    """Predict Customer Lifetime Value"""
    print_section("5. Predict Customer Lifetime Value")
    
    clv_data = {
        "customer_id": customer_id
    }
    
    response = requests.post(f"{API_BASE_URL}/predictions/clv/predict", json=clv_data)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        clv = response.json()
        print(f"\n💰 CLV Prediction:")
        print(f"   Predicted CLV: ${clv['predicted_clv']:.2f}")
        print(f"   Segment:       {clv['clv_segment'].upper()}")
        print(f"   Confidence:    ${clv['confidence_interval']['lower']:.2f} - ${clv['confidence_interval']['upper']:.2f}")
        return clv
    else:
        print(f"Error: {response.text}")
        return None


def detect_anomalies(customer_id):
    """Detect behavioral anomalies"""
    print_section("6. Detect Anomalies")
    
    response = requests.post(f"{API_BASE_URL}/predictions/anomaly/detect?customer_id={customer_id}")
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"\n🔔 Anomaly Detection:")
        print(f"   Is Anomalous:   {result['is_anomalous']}")
        print(f"   Anomaly Score:  {result['overall_score']:.4f}")
        
        if result['anomalies']:
            print(f"\n   Detected Issues:")
            for anomaly in result['anomalies']:
                print(f"   - {anomaly['description']} (Severity: {anomaly['severity']})")
        
        return result
    else:
        print(f"Error: {response.text}")
        return None


def get_dashboard_metrics():
    """Get dashboard metrics"""
    print_section("7. Dashboard Metrics")
    
    response = requests.get(f"{API_BASE_URL}/dashboard")
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        metrics = response.json()
        print(f"\n📈 Platform Metrics:")
        print(f"   Total Customers:      {metrics['total_customers']}")
        print(f"   High Risk:            {metrics['high_risk_customers']}")
        print(f"   Average Churn Prob:   {metrics['avg_churn_probability']:.2%}")
        print(f"   Average CLV:          ${metrics['avg_clv']:.2f}")
        print(f"   Retention Lift:       {metrics['retention_lift']}%")
        print(f"   ROI:                  {metrics['roi']}x")
        return metrics
    else:
        print(f"Error: {response.text}")
        return None


def create_campaign(customer_id):
    """Create an automated campaign"""
    print_section("8. Create Automated Campaign")
    
    campaign_data = {
        "customer_id": customer_id,
        "campaign_type": "email",
        "campaign_name": "Demo Win-back Campaign",
        "message_template": "Hi there! We miss you. Come back for a special offer!",
        "trigger_reason": "demo",
        "trigger_score": 0.75
    }
    
    response = requests.post(f"{API_BASE_URL}/campaigns", json=campaign_data)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        campaign = response.json()
        print(f"✅ Campaign created successfully!")
        print(f"   Campaign ID:   {campaign['id']}")
        print(f"   Type:          {campaign['campaign_type']}")
        print(f"   Status:        {campaign['status']}")
        return campaign['id']
    else:
        print(f"Error: {response.text}")
        return None


def main():
    """Run the demo"""
    print("\n" + "🚀 "*20)
    print("   ChurnGuard AI - Platform Demo")
    print("   E-commerce Retention with ML")
    print("🚀 "*20)
    
    # Check if API is running
    try:
        if not test_health_check():
            print("\n❌ API is not running. Please start it with:")
            print("   cd backend && uvicorn app.main:app --reload")
            return
    except Exception as e:
        print(f"\n❌ Cannot connect to API: {e}")
        print("   Please start the backend server first.")
        return
    
    # Run demo steps
    customer_id = create_sample_customer()
    
    if customer_id:
        time.sleep(1)
        add_transaction(customer_id)
        
        time.sleep(1)
        predict_churn(customer_id)
        
        time.sleep(1)
        predict_clv(customer_id)
        
        time.sleep(1)
        detect_anomalies(customer_id)
        
        time.sleep(1)
        create_campaign(customer_id)
    
    time.sleep(1)
    get_dashboard_metrics()
    
    print("\n" + "✅ "*20)
    print("   Demo Complete!")
    print("   Visit http://localhost:3000 for the UI")
    print("   API Docs: http://localhost:8000/docs")
    print("✅ "*20 + "\n")


if __name__ == "__main__":
    main()
