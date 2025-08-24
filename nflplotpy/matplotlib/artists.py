"""Custom matplotlib artists for NFL logos and headshots."""

from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
from matplotlib.artist import Artist
from matplotlib.offsetbox import AnnotationBbox, OffsetImage
from PIL import Image

from nflplotpy.core.logos import get_asset_manager, get_team_logo
from nflplotpy.core.utils import validate_teams

if TYPE_CHECKING:
    import matplotlib.pyplot as plt


def _warn_quantile_range(q: float) -> None:
    """Warn about quantile out of range."""
    import warnings

    warnings.warn(f"Quantile {q} not in range [0,1], skipping", stacklevel=3)


def _warn_unknown_stat_type(stat_type: str, available: list[str]) -> None:
    """Warn about unknown stat type."""
    import warnings

    warnings.warn(
        f"Unknown stat_type: {stat_type}. Available: {available}", stacklevel=3
    )


def _warn_unknown_line_type(line_type: str) -> None:
    """Warn about unknown line type."""
    import warnings

    warnings.warn(f"Unknown line_type: {line_type}", stacklevel=3)


def _raise_file_not_found(image_path) -> None:
    """Raise FileNotFoundError for missing file."""
    msg = f"Image file not found: {image_path}"
    raise FileNotFoundError(msg)


class NFLLogoArtist(Artist):
    """Custom matplotlib artist for rendering NFL logos."""

    def __init__(
        self,
        team: str,
        xy: tuple[float, float],
        width: float = 0.1,
        height: float | None = None,
        alpha: float = 1.0,
        zorder: int = 10,
    ):
        """Initialize NFL logo artist.

        Args:
            team: Team abbreviation
            xy: Position (x, y) in axes coordinates
            width: Logo width in axes coordinates
            height: Logo height in axes coordinates (if None, maintains aspect ratio)
            alpha: Transparency level (0-1)
            zorder: Drawing order
        """
        super().__init__()
        self.team = team.upper()
        self.xy = xy
        self.width = width
        self.height = height
        self.alpha = alpha
        self.zorder = zorder
        self._logo_image = None
        self._annotation_bbox = None

    def draw(self, renderer):
        """Draw the logo on the axes."""
        if self._logo_image is None:
            self._load_logo()

        if self._annotation_bbox is not None:
            self._annotation_bbox.draw(renderer)

    def _load_logo(self):
        """Load the team logo image."""
        try:
            # Get logo image
            pil_image = get_team_logo(self.team)

            # Convert to numpy array for matplotlib
            image_array = np.array(pil_image)

            # Create OffsetImage
            offset_image = OffsetImage(image_array, zoom=self.width, alpha=self.alpha)

            # Create AnnotationBbox
            self._annotation_bbox = AnnotationBbox(
                offset_image, self.xy, frameon=False, pad=0, zorder=self.zorder
            )

            self._logo_image = image_array

        except Exception:
            pass


def add_nfl_logo(
    ax: plt.Axes,
    team: str,
    x: float,
    y: float,
    width: float = 0.1,
    height: float | None = None,
    alpha: float = 1.0,
    zorder: int = 10,
    target_width_pixels: int | None = None,
    **kwargs,
) -> AnnotationBbox:
    """Add NFL team logo to matplotlib axes.

    Equivalent to nflplotR's geom_nfl_logos().

    Args:
        ax: Matplotlib axes
        team: Team abbreviation
        x: X position
        y: Y position
        width: Logo width (as fraction of axes width) - ignored if
            target_width_pixels is set
        height: Logo height (if None, maintains aspect ratio)
        alpha: Transparency level (0-1)
        zorder: Drawing order
        target_width_pixels: Target width in pixels for consistent sizing
            (overrides width parameter)
        **kwargs: Additional arguments passed to AnnotationBbox

    Returns:
        AnnotationBbox containing the logo

    Raises:
        ValueError: If team abbreviation is invalid
    """
    # Validate team
    validate_teams(team)

    try:
        # Get logo image
        pil_image = get_team_logo(team)

        # For adaptive sizing, resize the PIL image first before converting to numpy
        if target_width_pixels is not None:
            # Get original dimensions
            orig_width, orig_height = pil_image.size

            # Calculate new height maintaining aspect ratio
            aspect_ratio = orig_height / orig_width
            new_height = int(target_width_pixels * aspect_ratio)

            # Resize the PIL image to exact target dimensions
            pil_image = pil_image.resize(
                (target_width_pixels, new_height), Image.Resampling.LANCZOS
            )

            # Now use zoom=1 since we've already resized
            zoom = 1.0
        else:
            # Fallback to old method with zoom scaling
            zoom = width * 10

        # Convert PIL to numpy array after any resizing
        image_array = np.array(pil_image)

        # Create OffsetImage with calculated zoom
        offset_image = OffsetImage(image_array, zoom=zoom, alpha=alpha)

        # Create AnnotationBbox
        ab = AnnotationBbox(
            offset_image, (x, y), frameon=False, pad=0, zorder=zorder, **kwargs
        )

        # Add to axes
        ax.add_artist(ab)

        return ab

    except Exception:
        return None


def add_nfl_logos(
    ax: plt.Axes,
    teams: list[str],
    x: list[float] | np.ndarray,
    y: list[float] | np.ndarray,
    width: float = 0.1,
    target_width_pixels: int | None = None,
    **kwargs,
) -> list[AnnotationBbox]:
    """Add multiple NFL team logos to matplotlib axes.

    Args:
        ax: Matplotlib axes
        teams: List of team abbreviations
        x: X positions (must be same length as teams)
        y: Y positions (must be same length as teams)
        width: Logo width for all logos - ignored if target_width_pixels is set
        target_width_pixels: Target width in pixels for consistent sizing
            across all logos
        **kwargs: Additional arguments passed to add_nfl_logo

    Returns:
        List of AnnotationBbox objects

    Raises:
        ValueError: If arrays have different lengths
    """
    if len(teams) != len(x) or len(teams) != len(y):
        msg = "teams, x, and y must have the same length"
        raise ValueError(msg)

    annotations = []
    for team, xi, yi in zip(teams, x, y):
        ab = add_nfl_logo(
            ax,
            team,
            xi,
            yi,
            width=width,
            target_width_pixels=target_width_pixels,
            **kwargs,
        )
        if ab is not None:
            annotations.append(ab)

    return annotations


def add_nfl_headshot(
    ax: plt.Axes, player_id: str, x: float, y: float, width: float = 0.1, **kwargs
) -> AnnotationBbox | None:
    """Add NFL player headshot to matplotlib axes.

    Equivalent to nflplotR's geom_nfl_headshots().

    Args:
        ax: Matplotlib axes
        player_id: Player ID or name
        x: X position
        y: Y position
        width: Headshot width
        **kwargs: Additional arguments

    Returns:
        AnnotationBbox containing the headshot

    Note:
        Currently uses placeholder implementation.
    """
    try:
        # Get asset manager
        manager = get_asset_manager()
        pil_image = manager.get_headshot(player_id)

        # Convert PIL to numpy array
        image_array = np.array(pil_image)

        # Calculate zoom
        zoom = width * 10

        # Create OffsetImage
        offset_image = OffsetImage(image_array, zoom=zoom)

        # Create AnnotationBbox
        ab = AnnotationBbox(offset_image, (x, y), frameon=False, pad=0, **kwargs)

        # Add to axes
        ax.add_artist(ab)

        return ab

    except Exception:
        return None


def add_nfl_wordmark(
    ax: plt.Axes, team: str, x: float, y: float, width: float = 0.2, **kwargs
) -> AnnotationBbox | None:
    """Add NFL team wordmark to matplotlib axes.

    Equivalent to nflplotR's geom_nfl_wordmarks().

    Args:
        ax: Matplotlib axes
        team: Team abbreviation
        x: X position
        y: Y position
        width: Wordmark width
        **kwargs: Additional arguments

    Returns:
        AnnotationBbox containing the wordmark
    """
    validate_teams(team)

    try:
        # Get asset manager
        manager = get_asset_manager()
        pil_image = manager.get_wordmark(team)

        # Convert PIL to numpy array
        image_array = np.array(pil_image)

        # Calculate zoom
        zoom = width * 10

        # Create OffsetImage
        offset_image = OffsetImage(image_array, zoom=zoom)

        # Create AnnotationBbox
        ab = AnnotationBbox(offset_image, (x, y), frameon=False, pad=0, **kwargs)

        # Add to axes
        ax.add_artist(ab)

        return ab

    except Exception:
        return None


def add_median_lines(
    ax: plt.Axes, data: np.ndarray | list[float], axis: str = "both", **kwargs
):
    """Add median reference lines to plot.

    Equivalent to nflplotR's geom_median_lines().

    Args:
        ax: Matplotlib axes
        data: Data to calculate median from
        axis: Which axis to add lines ('x', 'y', 'both')
        **kwargs: Arguments passed to axhline/axvline
    """
    if isinstance(data, list):
        data = np.array(data)

    median_val = np.median(data)

    # Default line styling
    line_kwargs = {"color": "red", "linestyle": "--", "alpha": 0.7, "linewidth": 1}
    line_kwargs.update(kwargs)

    if axis in ["y", "both"]:
        ax.axhline(y=median_val, **line_kwargs)

    if axis in ["x", "both"]:
        ax.axvline(x=median_val, **line_kwargs)


def add_mean_lines(
    ax: plt.Axes, data: np.ndarray | list[float], axis: str = "both", **kwargs
):
    """Add mean reference lines to plot.

    Equivalent to nflplotR's geom_mean_lines().

    Args:
        ax: Matplotlib axes
        data: Data to calculate mean from
        axis: Which axis to add lines ('x', 'y', 'both')
        **kwargs: Arguments passed to axhline/axvline
    """
    if isinstance(data, list):
        data = np.array(data)

    mean_val = np.mean(data)

    # Default line styling
    line_kwargs = {"color": "blue", "linestyle": "-", "alpha": 0.7, "linewidth": 1}
    line_kwargs.update(kwargs)

    if axis in ["y", "both"]:
        ax.axhline(y=mean_val, **line_kwargs)

    if axis in ["x", "both"]:
        ax.axvline(x=mean_val, **line_kwargs)


def add_quantile_lines(
    ax: plt.Axes,
    data: np.ndarray | list[float],
    quantiles: list[float] | None = None,
    axis: str = "both",
    **kwargs,
):
    """Add quantile reference lines to plot.

    Args:
        ax: Matplotlib axes
        data: Data to calculate quantiles from
        quantiles: List of quantiles to show (0-1)
        axis: Which axis to add lines ('x', 'y', 'both')
        **kwargs: Arguments passed to axhline/axvline
    """
    if quantiles is None:
        quantiles = [0.25, 0.75]
    if isinstance(data, list):
        data = np.array(data)

    # Default line styling
    line_kwargs = {"color": "orange", "linestyle": ":", "alpha": 0.6, "linewidth": 1}
    line_kwargs.update(kwargs)

    for q in quantiles:
        if not 0 <= q <= 1:
            _warn_quantile_range(q)
            continue

        q_val = np.quantile(data, q)

        if axis in ["y", "both"]:
            ax.axhline(y=q_val, **line_kwargs)

        if axis in ["x", "both"]:
            ax.axvline(x=q_val, **line_kwargs)


def add_percentile_lines(
    ax: plt.Axes,
    data: np.ndarray | list[float],
    percentiles: list[int] | None = None,
    axis: str = "both",
    **kwargs,
):
    """Add percentile reference lines to plot.

    Args:
        ax: Matplotlib axes
        data: Data to calculate percentiles from
        percentiles: List of percentiles to show (0-100)
        axis: Which axis to add lines ('x', 'y', 'both')
        **kwargs: Arguments passed to axhline/axvline
    """
    # Convert percentiles to quantiles
    if percentiles is None:
        percentiles = [25, 75]
    quantiles = [p / 100 for p in percentiles]

    # Default styling for percentiles
    line_kwargs = {"color": "purple", "linestyle": "-.", "alpha": 0.5, "linewidth": 1}
    line_kwargs.update(kwargs)

    add_quantile_lines(ax, data, quantiles, axis, **line_kwargs)


def add_std_lines(
    ax: plt.Axes,
    data: np.ndarray | list[float],
    n_std: list[float] | None = None,
    axis: str = "both",
    center: str = "mean",
    **kwargs,
):
    """Add standard deviation reference lines to plot.

    Args:
        ax: Matplotlib axes
        data: Data to calculate std dev from
        n_std: List of standard deviation multipliers
        axis: Which axis to add lines ('x', 'y', 'both')
        center: Center point ('mean' or 'median')
        **kwargs: Arguments passed to axhline/axvline
    """
    if n_std is None:
        n_std = [1, 2]
    if isinstance(data, list):
        data = np.array(data)

    if center == "mean":
        center_val = np.mean(data)
    elif center == "median":
        center_val = np.median(data)
    else:
        msg = f"Invalid center: {center}. Must be 'mean' or 'median'"
        raise ValueError(msg)

    std_val = np.std(data)

    # Default line styling
    line_kwargs = {"color": "green", "linestyle": "--", "alpha": 0.4, "linewidth": 1}
    line_kwargs.update(kwargs)

    for n in n_std:
        upper_val = center_val + n * std_val
        lower_val = center_val - n * std_val

        if axis in ["y", "both"]:
            ax.axhline(y=upper_val, **line_kwargs)
            ax.axhline(y=lower_val, **line_kwargs)

        if axis in ["x", "both"]:
            ax.axvline(x=upper_val, **line_kwargs)
            ax.axvline(x=lower_val, **line_kwargs)


def add_iqr_lines(
    ax: plt.Axes,
    data: np.ndarray | list[float],
    axis: str = "both",
    show_outliers: bool = True,
    **kwargs,
):
    """Add interquartile range (IQR) reference lines to plot.

    Args:
        ax: Matplotlib axes
        data: Data to calculate IQR from
        axis: Which axis to add lines ('x', 'y', 'both')
        show_outliers: Whether to add outlier threshold lines
        **kwargs: Arguments passed to axhline/axvline
    """
    if isinstance(data, list):
        data = np.array(data)

    q1 = np.quantile(data, 0.25)
    q3 = np.quantile(data, 0.75)
    iqr = q3 - q1

    # Default line styling
    line_kwargs = {"color": "brown", "linestyle": "-", "alpha": 0.5, "linewidth": 1.5}
    line_kwargs.update(kwargs)

    # Add quartile lines
    if axis in ["y", "both"]:
        ax.axhline(y=q1, **line_kwargs)
        ax.axhline(y=q3, **line_kwargs)

    if axis in ["x", "both"]:
        ax.axvline(x=q1, **line_kwargs)
        ax.axvline(x=q3, **line_kwargs)

    # Add outlier threshold lines if requested
    if show_outliers:
        outlier_kwargs = line_kwargs.copy()
        outlier_kwargs.update({"linestyle": ":", "alpha": 0.3})

        lower_outlier = q1 - 1.5 * iqr
        upper_outlier = q3 + 1.5 * iqr

        if axis in ["y", "both"]:
            ax.axhline(y=lower_outlier, **outlier_kwargs)
            ax.axhline(y=upper_outlier, **outlier_kwargs)

        if axis in ["x", "both"]:
            ax.axvline(x=lower_outlier, **outlier_kwargs)
            ax.axvline(x=upper_outlier, **outlier_kwargs)


def add_reference_band(
    ax: plt.Axes,
    data: np.ndarray | list[float],
    band_type: str = "std",
    n_std: float = 1,
    quantiles: tuple[float, float] = (0.25, 0.75),
    axis: str = "y",
    alpha: float = 0.2,
    color: str = "gray",
    **kwargs,
):
    """Add reference band (shaded area) to plot.

    Args:
        ax: Matplotlib axes
        data: Data to calculate band from
        band_type: Type of band ('std', 'quantile', 'iqr')
        n_std: Number of standard deviations for 'std' band
        quantiles: Tuple of quantiles for 'quantile' band
        axis: Which axis for the band ('x' or 'y')
        alpha: Band transparency
        color: Band color
        **kwargs: Additional arguments for fill_between/fill_betweenx
    """
    if isinstance(data, list):
        data = np.array(data)

    if band_type == "std":
        center = np.mean(data)
        std = np.std(data)
        lower = center - n_std * std
        upper = center + n_std * std
    elif band_type == "quantile":
        lower = np.quantile(data, quantiles[0])
        upper = np.quantile(data, quantiles[1])
    elif band_type == "iqr":
        lower = np.quantile(data, 0.25)
        upper = np.quantile(data, 0.75)
    else:
        msg = f"Invalid band_type: {band_type}. Must be 'std', 'quantile', or 'iqr'"
        raise ValueError(msg)

    # Get axis limits for the band
    if axis == "y":
        xlim = ax.get_xlim()
        ax.fill_between(xlim, lower, upper, alpha=alpha, color=color, **kwargs)
    elif axis == "x":
        ylim = ax.get_ylim()
        ax.fill_betweenx(ylim, lower, upper, alpha=alpha, color=color, **kwargs)
    else:
        msg = f"Invalid axis: {axis}. Must be 'x' or 'y'"
        raise ValueError(msg)


def add_nfl_league_averages(
    ax: plt.Axes,
    stat_type: str,
    axis: str = "both",
    season: int | None = None,
    **kwargs,
):
    """Add NFL league average reference lines.

    Args:
        ax: Matplotlib axes
        stat_type: Type of statistic ('passing_yards', 'rushing_yards', etc.)
        axis: Which axis to add lines ('x', 'y', 'both')
        season: NFL season (if None, uses most recent)
        **kwargs: Arguments passed to axhline/axvline
    """
    # This would ideally pull from nfl_data_py or other data source
    # For now, we'll use some common NFL averages

    league_averages = {
        "passing_yards": 240,
        "passing_tds": 1.5,
        "rushing_yards": 120,
        "rushing_tds": 1.0,
        "points": 22,
        "total_yards": 360,
        "turnovers": 1.2,
        "sacks": 2.5,
    }

    if stat_type not in league_averages:
        _warn_unknown_stat_type(stat_type, list(league_averages.keys()))
        return

    avg_val = league_averages[stat_type]

    # Default NFL styling
    line_kwargs = {
        "color": "#013369",
        "linestyle": "-",
        "alpha": 0.8,
        "linewidth": 2,
        "label": f"NFL Avg ({stat_type})",
    }
    line_kwargs.update(kwargs)

    if axis in ["y", "both"]:
        ax.axhline(y=avg_val, **line_kwargs)

    if axis in ["x", "both"]:
        ax.axvline(x=avg_val, **line_kwargs)


def add_multiple_reference_lines(
    ax: plt.Axes,
    data: np.ndarray | list[float],
    line_types: list[str] | None = None,
    axis: str = "both",
    **kwargs,
):
    """Add multiple types of reference lines at once.

    Args:
        ax: Matplotlib axes
        data: Data to calculate references from
        line_types: Types of lines to add ('mean', 'median', 'quartiles', 'std')
        axis: Which axis to add lines ('x', 'y', 'both')
        **kwargs: Additional arguments
    """
    if line_types is None:
        line_types = ["mean", "median"]
    if isinstance(data, list):
        data = np.array(data)

    for line_type in line_types:
        if line_type == "mean":
            add_mean_lines(ax, data, axis, color="blue", linestyle="-", **kwargs)
        elif line_type == "median":
            add_median_lines(ax, data, axis, color="red", linestyle="--", **kwargs)
        elif line_type == "quartiles":
            add_quantile_lines(
                ax, data, [0.25, 0.75], axis, color="orange", linestyle=":", **kwargs
            )
        elif line_type == "std":
            add_std_lines(ax, data, [1], axis, color="green", linestyle="--", **kwargs)
        elif line_type == "iqr":
            add_iqr_lines(ax, data, axis, **kwargs)
        else:
            _warn_unknown_line_type(line_type)


def add_image_from_path(
    ax: plt.Axes,
    path: str,
    x: float,
    y: float,
    width: float = 0.1,
    height: float | None = None,
    alpha: float = 1.0,
    angle: float = 0.0,
    hjust: float = 0.5,
    vjust: float = 0.5,
    transform: plt.Transform | None = None,
    colorize: str | None = None,
    **kwargs,
) -> AnnotationBbox | None:
    """Add image from URL or file path to matplotlib plot.

    Equivalent to nflplotR/ggpath's geom_from_path(). Provides generic
    image placement capabilities for any image source.

    Args:
        ax: Matplotlib axes
        path: URL or local file path to image
        x: X position
        y: Y position
        width: Image width in axes coordinates
        height: Image height in axes coordinates (maintains aspect ratio if None)
        alpha: Transparency level (0-1)
        angle: Rotation angle in degrees
        hjust: Horizontal justification (0=left, 0.5=center, 1=right)
        vjust: Vertical justification (0=bottom, 0.5=center, 1=top)
        transform: Coordinate transform (defaults to ax.transAxes)
        colorize: Color to apply to image (hex color code)
        **kwargs: Additional arguments passed to AnnotationBbox

    Returns:
        AnnotationBbox containing the image, or None if loading failed

    Example:
        ```python
        # Add image from URL
        add_image_from_path(ax, 'https://example.com/image.png', 0.5, 0.5, width=0.2)

        # Add local image with rotation
        add_image_from_path(ax, './logo.png', 0.3, 0.7, width=0.1, angle=45)

        # Colorize image
        add_image_from_path(ax, 'image.png', 0.2, 0.8, colorize='#FF0000')
        ```
    """
    from io import BytesIO
    from pathlib import Path

    import requests
    from matplotlib import colors as mcolors
    from PIL import ImageEnhance

    try:
        # Load image from path or URL
        if path.startswith(("http://", "https://")):
            # Download from URL
            response = requests.get(path, timeout=30)
            response.raise_for_status()
            image = Image.open(BytesIO(response.content))
        else:
            # Load from local file
            image_path = Path(path).expanduser().resolve()
            if not image_path.exists():
                _raise_file_not_found(image_path)
            image = Image.open(image_path)

        # Convert to RGBA to handle all image types consistently
        if image.mode != "RGBA":
            image = image.convert("RGBA")

        # Apply colorization if specified
        if colorize is not None:
            # Convert colorize to RGB if hex
            if colorize.startswith("#"):
                colorize_rgb = mcolors.hex2color(colorize)
            else:
                colorize_rgb = mcolors.to_rgb(colorize)

            # Create colored overlay
            colored_image = Image.new(
                "RGBA", image.size, (*[int(c * 255) for c in colorize_rgb], 255)
            )

            # Blend with original using alpha channel as mask
            alpha_channel = image.split()[-1]  # Get alpha channel
            image = Image.composite(colored_image, image, alpha_channel)

        # Apply alpha if not 1.0
        if alpha != 1.0:
            # Adjust alpha channel
            alpha_channel = image.split()[-1]
            alpha_channel = ImageEnhance.Brightness(alpha_channel).enhance(alpha)
            image.putalpha(alpha_channel)

        # Apply rotation if specified
        if angle != 0:
            image = image.rotate(angle, expand=True, fillcolor=(0, 0, 0, 0))

        # Calculate size
        image_array = np.array(image)

        # Calculate zoom factor based on desired width
        # This is approximate and may need adjustment based on DPI
        zoom = width * ax.figure.dpi / max(image.size) * 0.01

        if height is not None:
            # If height specified, we need to adjust zoom differently
            height_zoom = height * ax.figure.dpi / max(image.size) * 0.01
            # Use average of width and height zooms
            zoom = (zoom + height_zoom) / 2

        # Create OffsetImage
        offset_image = OffsetImage(image_array, zoom=zoom)

        # Calculate position adjustments for hjust/vjust
        # These adjust the position based on justification
        x_offset = (hjust - 0.5) * width
        y_offset = (vjust - 0.5) * (height if height else width)

        adjusted_x = x + x_offset
        adjusted_y = y + y_offset

        # Create AnnotationBbox with proper positioning
        annotation_kwargs = {
            "frameon": False,
            "pad": 0,
        }
        annotation_kwargs.update(kwargs)

        ab = AnnotationBbox(
            offset_image,
            (adjusted_x, adjusted_y),
            transform=transform or ax.transAxes,
            **annotation_kwargs,
        )

        # Add to axes
        ax.add_artist(ab)
        return ab

    except Exception as e:
        import warnings

        warnings.warn(f"Could not load image from path '{path}': {e}", stacklevel=2)
        return None


def add_images_from_paths(
    ax: plt.Axes,
    paths: list[str],
    x: list[float] | np.ndarray,
    y: list[float] | np.ndarray,
    width: float | list[float] = 0.1,
    height: float | list[float] | None = None,
    alpha: float | list[float] = 1.0,
    angle: float | list[float] = 0.0,
    **kwargs,
) -> list[AnnotationBbox]:
    """Add multiple images from paths/URLs to matplotlib plot.

    Vectorized version of add_image_from_path() for multiple images.

    Args:
        ax: Matplotlib axes
        paths: List of URLs or file paths
        x: X positions (must match length of paths)
        y: Y positions (must match length of paths)
        width: Image width(s) - single value or list
        height: Image height(s) - single value, list, or None
        alpha: Alpha value(s) - single value or list
        angle: Rotation angle(s) - single value or list
        **kwargs: Additional arguments passed to add_image_from_path

    Returns:
        List of AnnotationBbox objects (None entries for failed loads)
    """
    # Convert inputs to lists if needed
    if not isinstance(x, (list, np.ndarray)):
        x = [x]
    if not isinstance(y, (list, np.ndarray)):
        y = [y]
    if not isinstance(width, (list, np.ndarray)):
        width = [width] * len(paths)
    if height is not None and not isinstance(height, (list, np.ndarray)):
        height = [height] * len(paths)
    if not isinstance(alpha, (list, np.ndarray)):
        alpha = [alpha] * len(paths)
    if not isinstance(angle, (list, np.ndarray)):
        angle = [angle] * len(paths)

    # Validate lengths
    n = len(paths)
    if len(x) != n or len(y) != n:
        msg = f"Length of x ({len(x)}) and y ({len(y)}) must match paths ({n})"
        raise ValueError(msg)

    if len(width) != n:
        msg = f"Length of width ({len(width)}) must match paths ({n})"
        raise ValueError(msg)

    if height is not None and len(height) != n:
        msg = f"Length of height ({len(height)}) must match paths ({n})"
        raise ValueError(msg)

    if len(alpha) != n or len(angle) != n:
        msg = f"Length of alpha and angle must match paths ({n})"
        raise ValueError(msg)

    # Add each image
    annotations = []
    for i in range(n):
        img_height = height[i] if height is not None else None

        ab = add_image_from_path(
            ax,
            paths[i],
            x[i],
            y[i],
            width=width[i],
            height=img_height,
            alpha=alpha[i],
            angle=angle[i],
            **kwargs,
        )
        annotations.append(ab)

    return annotations
