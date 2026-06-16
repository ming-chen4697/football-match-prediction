"""
Data Analyzer for Imported Data
Analyze and process data from imported GitHub repositories
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import List, Dict, Optional
from loguru import logger
import json
import csv


class ImportedDataAnalyzer:
    """Analyze data from imported repositories"""
    
    def __init__(self, import_dir: str = 'data/imports'):
        """Initialize analyzer"""
        self.import_dir = Path(import_dir)
        logger.info(f"Data Analyzer initialized")
    
    def detect_data_files(self, repo_name: str) -> Dict:
        """
        Detect potential data files in repository
        
        Args:
            repo_name: Repository name
        
        Returns:
            Dictionary with detected data files
        """
        try:
            repo_path = self.import_dir / repo_name
            data_files = {
                'csv': [],
                'json': [],
                'xlsx': [],
                'parquet': [],
                'other': []
            }
            
            for root, dirs, files in os.walk(repo_path):
                for file in files:
                    file_path = Path(root) / file
                    suffix = file_path.suffix.lower()
                    
                    if suffix == '.csv':
                        data_files['csv'].append(str(file_path.relative_to(repo_path)))
                    elif suffix == '.json':
                        data_files['json'].append(str(file_path.relative_to(repo_path)))
                    elif suffix in ['.xlsx', '.xls']:
                        data_files['xlsx'].append(str(file_path.relative_to(repo_path)))
                    elif suffix == '.parquet':
                        data_files['parquet'].append(str(file_path.relative_to(repo_path)))
                    elif suffix in ['.txt', '.dat']:
                        data_files['other'].append(str(file_path.relative_to(repo_path)))
            
            return {
                'success': True,
                'repo': repo_name,
                'data_files': data_files
            }
        
        except Exception as e:
            logger.error(f"Error detecting data files: {e}")
            return {'success': False, 'error': str(e)}
    
    def load_csv(self, repo_name: str, file_path: str) -> Dict:
        """
        Load and analyze CSV file
        
        Args:
            repo_name: Repository name
            file_path: CSV file path
        
        Returns:
            Dictionary with CSV data and analysis
        """
        try:
            full_path = self.import_dir / repo_name / file_path
            
            if not full_path.exists() or full_path.suffix.lower() != '.csv':
                return {'success': False, 'error': 'CSV file not found'}
            
            df = pd.read_csv(full_path)
            
            return {
                'success': True,
                'repo': repo_name,
                'file': file_path,
                'shape': list(df.shape),
                'columns': list(df.columns),
                'dtypes': df.dtypes.to_dict(),
                'preview': df.head(10).to_dict('records'),
                'missing_values': df.isnull().sum().to_dict(),
                'statistics': df.describe().to_dict()
            }
        
        except Exception as e:
            logger.error(f"Error loading CSV: {e}")
            return {'success': False, 'error': str(e)}
    
    def load_json(self, repo_name: str, file_path: str) -> Dict:
        """
        Load and analyze JSON file
        
        Args:
            repo_name: Repository name
            file_path: JSON file path
        
        Returns:
            Dictionary with JSON data
        """
        try:
            full_path = self.import_dir / repo_name / file_path
            
            if not full_path.exists() or full_path.suffix.lower() != '.json':
                return {'success': False, 'error': 'JSON file not found'}
            
            with open(full_path, 'r') as f:
                data = json.load(f)
            
            return {
                'success': True,
                'repo': repo_name,
                'file': file_path,
                'data': data,
                'type': type(data).__name__,
                'size': len(data) if isinstance(data, (list, dict)) else 0
            }
        
        except Exception as e:
            logger.error(f"Error loading JSON: {e}")
            return {'success': False, 'error': str(e)}


import os
