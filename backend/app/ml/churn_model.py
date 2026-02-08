import numpy as np
import pandas as pd
import xgboost as xgb
from tensorflow import keras
from sklearn.preprocessing import StandardScaler
import joblib
import shap
from typing import Dict, List, Tuple
import os


class ChurnPredictionModel:
    """Ensemble model for churn prediction using XGBoost and Neural Network"""
    
    def __init__(self, model_path: str = "./models"):
        self.model_path = model_path
        self.xgb_model = None
        self.nn_model = None
        self.scaler = None
        self.feature_names = [
            'total_orders', 'total_spent', 'avg_order_value',
            'days_since_last_order', 'order_frequency',
            'email_open_rate', 'email_click_rate',
            'sms_engagement_rate', 'app_sessions'
        ]
        
        # Initialize models
        self._initialize_models()
    
    def _initialize_models(self):
        """Initialize or load pre-trained models"""
        xgb_path = os.path.join(self.model_path, "xgboost_churn_model.pkl")
        nn_path = os.path.join(self.model_path, "nn_churn_model.h5")
        scaler_path = os.path.join(self.model_path, "scaler.pkl")
        
        # Create models directory if it doesn't exist
        os.makedirs(self.model_path, exist_ok=True)
        
        try:
            # Try to load existing models
            self.xgb_model = joblib.load(xgb_path)
            self.nn_model = keras.models.load_model(nn_path)
            self.scaler = joblib.load(scaler_path)
        except FileNotFoundError:
            # Create new models if they don't exist
            self._create_default_models()
            self._save_models()
    
    def _create_default_models(self):
        """Create default trained models with synthetic data"""
        # XGBoost model
        self.xgb_model = xgb.XGBClassifier(
            n_estimators=100,
            max_depth=6,
            learning_rate=0.1,
            random_state=42,
            eval_metric='logloss'
        )
        
        # Neural Network model
        self.nn_model = keras.Sequential([
            keras.layers.Dense(64, activation='relu', input_shape=(len(self.feature_names),)),
            keras.layers.Dropout(0.3),
            keras.layers.Dense(32, activation='relu'),
            keras.layers.Dropout(0.2),
            keras.layers.Dense(16, activation='relu'),
            keras.layers.Dense(1, activation='sigmoid')
        ])
        
        self.nn_model.compile(
            optimizer='adam',
            loss='binary_crossentropy',
            metrics=['accuracy']
        )
        
        # Scaler
        self.scaler = StandardScaler()
        
        # Train with synthetic data
        X_train = self._generate_synthetic_data(1000)
        y_train = self._generate_synthetic_labels(X_train)
        
        # Fit scaler
        X_scaled = self.scaler.fit_transform(X_train)
        
        # Train models
        self.xgb_model.fit(X_train, y_train)
        self.nn_model.fit(X_scaled, y_train, epochs=10, verbose=0, validation_split=0.2)
    
    def _generate_synthetic_data(self, n_samples: int) -> np.ndarray:
        """Generate synthetic customer data for initial training"""
        np.random.seed(42)
        data = {
            'total_orders': np.random.randint(1, 50, n_samples),
            'total_spent': np.random.uniform(50, 5000, n_samples),
            'avg_order_value': np.random.uniform(20, 500, n_samples),
            'days_since_last_order': np.random.randint(0, 365, n_samples),
            'order_frequency': np.random.uniform(0.1, 10, n_samples),
            'email_open_rate': np.random.uniform(0, 1, n_samples),
            'email_click_rate': np.random.uniform(0, 0.5, n_samples),
            'sms_engagement_rate': np.random.uniform(0, 1, n_samples),
            'app_sessions': np.random.randint(0, 100, n_samples)
        }
        return pd.DataFrame(data).values
    
    def _generate_synthetic_labels(self, X: np.ndarray) -> np.ndarray:
        """Generate synthetic churn labels based on features"""
        # Simple rule-based labeling for demonstration
        # High churn if: low orders, high days since last order, low engagement
        labels = []
        for row in X:
            score = 0
            if row[0] < 5:  # low total orders
                score += 1
            if row[3] > 180:  # high days since last order
                score += 1
            if row[5] < 0.3:  # low email open rate
                score += 1
            if row[7] < 0.3:  # low sms engagement
                score += 1
            
            labels.append(1 if score >= 2 else 0)
        
        return np.array(labels)
    
    def _save_models(self):
        """Save models to disk"""
        xgb_path = os.path.join(self.model_path, "xgboost_churn_model.pkl")
        nn_path = os.path.join(self.model_path, "nn_churn_model.h5")
        scaler_path = os.path.join(self.model_path, "scaler.pkl")
        
        joblib.dump(self.xgb_model, xgb_path)
        self.nn_model.save(nn_path)
        joblib.dump(self.scaler, scaler_path)
    
    def prepare_features(self, customer_data: Dict) -> np.ndarray:
        """Prepare features from customer data"""
        features = []
        for feature_name in self.feature_names:
            features.append(customer_data.get(feature_name, 0))
        
        return np.array(features).reshape(1, -1)
    
    def predict(self, customer_data: Dict) -> Tuple[float, float, float]:
        """
        Predict churn probability using ensemble of XGBoost and Neural Network
        
        Returns:
            Tuple of (xgboost_score, nn_score, ensemble_score)
        """
        features = self.prepare_features(customer_data)
        
        # XGBoost prediction
        xgb_proba = self.xgb_model.predict_proba(features)[0][1]
        
        # Neural Network prediction
        features_scaled = self.scaler.transform(features)
        nn_proba = self.nn_model.predict(features_scaled, verbose=0)[0][0]
        
        # Ensemble prediction (weighted average)
        ensemble_proba = 0.6 * xgb_proba + 0.4 * float(nn_proba)
        
        return float(xgb_proba), float(nn_proba), float(ensemble_proba)
    
    def get_risk_level(self, ensemble_score: float) -> str:
        """Determine risk level based on ensemble score"""
        if ensemble_score >= 0.75:
            return "high"
        elif ensemble_score >= 0.5:
            return "medium"
        else:
            return "low"
    
    def explain_prediction(self, customer_data: Dict) -> Dict:
        """
        Use SHAP to explain prediction
        
        Returns:
            Dictionary with SHAP values and top features
        """
        features = self.prepare_features(customer_data)
        
        # Create SHAP explainer for XGBoost (more stable than NN)
        explainer = shap.TreeExplainer(self.xgb_model)
        shap_values = explainer.shap_values(features)
        
        # Get feature importance
        feature_importance = []
        for i, feature_name in enumerate(self.feature_names):
            feature_importance.append({
                'feature': feature_name,
                'shap_value': float(shap_values[0][i]),
                'feature_value': float(features[0][i])
            })
        
        # Sort by absolute SHAP value
        feature_importance.sort(key=lambda x: abs(x['shap_value']), reverse=True)
        
        return {
            'shap_values': {f['feature']: f['shap_value'] for f in feature_importance},
            'top_features': feature_importance[:5]
        }
    
    def retrain(self, X: np.ndarray, y: np.ndarray):
        """Retrain models with new data"""
        # Refit scaler
        X_scaled = self.scaler.fit_transform(X)
        
        # Retrain XGBoost
        self.xgb_model.fit(X, y)
        
        # Retrain Neural Network
        self.nn_model.fit(X_scaled, y, epochs=10, verbose=0, validation_split=0.2)
        
        # Save updated models
        self._save_models()
