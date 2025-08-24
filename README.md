# nflplotpy

**Python NFL Visualization Package - Complete nflplotR Equivalent**

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/release/python-380/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

nflplotpy is a comprehensive Python visualization package for NFL data analysis, providing complete feature parity with R's popular `nflplotR` package. Built for the NFL analytics community, it seamlessly integrates with matplotlib, plotly, seaborn, and pandas to create stunning NFL-themed visualizations.

*Inspired by and building upon the amazing work of the nflverse ecosystem and nflplotR package.*

## 🚀 Quick Start

```bash
pip install nflplotpy
```

```python
import nflplotpy as nflplot
import matplotlib.pyplot as plt
import pandas as pd

# Create a simple team performance scatter plot
fig, ax = plt.subplots(figsize=(12, 8))

# Add team logos at coordinates
nflplot.add_nfl_logo(ax, 'KC', x=0.5, y=0.5, width=0.1)
nflplot.add_nfl_logo(ax, 'BUF', x=0.3, y=0.7, width=0.1)

# Apply NFL theme
nflplot.apply_nfl_theme(ax, team='KC')
plt.show()
```

## 🖼️ Gallery & Examples

### Team Performance Analysis with Real NFL Data

<div align="center">

**All Teams EPA Analysis**  
![All Teams EPA](examples/2024_all_teams_epa.png)

**Division Breakdown**  
![Division Breakdown](examples/2024_divisions_epa.png)

*Examples using real 2024 NFL Expected Points Added (EPA) data with team logos*

</div>

### 📚 **Comprehensive Examples Available**

Check out our [examples directory](examples/) for detailed code and documentation:

- **[`nfl_examples.py`](examples/nfl_examples.py)**: Real 2024 NFL data analysis with team logos
- **[`nflplotpy_demo.py`](examples/nflplotpy_demo.py)**: Complete feature demonstrations  
- **[`table_examples.py`](examples/table_examples.py)**: NFL table styling examples
- **[`quick_test.py`](examples/quick_test.py)**: Quick functionality verification

➤ **[View Full Examples Documentation](examples/README.md)** for detailed tutorials and customization guides.

## ✨ Core Features

### 🎨 **Team Colors & Branding**
```python
# Get team colors
nflplot.get_team_colors('KC', 'primary')  # '#e31837'
nflplot.get_team_colors(['KC', 'BUF', 'GB'])  # Multiple teams

# Create color palettes
palette = nflplot.NFLColorPalette()
afc_colors = palette.create_conference_palette('AFC')
gradient = palette.create_gradient('KC', 'SF', n_colors=10)
```

### 🏈 **NFL Elements**
```python
import matplotlib.pyplot as plt

fig, ax = plt.subplots()

# Add team logos
nflplot.add_nfl_logo(ax, 'KC', x=0.5, y=0.5, width=0.1)

# 🆕 Add team wordmarks  
nflplot.add_team_wordmark(ax, 'KC', x=0.3, y=0.8, width=0.12)

# 🆕 Add player headshots
nflplot.add_player_headshot(ax, 'Patrick Mahomes', x=0.7, y=0.2, width=0.1)

# Add reference lines
nflplot.add_median_lines(ax, data, axis='both')

# Apply NFL theme
nflplot.apply_nfl_theme(ax, team='KC', style='default')
```

### 📊 **High-Level Plotting**
```python
# Team performance scatter plot
fig = nflplot.plot_team_stats(
    data, x='offensive_epa', y='defensive_epa',
    show_logos=True, add_reference_lines=True
)

# Player comparison radar chart
fig = nflplot.plot_player_comparison(
    player_data, players=['Josh Allen', 'Patrick Mahomes'],
    metrics=['passing_yards', 'passing_tds', 'qbr'],
    plot_type='radar'
)
```

### 📋 **NFL Tables**
```python
# Style pandas DataFrames with team logos
styled = nflplot.style_with_logos(df, 'team')
styled.to_html('nfl_table.html')

# 🆕 Add team wordmarks to tables
styled_wm = nflplot.style_with_wordmarks(df, 'team', wordmark_height=25)

# 🆕 Add player headshots to tables  
styled_hs = nflplot.style_with_headshots(
    player_df, 'player', id_type='name', headshot_height=40
)

# Comprehensive NFL-themed tables
table = nflplot.create_nfl_table(
    standings_df, 
    team_column='team',
    title='2024 NFL Standings'
)
table.save_html('standings.html')
```

### 🔍 **Plot Preview**
```python
# Preview plots with specified dimensions
nflplot.nfl_preview(fig, width=12, height=8, dpi=150)

# Quick preview with presets
nflplot.preview_with_dimensions(fig, 'presentation')  # 16:9 format
```

### 🏷️ **Advanced Elements**
```python
# Add logos to axis labels
nflplot.set_xlabel_with_logos(ax, ['KC', 'BUF', 'NE', 'NYJ'])

# Add logo watermarks
nflplot.add_logo_watermark(ax, 'KC', position='bottom_right')

# Create team comparison layouts
left_ax, right_ax = nflplot.create_team_comparison_axes(fig, 'KC', 'BUF')
```

## API Reference

### Main Functions

| Function | Description | nflplotR Equivalent |
|----------|-------------|-------------------|
| `get_team_colors()` | Get NFL team colors | `team_colors` |
| `add_nfl_logo()` | Add team logo to plot | `geom_nfl_logos()` |
| `add_median_lines()` | Add reference lines | `geom_median_lines()` |
| `style_with_logos()` | Add logos to tables | `gt_nfl_logos()` |
| `nfl_preview()` | Preview plots | `ggpreview()` |
| `nfl_sitrep()` | System information | `nflverse_sitrep` |
| `plot_team_stats()` | High-level team plots | Custom implementation |
| `team_factor()` | Ordered team factors | `nfl_team_factor()` |
| `team_tiers()` | Group teams by tiers | `nfl_team_tiers()` |

### Classes

- **`NFLAssetManager`**: Manages logo caching and asset downloads
- **`NFLColorPalette`**: Advanced color palette management
- **`NFLTableStyler`**: Pandas DataFrame styling with NFL elements
- **`AssetURLManager`**: Comprehensive URL management for all NFL assets

### Visualization Backends

- **Matplotlib**: `nflplotpy.matplotlib.*`
- **Plotly**: `nflplotpy.plotly.*` 
- **Seaborn**: `nflplotpy.seaborn.*`

## 📦 Installation Options

```bash
# Basic installation
pip install nflplotpy

# With plotly support
pip install nflplotpy[plotly]

# With seaborn support  
pip install nflplotpy[seaborn]

# Complete installation with all backends
pip install nflplotpy[all]

# Development installation
pip install nflplotpy[dev]
```

## 🏗️ Package Structure

```
nflplotpy/
├── core/           # Core functionality (colors, logos, utilities, URLs)
├── matplotlib/     # Matplotlib integration (artists, scales, preview, elements)
├── plotly/         # Plotly integration  
├── seaborn/        # Seaborn integration
├── pandas/         # Pandas table styling integration
├── data/           # Team metadata
├── examples/       # Usage examples and tutorials
└── tests/          # Comprehensive test suite
```

## 🤝 Contributing

nflplotpy welcomes contributions! Here's how you can help:

1. **Report Issues**: Found a bug? [Open an issue](https://github.com/joelfeinberg/nflplotpy/issues)
2. **Feature Requests**: Have an idea? We'd love to hear it!
3. **Code Contributions**: Fork, develop, and submit a pull request
4. **Documentation**: Help improve our docs and examples

### Development Setup

```bash
git clone https://github.com/joelfeinberg/nflplotpy.git
cd nflplotpy
pip install -e .[dev]
pytest tests/
```

## 🌟 Community & Support

- **Discord**: Join the [nflverse Discord](https://discord.gg/5Er2FBnnQa)  
- **Issues**: [GitHub Issues](https://github.com/joelfeinberg/nflplotpy/issues)
- **Discussions**: [GitHub Discussions](https://github.com/joelfeinberg/nflplotpy/discussions)

## ⚡ Requirements

- **Python**: 3.8+
- **Core Dependencies**: matplotlib, pandas, numpy, pillow, requests
- **Optional**: plotly (5.0+), seaborn (0.11+)
- **Supports**: CPython, PyPy

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

*This package is inspired by and builds upon the amazing work of the nflverse ecosystem and nflplotR package.*

## 🙏 Acknowledgments

- **nflplotR**: Original R package that inspired this work
- **nflverse**: Amazing NFL data ecosystem and community
- **NFL Analytics Community**: For continuous feedback and support

---

**Built for the NFL analytics community** 🏈

*Compatible with nfl_data_py, nflfastR, and other nflverse tools.*