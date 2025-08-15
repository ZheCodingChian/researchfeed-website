@echo off
echo Research Papers Dashboard - Setup Script
echo ==========================================
echo.

echo Step 1: Processing papers data...
python process_papers.py

if %ERRORLEVEL% neq 0 (
    echo ERROR: Failed to process papers data!
    echo Make sure papers_2025-07-22.json exists and Python is installed.
    pause
    exit /b 1
)

echo.
echo Step 2: Starting web server...
echo The website will be available at: http://localhost:8000/page.html
echo Press Ctrl+C to stop the server
echo.

python -m http.server 8000
