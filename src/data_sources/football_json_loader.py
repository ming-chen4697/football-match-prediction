"""
football.json data loader - Load data from football.json
References: https://github.com/openfootball/football.json
"""

import requests
import pandas as pd
from typing import Optional, List
from loguru import logger
from src.data_sources import BaseLoader


class FootballJsonLoader(BaseLoader):
    """Load data from football.json open data repository"""
    
    BASE_URL = "https://raw.githubusercontent.com/openfootball/football.json/master"
    
    def __init__(self, cache_enabled: bool = True):
        """Initialize football.json loader"""
        super().__init__("football.json", cache_enabled)
    
    def _fetch_json(self, url: str) -> Optional[dict]:
        """Fetch JSON data from URL"""
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching data from {url}: {e}")
            return None
    
    def fetch_matches(self, league: str, season: int) -> pd.DataFrame:
        """Fetch matches for a specific league and season"""
        cache_key = f"matches_{league}_{season}"
        cached_data = self._get_cached_data(cache_key)
        if cached_data is not None:
            return cached_data
        
        try:
            url = f"{self.BASE_URL}/2023-24/{league}.1.json"
            data = self._fetch_json(url)
            
            if data and 'matches' in data:
                df = pd.DataFrame(data['matches'])
                self._cache_data(cache_key, df)
                logger.info(f"Loaded {len(df)} matches for {league}")
                return df
        except Exception as e:
            logger.error(f"Error fetching matches: {e}")
        
        return pd.DataFrame()
    
    def fetch_teams(self, league: str, season: int) -> pd.DataFrame:
        """Fetch teams for a league and season"""
        cache_key = f"teams_{league}_{season}"
        cached_data = self._get_cached_data(cache_key)
        if cached_data is not None:
            return cached_data
        
        try:
            url = f"{self.BASE_URL}/2023-24/{league}.1.json"
            data = self._fetch_json(url)
            
            if data and 'teams' in data:
                df = pd.DataFrame(data['teams'])
                self._cache_data(cache_key, df)
                logger.info(f"Loaded {len(df)} teams for {league}")
                return df
        except Exception as e:
            logger.error(f"Error fetching teams: {e}")
        
        return pd.DataFrame()
    
    def fetch_players(self, team_id: str) -> pd.DataFrame:
        """Fetch players for a team"""
        logger.info(f"Fetching players for team {team_id}")
        return pd.DataFrame()
