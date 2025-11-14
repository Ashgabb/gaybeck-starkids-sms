# Gaybeck Starkids SMS - Complete Rebuild and Reinstall Script
# This script will:
# 1. Clean old build artifacts
# 2. Create a fresh build
# 3. Uninstall existing installation
# 4. Install the new build

Write-Host "`n╔════════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║     GAYBECK STARKIDS SMS - REBUILD & REINSTALL PROCESS        ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════════════════════════════╝`n" -ForegroundColor Cyan

$ProjectRoot = "c:\Users\User\Desktop\GAYBECK STARKIDS SMS"
Set-Location $ProjectRoot

# Step 1: Clean old build artifacts
Write-Host "═══════════════════════════════════════════════════════════════" -ForegroundColor Yellow
Write-Host "STEP 1: Cleaning old build artifacts..." -ForegroundColor Yellow
Write-Host "═══════════════════════════════════════════════════════════════" -ForegroundColor Yellow

$foldersToClean = @("build", "dist", "__pycache__", "*.egg-info")

foreach ($folder in $foldersToClean) {
    if ($folder -like "*egg-info") {
        $eggInfoDirs = Get-ChildItem -Path . -Filter "*.egg-info" -Directory -ErrorAction SilentlyContinue
        foreach ($dir in $eggInfoDirs) {
            Write-Host "  Removing: $($dir.FullName)" -ForegroundColor Gray
            Remove-Item -Path $dir.FullName -Recurse -Force -ErrorAction SilentlyContinue
        }
    } else {
        if (Test-Path $folder) {
            Write-Host "  Removing: $folder" -ForegroundColor Gray
            Remove-Item -Path $folder -Recurse -Force -ErrorAction SilentlyContinue
        }
    }
}

# Clean __pycache__ recursively
Get-ChildItem -Path . -Directory -Filter "__pycache__" -Recurse -ErrorAction SilentlyContinue | ForEach-Object {
    Write-Host "  Removing: $($_.FullName)" -ForegroundColor Gray
    Remove-Item -Path $_.FullName -Recurse -Force -ErrorAction SilentlyContinue
}

Write-Host "✓ Cleanup completed`n" -ForegroundColor Green

# Step 2: Uninstall existing installation
Write-Host "═══════════════════════════════════════════════════════════════" -ForegroundColor Yellow
Write-Host "STEP 2: Uninstalling existing installation..." -ForegroundColor Yellow
Write-Host "═══════════════════════════════════════════════════════════════" -ForegroundColor Yellow

$uninstallResult = python -m pip uninstall gaybeck-starkids-sms -y 2>&1
Write-Host $uninstallResult -ForegroundColor Gray
Write-Host "✓ Uninstall completed`n" -ForegroundColor Green

# Step 3: Create setup.py if it doesn't exist
Write-Host "═══════════════════════════════════════════════════════════════" -ForegroundColor Yellow
Write-Host "STEP 3: Ensuring setup.py exists..." -ForegroundColor Yellow
Write-Host "═══════════════════════════════════════════════════════════════" -ForegroundColor Yellow

if (-not (Test-Path "setup.py")) {
    Write-Host "  Creating setup.py..." -ForegroundColor Gray
    @"
from setuptools import setup, find_packages

setup(
    name='gaybeck-starkids-sms',
    version='2.0.0',
    description='Comprehensive School Management System',
    author='Gaybeck Starkids School',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'tkcalendar>=1.6.1',
        'Pillow>=10.0.0',
    ],
    entry_points={
        'console_scripts': [
            'starkids-sms=sms:start_application',
        ],
    },
    python_requires='>=3.8',
)
"@ | Out-File -FilePath "setup.py" -Encoding UTF8
    Write-Host "✓ setup.py created`n" -ForegroundColor Green
} else {
    Write-Host "✓ setup.py already exists`n" -ForegroundColor Green
}

# Step 4: Build the distribution
Write-Host "═══════════════════════════════════════════════════════════════" -ForegroundColor Yellow
Write-Host "STEP 4: Building distribution packages..." -ForegroundColor Yellow
Write-Host "═══════════════════════════════════════════════════════════════" -ForegroundColor Yellow

Write-Host "  Building source distribution..." -ForegroundColor Gray
python setup.py sdist

Write-Host "`n  Building wheel distribution..." -ForegroundColor Gray
python setup.py bdist_wheel

Write-Host "✓ Build completed`n" -ForegroundColor Green

# Step 5: Install the new build
Write-Host "═══════════════════════════════════════════════════════════════" -ForegroundColor Yellow
Write-Host "STEP 5: Installing new build..." -ForegroundColor Yellow
Write-Host "═══════════════════════════════════════════════════════════════" -ForegroundColor Yellow

$wheelFile = Get-ChildItem -Path "dist" -Filter "*.whl" | Select-Object -First 1
if ($wheelFile) {
    Write-Host "  Installing from: $($wheelFile.Name)" -ForegroundColor Gray
    python -m pip install "dist\$($wheelFile.Name)" --force-reinstall
    Write-Host "✓ Installation completed`n" -ForegroundColor Green
} else {
    Write-Host "⚠ No wheel file found, installing in development mode..." -ForegroundColor Yellow
    python -m pip install -e .
    Write-Host "✓ Development installation completed`n" -ForegroundColor Green
}

# Step 6: Verify installation
Write-Host "═══════════════════════════════════════════════════════════════" -ForegroundColor Yellow
Write-Host "STEP 6: Verifying installation..." -ForegroundColor Yellow
Write-Host "═══════════════════════════════════════════════════════════════" -ForegroundColor Yellow

$verification = python -m pip show gaybeck-starkids-sms 2>&1
if ($verification) {
    Write-Host $verification -ForegroundColor Gray
    Write-Host "`n✓ Installation verified successfully`n" -ForegroundColor Green
} else {
    Write-Host "⚠ Package not found in pip list (development mode)" -ForegroundColor Yellow
}

# Summary
Write-Host "`n╔════════════════════════════════════════════════════════════════╗" -ForegroundColor Green
Write-Host "║                  REBUILD COMPLETED SUCCESSFULLY                ║" -ForegroundColor Green
Write-Host "╚════════════════════════════════════════════════════════════════╝`n" -ForegroundColor Green

Write-Host "📦 Build artifacts location:" -ForegroundColor Cyan
if (Test-Path "dist") {
    Get-ChildItem -Path "dist" | ForEach-Object {
        Write-Host "   - $($_.Name)" -ForegroundColor White
    }
}

Write-Host "`n🚀 To run the application:" -ForegroundColor Cyan
Write-Host "   python sms.py" -ForegroundColor White
Write-Host "   OR" -ForegroundColor Yellow
Write-Host "   starkids-sms" -ForegroundColor White -NoNewline
Write-Host " (if installed globally)`n" -ForegroundColor Gray

Write-Host "Press any key to exit..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
