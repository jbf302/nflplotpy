"""Matplotlib integration for nflplotpy."""

from .artists import add_nfl_headshot, add_nfl_logo, add_nfl_wordmark
from .scales import apply_nfl_theme, nfl_color_scale

__all__ = [
    "add_nfl_headshot",
    "add_nfl_logo",
    "add_nfl_wordmark",
    "apply_nfl_theme",
    "nfl_color_scale",
]
