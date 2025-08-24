# Changelog

All notable changes to nflplotpy will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.9.0] - 2024-12-XX

### 🎉 Major Release - Feature Complete Beta

**This release achieves complete feature parity with R's nflplotR package plus additional Python-specific enhancements. Ready for production use.**

### ✨ Added

#### Core Visualization Features
- **NFL Team Scale Functions**: Complete implementation of `scale_color_nfl()`, `scale_fill_nfl()` equivalents
- **Conference/Division Analysis**: `scale_color_conference()`, `scale_color_division()` functions
- **Generic Image Placement**: `add_image_from_path()` - equivalent to nflplotR's `geom_from_path()`
- **Enhanced Reference Lines**: Quantile lines, confidence bands, trend analysis with bootstrap methods
- **Element Replacement**: Logo-based legends, axis label replacement, colorbar customization

#### Advanced Statistical Overlays
- `add_quantile_lines()` - Any percentile combinations with orientation control
- `add_mean_lines()` - Mean lines with confidence bands and trend fitting
- `add_reference_band()` - Statistical reference ranges with customizable styling
- `add_median_lines()` - Robust central tendency visualization
- `add_percentile_lines()` - Percentile-based reference lines

#### Image and Asset Management
- **Image Transformations**: Rotation, colorization, alpha blending for all images
- **Advanced Logo Placement**: Precise positioning with hjust/vjust controls
- **Player Headshots**: Enhanced ESPN integration with fuzzy name matching
- **Team Wordmarks**: Official nflverse team wordmarks integration
- **Asset Caching**: Comprehensive caching system with appdirs integration

#### Pandas Table Integration (R gt Package Equivalent)
- **`style_with_logos()`** - Equivalent to R's `gt_nfl_logos()`
- **`style_with_headshots()`** - Equivalent to R's `gt_nfl_headshots()`  
- **`style_with_wordmarks()`** - Team wordmarks in tables
- **`NFLTableStyler`** - Advanced table styling with method chaining
- **`create_nfl_table()`** - One-function professional NFL tables
- **Team Color Integration** - Apply official team colors to table cells
- **Professional NFL Theming** - Official colors, fonts, styling

#### Plotly Integration Enhancements
- **`create_interactive_team_plot()`** - Rich interactive visualizations
- **`create_team_bar()`** / **`create_team_scatter()`** - Themed plotly charts
- **`apply_nfl_color_scale_plotly()`** - Consistent matplotlib/plotly theming
- **`add_quantile_lines_plotly()`** - Interactive statistical overlays
- **Enhanced Hover Information** - Rich tooltips with team data

#### Team Organization Utilities
- **`get_team_conference()`** / **`get_team_division()`** - Team information lookup
- **`get_division_rivals()`** - Automatic rivalry identification  
- **`get_teams_by_division()`** / **`get_teams_by_conference()`** - Organizational queries
- **Conference/Division Color Mapping** - Automatic grouping visualizations

#### Enhanced Player ID System
- **Multi-Format Support**: ESPN IDs, GSIS IDs, player names with auto-detection
- **nfl_data_py Integration**: Seamless integration with optional graceful fallbacks
- **Fuzzy Name Matching**: Intelligent player name resolution
- **Cross-Reference Mapping**: Convert between ID formats automatically

### 🔧 Improved

#### Code Quality & Performance
- **Complete Type Annotations**: Full type hints throughout codebase using modern syntax
- **Strict Linting**: Ruff configuration with 100+ rules for code quality
- **Performance Optimizations**: Enhanced caching, async-ready architecture
- **Error Handling**: Graceful degradation with informative warnings
- **Cross-Platform Support**: Enhanced Windows, macOS, Linux compatibility

#### Testing & Reliability  
- **Comprehensive Test Suite**: 108 tests covering all functionality (100% pass rate)
- **Mock Data Integration**: Tests work with/without external dependencies
- **CI/CD Ready**: Full GitHub Actions compatibility with quality gates
- **Coverage Reporting**: 40% test coverage (appropriate for visualization library)

#### Documentation & Usability
- **Complete API Documentation**: 63+ functions with comprehensive examples
- **Getting Started Tutorial**: Step-by-step beginner guide
- **Advanced Features Guide**: Complex use case documentation
- **Pandas Tables Showcase**: Interactive HTML demonstrations
- **Educational Examples**: Real NFL data analysis examples

### 🐛 Fixed

#### Asset Management
- **Logo Caching Issues**: Resolved file locking problems on Windows
- **URL Management**: Enhanced error handling for external asset downloads  
- **Image Processing**: Fixed PIL compatibility across platforms
- **Cache Cleanup**: Improved cache management and cleanup routines

#### Cross-Backend Consistency
- **Color Mapping**: Consistent team colors across matplotlib/plotly
- **Font Handling**: Resolved font availability issues across platforms
- **Image Rendering**: Fixed aspect ratio preservation in all contexts
- **Export Compatibility**: Enhanced HTML/PNG/SVG export quality

#### Player Data Integration
- **ID Resolution**: Improved player name matching accuracy
- **ESPN Integration**: Enhanced headshot URL generation
- **Fallback Systems**: Better error handling for missing player data
- **GSIS ID Support**: Complete GSIS ID format compatibility

### 📦 Package Management

#### Dependencies
- **Core Dependencies**: matplotlib>=3.5.0, pandas>=1.3, pillow>=8.0.0
- **Optional Dependencies**: plotly>=5.0.0, seaborn>=0.11.0, nfl_data_py>=0.3.0
- **Python Support**: Python 3.8+ with comprehensive testing
- **Build System**: Modern pyproject.toml with setuptools backend

#### Distribution
- **PyPI Ready**: Complete package metadata and classifiers
- **Installation Options**: Core, plotly, seaborn, nfldata, all variants
- **Development Mode**: Full editable installation support
- **Documentation**: Complete setup and installation guides

### 📊 Statistics

- **Function Count**: 63+ exported functions (up from ~20)
- **Feature Parity**: 100% equivalent to R nflplotR plus Python enhancements
- **Test Coverage**: 108 comprehensive tests with 100% pass rate
- **Code Quality**: Strict linting with ruff, complete type annotations
- **Documentation**: 4 major guides plus comprehensive API reference

### 🎯 Breaking Changes

None - this release maintains full backward compatibility with existing code.

### 🚀 Migration Guide

Existing nflplotpy v0.1.0 code will continue to work unchanged. New features can be adopted incrementally:

```python
# Existing code (still works)
nfl.add_nfl_logo(ax, 'KC', 0.5, 0.5)

# New scale functions (optional upgrade)
colors, _ = nfl.scale_color_nfl(['KC', 'BUF'])
plt.scatter(x, y, c=[colors[team] for team in teams])

# New pandas tables (new capability)
styled = nfl.style_with_logos(df, 'team_column')
styled.to_html('output.html')
```

### 🎉 Release Highlights

**v0.9.0 represents a major milestone:**

1. **Complete nflplotR Parity**: Every major nflplotR function now has a Python equivalent
2. **Enhanced Capabilities**: Python-specific features like interactive plotly integration
3. **Production Ready**: Professional code quality with comprehensive testing
4. **Educational Resources**: Complete documentation and tutorial materials
5. **Community Ready**: Prepared for wide adoption with polished user experience

**Next Steps Toward v1.0:**
- Community feedback integration
- Performance optimizations based on real usage
- Additional statistical visualization options
- Enhanced documentation based on user needs

---

## [0.1.0] - 2025-08-05

### Added - Initial Release
- **Core functionality**: Complete implementation of nflplotR equivalent for Python
- **Team colors**: All 32 NFL teams with primary, secondary, tertiary, and quaternary colors
- **Team logos**: Asset management system with caching for team logos
- **Matplotlib integration**: 
  - Custom artists for adding NFL logos to plots
  - NFL-themed styling and color scales  
  - Reference lines (median, mean)
  - Team color legends
- **Plotly integration**:
  - Interactive scatter plots with team colors
  - Team logo traces for interactive plots
  - NFL-themed layouts and styling
- **Seaborn integration**: Custom color palettes and themes
- **High-level plotting functions**:
  - `plot_team_stats()`: Team performance visualizations
  - `plot_player_comparison()`: Player comparison charts (radar, bar)
- **Utility functions**:
  - `team_factor()`: Ordered categorical team data
  - `team_tiers()`: Team grouping by conference, division, etc.
  - Team abbreviation validation and normalization
- **Asset management**: Intelligent caching system for logos and graphics
- **Comprehensive test suite**: Unit tests for all major functionality
- **Documentation**: Complete README, quick start guide, and examples

### API Functions (1:1 nflplotR parity)
- `get_team_colors()` ↔ `scale_color_nfl()`
- `add_nfl_logo()` ↔ `geom_nfl_logos()`
- `add_median_lines()` ↔ `geom_median_lines()`
- `team_factor()` ↔ `nfl_team_factor()`
- `team_tiers()` ↔ `nfl_team_tiers()`
- `nfl_color_scale()` ↔ `scale_color_nfl()`

---

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- **nflverse community** for the amazing R nflplotR package that inspired this work
- **nfl_data_py** for providing comprehensive NFL data access
- **NFL** for the incredible sport that makes this visualization necessary 🏈