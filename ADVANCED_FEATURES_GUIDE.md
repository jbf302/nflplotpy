# Advanced Features Guide - nflplotpy v2.0

This guide showcases the newest advanced features that achieve **full parity with R's nflplotR package**.

## 🎨 NFL Team Scale Functions

### Automatic Team Color Mapping
```python
import nflplotpy as nfl

# Basic team color mapping (equivalent to nflplotR's scale_color_nfl)
teams = ['BUF', 'MIA', 'NE', 'NYJ']
colors, legend_info = nfl.scale_color_nfl(data=teams)
plt.scatter(x, y, c=[colors[team] for team in teams])

# Use secondary colors
colors_sec, _ = nfl.scale_color_nfl(data=teams, color_type='secondary')

# Conference-based colors (AFC/NFC)
conf_colors, _ = nfl.scale_color_conference(data=teams)

# Division-based colors  
div_colors, _ = nfl.scale_color_division(data=teams)
```

### Color Scale Options
- `color_type`: `'primary'`, `'secondary'`, `'alt'`
- Automatic legend creation with team info
- Alpha transparency support
- Custom value mapping

## 🖼️ Generic Image Placement (geom_from_path equivalent)

### Place Any Image in Your Plots
```python
# Add image from URL or file path
nfl.add_image_from_path(
    ax, 
    image_url,           # URL or file path
    x=5, y=10,          # Position
    width=0.1,          # Size
    angle=45,           # Rotation
    colorize='#FF6B6B', # Color overlay
    alpha=0.8           # Transparency
)

# Common use cases
logo_url = nfl.AssetURLManager().get_logo_url('BUF')
nfl.add_image_from_path(ax, logo_url, x, y, width=0.08)
```

### Features
- **Rotation**: Any angle in degrees
- **Colorization**: Apply color overlays to images
- **Positioning**: Precise control with hjust/vjust
- **Transforms**: Support for coordinate transformations
- **Alpha blending**: Transparency controls

## 📊 Enhanced Reference Lines & Statistical Overlays

### Advanced Statistical Visualizations
```python
# Quantile lines (any percentiles)
nfl.add_quantile_lines(ax, data, [0.25, 0.5, 0.75], 
                      orientation='vertical')

# Mean lines with confidence bands
nfl.add_mean_lines(ax, x_data, y_data, 
                  confidence_band=True, method='trend')

# Reference bands for ranges
nfl.add_reference_band(ax, y_min, y_max, 
                      orientation='horizontal', alpha=0.3)

# Median lines
nfl.add_median_lines(ax, data, orientation='horizontal')
```

### Statistical Methods
- **Quantiles**: Any percentile combinations
- **Confidence bands**: Bootstrap or parametric
- **Trend analysis**: Linear, polynomial, or LOESS
- **Orientation**: Horizontal or vertical reference lines

## 🔄 Advanced Element Replacement

### Replace Plot Elements with NFL Logos
```python
# Custom logo-based legends
teams = ['BUF', 'MIA', 'NE']
nfl.create_logo_legend(ax, teams, 
                      labels=['Buffalo Bills', 'Miami Dolphins', 'New England Patriots'],
                      loc='upper right', logo_size=0.06)

# Replace axis labels with logos
for i, team in enumerate(teams):
    logo_url = nfl.AssetURLManager().get_logo_url(team)
    nfl.add_image_from_path(ax, logo_url, i, -2, width=0.08)
```

### Element Types
- **Legends**: Logo-based legends with custom positioning
- **Axis labels**: Replace text with team logos
- **Colorbar elements**: NFL-themed color scales
- **Facet labels**: Division/conference grouping

## 🏈 Conference & Division Analysis

### Team Organization Utilities
```python
# Get team information
conference = nfl.get_team_conference('BUF')  # Returns 'AFC'
division = nfl.get_team_division('BUF')      # Returns 'East'

# Get division rivals
rivals = nfl.get_division_rivals('BUF')      # ['MIA', 'NE', 'NYJ']

# Get teams by organization
afc_east = nfl.get_teams_by_division('AFC', 'East')
afc_teams = nfl.get_teams_by_conference('AFC')
```

### Analysis Functions
- **Division rivalry analysis**: Automatic rival identification
- **Conference comparisons**: AFC vs NFC grouping
- **Seasonal analysis**: Division standings and matchups
- **Geographic clustering**: Regional team groupings

## 🌐 Enhanced Plotly Integration

### Interactive NFL Visualizations
```python
# Create interactive team plots
fig = nfl.create_interactive_team_plot(
    df, 
    x_col='passing_yards',
    y_col='points', 
    team_col='team',
    hover_data=['rushing_yards', 'turnovers']
)

# Interactive bar charts with NFL styling
bar_fig = nfl.create_team_bar(
    df,
    x_col='team',
    y_col='points', 
    color_scale='primary'
)

# Apply NFL color scales to plotly
nfl.apply_nfl_color_scale_plotly(fig, teams)
```

### Interactive Features
- **Hover information**: Rich tooltips with team data
- **Logo integration**: Team logos in interactive plots  
- **Color consistency**: Matching matplotlib and plotly themes
- **Export options**: HTML, PNG, PDF output formats

## 🎯 Key Improvements Over Previous Versions

1. **Full nflplotR Parity**: All major nflplotR functions now available
2. **Enhanced Performance**: Optimized image loading and caching
3. **Cross-Backend Consistency**: Matplotlib and Plotly feature parity
4. **Advanced Statistics**: Comprehensive statistical overlay options
5. **Interactive Capabilities**: Rich plotly integration with NFL theming

## 📦 Function Count: 67+ Functions Available

The package now exports 67+ functions (up from ~20), providing comprehensive NFL data visualization capabilities across all major Python plotting backends.

### Quick Start Examples

```python
import nflplotpy as nfl
import matplotlib.pyplot as plt
import pandas as pd

# Sample data
teams = ['BUF', 'KC', 'SF', 'DAL'] 
points = [28, 31, 24, 21]

# Create NFL-styled plot with automatic colors
colors, _ = nfl.scale_color_nfl(data=teams)
plt.scatter(range(len(teams)), points, 
           c=[colors[team] for team in teams], s=200)

# Add team logos
for i, team in enumerate(teams):
    nfl.add_nfl_logo(plt.gca(), team, i, points[i] + 1, size=0.08)

# Add statistical overlays
nfl.add_mean_lines(plt.gca(), points, orientation='horizontal')
nfl.add_quantile_lines(plt.gca(), points, [0.25, 0.75], 
                      orientation='horizontal')

plt.show()
```

This represents a major milestone in achieving complete feature parity with the R nflplotR package while adding Python-specific enhancements.