# nflplotpy API Documentation

**Complete API Reference for NFL Data Visualization in Python**

This document provides comprehensive documentation for all functions and classes in nflplotpy, organized by functionality.

---

## 📋 Table of Contents

- [Installation & Setup](#installation--setup)
- [Core Functions](#core-functions)
- [Matplotlib Integration](#matplotlib-integration)
- [Plotly Integration](#plotly-integration)
- [Pandas Table Styling](#pandas-table-styling)
- [Color Management](#color-management)
- [Asset Management](#asset-management)
- [Utility Functions](#utility-functions)
- [Configuration](#configuration)

---

## 🔧 Installation & Setup

### Basic Installation
```bash
pip install nflplotpy
```

### With Optional Dependencies
```bash
# For plotly support
pip install nflplotpy[plotly]

# For seaborn integration  
pip install nflplotpy[seaborn]

# For nfl_data_py integration
pip install nflplotpy[nfldata]

# Install everything
pip install nflplotpy[all]
```

### Basic Usage
```python
import nflplotpy as nfl
import matplotlib.pyplot as plt
import pandas as pd

# Ready to create NFL visualizations!
```

---

## 🏈 Core Functions

### Logo and Image Management

#### `add_nfl_logo(ax, team, x, y, width=0.1, alpha=1.0, **kwargs)`
Add a single NFL team logo to matplotlib plot.

**Parameters:**
- `ax` (matplotlib.Axes): The axes to add logo to
- `team` (str): Team abbreviation (e.g., 'KC', 'BUF')  
- `x` (float): X coordinate for logo placement
- `y` (float): Y coordinate for logo placement
- `width` (float): Logo width in axes coordinates
- `alpha` (float): Transparency (0-1)

**Returns:** `AnnotationBbox` object

**Example:**
```python
fig, ax = plt.subplots()
nfl.add_nfl_logo(ax, 'KC', 0.5, 0.5, width=0.15)
plt.show()
```

#### `add_nfl_logos(ax, teams, x, y, width=0.1, alpha=1.0, **kwargs)`
Add multiple NFL team logos to matplotlib plot.

**Parameters:**
- `teams` (list): List of team abbreviations
- `x` (list): X coordinates for each logo
- `y` (list): Y coordinates for each logo
- Other parameters same as `add_nfl_logo()`

**Example:**
```python
teams = ['KC', 'BUF', 'CIN']
x_pos = [0.2, 0.5, 0.8]  
y_pos = [0.3, 0.7, 0.4]
nfl.add_nfl_logos(ax, teams, x_pos, y_pos, width=0.1)
```

#### `add_nfl_headshots(ax, player_ids, x, y, width=0.1, id_type='auto', **kwargs)`
Add NFL player headshots to matplotlib plot.

**Parameters:**
- `player_ids` (list): Player identifiers (names, ESPN IDs, GSIS IDs)
- `id_type` (str): Type of identifier ('espn', 'gsis', 'name', 'auto')
- Other parameters same as logo functions

**Example:**
```python
# Using player names
players = ['Patrick Mahomes', 'Josh Allen']
x_pos = [0.3, 0.7]
y_pos = [0.5, 0.5] 
nfl.add_nfl_headshots(ax, players, x_pos, y_pos, width=0.12)
```

---

## 📊 Matplotlib Integration

### Advanced Plotting Functions

#### `add_image_from_path(ax, path, x, y, width=0.1, height=None, **kwargs)`
Add any image from URL or file path to matplotlib plot. **Equivalent to nflplotR's `geom_from_path()`**.

**Parameters:**
- `path` (str): URL or file path to image
- `x, y` (float): Position coordinates  
- `width` (float): Image width
- `height` (float, optional): Image height (maintains aspect ratio if None)
- `angle` (float): Rotation angle in degrees
- `colorize` (str, optional): Color overlay (hex code)
- `alpha` (float): Transparency

**Example:**
```python
# Add image with rotation and colorization
nfl.add_image_from_path(ax, 'https://example.com/logo.png', 
                       x=0.5, y=0.5, width=0.1, 
                       angle=45, colorize='#FF0000')
```

### Scale Functions (nflplotR Equivalents)

#### `scale_color_nfl(data=None, color_type='primary', guide=True, **kwargs)`
Create NFL team color scale mapping. **Equivalent to nflplotR's `scale_color_nfl()`**.

**Parameters:**
- `data` (list): List of team abbreviations
- `color_type` (str): 'primary', 'secondary', or 'alt'  
- `guide` (bool): Whether to include legend information
- `alpha` (float): Color transparency

**Returns:** `(colors_dict, legend_info)` tuple

**Example:**
```python
teams = ['KC', 'BUF', 'NE', 'MIA']
colors, legend = nfl.scale_color_nfl(teams, color_type='primary')

# Use in scatter plot
plt.scatter(x_data, y_data, c=[colors[team] for team in teams])
```

#### `scale_color_conference(data, guide=True, **kwargs)`
Color teams by conference (AFC/NFC).

**Example:**
```python
colors, _ = nfl.scale_color_conference(['KC', 'SF', 'BUF', 'DAL'])
# AFC teams get one color, NFC teams get another
```

#### `scale_color_division(data, guide=True, **kwargs)`
Color teams by division.

### Statistical Reference Lines

#### `add_mean_lines(ax, data, orientation='both', confidence_band=False, **kwargs)`
Add mean reference lines with optional confidence bands.

**Parameters:**
- `data` (array-like): Data for calculating mean
- `orientation` (str): 'horizontal', 'vertical', or 'both'
- `confidence_band` (bool): Add confidence interval shading
- `method` (str): 'simple' or 'trend' for trend line

#### `add_quantile_lines(ax, data, quantiles=[0.25, 0.75], **kwargs)`
Add quantile reference lines.

**Example:**
```python
# Add quartile lines
nfl.add_quantile_lines(ax, data, quantiles=[0.25, 0.5, 0.75])
```

#### `add_reference_band(ax, lower, upper, orientation='horizontal', **kwargs)`
Add reference band between two values.

### Element Replacement

#### `create_logo_legend(ax, teams, labels=None, loc='best', logo_size=0.06, **kwargs)`
Create custom legend using team logos instead of color patches.

**Example:**
```python
teams = ['KC', 'BUF', 'CIN']
labels = ['Kansas City Chiefs', 'Buffalo Bills', 'Cincinnati Bengals']
nfl.create_logo_legend(ax, teams, labels, loc='upper right')
```

---

## 🌐 Plotly Integration

### Interactive Plotting

#### `create_interactive_team_plot(df, x_col, y_col, team_col, title=None, **kwargs)`
Create interactive plotly scatter plot with team logos and hover data.

**Parameters:**
- `df` (DataFrame): Data containing team information
- `x_col, y_col` (str): Column names for x and y axes
- `team_col` (str): Column containing team abbreviations
- `hover_data` (list): Additional columns to show on hover
- `show_logos` (bool): Whether to show team logos as points

**Example:**
```python
df = pd.DataFrame({
    'team': ['KC', 'BUF', 'CIN'],
    'offense_epa': [0.15, 0.12, 0.08], 
    'defense_epa': [-0.10, -0.08, -0.05]
})

fig = nfl.create_interactive_team_plot(
    df, 'offense_epa', 'defense_epa', 'team',
    title='Team EPA Analysis',
    hover_data=['wins', 'losses']
)
fig.show()
```

#### `add_nfl_logo_trace(fig, team, x, y, size=0.1, opacity=1.0)`
Add team logo to plotly figure.

#### `apply_nfl_color_scale_plotly(fig, teams, scale_type='team', **kwargs)`
Apply NFL color scales to plotly traces.

---

## 📋 Pandas Table Styling

### Quick Start Functions

#### `style_with_logos(df, team_columns, logo_height=25, replace_text=True)`
Add team logos to DataFrame columns. **Equivalent to R's `gt_nfl_logos()`**.

**Example:**
```python
standings = pd.DataFrame({
    'team': ['KC', 'BUF', 'CIN'],
    'wins': [14, 13, 12],
    'losses': [3, 4, 5]
})

# Create table with logos
styled = nfl.style_with_logos(standings, 'team')
styled.to_html('standings.html')
```

#### `style_with_headshots(df, player_columns, headshot_height=30, id_type='auto')`
Add player headshots to DataFrame. **Equivalent to R's `gt_nfl_headshots()`**.

**Example:**
```python
qb_stats = pd.DataFrame({
    'player': ['Patrick Mahomes', 'Josh Allen', 'Joe Burrow'],
    'team': ['KC', 'BUF', 'CIN'],
    'passing_yards': [4183, 4306, 3446]
})

styled = nfl.style_with_headshots(qb_stats, 'player')
```

#### `style_with_wordmarks(df, team_columns, wordmark_height=20)`
Add team wordmarks to DataFrame columns.

### Advanced Table Styling

#### `create_nfl_table(df, team_column=None, logo_columns=None, color_columns=None, title=None)`
Create comprehensive NFL-styled table with logos, colors, and professional styling.

**Example:**
```python
table = nfl.create_nfl_table(
    standings,
    team_column='team',
    logo_columns=['team'],
    color_columns=['wins'],
    title='2024 NFL Standings'
)
table.save_html('standings.html')
```

### NFLTableStyler Class

For advanced customization, use the `NFLTableStyler` class with method chaining:

```python
styler = nfl.NFLTableStyler(df)
table = (styler
    .with_team_logos('team', logo_height=30)
    .with_team_colors(['wins', 'losses'], 'team', apply_to='background')
    .with_nfl_theme(alternating_rows=True)
)
table.save_html('custom_table.html')
```

**Methods:**
- `.with_team_logos(columns, logo_height=25, replace_text=True)`
- `.with_team_colors(columns, team_column, color_type='primary', apply_to='background')`
- `.with_nfl_theme(alternating_rows=True, header_style='default')`
- `.to_html(**kwargs)` - Export to HTML string
- `.save_html(filename, **kwargs)` - Save to HTML file

---

## 🎨 Color Management

### Team Colors

#### `get_team_colors(teams, color_type='primary')`
Get team colors for multiple teams.

**Parameters:**
- `teams` (list): Team abbreviations
- `color_type` (str): 'primary', 'secondary', 'alt'

**Returns:** List of color hex codes

#### `create_nfl_colormap(teams=None, color_type='primary')`
Create matplotlib colormap from team colors.

### Color Palettes

#### `NFLColorPalette()`
Advanced color palette management class.

**Methods:**
- `.get_team_palette(team, n_colors=5)` - Get color palette for team
- `.create_gradient(team1, team2, n_colors=10)` - Gradient between teams
- `.get_division_palette(conference, division)` - Colors for division teams

---

## 🔧 Asset Management

### URLs and Downloads

#### `AssetURLManager()`
Manages URLs for all NFL assets.

**Methods:**
- `.get_logo_url(team)` - Get team logo URL
- `.get_wordmark_url(team)` - Get team wordmark URL  
- `.get_player_headshot_urls(player_id, id_type='auto')` - Get headshot URLs

#### `get_team_logo(team, cache=True)`
Download and cache team logo as PIL Image.

**Parameters:**
- `team` (str): Team abbreviation
- `cache` (bool): Whether to use local caching

**Returns:** PIL Image object

---

## 🛠️ Utility Functions

### Team Information

#### `get_team_conference(team)`
Get team's conference ('AFC' or 'NFC').

#### `get_team_division(team)`
Get team's division ('East', 'West', 'North', 'South').

#### `get_division_rivals(team)`
Get list of division rival teams.

**Example:**
```python
rivals = nfl.get_division_rivals('KC')  # ['LV', 'LAC', 'DEN']
```

#### `get_teams_by_conference(conference)`
Get all teams in a conference.

#### `get_teams_by_division(conference, division)`
Get all teams in a specific division.

**Example:**
```python
afc_west = nfl.get_teams_by_division('AFC', 'West')
# Returns: ['KC', 'LV', 'LAC', 'DEN']
```

### Validation

#### `validate_teams(teams)`
Validate team abbreviations and suggest corrections.

#### `get_available_teams()`
Get list of all valid team abbreviations.

---

## ⚙️ Configuration

### Environment Setup

#### `nfl_sitrep()`
Display system information and package status.

```python
nfl.nfl_sitrep()
# Shows: Python version, package versions, available features
```

### Player ID Management

#### Enhanced player ID support with `nfl_data_py` integration:
- Automatic ID type detection
- Fuzzy name matching  
- Cross-reference between ESPN, GSIS, and NFL IDs
- Graceful fallbacks when external data unavailable

---

## 📊 Function Summary by Category

### Core Visualization (13 functions)
- `add_nfl_logo`, `add_nfl_logos`, `add_nfl_headshots`
- `add_image_from_path`, `create_logo_legend`
- Matplotlib and Plotly integration functions

### Scale & Color Functions (8 functions) 
- `scale_color_nfl`, `scale_color_conference`, `scale_color_division`
- `get_team_colors`, `create_nfl_colormap`
- Color palette management

### Statistical Overlays (6 functions)
- `add_mean_lines`, `add_quantile_lines`, `add_reference_band`
- `add_median_lines`, `add_percentile_lines`

### Pandas Integration (5 functions)
- `style_with_logos`, `style_with_headshots`, `style_with_wordmarks`
- `create_nfl_table`, `NFLTableStyler` class

### Team Utilities (12 functions)
- Conference/division functions, team validation
- Asset URL management, team information lookup

### Interactive Features (8 functions)
- Plotly integration, interactive plots
- Enhanced hover information, logo traces

### Advanced Features (11 functions)
- Element replacement, custom styling
- Image transformations, statistical analysis

**Total: 63+ exported functions providing complete nflplotR parity**

---

## 🎯 Quick Reference

### Most Common Use Cases

**1. Simple Logo Scatter Plot:**
```python
fig, ax = plt.subplots()
teams = ['KC', 'BUF', 'CIN']
x, y = [1, 2, 3], [10, 15, 12]
nfl.add_nfl_logos(ax, teams, x, y, width=0.1)
```

**2. Colored by Conference:**
```python
colors, _ = nfl.scale_color_conference(teams)
plt.scatter(x, y, c=[colors[t] for t in teams])
```

**3. Professional Table:**
```python
table = nfl.create_nfl_table(df, team_column='team', title='NFL Stats')
table.save_html('report.html')
```

**4. Interactive Plot:**
```python
fig = nfl.create_interactive_team_plot(df, 'x_col', 'y_col', 'team')
fig.show()
```

---

## 🔗 Additional Resources

- **Examples**: See `examples/` directory for comprehensive usage examples
- **Advanced Guide**: `ADVANCED_FEATURES_GUIDE.md` for complex visualizations
- **GitHub**: [nflplotpy repository](https://github.com/joelfeinberg/nflplotpy) for latest updates
- **Issues**: Report bugs and request features on GitHub

This documentation covers all 63+ functions available in nflplotpy v2.0, providing complete feature parity with R's nflplotR package plus additional Python-specific enhancements.