# Research Papers Dashboard

An elegant web interface for displaying AI research papers with proper LaTeX rendering and interactive features.

## Features

- **LaTeX Support**: Mathematical expressions are properly rendered using MathJax
- **HTML Escaping**: All text content is safely escaped to prevent XSS
- **Interactive UI**: Expandable abstracts, justifications, and score comparisons
- **Responsive Design**: Works on both mobile and desktop devices
- **Real-time Data**: Loads processed papers data dynamically

## Setup and Usage

### 1. Process the Papers Data

First, run the Python script to process your raw papers JSON file:

```bash
python process_papers.py
```

This script will:
- Load `papers_2025-07-22.json` (your raw papers data)
- Escape HTML characters in all text fields
- Convert LaTeX mathematical notation to MathJax format
- Filter out incomplete entries
- Save the processed data to `processed_papers.json`

### 2. Serve the Website

Start a local HTTP server to serve the files:

```bash
python -m http.server 8000
```

Then open your browser and navigate to:
```
http://localhost:8000/page.html
```

## File Structure

```
├── papers_2025-07-22.json     # Raw papers data (input)
├── processed_papers.json      # Processed papers data (output)
├── process_papers.py          # Python processing script
├── page.html                  # Main web interface
└── README.md                  # This file
```

## Data Processing

The `process_papers.py` script handles:

### Text Escaping
- HTML characters (`<`, `>`, `&`, `"`, `'`) are properly escaped
- LaTeX expressions are protected during escaping

### LaTeX Conversion
- Inline math: `$expression$` → `\(expression\)`
- Display math: `$$expression$$` → `\[expression\]`
- Mathematical symbols are preserved and rendered by MathJax

### Data Validation
- Only complete paper entries are included
- Missing or null fields are handled gracefully
- Original data structure is preserved

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

## Development

### Adding New Features
1. Modify the data processing in `process_papers.py`
2. Update the HTML template and JavaScript in `page.html`
3. Test with your processed data

### Customizing Styles
- The interface uses Tailwind CSS for styling
- Custom colors and spacing are defined in the configuration
- Responsive breakpoints are pre-configured

## Troubleshooting

### Common Issues

**"Failed to load papers data"**
- Ensure `processed_papers.json` exists
- Run `python process_papers.py` first
- Check that the HTTP server is running

**LaTeX not rendering**
- Check internet connection (MathJax CDN)
- Verify mathematical expressions are properly formatted
- Look for JavaScript console errors

**Styling issues**
- Ensure Tailwind CSS CDN is loading
- Check for JavaScript errors in console
- Verify responsive viewport meta tag

### Performance
- For large datasets (>1000 papers), consider implementing pagination
- Virtual scrolling can be added for better performance
- Consider lazy loading for images and heavy content

## License

This project is designed for research and educational purposes.
