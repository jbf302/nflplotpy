#!/usr/bin/env python3
"""
NFL Team Performance with Wordmarks (Matplotlib Version)

This script demonstrates proper wordmark integration using matplotlib:
- X-axis: Teams with wordmarks replacing text labels
- Y-axis: Net Points per Win for 2024 season
- Team-colored bars with wordmarks below
- Comprehensive hover-like annotations

Requirements:
- nflplotpy[all] or nflplotpy with matplotlib and nfl_data_py installed
"""

import warnings
warnings.filterwarnings('ignore')

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

try:
    import nfl_data_py as nfl
    NFL_DATA_AVAILABLE = True
except ImportError:
    NFL_DATA_AVAILABLE = False
    print("nfl_data_py not available. Using sample data instead.")

import nflplotpy as nflplot
from nflplotpy.matplotlib.elements import set_xlabel_with_wordmarks, add_team_wordmark
from nflplotpy.matplotlib.artists import add_median_lines
from nflplotpy.core.colors import get_team_colors


def load_2024_team_data():
    """Load 2024 team performance data."""
    
    # Team abbreviation mapping from nfl_data_py to nflplotpy
    TEAM_MAPPING = {
        'JAX': 'JAC',  # Jacksonville
        'LA': 'LAR',   # Los Angeles Rams (assuming LAR for LA)
    }
    
    if not NFL_DATA_AVAILABLE:
        print("Using sample 2024 team data...")
        teams = [
            'KC', 'BUF', 'CIN', 'BAL', 'TEN', 'IND', 'HOU', 'JAC', 'LAC', 'LV', 'DEN', 'CLE', 'PIT', 'NYJ', 'MIA', 'NE',
            'DAL', 'PHI', 'NYG', 'WAS', 'GB', 'MIN', 'CHI', 'DET', 'TB', 'NO', 'ATL', 'CAR', 'LAR', 'SF', 'SEA', 'ARI'
        ]
        
        sample_data = []
        for i, team in enumerate(teams):
            # Generate realistic 2024 performance metrics
            wins = np.random.randint(4, 15)
            points_for = np.random.randint(250, 450) 
            points_against = np.random.randint(250, 450)
            net_points = points_for - points_against
            net_points_per_win = net_points / max(wins, 1)
            
            sample_data.append({
                'team': team,
                'wins': wins,
                'losses': 17 - wins,
                'points_for': points_for,
                'points_against': points_against,
                'net_points': net_points,
                'net_points_per_win': net_points_per_win
            })
        
        return pd.DataFrame(sample_data)
    
    print("Loading real 2024 NFL team data...")
    
    try:
        # Load 2024 schedule data
        schedule = nfl.import_schedules([2024])
        completed_games = schedule[schedule['result'].notna()].copy()
        
        team_stats = []
        teams = set(completed_games['home_team'].unique()) | set(completed_games['away_team'].unique())
        
        for team in teams:
            # Map team abbreviations to nflplotpy format
            mapped_team = TEAM_MAPPING.get(team, team)
            # Home games
            home_games = completed_games[completed_games['home_team'] == team].copy()
            home_wins = len(home_games[home_games['result'] > 0])
            home_points_for = home_games['home_score'].sum()
            home_points_against = home_games['away_score'].sum()
            
            # Away games  
            away_games = completed_games[completed_games['away_team'] == team].copy()
            away_wins = len(away_games[away_games['result'] < 0])
            away_points_for = away_games['away_score'].sum()
            away_points_against = away_games['home_score'].sum()
            
            # Combined stats
            total_wins = home_wins + away_wins
            total_games = len(home_games) + len(away_games)
            total_points_for = home_points_for + away_points_for
            total_points_against = home_points_against + away_points_against
            net_points = total_points_for - total_points_against
            net_points_per_win = net_points / max(total_wins, 1)
            
            team_stats.append({
                'team': mapped_team,  # Use mapped team name
                'games': total_games,
                'wins': total_wins,
                'losses': total_games - total_wins,
                'points_for': total_points_for,
                'points_against': total_points_against,
                'net_points': net_points,
                'net_points_per_win': net_points_per_win
            })
        
        df = pd.DataFrame(team_stats)
        df = df[df['games'] >= 10]  # Filter for teams with meaningful sample
        print(f"Loaded data for {len(df)} teams")
        return df
        
    except Exception as e:
        print(f"Error loading NFL data: {e}")
        print("Falling back to sample data...")
        return load_2024_team_data()


def split_afc_nfc_teams(team_data):
    """Split team data into AFC and NFC divisions."""
    
    # AFC teams
    afc_teams = [
        'BUF', 'MIA', 'NE', 'NYJ',  # AFC East
        'BAL', 'CIN', 'CLE', 'PIT',  # AFC North
        'HOU', 'IND', 'JAC', 'TEN',  # AFC South
        'DEN', 'KC', 'LV', 'LAC'     # AFC West
    ]
    
    # NFC teams  
    nfc_teams = [
        'DAL', 'NYG', 'PHI', 'WAS',  # NFC East
        'CHI', 'DET', 'GB', 'MIN',   # NFC North
        'ATL', 'CAR', 'NO', 'TB',    # NFC South
        'ARI', 'LAR', 'SF', 'SEA'    # NFC West
    ]
    
    afc_data = team_data[team_data['team'].isin(afc_teams)].copy()
    nfc_data = team_data[team_data['team'].isin(nfc_teams)].copy()
    
    return afc_data, nfc_data


def create_conference_wordmark_charts(team_data):
    """Create separate bar charts for AFC and NFC with team wordmarks."""
    
    # Split into conferences
    afc_data, nfc_data = split_afc_nfc_teams(team_data)
    
    # Sort each conference by net points per win
    afc_data = afc_data.sort_values('net_points_per_win', ascending=True)
    nfc_data = nfc_data.sort_values('net_points_per_win', ascending=True)
    
    # Create side-by-side subplots
    fig, (ax_afc, ax_nfc) = plt.subplots(2, 1, figsize=(16, 16))
    
    conferences = [
        (afc_data, ax_afc, 'AFC', '#013369'),  # NFL blue
        (nfc_data, ax_nfc, 'NFC', '#d50a0a')   # NFL red
    ]
    
    for conf_data, ax, conf_name, conf_color in conferences:
        # Get team data for this conference
        teams = conf_data['team'].tolist()
        values = conf_data['net_points_per_win'].tolist()
        
        # Get team colors for bars
        colors = []
        for team in teams:
            try:
                color = get_team_colors(team, 'primary')
                colors.append(color)
            except:
                colors.append(conf_color)  # Conference color fallback
        
        # Create bars
        x_positions = range(len(teams))
        bars = ax.bar(x_positions, values, color=colors, alpha=0.8, 
                      edgecolor='white', linewidth=1.5)
        
        # Add value labels on bars
        for i, (bar, value) in enumerate(zip(bars, values)):
            height = bar.get_height()
            label_y = height + (2 if height > 0 else -8)
            ax.text(bar.get_x() + bar.get_width()/2., label_y,
                    f'{value:+.1f}',
                    ha='center', va='bottom' if height > 0 else 'top',
                    fontweight='bold', fontsize=10,
                    color='black' if height > 0 else 'red')
        
        # Replace x-axis labels with team wordmarks
        print(f"Adding {conf_name} team wordmarks to x-axis...")
        set_xlabel_with_wordmarks(ax, teams, positions=x_positions, wordmark_size=0.12)
        
        # Add reference line at zero
        ax.axhline(y=0, color='black', linestyle='-', linewidth=2, alpha=0.8)
        
        # Add median line for this conference
        median_val = np.median(values)
        ax.axhline(y=median_val, color=conf_color, linestyle='--', linewidth=2, alpha=0.7)
        ax.text(len(teams)-1, median_val + 3, f'{conf_name} Median: {median_val:+.1f}', 
                ha='right', va='bottom', color=conf_color, fontweight='bold')
        
        # Styling for each subplot
        ax.set_ylabel('Net Points per Win', fontsize=12, fontweight='bold')
        ax.set_title(f'{conf_name} 2024 Team Performance: Net Points per Win\n'
                     f'Team Wordmarks • Positive = Scoring More Than Opponents', 
                     fontsize=14, fontweight='bold', pad=15)
        
        # Apply NFL theme
        nflplot.apply_nfl_theme(ax, style='default')
        
        # Add subtle grid
        ax.grid(True, axis='y', alpha=0.3, linestyle='-', linewidth=0.5)
        ax.set_axisbelow(True)
    
    # Adjust layout for wordmarks
    plt.tight_layout()
    plt.subplots_adjust(bottom=0.15)  # Extra space for wordmarks
    
    return fig, (ax_afc, ax_nfc), afc_data, nfc_data


def create_wordmark_bar_chart(team_data):
    """Create bar chart with team wordmarks on x-axis."""
    
    # Use the new conference-based approach
    return create_conference_wordmark_charts(team_data)


def add_performance_annotations(ax, team_data):
    """Add annotations highlighting top and bottom performers."""
    
    # Find top 3 and bottom 3 performers
    top_3 = team_data.nlargest(3, 'net_points_per_win')
    bottom_3 = team_data.nsmallest(3, 'net_points_per_win')
    
    # Add top performers annotation
    top_teams = ', '.join(top_3['team'].tolist())
    top_text = f"🏆 Top Performers: {top_teams}"
    ax.text(0.02, 0.98, top_text, transform=ax.transAxes, fontsize=11,
            verticalalignment='top', bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.8))
    
    # Add bottom performers annotation  
    bottom_teams = ', '.join(bottom_3['team'].tolist())
    bottom_text = f"📉 Needs Improvement: {bottom_teams}"
    ax.text(0.02, 0.02, bottom_text, transform=ax.transAxes, fontsize=11,
            verticalalignment='bottom', bbox=dict(boxstyle='round', facecolor='lightcoral', alpha=0.8))


def create_summary_table(team_data):
    """Create and display summary statistics."""
    
    print("\n" + "="*60)
    print("2024 NFL TEAM PERFORMANCE SUMMARY")
    print("="*60)
    
    # Top 5 teams
    top_5 = team_data.nlargest(5, 'net_points_per_win')[
        ['team', 'wins', 'losses', 'net_points', 'net_points_per_win']
    ]
    print("\n🏆 TOP 5 TEAMS (Net Points per Win):")
    print(top_5.to_string(index=False, float_format='{:+.1f}'.format))
    
    # Bottom 5 teams
    bottom_5 = team_data.nsmallest(5, 'net_points_per_win')[
        ['team', 'wins', 'losses', 'net_points', 'net_points_per_win']
    ]
    print("\n📉 BOTTOM 5 TEAMS (Net Points per Win):")
    print(bottom_5.to_string(index=False, float_format='{:+.1f}'.format))
    
    # Statistical summary
    print(f"\n📊 LEAGUE STATISTICS:")
    print(f"Average Net Points per Win: {team_data['net_points_per_win'].mean():+.1f}")
    print(f"Median Net Points per Win: {team_data['net_points_per_win'].median():+.1f}")
    print(f"Standard Deviation: {team_data['net_points_per_win'].std():.1f}")
    print(f"Range: {team_data['net_points_per_win'].min():+.1f} to {team_data['net_points_per_win'].max():+.1f}")


def main():
    """Main execution function."""
    
    print("🏈 NFL Team Performance with Wordmarks (Matplotlib)")
    print("=" * 55)
    
    # Load team performance data
    team_data = load_2024_team_data()
    print(f"\nLoaded data for {len(team_data)} teams")
    
    # Create the visualization
    print(f"\nCreating AFC and NFC wordmark charts...")
    fig, (ax_afc, ax_nfc), afc_data, nfc_data = create_wordmark_bar_chart(team_data)
    
    # Add performance annotations for both conferences
    add_performance_annotations(ax_afc, afc_data)
    add_performance_annotations(ax_nfc, nfc_data)
    
    # Display summary statistics
    print(f"\n{'='*60}")
    print("AFC CONFERENCE SUMMARY")
    print(f"{'='*60}")
    create_summary_table(afc_data)
    
    print(f"\n{'='*60}")
    print("NFC CONFERENCE SUMMARY") 
    print(f"{'='*60}")
    create_summary_table(nfc_data)
    
    # Save the plot
    output_file = 'examples/2024_team_wordmarks_matplotlib.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight', 
                facecolor='white', edgecolor='none')
    print(f"\n✅ Plot saved to: {output_file}")
    
    # Show the plot
    plt.show()
    
    print("\n📊 Visualization Features:")
    print("• Team wordmarks replace traditional x-axis labels")
    print("• Bar colors match official team colors")
    print("• Positive values = team scored more than opponents")
    print("• Red dashed line shows league median performance")
    print("• Value labels show exact net points per win")
    print("• Performance annotations highlight top/bottom teams")


if __name__ == "__main__":
    main()