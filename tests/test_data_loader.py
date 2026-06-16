"""
Test data loader module
"""

import pytest
import pandas as pd
from src.data_sources.football_json_loader import FootballJsonLoader


def test_football_json_loader_init():
    """Test loader initialization"""
    loader = FootballJsonLoader()
    assert loader is not None
    assert loader.name == "football.json"


def test_fetch_matches():
    """Test fetching matches"""
    loader = FootballJsonLoader()
    matches = loader.fetch_matches('en', 2023)
    
    # Should return DataFrame (may be empty if API is down)
    assert isinstance(matches, pd.DataFrame)


def test_cache_functionality():
    """Test caching mechanism"""
    loader = FootballJsonLoader(cache_enabled=True)
    
    # Cache should be empty initially
    assert len(loader.cache) == 0
    
    # Test clearing cache
    loader.clear_cache()
    assert len(loader.cache) == 0
