"""
GitHub Repository Importer Module
Allows importing and analyzing football data from external GitHub repositories
"""

import os
import json
import requests
import shutil
from pathlib import Path
from typing import Dict, List, Optional
from loguru import logger
from datetime import datetime
import subprocess


class GitHubImporter:
    """Handle GitHub repository imports"""
    
    def __init__(self, import_dir: str = 'data/imports'):
        """Initialize importer"""
        self.import_dir = Path(import_dir)
        self.import_dir.mkdir(parents=True, exist_ok=True)
        self.github_api = 'https://api.github.com'
        logger.info(f"GitHub Importer initialized with directory: {import_dir}")
    
    def validate_repo_url(self, repo_url: str) -> bool:
        """
        Validate GitHub repository URL
        
        Args:
            repo_url: GitHub URL (e.g., https://github.com/user/repo)
        
        Returns:
            True if valid, False otherwise
        """
        valid_patterns = [
            'https://github.com/',
            'http://github.com/',
            'git@github.com:'
        ]
        
        return any(repo_url.startswith(pattern) for pattern in valid_patterns)
    
    def get_repo_info(self, owner: str, repo: str, token: Optional[str] = None) -> Dict:
        """
        Get repository information from GitHub API
        
        Args:
            owner: Repository owner
            repo: Repository name
            token: GitHub API token (optional)
        
        Returns:
            Dictionary with repository info
        """
        try:
            headers = {}
            if token:
                headers['Authorization'] = f'token {token}'
            
            url = f'{self.github_api}/repos/{owner}/{repo}'
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            repo_data = response.json()
            
            return {
                'name': repo_data.get('name'),
                'full_name': repo_data.get('full_name'),
                'description': repo_data.get('description'),
                'url': repo_data.get('html_url'),
                'clone_url': repo_data.get('clone_url'),
                'ssh_url': repo_data.get('ssh_url'),
                'stars': repo_data.get('stargazers_count'),
                'forks': repo_data.get('forks_count'),
                'language': repo_data.get('language'),
                'created_at': repo_data.get('created_at'),
                'updated_at': repo_data.get('pushed_at'),
                'topics': repo_data.get('topics', []),
                'is_fork': repo_data.get('fork'),
                'size': repo_data.get('size'),
                'success': True
            }
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching repo info: {e}")
            return {'success': False, 'error': str(e)}
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return {'success': False, 'error': str(e)}
    
    def clone_repository(self, repo_url: str, repo_name: str) -> Dict:
        """
        Clone a GitHub repository
        
        Args:
            repo_url: Full GitHub URL
            repo_name: Local repository name
        
        Returns:
            Status dictionary
        """
        try:
            if not self.validate_repo_url(repo_url):
                return {'success': False, 'error': 'Invalid GitHub URL'}
            
            clone_path = self.import_dir / repo_name
            
            if clone_path.exists():
                logger.warning(f"Repository already exists: {clone_path}")
                return {'success': False, 'error': 'Repository already imported'}
            
            logger.info(f"Cloning repository: {repo_url}")
            
            result = subprocess.run(
                ['git', 'clone', repo_url, str(clone_path)],
                capture_output=True,
                text=True,
                timeout=300
            )
            
            if result.returncode != 0:
                logger.error(f"Git clone failed: {result.stderr}")
                return {'success': False, 'error': result.stderr}
            
            logger.info(f"Repository cloned successfully: {clone_path}")
            
            return {
                'success': True,
                'message': 'Repository cloned successfully',
                'path': str(clone_path),
                'size': self._get_dir_size(clone_path)
            }
        
        except subprocess.TimeoutExpired:
            logger.error("Clone operation timed out")
            return {'success': False, 'error': 'Clone operation timed out'}
        except Exception as e:
            logger.error(f"Error cloning repository: {e}")
            return {'success': False, 'error': str(e)}
    
    def list_files(self, repo_name: str, path: str = '', file_types: List[str] = None) -> Dict:
        """
        List files in imported repository
        
        Args:
            repo_name: Local repository name
            path: Subdirectory path
            file_types: Filter by file types (e.g., ['.csv', '.json'])
        
        Returns:
            Dictionary with file list
        """
        try:
            repo_path = self.import_dir / repo_name / path
            
            if not repo_path.exists():
                return {'success': False, 'error': 'Repository not found'}
            
            files = []
            directories = []
            
            for item in repo_path.iterdir():
                if item.name.startswith('.'):
                    continue
                
                if item.is_dir():
                    directories.append({
                        'name': item.name,
                        'type': 'directory',
                        'path': str(item.relative_to(self.import_dir / repo_name))
                    })
                else:
                    if file_types is None or any(item.suffix == ft for ft in file_types):
                        files.append({
                            'name': item.name,
                            'type': 'file',
                            'size': item.stat().st_size,
                            'path': str(item.relative_to(self.import_dir / repo_name)),
                            'suffix': item.suffix
                        })
            
            return {
                'success': True,
                'repo': repo_name,
                'path': path,
                'files': files,
                'directories': directories,
                'total_items': len(files) + len(directories)
            }
        
        except Exception as e:
            logger.error(f"Error listing files: {e}")
            return {'success': False, 'error': str(e)}
    
    def read_file(self, repo_name: str, file_path: str) -> Dict:
        """
        Read file content from imported repository
        
        Args:
            repo_name: Local repository name
            file_path: File path relative to repository
        
        Returns:
            Dictionary with file content
        """
        try:
            full_path = self.import_dir / repo_name / file_path
            
            if not full_path.exists():
                return {'success': False, 'error': 'File not found'}
            
            if not full_path.is_file():
                return {'success': False, 'error': 'Not a file'}
            
            # Check file size (limit to 5MB)
            if full_path.stat().st_size > 5 * 1024 * 1024:
                return {'success': False, 'error': 'File too large (max 5MB)'}
            
            with open(full_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            return {
                'success': True,
                'repo': repo_name,
                'file': file_path,
                'size': full_path.stat().st_size,
                'content': content
            }
        
        except UnicodeDecodeError:
            return {'success': False, 'error': 'File is not text'}
        except Exception as e:
            logger.error(f"Error reading file: {e}")
            return {'success': False, 'error': str(e)}
    
    def search_files(self, repo_name: str, pattern: str, file_types: List[str] = None) -> Dict:
        """
        Search for files matching pattern
        
        Args:
            repo_name: Local repository name
            pattern: Search pattern (case-insensitive)
            file_types: Filter by file types
        
        Returns:
            Dictionary with matching files
        """
        try:
            repo_path = self.import_dir / repo_name
            
            if not repo_path.exists():
                return {'success': False, 'error': 'Repository not found'}
            
            matches = []
            pattern_lower = pattern.lower()
            
            for root, dirs, files in os.walk(repo_path):
                # Skip hidden directories
                dirs[:] = [d for d in dirs if not d.startswith('.')]
                
                for file in files:
                    if pattern_lower in file.lower():
                        file_types_match = file_types is None or any(file.endswith(ft) for ft in file_types)
                        
                        if file_types_match:
                            full_path = Path(root) / file
                            matches.append({
                                'name': file,
                                'path': str(full_path.relative_to(repo_path)),
                                'size': full_path.stat().st_size
                            })
            
            return {
                'success': True,
                'repo': repo_name,
                'pattern': pattern,
                'matches': matches,
                'count': len(matches)
            }
        
        except Exception as e:
            logger.error(f"Error searching files: {e}")
            return {'success': False, 'error': str(e)}
    
    def list_imports(self) -> Dict:
        """
        List all imported repositories
        
        Returns:
            Dictionary with import list
        """
        try:
            imports = []
            
            for repo_dir in self.import_dir.iterdir():
                if repo_dir.is_dir() and not repo_dir.name.startswith('.'):
                    git_config = repo_dir / '.git' / 'config'
                    origin_url = None
                    
                    if git_config.exists():
                        with open(git_config, 'r') as f:
                            content = f.read()
                            for line in content.split('\n'):
                                if 'url' in line:
                                    origin_url = line.split('=')[1].strip() if '=' in line else None
                    
                    imports.append({
                        'name': repo_dir.name,
                        'path': str(repo_dir.relative_to(self.import_dir)),
                        'origin': origin_url,
                        'created': datetime.fromtimestamp(repo_dir.stat().st_ctime).isoformat(),
                        'size': self._get_dir_size(repo_dir)
                    })
            
            return {
                'success': True,
                'imports': imports,
                'count': len(imports)
            }
        
        except Exception as e:
            logger.error(f"Error listing imports: {e}")
            return {'success': False, 'error': str(e)}
    
    def delete_import(self, repo_name: str) -> Dict:
        """
        Delete an imported repository
        
        Args:
            repo_name: Local repository name
        
        Returns:
            Status dictionary
        """
        try:
            repo_path = self.import_dir / repo_name
            
            if not repo_path.exists():
                return {'success': False, 'error': 'Repository not found'}
            
            shutil.rmtree(repo_path)
            logger.info(f"Repository deleted: {repo_name}")
            
            return {'success': True, 'message': 'Repository deleted successfully'}
        
        except Exception as e:
            logger.error(f"Error deleting repository: {e}")
            return {'success': False, 'error': str(e)}
    
    def get_repo_stats(self, repo_name: str) -> Dict:
        """
        Get statistics about imported repository
        
        Args:
            repo_name: Local repository name
        
        Returns:
            Dictionary with statistics
        """
        try:
            repo_path = self.import_dir / repo_name
            
            if not repo_path.exists():
                return {'success': False, 'error': 'Repository not found'}
            
            file_count = 0
            dir_count = 0
            file_types = {}
            total_size = 0
            
            for root, dirs, files in os.walk(repo_path):
                # Skip hidden directories
                dirs[:] = [d for d in dirs if not d.startswith('.')]
                
                dir_count += len(dirs)
                
                for file in files:
                    if not file.startswith('.'):
                        file_count += 1
                        file_path = Path(root) / file
                        file_size = file_path.stat().st_size
                        total_size += file_size
                        
                        suffix = file_path.suffix or 'no_extension'
                        file_types[suffix] = file_types.get(suffix, 0) + 1
            
            return {
                'success': True,
                'repo': repo_name,
                'file_count': file_count,
                'dir_count': dir_count,
                'total_size': total_size,
                'file_types': file_types
            }
        
        except Exception as e:
            logger.error(f"Error getting repository stats: {e}")
            return {'success': False, 'error': str(e)}
    
    @staticmethod
    def _get_dir_size(path: Path) -> int:
        """Calculate total directory size in bytes"""
        total = 0
        for entry in path.rglob('*'):
            if entry.is_file():
                total += entry.stat().st_size
        return total
