"""Seaborn styling and integration for NFL visualizations."""

from __future__ import annotations

import matplotlib.pyplot as plt
import seaborn as sns

from nflplotpy.core.colors import get_palette_manager, get_team_colors
from nflplotpy.core.utils import validate_teams


def set_nfl_style(style: str = "whitegrid", team: str | None = None, **kwargs):
    """Set seaborn style with NFL theming.

    Args:
        style: Base seaborn style
        team: Team to base colors on
        **kwargs: Additional style parameters
    """
    # Set base seaborn style
    sns.set_style(style, **kwargs)

    # Apply team-specific colors if specified
    if team is not None:
        team = validate_teams(team)[0]
        primary_color = get_team_colors(team, "primary")

        # Update matplotlib rcParams for team colors
        plt.rcParams.update(
            {
                "axes.edgecolor": primary_color,
                "axes.labelcolor": primary_color,
                "xtick.color": primary_color,
                "ytick.color": primary_color,
            }
        )


def create_nfl_palette(teams: list[str], color_type: str = "primary") -> list[str]:
    """Create seaborn-compatible color palette from NFL team colors.

    Args:
        teams: List of team abbreviations
        color_type: Type of color to use

    Returns:
        List of hex color codes
    """
    teams = validate_teams(teams)
    return get_team_colors(teams, color_type)


def set_team_palette(teams: list[str], color_type: str = "primary", **kwargs):
    """Set seaborn color palette to team colors.

    Args:
        teams: List of team abbreviations
        color_type: Type of color to use
        **kwargs: Additional arguments passed to sns.set_palette
    """
    palette = create_nfl_palette(teams, color_type)
    sns.set_palette(palette, **kwargs)


def create_conference_palette(
    conference: str = "NFL", color_type: str = "primary"
) -> list[str]:
    """Create seaborn palette for conference teams.

    Args:
        conference: 'AFC', 'NFC', or 'NFL'
        color_type: Type of color to use

    Returns:
        List of hex color codes
    """
    manager = get_palette_manager()
    return manager.create_conference_palette(conference, color_type)


def create_division_palette(division: str, color_type: str = "primary") -> list[str]:
    """Create seaborn palette for division teams.

    Args:
        division: Division name (e.g., 'AFC East')
        color_type: Type of color to use

    Returns:
        List of hex color codes
    """
    manager = get_palette_manager()
    return manager.create_division_palette(division, color_type)


def apply_nfl_context(
    context: str = "notebook",
    font_scale: float = 1.0,
    team: str | None = None,
    **kwargs,
):
    """Apply seaborn context with NFL styling.

    Args:
        context: Seaborn context ('notebook', 'talk', 'poster', 'paper')
        font_scale: Font scaling factor
        team: Team to base styling on
        **kwargs: Additional context parameters
    """
    # Set seaborn context
    sns.set_context(context, font_scale=font_scale, **kwargs)

    # Apply team styling if specified
    if team is not None:
        team = validate_teams(team)[0]
        primary_color = get_team_colors(team, "primary")

        # Update font colors
        plt.rcParams.update(
            {"text.color": primary_color, "axes.titlecolor": primary_color}
        )
