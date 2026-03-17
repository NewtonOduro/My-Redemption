@echo off
REM ASCII Image Converter - Build Script
REM This script creates an executable using PyInstaller

echo ASCII Image Converter - Build Script
echo =====================================
echo.

REM Check if PyInstaller is installed
python -m pip list | find "pyinstaller" >nul
if %errorlevel% neq 0 (
    echo PyInstaller not found. Installing...
    pip install pyinstaller
)

echo.
echo Building executable...
pyinstaller ascii_converter.spec

echo.
echo Build complete!
echo Executable created in: dist\ASCII_Image_Converter\
echo.
echo To run the application:
echo.
echo Option 1: Run from dist folder
echo   dist\ASCII_Image_Converter\ASCII_Image_Converter.exe
echo.
echo Option 2: Run from Python
echo   python main.py
echo.
pause
