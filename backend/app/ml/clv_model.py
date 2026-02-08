import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
import joblib
import os
from typing import Dict, Tuple


class CLVModel:
    """Customer Lifetime Value prediction model"""
    
    def __init__(self, model_path: str = "./models"):
        self.model_path = model_path
        self.model = None
        self.scaler = None
        self.feature_names = [
            'total_orders', 'total_spent', 'avg_order_value',
            'order_frequency', 'days_since_last_order',
            'email_open_rate', 'app_sessions'
        ]
        
        self._initialize_model()
    
    def _initialize_model(self):
        """Initialize or load pre-trained model"""
        model_path = os.path.join(self.model_path, "clv_model.pkl")
        scaler_path = os.path.join(self.model_path, "clv_scaler.pkl")
        
        os.makedirs(self.model_path, exist_ok=True)
        
        try:
            self.model = joblib.load(model_path)
            self.scaler = joblib.load(scaler_path)
        except FileNotFoundError:
            self._create_default_model()
            self._save_model()
    
    def _create_default_model(self):
        """Create default trained model"""
        self.model = RandomForestRegressor(
            n_estimators=100,
            max_depth=10,
            random_state=42
        )
        self.scaler = StandardScaler()
        
        # Train with synthetic data
        X_train = self._generate_synthetic_data(1000)
        y_train = self._generate_synthetic_clv(X_train)
        
        X_scaled = self.scaler.fit_transform(X_train)
        self.model.fit(X_scaled, y_train)
    
    def _generate_synthetic_data(self, n_samples: int) -> np.ndarray:
        """Generate synthetic customer data"""
        np.random.seed(42)
        data = {
            'total_orders': np.random.randint(1, 50, n_samples),
            'total_spent': np.random.uniform(50, 5000, n_samples),
            'avg_order_value': np.random.uniform(20, 500, n_samples),
            'order_frequency': np.random.uniform(0.1, 10, n_samples),
            'days_since_last_order': np.random.randint(0, 365, n_samples),
            'email_open_rate': np.random.uniform(0, 1, n_samples),
            'app_sessions': np.random.randint(0, 100, n_samples)
        }
        return pd.DataFrame(data).values
    
    def _generate_synthetic_clv(self, X: np.ndarray) -> np.ndarray:
        """Generate synthetic CLV based on features"""
        # CLV estimation: orders * avg_value * frequency * engagement
        clv = []
        for row in X:
            base_clv = row[0] * row[2] * row[3]  # orders * avg_value * frequency
            engagement_factor = 1 + (row[5] * 0.5)  # email engagement boost
            clv_value = base_clv * engagement_factor * np.random.uniform(0.8, 1.2)
            clv.append(max(clv_value, 100))  # Minimum CLV of 100
        
        return np.array(clv)
    
    def _save_model(self):
        """Save model to disk"""
        model_path = os.path.join(self.model_path, "clv_model.pkl")
        scaler_path = os.path.join(self.model_path, "clv_scaler.pkl")
        
        joblib.dump(self.model, model_path)
        joblib.dump(self.scaler, scaler_path)
    
    def prepare_features(self, customer_data: Dict) -> np.ndarray:
        """Prepare features from customer data"""
        features = []
        for feature_name in self.feature_names:
            features.append(customer_data.get(feature_name, 0))
        
        return np.array(features).reshape(1, -1)
    
    def predict(self, customer_data: Dict) -> Tuple[float, str, Dict]:
        """
        Predict customer lifetime value
        
        Returns:
            Tuple of (predicted_clv, segment, confidence_interval)
        """
        features = self.prepare_features(customer_data)
        features_scaled = self.scaler.transform(features)
        
        # Predict CLV
        predicted_clv = float(self.model.predict(features_scaled)[0])
        
        # Determine segment
        segment = self._get_clv_segment(predicted_clv)
        
        # Calculate confidence interval (using tree predictions variance)
        predictions = np.array([tree.predict(features_scaled)[0] 
                               for tree in self.model.estimators_])
        std = np.std(predictions)
        confidence_interval = {
            'lower': float(predicted_clv - 1.96 * std),
            'upper': float(predicted_clv + 1.96 * std),
            'std': float(std)
        }
        
        return predicted_clv, segment, confidence_interval
    
    def _get_clv_segment(self, clv: float) -> str:
        """Determine CLV segment"""
        if clv >= 5000:
            return "platinum"
        elif clv >= 2000:
            return "gold"
        elif clv >= 1000:
            return "silver"
        else:
            return "bronze"
