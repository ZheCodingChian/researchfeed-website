
# Prompt for Building SSG Architecture

You are tasked with completely rebuilding a research paper website from a Flask API-based architecture to a Static Site Generator (SSG) approach. This is a complete architectural overhaul with no backward compatibility required.

## Context \& Current State

The current system is a Flask API server that serves research paper data from a SQLite database (`cache.db`) through REST endpoints. The frontend makes API calls to fetch paginated paper data by date. The database contains comprehensive paper metadata including LaTeX notation in titles/abstracts, relevance scores, author h-indexes, and LLM-generated summaries.

**Current pain points:**

- Runtime API dependency
- Server hosting requirements
- Dynamic data fetching complexity

**Goal:** Transform this into a static site that pre-builds HTML pages with embedded JSON data, eliminating runtime API calls entirely.

## Task 1: Rebuild Project Structure

Create a new SSG project structure that separates build-time logic from static output:

```
research-feed-ssg/
├── builder.py              # Build script (your main task)
├── template.html           # Single HTML template  
├── cache.db               # Existing SQLite database (unchanged)
├── output/                # Generated static files
└── static/                # CSS/JS assets
```


## Task 2: Create template.html

Build a single HTML template that:

1. **Contains a complete webpage structure** with:
    - Header/navigation
    - Container div for paper cards (populated by JavaScript)
    - Footer
2. **Includes a JSON data placeholder using exactly this pattern:**

```html
<script id="paper-data" type="application/json">
<!--DATA_HERE-->
</script>
```

3. **Includes JavaScript that:**
    - Reads the embedded JSON: `JSON.parse(document.getElementById('paper-data').textContent)`
    - Dynamically generates paper card HTML from the JSON data
    - Handles LaTeX rendering (assume MathJax/KaTeX will be included)
4. **Remove all API fetch logic** - no XHR, fetch(), or AJAX calls anywhere
5. **Make it self-contained** - all necessary CSS and JavaScript should be inline or referenced locally

## Task 3: Build builder.py

Create a Python script that:

1. **Connects to the existing SQLite database** (`cache.db`) using the exact same schema as the current Flask API
2. **Queries paper data** with the same fields as the current API response:
    - Core fields: id, title, authors, categories, abstract, published_date, arxiv_url, pdf_url
    - Scores: rlhf_score, weak_supervision_score, diffusion_reasoning_score, etc.
    - LLM data: summary, novelty_score, impact_score, recommendation_score, justifications
    - Author data: h_index_status, author_h_indexes array, etc.
    - All status fields and relevance assessments
3. **Organizes data by publication date** (published_date field)
4. **For each date, generates one HTML file:**
    - Read `template.html`
    - Serialize the papers array for that date as JSON using `json.dumps(papers, ensure_ascii=False)`
    - Replace `<!--DATA_HERE-->` with the serialized JSON
    - Write the complete HTML to `output/papers_YYYY-MM-DD.html`
5. **Preserves LaTeX notation** in all text fields (titles, abstracts, summaries) during JSON serialization
6. **Creates an index page** (`output/index.html`) that lists all available dates with links
7. **Handles the JSON embedding safely** - ensure no `</script>` injection issues by using proper escaping

## Task 4: Requirements \& Constraints

- **No backward compatibility** - completely replace the Flask API approach
- **Preserve all existing data fields** from the current API response format
- **Maintain LaTeX notation** throughout the process (crucial for mathematical expressions)
- **Generate static files only** - no server-side processing after build
- **Use the exact same SQLite schema** - do not modify the database structure
- **Make it a complete, working system** - the output should be deployable to any static hosting


## Expected Deliverables

1. `template.html` - Complete HTML template with embedded JSON placeholder
2. `builder.py` - Complete Python build script that generates all static pages
3. Working static site in `output/` directory ready for deployment

The final result should be a static website where each date has its own HTML page containing all papers for that date embedded as JSON, with JavaScript dynamically rendering the paper cards from that embedded data.

