"""
Base data loader class for all data sources
"""

from abc import ABC, abstractmethod
import pandas as pd
from typing import Dict, List, Optional
from loguru import logger


class BaseLoader(ABC):
    """Abstract base class for data loaders"""
    
    def __init__(self, name: str, cache_enabled: bool = True):
        """Initialize base loader"""
        self.name = name
        self.cache_enabled = cache_enabled
        self.cache: Dict = {}
        logger.info(f"Initializing {name} loader")
    
    @abstractmethod
    def fetch_matches(self, league: str, season: int) -> pd.DataFrame:
        """Fetch match data"""
        pass
    
    @abstractmethod
    def fetch_teams(self, league: str, season: int) -> pd.DataFrame:
        """Fetch team data"""
        pass
    
    @abstractmethod
    def fetch_players(self, team_id: str) -> pd.DataFrame:
        """Fetch player data for a team"""
        pass
    
    def _cache_data(self, key: str, data: pd.DataFrame):
        """Cache data"""
        if self.cache_enabled:
            self.cache[key] = data
    
    def _get_cached_data(self, key: str) -> Optional[pd.DataFrame]:
        """Retrieve cached data"""
        if self.cache_enabled and key in self.cache:
            return self.cache[key]
        return None
    
    def clear_cache(self):
        """Clear all cached data"""
        self.cache.clear()
        logger.info(f"Cache cleared for {self.name}")
