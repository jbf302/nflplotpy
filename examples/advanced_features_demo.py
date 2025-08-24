#!/usr/bin/env python3
"""
Advanced Features Demo for nflplotpy

This example showcases the newest advanced features that achieve full parity
with R's nflplotR package, including:
- NFL team scale functions (scale_color_nfl, scale_fill_nfl)
- Conference and division-based color mapping
- Generic image placement (geom_from_path equivalent)
- Advanced element replacement with logos
- Enhanced reference lines and statistical overlays
- Interactive plotly visualizations

Requirements:
    - matplotlib
    - plotly (optional)
    - pandas
    - numpy
"""

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from typing import Optional

# Set up the environment
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import nflplotpy as nfl

# Create sample data
np.random.seed(42)
teams = ['BUF', 'MIA', 'NE', 'NYJ', 'BAL', 'CIN', 'CLE', 'PIT']
sample_data = pd.DataFrame({
    'team': teams,
    'passing_yards': np.random.normal(250, 50, len(teams)),
    'rushing_yards': np.random.normal(120, 30, len(teams)),
    'points': np.random.normal(24, 8, len(teams)),
    'turnovers': np.random.poisson(2, len(teams))
})

def demo_scale_functions():
    """Demonstrate the new NFL scale functions."""
    print("🎨 Demonstrating NFL Scale Functions")
    
    # Create figure with subplots
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))
    fig.suptitle('NFL Scale Functions Demo - Full nflplotR Parity', fontsize=16, fontweight='bold')
    
    # 1. Basic team color mapping
    colors, legend_info = nfl.scale_color_nfl(data=sample_data['team'].tolist())
    ax1.scatter(sample_data['passing_yards'], sample_data['points'], 
               c=[colors[team] for team in sample_data['team']], s=100, alpha=0.8)
    ax1.set_xlabel('Passing Yards')
    ax1.set_ylabel('Points Scored')
    ax1.set_title('Team Colors (Primary)')
    nfl.add_nfl_logos(ax1, sample_data['team'], sample_data['passing_yards'], 
                      sample_data['points'], size=0.05, alpha=0.7)
    
    # 2. Secondary team colors
    colors_sec, _ = nfl.scale_color_nfl(data=sample_data['team'].tolist(), color_type='secondary')
    ax2.bar(range(len(sample_data)), sample_data['rushing_yards'],
            color=[colors_sec[team] for team in sample_data['team']], alpha=0.8)
    ax2.set_xlabel('Teams')
    ax2.set_ylabel('Rushing Yards')
    ax2.set_title('Team Colors (Secondary)')
    ax2.set_xticks(range(len(sample_data)))
    ax2.set_xticklabels(sample_data['team'])
    
    # 3. Conference-based colors
    conf_colors, _ = nfl.scale_color_conference(data=sample_data['team'].tolist())
    ax3.scatter(sample_data['turnovers'], sample_data['points'],
               c=[conf_colors[team] for team in sample_data['team']], s=150, alpha=0.8)
    ax3.set_xlabel('Turnovers')
    ax3.set_ylabel('Points Scored')
    ax3.set_title('Conference Colors (AFC/NFC)')
    
    # Add conference legend
    afc_teams = [t for t in sample_data['team'] if nfl.get_team_conference(t) == 'AFC']
    nfc_teams = [t for t in sample_data['team'] if nfl.get_team_conference(t) == 'NFC']
    if afc_teams:
        ax3.scatter([], [], c=conf_colors[afc_teams[0]], label='AFC', s=100)
    if nfc_teams:
        ax3.scatter([], [], c=conf_colors[nfc_teams[0]], label='NFC', s=100)
    ax3.legend()
    
    # 4. Division rivals demonstration
    rivals = nfl.get_division_rivals('BUF')
    rival_data = sample_data[sample_data['team'].isin(rivals)]
    div_colors, _ = nfl.scale_color_division(data=rivals)
    
    ax4.scatter(rival_data['passing_yards'], rival_data['rushing_yards'],
               c=[div_colors[team] for team in rival_data['team']], s=200, alpha=0.8)
    ax4.set_xlabel('Passing Yards')
    ax4.set_ylabel('Rushing Yards')
    ax4.set_title('Division Rivals (AFC East)')
    nfl.add_nfl_logos(ax4, rival_data['team'], rival_data['passing_yards'], 
                      rival_data['rushing_yards'], size=0.08, alpha=0.9)
    
    plt.tight_layout()
    plt.show()
    print("✅ NFL Scale Functions demonstration complete!\n")

def demo_image_placement():
    """Demonstrate generic image placement (geom_from_path equivalent)."""
    print("🖼️  Demonstrating Generic Image Placement (geom_from_path)")
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    fig.suptitle('Generic Image Placement - Equivalent to nflplotR geom_from_path()', 
                 fontsize=14, fontweight='bold')
    
    # 1. Basic image placement from URLs
    x_pos = np.linspace(0, 10, len(sample_data))
    y_pos = sample_data['points'].values
    
    ax1.plot(x_pos, y_pos, 'k--', alpha=0.5, linewidth=2, label='Trend')
    
    # Place NFL logos at each data point
    for i, (x, y, team) in enumerate(zip(x_pos, y_pos, sample_data['team'])):
        logo_url = nfl.AssetURLManager().get_logo_url(team)
        nfl.add_image_from_path(ax1, logo_url, x, y, width=0.08, alpha=0.9)
    
    ax1.set_xlabel('Game Week')
    ax1.set_ylabel('Points Scored')
    ax1.set_title('NFL Logos as Data Points')
    ax1.legend()
    
    # 2. Advanced image transformations
    base_x, base_y = 5, 20
    transformations = [
        {'angle': 0, 'colorize': None, 'label': 'Normal'},
        {'angle': 45, 'colorize': None, 'label': 'Rotated 45°'},
        {'angle': 0, 'colorize': '#FF6B6B', 'label': 'Colorized Red'},
        {'angle': -30, 'colorize': '#4ECDC4', 'label': 'Rotated -30° + Teal'}
    ]
    
    logo_url = nfl.AssetURLManager().get_logo_url('BUF')
    positions = [(2, 25), (4, 20), (6, 15), (8, 10)]
    
    for (x, y), transform in zip(positions, transformations):
        nfl.add_image_from_path(ax2, logo_url, x, y, width=0.12,
                               angle=transform['angle'],
                               colorize=transform['colorize'],
                               alpha=0.8)
        ax2.text(x, y-3, transform['label'], ha='center', fontsize=8)
    
    ax2.set_xlim(0, 10)
    ax2.set_ylim(5, 30)
    ax2.set_xlabel('X Position')
    ax2.set_ylabel('Y Position')
    ax2.set_title('Image Transformations (Rotation & Colorization)')
    
    plt.tight_layout()
    plt.show()
    print("✅ Generic image placement demonstration complete!\n")

def demo_enhanced_reference_lines():
    """Demonstrate enhanced reference lines with statistical options."""
    print("📊 Demonstrating Enhanced Reference Lines")
    
    # Generate more sample data for statistical demonstrations
    np.random.seed(123)
    extended_data = pd.DataFrame({
        'x': np.random.normal(100, 20, 50),
        'y': np.random.normal(50, 15, 50),
        'category': np.random.choice(['A', 'B', 'C'], 50)
    })
    
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))
    fig.suptitle('Enhanced Reference Lines - Advanced Statistical Overlays', 
                 fontsize=16, fontweight='bold')
    
    # 1. Quantile lines
    ax1.scatter(extended_data['x'], extended_data['y'], alpha=0.6, s=60)
    nfl.add_quantile_lines(ax1, extended_data['x'], [0.25, 0.5, 0.75], 
                          orientation='vertical', colors=['red', 'blue', 'green'],
                          alpha=0.7, linewidth=2)
    ax1.set_title('Vertical Quantile Lines (Q1, Median, Q3)')
    ax1.set_xlabel('X Values')
    ax1.set_ylabel('Y Values')
    
    # 2. Mean with confidence bands
    x_smooth = np.linspace(extended_data['x'].min(), extended_data['x'].max(), 100)
    y_trend = np.polyval(np.polyfit(extended_data['x'], extended_data['y'], 1), x_smooth)
    
    ax2.scatter(extended_data['x'], extended_data['y'], alpha=0.6, s=60)
    nfl.add_mean_lines(ax2, extended_data['x'], extended_data['y'], 
                      method='trend', confidence_band=True, alpha=0.8)
    ax2.set_title('Trend Line with Confidence Band')
    ax2.set_xlabel('X Values')
    ax2.set_ylabel('Y Values')
    
    # 3. Reference bands
    y_mean = extended_data['y'].mean()
    y_std = extended_data['y'].std()
    
    ax3.scatter(extended_data['x'], extended_data['y'], alpha=0.6, s=60)
    nfl.add_reference_band(ax3, y_mean - y_std, y_mean + y_std, 
                          orientation='horizontal', alpha=0.3, color='lightblue',
                          label='±1 Standard Deviation')
    nfl.add_mean_lines(ax3, extended_data['y'], orientation='horizontal', 
                      color='darkblue', linewidth=3, alpha=0.8)
    ax3.set_title('Horizontal Reference Band (Mean ± 1σ)')
    ax3.set_xlabel('X Values')
    ax3.set_ylabel('Y Values')
    ax3.legend()
    
    # 4. Multiple statistical overlays
    ax4.scatter(extended_data['x'], extended_data['y'], alpha=0.6, s=60)
    
    # Add multiple reference elements
    nfl.add_quantile_lines(ax4, extended_data['y'], [0.1, 0.9], 
                          orientation='horizontal', colors=['red'], 
                          linestyle='--', alpha=0.7, linewidth=2)
    nfl.add_mean_lines(ax4, extended_data['y'], orientation='horizontal',
                      color='darkgreen', linewidth=3)
    nfl.add_median_lines(ax4, extended_data['y'], orientation='horizontal',
                        color='orange', linewidth=2, linestyle='-.')
    
    ax4.set_title('Multiple Statistical References')
    ax4.set_xlabel('X Values')
    ax4.set_ylabel('Y Values')
    ax4.legend(['Data', '10th/90th Percentiles', 'Mean', 'Median'])
    
    plt.tight_layout()
    plt.show()
    print("✅ Enhanced reference lines demonstration complete!\n")

def demo_element_replacement():
    """Demonstrate advanced element replacement with logos."""
    print("🔄 Demonstrating Advanced Element Replacement")
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    fig.suptitle('Element Replacement - Replace Text with NFL Logos', 
                 fontsize=14, fontweight='bold')
    
    # 1. Custom logo-based legend
    team_stats = sample_data.copy()
    team_stats['efficiency'] = team_stats['points'] / team_stats['turnovers']
    
    scatter = ax1.scatter(team_stats['passing_yards'], team_stats['points'], 
                         c=team_stats['efficiency'], s=100, cmap='viridis', alpha=0.8)
    
    # Create custom logo legend for top 3 teams
    top_teams = team_stats.nlargest(3, 'efficiency')['team'].tolist()
    nfl.create_logo_legend(ax1, top_teams, labels=[f'{team} (Top Efficiency)' for team in top_teams],
                          loc='upper left', logo_size=0.06)
    
    ax1.set_xlabel('Passing Yards')
    ax1.set_ylabel('Points Scored')
    ax1.set_title('Custom Logo Legend')
    
    # Add colorbar
    cbar = plt.colorbar(scatter, ax=ax1)
    cbar.set_label('Efficiency (Points/Turnover)')
    
    # 2. Replace axis labels with team logos
    ax2.bar(range(len(sample_data)), sample_data['points'], 
           color=[nfl.scale_color_nfl(data=sample_data['team'].tolist())[0][team] 
                  for team in sample_data['team']], alpha=0.8)
    
    ax2.set_ylabel('Points Scored')
    ax2.set_title('Team Logos as X-Axis Labels')
    
    # Replace x-axis labels with logos
    ax2.set_xticks(range(len(sample_data)))
    ax2.set_xticklabels([])  # Remove text labels
    
    # Add team logos as x-axis labels
    for i, team in enumerate(sample_data['team']):
        logo_url = nfl.AssetURLManager().get_logo_url(team)
        nfl.add_image_from_path(ax2, logo_url, i, -2, width=0.08, alpha=0.9)
    
    # Adjust y-axis to accommodate logos
    ax2.set_ylim(-5, max(sample_data['points']) * 1.1)
    
    plt.tight_layout()
    plt.show()
    print("✅ Element replacement demonstration complete!\n")

def demo_interactive_plotly():
    """Demonstrate enhanced plotly integration."""
    print("🌐 Demonstrating Interactive Plotly Features")
    
    try:
        import plotly.graph_objects as go
        from plotly.subplots import make_subplots
        
        # Create interactive team plot
        fig = nfl.create_interactive_team_plot(
            sample_data, 
            x_col='passing_yards',
            y_col='points',
            team_col='team',
            title='Interactive NFL Team Performance',
            hover_data=['rushing_yards', 'turnovers']
        )
        
        # Save as HTML file
        output_file = os.path.join(os.path.dirname(__file__), 'advanced_features_interactive.html')
        fig.write_html(output_file)
        print(f"📄 Interactive plot saved to: {output_file}")
        
        # Create team bar chart with color scale
        bar_fig = nfl.create_team_bar(
            sample_data,
            x_col='team',
            y_col='points',
            title='Team Points - Interactive Bar Chart',
            color_scale='primary'
        )
        
        # Save bar chart
        bar_output = os.path.join(os.path.dirname(__file__), 'advanced_features_bar_chart.html')
        bar_fig.write_html(bar_output)
        print(f"📊 Interactive bar chart saved to: {bar_output}")
        
        print("✅ Interactive plotly demonstration complete!")
        
    except ImportError:
        print("⚠️  Plotly not available. Skipping interactive demonstrations.")
    print()

def demo_conference_division_analysis():
    """Demonstrate conference and division analysis utilities."""
    print("🏈 Demonstrating Conference & Division Analysis")
    
    # Get sample teams from different divisions
    afc_east = nfl.get_teams_by_division('AFC', 'East')
    nfc_north = nfl.get_teams_by_division('NFC', 'North')
    
    print("AFC East Teams:", afc_east)
    print("NFC North Teams:", nfc_north)
    
    # Analyze division matchups
    sample_team = 'BUF'
    rivals = nfl.get_division_rivals(sample_team)
    conference = nfl.get_team_conference(sample_team)
    division = nfl.get_team_division(sample_team)
    
    print(f"\n{sample_team} Analysis:")
    print(f"Conference: {conference}")
    print(f"Division: {division}")
    print(f"Division Rivals: {rivals}")
    
    # Create visualization
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Plot all AFC East teams
    afc_east_data = sample_data[sample_data['team'].isin(afc_east)]
    colors, _ = nfl.scale_color_nfl(data=afc_east_data['team'].tolist())
    
    bars = ax.bar(afc_east_data['team'], afc_east_data['points'],
                  color=[colors[team] for team in afc_east_data['team']],
                  alpha=0.8, edgecolor='black', linewidth=2)
    
    # Highlight the sample team
    for bar, team in zip(bars, afc_east_data['team']):
        if team == sample_team:
            bar.set_edgecolor('gold')
            bar.set_linewidth(4)
    
    ax.set_title(f'AFC East Division Analysis - {sample_team} Highlighted', 
                fontsize=14, fontweight='bold')
    ax.set_xlabel('Team')
    ax.set_ylabel('Points Scored')
    
    # Add team logos
    for team, points in zip(afc_east_data['team'], afc_east_data['points']):
        logo_url = nfl.AssetURLManager().get_logo_url(team)
        nfl.add_image_from_path(ax, logo_url, 
                               list(afc_east_data['team']).index(team), 
                               points + 1, width=0.1, alpha=0.9)
    
    plt.tight_layout()
    plt.show()
    print("✅ Conference & division analysis complete!\n")

def main():
    """Run all advanced features demonstrations."""
    print("🚀 nflplotpy Advanced Features Demo")
    print("=" * 50)
    print("Showcasing newest features for full nflplotR parity:")
    print("- NFL team scale functions")
    print("- Conference/division analysis")
    print("- Generic image placement")
    print("- Enhanced statistical overlays")
    print("- Advanced element replacement")
    print("- Interactive plotly integration")
    print("=" * 50)
    print()
    
    # Run all demonstrations
    demo_scale_functions()
    demo_image_placement()
    demo_enhanced_reference_lines()
    demo_element_replacement()
    demo_interactive_plotly()
    demo_conference_division_analysis()
    
    print("🎉 All advanced features demonstrations complete!")
    print("\nThese features provide full parity with R's nflplotR package")
    print("plus additional Python-specific enhancements for data analysis.")

if __name__ == "__main__":
    main()