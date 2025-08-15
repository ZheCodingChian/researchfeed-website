# Research Papers Dashboard

An elegant static web interface for displaying AI research papers with proper LaTeX rendering and interactive features.

## Features

- **Static HTML Generation**: No server required - works offline
- **LaTeX Support**: Mathematical expressions are properly rendered using MathJax
- **HTML Escaping**: All text content is safely escaped to prevent XSS
- **Interactive UI**: Expandable abstracts, justifications, and score comparisons
- **Responsive Design**: Works on both mobile and desktop devices
- **Embedded Data**: Papers data is embedded directly in the HTML file

## Quick Start

### Windows Users
Simply run the batch file:
```cmd
run.bat
```

### Manual Setup

Generate the static HTML file:

```bash
python generate_static_html.py
```

Then open `papers_dashboard.html` in your browser - no server needed!

## How It Works

The system generates a **complete, self-contained HTML file** with your papers data embedded directly in it:

1. **Data Processing**: Processes raw JSON with HTML escaping and LaTeX conversion
2. **Template Injection**: Injects processed data into the page template
3. **Static Output**: Creates `papers_dashboard.html` that works offline

## File Structure

```
├── papers_2025-07-22.json     # Raw papers data (input)
├── page.html                  # HTML template
├── generate_static_html.py    # Static HTML generator
├── papers_dashboard.html      # Generated static page (output)
├── run.bat                    # Windows batch file
└── README.md                  # This file
```

## Data Processing

The `generate_static_html.py` script handles:

### Text Escaping
- HTML characters (`<`, `>`, `&`, `"`, `'`) are properly escaped
- LaTeX expressions are protected during escaping

### LaTeX Conversion
- Inline math: `$expression$` → `\(expression\)`
- Display math: `$$expression$$` → `\[expression\]`
- Mathematical symbols are preserved and rendered by MathJax

### Data Validation
- All paper entries are preserved (including minimal entries)
- Missing or null fields are handled gracefully in the web interface
- Original data structure is maintained exactly as provided

### Static Generation
- Processes data and injects it directly into the HTML template
- Creates a self-contained file that works without a server
- Preserves all interactive functionality

## Web Interface Features

### Paper Display
- **Title**: Clickable link to PDF
- **Authors**: With H-index data when available
- **Abstract**: Truncated with expand/collapse functionality
- **Categories**: Research area tags

### Interactive Elements
- **Similarity Scores**: Toggle between raw and normalized views
- **Justifications**: Expandable sections for recommendations and relevance
- **H-Index Data**: Author publication metrics with Semantic Scholar links

### LaTeX Rendering
- Mathematical expressions render properly using MathJax
- Supports both inline and display math
- Fallback for unsupported expressions

## Browser Compatibility

- Modern browsers with JavaScript enabled
- MathJax requires internet connection for CDN resources
- Responsive design works on mobile and desktop
- **No server required** - works as a local file

## Development

### Adding New Features
1. Modify the data processing in `generate_static_html.py`
2. Update the HTML template (`page.html`)
3. Regenerate the static HTML

### Customizing Styles
- The interface uses Tailwind CSS for styling
- Custom colors and spacing are defined in the configuration
- Responsive breakpoints are pre-configured

## Troubleshooting

### Common Issues

**"Papers data not found"**
- Ensure `papers_2025-07-22.json` exists
- Run `python generate_static_html.py`
- Check for any error messages during generation

**LaTeX not rendering**
- Check internet connection (MathJax CDN required)
- Verify mathematical expressions are properly formatted
- Look for JavaScript console errors in browser

**Styling issues**
- Ensure Tailwind CSS CDN is loading (internet required)
- Check for JavaScript errors in browser console
- Try refreshing the page

### Performance
- Static HTML loads instantly - no server delays
- For very large datasets (>1000 papers), consider chunking
- All data is loaded at once - no pagination needed for 232 papers

## Advantages of Static Generation

✅ **No Server Required**: Open the HTML file directly in any browser  
✅ **Offline Compatible**: Works without internet (except MathJax CDN)  
✅ **Fast Loading**: No AJAX requests or data fetching delays  
✅ **Easy Sharing**: Single file contains everything  
✅ **Simple Deployment**: Just upload the HTML file anywhere  

## License

This project is designed for research and educational purposes.
