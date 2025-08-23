"""Theme elements for integrating logos, wordmarks, and headshots into plot components.

Provides functions to replace text elements (axis labels, titles, etc.)
with NFL team logos, wordmarks, and player headshots, similar to R's
element_nfl_logo() functionality.
"""

from __future__ import annotations

import warnings

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

from nflplotpy.core.colors import get_team_colors
from nflplotpy.core.urls import get_player_headshot_urls, get_url_manager
from nflplotpy.core.utils import validate_teams

from .artists import add_nfl_logo


def set_xlabel_with_logos(
    ax: plt.Axes,
    teams: list[str],
    positions: list[float] | None = None,
    logo_size: float = 0.05,
    text_labels: bool = False,
    **kwargs,
):
    """Replace x-axis labels with team logos.

    Equivalent to R's element_nfl_logo() for x-axis.

    Args:
        ax: matplotlib Axes
        teams: List of team abbreviations
        positions: X positions for logos. If None, uses evenly spaced positions.
        logo_size: Size of logos
        text_labels: Whether to keep text labels alongside logos
        **kwargs: Additional arguments for logo placement
    """
    teams = validate_teams(teams)

    if positions is None:
        positions = np.linspace(0, len(teams) - 1, len(teams))

    if len(positions) != len(teams):
        msg = "Length of positions must match length of teams"
        raise ValueError(msg)

    # Clear existing x-axis labels
    if not text_labels:
        ax.set_xticklabels([])

    # Set x-axis ticks at positions
    ax.set_xticks(positions)

    # Add team logos below x-axis
    y_offset = -0.1  # Position below axis

    for team, pos in zip(teams, positions):
        try:
            # Add logo
            add_nfl_logo(
                ax,
                team,
                pos,
                y_offset,
                width=logo_size,
                transform=ax.transData,
                clip_on=False,
                **kwargs,
            )
        except Exception as e:
            warnings.warn(f"Could not add logo for {team}: {e}", stacklevel=2)

    # Adjust bottom margin to accommodate logos
    plt.subplots_adjust(bottom=0.2)


def set_ylabel_with_logos(
    ax: plt.Axes,
    teams: list[str],
    positions: list[float] | None = None,
    logo_size: float = 0.05,
    text_labels: bool = False,
    **kwargs,
):
    """Replace y-axis labels with team logos.

    Equivalent to R's element_nfl_logo() for y-axis.

    Args:
        ax: matplotlib Axes
        teams: List of team abbreviations
        positions: Y positions for logos. If None, uses evenly spaced positions.
        logo_size: Size of logos
        text_labels: Whether to keep text labels alongside logos
        **kwargs: Additional arguments for logo placement
    """
    teams = validate_teams(teams)

    if positions is None:
        positions = np.linspace(0, len(teams) - 1, len(teams))

    if len(positions) != len(teams):
        msg = "Length of positions must match length of teams"
        raise ValueError(msg)

    # Clear existing y-axis labels
    if not text_labels:
        ax.set_yticklabels([])

    # Set y-axis ticks at positions
    ax.set_yticks(positions)

    # Add team logos to the left of y-axis
    x_offset = -0.1  # Position to left of axis

    for team, pos in zip(teams, positions):
        try:
            # Add logo
            add_nfl_logo(
                ax,
                team,
                x_offset,
                pos,
                width=logo_size,
                transform=ax.transData,
                clip_on=False,
                **kwargs,
            )
        except Exception as e:
            warnings.warn(f"Could not add logo for {team}: {e}", stacklevel=2)

    # Adjust left margin to accommodate logos
    plt.subplots_adjust(left=0.2)


def set_title_with_logos(
    ax: plt.Axes,
    title_text: str,
    teams: list[str],
    logo_positions: str = "sides",
    logo_size: float = 0.08,
    title_fontsize: int = 14,
    **kwargs,
):
    """Add team logos to plot title.

    Args:
        ax: matplotlib Axes
        title_text: Main title text
        teams: List of team abbreviations (max 2 for sides positioning)
        logo_positions: Where to place logos ('sides', 'above', 'below')
        logo_size: Size of logos
        title_fontsize: Font size for title text
        **kwargs: Additional arguments
    """
    teams = validate_teams(teams)

    # Set main title
    title = ax.set_title(title_text, fontsize=title_fontsize, pad=20)

    if logo_positions == "sides" and len(teams) <= 2:
        # Place logos on left and right sides of title
        title_bbox = title.get_window_extent()
        fig = ax.get_figure()

        # Convert to axes coordinates
        title_center = title_bbox.x0 + title_bbox.width / 2
        title_y = title_bbox.y1 + 10

        if len(teams) >= 1:
            # Left logo
            add_nfl_logo(
                ax,
                teams[0],
                title_center - title_bbox.width / 2 - 50,
                title_y,
                width=logo_size,
                transform=fig.transFigure,
                **kwargs,
            )

        if len(teams) == 2:
            # Right logo
            add_nfl_logo(
                ax,
                teams[1],
                title_center + title_bbox.width / 2 + 50,
                title_y,
                width=logo_size,
                transform=fig.transFigure,
                **kwargs,
            )

    elif logo_positions == "above":
        # Place logos above title in a row
        fig = ax.get_figure()

        # Calculate positions
        n_teams = len(teams)
        if n_teams > 6:
            warnings.warn(
                "Too many teams for above positioning, using first 6", stacklevel=2
            )
            teams = teams[:6]
            n_teams = 6

        # Center the logos above the plot
        start_x = 0.5 - (n_teams * 0.1) / 2
        y_pos = 0.95  # Near top of figure

        for i, team in enumerate(teams):
            x_pos = start_x + i * 0.1
            add_nfl_logo(
                ax,
                team,
                x_pos,
                y_pos,
                width=logo_size,
                transform=fig.transFigure,
                **kwargs,
            )

    else:
        warnings.warn(f"Unsupported logo_positions: {logo_positions}", stacklevel=2)


def add_logo_watermark(
    ax: plt.Axes,
    team: str,
    position: str = "bottom_right",
    alpha: float = 0.3,
    logo_size: float = 0.15,
):
    """Add team logo as watermark to plot.

    Args:
        ax: matplotlib Axes
        team: Team abbreviation
        position: Where to place watermark ('bottom_right', 'bottom_left',
                 'top_right', 'top_left', 'center')
        alpha: Transparency level
        logo_size: Size of watermark logo
    """
    team = validate_teams(team)[0]

    # Position mapping
    positions = {
        "bottom_right": (0.85, 0.15),
        "bottom_left": (0.15, 0.15),
        "top_right": (0.85, 0.85),
        "top_left": (0.15, 0.85),
        "center": (0.5, 0.5),
    }

    if position not in positions:
        msg = f"Invalid position: {position}. Choose from: {list(positions.keys())}"
        raise ValueError(msg)

    x, y = positions[position]

    # Add logo with transparency
    add_nfl_logo(
        ax,
        team,
        x,
        y,
        width=logo_size,
        alpha=alpha,
        transform=ax.transAxes,
        zorder=0,  # Behind other elements
    )


def create_team_comparison_axes(
    fig: plt.Figure, team1: str, team2: str, title: str | None = None
) -> tuple[plt.Axes, plt.Axes]:
    """Create split axes for team vs team comparisons.

    Args:
        fig: matplotlib Figure
        team1: First team abbreviation
        team2: Second team abbreviation
        title: Optional main title

    Returns:
        Tuple of (left_ax, right_ax) for each team
    """
    teams = validate_teams([team1, team2])
    team1, team2 = teams

    # Create two side-by-side subplots
    left_ax = fig.add_subplot(121)
    right_ax = fig.add_subplot(122)

    # Get team colors
    get_team_colors(team1, "primary")
    get_team_colors(team2, "primary")

    # Style each subplot with team colors
    from .scales import apply_nfl_theme

    apply_nfl_theme(left_ax, team=team1)
    apply_nfl_theme(right_ax, team=team2)

    # Add team logos as subplot titles
    add_nfl_logo(left_ax, team1, 0.5, 1.1, width=0.1, transform=left_ax.transAxes)
    add_nfl_logo(right_ax, team2, 0.5, 1.1, width=0.1, transform=right_ax.transAxes)

    # Main title if provided
    if title:
        fig.suptitle(title, fontsize=16, fontweight="bold")

    return left_ax, right_ax


def add_conference_logos(
    ax: plt.Axes, position: str = "corners", logo_size: float = 0.08, alpha: float = 0.6
):
    """Add AFC and NFC logos to plot.

    Args:
        ax: matplotlib Axes
        position: Where to place logos ('corners', 'top', 'bottom')
        logo_size: Size of logos
        alpha: Transparency level
    """
    if position == "corners":
        # AFC in top-left, NFC in top-right
        add_nfl_logo(
            ax, "AFC", 0.05, 0.95, width=logo_size, alpha=alpha, transform=ax.transAxes
        )
        add_nfl_logo(
            ax, "NFC", 0.95, 0.95, width=logo_size, alpha=alpha, transform=ax.transAxes
        )

    elif position == "top":
        # Both at top, centered
        add_nfl_logo(
            ax, "AFC", 0.4, 0.95, width=logo_size, alpha=alpha, transform=ax.transAxes
        )
        add_nfl_logo(
            ax, "NFC", 0.6, 0.95, width=logo_size, alpha=alpha, transform=ax.transAxes
        )

    elif position == "bottom":
        # Both at bottom, centered
        add_nfl_logo(
            ax, "AFC", 0.4, 0.05, width=logo_size, alpha=alpha, transform=ax.transAxes
        )
        add_nfl_logo(
            ax, "NFC", 0.6, 0.05, width=logo_size, alpha=alpha, transform=ax.transAxes
        )

    else:
        msg = f"Invalid position: {position}"
        raise ValueError(msg)


def create_division_subplot_grid(
    fig: plt.Figure, division_data: dict[str, list[str]], title: str | None = None
) -> dict[str, plt.Axes]:
    """Create subplot grid organized by NFL divisions.

    Args:
        fig: matplotlib Figure
        division_data: Dictionary mapping division names to team lists
        title: Optional main title

    Returns:
        Dictionary mapping division names to their axes
    """
    n_divisions = len(division_data)

    # Determine grid layout
    if n_divisions <= 4:
        rows, cols = 2, 2
    elif n_divisions <= 6:
        rows, cols = 2, 3
    elif n_divisions <= 8:
        rows, cols = 2, 4
    else:
        rows = int(np.ceil(n_divisions / 4))
        cols = 4

    axes = {}

    for i, (division, teams) in enumerate(division_data.items()):
        if i >= rows * cols:
            break

        ax = fig.add_subplot(rows, cols, i + 1)
        axes[division] = ax

        # Add division title with team logos
        ax.set_title(division, fontsize=12, fontweight="bold", pad=20)

        # Add small team logos above subplot
        if teams:
            n_teams = min(len(teams), 4)  # Max 4 logos per division
            for j, team in enumerate(teams[:n_teams]):
                x_pos = 0.2 + j * 0.15
                try:
                    add_nfl_logo(
                        ax, team, x_pos, 1.05, width=0.06, transform=ax.transAxes
                    )
                except Exception:
                    pass  # Skip invalid teams

    if title:
        fig.suptitle(title, fontsize=16, fontweight="bold", y=0.98)

    return axes


def add_team_wordmark(
    ax: plt.Axes,
    team: str,
    x: float,
    y: float,
    width: float = 0.1,
    transform: plt.Transform | None = None,
    **kwargs,
):
    """Add NFL team wordmark to plot.

    Args:
        ax: matplotlib Axes
        team: Team abbreviation
        x: X position
        y: Y position
        width: Width of wordmark
        transform: Coordinate transform to use
        **kwargs: Additional arguments for OffsetImage
    """
    from io import BytesIO

    import requests
    from matplotlib import offsetbox

    team = validate_teams(team)[0]

    try:
        # Get wordmark URL
        manager = get_url_manager()
        wordmark_url = manager.get_wordmark_url(team)

        # Download and load image
        response = requests.get(wordmark_url, timeout=10)
        response.raise_for_status()

        wordmark_img = Image.open(BytesIO(response.content))


        # Create OffsetImage
        imagebox = offsetbox.OffsetImage(
            wordmark_img, zoom=width * ax.figure.dpi / 100, **kwargs
        )

        # Create AnnotationBbox
        ab = offsetbox.AnnotationBbox(
            imagebox, (x, y), frameon=False, transform=transform or ax.transAxes
        )

        # Add to axes
        ax.add_artist(ab)
        return ab

    except Exception as e:
        warnings.warn(f"Could not add wordmark for {team}: {e}", stacklevel=2)
        return None


def add_player_headshot(
    ax: plt.Axes,
    player_id: str | int,
    x: float,
    y: float,
    width: float = 0.08,
    id_type: str = "auto",
    transform: plt.Transform | None = None,
    circular: bool = True,
    **kwargs,
):
    """Add NFL player headshot to plot.

    Args:
        ax: matplotlib Axes
        player_id: Player identifier (ESPN ID, GSIS ID, or name)
        x: X position
        y: Y position
        width: Width of headshot
        id_type: Type of player identifier ('espn', 'gsis', 'name', 'auto')
        transform: Coordinate transform to use
        circular: Whether to crop headshot to circular shape
        **kwargs: Additional arguments for OffsetImage
    """
    from io import BytesIO

    import requests
    from matplotlib import offsetbox

    try:
        # Get headshot URLs
        urls = get_player_headshot_urls(player_id, id_type=id_type)

        if "espn_full" not in urls:
            warnings.warn(
                f"No headshot URL found for player: {player_id}", stacklevel=2
            )
            return None

        headshot_url = urls["espn_full"]

        # Download and load image
        response = requests.get(headshot_url, timeout=10)
        response.raise_for_status()

        headshot_img = Image.open(BytesIO(response.content))

        # Make circular if requested
        if circular:
            # Convert to RGBA
            if headshot_img.mode != "RGBA":
                headshot_img = headshot_img.convert("RGBA")

            # Create circular mask
            size = min(headshot_img.size)
            mask = Image.new("L", (size, size), 0)
            from PIL import ImageDraw

            draw = ImageDraw.Draw(mask)
            draw.ellipse((0, 0, size, size), fill=255)

            # Crop to square and apply mask
            left = (headshot_img.width - size) // 2
            top = (headshot_img.height - size) // 2
            headshot_img = headshot_img.crop((left, top, left + size, top + size))

            # Apply circular mask
            headshot_img.putalpha(mask)

        # Create OffsetImage
        imagebox = offsetbox.OffsetImage(
            headshot_img, zoom=width * ax.figure.dpi / 100, **kwargs
        )

        # Create AnnotationBbox
        ab = offsetbox.AnnotationBbox(
            imagebox, (x, y), frameon=False, transform=transform or ax.transAxes
        )

        # Add to axes
        ax.add_artist(ab)
        return ab

    except Exception as e:
        warnings.warn(f"Could not add headshot for {player_id}: {e}", stacklevel=2)
        return None


def set_xlabel_with_wordmarks(
    ax: plt.Axes,
    teams: list[str],
    positions: list[float] | None = None,
    wordmark_size: float = 0.06,
    text_labels: bool = False,
    **kwargs,
):
    """Replace x-axis labels with team wordmarks.

    Args:
        ax: matplotlib Axes
        teams: List of team abbreviations
        positions: X positions for wordmarks. If None, uses evenly spaced positions.
        wordmark_size: Size of wordmarks
        text_labels: Whether to keep text labels alongside wordmarks
        **kwargs: Additional arguments for wordmark placement
    """
    teams = validate_teams(teams)

    if positions is None:
        positions = np.linspace(0, len(teams) - 1, len(teams))

    if len(positions) != len(teams):
        msg = "Length of positions must match length of teams"
        raise ValueError(msg)

    # Clear existing x-axis labels
    if not text_labels:
        ax.set_xticklabels([])

    # Set x-axis ticks at positions
    ax.set_xticks(positions)

    # Add team wordmarks below x-axis
    y_offset = -0.15  # Position below axis

    for team, pos in zip(teams, positions):
        try:
            # Add wordmark
            add_team_wordmark(
                ax,
                team,
                pos,
                y_offset,
                width=wordmark_size,
                transform=ax.transData,
                **kwargs,
            )
        except Exception as e:
            warnings.warn(f"Could not add wordmark for {team}: {e}", stacklevel=2)

    # Adjust bottom margin to accommodate wordmarks
    plt.subplots_adjust(bottom=0.2)
