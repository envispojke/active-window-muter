@echo off
title Active Window Muter Setup
echo ===================================================
echo     Active Window Muter - Dependency Installer
echo ===================================================
echo.

:: Check if Python is installed and in PATH
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not added to your system PATH!
    echo.
    echo Please download Python 3.8+ from python.org
    echo CRITICAL: Make sure to check the box that says "Add Python to PATH" during installation.
    echo.
    pause
    exit /b 1
)

:: Install the requirements
echo [INFO] Python detected. Installing required libraries...
echo.
pip install -r requirements.txt

:: Check if the installation was successful
echo.
if %errorlevel% equ 0 (
    echo [SUCCESS] All dependencies installed successfully!
    echo You can now close this window and set up your hotkey.
) else (
    echo [ERROR] Something went wrong during installation. Please read the errors above.
)
echo.
pause