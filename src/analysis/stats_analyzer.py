"""
Statistical analysis module for football data
References: Football_Prediction_Project and football_analytics
"""

import pandas as pd
import numpy as np
from typing import Dict, Tuple
from loguru import logger


class StatsAnalyzer:
    """Analyze football match statistics"""
    
    @staticmethod
    def calculate_team_stats(matches_df: pd.DataFrame) -> pd.DataFrame:
        """Calculate comprehensive team statistics"""
        logger.info("Calculating team statistics")
        
        teams = set(list(matches_df['home_team'].unique()) + 
                   list(matches_df['away_team'].unique()))
        
        stats = []
        
        for team in teams:
            # Home matches
            home_matches = matches_df[matches_df['home_team'] == team]
            home_wins = len(home_matches[home_matches['home_goals'] > home_matches['away_goals']])
            home_draws = len(home_matches[home_matches['home_goals'] == home_matches['away_goals']])
            home_losses = len(home_matches[home_matches['home_goals'] < home_matches['away_goals']])
            home_goals_for = home_matches['home_goals'].sum()
            home_goals_against = home_matches['away_goals'].sum()
            
            # Away matches
            away_matches = matches_df[matches_df['away_team'] == team]
            away_wins = len(away_matches[away_matches['away_goals'] > away_matches['home_goals']])
            away_draws = len(away_matches[away_matches['away_goals'] == away_matches['home_goals']])
            away_losses = len(away_matches[away_matches['away_goals'] < away_matches['home_goals']])
            away_goals_for = away_matches['away_goals'].sum()
            away_goals_against = away_matches['home_goals'].sum()
            
            # Total stats
            total_matches = len(home_matches) + len(away_matches)
            total_wins = home_wins + away_wins
            total_draws = home_draws + away_draws
            total_losses = home_losses + away_losses
            total_goals_for = home_goals_for + away_goals_for
            total_goals_against = home_goals_against + away_goals_against
            
            stats.append({
                'team': team,
                'matches': total_matches,
                'wins': total_wins,
                'draws': total_draws,
                'losses': total_losses,
                'goals_for': total_goals_for,
                'goals_against': total_goals_against,
                'goal_difference': total_goals_for - total_goals_against,
                'points': total_wins * 3 + total_draws,
                'avg_goals_for': total_goals_for / total_matches if total_matches > 0 else 0,
                'avg_goals_against': total_goals_against / total_matches if total_matches > 0 else 0,
            })
        
        return pd.DataFrame(stats).sort_values('points', ascending=False)
    
    @staticmethod
    def head_to_head_analysis(matches_df: pd.DataFrame, 
                             team1: str, 
                             team2: str) -> Dict:
        """Analyze head-to-head record between two teams"""
        logger.info(f"Analyzing H2H between {team1} and {team2}")
        
        h2h = matches_df[
            ((matches_df['home_team'] == team1) & (matches_df['away_team'] == team2)) |
            ((matches_df['home_team'] == team2) & (matches_df['away_team'] == team1))
        ]
        
        if len(h2h) == 0:
            return {'total_matches': 0, 'team1_wins': 0, 'team2_wins': 0, 'draws': 0}
        
        team1_wins = len(h2h[
            ((h2h['home_team'] == team1) & (h2h['home_goals'] > h2h['away_goals'])) |
            ((h2h['away_team'] == team1) & (h2h['away_goals'] > h2h['home_goals']))
        ])
        
        team2_wins = len(h2h[h2h['home_goals'] != h2h['away_goals']]) - team1_wins
        draws = len(h2h[h2h['home_goals'] == h2h['away_goals']])
        
        return {
            'total_matches': len(h2h),
            'team1_wins': team1_wins,
            'team2_wins': team2_wins,
            'draws': draws,
        }
    
    @staticmethod
    def form_analysis(matches_df: pd.DataFrame, 
                     team: str, 
                     last_n_matches: int = 10) -> Dict:
        """Analyze team form (recent performance)"""
        logger.info(f"Analyzing form for {team} (last {last_n_matches} matches)")
        
        team_matches = matches_df[
            (matches_df['home_team'] == team) | (matches_df['away_team'] == team)
        ].tail(last_n_matches)
        
        if len(team_matches) == 0:
            return {'matches': 0, 'wins': 0, 'draws': 0, 'losses': 0}
        
        wins = losses = draws = 0
        goals_for = goals_against = 0
        
        for _, match in team_matches.iterrows():
            if match['home_team'] == team:
                goals_for += match['home_goals']
                goals_against += match['away_goals']
                if match['home_goals'] > match['away_goals']:
                    wins += 1
                elif match['home_goals'] == match['away_goals']:
                    draws += 1
                else:
                    losses += 1
            else:
                goals_for += match['away_goals']
                goals_against += match['home_goals']
                if match['away_goals'] > match['home_goals']:
                    wins += 1
                elif match['away_goals'] == match['home_goals']:
                    draws += 1
                else:
                    losses += 1
        
        return {
            'matches': len(team_matches),
            'wins': wins,
            'draws': draws,
            'losses': losses,
            'goals_for': goals_for,
            'goals_against': goals_against,
            'avg_goals_for': goals_for / len(team_matches) if len(team_matches) > 0 else 0,
        }
