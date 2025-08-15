#!/bin/bash

echo "Research Papers Dashboard - Static HTML Generator"
echo "================================================"
echo

echo "Generating static HTML with embedded papers data..."
python3 generate_static_html.py

if [ $? -ne 0 ]; then
    echo "ERROR: Failed to generate static HTML!"
    echo "Make sure papers_2025-07-22.json exists and Python 3 is installed."
    exit 1
fi

echo
echo "✅ Success! Generated papers_dashboard.html"
echo
echo "You can now open the file in your browser:"
echo "  papers_dashboard.html"
echo
echo "No web server needed - the page works offline!"

# Try to open in default browser (works on macOS and many Linux distros)
if command -v open >/dev/null 2>&1; then
    open papers_dashboard.html
elif command -v xdg-open >/dev/null 2>&1; then
    xdg-open papers_dashboard.html
else
    echo "Please open papers_dashboard.html manually in your browser."
fi
