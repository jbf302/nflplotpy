# nflplotpy Examples 🏈

Welcome to the nflplotpy examples directory! This collection of scripts demonstrates the full capabilities of nflplotpy, the Python equivalent of R's nflplotR package for NFL data visualization.

## 📋 Quick Start

1. **Install Requirements**
   ```bash
   pip install -e .  # Install nfl_data_py with nflplotpy
   ```

2. **Run Examples**
   ```bash
   # Comprehensive feature demo
   python nflplotpy_demo.py
   
   # Real NFL data examples with team logos
   python real_data_examples.py
   
   # Quick functionality test
   python quick_test.py
   ```

## 📊 Available Examples

### 🆕 **NEW: Advanced Headshots & Wordmarks Examples**

### 1. `qb_headshots_analysis.py` - 2024 QB Performance with Player Headshots
**What it demonstrates:**
- 👤 **Player Headshots**: Real ESPN player photos in plots
- 📊 **Advanced Analytics**: EPA vs Completion + YAC EPA analysis
- 🔍 **Player ID System**: Auto-detection of ESPN/GSIS IDs and names
- 📈 **Real Data**: 2024 NFL play-by-play data from nfl_data_py
- 🎯 **Interactive Elements**: Hover-style annotations and quadrant analysis

**Key Features:**
- X-axis: Total average offensive EPA per game
- Y-axis: Completion + YAC EPA (how much EPA comes from after-the-catch)
- Player headshots displayed at each quarterback's performance point
- Median reference lines for league context
- Top performers highlighted in elite efficiency quadrant

**Output File:** `2024_qb_headshots_analysis.png`

### 2. `team_wordmarks_matplotlib.py` - Team Performance with Wordmarks
**What it demonstrates:**
- 🏷️ **Team Wordmarks**: Official nflverse wordmark images on x-axis
- 📊 **Performance Metrics**: 2024 Net Points per Win analysis  
- 🎨 **Team Colors**: Bars colored with official team colors
- 📈 **Statistical Context**: Median lines and performance annotations
- 🏆 **Rankings**: Automatic sorting by performance

**Key Features:**
- Team wordmarks replace traditional x-axis text labels
- Net Points per Win shows scoring efficiency relative to wins
- Top/bottom performer annotations with team highlights
- Professional NFL styling with reference lines

**Output File:** `2024_team_wordmarks_matplotlib.png`

### 3. `interactive_team_wordmarks.py` - Multi-Year Interactive Analysis
**What it demonstrates:**
- 🎮 **Interactive Plotly**: Multi-year slider and animation controls
- 📅 **Time Series**: 2019-2024 team performance data
- 🔄 **Animation**: Play button to animate through seasons
- 💡 **Rich Tooltips**: Detailed hover information with team stats
- 🎨 **Team Colors**: Dynamic coloring based on official team palettes

**Key Features:**
- Year slider to explore different NFL seasons
- Animated transitions between years
- Comprehensive hover details (wins, losses, points, net points)
- Teams sorted by performance within each season
- Export to interactive HTML file

**Output File:** `interactive_team_wordmarks.html`

---

### 4. `nflplotpy_demo.py` - Complete Feature Showcase

**What it demonstrates:**
- 🎨 **Team Colors**: Official NFL color palettes
- 🏟️ **Team Organization**: Conference/division groupings  
- 💾 **Asset Management**: Logo caching system
- 📊 **Matplotlib Integration**: Dots vs logos comparison
- 🚀 **High-Level Functions**: One-line plotting with `plot_team_stats()`
- 🎯 **Color Palettes**: Advanced color management
- 📈 **Real Data Integration**: Using nfl_data_py for authentic data

**Key Features:**
- Side-by-side comparison of traditional dots vs modern team logos
- Proper User-Agent handling for logo downloads
- Professional NFL styling and themes
- Reference lines for statistical context

**Output Files:**
- `matplotlib_integration_demo.png`
- `high_level_team_plot.png`
- `real_data_demo.png` (if internet available)

### 2. `real_data_examples.py` - Authentic NFL Analytics

**What it demonstrates:**
- 📊 **Real 2024 NFL Data**: Live play-by-play analysis
- 🏈 **Team Logos**: All plots use actual team logos instead of dots
- 📈 **EPA Analysis**: Expected Points Added per play metrics
- 🏆 **Multiple Views**: All teams, divisions, conferences
- 🎯 **Statistical Context**: Reference lines and quadrant analysis

**Key Metrics:**
- Offensive EPA per play
- Defensive EPA per play allowed  
- Team performance quadrants
- Division and conference comparisons

**Output Files:**
- `2024_real_all_teams_epa.png` - All 32 teams overview
- `2024_real_divisions_epa.png` - 8 division breakdown
- `2024_real_conferences_epa.png` - AFC vs NFC comparison

### 3. `quick_test.py` - Fast Functionality Check

**What it demonstrates:**
- ⚡ **Quick Setup Test**: Verify installation
- 🎨 **Basic Colors**: Simple color retrieval
- 🏈 **Logo Loading**: Test logo download system
- ✅ **System Check**: Validate all components work

## 🔑 Key Features Explained

### Team Logos vs Dots

**Traditional Approach (Dots):**
```python
# Old way - colored dots with team labels
colors = nflplot.get_team_colors(teams, 'primary')
ax.scatter(x, y, c=colors, s=200)
```

**Modern Approach (Logos):**
```python  
# New way - actual team logos
ax.scatter(x, y, c='white', s=1, alpha=0.01)  # Invisible positioning
add_nfl_logos(ax, teams, x, y, width=0.15)    # Add logos
```

### High-Level Function

The easiest way to create NFL plots:

```python
fig = nflplot.plot_team_stats(
    data,
    x='offensive_epa', 
    y='defensive_epa',
    show_logos=True,  # 🔑 Enable team logos
    add_reference_lines=True,
    title='Team Performance Analysis'
)
```

### Logo System Features

- ✅ **35+ working team logos** from official nflverse data
- 💾 **Automatic caching** for fast subsequent use
- 🔄 **Fallback system** gracefully handles failed downloads
- 📏 **Adjustable sizing** with `width` parameter
- 🎯 **Professional quality** suitable for presentations

## 🛠️ Customization

### Logo Sizes
```python
width=0.08   # Small logos
width=0.12   # Medium logos (default)
width=0.18   # Large logos
```

### Reference Lines
```python
add_reference_lines=True,
reference_type='median'  # or 'mean' or 'both'
```

### NFL Themes
```python
nflplot.apply_nfl_theme(ax, style='default')  # or 'minimal'
```

## 📋 Common Use Cases

1. **Team Performance Analysis**
   - EPA efficiency plots
   - Win rate comparisons
   - Offensive vs defensive metrics

2. **Division/Conference Breakdowns**
   - Comparing teams within divisions
   - AFC vs NFC analysis
   - Playoff race visualizations

3. **Season Tracking**
   - Week-by-week progression
   - Trend analysis
   - Performance correlation studies

## 🔍 Troubleshooting

### Logo Issues
If logos aren't loading:
1. Check internet connection
2. Verify User-Agent headers are working
3. Look for fallback to colored dots
4. Check cache directory permissions

### Data Issues  
If real data examples fail:
1. Ensure `nfl_data_py` is installed
2. Check internet connection for data download
3. Verify year parameter (2024 data availability)

### Import Issues
```python
# Make sure path is set correctly
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
```

## 🎯 Next Steps

1. **Modify Examples**: Edit the scripts to use your own data
2. **Create Custom Plots**: Use `plot_team_stats()` with your metrics
3. **Explore Colors**: Try different team color combinations
4. **Add Reference Lines**: Use median/mean lines for context
5. **Export High-DPI**: Save plots with `dpi=300` for presentations

## 📚 Documentation

- **Package Documentation**: See parent directory README files
- **Function Documentation**: All functions have detailed docstrings
- **nfl_data_py Integration**: Check nfl_data_py documentation for data options
- **Matplotlib Integration**: Standard matplotlib customization applies

---

**Happy plotting! 🏈📊**

*Questions? Check the test files in `nflplotpy/tests/` for more code examples.*