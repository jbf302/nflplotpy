#!/usr/bin/env python3
"""
Pandas Tables Showcase for nflplotpy

This example demonstrates the comprehensive pandas table styling capabilities
that provide equivalent functionality to R's gt_nfl_logos, gt_nfl_headshots, 
and gt_nfl_wordmarks functions.

Features demonstrated:
- Team logos in tables (gt_nfl_logos equivalent)
- Player headshots in tables (gt_nfl_headshots equivalent)  
- Team wordmarks styling
- Advanced table customization with team colors
- Professional NFL-themed styling
- Method chaining for complex layouts
- HTML export for web dashboards

Requirements:
    - pandas
    - pillow
    - requests
"""

import sys
import os
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import pandas as pd
import numpy as np

# Set random seed for reproducible results
np.random.seed(42)

try:
    import nflplotpy as nfl
    print("✅ Successfully imported nflplotpy")
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Make sure nflplotpy is installed: pip install -e .")
    sys.exit(1)

def create_sample_data():
    """Create comprehensive sample data for demonstrations."""
    print("📊 Creating sample NFL data...")
    
    # Team standings data
    teams = ['KC', 'BUF', 'CIN', 'BAL', 'SF', 'DAL', 'GB', 'TB', 'MIA', 'DET']
    standings_data = pd.DataFrame({
        'team': teams,
        'wins': [14, 13, 12, 11, 12, 12, 9, 9, 11, 12],
        'losses': [3, 4, 5, 6, 5, 5, 8, 8, 6, 5],
        'points_for': [456, 482, 421, 398, 421, 396, 369, 348, 404, 442],
        'points_against': [284, 298, 298, 327, 298, 352, 379, 365, 323, 314],
        'point_diff': [172, 184, 123, 71, 123, 44, -10, -17, 81, 128],
        'playoff_prob': [95.2, 87.4, 72.1, 45.8, 89.3, 78.2, 12.4, 8.7, 56.3, 83.9]
    })
    
    # QB performance data
    qb_data = pd.DataFrame({
        'player': ['Patrick Mahomes', 'Josh Allen', 'Joe Burrow', 'Lamar Jackson'],
        'team': ['KC', 'BUF', 'CIN', 'BAL'],
        'passing_yards': [4183, 4306, 3446, 3678],
        'touchdowns': [26, 29, 21, 24],
        'interceptions': [11, 18, 5, 7],
        'completion_pct': [67.2, 63.1, 66.8, 62.4],
        'passer_rating': [92.6, 87.4, 103.4, 109.7],
        'qbr': [58.2, 64.1, 72.4, 66.8]
    })
    
    # Division breakdown
    division_data = pd.DataFrame({
        'division': ['AFC East', 'AFC North', 'AFC South', 'AFC West',
                    'NFC East', 'NFC North', 'NFC South', 'NFC West'],
        'best_team': ['BUF', 'CIN', 'JAX', 'KC', 'DAL', 'DET', 'TB', 'SF'],
        'avg_wins': [8.5, 9.2, 7.8, 10.2, 9.1, 8.8, 7.4, 9.8],
        'playoff_teams': [2, 3, 1, 2, 2, 1, 1, 2],
        'total_points': [1847, 1956, 1682, 1823, 1789, 1723, 1564, 1887]
    })
    
    return standings_data, qb_data, division_data

def demo_basic_logo_table(standings_data):
    """Demonstrate basic team logo table functionality."""
    print("\n🏈 Creating Basic Logo Table (gt_nfl_logos equivalent)")
    
    # Method 1: Simple logo replacement
    basic_table = nfl.style_with_logos(
        standings_data.head(), 
        'team',               # Column containing team abbreviations
        logo_height=25,       # Size of logos in pixels
        replace_text=True     # Replace text with logos
    )
    
    # Export to HTML
    output_file = Path(__file__).parent / 'basic_logo_table.html'
    basic_table.to_html(str(output_file))
    print(f"✅ Saved: {output_file}")
    
    return basic_table

def demo_qb_headshots_table(qb_data):
    """Demonstrate player headshots table functionality.""" 
    print("\n👤 Creating QB Headshots Table (gt_nfl_headshots equivalent)")
    
    # Create table with player headshots
    headshots_table = nfl.style_with_headshots(
        qb_data,
        'player',              # Column with player names/IDs
        headshot_height=35,    # Size of headshots
        id_type='auto',        # Auto-detect ID type (name, ESPN, GSIS)
        replace_text=False     # Keep text alongside headshots
    )
    
    # Export to HTML
    output_file = Path(__file__).parent / 'qb_headshots_table.html'
    headshots_table.to_html(str(output_file))
    print(f"✅ Saved: {output_file}")
    
    return headshots_table

def demo_wordmarks_table(standings_data):
    """Demonstrate team wordmarks table functionality."""
    print("\n🏷️  Creating Wordmarks Table (gt_nfl_wordmarks equivalent)")
    
    # Create table with team wordmarks
    wordmarks_table = nfl.style_with_wordmarks(
        standings_data.head(),
        'team',                # Column with team abbreviations
        wordmark_height=18,    # Size of wordmarks
        replace_text=True      # Replace text with wordmarks
    )
    
    # Export to HTML
    output_file = Path(__file__).parent / 'wordmarks_table.html'
    wordmarks_table.to_html(str(output_file))
    print(f"✅ Saved: {output_file}")
    
    return wordmarks_table

def demo_advanced_styling(standings_data):
    """Demonstrate advanced table styling with team colors and NFL theme."""
    print("\n🎨 Creating Advanced Styled Table")
    
    # Use the NFLTableStyler class for advanced customization
    advanced_table = (
        nfl.NFLTableStyler(standings_data)
        .with_team_logos('team', logo_height=30)
        .with_team_colors(['wins', 'losses'], 'team', 
                         color_type='primary', apply_to='background')
        .with_nfl_theme(alternating_rows=True, header_style='bold')
    )
    
    # Export to HTML
    output_file = Path(__file__).parent / 'advanced_styled_table.html'
    advanced_table.save_html(str(output_file))
    print(f"✅ Saved: {output_file}")
    
    return advanced_table

def demo_comprehensive_table(standings_data):
    """Demonstrate the high-level create_nfl_table function."""
    print("\n🏆 Creating Comprehensive NFL Table")
    
    # Use high-level function for quick professional tables
    comprehensive_table = nfl.create_nfl_table(
        standings_data,
        team_column='team',
        logo_columns=['team'],            # Columns to add logos to
        color_columns=['point_diff'],     # Columns to color by team
        title='2024 NFL Standings Analysis'
    )
    
    # Export to HTML
    output_file = Path(__file__).parent / 'comprehensive_nfl_table.html'
    comprehensive_table.save_html(str(output_file))
    print(f"✅ Saved: {output_file}")
    
    return comprehensive_table

def demo_division_analysis(division_data):
    """Create division analysis table with best team logos."""
    print("\n🏟️  Creating Division Analysis Table")
    
    # Create table showing best team from each division
    division_table = nfl.style_with_logos(
        division_data,
        'best_team',           # Column containing team abbreviations
        logo_height=28,
        replace_text=False     # Keep team abbreviation + logo
    )
    
    # Export to HTML
    output_file = Path(__file__).parent / 'division_analysis_table.html'
    division_table.to_html(str(output_file))
    print(f"✅ Saved: {output_file}")
    
    return division_table

def demo_multi_feature_table(standings_data, qb_data):
    """Create a complex table combining multiple features."""
    print("\n🔧 Creating Multi-Feature Showcase Table")
    
    # Merge standings with QB data for comprehensive view
    merged_data = standings_data.merge(
        qb_data[['team', 'player', 'passer_rating']], 
        on='team', 
        how='left'
    ).fillna({'player': 'Team QB', 'passer_rating': 0})
    
    # Create complex table with multiple styling elements
    multi_table = (
        nfl.NFLTableStyler(merged_data.head(6))
        .with_team_logos('team', logo_height=25, replace_text=True)
        .with_team_colors(['wins'], 'team', color_type='primary', apply_to='background')
        .with_team_colors(['losses'], 'team', color_type='secondary', apply_to='text')
        .with_nfl_theme(alternating_rows=True)
    )
    
    # Export to HTML
    output_file = Path(__file__).parent / 'multi_feature_table.html'
    multi_table.save_html(str(output_file))
    print(f"✅ Saved: {output_file}")
    
    return multi_table

def create_summary_report():
    """Create an HTML summary report linking all created tables."""
    print("\n📋 Creating Summary Report")
    
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>NFL Pandas Tables Showcase</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; background-color: #f5f5f5; }
            .container { max-width: 1200px; margin: 0 auto; background: white; padding: 20px; border-radius: 10px; }
            h1 { color: #013369; text-align: center; }
            .section { margin: 30px 0; padding: 20px; border: 1px solid #ddd; border-radius: 5px; }
            .section h2 { color: #d50a0a; }
            .table-link { display: inline-block; margin: 10px; padding: 10px 15px; 
                         background: #013369; color: white; text-decoration: none; border-radius: 5px; }
            .table-link:hover { background: #d50a0a; }
            .feature-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; }
            .feature-card { padding: 15px; border: 1px solid #ddd; border-radius: 5px; background: #f9f9f9; }
            .code-sample { background: #f4f4f4; padding: 10px; border-radius: 3px; font-family: monospace; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🏈 NFL Pandas Tables Showcase</h1>
            <p style="text-align: center; color: #666; font-size: 18px;">
                Complete demonstration of nflplotpy's pandas table styling capabilities
            </p>
            
            <div class="section">
                <h2>📊 Generated Tables</h2>
                <p>Click the links below to view each generated table:</p>
                <div>
                    <a href="basic_logo_table.html" class="table-link">🏈 Basic Logo Table</a>
                    <a href="qb_headshots_table.html" class="table-link">👤 QB Headshots</a>
                    <a href="wordmarks_table.html" class="table-link">🏷️ Wordmarks Table</a>
                    <a href="advanced_styled_table.html" class="table-link">🎨 Advanced Styling</a>
                    <a href="comprehensive_nfl_table.html" class="table-link">🏆 Comprehensive</a>
                    <a href="division_analysis_table.html" class="table-link">🏟️ Division Analysis</a>
                    <a href="multi_feature_table.html" class="table-link">🔧 Multi-Feature</a>
                </div>
            </div>
            
            <div class="section">
                <h2>✨ Key Features Demonstrated</h2>
                <div class="feature-grid">
                    <div class="feature-card">
                        <h3>🏈 Team Logos (gt_nfl_logos)</h3>
                        <p>Replace team abbreviations with actual NFL team logos in tables</p>
                        <div class="code-sample">nfl.style_with_logos(df, 'team')</div>
                    </div>
                    <div class="feature-card">
                        <h3>👤 Player Headshots (gt_nfl_headshots)</h3>
                        <p>Add ESPN player headshot photos to player name columns</p>
                        <div class="code-sample">nfl.style_with_headshots(df, 'player')</div>
                    </div>
                    <div class="feature-card">
                        <h3>🏷️ Team Wordmarks</h3>
                        <p>Use official team wordmarks for subtle professional styling</p>
                        <div class="code-sample">nfl.style_with_wordmarks(df, 'team')</div>
                    </div>
                    <div class="feature-card">
                        <h3>🎨 Team Color Integration</h3>
                        <p>Apply official team colors as backgrounds or text colors</p>
                        <div class="code-sample">styler.with_team_colors(['col'], 'team')</div>
                    </div>
                    <div class="feature-card">
                        <h3>🏆 Professional NFL Theming</h3>
                        <p>Official NFL colors, fonts, and styling for professional reports</p>
                        <div class="code-sample">styler.with_nfl_theme()</div>
                    </div>
                    <div class="feature-card">
                        <h3>🔧 Method Chaining</h3>
                        <p>Fluent interface for complex table customizations</p>
                        <div class="code-sample">NFLTableStyler(df).with_logos().with_colors()</div>
                    </div>
                </div>
            </div>
            
            <div class="section">
                <h2>🚀 Usage Examples</h2>
                <h3>Quick Start:</h3>
                <div class="code-sample">
import nflplotpy as nfl<br>
styled = nfl.style_with_logos(df, 'team_column')<br>
styled.to_html('output.html')
                </div>
                
                <h3>Advanced Customization:</h3>
                <div class="code-sample">
table = nfl.create_nfl_table(<br>
&nbsp;&nbsp;&nbsp;&nbsp;df, team_column='team',<br>
&nbsp;&nbsp;&nbsp;&nbsp;logo_columns=['team'],<br>
&nbsp;&nbsp;&nbsp;&nbsp;color_columns=['wins'],<br>
&nbsp;&nbsp;&nbsp;&nbsp;title='NFL Analysis'<br>
)<br>
table.save_html('analysis.html')
                </div>
            </div>
            
            <div class="section">
                <h2>📈 Benefits</h2>
                <ul>
                    <li><strong>Professional Output:</strong> Publication-ready tables for reports and dashboards</li>
                    <li><strong>No Manual Work:</strong> Automatically fetches and embeds NFL assets</li>
                    <li><strong>Full R Parity:</strong> Complete equivalent to gt_nfl_logos(), gt_nfl_headshots()</li>
                    <li><strong>Web Ready:</strong> HTML output perfect for web dashboards</li>
                    <li><strong>Customizable:</strong> Extensive styling options and method chaining</li>
                </ul>
            </div>
            
            <div style="text-align: center; margin-top: 40px; color: #666;">
                <p>Generated by nflplotpy v2.0 - Python NFL Data Visualization</p>
                <p>🏈 Complete feature parity with R's nflplotR package 📊</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    output_file = Path(__file__).parent / 'pandas_tables_showcase.html'
    output_file.write_text(html_content, encoding='utf-8')
    print(f"✅ Saved summary report: {output_file}")

def main():
    """Run the complete pandas tables showcase."""
    print("🏈 NFL Pandas Tables Showcase")
    print("=" * 50)
    print("This example demonstrates all pandas table styling capabilities")
    print("equivalent to R's gt_nfl_logos, gt_nfl_headshots, and more!")
    print()
    
    # Create sample data
    standings_data, qb_data, division_data = create_sample_data()
    
    # Run all demonstrations
    try:
        demo_basic_logo_table(standings_data)
        demo_qb_headshots_table(qb_data)
        demo_wordmarks_table(standings_data)
        demo_advanced_styling(standings_data)
        demo_comprehensive_table(standings_data)
        demo_division_analysis(division_data)
        demo_multi_feature_table(standings_data, qb_data)
        
        # Create summary report
        create_summary_report()
        
        print("\n" + "=" * 50)
        print("🎉 Pandas Tables Showcase Complete!")
        print("=" * 50)
        print("\n📋 Generated Files:")
        
        output_dir = Path(__file__).parent
        html_files = list(output_dir.glob('*.html'))
        
        for html_file in sorted(html_files):
            if html_file.name.startswith(('basic_', 'qb_', 'word', 'adv', 'comp', 'div', 'multi', 'panda')):
                print(f"  📄 {html_file.name}")
        
        print(f"\n🌐 Open pandas_tables_showcase.html in your browser to see all examples!")
        print("\n💡 Key Features Demonstrated:")
        print("  ✅ Team logos in tables (gt_nfl_logos equivalent)")
        print("  ✅ Player headshots (gt_nfl_headshots equivalent)")
        print("  ✅ Team wordmarks styling")
        print("  ✅ Advanced color theming with team colors")
        print("  ✅ Professional NFL styling")
        print("  ✅ Method chaining for complex customization")
        print("  ✅ HTML export for web dashboards")
        
    except Exception as e:
        print(f"\n❌ Error during execution: {e}")
        print("Make sure you have all required dependencies installed")
        return 1
        
    return 0

if __name__ == "__main__":
    exit(main())