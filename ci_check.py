#!/usr/bin/env python3
"""
CI Check Script - Simulates typical GitHub Actions workflow
"""
import subprocess
import sys
import os

def run_command(cmd, description):
    """Run a command and report results."""
    print(f"\n{'='*60}")
    print(f"🔍 {description}")
    print(f"{'='*60}")
    print(f"Running: {cmd}")
    
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    
    if result.returncode == 0:
        print(f"✅ {description} - PASSED")
        if result.stdout.strip():
            print("Output:")
            print(result.stdout)
    else:
        print(f"❌ {description} - FAILED")
        if result.stderr.strip():
            print("Errors:")
            print(result.stderr)
        if result.stdout.strip():
            print("Output:")
            print(result.stdout)
            
    return result.returncode == 0

def main():
    """Run comprehensive CI checks."""
    print("🚀 NFL Plotpy CI Check Suite")
    print("Simulating typical GitHub Actions workflow")
    
    # Ensure we're in a virtual environment
    if not os.environ.get('VIRTUAL_ENV'):
        print("⚠️  Warning: Not in a virtual environment")
    
    checks = [
        ("source .venv/bin/activate && ruff check nflplotpy/", "Ruff Linting"),
        ("source .venv/bin/activate && ruff format --check nflplotpy/", "Ruff Formatting"),
        ("source .venv/bin/activate && python -c 'import nflplotpy; print(f\"Package imports successfully. Version info available.\")'", "Package Import"),
        ("source .venv/bin/activate && python -m pytest tests/ --tb=short -q --disable-warnings", "Test Suite"),
        ("source .venv/bin/activate && python -c 'import nflplotpy as nfl; print(f\"Exported functions: {len(nfl.__all__)}\")'", "Function Exports"),
    ]
    
    results = []
    
    for cmd, description in checks:
        success = run_command(cmd, description)
        results.append((description, success))
    
    print(f"\n{'='*60}")
    print("📊 CI CHECK SUMMARY")
    print(f"{'='*60}")
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for description, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status:<10} {description}")
    
    print(f"\nOverall: {passed}/{total} checks passed")
    
    if passed == total:
        print("🎉 ALL CI CHECKS PASSED - Ready for deployment!")
        return 0
    else:
        print("💥 SOME CI CHECKS FAILED - Fix required before deployment")
        return 1

if __name__ == "__main__":
    sys.exit(main())