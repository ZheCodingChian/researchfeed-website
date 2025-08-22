# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

### Build Static Site
```bash
# Build all available dates from database
python builder.py

# Build specific date only
python builder.py --date 2025-07-15

# Build with limited papers per date (useful for testing)
python builder.py --max-papers 10
```

### Installing Dependencies
```bash
pip install -r requirements.txt
```

## Project Architecture

This is a **static site generator** for a research paper feed website. The architecture consists of:

### Core Components

1. **`builder.py`** - Main static site generator that:
   - Connects to SQLite database (`cache.db`) containing research papers
   - Processes paper data with safe JSON escaping for web display
   - Generates static HTML pages using template injection
   - Outputs date-specific pages to `output/` directory

2. **`template.html`** - HTML template with:
   - Responsive design using Tailwind CSS
   - Placeholder injection points for dynamic content
   - Complex JavaScript-based paper filtering and display system
   - Mathematical notation support via KaTeX

3. **`landingpage.html`** - Static landing page showcasing daily paper feeds

4. **`cache.db`** - SQLite database containing research papers with extensive metadata including:
   - Author information and H-index data
   - Topic relevance scores (RLHF, weak supervision, diffusion reasoning, etc.)
   - Novelty, impact, and recommendation scores
   - Abstract summaries and justifications

### Data Flow
1. Papers are stored in SQLite database with rich metadata
2. `builder.py` queries database by publication date
3. Paper data is safely escaped and serialized to JSON
4. JSON data is injected into HTML template placeholders
5. Static HTML files are generated in `output/` directory

### Key Features
- **Security-focused**: Extensive JSON escaping and HTML injection prevention
- **Responsive design**: Mobile-first approach with desktop adaptations
- **Rich metadata**: Papers include AI-generated scores, summaries, and topic relevance
- **Date-based organization**: Each day's papers get their own static page

### File Structure
```
├── builder.py          # Static site generator
├── template.html       # Main HTML template
├── landingpage.html    # Landing page
├── cache.db           # SQLite database
├── requirements.txt   # Python dependencies
└── output/           # Generated static pages
    ├── 2025-07-09.html
    ├── 2025-07-10.html
    └── ...
```

## Database Schema Notes

The `papers` table contains comprehensive metadata including:
- Basic paper info (title, authors, abstract, URLs)
- AI-generated relevance scores for specific topics
- Author H-index data from academic databases
- Quality scores (novelty, impact, recommendation)
- Processing status fields for various pipeline stages