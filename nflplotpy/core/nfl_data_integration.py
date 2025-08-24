"""Integration with nfl_data_py for comprehensive player ID mapping.

This module provides enhanced player ID management using the nfl_data_py
package's comprehensive player database.
"""

from __future__ import annotations

import warnings


class NFLDataPlayerManager:
    """Enhanced player ID manager using nfl_data_py."""

    def __init__(self):
        """Initialize the player manager."""
        self._id_data = None
        self._cache = {}

    def _load_data(self):
        """Load player ID data from nfl_data_py."""
        if self._id_data is not None:
            return True

        try:
            import nfl_data_py as nfl

            self._id_data = nfl.import_ids()

            # Validate required columns
            required_cols = ["gsis_id", "espn_id", "name"]
            missing_cols = [
                col for col in required_cols if col not in self._id_data.columns
            ]
            if missing_cols:
                warnings.warn(
                    f"Missing columns in nfl_data_py: {missing_cols}", stacklevel=2
                )
                return False

            return True

        except ImportError:
            warnings.warn(
                "nfl_data_py not available. Install with: pip install nfl_data_py",
                stacklevel=2,
            )
            return False
        except Exception as e:
            warnings.warn(f"Failed to load nfl_data_py: {e}", stacklevel=2)
            return False

    def gsis_to_espn(self, gsis_id: str) -> str | None:
        """Convert GSIS ID to ESPN ID.

        Args:
            gsis_id: NFL GSIS ID (format: 00-0012345)

        Returns:
            ESPN ID if found, None otherwise
        """
        if not self._load_data():
            return None

        cache_key = f"gsis:{gsis_id}"
        if cache_key in self._cache:
            return self._cache[cache_key]

        try:
            import pandas as pd

            match = self._id_data[self._id_data["gsis_id"] == gsis_id]
            if not match.empty and pd.notna(match.iloc[0]["espn_id"]):
                espn_id = str(int(match.iloc[0]["espn_id"]))
                self._cache[cache_key] = espn_id
                return espn_id

        except Exception as e:
            warnings.warn(
                f"Error converting GSIS to ESPN for {gsis_id}: {e}", stacklevel=2
            )

        self._cache[cache_key] = None
        return None

    def name_to_ids(
        self, player_name: str, team: str | None = None
    ) -> dict[str, str | None]:
        """Find player IDs by name using fuzzy matching.

        Args:
            player_name: Player's full name
            team: Team abbreviation (helps with disambiguation)

        Returns:
            Dictionary with 'gsis_id', 'espn_id', and 'name' keys
        """
        if not self._load_data():
            return {"gsis_id": None, "espn_id": None, "name": None}

        normalized_name = player_name.lower().strip()
        cache_key = f"name:{normalized_name}:{team or 'any'}"

        if cache_key in self._cache:
            return self._cache[cache_key]

        try:
            import pandas as pd

            # Try exact name match
            matches = self._id_data[
                self._id_data["name"].str.lower() == normalized_name
            ]

            # Filter by team if provided and available
            if team and "team" in self._id_data.columns:
                team_matches = matches[matches["team"] == team.upper()]
                if not team_matches.empty:
                    matches = team_matches

            # Try fuzzy matching if no exact match
            if matches.empty:
                # Simple fuzzy matching - contains the name
                fuzzy_matches = self._id_data[
                    self._id_data["name"]
                    .str.lower()
                    .str.contains(normalized_name, na=False)
                ]

                if team and "team" in self._id_data.columns:
                    team_fuzzy = fuzzy_matches[fuzzy_matches["team"] == team.upper()]
                    if not team_fuzzy.empty:
                        fuzzy_matches = team_fuzzy

                if not fuzzy_matches.empty:
                    matches = fuzzy_matches

            if not matches.empty:
                player_row = matches.iloc[0]  # Take first match
                result = {
                    "gsis_id": str(player_row["gsis_id"])
                    if pd.notna(player_row["gsis_id"])
                    else None,
                    "espn_id": str(int(player_row["espn_id"]))
                    if pd.notna(player_row["espn_id"])
                    else None,
                    "name": str(player_row["name"])
                    if pd.notna(player_row["name"])
                    else None,
                }
                self._cache[cache_key] = result
                return result

        except Exception as e:
            warnings.warn(
                f"Error searching for player {player_name}: {e}", stacklevel=2
            )

        result = {"gsis_id": None, "espn_id": None, "name": None}
        self._cache[cache_key] = result
        return result

    def get_player_info_by_id(
        self, player_id: str, id_type: str = "gsis"
    ) -> dict[str, str | None]:
        """Get comprehensive player info by ID.

        Args:
            player_id: Player identifier
            id_type: Type of ID ('gsis', 'espn', 'nfl')

        Returns:
            Dictionary with all available player information
        """
        if not self._load_data():
            return {"gsis_id": None, "espn_id": None, "name": None}

        cache_key = f"id:{id_type}:{player_id}"
        if cache_key in self._cache:
            return self._cache[cache_key]

        try:
            import pandas as pd

            # Map ID type to column name
            column_map = {"gsis": "gsis_id", "espn": "espn_id", "nfl": "nfl_id"}

            if id_type not in column_map:
                self._raise_unsupported_id_type(id_type)

            column_name = column_map[id_type]

            # Handle different ID formats
            search_id = player_id
            if id_type == "espn":
                # Ensure ESPN ID is numeric
                search_id = float(player_id)

            # Find player by ID
            matches = self._id_data[self._id_data[column_name] == search_id]

            if not matches.empty:
                player_row = matches.iloc[0]
                result = {
                    "gsis_id": str(player_row["gsis_id"])
                    if pd.notna(player_row["gsis_id"])
                    else None,
                    "espn_id": str(int(player_row["espn_id"]))
                    if pd.notna(player_row["espn_id"])
                    else None,
                    "name": str(player_row["name"])
                    if pd.notna(player_row["name"])
                    else None,
                    "team": str(player_row["team"])
                    if pd.notna(player_row.get("team"))
                    else None,
                    "position": str(player_row["position"])
                    if pd.notna(player_row.get("position"))
                    else None,
                }
                self._cache[cache_key] = result
                return result

        except Exception as e:
            warnings.warn(
                f"Error looking up player by {id_type} ID {player_id}: {e}",
                stacklevel=2,
            )

        result = {"gsis_id": None, "espn_id": None, "name": None}
        self._cache[cache_key] = result
        return result

    def _raise_unsupported_id_type(self, id_type: str) -> None:
        """Raise ValueError for unsupported ID type."""
        msg = f"Unsupported ID type: {id_type}"
        raise ValueError(msg)

    def get_all_players(self, active_only: bool = True) -> object | None:
        """Get all players data.

        Args:
            active_only: If True, filter to active players only

        Returns:
            Pandas DataFrame with all player data, or None if unavailable
        """
        if not self._load_data():
            return None

        try:
            data = self._id_data.copy()

            # Filter to active players if requested
            if active_only and "status" in data.columns:
                data = data[data["status"] == "ACT"]

            return data
        except Exception as e:
            warnings.warn(f"Error getting player data: {e}", stacklevel=2)
            return None


# Singleton instance
_nfl_data_manager: NFLDataPlayerManager | None = None


def get_nfl_data_manager() -> NFLDataPlayerManager:
    """Get singleton NFL data manager."""
    global _nfl_data_manager
    if _nfl_data_manager is None:
        _nfl_data_manager = NFLDataPlayerManager()
    return _nfl_data_manager


def is_nfl_data_py_available() -> bool:
    """Check if nfl_data_py is available and working."""
    try:
        import nfl_data_py as nfl

        # Try a simple operation to verify it works
        _ = nfl.import_ids()
        return True
    except ImportError:
        return False
    except Exception:
        return False
