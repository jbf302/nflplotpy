"""Enhanced URL management for NFL assets.

Provides comprehensive URL mapping and management for team logos,
player headshots, wordmarks, and other NFL assets.
"""

from __future__ import annotations

import re
import warnings

from .logos import NFL_TEAM_LOGOS

# Team wordmark URLs following nflverse patterns
# These URLs point to high-quality team wordmarks
NFL_TEAM_WORDMARKS: dict[str, str] = {
    "ARI": "https://github.com/nflverse/nflfastR-data/raw/master/wordmarks/ARI.png",
    "ATL": "https://github.com/nflverse/nflfastR-data/raw/master/wordmarks/ATL.png",
    "BAL": "https://github.com/nflverse/nflfastR-data/raw/master/wordmarks/BAL.png",
    "BUF": "https://github.com/nflverse/nflfastR-data/raw/master/wordmarks/BUF.png",
    "CAR": "https://github.com/nflverse/nflfastR-data/raw/master/wordmarks/CAR.png",
    "CHI": "https://github.com/nflverse/nflfastR-data/raw/master/wordmarks/CHI.png",
    "CIN": "https://github.com/nflverse/nflfastR-data/raw/master/wordmarks/CIN.png",
    "CLE": "https://github.com/nflverse/nflfastR-data/raw/master/wordmarks/CLE.png",
    "DAL": "https://github.com/nflverse/nflfastR-data/raw/master/wordmarks/DAL.png",
    "DEN": "https://github.com/nflverse/nflfastR-data/raw/master/wordmarks/DEN.png",
    "DET": "https://github.com/nflverse/nflfastR-data/raw/master/wordmarks/DET.png",
    "GB": "https://github.com/nflverse/nflfastR-data/raw/master/wordmarks/GB.png",
    "HOU": "https://github.com/nflverse/nflfastR-data/raw/master/wordmarks/HOU.png",
    "IND": "https://github.com/nflverse/nflfastR-data/raw/master/wordmarks/IND.png",
    "JAC": "https://github.com/nflverse/nflfastR-data/raw/master/wordmarks/JAC.png",
    "KC": "https://github.com/nflverse/nflfastR-data/raw/master/wordmarks/KC.png",
    "LV": "https://github.com/nflverse/nflfastR-data/raw/master/wordmarks/LV.png",
    "LAC": "https://github.com/nflverse/nflfastR-data/raw/master/wordmarks/LAC.png",
    "LAR": "https://github.com/nflverse/nflfastR-data/raw/master/wordmarks/LAR.png",
    "MIA": "https://github.com/nflverse/nflfastR-data/raw/master/wordmarks/MIA.png",
    "MIN": "https://github.com/nflverse/nflfastR-data/raw/master/wordmarks/MIN.png",
    "NE": "https://github.com/nflverse/nflfastR-data/raw/master/wordmarks/NE.png",
    "NO": "https://github.com/nflverse/nflfastR-data/raw/master/wordmarks/NO.png",
    "NYG": "https://github.com/nflverse/nflfastR-data/raw/master/wordmarks/NYG.png",
    "NYJ": "https://github.com/nflverse/nflfastR-data/raw/master/wordmarks/NYJ.png",
    "PHI": "https://github.com/nflverse/nflfastR-data/raw/master/wordmarks/PHI.png",
    "PIT": "https://github.com/nflverse/nflfastR-data/raw/master/wordmarks/PIT.png",
    "SEA": "https://github.com/nflverse/nflfastR-data/raw/master/wordmarks/SEA.png",
    "SF": "https://github.com/nflverse/nflfastR-data/raw/master/wordmarks/SF.png",
    "TB": "https://github.com/nflverse/nflfastR-data/raw/master/wordmarks/TB.png",
    "TEN": "https://github.com/nflverse/nflfastR-data/raw/master/wordmarks/TEN.png",
    "WAS": "https://github.com/nflverse/nflfastR-data/raw/master/wordmarks/WAS.png",
}


class PlayerIDManager:
    """Manages mapping between different player ID systems."""

    def __init__(self):
        """Initialize player ID manager."""
        self._gsis_to_espn_cache: dict[str, str] = {}
        self._player_name_cache: dict[str, dict[str, str]] = {}

        # Known mappings for testing (these would come from nflreadr in production)
        self._test_mappings = {
            "00-0033873": "3139477",  # Patrick Mahomes
            "00-0034796": "3918298",  # Josh Allen
            "00-0019596": "2330",  # Tom Brady (retired)
            "00-0023459": "8439",  # Aaron Rodgers
            "00-0031280": "3916387",  # Lamar Jackson
            "00-0034857": "4035538",  # Justin Herbert
        }

    def gsis_to_espn_id(self, gsis_id: str) -> str | None:
        """Convert GSIS ID to ESPN player ID.

        Args:
            gsis_id: NFL GSIS ID (format: 00-0012345)

        Returns:
            ESPN player ID if found, None otherwise
        """
        # Check cache first
        if gsis_id in self._gsis_to_espn_cache:
            return self._gsis_to_espn_cache[gsis_id]

        # Check test mappings
        if gsis_id in self._test_mappings:
            espn_id = self._test_mappings[gsis_id]
            self._gsis_to_espn_cache[gsis_id] = espn_id
            return espn_id

        # In production, this would query nflreadr's player ID mapping
        warnings.warn(
            f"GSIS to ESPN ID mapping not available for: {gsis_id}", stacklevel=2
        )
        return None

    def discover_player_by_name(
        self, player_name: str, team: str | None = None
    ) -> dict[str, str | None]:
        """Discover player IDs by name.

        Args:
            player_name: Player's full name
            team: Team abbreviation (helps with disambiguation)

        Returns:
            Dictionary with available player IDs
        """
        # Normalize name for lookup
        normalized_name = player_name.lower().strip()

        # Test data for development
        test_players = {
            "patrick mahomes": {"gsis_id": "00-0033873", "espn_id": "3139477"},
            "josh allen": {"gsis_id": "00-0034796", "espn_id": "3918298"},
            "tom brady": {"gsis_id": "00-0019596", "espn_id": "2330"},
            "aaron rodgers": {"gsis_id": "00-0023459", "espn_id": "8439"},
            "lamar jackson": {"gsis_id": "00-0031280", "espn_id": "3916387"},
            "justin herbert": {"gsis_id": "00-0034857", "espn_id": "4035538"},
        }

        if normalized_name in test_players:
            return test_players[normalized_name]

        return {"gsis_id": None, "espn_id": None}


class PlayerHeadshotURLBuilder:
    """Builds URLs for NFL player headshots from various sources."""

    # ESPN headshot URL patterns
    ESPN_HEADSHOT_BASE = (
        "https://a.espncdn.com/i/headshots/nfl/players/full/{player_id}.png"
    )
    ESPN_HEADSHOT_SMALL = (
        "https://a.espncdn.com/i/headshots/nfl/players/small/{player_id}.png"
    )

    def __init__(self):
        """Initialize headshot URL builder."""
        self.player_id_manager = PlayerIDManager()

    def get_espn_headshot_url(self, player_id: str | int, size: str = "full") -> str:
        """Get ESPN headshot URL for a player.

        Args:
            player_id: ESPN player ID
            size: Size variant ('full', 'small')

        Returns:
            URL to player headshot
        """
        if size == "full":
            return self.ESPN_HEADSHOT_BASE.format(player_id=player_id)
        if size == "small":
            return self.ESPN_HEADSHOT_SMALL.format(player_id=player_id)
        msg = f"Invalid size: {size}. Use 'full' or 'small'"
        raise ValueError(msg)

    def build_headshot_urls(
        self,
        player_id: str | int,
        id_type: str = "auto",
        sources: list[str] | None = None,
    ) -> dict[str, str]:
        """Build headshot URLs from multiple sources.

        Args:
            player_id: Player identifier (ESPN ID, GSIS ID, or name)
            id_type: Type of player_id ('espn', 'gsis', 'name', 'auto')
            sources: List of sources to try ('espn')

        Returns:
            Dictionary mapping source names to URLs
        """
        if sources is None:
            sources = ["espn"]

        urls = {}
        espn_id = None

        # Determine ESPN ID based on input type
        if id_type == "auto":
            # Try to auto-detect ID type
            player_id_str = str(player_id)
            if player_id_str.startswith("00-"):
                # Looks like GSIS ID
                espn_id = self.player_id_manager.gsis_to_espn_id(player_id_str)
            elif player_id_str.isdigit():
                # Looks like ESPN ID
                espn_id = player_id_str
            else:
                # Treat as player name
                player_info = self.player_id_manager.discover_player_by_name(
                    player_id_str
                )
                espn_id = player_info.get("espn_id")
        elif id_type == "espn":
            espn_id = str(player_id)
        elif id_type == "gsis":
            espn_id = self.player_id_manager.gsis_to_espn_id(str(player_id))
        elif id_type == "name":
            player_info = self.player_id_manager.discover_player_by_name(str(player_id))
            espn_id = player_info.get("espn_id")

        # Build URLs if we have an ESPN ID
        if espn_id:
            for source in sources:
                try:
                    if source == "espn":
                        urls["espn_full"] = self.get_espn_headshot_url(espn_id, "full")
                        urls["espn_small"] = self.get_espn_headshot_url(
                            espn_id, "small"
                        )
                except Exception as e:
                    warnings.warn(
                        f"Could not build {source} URL for {player_id}: {e}",
                        stacklevel=2,
                    )
        else:
            warnings.warn(
                f"Could not resolve ESPN ID for player: {player_id}", stacklevel=2
            )

        return urls


class AssetURLManager:
    """Comprehensive manager for all NFL asset URLs."""

    def __init__(self):
        """Initialize URL manager."""
        self.logos = NFL_TEAM_LOGOS.copy()
        self.wordmarks = NFL_TEAM_WORDMARKS.copy()
        self.headshot_builder = PlayerHeadshotURLBuilder()
        self.player_id_manager = self.headshot_builder.player_id_manager

    def get_logo_url(self, team: str) -> str:
        """Get team logo URL.

        Args:
            team: Team abbreviation

        Returns:
            URL to team logo
        """
        team = team.upper()
        if team not in self.logos:
            msg = f"No logo URL found for team: {team}"
            raise ValueError(msg)
        return self.logos[team]

    def get_wordmark_url(self, team: str) -> str:
        """Get team wordmark URL.

        Args:
            team: Team abbreviation

        Returns:
            URL to team wordmark
        """
        team = team.upper()
        if team not in self.wordmarks:
            # Fallback to logo if wordmark not available
            return self.get_logo_url(team)
        return self.wordmarks[team]

    def get_headshot_urls(
        self,
        player_id: str | int,
        id_type: str = "auto",
        sources: list[str] | None = None,
    ) -> dict[str, str]:
        """Get player headshot URLs.

        Args:
            player_id: Player identifier (ESPN ID, GSIS ID, or name)
            id_type: Type of player_id ('espn', 'gsis', 'name', 'auto')
            sources: Sources to try

        Returns:
            Dictionary of source -> URL mappings
        """
        return self.headshot_builder.build_headshot_urls(player_id, id_type, sources)

    def add_custom_logo_url(self, team: str, url: str):
        """Add or override team logo URL.

        Args:
            team: Team abbreviation
            url: URL to logo image
        """
        self.logos[team.upper()] = url

    def add_custom_wordmark_url(self, team: str, url: str):
        """Add or override team wordmark URL.

        Args:
            team: Team abbreviation
            url: URL to wordmark image
        """
        self.wordmarks[team.upper()] = url

    def validate_url(self, url: str) -> bool:
        """Validate that a URL is properly formatted.

        Args:
            url: URL to validate

        Returns:
            True if URL appears valid
        """
        # Basic URL validation
        url_pattern = re.compile(
            r"^https?://"  # http:// or https://
            r"(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|"  # domain...
            r"localhost|"  # localhost...
            r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"  # ...or ip
            r"(?::\d+)?"  # optional port
            r"(?:/?|[/?]\S+)$",
            re.IGNORECASE,
        )

        return url_pattern.match(url) is not None

    def get_all_urls(self) -> dict[str, dict[str, str]]:
        """Get all managed URLs.

        Returns:
            Dictionary with 'logos' and 'wordmarks' sections
        """
        return {"logos": self.logos.copy(), "wordmarks": self.wordmarks.copy()}

    def update_urls_from_dict(self, url_dict: dict[str, dict[str, str]]):
        """Update URLs from dictionary.

        Args:
            url_dict: Dictionary with 'logos' and/or 'wordmarks' keys
        """
        if "logos" in url_dict:
            self.logos.update(url_dict["logos"])

        if "wordmarks" in url_dict:
            self.wordmarks.update(url_dict["wordmarks"])


# Singleton URL manager
_url_manager: AssetURLManager | None = None


def get_url_manager() -> AssetURLManager:
    """Get singleton URL manager instance."""
    global _url_manager
    if _url_manager is None:
        _url_manager = AssetURLManager()
    return _url_manager


def get_team_wordmark_url(team: str) -> str:
    """Get team wordmark URL.

    Convenience function using singleton URL manager.

    Args:
        team: Team abbreviation

    Returns:
        URL to team wordmark
    """
    manager = get_url_manager()
    return manager.get_wordmark_url(team)


def get_player_headshot_urls(
    player_id: str | int, id_type: str = "auto", sources: list[str] | None = None
) -> dict[str, str]:
    """Get player headshot URLs from multiple sources.

    Convenience function using singleton URL manager.

    Args:
        player_id: Player identifier (ESPN ID, GSIS ID, or name)
        id_type: Type of player_id ('espn', 'gsis', 'name', 'auto')
        sources: Sources to try ('espn')

    Returns:
        Dictionary mapping sources to URLs

    Example:
        >>> # Using ESPN ID
        >>> urls = get_player_headshot_urls("3139477", id_type="espn")
        >>> print(urls['espn_full'])

        >>> # Using GSIS ID
        >>> urls = get_player_headshot_urls("00-0033873", id_type="gsis")
        >>> print(urls['espn_full'])

        >>> # Using player name (auto-detection)
        >>> urls = get_player_headshot_urls("Patrick Mahomes")
        >>> print(urls['espn_full'])
    """
    manager = get_url_manager()
    return manager.get_headshot_urls(player_id, id_type, sources)


def discover_player_id(
    player_name: str, team: str | None = None
) -> dict[str, str | None]:
    """Attempt to discover player IDs from name.

    Args:
        player_name: Player's full name (e.g., "Patrick Mahomes")
        team: Team abbreviation (helps with disambiguation)

    Returns:
        Dictionary with available player IDs (gsis_id, espn_id)

    Example:
        >>> ids = discover_player_id("Patrick Mahomes")
        >>> print(ids['espn_id'])  # "3139477"
        >>> print(ids['gsis_id'])  # "00-0033873"
    """
    manager = get_url_manager()
    return manager.player_id_manager.discover_player_by_name(player_name, team)


def validate_all_urls() -> dict[str, list[str]]:
    """Validate all managed URLs for accessibility.

    Returns:
        Dictionary with 'valid' and 'invalid' URL lists

    Note:
        This function makes HTTP requests to check URL accessibility.
        Use sparingly to avoid overwhelming servers.
    """
    import time
    from concurrent.futures import ThreadPoolExecutor, as_completed

    import requests

    manager = get_url_manager()
    all_urls = {**manager.logos, **manager.wordmarks}

    valid_urls = []
    invalid_urls = []

    def check_url(url):
        try:
            response = requests.head(url, timeout=10)
            return url, response.status_code < 400
        except Exception:
            return url, False

    # Check URLs with rate limiting
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = {executor.submit(check_url, url): url for url in all_urls.values()}

        for future in as_completed(futures):
            url, is_valid = future.result()

            if is_valid:
                valid_urls.append(url)
            else:
                invalid_urls.append(url)

            # Rate limiting
            time.sleep(0.1)

    return {"valid": valid_urls, "invalid": invalid_urls}
