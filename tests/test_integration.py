"""
Integration tests for the complete pipeline
"""

import pytest
import pandas as pd
import numpy as np
import os
import tempfile
from src.preprocessing import DataCleaner
from src.preprocessing.feature_engineer import FeatureEngineer
from src.analysis.stats_analyzer import StatsAnalyzer
from src.prediction.ml_predictor import MLPredictor


def create_integration_data():
    """Create sample data for integration testing"""
    data = {
        'home_team': ['Arsenal', 'Chelsea', 'Liverpool', 'Man Utd', 'Man City'] * 5,
        'away_team': ['Chelsea', 'Liverpool', 'Man Utd', 'Man City', 'Arsenal'] * 5,
        'home_goals': np.random.randint(0, 5, 25),
        'away_goals': np.random.randint(0, 5, 25),
        'match_date': pd.date_range('2023-01-01', periods=25)
    }
    return pd.DataFrame(data)


def test_complete_pipeline():
    """Test complete analysis pipeline"""
    # Create sample data
    df = create_integration_data()
    
    # Clean data
    df_clean = DataCleaner.clean_pipeline(df)
    assert len(df_clean) > 0
    
    # Engineer features
    df_features = FeatureEngineer.feature_engineering_pipeline(df_clean)
    assert len(df_features.columns) > len(df_clean.columns)
    
    # Analyze
    analyzer = StatsAnalyzer()
    team_stats = analyzer.calculate_team_stats(df_clean)
    assert len(team_stats) > 0
    
    print("Integration test passed!")


def test_prediction_pipeline():
    """Test prediction pipeline"""
    # Create data
    df = create_integration_data()
    
    # Prepare features
    df = FeatureEngineer.feature_engineering_pipeline(df)
    df['result'] = np.where(
        df['home_goals'] > df['away_goals'], 1,
        np.where(df['home_goals'] == df['away_goals'], 0, -1)
    )
    
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    numeric_cols = [col for col in numeric_cols if col != 'result']
    
    X = df[numeric_cols].fillna(0).values
    y = df['result'].values
    
    # Train and predict
    predictor = MLPredictor(model_type='random_forest')
    metrics = predictor.train(X, y)
    
    assert metrics['test_score'] >= 0
    
    predictions, _ = predictor.predict(X[:5])
    assert len(predictions) == 5
    
    print("Prediction pipeline test passed!")


if __name__ == "__main__":
    test_complete_pipeline()
    test_prediction_pipeline()
    print("All integration tests passed!")
