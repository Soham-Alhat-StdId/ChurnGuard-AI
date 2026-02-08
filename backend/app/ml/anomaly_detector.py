import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import joblib
import os
from typing import Dict, List


class AnomalyDetector:
    """Anomaly detection for customer behavior"""
    
    def __init__(self, model_path: str = "./models"):
        self.model_path = model_path
        self.model = None
        self.scaler = None
        self.feature_names = [
            'total_orders', 'total_spent', 'avg_order_value',
            'days_since_last_order', 'order_frequency',
            'email_open_rate', 'email_click_rate',
            'sms_engagement_rate', 'app_sessions'
        ]
        
        self._initialize_model()
    
    def _initialize_model(self):
        """Initialize or load pre-trained model"""
        model_path = os.path.join(self.model_path, "anomaly_model.pkl")
        scaler_path = os.path.join(self.model_path, "anomaly_scaler.pkl")
        
        os.makedirs(self.model_path, exist_ok=True)
        
        try:
            self.model = joblib.load(model_path)
            self.scaler = joblib.load(scaler_path)
        except FileNotFoundError:
            self._create_default_model()
            self._save_model()
    
    def _create_default_model(self):
        """Create default trained model"""
        self.model = IsolationForest(
            contamination=0.1,
            random_state=42,
            n_estimators=100
        )
        self.scaler = StandardScaler()
        
        # Train with synthetic data
        X_train = self._generate_synthetic_data(1000)
        X_scaled = self.scaler.fit_transform(X_train)
        self.model.fit(X_scaled)
    
    def _generate_synthetic_data(self, n_samples: int) -> np.ndarray:
        """Generate synthetic customer data"""
        np.random.seed(42)
        data = []
        for _ in range(n_samples):
            data.append([
                np.random.randint(1, 50),           # total_orders
                np.random.uniform(50, 5000),        # total_spent
                np.random.uniform(20, 500),         # avg_order_value
                np.random.randint(0, 365),          # days_since_last_order
                np.random.uniform(0.1, 10),         # order_frequency
                np.random.uniform(0, 1),            # email_open_rate
                np.random.uniform(0, 0.5),          # email_click_rate
                np.random.uniform(0, 1),            # sms_engagement_rate
                np.random.randint(0, 100)           # app_sessions
            ])
        
        return np.array(data)
    
    def _save_model(self):
        """Save model to disk"""
        model_path = os.path.join(self.model_path, "anomaly_model.pkl")
        scaler_path = os.path.join(self.model_path, "anomaly_scaler.pkl")
        
        joblib.dump(self.model, model_path)
        joblib.dump(self.scaler, scaler_path)
    
    def prepare_features(self, customer_data: Dict) -> np.ndarray:
        """Prepare features from customer data"""
        features = []
        for feature_name in self.feature_names:
            features.append(customer_data.get(feature_name, 0))
        
        return np.array(features).reshape(1, -1)
    
    def detect(self, customer_data: Dict) -> Dict:
        """
        Detect anomalies in customer behavior
        
        Returns:
            Dictionary with anomaly detection results
        """
        features = self.prepare_features(customer_data)
        features_scaled = self.scaler.transform(features)
        
        # Predict anomaly (-1 for anomaly, 1 for normal)
        prediction = self.model.predict(features_scaled)[0]
        
        # Get anomaly score (lower is more anomalous)
        score = float(self.model.score_samples(features_scaled)[0])
        
        # Identify specific anomalies
        anomalies = self._identify_specific_anomalies(customer_data, features[0])
        
        return {
            'is_anomalous': prediction == -1,
            'anomaly_score': abs(score),
            'anomalies': anomalies
        }
    
    def _identify_specific_anomalies(self, customer_data: Dict, features: np.ndarray) -> List[Dict]:
        """Identify specific types of anomalies"""
        anomalies = []
        
        # Check for transaction anomalies
        if customer_data.get('days_since_last_order', 0) > 180:
            anomalies.append({
                'type': 'behavior',
                'description': 'Customer has been inactive for over 180 days',
                'severity': 'high',
                'feature': 'days_since_last_order',
                'value': customer_data.get('days_since_last_order', 0)
            })
        
        # Check for engagement anomalies
        if customer_data.get('email_open_rate', 0) < 0.1:
            anomalies.append({
                'type': 'engagement',
                'description': 'Very low email engagement rate',
                'severity': 'medium',
                'feature': 'email_open_rate',
                'value': customer_data.get('email_open_rate', 0)
            })
        
        # Check for order frequency anomalies
        if customer_data.get('order_frequency', 0) < 0.5 and customer_data.get('total_orders', 0) > 5:
            anomalies.append({
                'type': 'transaction',
                'description': 'Decreasing order frequency for established customer',
                'severity': 'high',
                'feature': 'order_frequency',
                'value': customer_data.get('order_frequency', 0)
            })
        
        # Check for high-value customer at risk
        if customer_data.get('total_spent', 0) > 2000 and customer_data.get('days_since_last_order', 0) > 90:
            anomalies.append({
                'type': 'behavior',
                'description': 'High-value customer showing signs of churn',
                'severity': 'critical',
                'feature': 'total_spent',
                'value': customer_data.get('total_spent', 0)
            })
        
        return anomalies
