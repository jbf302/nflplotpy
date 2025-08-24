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

        # Fix palette mode issues while preserving transparency
        if wordmark_img.mode == "P":
            # Palette mode can cause color mapping issues - convert to RGBA to preserve transparency
            wordmark_img = wordmark_img.convert("RGBA")
        elif wordmark_img.mode in ["RGBA", "LA", "PA"]:
            # Already has alpha channel - just ensure RGBA mode
            wordmark_img = wordmark_img.convert("RGBA")
        else:
            # RGB or other modes - convert to RGBA for consistent transparency
            wordmark_img = wordmark_img.convert("RGBA")

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
    add_background: bool = True,
    background_alpha: float = 0.8,
    spacing_factor: float = 1.2,
    **kwargs,
):
    """Replace x-axis labels with team wordmarks.

    Args:
        ax: matplotlib Axes
        teams: List of team abbreviations
        positions: X positions for wordmarks. If None, uses evenly spaced positions.
        wordmark_size: Size of wordmarks
        text_labels: Whether to keep text labels alongside wordmarks
        add_background: Whether to add white background behind wordmarks for clarity
        background_alpha: Transparency of background (0=transparent, 1=opaque)
        spacing_factor: Multiplier for spacing between wordmarks
        **kwargs: Additional arguments for wordmark placement
    """
    teams = validate_teams(teams)

    if positions is None:
        # Add spacing between positions to prevent overlap
        total_width = len(teams) - 1
        positions = np.linspace(0, total_width, len(teams))

    if len(positions) != len(teams):
        msg = "Length of positions must match length of teams"
        raise ValueError(msg)

    # Clear existing x-axis labels
    if not text_labels:
        ax.set_xticklabels([])

    # Set x-axis ticks at positions
    ax.set_xticks(positions)

    # Calculate improved y-offset based on plot size
    ylim_range = ax.get_ylim()[1] - ax.get_ylim()[0]
    y_offset = -ylim_range * 0.08  # Dynamic offset based on y-range

    # Adjust wordmark size based on number of teams to prevent overlap
    adjusted_size = wordmark_size * min(1.0, 12.0 / len(teams))

    for team, pos in zip(teams, positions):
        try:
            # Add background circle/rectangle for better visibility
            if add_background:
                from matplotlib.patches import FancyBboxPatch

                # Calculate wordmark bounds for background
                bg_width = adjusted_size * ax.get_figure().get_figwidth() * 0.8
                bg_height = bg_width * 0.6  # Typical wordmark aspect ratio

                background = FancyBboxPatch(
                    (pos - bg_width / 2, y_offset - bg_height / 2),
                    bg_width,
                    bg_height,
                    boxstyle="round,pad=0.01",
                    facecolor="white",
                    edgecolor="lightgray",
                    alpha=background_alpha,
                    transform=ax.transData,
                    zorder=0,
                )
                ax.add_patch(background)

            # Add wordmark with improved positioning
            add_team_wordmark(
                ax,
                team,
                pos,
                y_offset,
                width=adjusted_size,
                transform=ax.transData,
                **kwargs,
            )
        except Exception as e:
            warnings.warn(f"Could not add wordmark for {team}: {e}", stacklevel=2)

    # Dynamically adjust bottom margin based on content
    current_bottom = plt.rcParams.get("figure.subplot.bottom", 0.1)
    new_bottom = max(current_bottom, 0.25 if len(teams) > 16 else 0.2)
    plt.subplots_adjust(bottom=new_bottom)


def replace_legend_text_with_logos(
    ax: plt.Axes,
    team_mapping: dict[str, str],
    logo_size: float = 0.04,
    **kwargs,
):
    """Replace legend text labels with team logos.

    Args:
        ax: matplotlib Axes
        team_mapping: Dictionary mapping legend labels to team abbreviations
        logo_size: Size of logos in legend
        **kwargs: Additional arguments for logo placement
    """
    legend = ax.get_legend()
    if legend is None:
        warnings.warn("No legend found on axes", stacklevel=2)
        return

    # Get legend information
    legend_texts = [text.get_text() for text in legend.get_texts()]

    # Replace matching text with logos
    for i, text_label in enumerate(legend_texts):
        if text_label in team_mapping:
            team = team_mapping[text_label]
            try:
                # Get legend text position
                text_obj = legend.get_texts()[i]

                # Hide original text
                text_obj.set_visible(False)

                # Get position in figure coordinates
                bbox = text_obj.get_window_extent()
                fig = ax.get_figure()

                # Convert to figure coordinates
                x_fig = bbox.x0 / fig.get_figwidth()
                y_fig = bbox.y0 / fig.get_figheight()

                # Add logo at text position
                add_nfl_logo(
                    ax,
                    team,
                    x_fig,
                    y_fig,
                    width=logo_size,
                    transform=fig.transFigure,
                    **kwargs,
                )
            except Exception as e:
                warnings.warn(
                    f"Could not replace legend text with logo for {team}: {e}",
                    stacklevel=2,
                )


def set_facet_labels_with_logos(
    fig: plt.Figure,
    axes_grid: list[plt.Axes] | np.ndarray,
    team_mapping: dict[str, str],
    logo_size: float = 0.06,
    position: str = "top",
    **kwargs,
):
    """Replace facet/subplot labels with team logos.

    Args:
        fig: matplotlib Figure
        axes_grid: Grid of axes (from subplots)
        team_mapping: Dictionary mapping subplot titles to team abbreviations
        logo_size: Size of logos
        position: Where to place logos ('top', 'right', 'left', 'bottom')
        **kwargs: Additional arguments for logo placement
    """
    # Flatten axes grid if needed
    if isinstance(axes_grid, np.ndarray):
        axes_list = axes_grid.flatten()
    else:
        axes_list = axes_grid

    for ax in axes_list:
        title_text = ax.get_title()

        if title_text in team_mapping:
            team = team_mapping[title_text]

            try:
                # Hide original title
                ax.set_title("")

                # Position logo based on location
                if position == "top":
                    logo_x, logo_y = 0.5, 1.1
                elif position == "right":
                    logo_x, logo_y = 1.1, 0.5
                elif position == "left":
                    logo_x, logo_y = -0.1, 0.5
                elif position == "bottom":
                    logo_x, logo_y = 0.5, -0.1
                else:
                    logo_x, logo_y = 0.5, 1.1  # Default to top

                # Add team logo
                add_nfl_logo(
                    ax,
                    team,
                    logo_x,
                    logo_y,
                    width=logo_size,
                    transform=ax.transAxes,
                    **kwargs,
                )
            except Exception as e:
                warnings.warn(
                    f"Could not replace facet label with logo for {team}: {e}",
                    stacklevel=2,
                )


def add_logo_to_colorbar(
    fig: plt.Figure,
    colorbar,
    team: str,
    position: str = "top",
    logo_size: float = 0.05,
    **kwargs,
):
    """Add team logo to colorbar.

    Args:
        fig: matplotlib Figure
        colorbar: Colorbar object
        team: Team abbreviation
        position: Where to place logo relative to colorbar
        logo_size: Size of logo
        **kwargs: Additional arguments for logo placement
    """
    try:
        # Get colorbar axes position
        cbar_ax = colorbar.ax
        cbar_bbox = cbar_ax.get_position()

        # Calculate logo position based on colorbar location
        if position == "top":
            logo_x = cbar_bbox.x0 + cbar_bbox.width / 2
            logo_y = cbar_bbox.y1 + 0.05
        elif position == "bottom":
            logo_x = cbar_bbox.x0 + cbar_bbox.width / 2
            logo_y = cbar_bbox.y0 - 0.05
        elif position == "left":
            logo_x = cbar_bbox.x0 - 0.05
            logo_y = cbar_bbox.y0 + cbar_bbox.height / 2
        elif position == "right":
            logo_x = cbar_bbox.x1 + 0.05
            logo_y = cbar_bbox.y0 + cbar_bbox.height / 2
        else:
            logo_x = cbar_bbox.x1 + 0.05
            logo_y = cbar_bbox.y0 + cbar_bbox.height / 2

        # Add logo in figure coordinates
        add_nfl_logo(
            cbar_ax,
            team,
            logo_x,
            logo_y,
            width=logo_size,
            transform=fig.transFigure,
            **kwargs,
        )

    except Exception as e:
        warnings.warn(f"Could not add logo to colorbar: {e}", stacklevel=2)


def create_logo_legend(
    ax: plt.Axes,
    teams: list[str],
    labels: list[str] | None = None,
    ncols: int = 1,
    logo_size: float = 0.04,
    spacing: float = 0.02,
    title: str | None = None,
    loc: str = "best",
    **kwargs,
) -> plt.Artist:
    """Create a legend using team logos instead of standard legend elements.

    Args:
        ax: matplotlib Axes
        teams: List of team abbreviations
        labels: Custom labels for each team (if None, uses team abbreviations)
        ncols: Number of columns in legend
        logo_size: Size of team logos
        spacing: Spacing between legend items
        title: Legend title
        loc: Legend location
        **kwargs: Additional arguments

    Returns:
        Legend-like artist (actually a collection of logos and text)
    """
    teams = validate_teams(teams)

    if labels is None:
        labels = teams

    if len(labels) != len(teams):
        msg = f"Length of labels ({len(labels)}) must match teams ({len(teams)})"
        raise ValueError(msg)

    try:
        # Calculate legend position
        if loc == "best":
            # Simple heuristic for best position
            loc = "upper right"

        # Position mapping
        positions = {
            "upper right": (0.95, 0.95),
            "upper left": (0.05, 0.95),
            "lower right": (0.95, 0.05),
            "lower left": (0.05, 0.05),
            "center": (0.5, 0.5),
        }

        base_x, base_y = positions.get(loc, (0.95, 0.95))

        # Calculate grid layout
        n_teams = len(teams)
        nrows = int(np.ceil(n_teams / ncols))

        # Add background rectangle (optional)
        from matplotlib.patches import FancyBboxPatch

        legend_width = ncols * (logo_size + spacing) + spacing
        legend_height = nrows * (logo_size + spacing) + spacing

        if title:
            legend_height += 0.03  # Extra space for title

        # Adjust position based on location
        if "right" in loc:
            rect_x = base_x - legend_width
        else:
            rect_x = base_x

        if "upper" in loc:
            rect_y = base_y - legend_height
        else:
            rect_y = base_y

        # Add background
        bg_rect = FancyBboxPatch(
            (rect_x, rect_y),
            legend_width,
            legend_height,
            boxstyle="round,pad=0.01",
            facecolor="white",
            edgecolor="gray",
            alpha=0.9,
            transform=ax.transAxes,
            zorder=1000,
        )
        ax.add_patch(bg_rect)

        # Add title if provided
        if title:
            title_x = rect_x + legend_width / 2
            title_y = rect_y + legend_height - 0.02
            ax.text(
                title_x,
                title_y,
                title,
                transform=ax.transAxes,
                ha="center",
                va="top",
                fontweight="bold",
                zorder=1001,
            )

        # Add logos and labels
        for i, (team, label) in enumerate(zip(teams, labels)):
            row = i // ncols
            col = i % ncols

            # Calculate position
            logo_x = rect_x + spacing + col * (logo_size + spacing) + logo_size / 2
            logo_y = (
                rect_y
                + legend_height
                - spacing
                - row * (logo_size + spacing)
                - logo_size / 2
            )

            if title:
                logo_y -= 0.03

            # Add logo
            add_nfl_logo(
                ax,
                team,
                logo_x,
                logo_y,
                width=logo_size,
                transform=ax.transAxes,
                zorder=1001,
                **kwargs,
            )

            # Add text label next to logo
            text_x = logo_x + logo_size / 2 + 0.01
            ax.text(
                text_x,
                logo_y,
                label,
                transform=ax.transAxes,
                ha="left",
                va="center",
                fontsize=8,
                zorder=1001,
            )

        return bg_rect

    except Exception as e:
        warnings.warn(f"Could not create logo legend: {e}", stacklevel=2)
        return None


def replace_tick_labels_with_images(
    ax: plt.Axes,
    axis: str,
    image_mapping: dict[str, str],
    image_size: float = 0.04,
    **kwargs,
):
    """Replace tick labels with images from URLs or paths.

    Generic version of set_xlabel_with_logos that works with any images.

    Args:
        ax: matplotlib Axes
        axis: Which axis to modify ('x' or 'y')
        image_mapping: Dictionary mapping tick labels to image URLs/paths
        image_size: Size of images
        **kwargs: Additional arguments for image placement
    """
    from .artists import add_image_from_path

    if axis == "x":
        tick_labels = [label.get_text() for label in ax.get_xticklabels()]
        tick_positions = ax.get_xticks()
        ax.set_xticklabels([])  # Clear original labels

        y_offset = -0.1  # Below x-axis

        for pos, label in zip(tick_positions, tick_labels):
            if label in image_mapping:
                image_path = image_mapping[label]
                add_image_from_path(
                    ax,
                    image_path,
                    pos,
                    y_offset,
                    width=image_size,
                    transform=ax.transData,
                    **kwargs,
                )

    elif axis == "y":
        tick_labels = [label.get_text() for label in ax.get_yticklabels()]
        tick_positions = ax.get_yticks()
        ax.set_yticklabels([])  # Clear original labels

        x_offset = -0.1  # Left of y-axis

        for pos, label in zip(tick_positions, tick_labels):
            if label in image_mapping:
                image_path = image_mapping[label]
                add_image_from_path(
                    ax,
                    image_path,
                    x_offset,
                    pos,
                    width=image_size,
                    transform=ax.transData,
                    **kwargs,
                )
    else:
        msg = f"Invalid axis: {axis}. Must be 'x' or 'y'"
        raise ValueError(msg)
