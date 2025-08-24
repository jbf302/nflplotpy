"""Color scales and themes for matplotlib integration."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

import matplotlib.colors as mcolors
import matplotlib.pyplot as plt

from nflplotpy.core.colors import create_nfl_colormap, get_team_colors
from nflplotpy.core.utils import validate_teams

if TYPE_CHECKING:
    from matplotlib.axes import Axes


def nfl_color_scale(
    teams: list[str], color_type: str = "primary"
) -> mcolors.ListedColormap:
    """Create matplotlib colormap from NFL team colors.

    Equivalent to nflplotR's scale_color_nfl().

    Args:
        teams: List of team abbreviations
        color_type: Type of color ('primary', 'secondary', 'tertiary', 'quaternary')

    Returns:
        matplotlib ListedColormap
    """
    return create_nfl_colormap(teams, color_type)


def set_team_colors(
    ax: Axes,
    teams: list[str],
    data_values: list[Any] | None = None,
    color_type: str = "primary",
    **kwargs,
):
    """Set team colors for plot elements.

    Args:
        ax: Matplotlib axes
        teams: List of team abbreviations
        data_values: Values to map colors to (if None, uses teams directly)
        color_type: Type of color to use
        **kwargs: Additional arguments
    """
    # Validate teams
    teams = validate_teams(teams)

    # Get colors
    colors = get_team_colors(teams, color_type)

    # Create color mapping
    if data_values is None:
        data_values = teams

    return dict(zip(data_values, colors))


def set_team_fill_colors(
    ax: Axes, teams: list[str], color_type: str = "primary", **kwargs
):
    """Set team fill colors for plot elements.

    Equivalent to nflplotR's scale_fill_nfl().

    Args:
        ax: Matplotlib axes
        teams: List of team abbreviations
        color_type: Type of color to use
        **kwargs: Additional arguments
    """
    return set_team_colors(ax, teams, color_type=color_type, **kwargs)


def apply_nfl_theme(
    ax: Axes, team: str | None = None, style: str = "default", **kwargs
):
    """Apply NFL-themed styling to matplotlib axes.

    Args:
        ax: Matplotlib axes
        team: Specific team to theme around (optional)
        style: Theme style ('default', 'minimal', 'dark')
        **kwargs: Additional styling arguments
    """
    if style == "default":
        _apply_default_nfl_theme(ax, team, **kwargs)
    elif style == "minimal":
        _apply_minimal_nfl_theme(ax, team, **kwargs)
    elif style == "dark":
        _apply_dark_nfl_theme(ax, team, **kwargs)
    else:
        msg = f"Unknown style: {style}"
        raise ValueError(msg)


def _apply_default_nfl_theme(ax: Axes, team: str | None = None, **kwargs):
    """Apply default NFL theme styling."""

    # Grid styling
    ax.grid(True, alpha=0.3, linestyle="-", linewidth=0.5)
    ax.set_axisbelow(True)

    # Spine styling
    for spine in ax.spines.values():
        spine.set_linewidth(1.5)
        spine.set_color("#333333")

    # Tick styling
    ax.tick_params(which="major", labelsize=10, color="#333333", width=1, length=5)

    # If team is specified, use team colors
    if team is not None:
        team = validate_teams(team)[0]
        primary_color = get_team_colors(team, "primary")
        get_team_colors(team, "secondary")

        # Apply team colors to spines
        ax.spines["top"].set_color(primary_color)
        ax.spines["bottom"].set_color(primary_color)
        ax.spines["left"].set_color(primary_color)
        ax.spines["right"].set_color(primary_color)

        # Apply to ticks
        ax.tick_params(color=primary_color)


def _apply_minimal_nfl_theme(ax: Axes, team: str | None = None, **kwargs):
    """Apply minimal NFL theme styling."""

    # Remove top and right spines
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    # Style remaining spines
    ax.spines["left"].set_linewidth(1)
    ax.spines["bottom"].set_linewidth(1)
    ax.spines["left"].set_color("#666666")
    ax.spines["bottom"].set_color("#666666")

    # Minimal grid
    ax.grid(True, alpha=0.2, linestyle="-", linewidth=0.5)
    ax.set_axisbelow(True)

    # Clean tick styling
    ax.tick_params(which="major", labelsize=9, color="#666666", width=0.5, length=3)

    if team is not None:
        team = validate_teams(team)[0]
        primary_color = get_team_colors(team, "primary")

        ax.spines["left"].set_color(primary_color)
        ax.spines["bottom"].set_color(primary_color)


def _apply_dark_nfl_theme(ax: Axes, team: str | None = None, **kwargs):
    """Apply dark NFL theme styling."""

    # Dark background
    ax.set_facecolor("#1e1e1e")

    # Light grid
    ax.grid(True, alpha=0.2, linestyle="-", linewidth=0.5, color="white")
    ax.set_axisbelow(True)

    # Light spines
    for spine in ax.spines.values():
        spine.set_linewidth(1.5)
        spine.set_color("#cccccc")

    # Light ticks and labels
    ax.tick_params(
        which="major",
        labelsize=10,
        color="#cccccc",
        labelcolor="white",
        width=1,
        length=5,
    )

    if team is not None:
        team = validate_teams(team)[0]
        primary_color = get_team_colors(team, "primary")

        # Brighten team color for dark theme
        import matplotlib.colors as mcolors

        rgb = mcolors.hex2color(primary_color)
        # Simple brightness adjustment
        bright_rgb = tuple(min(1.0, c * 1.3) for c in rgb)
        bright_color = mcolors.rgb2hex(bright_rgb)

        for spine in ax.spines.values():
            spine.set_color(bright_color)


def create_team_scatter_colors(
    teams: list[str],
    values: list[float] | None = None,
    color_type: str = "primary",
    colormap: str | None = None,
) -> list[str]:
    """Create colors for scatter plot points based on teams.

    Args:
        teams: List of team abbreviations
        values: Optional values to map to colors (for gradient coloring)
        color_type: Type of team color to use
        colormap: Optional matplotlib colormap name

    Returns:
        List of color values for each point
    """
    if values is None:
        # Use team colors directly
        return get_team_colors(teams, color_type)
    # Use colormap with team color influence
    if colormap is None:
        # Create custom colormap from team colors
        unique_teams = list(set(teams))
        cmap = nfl_color_scale(unique_teams, color_type)
    else:
        cmap = plt.get_cmap(colormap)

    # Normalize values
    norm = mcolors.Normalize(vmin=min(values), vmax=max(values))
    return [cmap(norm(v)) for v in values]


def add_team_color_legend(
    ax: Axes, teams: list[str], color_type: str = "primary", loc: str = "best", **kwargs
):
    """Add legend showing team colors.

    Args:
        ax: Matplotlib axes
        teams: List of team abbreviations to include in legend
        color_type: Type of color to show
        loc: Legend location
        **kwargs: Additional arguments passed to legend()

    Returns:
        matplotlib Legend object
    """
    from matplotlib.patches import Patch

    # Validate teams
    teams = validate_teams(teams)

    # Get colors
    colors = get_team_colors(teams, color_type)

    # Create legend elements
    legend_elements = [
        Patch(facecolor=color, label=team) for team, color in zip(teams, colors)
    ]

    # Default legend styling
    legend_kwargs = {
        "frameon": True,
        "fancybox": True,
        "shadow": True,
        "framealpha": 0.9,
        "fontsize": 9,
    }
    legend_kwargs.update(kwargs)

    return ax.legend(handles=legend_elements, loc=loc, **legend_kwargs)


def scale_color_nfl(
    data: list[str] | None = None,
    values: list[str] | None = None,
    color_type: str = "primary",
    guide: bool = True,
    alpha: float = 1.0,
    **kwargs,
) -> dict[str, str] | tuple[list[str], dict[str, str]]:
    """Create NFL team color scale mapping for matplotlib plots.

    Equivalent to nflplotR's scale_color_nfl(). Provides automatic color
    mapping for team data in plots.

    Args:
        data: Team abbreviations from your dataset
        values: Specific values to map to teams (if different from data)
        color_type: Type of team color ('primary', 'secondary', 'tertiary', 'quaternary')
        guide: Whether to return legend information
        alpha: Alpha transparency (0-1)
        **kwargs: Additional arguments

    Returns:
        Color mapping dictionary, or tuple of (colors, mapping) if guide=True

    Example:
        ```python
        # Basic usage
        colors = scale_color_nfl(['KC', 'BUF', 'DAL'])

        # With custom values
        colors = scale_color_nfl(values=['Team1', 'Team2'], data=['KC', 'BUF'])

        # Get colors and legend info
        colors, legend_info = scale_color_nfl(['KC', 'BUF'], guide=True)
        ```
    """
    if data is None:
        data = []

    # Validate teams
    teams = validate_teams(data)

    # If values provided, use those as keys, otherwise use teams
    keys = values if values is not None else teams

    if len(keys) != len(teams):
        msg = f"Length of values ({len(keys)}) must match length of data ({len(teams)})"
        raise ValueError(msg)

    # Get team colors
    colors = get_team_colors(teams, color_type)

    # Apply alpha if not 1.0
    if alpha != 1.0:
        import matplotlib.colors as mcolors

        rgba_colors = []
        for color in colors:
            rgb = mcolors.hex2color(color)
            rgba_colors.append((*rgb, alpha))
        colors = rgba_colors

    # Create mapping
    color_mapping = dict(zip(keys, colors))

    if guide:
        legend_info = {
            "teams": teams,
            "colors": colors,
            "color_type": color_type,
            "alpha": alpha,
        }
        return color_mapping, legend_info

    return color_mapping


def scale_fill_nfl(
    data: list[str] | None = None,
    values: list[str] | None = None,
    color_type: str = "primary",
    guide: bool = True,
    alpha: float = 1.0,
    **kwargs,
) -> dict[str, str] | tuple[list[str], dict[str, str]]:
    """Create NFL team fill color scale mapping for matplotlib plots.

    Equivalent to nflplotR's scale_fill_nfl(). Same as scale_color_nfl
    but intended for fill colors.

    Args:
        data: Team abbreviations from your dataset
        values: Specific values to map to teams (if different from data)
        color_type: Type of team color ('primary', 'secondary', 'tertiary', 'quaternary')
        guide: Whether to return legend information
        alpha: Alpha transparency (0-1)
        **kwargs: Additional arguments

    Returns:
        Color mapping dictionary, or tuple of (colors, mapping) if guide=True
    """
    return scale_color_nfl(data, values, color_type, guide, alpha, **kwargs)


def scale_color_conference(
    data: list[str] | None = None,
    values: list[str] | None = None,
    palette_type: str = "classic",
    guide: bool = True,
    alpha: float = 1.0,
    **kwargs,
) -> dict[str, str]:
    """Create conference-based color scale.

    Maps teams to colors based on their conference (AFC/NFC).

    Args:
        data: Team abbreviations from your dataset
        values: Specific values to map to teams (if different from data)
        palette_type: Color palette style ('classic', 'modern', 'contrast')
        guide: Whether to return legend information
        alpha: Alpha transparency (0-1)
        **kwargs: Additional arguments

    Returns:
        Color mapping dictionary
    """
    if data is None:
        data = []

    teams = validate_teams(data)
    keys = values if values is not None else teams

    # Conference color schemes
    palettes = {
        "classic": {"AFC": "#FF0000", "NFC": "#0000FF"},  # Red/Blue
        "modern": {"AFC": "#1f77b4", "NFC": "#ff7f0e"},  # Modern blue/orange
        "contrast": {"AFC": "#2ca02c", "NFC": "#d62728"},  # Green/Red
    }

    if palette_type not in palettes:
        msg = f"Unknown palette_type: {palette_type}. Choose from: {list(palettes.keys())}"
        raise ValueError(msg)

    colors = palettes[palette_type]

    # Map teams to conference colors
    from nflplotpy.core.utils import get_team_conference

    color_mapping = {}

    for i, team in enumerate(teams):
        conf = get_team_conference(team)
        color_mapping[keys[i]] = colors.get(conf, "#888888")  # Gray fallback

    return color_mapping


def scale_color_division(
    data: list[str] | None = None,
    values: list[str] | None = None,
    palette: str = "Set1",
    guide: bool = True,
    alpha: float = 1.0,
    **kwargs,
) -> dict[str, str]:
    """Create division-based color scale.

    Maps teams to colors based on their division.

    Args:
        data: Team abbreviations from your dataset
        values: Specific values to map to teams (if different from data)
        palette: Matplotlib colormap name for divisions
        guide: Whether to return legend information
        alpha: Alpha transparency (0-1)
        **kwargs: Additional arguments

    Returns:
        Color mapping dictionary
    """
    if data is None:
        data = []

    teams = validate_teams(data)
    keys = values if values is not None else teams

    # Get unique divisions
    from nflplotpy.core.utils import get_team_division

    divisions = [get_team_division(team) for team in teams]
    unique_divs = list(set(divisions))

    # Create color palette
    cmap = plt.get_cmap(palette)
    div_colors = {}

    for i, div in enumerate(unique_divs):
        color = cmap(i / max(1, len(unique_divs) - 1))
        div_colors[div] = mcolors.rgb2hex(color[:3])  # Convert to hex

    # Map teams to division colors
    color_mapping = {}
    for i, team in enumerate(teams):
        div = get_team_division(team)
        color_mapping[keys[i]] = div_colors[div]

    return color_mapping


def apply_nfl_color_scale(
    ax: Axes,
    artists: list,
    teams: list[str],
    scale_type: str = "team",
    color_type: str = "primary",
    **kwargs,
):
    """Apply NFL color scaling to plot artists.

    Automatically colors plot elements (bars, points, lines) using NFL colors.

    Args:
        ax: Matplotlib axes
        artists: List of matplotlib artists (bars, scatter points, etc.)
        teams: List of team abbreviations corresponding to artists
        scale_type: Type of scale ('team', 'conference', 'division')
        color_type: Color type for team scale
        **kwargs: Additional arguments passed to scale functions
    """
    if len(artists) != len(teams):
        msg = f"Number of artists ({len(artists)}) must match number of teams ({len(teams)})"
        raise ValueError(msg)

    # Get color mapping based on scale type
    if scale_type == "team":
        color_map = scale_color_nfl(teams, color_type=color_type, guide=False, **kwargs)
    elif scale_type == "conference":
        color_map = scale_color_conference(teams, guide=False, **kwargs)
    elif scale_type == "division":
        color_map = scale_color_division(teams, guide=False, **kwargs)
    else:
        msg = f"Unknown scale_type: {scale_type}"
        raise ValueError(msg)

    # Apply colors to artists
    for artist, team in zip(artists, teams):
        color = color_map.get(team, "#888888")  # Gray fallback

        if hasattr(artist, "set_color"):
            artist.set_color(color)
        elif hasattr(artist, "set_facecolor"):
            artist.set_facecolor(color)
        elif hasattr(artist, "set_edgecolor"):
            artist.set_edgecolor(color)


def create_nfl_color_palette(
    teams: list[str] | None = None,
    scale_type: str = "team",
    color_type: str = "primary",
    n_colors: int | None = None,
    **kwargs,
) -> list[str]:
    """Create a color palette for NFL visualizations.

    Args:
        teams: Team abbreviations to include
        scale_type: Type of scale ('team', 'conference', 'division', 'gradient')
        color_type: Color type for team scale
        n_colors: Number of colors for gradient palettes
        **kwargs: Additional arguments

    Returns:
        List of hex color codes
    """
    if scale_type == "gradient" and teams and len(teams) >= 2:
        # Create gradient between team colors
        from nflplotpy.core.colors import NFLColorPalette

        palette = NFLColorPalette()
        n = n_colors or 10
        return palette.create_gradient(teams[0], teams[1], n_colors=n)

    if teams is None:
        # Return all team colors
        from nflplotpy.core.colors import NFL_TEAM_COLORS

        return [NFL_TEAM_COLORS[team][color_type] for team in NFL_TEAM_COLORS]

    # Use appropriate scale function
    if scale_type == "team":
        color_map = scale_color_nfl(teams, color_type=color_type, guide=False, **kwargs)
    elif scale_type == "conference":
        color_map = scale_color_conference(teams, guide=False, **kwargs)
    elif scale_type == "division":
        color_map = scale_color_division(teams, guide=False, **kwargs)
    else:
        msg = f"Unknown scale_type: {scale_type}"
        raise ValueError(msg)

    return list(color_map.values())
