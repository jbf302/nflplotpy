# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

nflplotpy is a comprehensive Python visualization package for NFL data analysis, providing complete feature parity with R's nflplotR package. It integrates with matplotlib, plotly, seaborn, and pandas to create NFL-themed visualizations including team logos, wordmarks, and player headshots.

## Development Commands

### Environment Setup
```bash
# Install in development mode (use .venv if available)
pip install -e .[dev]

# Install with all optional dependencies
pip install -e .[all]
```

### Testing
```bash
# Run all tests
pytest tests/

# Run with coverage
pytest tests/ --cov=nflplotpy

# Run specific test file
pytest tests/test_core.py -v
```

### Code Quality
```bash
# Lint with ruff
ruff check .

# Format with ruff
ruff format .

# Type checking with mypy
mypy nflplotpy/
```

### Building
```bash
# Build package
python -m build

# Install built package
pip install dist/nflplotpy-*.whl
```

## Architecture Overview

### Core Components

**nflplotpy/core/**: Foundation modules
- `colors.py`: NFL team color palettes and management
- `logos.py`: Asset downloading and caching (NFLAssetManager) 
- `urls.py`: Comprehensive URL management with nfl_data_py integration
- `plotting.py`: High-level plotting functions
- `utils.py`: Team validation, factors, and system utilities
- `assets.py`: Asset management utilities
- `nfl_data_integration.py`: nfl_data_py integration layer for player ID mapping

**Backend Integrations**:
- `matplotlib/`: Matplotlib artists, elements, scales, and preview
- `plotly/`: Plotly layouts and traces  
- `seaborn/`: Seaborn style integration
- `pandas/`: DataFrame styling with NFL elements

### Key Classes

- **NFLAssetManager**: Handles logo/asset caching and downloads
- **NFLColorPalette**: Advanced color palette management
- **AssetURLManager**: Manages URLs for all NFL assets (logos, wordmarks, headshots)
- **NFLTableStyler**: Pandas DataFrame styling with NFL elements

### Player ID System

The package supports multiple player identification methods:
- **ESPN IDs**: Numeric ESPN player identifiers
- **GSIS IDs**: NFL's official player IDs (format: 00-0012345)
- **Player Names**: Fuzzy matching against player database
- **Auto-detection**: Automatically determines ID type and converts between formats

Uses `nfl_data_py` for player ID mapping with graceful fallbacks when unavailable.

### Asset Management

- **Logos**: Team logos cached locally, downloaded from nflverse GitHub
- **Wordmarks**: Team wordmark images from nflverse repository
- **Headshots**: Player photos from ESPN with ID-based URLs
- **Caching**: Comprehensive caching system for all assets using appdirs

## Testing Notes

- Full test suite with 108+ tests covering all functionality
- Tests work with and without nfl_data_py installed (fallback system)
- Cross-platform compatibility (Windows, macOS, Linux)
- Mock data available for testing when external dependencies unavailable

## Key Dependencies

**Core**: matplotlib, pandas, numpy, pillow, requests, jinja2, appdirs
**Optional**: plotly (5.0+), seaborn (0.11+), nfl_data_py (0.3.0+)

## Development Notes

- Python 3.8+ support with type hints
- Ruff for linting/formatting (line length 88)
- MyPy for type checking with strict configuration
- Uses nflverse ecosystem URLs and standards
- Extensive caching to minimize external requests
- Graceful degradation when optional dependencies unavailable