"""
Machine learning prediction models for football match outcomes
References: Football_Prediction_Project
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from typing import Tuple, Dict, List
from loguru import logger
import pickle
import os


class MLPredictor:
    """Machine learning-based match outcome predictor"""
    
    def __init__(self, model_type: str = 'xgboost'):
        """Initialize predictor"""
        self.model_type = model_type
        self.model = None
        self.scaler = StandardScaler()
        self.feature_names = None
        self.label_encoder = {}
        logger.info(f"Initialized ML Predictor with model type: {model_type}")
    
    def _create_model(self):
        """Create model based on specified type"""
        if self.model_type == 'logistic':
            self.model = LogisticRegression(max_iter=1000, random_state=42)
        elif self.model_type == 'random_forest':
            self.model = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42)
        elif self.model_type == 'xgboost':
            self.model = XGBClassifier(n_estimators=100, max_depth=6, learning_rate=0.1, random_state=42)
        else:
            raise ValueError(f"Unknown model type: {self.model_type}")
    
    def prepare_features(self, df: pd.DataFrame, 
                        feature_cols: List[str] = None) -> Tuple[np.ndarray, List[str]]:
        """Prepare features for modeling"""
        if feature_cols is None:
            feature_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        
        feature_cols = [col for col in feature_cols if col not in ['result', 'outcome', 'target']]
        self.feature_names = feature_cols
        
        X = df[feature_cols].values
        X = self.scaler.fit_transform(X)
        
        logger.info(f"Prepared {len(feature_cols)} features for modeling")
        return X, feature_cols
    
    def train(self, X: np.ndarray, 
             y: np.ndarray,
             test_size: float = 0.2) -> Dict:
        """Train the model"""
        logger.info(f"Starting model training with {self.model_type}")
        
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=42
        )
        
        self._create_model()
        self.model.fit(X_train, y_train)
        
        train_score = self.model.score(X_train, y_train)
        test_score = self.model.score(X_test, y_test)
        
        logger.info(f"Model trained. Test score: {test_score:.4f}")
        
        return {
            'train_score': train_score,
            'test_score': test_score,
            'train_samples': len(X_train),
            'test_samples': len(X_test),
        }
    
    def predict(self, X: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """Make predictions"""
        if self.model is None:
            raise ValueError("Model not trained. Call train() first.")
        
        predictions = self.model.predict(X)
        probabilities = self.model.predict_proba(X)
        
        return predictions, probabilities
    
    def save_model(self, filepath: str):
        """Save model to file"""
        model_data = {
            'model': self.model,
            'scaler': self.scaler,
            'feature_names': self.feature_names,
        }
        
        os.makedirs(os.path.dirname(filepath) or '.', exist_ok=True)
        
        with open(filepath, 'wb') as f:
            pickle.dump(model_data, f)
        
        logger.info(f"Model saved to {filepath}")
    
    def load_model(self, filepath: str):
        """Load model from file"""
        with open(filepath, 'rb') as f:
            model_data = pickle.load(f)
        
        self.model = model_data['model']
        self.scaler = model_data['scaler']
        self.feature_names = model_data['feature_names']
        
        logger.info(f"Model loaded from {filepath}")
