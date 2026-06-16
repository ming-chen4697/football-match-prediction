"""
Test analyzer module
"""

import pytest
import pandas as pd
import numpy as np
from src.analysis.stats_analyzer import StatsAnalyzer


def create_sample_data():
    """Create sample match data for testing"""
    data = {
        'home_team': ['Team A', 'Team B', 'Team A', 'Team B'],
        'away_team': ['Team B', 'Team A', 'Team C', 'Team C'],
        'home_goals': [2, 1, 3, 0],
        'away_goals': [1, 1, 1, 2],
        'match_date': ['2023-01-01', '2023-01-02', '2023-01-03', '2023-01-04']
    }
    return pd.DataFrame(data)


def test_calculate_team_stats():
    """Test team statistics calculation"""
    df = create_sample_data()
    analyzer = StatsAnalyzer()
    
    team_stats = analyzer.calculate_team_stats(df)
    
    assert isinstance(team_stats, pd.DataFrame)
    assert 'team' in team_stats.columns
    assert 'points' in team_stats.columns
    assert len(team_stats) > 0


def test_head_to_head_analysis():
    """Test H2H analysis"""
    df = create_sample_data()
    analyzer = StatsAnalyzer()
    
    h2h = analyzer.head_to_head_analysis(df, 'Team A', 'Team B')
    
    assert isinstance(h2h, dict)
    assert 'total_matches' in h2h
    assert h2h['total_matches'] >= 0


def test_form_analysis():
    """Test form analysis"""
    df = create_sample_data()
    analyzer = StatsAnalyzer()
    
    form = analyzer.form_analysis(df, 'Team A', last_n_matches=5)
    
    assert isinstance(form, dict)
    assert 'matches' in form
    assert 'wins' in form
