# API endpoints for GitHub imports

from flask import request, jsonify
from src.importers.github_importer import GitHubImporter
from src.importers.data_analyzer import ImportedDataAnalyzer
from loguru import logger

importer = GitHubImporter()
analyzer = ImportedDataAnalyzer()


def setup_import_routes(app):
    """Setup import-related API routes"""
    
    @app.route('/api/import/repo-info', methods=['GET'])
    def get_repo_info():
        """Get information about a GitHub repository"""
        try:
            owner = request.args.get('owner')
            repo = request.args.get('repo')
            token = request.args.get('token')
            
            if not owner or not repo:
                return jsonify({'error': 'owner and repo parameters required'}), 400
            
            info = importer.get_repo_info(owner, repo, token)
            return jsonify(info)
        
        except Exception as e:
            logger.error(f"Error getting repo info: {e}")
            return jsonify({'error': str(e)}), 500
    
    @app.route('/api/import/clone', methods=['POST'])
    def clone_repo():
        """Clone a GitHub repository"""
        try:
            data = request.get_json()
            repo_url = data.get('repo_url')
            repo_name = data.get('repo_name')
            
            if not repo_url or not repo_name:
                return jsonify({'error': 'repo_url and repo_name required'}), 400
            
            result = importer.clone_repository(repo_url, repo_name)
            return jsonify(result)
        
        except Exception as e:
            logger.error(f"Error cloning repo: {e}")
            return jsonify({'error': str(e)}), 500
    
    @app.route('/api/import/list', methods=['GET'])
    def list_imports():
        """List all imported repositories"""
        try:
            result = importer.list_imports()
            return jsonify(result)
        
        except Exception as e:
            logger.error(f"Error listing imports: {e}")
            return jsonify({'error': str(e)}), 500
    
    @app.route('/api/import/<repo_name>/files', methods=['GET'])
    def list_files(repo_name):
        """List files in imported repository"""
        try:
            path = request.args.get('path', '')
            file_types = request.args.getlist('file_types')
            
            result = importer.list_files(repo_name, path, file_types if file_types else None)
            return jsonify(result)
        
        except Exception as e:
            logger.error(f"Error listing files: {e}")
            return jsonify({'error': str(e)}), 500
    
    @app.route('/api/import/<repo_name>/file', methods=['GET'])
    def read_file(repo_name):
        """Read file from imported repository"""
        try:
            file_path = request.args.get('path')
            
            if not file_path:
                return jsonify({'error': 'path parameter required'}), 400
            
            result = importer.read_file(repo_name, file_path)
            return jsonify(result)
        
        except Exception as e:
            logger.error(f"Error reading file: {e}")
            return jsonify({'error': str(e)}), 500
    
    @app.route('/api/import/<repo_name>/search', methods=['GET'])
    def search_files(repo_name):
        """Search for files in imported repository"""
        try:
            pattern = request.args.get('pattern')
            file_types = request.args.getlist('file_types')
            
            if not pattern:
                return jsonify({'error': 'pattern parameter required'}), 400
            
            result = importer.search_files(repo_name, pattern, file_types if file_types else None)
            return jsonify(result)
        
        except Exception as e:
            logger.error(f"Error searching files: {e}")
            return jsonify({'error': str(e)}), 500
    
    @app.route('/api/import/<repo_name>/stats', methods=['GET'])
    def get_stats(repo_name):
        """Get statistics about imported repository"""
        try:
            result = importer.get_repo_stats(repo_name)
            return jsonify(result)
        
        except Exception as e:
            logger.error(f"Error getting stats: {e}")
            return jsonify({'error': str(e)}), 500
    
    @app.route('/api/import/<repo_name>/delete', methods=['DELETE'])
    def delete_repo(repo_name):
        """Delete imported repository"""
        try:
            result = importer.delete_import(repo_name)
            return jsonify(result)
        
        except Exception as e:
            logger.error(f"Error deleting repo: {e}")
            return jsonify({'error': str(e)}), 500
    
    @app.route('/api/import/<repo_name>/data-files', methods=['GET'])
    def detect_data_files(repo_name):
        """Detect data files in repository"""
        try:
            result = analyzer.detect_data_files(repo_name)
            return jsonify(result)
        
        except Exception as e:
            logger.error(f"Error detecting data files: {e}")
            return jsonify({'error': str(e)}), 500
    
    @app.route('/api/import/<repo_name>/load-csv', methods=['GET'])
    def load_csv(repo_name):
        """Load CSV file from repository"""
        try:
            file_path = request.args.get('path')
            
            if not file_path:
                return jsonify({'error': 'path parameter required'}), 400
            
            result = analyzer.load_csv(repo_name, file_path)
            return jsonify(result)
        
        except Exception as e:
            logger.error(f"Error loading CSV: {e}")
            return jsonify({'error': str(e)}), 500
