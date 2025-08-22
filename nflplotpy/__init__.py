"""
nflplotpy - Python NFL Visualization Package

A Python equivalent to R's nflplotR package, providing NFL-specific
plotting capabilities with matplotlib, plotly, and seaborn integration.
"""

__version__ = "0.1.0"
__author__ = "nflverse"

# Core functionality
from .core.colors import NFL_TEAM_COLORS, NFLColorPalette, get_team_colors
from .core.logos import NFLAssetManager, get_available_teams

# High-level plotting functions
from .core.plotting import plot_player_comparison, plot_team_stats

# Enhanced URL management
from .core.urls import (
    AssetURLManager,
    discover_player_id,
    get_player_headshot_urls,
    get_team_wordmark_url,
)
from .core.utils import (
    clear_all_cache,
    get_nflverse_info,
    nfl_sitrep,
    team_factor,
    team_tiers,
    validate_player_ids,
    validate_teams,
)

# Matplotlib integration
from .matplotlib.artists import (
    add_mean_lines,
    add_median_lines,
    add_nfl_headshot,
    add_nfl_logo,
    add_nfl_wordmark,
)
from .matplotlib.elements import (
    add_logo_watermark,
    create_team_comparison_axes,
    set_title_with_logos,
    set_xlabel_with_logos,
    set_ylabel_with_logos,
)
from .matplotlib.preview import ggpreview, nfl_preview, preview_with_dimensions
from .matplotlib.scales import apply_nfl_theme, nfl_color_scale

# Pandas integration
from .pandas.styling import (
    NFLTableStyler,
    create_nfl_table,
    style_with_headshots,
    style_with_logos,
    style_with_wordmarks,
)

__all__ = [
    "NFL_TEAM_COLORS",
    "AssetURLManager",
    "NFLAssetManager",
    "NFLColorPalette",
    "NFLTableStyler",
    "add_logo_watermark",
    "add_mean_lines",
    "add_median_lines",
    "add_nfl_headshot",
    "add_nfl_logo",
    "add_nfl_wordmark",
    "apply_nfl_theme",
    "clear_all_cache",
    "create_nfl_table",
    "create_team_comparison_axes",
    "discover_player_id",
    "get_available_teams",
    "get_nflverse_info",
    "get_player_headshot_urls",
    "get_team_colors",
    "get_team_wordmark_url",
    "ggpreview",
    "nfl_color_scale",
    "nfl_preview",
    "nfl_sitrep",
    "plot_player_comparison",
    "plot_team_stats",
    "preview_with_dimensions",
    "set_title_with_logos",
    "set_xlabel_with_logos",
    "set_ylabel_with_logos",
    "style_with_headshots",
    "style_with_logos",
    "style_with_wordmarks",
    "team_factor",
    "team_tiers",
    "validate_player_ids",
    "validate_teams",
]
