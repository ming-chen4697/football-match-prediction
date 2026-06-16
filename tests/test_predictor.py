"""
Test ML predictor module
"""

import pytest
import numpy as np
import pandas as pd
from src.prediction.ml_predictor import MLPredictor


def create_sample_features():
    """Create sample features for testing"""
    np.random.seed(42)
    X = np.random.randn(100, 10)
    y = np.random.randint(0, 3, 100)
    return X, y


def test_ml_predictor_init():
    """Test predictor initialization"""
    predictor = MLPredictor(model_type='xgboost')
    assert predictor is not None
    assert predictor.model_type == 'xgboost'


def test_model_training():
    """Test model training"""
    X, y = create_sample_features()
    predictor = MLPredictor(model_type='random_forest')
    
    metrics = predictor.train(X, y, test_size=0.2)
    
    assert isinstance(metrics, dict)
    assert 'train_score' in metrics
    assert 'test_score' in metrics
    assert metrics['test_score'] >= 0
    assert metrics['test_score'] <= 1


def test_model_prediction():
    """Test model prediction"""
    X, y = create_sample_features()
    predictor = MLPredictor(model_type='logistic')
    
    predictor.train(X, y)
    predictions, probabilities = predictor.predict(X[:5])
    
    assert predictions.shape[0] == 5
    assert probabilities.shape[0] == 5
    assert probabilities.shape[1] >= 2  # At least binary classification


def test_model_save_load(tmp_path):
    """Test model saving and loading"""
    X, y = create_sample_features()
    predictor = MLPredictor(model_type='xgboost')
    
    predictor.train(X, y)
    
    # Save model
    filepath = str(tmp_path / "test_model.pkl")
    predictor.save_model(filepath)
    
    # Load model
    predictor2 = MLPredictor(model_type='xgboost')
    predictor2.load_model(filepath)
    
    # Both should make same predictions
    pred1, _ = predictor.predict(X[:5])
    pred2, _ = predictor2.predict(X[:5])
    
    np.testing.assert_array_equal(pred1, pred2)
