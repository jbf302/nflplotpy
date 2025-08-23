#!/usr/bin/env python3
"""
Player ID Validation Script

This script validates the accuracy of player ID lookups and headshot matching
to ensure we're displaying the correct player photos.

Requirements:
- nflplotpy with nfl_data_py integration
"""

import warnings
warnings.filterwarnings('ignore')

import pandas as pd
import requests
from io import BytesIO
from PIL import Image
import matplotlib.pyplot as plt

try:
    import nfl_data_py as nfl
    NFL_DATA_AVAILABLE = True
except ImportError:
    NFL_DATA_AVAILABLE = False
    print("nfl_data_py not available. Please install for full validation.")

from nflplotpy.core.urls import get_player_info_by_id, get_player_headshot_urls, discover_player_id


def validate_known_players():
    """Test player ID lookups for well-known players."""
    
    print("🔍 VALIDATING KNOWN PLAYERS")
    print("=" * 40)
    
    # Known player test cases (name, expected GSIS ID, expected ESPN ID)
    known_players = [
        ("Patrick Mahomes", "00-0033873", "3139477"),
        ("Josh Allen", "00-0034857", "3918298"),  # Note: Was showing wrong ID before
        ("Tom Brady", "00-0019596", "2330"),
        ("Aaron Rodgers", "00-0023459", "8439"),
        ("Lamar Jackson", "00-0031280", "3916387"),
    ]
    
    validation_results = []
    
    for name, expected_gsis, expected_espn in known_players:
        print(f"\n🏈 Testing: {name}")
        
        # Test name-based lookup
        name_result = discover_player_id(name)
        print(f"   Name lookup - GSIS: {name_result.get('gsis_id')}, ESPN: {name_result.get('espn_id')}")
        
        # Test GSIS ID lookup
        gsis_result = get_player_info_by_id(expected_gsis, id_type='gsis')
        print(f"   GSIS lookup - Name: {gsis_result.get('name')}, ESPN: {gsis_result.get('espn_id')}")
        
        # Test ESPN ID lookup  
        espn_result = get_player_info_by_id(expected_espn, id_type='espn')
        print(f"   ESPN lookup - Name: {espn_result.get('name')}, GSIS: {espn_result.get('gsis_id')}")
        
        # Validate headshot URL accessibility
        headshot_urls = get_player_headshot_urls(expected_espn, id_type='espn')
        headshot_accessible = False
        if headshot_urls.get('espn_full'):
            try:
                response = requests.head(headshot_urls['espn_full'], timeout=5)
                headshot_accessible = response.status_code == 200
                print(f"   Headshot URL: {'✅ Accessible' if headshot_accessible else '❌ Not accessible'}")
            except Exception:
                print(f"   Headshot URL: ❌ Error checking accessibility")
        
        # Record validation result
        validation_results.append({
            'name': name,
            'expected_gsis': expected_gsis,
            'expected_espn': expected_espn,
            'name_gsis_match': name_result.get('gsis_id') == expected_gsis,
            'name_espn_match': name_result.get('espn_id') == expected_espn,
            'gsis_lookup_success': gsis_result.get('espn_id') == expected_espn,
            'espn_lookup_success': espn_result.get('gsis_id') == expected_gsis,
            'headshot_accessible': headshot_accessible,
        })
    
    return pd.DataFrame(validation_results)


def validate_2024_qb_ids():
    """Validate player IDs from actual 2024 play-by-play data."""
    
    print("\n🏈 VALIDATING 2024 QB DATA")
    print("=" * 40)
    
    if not NFL_DATA_AVAILABLE:
        print("⚠️  nfl_data_py not available - skipping real data validation")
        return pd.DataFrame()
    
    try:
        # Load 2024 play-by-play data
        print("Loading 2024 play-by-play data...")
        pbp_data = nfl.import_pbp_data([2024])
        
        # Get top QBs by attempts
        qb_data = pbp_data[
            (pbp_data['passer_player_name'].notna()) &
            (pbp_data['passer_player_id'].notna()) &
            (pbp_data['season_type'] == 'REG')
        ].copy()
        
        # Top QBs by pass attempts
        top_qbs = qb_data.groupby(['passer_player_id', 'passer_player_name']).size().nlargest(10)
        
        validation_results = []
        
        print(f"\nValidating top 10 QBs by attempts...")
        
        for (player_id, player_name), attempts in top_qbs.items():
            print(f"\n📊 {player_name} (GSIS: {player_id}, Attempts: {attempts})")
            
            # Lookup player info using GSIS ID
            player_info = get_player_info_by_id(player_id, id_type='gsis')
            
            if player_info['espn_id']:
                print(f"   ✅ Found ESPN ID: {player_info['espn_id']}")
                print(f"   ✅ Validated name: {player_info['name']}")
                
                # Test headshot URL
                headshot_urls = get_player_headshot_urls(player_info['espn_id'], id_type='espn')
                headshot_accessible = False
                
                if headshot_urls.get('espn_full'):
                    try:
                        response = requests.head(headshot_urls['espn_full'], timeout=5)
                        headshot_accessible = response.status_code == 200
                        print(f"   {'✅' if headshot_accessible else '❌'} Headshot: {headshot_urls['espn_full']}")
                    except Exception as e:
                        print(f"   ❌ Headshot error: {e}")
                
                validation_results.append({
                    'pbp_name': player_name,
                    'gsis_id': player_id,
                    'espn_id': player_info['espn_id'],
                    'validated_name': player_info['name'],
                    'attempts': attempts,
                    'name_match': player_info['name'] and player_name.lower() in player_info['name'].lower(),
                    'headshot_accessible': headshot_accessible,
                    'headshot_url': headshot_urls.get('espn_full', '')
                })
            else:
                print(f"   ❌ No ESPN ID found")
                validation_results.append({
                    'pbp_name': player_name,
                    'gsis_id': player_id,
                    'espn_id': None,
                    'validated_name': None,
                    'attempts': attempts,
                    'name_match': False,
                    'headshot_accessible': False,
                    'headshot_url': ''
                })
        
        return pd.DataFrame(validation_results)
        
    except Exception as e:
        print(f"❌ Error validating 2024 QB data: {e}")
        return pd.DataFrame()


def create_validation_report(known_results, qb_results):
    """Create a comprehensive validation report."""
    
    print("\n📊 VALIDATION REPORT")
    print("=" * 50)
    
    if not known_results.empty:
        print("\n🔍 Known Players Validation:")
        print(f"   ✅ Name→GSIS matches: {known_results['name_gsis_match'].sum()}/{len(known_results)}")
        print(f"   ✅ Name→ESPN matches: {known_results['name_espn_match'].sum()}/{len(known_results)}")
        print(f"   ✅ GSIS lookup success: {known_results['gsis_lookup_success'].sum()}/{len(known_results)}")
        print(f"   ✅ ESPN lookup success: {known_results['espn_lookup_success'].sum()}/{len(known_results)}")
        print(f"   ✅ Headshots accessible: {known_results['headshot_accessible'].sum()}/{len(known_results)}")
        
        # Show any failures
        failures = known_results[~(known_results['name_gsis_match'] & known_results['name_espn_match'])]
        if not failures.empty:
            print("\n❌ Failed validations:")
            for _, row in failures.iterrows():
                print(f"   - {row['name']}: GSIS={row['name_gsis_match']}, ESPN={row['name_espn_match']}")
    
    if not qb_results.empty:
        print(f"\n🏈 2024 QB Data Validation:")
        print(f"   ✅ Players with ESPN IDs: {qb_results['espn_id'].notna().sum()}/{len(qb_results)}")
        print(f"   ✅ Name matches: {qb_results['name_match'].sum()}/{len(qb_results)}")
        print(f"   ✅ Accessible headshots: {qb_results['headshot_accessible'].sum()}/{len(qb_results)}")
        
        # Show players without ESPN IDs
        missing_espn = qb_results[qb_results['espn_id'].isna()]
        if not missing_espn.empty:
            print("\n⚠️  Players missing ESPN IDs:")
            for _, row in missing_espn.iterrows():
                print(f"   - {row['pbp_name']} (GSIS: {row['gsis_id']})")
        
        # Show inaccessible headshots
        bad_headshots = qb_results[~qb_results['headshot_accessible'] & qb_results['espn_id'].notna()]
        if not bad_headshots.empty:
            print("\n⚠️  Players with inaccessible headshots:")
            for _, row in bad_headshots.iterrows():
                print(f"   - {row['validated_name']} (ESPN: {row['espn_id']})")


def test_headshot_visual_validation():
    """Create a visual grid of headshots for manual validation."""
    
    print("\n🖼️  CREATING VISUAL VALIDATION GRID")
    print("=" * 40)
    
    # Test a few known players
    test_players = [
        ("Patrick Mahomes", "3139477"),
        ("Josh Allen", "3918298"), 
        ("Tom Brady", "2330"),
        ("Aaron Rodgers", "8439")
    ]
    
    fig, axes = plt.subplots(2, 2, figsize=(10, 10))
    axes = axes.flatten()
    
    for i, (name, espn_id) in enumerate(test_players):
        ax = axes[i]
        
        try:
            # Get headshot URL
            urls = get_player_headshot_urls(espn_id, id_type='espn')
            if urls.get('espn_full'):
                # Download and display image
                response = requests.get(urls['espn_full'], timeout=10)
                response.raise_for_status()
                
                img = Image.open(BytesIO(response.content))
                ax.imshow(img)
                ax.set_title(f"{name}\nESPN ID: {espn_id}", fontsize=12)
                ax.axis('off')
            else:
                ax.text(0.5, 0.5, f"No headshot\navailable\nfor {name}", 
                       ha='center', va='center', transform=ax.transAxes)
                ax.set_title(f"{name}\nESPN ID: {espn_id}", fontsize=12)
                ax.axis('off')
                
        except Exception as e:
            ax.text(0.5, 0.5, f"Error loading\n{name}\n{str(e)[:50]}...", 
                   ha='center', va='center', transform=ax.transAxes)
            ax.set_title(f"{name} - ERROR", fontsize=12)
            ax.axis('off')
    
    plt.tight_layout()
    plt.savefig('examples/headshot_validation_grid.png', dpi=150, bbox_inches='tight')
    print("✅ Saved visual validation grid to: examples/headshot_validation_grid.png")
    plt.close()


def main():
    """Main validation execution."""
    
    print("🔧 PLAYER ID & HEADSHOT VALIDATION")
    print("=" * 50)
    print("This script validates player ID lookups and headshot accuracy")
    print("to ensure we're matching the correct players to their photos.\n")
    
    # Run validations
    known_results = validate_known_players()
    qb_results = validate_2024_qb_ids()
    
    # Create comprehensive report
    create_validation_report(known_results, qb_results)
    
    # Create visual validation
    test_headshot_visual_validation()
    
    print("\n🎉 VALIDATION COMPLETE")
    print("Review the results above and check the visual validation grid.")
    print("Any failures indicate areas that need improvement in ID matching.")


if __name__ == "__main__":
    main()