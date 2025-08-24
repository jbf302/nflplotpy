"""Custom plotly traces for NFL logos and headshots."""

from __future__ import annotations

import base64
from io import BytesIO

import numpy as np
import plotly.graph_objects as go

from nflplotpy.core.colors import get_team_colors
from nflplotpy.core.logos import get_asset_manager, get_team_logo
from nflplotpy.core.utils import validate_teams


def _raise_file_not_found(image_path) -> None:
    """Raise FileNotFoundError for missing file."""
    msg = f"Image file not found: {image_path}"
    raise FileNotFoundError(msg)


def _pil_to_base64(pil_image) -> str:
    """Convert PIL image to base64 string for plotly."""
    buffer = BytesIO()
    pil_image.save(buffer, format="PNG")
    img_str = base64.b64encode(buffer.getvalue()).decode()
    return f"data:image/png;base64,{img_str}"


def add_nfl_logo_trace(
    fig: go.Figure,
    team: str,
    x: float,
    y: float,
    size: float = 0.1,
    opacity: float = 1.0,
    layer: str = "above",
    **kwargs,
) -> go.Figure:
    """Add NFL team logo as image to plotly figure.

    Args:
        fig: Plotly figure
        team: Team abbreviation
        x: X position (in data coordinates)
        y: Y position (in data coordinates)
        size: Logo size (relative to plot)
        opacity: Logo opacity (0-1)
        layer: Image layer ('above', 'below')
        **kwargs: Additional arguments

    Returns:
        Updated plotly figure
    """
    # Validate team
    validate_teams(team)

    try:
        # Get logo image
        pil_image = get_team_logo(team)

        # Convert to base64
        img_base64 = _pil_to_base64(pil_image)

        # Add image to layout
        fig.add_layout_image(
            dict(
                source=img_base64,
                xref="x",
                yref="y",
                x=x,
                y=y,
                sizex=size,
                sizey=size,
                sizing="contain",
                opacity=opacity,
                layer=layer,
                xanchor="center",
                yanchor="middle",
                **kwargs,
            )
        )

        return fig

    except Exception:
        return fig


def add_nfl_logos_trace(
    fig: go.Figure,
    teams: list[str],
    x: list[float] | np.ndarray,
    y: list[float] | np.ndarray,
    size: float = 0.1,
    **kwargs,
) -> go.Figure:
    """Add multiple NFL team logos to plotly figure.

    Args:
        fig: Plotly figure
        teams: List of team abbreviations
        x: X positions
        y: Y positions
        size: Logo size for all logos
        **kwargs: Additional arguments

    Returns:
        Updated plotly figure

    Raises:
        ValueError: If arrays have different lengths
    """
    if len(teams) != len(x) or len(teams) != len(y):
        msg = "teams, x, and y must have the same length"
        raise ValueError(msg)

    for team, xi, yi in zip(teams, x, y):
        fig = add_nfl_logo_trace(fig, team, xi, yi, size=size, **kwargs)

    return fig


def add_nfl_headshot_trace(
    fig: go.Figure, player_id: str, x: float, y: float, size: float = 0.1, **kwargs
) -> go.Figure:
    """Add NFL player headshot to plotly figure.

    Args:
        fig: Plotly figure
        player_id: Player ID or name
        x: X position
        y: Y position
        size: Headshot size
        **kwargs: Additional arguments

    Returns:
        Updated plotly figure
    """
    try:
        # Get asset manager
        manager = get_asset_manager()
        pil_image = manager.get_headshot(player_id)

        # Convert to base64
        img_base64 = _pil_to_base64(pil_image)

        # Add image to layout
        fig.add_layout_image(
            dict(
                source=img_base64,
                xref="x",
                yref="y",
                x=x,
                y=y,
                sizex=size,
                sizey=size,
                sizing="contain",
                opacity=1.0,
                layer="above",
                xanchor="center",
                yanchor="middle",
                **kwargs,
            )
        )

        return fig

    except Exception:
        return fig


def create_team_scatter(
    teams: list[str],
    x: list[float],
    y: list[float],
    color_type: str = "primary",
    show_logos: bool = True,
    logo_size: float = 0.05,
    marker_size: float | None = None,
    **kwargs,
) -> go.Figure:
    """Create scatter plot with team colors and optional logos.

    Args:
        teams: List of team abbreviations
        x: X values
        y: Y values
        color_type: Type of team color to use
        show_logos: Whether to show team logos
        logo_size: Size of logos
        marker_size: Size of markers (if not showing logos)
        **kwargs: Additional arguments passed to go.Scatter

    Returns:
        Plotly figure with scatter plot
    """
    # Validate inputs
    if len(teams) != len(x) or len(teams) != len(y):
        msg = "teams, x, and y must have the same length"
        raise ValueError(msg)

    teams = validate_teams(teams)

    # Get team colors
    colors = get_team_colors(teams, color_type)

    # Create figure
    fig = go.Figure()

    if show_logos:
        # Create invisible scatter trace for hover info
        fig.add_trace(
            go.Scatter(
                x=x,
                y=y,
                mode="markers",
                marker={
                    "size": 20,
                    "color": "rgba(0,0,0,0)",  # Transparent
                    "line": {"width": 0},
                },
                text=teams,
                hovertemplate="<b>%{text}</b><br>X: %{x}<br>Y: %{y}<extra></extra>",
                showlegend=False,
                **kwargs,
            )
        )

        # Add logos
        fig = add_nfl_logos_trace(fig, teams, x, y, size=logo_size)

    else:
        # Create scatter with team colors
        marker_size = marker_size or 15

        fig.add_trace(
            go.Scatter(
                x=x,
                y=y,
                mode="markers",
                marker={
                    "size": marker_size,
                    "color": colors,
                    "line": {"width": 2, "color": "white"},
                },
                text=teams,
                hovertemplate="<b>%{text}</b><br>X: %{x}<br>Y: %{y}<extra></extra>",
                showlegend=False,
                **kwargs,
            )
        )

    return fig


def create_team_bar(
    teams: list[str],
    values: list[float],
    color_type: str = "primary",
    orientation: str = "v",
    show_logos: bool = False,
    **kwargs,
) -> go.Figure:
    """Create bar chart with team colors.

    Args:
        teams: List of team abbreviations
        values: Bar values
        color_type: Type of team color to use
        orientation: Bar orientation ('v' for vertical, 'h' for horizontal)
        show_logos: Whether to add team logos (experimental)
        **kwargs: Additional arguments passed to go.Bar

    Returns:
        Plotly figure with bar chart
    """
    # Validate inputs
    if len(teams) != len(values):
        msg = "teams and values must have the same length"
        raise ValueError(msg)

    teams = validate_teams(teams)

    # Get team colors
    colors = get_team_colors(teams, color_type)

    # Create figure
    fig = go.Figure()

    if orientation == "v":
        fig.add_trace(
            go.Bar(
                x=teams,
                y=values,
                marker_color=colors,
                text=teams,
                textposition="auto",
                **kwargs,
            )
        )
    else:  # horizontal
        fig.add_trace(
            go.Bar(
                x=values,
                y=teams,
                orientation="h",
                marker_color=colors,
                text=teams,
                textposition="auto",
                **kwargs,
            )
        )

    return fig


def add_median_lines(
    fig: go.Figure, data: list[float], axis: str = "both", **kwargs
) -> go.Figure:
    """Add median reference lines to plotly figure.

    Args:
        fig: Plotly figure
        data: Data to calculate median from
        axis: Which axis to add lines ('x', 'y', 'both')
        **kwargs: Arguments passed to add_hline/add_vline

    Returns:
        Updated plotly figure
    """
    median_val = np.median(data)

    # Default line styling
    line_kwargs = {
        "line_color": "red",
        "line_dash": "dash",
        "opacity": 0.7,
        "line_width": 1,
    }
    line_kwargs.update(kwargs)

    if axis in ["y", "both"]:
        fig.add_hline(y=median_val, **line_kwargs)

    if axis in ["x", "both"]:
        fig.add_vline(x=median_val, **line_kwargs)

    return fig


def add_mean_lines(
    fig: go.Figure, data: list[float], axis: str = "both", **kwargs
) -> go.Figure:
    """Add mean reference lines to plotly figure.

    Args:
        fig: Plotly figure
        data: Data to calculate mean from
        axis: Which axis to add lines ('x', 'y', 'both')
        **kwargs: Arguments passed to add_hline/add_vline

    Returns:
        Updated plotly figure
    """
    mean_val = np.mean(data)

    # Default line styling
    line_kwargs = {
        "line_color": "blue",
        "line_dash": "solid",
        "opacity": 0.7,
        "line_width": 1,
    }
    line_kwargs.update(kwargs)

    if axis in ["y", "both"]:
        fig.add_hline(y=mean_val, **line_kwargs)

    if axis in ["x", "both"]:
        fig.add_vline(x=mean_val, **line_kwargs)

    return fig


def add_image_from_path_trace(
    fig: go.Figure,
    path: str,
    x: float,
    y: float,
    size: float = 0.1,
    opacity: float = 1.0,
    layer: str = "above",
    **kwargs,
) -> go.Figure:
    """Add image from URL or path to plotly figure.

    Plotly equivalent of matplotlib's add_image_from_path.

    Args:
        fig: Plotly figure
        path: URL or local file path to image
        x: X position (in data coordinates)
        y: Y position (in data coordinates)
        size: Image size (relative to plot)
        opacity: Image opacity (0-1)
        layer: Image layer ('above', 'below')
        **kwargs: Additional arguments

    Returns:
        Updated plotly figure
    """
    from pathlib import Path

    import requests
    from PIL import Image

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

        # Convert to base64
        img_base64 = _pil_to_base64(image)

        # Add image to layout
        fig.add_layout_image(
            dict(
                source=img_base64,
                xref="x",
                yref="y",
                x=x,
                y=y,
                sizex=size,
                sizey=size,
                sizing="contain",
                opacity=opacity,
                layer=layer,
                xanchor="center",
                yanchor="middle",
                **kwargs,
            )
        )

        return fig

    except Exception as e:
        import warnings

        warnings.warn(f"Could not add image from path '{path}': {e}", stacklevel=2)
        return fig


def create_nfl_color_scale_plotly(
    teams: list[str], scale_type: str = "team", color_type: str = "primary", **kwargs
) -> dict:
    """Create plotly color scale from NFL teams.

    Args:
        teams: List of team abbreviations
        scale_type: Type of scale ('team', 'conference', 'division')
        color_type: Color type for team scale
        **kwargs: Additional arguments

    Returns:
        Dictionary suitable for plotly color mapping
    """
    from nflplotpy.matplotlib.scales import (
        scale_color_conference,
        scale_color_division,
        scale_color_nfl,
    )

    if scale_type == "team":
        return scale_color_nfl(teams, color_type=color_type, guide=False, **kwargs)
    if scale_type == "conference":
        return scale_color_conference(teams, guide=False, **kwargs)
    if scale_type == "division":
        return scale_color_division(teams, guide=False, **kwargs)
    msg = f"Unknown scale_type: {scale_type}"
    raise ValueError(msg)


def apply_nfl_color_scale_plotly(
    fig: go.Figure,
    teams: list[str],
    scale_type: str = "team",
    color_type: str = "primary",
    trace_selector: dict | None = None,
    **kwargs,
) -> go.Figure:
    """Apply NFL color scale to plotly figure traces.

    Args:
        fig: Plotly figure
        teams: List of team abbreviations
        scale_type: Type of scale ('team', 'conference', 'division')
        color_type: Color type for team scale
        trace_selector: Dictionary to select specific traces (optional)
        **kwargs: Additional arguments

    Returns:
        Updated plotly figure
    """
    # Get color mapping
    color_mapping = create_nfl_color_scale_plotly(
        teams, scale_type, color_type, **kwargs
    )
    colors = [color_mapping.get(team, "#888888") for team in teams]

    # Apply to traces
    for trace in fig.data:
        if trace_selector is None or all(
            getattr(trace, k, None) == v for k, v in trace_selector.items()
        ):
            if hasattr(trace, "marker") and trace.marker is not None:
                trace.marker.color = colors
            elif hasattr(trace, "line") and trace.line is not None:
                trace.line.color = colors

    return fig


def add_quantile_lines_plotly(
    fig: go.Figure,
    data: list[float],
    quantiles: list[float] | None = None,
    axis: str = "both",
    **kwargs,
) -> go.Figure:
    """Add quantile reference lines to plotly figure.

    Args:
        fig: Plotly figure
        data: Data to calculate quantiles from
        quantiles: List of quantiles to show (0-1)
        axis: Which axis to add lines ('x', 'y', 'both')
        **kwargs: Arguments passed to add_hline/add_vline

    Returns:
        Updated plotly figure
    """
    # Default line styling
    if quantiles is None:
        quantiles = [0.25, 0.75]
    line_kwargs = {
        "line_color": "orange",
        "line_dash": "dot",
        "opacity": 0.6,
        "line_width": 1,
    }
    line_kwargs.update(kwargs)

    for q in quantiles:
        if not 0 <= q <= 1:
            import warnings

            warnings.warn(f"Quantile {q} not in range [0,1], skipping", stacklevel=2)
            continue

        q_val = np.quantile(data, q)

        if axis in ["y", "both"]:
            fig.add_hline(y=q_val, **line_kwargs)

        if axis in ["x", "both"]:
            fig.add_vline(x=q_val, **line_kwargs)

    return fig


def add_reference_band_plotly(
    fig: go.Figure,
    data: list[float],
    band_type: str = "std",
    n_std: float = 1,
    quantiles: tuple[float, float] = (0.25, 0.75),
    axis: str = "y",
    fillcolor: str = "rgba(128,128,128,0.2)",
    **kwargs,
) -> go.Figure:
    """Add reference band (shaded area) to plotly figure.

    Args:
        fig: Plotly figure
        data: Data to calculate band from
        band_type: Type of band ('std', 'quantile', 'iqr')
        n_std: Number of standard deviations for 'std' band
        quantiles: Tuple of quantiles for 'quantile' band
        axis: Which axis for the band ('x' or 'y')
        fillcolor: Band color
        **kwargs: Additional arguments

    Returns:
        Updated plotly figure
    """

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

    # Add shape for the band
    if axis == "y":
        # Get x-axis range
        x_range = (
            fig.layout.xaxis.range
            if fig.layout.xaxis and fig.layout.xaxis.range
            else [-1, 1]
        )

        fig.add_shape(
            type="rect",
            x0=x_range[0],
            x1=x_range[1],
            y0=lower,
            y1=upper,
            fillcolor=fillcolor,
            line={"width": 0},
            layer="below",
            **kwargs,
        )
    elif axis == "x":
        # Get y-axis range
        y_range = (
            fig.layout.yaxis.range
            if fig.layout.yaxis and fig.layout.yaxis.range
            else [-1, 1]
        )

        fig.add_shape(
            type="rect",
            x0=lower,
            x1=upper,
            y0=y_range[0],
            y1=y_range[1],
            fillcolor=fillcolor,
            line={"width": 0},
            layer="below",
            **kwargs,
        )

    return fig


def create_interactive_team_plot(
    teams: list[str],
    x: list[float],
    y: list[float],
    hover_data: dict | None = None,
    plot_type: str = "scatter",
    show_logos: bool = True,
    color_scale: str = "team",
    **kwargs,
) -> go.Figure:
    """Create interactive NFL team plot with enhanced hover and click functionality.

    Args:
        teams: List of team abbreviations
        x: X values
        y: Y values
        hover_data: Additional data to show on hover
        plot_type: Type of plot ('scatter', 'bar')
        show_logos: Whether to show team logos
        color_scale: Color scale type ('team', 'conference', 'division')
        **kwargs: Additional arguments

    Returns:
        Interactive plotly figure
    """
    # Validate inputs
    if len(teams) != len(x) or len(teams) != len(y):
        msg = "teams, x, and y must have the same length"
        raise ValueError(msg)

    # Get colors
    color_mapping = create_nfl_color_scale_plotly(teams, color_scale)
    colors = [color_mapping.get(team, "#888888") for team in teams]

    # Create hover text
    hover_template = "<b>%{customdata[0]}</b><br>"
    hover_template += "X: %{x}<br>Y: %{y}<br>"

    customdata = [[team] for team in teams]

    if hover_data:
        for key, values in hover_data.items():
            hover_template += f"{key}: %{{customdata[{len(customdata[0])}]}}<br>"
            for i, val in enumerate(values):
                customdata[i].append(val)

    hover_template += "<extra></extra>"

    # Create figure based on plot type
    fig = go.Figure()

    if plot_type == "scatter":
        if show_logos:
            # Invisible points for hover + logos
            fig.add_trace(
                go.Scatter(
                    x=x,
                    y=y,
                    mode="markers",
                    marker={"size": 20, "color": "rgba(0,0,0,0)"},
                    customdata=customdata,
                    hovertemplate=hover_template,
                    showlegend=False,
                    **kwargs,
                )
            )

            # Add logos
            for team, xi, yi in zip(teams, x, y):
                add_nfl_logo_trace(fig, team, xi, yi, size=0.05)

        else:
            fig.add_trace(
                go.Scatter(
                    x=x,
                    y=y,
                    mode="markers",
                    marker={
                        "size": 15,
                        "color": colors,
                        "line": {"width": 2, "color": "white"},
                    },
                    customdata=customdata,
                    hovertemplate=hover_template,
                    showlegend=False,
                    **kwargs,
                )
            )

    elif plot_type == "bar":
        fig.add_trace(
            go.Bar(
                x=teams,
                y=y,
                marker_color=colors,
                customdata=customdata,
                hovertemplate=hover_template,
                **kwargs,
            )
        )

    return fig
