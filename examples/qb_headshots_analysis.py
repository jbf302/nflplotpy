#!/usr/bin/env python3
"""
2024 NFL QB Analysis with Player Headshots

This script demonstrates nflplotpy's headshot functionality by creating
a scatter plot analyzing quarterback performance metrics:
- X-axis: Total offensive EPA per game
- Y-axis: % of EPA that is YAC EPA

Player headshots are displayed for each quarterback.

Requirements:
- nflplotpy[all] or nflplotpy with nfl_data_py installed
- matplotlib
"""

import warnings

warnings.filterwarnings("ignore")

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

try:
    import nfl_data_py as nfl

    NFL_DATA_AVAILABLE = True  # Try real data first
except ImportError:
    NFL_DATA_AVAILABLE = False
    print("nfl_data_py not available. Using sample data instead.")

import nflplotpy as nflplot
from nflplotpy.matplotlib.elements import add_player_headshot
from nflplotpy.matplotlib.artists import add_median_lines


def load_qb_data():
    """Load and process 2024 QB data."""

    if not NFL_DATA_AVAILABLE:
        # Sample data for demonstration
        print("Using sample QB data for demonstration...")
        sample_data = pd.DataFrame(
            {
                "player_display_name": [
                    "Patrick Mahomes",
                    "Josh Allen",
                    "Lamar Jackson",
                    "Dak Prescott",
                    "Tua Tagovailoa",
                    "Aaron Rodgers",
                    "Russell Wilson",
                    "Kyler Murray",
                    "Jalen Hurts",
                    "Joe Burrow",
                    "Justin Herbert",
                    "Geno Smith",
                ],
                "recent_team": [
                    "KC",
                    "BUF",
                    "BAL",
                    "DAL",
                    "MIA",
                    "NYJ",
                    "PIT",
                    "ARI",
                    "PHI",
                    "CIN",
                    "LAC",
                    "SEA",
                ],
                "games": [17, 17, 12, 16, 17, 4, 17, 11, 15, 10, 17, 16],
                "total_offensive_epa": [
                    145.2,
                    138.7,
                    89.3,
                    112.8,
                    98.4,
                    -8.2,
                    67.3,
                    45.1,
                    78.9,
                    34.2,
                    89.7,
                    78.3,
                ],
                "yac_yards": [
                    1247,
                    1156,
                    623,
                    981,
                    1034,
                    198,
                    734,
                    456,
                    891,
                    387,
                    956,
                    743,
                ],  # YAC yards
                "total_passing_yards": [
                    4321,
                    4169,
                    2635,
                    3602,
                    4067,
                    849,
                    2897,
                    2106,
                    3701,
                    1573,
                    3631,
                    2976,
                ],  # Total passing yards
            }
        )

        # Calculate per-game averages and YAC yards percentage
        sample_data["epa_per_game"] = (
            sample_data["total_offensive_epa"] / sample_data["games"]
        )

        # Handle YAC yards percentage calculation
        def calculate_yac_percentage(row):
            if row["total_passing_yards"] <= 0:  # Avoid division by zero/negative
                return 0.0
            else:
                # % of passing yards that come from YAC (should be 0-100%)
                return round((row["yac_yards"] / row["total_passing_yards"] * 100), 1)

        sample_data["yac_yards_percentage"] = sample_data.apply(
            calculate_yac_percentage, axis=1
        )

        # Add known ESPN IDs for accurate headshot matching
        espn_id_mapping = {
            "Patrick Mahomes": "3139477",
            "Josh Allen": "3918298",
            "Lamar Jackson": "3916387",
            "Dak Prescott": "2577417",
            "Tua Tagovailoa": "4241479",
            "Aaron Rodgers": "8439",
            "Russell Wilson": "14881",
            "Kyler Murray": "4038941",
            "Jalen Hurts": "4241464",
            "Joe Burrow": "4035004",
            "Justin Herbert": "4035538",
            "Geno Smith": "14880",
        }

        sample_data["espn_id"] = sample_data["player_display_name"].map(espn_id_mapping)
        sample_data["validated_name"] = sample_data["player_display_name"]

        return sample_data

    print("Loading real 2024 NFL data...")

    try:
        # Load play-by-play data for 2024
        pbp_data = nfl.import_pbp_data([2024])

        # Filter for QB plays and calculate EPA metrics
        qb_plays = pbp_data[
            (pbp_data["passer_player_name"].notna())
            & (pbp_data["epa"].notna())
            & (pbp_data["season_type"] == "REG")
        ].copy()

        # Calculate QB stats (keep passer_player_id for accurate lookups)
        qb_stats = (
            qb_plays.groupby(["passer_player_id", "passer_player_name", "posteam"])
            .agg(
                {
                    "epa": ["sum", "count"],
                    "yards_after_catch": "sum",  # Total YAC yards
                    "passing_yards": "sum",  # Total passing yards
                    "week": "nunique",
                }
            )
            .round(2)
        )

        qb_stats.columns = [
            "total_offensive_epa",
            "attempts",
            "yac_yards",
            "total_passing_yards",
            "games",
        ]
        qb_stats = qb_stats.reset_index()

        # Filter for QBs with meaningful sample size
        qb_stats = qb_stats[
            (qb_stats["attempts"] >= 150) & (qb_stats["games"] >= 8)
        ].copy()

        # Calculate per-game averages and YAC EPA percentage
        qb_stats["epa_per_game"] = qb_stats["total_offensive_epa"] / qb_stats["games"]

        # Handle YAC yards percentage calculation
        def calculate_yac_percentage(row):
            if row["total_passing_yards"] <= 0:  # Avoid division by zero/negative
                return 0.0
            else:
                # % of passing yards that come from YAC (should be 0-100%)
                return round((row["yac_yards"] / row["total_passing_yards"] * 100), 1)

        qb_stats["yac_yards_percentage"] = qb_stats.apply(
            calculate_yac_percentage, axis=1
        )

        # Keep both player ID and name for accurate headshot lookup
        qb_stats = qb_stats.rename(
            columns={
                "passer_player_name": "player_display_name",
                "posteam": "recent_team",
            }
        )

        # Add ESPN IDs for accurate headshot matching
        print("Resolving player IDs for accurate headshots...")
        from nflplotpy.core.urls import get_player_info_by_id

        qb_stats["espn_id"] = None
        qb_stats["validated_name"] = None

        for idx, row in qb_stats.iterrows():
            if pd.notna(row["passer_player_id"]):
                # Use the GSIS ID from play-by-play data for accurate lookup
                player_info = get_player_info_by_id(
                    row["passer_player_id"], id_type="gsis"
                )
                if player_info["espn_id"]:
                    qb_stats.at[idx, "espn_id"] = player_info["espn_id"]
                    qb_stats.at[idx, "validated_name"] = (
                        player_info["name"] or row["player_display_name"]
                    )
                else:
                    qb_stats.at[idx, "validated_name"] = row["player_display_name"]

        # Sort by total EPA and take top performers
        qb_stats = qb_stats.nlargest(16, "total_offensive_epa")

        print(f"Loaded data for {len(qb_stats)} qualifying quarterbacks")
        return qb_stats

    except Exception as e:
        print(f"Error loading NFL data: {e}")
        print("Falling back to sample data...")
        return load_qb_data()  # Recursive call to get sample data


def create_qb_headshot_plot(qb_data):
    """Create the main QB analysis plot with headshots."""

    # Create figure and axis
    fig, ax = plt.subplots(figsize=(14, 10))

    # Calculate per-game metrics if not already present
    if "epa_per_game" not in qb_data.columns:
        qb_data["epa_per_game"] = qb_data["total_offensive_epa"] / qb_data["games"]

        # Handle YAC yards percentage calculation
        def calculate_yac_percentage(row):
            if row["total_passing_yards"] <= 0:  # Avoid division by zero/negative
                return 0.0
            else:
                # % of passing yards that come from YAC (should be 0-100%)
                return round((row["yac_yards"] / row["total_passing_yards"] * 100), 1)

        qb_data["yac_yards_percentage"] = qb_data.apply(
            calculate_yac_percentage, axis=1
        )

    # Create scatter plot points (invisible - headshots will replace them)
    x_vals = qb_data["epa_per_game"].values
    y_vals = qb_data["yac_yards_percentage"].values

    # Add invisible scatter points for reference
    ax.scatter(x_vals, y_vals, alpha=0.0, s=100)

    # Add player headshots
    print("Adding player headshots to plot...")
    headshot_size = 0.06  # Size of headshots (made smaller)

    for idx, row in qb_data.iterrows():
        x = row["epa_per_game"]
        y = row["yac_yards_percentage"]
        player_name = row.get("validated_name", row["player_display_name"])

        try:
            # Use ESPN ID if available for accurate headshot matching
            if pd.notna(row.get("espn_id")):
                add_player_headshot(
                    ax,
                    row["espn_id"],
                    x,
                    y,
                    width=headshot_size,
                    id_type="espn",  # Use ESPN ID for accurate matching
                    circular=False,  # Remove black circular background
                    transform=ax.transData,
                    alpha=0.9,  # Add transparency for overlapping
                )
            else:
                # Fall back to name-based lookup
                add_player_headshot(
                    ax,
                    player_name,
                    x,
                    y,
                    width=headshot_size,
                    id_type="name",
                    circular=False,  # Remove black circular background
                    transform=ax.transData,
                    alpha=0.9,  # Add transparency for overlapping
                )

            # Add subtle text label below headshot
            ax.annotate(
                player_name.split()[-1],  # Last name only
                xy=(x, y),
                xytext=(0, -35),
                textcoords="offset points",
                ha="center",
                va="top",
                fontsize=8,
                color="#333333",
                alpha=0.8,
                weight="bold",
            )

        except Exception as e:
            print(f"Warning: Could not add headshot for {player_name}: {e}")
            # Fallback to regular scatter point
            team_color = nflplot.get_team_colors(row["recent_team"], "primary")
            ax.scatter(
                x, y, c=team_color, s=200, alpha=0.8, edgecolors="white", linewidth=2
            )
            ax.annotate(
                player_name.split()[-1],
                xy=(x, y),
                xytext=(5, 5),
                textcoords="offset points",
                fontsize=9,
            )

    # Add reference lines at medians
    add_median_lines(
        ax, x_vals, axis="x", color="red", linestyle="--", alpha=0.5, linewidth=1
    )
    add_median_lines(
        ax, y_vals, axis="y", color="red", linestyle="--", alpha=0.5, linewidth=1
    )

    # Styling
    ax.set_xlabel("Total Offensive EPA per Game", fontsize=14, fontweight="bold")
    ax.set_ylabel("% of Passing Yards from YAC", fontsize=14, fontweight="bold")
    ax.set_title(
        "2024 NFL Quarterback Performance Analysis\n"
        "Total EPA per Game vs. % of Passing Yards from YAC",
        fontsize=16,
        fontweight="bold",
        pad=20,
    )

    # Apply NFL theme
    nflplot.apply_nfl_theme(ax, style="default")

    # Add subtle grid
    ax.grid(True, alpha=0.3, linestyle="-", linewidth=0.5)
    ax.set_axisbelow(True)

    # Set Y-axis limits to focus on actual data range
    y_min = min(y_vals) - 2
    y_max = max(y_vals) + 2
    ax.set_ylim(y_min, y_max)

    # Add explanatory text
    textstr = (
        "Top Right: High EPA QBs with receiver-dependent offense\n"
        "Bottom Right: High EPA QBs with precise passing (less YAC)\n"
        "Red lines indicate median values"
    )

    props = dict(boxstyle="round", facecolor="wheat", alpha=0.8)
    ax.text(
        0.02,
        0.98,
        textstr,
        transform=ax.transAxes,
        fontsize=10,
        verticalalignment="top",
        bbox=props,
    )

    # Adjust layout to prevent headshot clipping
    plt.tight_layout()
    plt.subplots_adjust(bottom=0.15, top=0.9)

    return fig, ax


def add_quadrant_analysis(ax, x_vals, y_vals):
    """Add quadrant analysis labels."""

    x_median = np.median(x_vals)
    y_median = np.median(y_vals)

    # Quadrant labels
    quadrants = [
        ("High EPA + High YAC", 0.75, 0.9, "green"),
        ("High EPA + Precise Passing", 0.75, 0.1, "blue"),
        ("Lower EPA + Precise Passing", 0.25, 0.1, "orange"),
        ("Lower EPA + High YAC", 0.25, 0.9, "purple"),
    ]

    for label, x_pos, y_pos, color in quadrants:
        ax.text(
            x_pos,
            y_pos,
            label,
            transform=ax.transAxes,
            fontsize=11,
            fontweight="bold",
            color=color,
            ha="center",
            va="center",
            bbox=dict(
                boxstyle="round,pad=0.3", facecolor="white", edgecolor=color, alpha=0.8
            ),
        )


def main():
    """Main execution function."""

    print("🏈 2024 NFL QB Analysis with Player Headshots")
    print("=" * 50)

    # Load QB data
    qb_data = load_qb_data()
    print(f"\nLoaded data for {len(qb_data)} quarterbacks")

    if NFL_DATA_AVAILABLE:
        print("\nTop 5 QBs by Total EPA:")
        top_qbs = qb_data.nlargest(5, "total_offensive_epa")[
            ["player_display_name", "recent_team", "total_offensive_epa", "games"]
        ]
        print(top_qbs.to_string(index=False))

    # Create the plot
    print(f"\nCreating visualization...")
    fig, ax = create_qb_headshot_plot(qb_data)

    # Add quadrant analysis
    if "epa_per_game" in qb_data.columns:
        add_quadrant_analysis(
            ax, qb_data["epa_per_game"], qb_data["yac_yards_percentage"]
        )

    # Save the plot
    output_file = "examples/2024_qb_headshots_analysis.png"
    plt.savefig(
        output_file, dpi=300, bbox_inches="tight", facecolor="white", edgecolor="none"
    )
    print(f"\n✅ Plot saved to: {output_file}")

    # Show the plot
    plt.show()

    print("\n📊 Analysis Notes:")
    print("• Player headshots show individual QB performance")
    print("• X-axis: Team's offensive EPA per game when QB starts (productivity)")
    print("• Y-axis: % of passing yards gained after the catch (0-100%)")
    print("• Red dashed lines show median values for reference")
    print("• Higher YAC% = More yards gained by receivers after catching the ball")
    print("• Lower YAC% = More yards gained through precise passing to open receivers")
    print("• Both styles can be effective - shows different offensive approaches")


if __name__ == "__main__":
    main()
