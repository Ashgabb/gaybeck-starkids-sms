#!/bin/bash
# Build script for macOS and Linux
# Creates standalone executable using PyInstaller

set -e  # Exit on error

echo "╔════════════════════════════════════════════════════╗"
echo "║  Gaybeck Starkids SMS - Build Script (macOS/Linux) ║"
echo "║  Version: 2.0.3                                    ║"
echo "╚════════════════════════════════════════════════════╝"
echo ""

# Check Python version
echo "Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "✓ Python $python_version detected"

if ! command -v python3 &> /dev/null; then
    echo "✗ Python 3 is required but not installed."
    echo "Please install Python 3.13+ from https://www.python.org"
    exit 1
fi

# Create virtual environment
echo ""
echo "Setting up virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi

# Activate virtual environment
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi
echo "✓ Virtual environment activated"

# Upgrade pip
echo ""
echo "Upgrading pip..."
pip install --upgrade pip

# Install PyInstaller
echo ""
echo "Installing PyInstaller..."
pip install pyinstaller>=6.0

# Install application dependencies
echo ""
echo "Installing application dependencies..."
pip install -r requirements.txt

# Clean previous builds
echo ""
echo "Cleaning previous builds..."
rm -rf build dist *.spec
echo "✓ Cleanup complete"

# Build executable
echo ""
echo "Building executable (this may take 2-3 minutes)..."
pyinstaller build_config.spec --onedir

# Create distribution package
echo ""
echo "Creating distribution package..."
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    app_name="GaybeckStarKidsSMS.app"
    if [ -d "dist/$app_name" ]; then
        cd dist
        zip -r "GaybeckStarKidsSMS_macOS_$(date +%Y%m%d).zip" "$app_name"
        cd ..
        echo "✓ macOS app package created: dist/GaybeckStarKidsSMS_macOS_$(date +%Y%m%d).zip"
    fi
else
    # Linux
    if [ -d "dist/GaybeckStarKidsSMS" ]; then
        cd dist
        tar -czf "GaybeckStarKidsSMS_linux_$(date +%Y%m%d).tar.gz" GaybeckStarKidsSMS
        cd ..
        echo "✓ Linux package created: dist/GaybeckStarKidsSMS_linux_$(date +%Y%m%d).tar.gz"
    fi
fi

echo ""
echo "╔════════════════════════════════════════════════════╗"
echo "║  ✓ Build Complete!                                 ║"
echo "║                                                    ║"
echo "║  Executable location:                              ║"
echo "║  → dist/GaybeckStarKidsSMS/GaybeckStarKidsSMS      ║"
echo "║                                                    ║"
echo "║  To run:                                           ║"
echo "║  → ./dist/GaybeckStarKidsSMS/GaybeckStarKidsSMS    ║"
echo "║                                                    ║"
echo "╚════════════════════════════════════════════════════╝"
echo ""
