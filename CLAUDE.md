# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Architecture

This is a static site generator for a research paper feed. The system generates daily HTML pages showing research papers with filtering, scoring, and analysis capabilities.

### Core Components

- **`builder.py`**: Main static site generator that converts SQLite database papers into static HTML pages with embedded JSON data
- **`template.html`**: HTML template with Tailwind CSS styling, JavaScript filtering/sorting, and data visualization components  
- **`cache.db`**: SQLite database containing research papers with metadata, scores, author h-indexes, and relevance classifications
- **`output/`**: Generated HTML files (one per date) containing the research papers for that day
- **`landingpage.html`**: Landing page for the research feed website

### Database Schema

The `papers` table contains comprehensive paper metadata including:
- Basic paper info (title, authors, abstract, categories, publication date, URLs)
- Processing status fields (scraper_status, intro_status, embedding_status, etc.)
- Relevance scores and justifications for multiple research areas (RLHF, weak supervision, diffusion reasoning, distributed training, datasets)
- Quality metrics (novelty_score, impact_score, recommendation_score)
- Author analysis (h-indexes, author counts, notable authors)

### Template System

The template uses placeholder replacement:
- `PLACEHOLDER_TITLE` → formatted date for page titles
- `<!--DATA_HERE-->` → JSON data containing all papers for the date

The frontend includes:
- Interactive filtering by relevance, scores, h-index, etc.
- Sortable columns and search functionality
- Responsive design with mobile/desktop layouts
- LaTeX rendering support via KaTeX
- Data visualization with progress bars and status indicators

## Development Commands

### Build Static Site
```bash
# Build all pages
python3 builder.py

# Build specific date
python3 builder.py --date 2025-07-15

# Build with paper limit (for testing)
python3 builder.py --max-papers 10
```

### Database Operations
```bash
# View database schema
sqlite3 cache.db ".schema papers"

# Check paper count
sqlite3 cache.db "SELECT COUNT(*) FROM papers"

# List available dates
sqlite3 cache.db "SELECT DISTINCT DATE(published_date) FROM papers ORDER BY DATE(published_date) DESC"
```

## Key Implementation Details

### Data Processing
- Papers are fetched from database using `get_papers_for_date()`
- JSON escaping handles LaTeX notation and prevents script injection
- Date formatting converts ISO datetime to readable format
- Author h-index data is structured as JSON arrays within the database

### Frontend Features
- All filtering/sorting happens client-side via JavaScript embedded in template
- Papers data is embedded as JSON in each HTML file for offline functionality
- Responsive spacing and typography using clamp() CSS functions
- Status indicators use color-coded badges for processing states

### File Organization
- Each generated HTML file is self-contained with embedded data
- Template placeholders allow dynamic content injection
- Static assets (fonts, CSS) loaded from CDNs for simplicity