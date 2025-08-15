@echo off
echo Research Papers Dashboard - Static HTML Generator
echo ================================================
echo.

echo Generating static HTML with embedded papers data...
python generate_static_html.py

if %ERRORLEVEL% neq 0 (
    echo ERROR: Failed to generate static HTML!
    echo Make sure papers_2025-07-22.json exists and Python is installed.
    pause
    exit /b 1
)

echo.
echo ✅ Success! Opening papers_dashboard.html in your default browser...
echo.
echo You can also open the file directly:
echo   papers_dashboard.html
echo.
echo No web server needed - the page works offline!

start papers_dashboard.html
