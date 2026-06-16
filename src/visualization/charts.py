"""
Data visualization module for football analytics
"""

import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from typing import List, Dict
from loguru import logger


class FootballVisualizer:
    """Create visualizations for football data"""
    
    COLORS = {
        'primary': '#1f77b4',
        'secondary': '#ff7f0e',
        'success': '#2ca02c',
        'danger': '#d62728',
        'neutral': '#7f7f7f',
    }
    
    @staticmethod
    def plot_team_comparison(teams_stats: pd.DataFrame, 
                            metric: str = 'points') -> go.Figure:
        """Create bar chart comparing teams by metric"""
        logger.info(f"Creating team comparison chart for metric: {metric}")
        
        if metric not in teams_stats.columns:
            logger.warning(f"Metric {metric} not found in DataFrame")
            return go.Figure()
        
        df_sorted = teams_stats.nlargest(10, metric)
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=df_sorted['team'],
            y=df_sorted[metric],
            marker_color=FootballVisualizer.COLORS['primary'],
            text=df_sorted[metric],
            textposition='auto',
        ))
        
        fig.update_layout(
            title=f'Top 10 Teams by {metric.title()}',
            xaxis_title='Team',
            yaxis_title=metric.title(),
            hovermode='x unified',
            template='plotly_white',
        )
        
        return fig
    
    @staticmethod
    def plot_goal_distribution(matches_df: pd.DataFrame) -> go.Figure:
        """Create histogram of goal distribution"""
        logger.info("Creating goal distribution chart")
        
        if 'home_goals' not in matches_df.columns or 'away_goals' not in matches_df.columns:
            logger.warning("Goals columns not found in DataFrame")
            return go.Figure()
        
        all_goals = pd.concat([matches_df['home_goals'], matches_df['away_goals']])
        
        fig = go.Figure()
        fig.add_trace(go.Histogram(
            x=all_goals,
            nbinsx=max(int(all_goals.max()), 8),
            marker_color=FootballVisualizer.COLORS['primary'],
            name='Goals'
        ))
        
        fig.update_layout(
            title='Distribution of Goals per Match',
            xaxis_title='Number of Goals',
            yaxis_title='Frequency',
            hovermode='x',
            template='plotly_white',
        )
        
        return fig
    
    @staticmethod
    def export_html(fig: go.Figure, filepath: str):
        """Export figure to HTML file"""
        fig.write_html(filepath)
        logger.info(f"Chart exported to {filepath}")
