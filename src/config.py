"""
Configuration management for the Football Prediction System
"""

import os
import yaml
from pathlib import Path
from typing import Any, Dict
from loguru import logger

class Config:
    """Configuration manager for the application"""
    
    def __init__(self, config_file: str = "config.yaml"):
        """Initialize configuration"""
        self.config_path = Path(config_file)
        self.config_data: Dict[str, Any] = {}
        
        if self.config_path.exists():
            self._load_yaml()
        else:
            logger.warning(f"Configuration file {config_file} not found. Using defaults.")
            self._set_defaults()
    
    def _load_yaml(self):
        """Load configuration from YAML file"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                self.config_data = yaml.safe_load(f)
            logger.info(f"Configuration loaded from {self.config_path}")
        except Exception as e:
            logger.error(f"Error loading configuration: {e}")
            self._set_defaults()
    
    def _set_defaults(self):
        """Set default configuration values"""
        self.config_data = {
            'data_sources': {'statsbomb': {'enabled': True}},
            'ml': {'test_size': 0.2, 'random_state': 42}
        }
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value by key (supports dot notation)"""
        keys = key.split('.')
        value = self.config_data
        
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
            else:
                return default
        
        return value if value is not None else default
    
    def set(self, key: str, value: Any):
        """Set configuration value by key"""
        keys = key.split('.')
        config = self.config_data
        
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        config[keys[-1]] = value

# Create global config instance
config = Config()
