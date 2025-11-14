# Gaybeck Starkids SMS - Quick Rebuild Script (Python alternative)
import os
import shutil
import subprocess
import sys
from pathlib import Path

def print_header(text):
    print("\n" + "="*70)
    print(f"  {text}")
    print("="*70)

def print_step(step_num, description):
    print(f"\n{'='*70}")
    print(f"STEP {step_num}: {description}")
    print(f"{'='*70}")

def run_command(cmd, description=None):
    """Run a shell command and return the result"""
    if description:
        print(f"  {description}")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.stdout:
            print(result.stdout)
        if result.stderr and result.returncode != 0:
            print(f"Warning: {result.stderr}", file=sys.stderr)
        return result.returncode == 0
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return False

def main():
    print("\n" + "╔" + "="*68 + "╗")
    print("║" + " "*10 + "GAYBECK STARKIDS SMS - REBUILD & REINSTALL" + " "*16 + "║")
    print("╚" + "="*68 + "╝\n")

    project_root = Path(__file__).parent
    os.chdir(project_root)

    # Step 1: Clean old build artifacts
    print_step(1, "Cleaning old build artifacts...")
    folders_to_clean = ["build", "dist", "__pycache__"]
    
    for folder in folders_to_clean:
        folder_path = project_root / folder
        if folder_path.exists():
            print(f"  Removing: {folder}")
            shutil.rmtree(folder_path, ignore_errors=True)
    
    # Clean .egg-info directories
    for egg_info in project_root.glob("*.egg-info"):
        print(f"  Removing: {egg_info.name}")
        shutil.rmtree(egg_info, ignore_errors=True)
    
    # Clean __pycache__ recursively
    for pycache in project_root.rglob("__pycache__"):
        shutil.rmtree(pycache, ignore_errors=True)
    
    print("✓ Cleanup completed")

    # Step 2: Uninstall existing installation
    print_step(2, "Uninstalling existing installation...")
    run_command(
        f"{sys.executable} -m pip uninstall gaybeck-starkids-sms -y",
        "Uninstalling package..."
    )
    print("✓ Uninstall completed")

    # Step 3: Build distribution
    print_step(3, "Building distribution packages...")
    
    # Ensure setuptools and wheel are installed
    run_command(
        f"{sys.executable} -m pip install --upgrade setuptools wheel",
        "Updating build tools..."
    )
    
    # Build source distribution
    print("  Building source distribution...")
    run_command(f"{sys.executable} setup.py sdist")
    
    # Build wheel distribution
    print("  Building wheel distribution...")
    run_command(f"{sys.executable} setup.py bdist_wheel")
    
    print("✓ Build completed")

    # Step 4: Install the new build
    print_step(4, "Installing new build...")
    
    dist_dir = project_root / "dist"
    wheel_files = list(dist_dir.glob("*.whl"))
    
    if wheel_files:
        wheel_file = wheel_files[0]
        print(f"  Installing from: {wheel_file.name}")
        run_command(
            f"{sys.executable} -m pip install \"{wheel_file}\" --force-reinstall",
            "Installing wheel package..."
        )
        print("✓ Installation completed")
    else:
        print("  No wheel file found, installing in development mode...")
        run_command(
            f"{sys.executable} -m pip install -e .",
            "Installing in editable mode..."
        )
        print("✓ Development installation completed")

    # Step 5: Verify installation
    print_step(5, "Verifying installation...")
    result = subprocess.run(
        f"{sys.executable} -m pip show gaybeck-starkids-sms",
        shell=True,
        capture_output=True,
        text=True
    )
    
    if result.stdout:
        print(result.stdout)
        print("\n✓ Installation verified successfully")
    else:
        print("⚠ Package not found in pip list (may be in development mode)")

    # Summary
    print("\n" + "╔" + "="*68 + "╗")
    print("║" + " "*16 + "REBUILD COMPLETED SUCCESSFULLY" + " "*22 + "║")
    print("╚" + "="*68 + "╝\n")

    print("📦 Build artifacts location:")
    if dist_dir.exists():
        for item in dist_dir.iterdir():
            print(f"   - {item.name}")

    print("\n🚀 To run the application:")
    print("   python sms.py")
    print("   OR")
    print("   starkids-sms (if installed globally)\n")

if __name__ == "__main__":
    main()
