"""
StatsBomb data loader - Load data from StatsBomb open data
References: https://github.com/statsbomb/open-data
"""

import requests
import pandas as pd
from typing import Optional
from loguru import logger
from src.data_sources import BaseLoader


class StatsBombLoader(BaseLoader):
    """Load data from StatsBomb open data repository"""
    
    BASE_URL = "https://raw.githubusercontent.com/statsbomb/open-data/master/data"
    
    def __init__(self, cache_enabled: bool = True):
        """Initialize StatsBomb loader"""
        super().__init__("StatsBomb", cache_enabled)
    
    def _fetch_json(self, url: str) -> Optional[dict]:
        """Fetch JSON data from URL"""
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching data from {url}: {e}")
            return None
    
    def get_competitions(self) -> pd.DataFrame:
        """Get available competitions"""
        cache_key = "competitions"
        cached_data = self._get_cached_data(cache_key)
        if cached_data is not None:
            return cached_data
        
        url = f"{self.BASE_URL}/competitions.json"
        data = self._fetch_json(url)
        
        if data:
            df = pd.DataFrame(data)
            self._cache_data(cache_key, df)
            logger.info(f"Loaded {len(df)} competitions from StatsBomb")
            return df
        
        return pd.DataFrame()
    
    def fetch_matches(self, league: str, season: int) -> pd.DataFrame:
        """Fetch matches for a specific league and season"""
        cache_key = f"matches_{league}_{season}"
        cached_data = self._get_cached_data(cache_key)
        if cached_data is not None:
            return cached_data
        
        logger.info(f"Fetching matches for {league} season {season}")
        return pd.DataFrame()
    
    def fetch_teams(self, league: str, season: int) -> pd.DataFrame:
        """Fetch teams for a league and season"""
        logger.info(f"Fetching teams for {league} season {season}")
        return pd.DataFrame()
    
    def fetch_players(self, team_id: str) -> pd.DataFrame:
        """Fetch players for a team"""
        logger.info(f"Fetching players for team {team_id}")
        return pd.DataFrame()
