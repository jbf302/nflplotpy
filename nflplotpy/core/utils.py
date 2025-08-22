"""Utility functions for nflplotpy."""

from __future__ import annotations

import warnings
from typing import Any

import numpy as np
import pandas as pd

from .logos import get_available_teams, get_conference_teams


def team_factor(
    teams: list[str] | pd.Series, levels: list[str] | None = None
) -> pd.Categorical:
    """Create categorical factor for NFL teams with proper ordering.

    Equivalent to nflplotR's nfl_team_factor().

    Args:
        teams: List or Series of team abbreviations
        levels: Custom ordering for teams. If None, uses alphabetical.

    Returns:
        pandas Categorical with proper team ordering

    Raises:
        ValueError: If any team abbreviation is invalid
    """
    if isinstance(teams, pd.Series):
        teams = teams.tolist()

    # Validate all teams
    available_teams = [*get_available_teams(), "AFC", "NFC", "NFL"]
    invalid_teams = [t for t in teams if t.upper() not in available_teams]
    if invalid_teams:
        msg = f"Invalid team abbreviations: {invalid_teams}"
        raise ValueError(msg)

    # Normalize to uppercase
    teams = [t.upper() for t in teams]

    # Set levels (categories)
    if levels is None:
        # Default alphabetical ordering of all NFL teams
        levels = sorted(available_teams)
    else:
        levels = [t.upper() for t in levels]

    return pd.Categorical(teams, categories=levels, ordered=True)


def team_tiers(
    method: str = "draft_order", season: int | None = None
) -> dict[str, list[str]]:
    """Create NFL team tiers based on various ranking methods.

    Equivalent to nflplotR's nfl_team_tiers().

    Args:
        method: Method for creating tiers ('draft_order', 'conference', 'division',
            'random')
        season: Season year for data-based methods (not used in basic implementation)

    Returns:
        Dictionary mapping tier names to lists of team abbreviations

    Raises:
        ValueError: If method is not supported
    """
    available_teams = get_available_teams()

    if method == "draft_order":
        # Reverse draft order (best teams first)
        # This is a simplified implementation - real version would use actual standings
        np.random.seed(42)  # For reproducible "random" draft order
        shuffled_teams = np.random.permutation(available_teams).tolist()

        n_teams = len(shuffled_teams)
        tier_size = n_teams // 4

        return {
            "Tier 1": shuffled_teams[:tier_size],
            "Tier 2": shuffled_teams[tier_size : 2 * tier_size],
            "Tier 3": shuffled_teams[2 * tier_size : 3 * tier_size],
            "Tier 4": shuffled_teams[3 * tier_size :],
        }

    if method == "conference":
        return {"AFC": get_conference_teams("AFC"), "NFC": get_conference_teams("NFC")}

    if method == "division":
        return {
            "AFC East": ["BUF", "MIA", "NE", "NYJ"],
            "AFC North": ["BAL", "CIN", "CLE", "PIT"],
            "AFC South": ["HOU", "IND", "JAC", "TEN"],
            "AFC West": ["DEN", "KC", "LV", "LAC"],
            "NFC East": ["DAL", "NYG", "PHI", "WAS"],
            "NFC North": ["CHI", "DET", "GB", "MIN"],
            "NFC South": ["ATL", "CAR", "NO", "TB"],
            "NFC West": ["ARI", "LAR", "SEA", "SF"],
        }

    if method == "random":
        np.random.shuffle(available_teams)
        n_teams = len(available_teams)
        tier_size = n_teams // 4

        return {
            "Random Tier 1": available_teams[:tier_size],
            "Random Tier 2": available_teams[tier_size : 2 * tier_size],
            "Random Tier 3": available_teams[2 * tier_size : 3 * tier_size],
            "Random Tier 4": available_teams[3 * tier_size :],
        }

    msg = f"Unsupported method: {method}"
    raise ValueError(msg)


def validate_teams(teams: str | list[str], allow_conferences: bool = True) -> list[str]:
    """Validate and normalize team abbreviations.

    Args:
        teams: Team abbreviation(s) to validate
        allow_conferences: Whether to allow 'AFC', 'NFC', 'NFL'

    Returns:
        List of normalized (uppercase) team abbreviations

    Raises:
        ValueError: If any team abbreviation is invalid
    """
    if isinstance(teams, str):
        teams = [teams]

    # Normalize to uppercase
    teams = [t.upper() for t in teams]

    # Get valid teams
    valid_teams = get_available_teams()
    if allow_conferences:
        valid_teams.extend(["AFC", "NFC", "NFL"])

    # Check for invalid teams
    invalid_teams = [t for t in teams if t not in valid_teams]
    if invalid_teams:
        msg = f"Invalid team abbreviations: {invalid_teams}"
        raise ValueError(msg)

    return teams


def get_team_info(teams: str | list[str] | None = None) -> pd.DataFrame:
    """Get comprehensive team information.

    Args:
        teams: Specific teams to get info for. If None, returns all teams.

    Returns:
        DataFrame with team information including colors, conference, division
    """
    from .colors import NFL_TEAM_COLORS

    if teams is None:
        teams = get_available_teams()
    else:
        teams = validate_teams(teams, allow_conferences=False)

    # Create team info DataFrame
    team_data = []

    # Simplified division mappings
    divisions = {
        "BUF": "AFC East",
        "MIA": "AFC East",
        "NE": "AFC East",
        "NYJ": "AFC East",
        "BAL": "AFC North",
        "CIN": "AFC North",
        "CLE": "AFC North",
        "PIT": "AFC North",
        "HOU": "AFC South",
        "IND": "AFC South",
        "JAC": "AFC South",
        "TEN": "AFC South",
        "DEN": "AFC West",
        "KC": "AFC West",
        "LV": "AFC West",
        "LAC": "AFC West",
        "DAL": "NFC East",
        "NYG": "NFC East",
        "PHI": "NFC East",
        "WAS": "NFC East",
        "CHI": "NFC North",
        "DET": "NFC North",
        "GB": "NFC North",
        "MIN": "NFC North",
        "ATL": "NFC South",
        "CAR": "NFC South",
        "NO": "NFC South",
        "TB": "NFC South",
        "ARI": "NFC West",
        "LAR": "NFC West",
        "SEA": "NFC West",
        "SF": "NFC West",
    }

    # Team full names
    team_names = {
        "ARI": "Arizona Cardinals",
        "ATL": "Atlanta Falcons",
        "BAL": "Baltimore Ravens",
        "BUF": "Buffalo Bills",
        "CAR": "Carolina Panthers",
        "CHI": "Chicago Bears",
        "CIN": "Cincinnati Bengals",
        "CLE": "Cleveland Browns",
        "DAL": "Dallas Cowboys",
        "DEN": "Denver Broncos",
        "DET": "Detroit Lions",
        "GB": "Green Bay Packers",
        "HOU": "Houston Texans",
        "IND": "Indianapolis Colts",
        "JAC": "Jacksonville Jaguars",
        "KC": "Kansas City Chiefs",
        "LV": "Las Vegas Raiders",
        "LAC": "Los Angeles Chargers",
        "LAR": "Los Angeles Rams",
        "MIA": "Miami Dolphins",
        "MIN": "Minnesota Vikings",
        "NE": "New England Patriots",
        "NO": "New Orleans Saints",
        "NYG": "New York Giants",
        "NYJ": "New York Jets",
        "PHI": "Philadelphia Eagles",
        "PIT": "Pittsburgh Steelers",
        "SEA": "Seattle Seahawks",
        "SF": "San Francisco 49ers",
        "TB": "Tampa Bay Buccaneers",
        "TEN": "Tennessee Titans",
        "WAS": "Washington Commanders",
    }

    for team in teams:
        division = divisions.get(team, "Unknown")
        conference = division.split()[0] if division != "Unknown" else "Unknown"

        team_data.append(
            {
                "team_abbr": team,
                "team_name": team_names.get(team, f"{team} Team"),
                "conference": conference,
                "division": division,
                "primary_color": NFL_TEAM_COLORS[team]["primary"],
                "secondary_color": NFL_TEAM_COLORS[team]["secondary"],
                "tertiary_color": NFL_TEAM_COLORS[team]["tertiary"],
                "quaternary_color": NFL_TEAM_COLORS[team]["quaternary"],
            }
        )

    return pd.DataFrame(team_data)


def clean_team_abbreviations(
    data: pd.DataFrame, team_column: str = "team"
) -> pd.DataFrame:
    """Clean and normalize team abbreviations in a DataFrame.

    Args:
        data: DataFrame containing team data
        team_column: Name of column containing team abbreviations

    Returns:
        DataFrame with normalized team abbreviations

    Raises:
        ValueError: If team_column doesn't exist or contains invalid teams
    """
    if team_column not in data.columns:
        msg = f"Column '{team_column}' not found in DataFrame"
        raise ValueError(msg)

    df = data.copy()

    # Normalize team abbreviations
    from .logos import normalize_team_abbreviation

    try:
        df[team_column] = df[team_column].apply(
            lambda x: normalize_team_abbreviation(str(x)) if pd.notna(x) else x
        )
    except ValueError as e:
        msg = f"Error normalizing teams in column '{team_column}': {e}"
        raise ValueError(msg)

    return df


def get_nflverse_info() -> dict[str, Any]:
    """Get information about nflplotpy and nflverse ecosystem.

    Returns:
        Dictionary with package and ecosystem information
    """
    return {
        "package": "nflplotpy",
        "version": "0.1.0",
        "description": "Python NFL visualization package - equivalent to R's nflplotR",
        "ecosystem": "nflverse",
        "companion_packages": [
            "nfl_data_py",
            "nflreadr (R)",
            "nflplotR (R)",
            "nflfastR (R)",
        ],
        "data_sources": [
            "nflverse/nflverse-data",
            "Lee Sharpe's nfldata",
            "Wikipedia",
            "ESPN",
        ],
        "supported_backends": ["matplotlib", "plotly", "seaborn"],
    }


def nfl_sitrep() -> None:
    """Print comprehensive system and package information.

    Equivalent to R's nflverse_sitrep().
    """
    print("🏈 nflplotpy System Report")
    print("=" * 50)

    # Package information
    pkg_info = get_nflverse_info()
    print(f"\nPackage: {pkg_info['package']} v{pkg_info['version']}")
    print(f"Description: {pkg_info['description']}")
    print(f"Ecosystem: {pkg_info['ecosystem']}")

    # System information
    import sys

    print(f"\nPython: {sys.version}")
    print(f"Platform: {sys.platform}")

    # Core dependencies
    print("\nCore Dependencies:")
    core_deps = ["pandas", "numpy", "matplotlib", "PIL"]
    for dep in core_deps:
        try:
            module = __import__(dep)
            print(f"  {dep}: {module.__version__}")
        except ImportError:
            print(f"  {dep}: Not installed")
        except AttributeError:
            print(f"  {dep}: Installed (version unavailable)")

    # Optional dependencies
    print("\nOptional Dependencies:")
    optional_deps = []

    try:
        import plotly

        optional_deps.append(f"  plotly: {plotly.__version__}")
    except ImportError:
        optional_deps.append("  plotly: Not installed")

    try:
        import seaborn as sns

        optional_deps.append(f"  seaborn: {sns.__version__}")
    except ImportError:
        optional_deps.append("  seaborn: Not installed")

    try:
        import PIL

        optional_deps.append(f"  PIL/Pillow: {PIL.__version__}")
    except ImportError:
        optional_deps.append("  PIL/Pillow: Not installed")

    try:
        import requests

        optional_deps.append(f"  requests: {requests.__version__}")
    except ImportError:
        optional_deps.append("  requests: Not installed")

    for dep in optional_deps:
        print(dep)

    # Asset cache information
    print("\nAsset Cache:")
    try:
        from .assets import NFLAssetManager

        manager = NFLAssetManager()
        cache_info = manager.get_cache_info()
        print(f"  Cache directory: {cache_info['cache_dir']}")
        print(f"  Logos cached: {cache_info['logos_count']}")
        print(f"  Headshots cached: {cache_info['headshots_count']}")
        print(f"  Wordmarks cached: {cache_info['wordmarks_count']}")
        print(f"  Total cache size: {cache_info['total_size_bytes']} bytes")

    except Exception as e:
        print(f"  Error accessing cache: {e}")

    # Team data availability
    teams = get_available_teams()
    print("\nTeam Data:")
    print(f"  Available teams: {len(teams)}")
    print(f"  Sample teams: {teams[:5]}")

    # URL availability (sample check)
    print("\nURL Connectivity:")
    try:
        from .urls import get_url_manager

        manager = get_url_manager()

        # Test a few logo URLs
        import requests

        test_teams = ["KC", "BUF", "SF"]
        working_urls = 0

        for team in test_teams:
            try:
                url = manager.get_logo_url(team)
                response = requests.head(url, timeout=5)
                if response.status_code < 400:
                    working_urls += 1
            except Exception:
                pass

        print(f"  Logo URLs tested: {len(test_teams)}")
        print(f"  Working URLs: {working_urls}")

    except Exception as e:
        print(f"  Error testing URLs: {e}")

    # Plotting backends
    print("\nPlotting Backends:")
    backends = pkg_info["supported_backends"]
    for backend in backends:
        if backend == "matplotlib":
            print(f"  {backend}: Available")
        elif backend == "plotly":
            try:
                import plotly

                print(f"  {backend}: Available (v{plotly.__version__})")
            except ImportError:
                print(f"  {backend}: Not installed")
        elif backend == "seaborn":
            try:
                import seaborn as sns

                print(f"  {backend}: Available (v{sns.__version__})")
            except ImportError:
                print(f"  {backend}: Not installed")

    # Integration status
    print("\nIntegration Status:")
    try:
        import nfl_data_py

        print(f"  nfl_data_py: Available (v{nfl_data_py.__version__})")
    except ImportError:
        print("  nfl_data_py: Not installed")

    # Jupyter notebook detection
    print("\nEnvironment:")
    try:
        from IPython import get_ipython

        if get_ipython() is not None:
            print("  Running in: Jupyter/IPython")
        else:
            print("  Running in: Standard Python")
    except ImportError:
        print("  Running in: Standard Python")

    # Recommendations
    print("\nRecommendations:")
    recommendations = []

    try:
        import plotly
    except ImportError:
        recommendations.append(
            "Install plotly for interactive plots: pip install plotly"
        )

    try:
        import seaborn as sns
    except ImportError:
        recommendations.append(
            "Install seaborn for enhanced styling: pip install seaborn"
        )

    try:
        import nfl_data_py
    except ImportError:
        recommendations.append(
            "Install nfl_data_py for NFL data: pip install nfl_data_py"
        )

    if recommendations:
        for rec in recommendations:
            print(f"  • {rec}")
    else:
        print("  All recommended packages are installed! 🎉")

    print("\n" + "=" * 50)
    print("Report complete! Package is ready to use.")


def clear_all_cache() -> None:
    """Clear all nflplotpy caches.

    Clears logos, headshots, wordmarks, and any other cached assets.
    """
    try:
        from .assets import NFLAssetManager

        manager = NFLAssetManager()
        manager.get_cache_info()

        manager.clear_cache()

        manager.get_cache_info()

    except Exception:
        pass


def validate_player_ids(player_ids: list[str | int]) -> dict[str, bool]:
    """Validate player IDs for headshot availability.

    Args:
        player_ids: List of player IDs to validate

    Returns:
        Dictionary mapping player IDs to availability status

    Note:
        Currently checks format only. Full implementation would
        verify against ESPN/NFL databases.
    """
    results = {}

    for pid in player_ids:
        try:
            # Basic validation - ESPN IDs are typically numeric
            str_id = str(pid).strip()
            if str_id.isdigit() and len(str_id) >= 4:
                results[str_id] = True  # Assume valid for now
            else:
                results[str_id] = False
        except Exception:
            results[str(pid)] = False

    return results


def get_player_team_mapping(season: int = 2024) -> dict[str, str]:
    """Get mapping of player names/IDs to current teams.

    Args:
        season: Season year for team assignments

    Returns:
        Dictionary mapping player identifiers to team abbreviations

    Note:
        This is a placeholder implementation. Full implementation would
        integrate with nfl_data_py roster data.
    """
    # Placeholder implementation with a few known players
    # Real implementation would query nfl_data_py roster data

    sample_mapping = {
        "Patrick Mahomes": "KC",
        "Josh Allen": "BUF",
        "Lamar Jackson": "BAL",
        "Dak Prescott": "DAL",
        "Tua Tagovailoa": "MIA",
        "Aaron Rodgers": "NYJ",
        "Russell Wilson": "DEN",
        "Kyler Murray": "ARI",
    }

    warnings.warn(
        f"Player-team mapping not fully implemented for {season}. Using sample data.",
        stacklevel=2,
    )
    return sample_mapping


def discover_team_from_colors(hex_color: str) -> str | None:
    """Find NFL team that uses a given color.

    Args:
        hex_color: Hex color code (e.g., '#e31837')

    Returns:
        Team abbreviation if found, None otherwise
    """
    from .colors import NFL_TEAM_COLORS

    hex_color = hex_color.lower()

    for team, colors in NFL_TEAM_COLORS.items():
        for color_value in colors.values():
            if color_value.lower() == hex_color:
                return team

    return None


def get_season_info(season: int) -> dict[str, Any]:
    """Get information about a specific NFL season.

    Args:
        season: Season year

    Returns:
        Dictionary with season information

    Note:
        This is a basic implementation. Could be enhanced with
        playoff info, schedule details, etc.
    """
    current_year = 2024  # Update as needed

    info = {
        "season": season,
        "is_current": season == current_year,
        "is_future": season > current_year,
        "is_historical": season < current_year,
        "data_available": season >= 1999,  # Based on nfl_data_py availability
        "regular_season_weeks": 18 if season >= 2021 else 17 if season >= 2021 else 16,
        "playoff_format": "expanded" if season >= 2020 else "traditional",
    }

    # Add notable season information
    notable_seasons = {
        2007: "Patriots 16-0 regular season",
        2013: "Peyton Manning 55 TD season",
        2016: "Patriots 28-3 comeback",
        2020: "COVID-19 affected season",
        2021: "17-game regular season begins",
    }

    if season in notable_seasons:
        info["notable"] = notable_seasons[season]

    return info
