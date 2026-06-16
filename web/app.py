"""
Flask Web Application for Football Prediction
"""

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import pandas as pd
import numpy as np
from loguru import logger
import json
from datetime import datetime

from src.data_sources.football_json_loader import FootballJsonLoader
from src.analysis.stats_analyzer import StatsAnalyzer
from src.prediction.ml_predictor import MLPredictor
from src.visualization.charts import FootballVisualizer
from src.preprocessing import DataCleaner
from src.preprocessing.feature_engineer import FeatureEngineer

app = Flask(__name__, template_folder='web/templates', static_folder='web/static')
CORS(app)

# Global variables for caching
matches_df = None
team_stats = None
analyzer = StatsAnalyzer()
visualizer = FootballVisualizer()


def load_data():
    """Load football data from CSV"""
    global matches_df, team_stats
    
    try:
        matches_df = pd.read_csv('data/processed/matches.csv')
        team_stats = analyzer.calculate_team_stats(matches_df)
        logger.info(f"Loaded {len(matches_df)} matches and {len(team_stats)} teams")
    except FileNotFoundError:
        logger.warning("No processed data found. Creating sample data...")
        # Create sample data if file doesn't exist
        matches_df = pd.DataFrame()
        team_stats = pd.DataFrame()


@app.route('/')
def index():
    """Home page"""
    return render_template('index.html')


@app.route('/api/dashboard')
def dashboard_data():
    """Get dashboard data"""
    if matches_df is None or matches_df.empty:
        return jsonify({
            'total_matches': 0,
            'total_teams': 0,
            'avg_goals': 0,
            'error': 'No data available'
        })
    
    try:
        total_matches = len(matches_df)
        total_teams = len(team_stats)
        avg_goals = 0
        
        if 'home_goals' in matches_df.columns and 'away_goals' in matches_df.columns:
            avg_goals = (matches_df['home_goals'].mean() + matches_df['away_goals'].mean()) / 2
        
        return jsonify({
            'total_matches': int(total_matches),
            'total_teams': int(total_teams),
            'avg_goals': round(float(avg_goals), 2)
        })
    except Exception as e:
        logger.error(f"Error getting dashboard data: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/teams')
def get_teams():
    """Get team list and statistics"""
    if team_stats is None or team_stats.empty:
        return jsonify({'teams': []})
    
    try:
        # Get top teams
        top_teams = team_stats.nlargest(20, 'points')
        
        teams_data = []
        for _, row in top_teams.iterrows():
            teams_data.append({
                'team': str(row['team']),
                'matches': int(row['matches']),
                'wins': int(row['wins']),
                'draws': int(row['draws']),
                'losses': int(row['losses']),
                'goals_for': int(row['goals_for']),
                'goals_against': int(row['goals_against']),
                'points': int(row['points']),
                'goal_difference': int(row['goal_difference']),
                'avg_goals_for': round(float(row['avg_goals_for']), 2) if 'avg_goals_for' in row else 0,
                'avg_goals_against': round(float(row['avg_goals_against']), 2) if 'avg_goals_against' in row else 0,
            })
        
        return jsonify({
            'teams': teams_data,
            'total': len(team_stats)
        })
    except Exception as e:
        logger.error(f"Error getting teams: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/team/<team_name>')
def get_team_detail(team_name):
    """Get detailed information for a specific team"""
    if team_stats is None or team_stats.empty:
        return jsonify({'error': 'No data'}), 404
    
    try:
        team_data = team_stats[team_stats['team'] == team_name]
        
        if team_data.empty:
            return jsonify({'error': 'Team not found'}), 404
        
        row = team_data.iloc[0]
        
        # Get form analysis
        form = analyzer.form_analysis(matches_df, team_name, last_n_matches=10)
        
        return jsonify({
            'team': str(row['team']),
            'matches': int(row['matches']),
            'wins': int(row['wins']),
            'draws': int(row['draws']),
            'losses': int(row['losses']),
            'goals_for': int(row['goals_for']),
            'goals_against': int(row['goals_against']),
            'points': int(row['points']),
            'goal_difference': int(row['goal_difference']),
            'avg_goals_for': round(float(row['avg_goals_for']), 2) if 'avg_goals_for' in row else 0,
            'form': form
        })
    except Exception as e:
        logger.error(f"Error getting team detail: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/h2h', methods=['POST'])
def head_to_head():
    """Get head-to-head analysis between two teams"""
    if matches_df is None or matches_df.empty:
        return jsonify({'error': 'No data'}), 400
    
    try:
        data = request.get_json()
        team1 = data.get('team1')
        team2 = data.get('team2')
        
        if not team1 or not team2:
            return jsonify({'error': 'Both teams required'}), 400
        
        h2h = analyzer.head_to_head_analysis(matches_df, team1, team2)
        
        return jsonify({
            'team1': team1,
            'team2': team2,
            'total_matches': h2h['total_matches'],
            'team1_wins': h2h['team1_wins'],
            'team2_wins': h2h['team2_wins'],
            'draws': h2h['draws']
        })
    except Exception as e:
        logger.error(f"Error in H2H analysis: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/predict', methods=['POST'])
def predict_match():
    """Predict match outcome"""
    try:
        data = request.get_json()
        team1 = data.get('team1')
        team2 = data.get('team2')
        
        if not team1 or not team2:
            return jsonify({'error': 'Both teams required'}), 400
        
        # Get team stats for prediction
        team1_stats = team_stats[team_stats['team'] == team1]
        team2_stats = team_stats[team_stats['team'] == team2]
        
        if team1_stats.empty or team2_stats.empty:
            return jsonify({'error': 'Team not found'}), 404
        
        # Simple prediction based on strength
        team1_strength = team1_stats.iloc[0]['avg_goals_for']
        team2_strength = team2_stats.iloc[0]['avg_goals_for']
        
        # Use Poisson-based probabilities (simplified)
        from scipy.stats import poisson
        
        home_advantage = 0.3
        team1_expected = team1_strength + home_advantage
        team2_expected = team2_strength
        
        team1_win_prob = 0
        draw_prob = 0
        team2_win_prob = 0
        
        for g1 in range(10):
            for g2 in range(10):
                prob = poisson.pmf(g1, team1_expected) * poisson.pmf(g2, team2_expected)
                if g1 > g2:
                    team1_win_prob += prob
                elif g1 == g2:
                    draw_prob += prob
                else:
                    team2_win_prob += prob
        
        return jsonify({
            'team1': team1,
            'team2': team2,
            'team1_win_prob': round(float(team1_win_prob), 3),
            'draw_prob': round(float(draw_prob), 3),
            'team2_win_prob': round(float(team2_win_prob), 3),
            'expected_goals': {
                'team1': round(float(team1_expected), 2),
                'team2': round(float(team2_expected), 2)
            }
        })
    except Exception as e:
        logger.error(f"Error in prediction: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/matches')
def get_matches():
    """Get recent matches"""
    if matches_df is None or matches_df.empty:
        return jsonify({'matches': []})
    
    try:
        # Get last 20 matches
        recent_matches = matches_df.tail(20).copy()
        
        matches_data = []
        for _, row in recent_matches.iterrows():
            match = {
                'home_team': str(row['home_team']) if 'home_team' in row else 'Unknown',
                'away_team': str(row['away_team']) if 'away_team' in row else 'Unknown',
            }
            
            if 'home_goals' in row and 'away_goals' in row:
                match['home_goals'] = int(row['home_goals'])
                match['away_goals'] = int(row['away_goals'])
                match['result'] = 'Home Win' if row['home_goals'] > row['away_goals'] else \
                                 'Away Win' if row['away_goals'] > row['home_goals'] else 'Draw'
            
            if 'match_date' in row:
                match['date'] = str(row['match_date'])
            
            matches_data.append(match)
        
        return jsonify({
            'matches': matches_data
        })
    except Exception as e:
        logger.error(f"Error getting matches: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/statistics')
def get_statistics():
    """Get overall statistics"""
    if matches_df is None or matches_df.empty:
        return jsonify({'error': 'No data'}), 400
    
    try:
        home_wins = len(matches_df[matches_df['home_goals'] > matches_df['away_goals']])
        draws = len(matches_df[matches_df['home_goals'] == matches_df['away_goals']])
        away_wins = len(matches_df[matches_df['home_goals'] < matches_df['away_goals']])
        
        return jsonify({
            'total_matches': int(len(matches_df)),
            'home_wins': int(home_wins),
            'draws': int(draws),
            'away_wins': int(away_wins),
            'avg_goals': round(float((matches_df['home_goals'].sum() + matches_df['away_goals'].sum()) / len(matches_df)), 2),
            'home_win_rate': round(float(home_wins / len(matches_df)), 3),
            'draw_rate': round(float(draws / len(matches_df)), 3),
            'away_win_rate': round(float(away_wins / len(matches_df)), 3)
        })
    except Exception as e:
        logger.error(f"Error getting statistics: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/health')
def health():
    """Health check"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat()
    })


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({'error': 'Not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    logger.error(f"Internal server error: {error}")
    return jsonify({'error': 'Internal server error'}), 500


if __name__ == '__main__':
    load_data()
    app.run(debug=True, host='0.0.0.0', port=5000)
