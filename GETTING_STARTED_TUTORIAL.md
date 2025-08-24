# Getting Started with nflplotpy 🏈

**A Step-by-Step Tutorial for NFL Data Visualization in Python**

Welcome to nflplotpy! This tutorial will guide you from installation to creating professional NFL visualizations in just a few minutes.

---

## 🎯 What You'll Learn

By the end of this tutorial, you'll know how to:
1. Install and set up nflplotpy
2. Create your first plot with NFL team logos
3. Make professional NFL-themed tables
4. Add statistical overlays and reference lines
5. Create interactive visualizations
6. Export your work for presentations

**Estimated time: 15 minutes**

---

## 📦 Step 1: Installation

### Basic Installation
```bash
pip install nflplotpy
```

### Full Installation (Recommended)
```bash
pip install nflplotpy[all]
```
This includes plotly for interactive charts and nfl_data_py for real NFL data.

### Verify Installation
```python
import nflplotpy as nfl
nfl.nfl_sitrep()  # Shows system info and available features
```

---

## 🚀 Step 2: Your First NFL Plot

Let's create a simple scatter plot with NFL team logos:

```python
import nflplotpy as nfl
import matplotlib.pyplot as plt
import pandas as pd

# Create sample data
teams = ['KC', 'BUF', 'SF', 'DAL']
offense_scores = [28.5, 26.8, 25.1, 24.2]
defense_scores = [8.2, 7.9, 12.4, 15.6]

# Create the plot
fig, ax = plt.subplots(figsize=(10, 8))

# Add team logos instead of dots
nfl.add_nfl_logos(ax, teams, offense_scores, defense_scores, width=0.12)

# Styling
ax.set_xlabel('Offensive EPA per Game')
ax.set_ylabel('Defensive EPA Allowed per Game')
ax.set_title('Team Performance Analysis with NFL Logos', fontsize=16, fontweight='bold')

# Add reference lines
ax.axhline(y=10, color='gray', linestyle='--', alpha=0.7, label='League Average Defense')
ax.axvline(x=25, color='gray', linestyle='--', alpha=0.7, label='League Average Offense')

plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()
plt.show()
```

**🎉 Congratulations!** You just created your first NFL visualization with team logos!

---

## 📊 Step 3: Using Team Colors (nflplotR Style)

Now let's add automatic team color mapping, just like R's nflplotR:

```python
# Get automatic team colors
colors, legend_info = nfl.scale_color_nfl(teams, color_type='primary')

# Create scatter plot with team colors
fig, ax = plt.subplots(figsize=(10, 8))

# Plot with team colors
for team, x, y in zip(teams, offense_scores, defense_scores):
    ax.scatter(x, y, c=colors[team], s=300, alpha=0.8, 
              edgecolor='white', linewidth=2, label=team)

# Add team logos on top
nfl.add_nfl_logos(ax, teams, offense_scores, defense_scores, width=0.08)

ax.set_xlabel('Offensive EPA per Game')
ax.set_ylabel('Defensive EPA Allowed per Game') 
ax.set_title('Team Colors + Logos Visualization')
ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()
```

---

## 🏈 Step 4: Conference and Division Analysis

Let's explore team organization features:

```python
# Analyze the AFC West division
afc_west_teams = nfl.get_teams_by_division('AFC', 'West')
print(f"AFC West teams: {afc_west_teams}")

# Get division rivals
kc_rivals = nfl.get_division_rivals('KC')
print(f"KC rivals: {kc_rivals}")

# Color by conference
all_teams = ['KC', 'BUF', 'SF', 'DAL', 'GB', 'TB']
conf_colors, _ = nfl.scale_color_conference(all_teams)

fig, ax = plt.subplots(figsize=(12, 8))

# Sample data for all teams
x_data = [28.5, 26.8, 25.1, 24.2, 23.8, 22.9]
y_data = [8.2, 7.9, 12.4, 15.6, 11.2, 13.8]

# Plot by conference colors
ax.scatter(x_data, y_data, c=[conf_colors[t] for t in all_teams], 
           s=400, alpha=0.7, edgecolor='white', linewidth=2)

# Add team logos
nfl.add_nfl_logos(ax, all_teams, x_data, y_data, width=0.1)

ax.set_title('AFC vs NFC Team Performance')
ax.set_xlabel('Offensive EPA')
ax.set_ylabel('Defensive EPA Allowed')

# Add conference legend
ax.scatter([], [], c=conf_colors['KC'], label='AFC', s=200, alpha=0.7)
ax.scatter([], [], c=conf_colors['SF'], label='NFC', s=200, alpha=0.7)
ax.legend()

plt.tight_layout()
plt.show()
```

---

## 📋 Step 5: Professional NFL Tables

Now let's create beautiful NFL tables with pandas integration:

```python
# Create sample standings data
standings_data = pd.DataFrame({
    'team': ['KC', 'BUF', 'SF', 'DAL', 'GB', 'TB'],
    'wins': [14, 13, 12, 12, 9, 9],
    'losses': [3, 4, 5, 5, 8, 8],
    'points_for': [456, 482, 421, 396, 369, 348],
    'points_against': [284, 298, 298, 352, 379, 365]
})

# Method 1: Quick logo table
styled_table = nfl.style_with_logos(standings_data, 'team', logo_height=30)
styled_table.to_html('nfl_standings.html')
print("✅ Saved NFL standings table with logos!")

# Method 2: Advanced table with colors and styling
advanced_table = nfl.create_nfl_table(
    standings_data,
    team_column='team',
    logo_columns=['team'],
    color_columns=['wins'],  # Color wins column by team colors
    title='2024 NFL Standings'
)
advanced_table.save_html('advanced_standings.html')
print("✅ Saved advanced NFL table!")

# Method 3: Custom styling with method chaining
custom_table = (nfl.NFLTableStyler(standings_data)
    .with_team_logos('team', logo_height=25)
    .with_team_colors(['points_for', 'points_against'], 'team', 
                     color_type='primary', apply_to='background')
    .with_nfl_theme(alternating_rows=True)
)
custom_table.save_html('custom_nfl_table.html')
print("✅ Saved custom styled table!")
```

### View Your Tables
Open the generated HTML files in your web browser to see beautiful NFL tables with:
- ✅ Team logos replacing abbreviations
- 🎨 Team colors as backgrounds
- 📊 Professional NFL styling
- 📱 Mobile-responsive design

---

## 📈 Step 6: Statistical Overlays

Add professional statistical analysis to your plots:

```python
# Sample performance data
perf_data = [28.5, 26.8, 25.1, 24.2, 23.8, 22.9, 21.1, 20.8, 19.5, 18.2]
teams_10 = ['KC', 'BUF', 'SF', 'DAL', 'GB', 'TB', 'MIA', 'DET', 'BAL', 'CIN']

fig, ax = plt.subplots(figsize=(14, 8))

# Create bar chart
bars = ax.bar(range(len(teams_10)), perf_data, alpha=0.7)

# Color bars by team colors
colors, _ = nfl.scale_color_nfl(teams_10)
for bar, team in zip(bars, teams_10):
    bar.set_color(colors[team])

# Add statistical overlays
nfl.add_mean_lines(ax, perf_data, orientation='horizontal', 
                  color='red', linewidth=2, linestyle='-', 
                  label='League Average')

nfl.add_quantile_lines(ax, perf_data, quantiles=[0.25, 0.75], 
                      orientation='horizontal', 
                      color='orange', linewidth=1, linestyle='--',
                      alpha=0.8)

# Replace x-axis labels with team logos
ax.set_xticks(range(len(teams_10)))
ax.set_xticklabels([])  # Remove text labels

# Add team logos as x-axis labels  
for i, team in enumerate(teams_10):
    nfl.add_nfl_logo(ax, team, i, -2, width=0.08)

ax.set_ylim(-4, max(perf_data) * 1.1)
ax.set_ylabel('Team Performance Score')
ax.set_title('NFL Team Performance with Statistical Context', fontsize=16)
ax.legend()
ax.grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.show()
```

---

## 🌐 Step 7: Interactive Visualizations

Create interactive plotly charts:

```python
# Create interactive data
interactive_data = pd.DataFrame({
    'team': teams_10,
    'offense_epa': [0.15, 0.12, 0.08, 0.05, 0.02, 0.01, -0.01, -0.03, -0.05, -0.08],
    'defense_epa': [-0.10, -0.08, -0.05, -0.02, 0.01, 0.03, 0.05, 0.07, 0.08, 0.10],
    'wins': [14, 13, 12, 12, 9, 9, 8, 8, 7, 6],
    'point_diff': [172, 184, 123, 44, -10, -17, -28, -45, -67, -89]
})

# Create interactive plot
fig = nfl.create_interactive_team_plot(
    interactive_data,
    x_col='offense_epa',
    y_col='defense_epa', 
    team_col='team',
    title='Interactive NFL Team Performance Analysis',
    hover_data=['wins', 'point_diff']
)

# Add reference lines
fig.add_hline(y=0, line_dash="dash", line_color="gray", opacity=0.7)
fig.add_vline(x=0, line_dash="dash", line_color="gray", opacity=0.7)

# Show interactive plot
fig.show()

# Save for sharing
fig.write_html('interactive_nfl_analysis.html')
print("✅ Saved interactive NFL analysis!")
```

---

## 🎨 Step 8: Player Analysis with Headshots

Let's add player headshots to our analysis:

```python
# Sample QB data (you can use real data with nfl_data_py)
qb_data = pd.DataFrame({
    'player': ['Patrick Mahomes', 'Josh Allen', 'Joe Burrow'],
    'team': ['KC', 'BUF', 'CIN'],
    'passing_epa': [0.15, 0.12, 0.08],
    'completion_pct': [67.2, 63.1, 66.8]
})

# Create table with player headshots
headshot_table = nfl.style_with_headshots(
    qb_data, 
    'player',           # Column with player names
    headshot_height=40, # Size of headshots
    id_type='auto'      # Auto-detect ID type
)

headshot_table.to_html('qb_analysis.html')
print("✅ Saved QB analysis table with headshots!")

# Create plot version (using logos for teams)
fig, ax = plt.subplots(figsize=(10, 8))

ax.scatter(qb_data['passing_epa'], qb_data['completion_pct'], 
          s=500, alpha=0.7, c='lightblue', edgecolor='navy', linewidth=2)

# Add team logos at QB positions
nfl.add_nfl_logos(ax, qb_data['team'], qb_data['passing_epa'], 
                  qb_data['completion_pct'], width=0.1)

# Add player labels
for _, row in qb_data.iterrows():
    ax.annotate(row['player'], 
                (row['passing_epa'], row['completion_pct']),
                xytext=(10, 10), textcoords='offset points',
                fontsize=10, fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.8))

ax.set_xlabel('Passing EPA per Play')
ax.set_ylabel('Completion Percentage')
ax.set_title('Top NFL Quarterbacks Analysis', fontsize=16)
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()
```

---

## 🎯 Quick Reference Cheat Sheet

### Essential Functions
```python
# Logos and images
nfl.add_nfl_logo(ax, 'KC', x, y, width=0.1)
nfl.add_nfl_logos(ax, teams, x_list, y_list)
nfl.add_nfl_headshots(ax, players, x_list, y_list)

# Colors (nflplotR equivalent)
colors, _ = nfl.scale_color_nfl(teams)
conf_colors, _ = nfl.scale_color_conference(teams)

# Tables
nfl.style_with_logos(df, 'team_column')
nfl.create_nfl_table(df, team_column='team')

# Interactive plots
nfl.create_interactive_team_plot(df, 'x_col', 'y_col', 'team_col')

# Statistical overlays
nfl.add_mean_lines(ax, data)
nfl.add_quantile_lines(ax, data, [0.25, 0.75])

# Team info
nfl.get_team_conference('KC')  # 'AFC'
nfl.get_division_rivals('KC')  # ['LV', 'LAC', 'DEN']
```

### Common Patterns
```python
# 1. Logo scatter plot
fig, ax = plt.subplots()
nfl.add_nfl_logos(ax, teams, x, y, width=0.1)

# 2. Team-colored bars  
colors, _ = nfl.scale_color_nfl(teams)
ax.bar(x, y, color=[colors[t] for t in teams])

# 3. Professional table
table = nfl.create_nfl_table(df, team_column='team')
table.save_html('output.html')

# 4. Interactive analysis
fig = nfl.create_interactive_team_plot(df, 'x', 'y', 'team')
fig.show()
```

---

## 🚀 Next Steps

Now that you've mastered the basics, try these advanced features:

1. **Real NFL Data**: Install `nfl_data_py` and use actual game data
2. **Advanced Styling**: Explore custom color palettes and themes  
3. **Complex Tables**: Combine logos, headshots, and wordmarks
4. **Statistical Analysis**: Add regression lines and confidence bands
5. **Custom Assets**: Use your own images with `add_image_from_path()`

### Recommended Learning Path
1. ✅ Complete this tutorial
2. 📊 Run examples in `examples/` directory
3. 📖 Read `API_DOCUMENTATION.md` for complete reference
4. 🔧 Check `ADVANCED_FEATURES_GUIDE.md` for complex use cases
5. 🏈 Build your own NFL analysis project!

---

## ❓ Getting Help

- **Documentation**: `API_DOCUMENTATION.md` - Complete function reference
- **Examples**: `examples/` directory - Real working code
- **Issues**: GitHub repository - Report bugs and get help
- **Features**: All 63+ functions provide complete nflplotR parity

**Happy NFL plotting! 🏈📊**