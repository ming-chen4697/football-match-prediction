"""
Data preprocessing module
"""

import pandas as pd
import numpy as np
from typing import List
from loguru import logger


class DataCleaner:
    """Handle data cleaning and preprocessing"""
    
    @staticmethod
    def remove_duplicates(df: pd.DataFrame, subset: List[str] = None) -> pd.DataFrame:
        """Remove duplicate rows"""
        initial_len = len(df)
        df = df.drop_duplicates(subset=subset)
        removed = initial_len - len(df)
        
        if removed > 0:
            logger.info(f"Removed {removed} duplicate rows")
        
        return df
    
    @staticmethod
    def handle_missing_values(df: pd.DataFrame, strategy: str = 'drop') -> pd.DataFrame:
        """Handle missing values"""
        initial_missing = df.isnull().sum().sum()
        
        if strategy == 'drop':
            df = df.dropna()
        elif strategy == 'mean':
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
        elif strategy == 'median':
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].median())
        
        final_missing = df.isnull().sum().sum()
        if initial_missing > 0:
            logger.info(f"Handled {initial_missing} missing values (strategy: {strategy})")
        
        return df
    
    @staticmethod
    def clean_pipeline(df: pd.DataFrame) -> pd.DataFrame:
        """Run complete cleaning pipeline"""
        logger.info("Starting data cleaning pipeline")
        logger.info(f"Initial shape: {df.shape}")
        
        df = DataCleaner.remove_duplicates(df)
        df = DataCleaner.handle_missing_values(df, strategy='drop')
        
        logger.info(f"Final shape: {df.shape}")
        return df
