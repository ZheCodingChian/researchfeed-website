#!/usr/bin/env python3
"""
Static Site Generator for Research Feed
Converts database papers into static HTML pages with embedded JSON data.
"""

import sqlite3
import json
import os
import re
import argparse
import logging
from datetime import datetime
from typing import List, Dict, Any, Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger(__name__)

# Constants
DATABASE_PATH = 'cache.db'
TEMPLATE_PATH = 'template.html'
OUTPUT_DIR = 'output'


def safe_json_escape(text: Any) -> Any:
    """
    Safely escape text for JSON embedding in HTML.
    Handles LaTeX notation, special characters, and potential injection issues.
    """
    if text is None:
        return None
    
    if not isinstance(text, str):
        return text
    
    # # Escape JSON-breaking characters in order
    # text = text.replace('\\', '\\\\')   # Escape backslashes first (for LaTeX)
    # text = text.replace('"', '\\"')     # Escape double quotes
    # text = text.replace('\n', '\\n')    # Escape newlines
    # text = text.replace('\r', '\\r')    # Escape carriage returns
    # text = text.replace('\t', '\\t')    # Escape tabs
    # text = text.replace('\b', '\\b')    # Escape backspace
    # text = text.replace('\f', '\\f')    # Escape form feed
    
    return text


def safe_json_dumps(data: Dict[str, Any]) -> str:
    """
    Safely serialize data to JSON with proper escaping and formatting.
    """
    try:
        # Use ensure_ascii=False to preserve Unicode, with proper indentation
        json_str = json.dumps(data, ensure_ascii=False, indent=2)
        
        # Additional HTML-safe escaping for script injection prevention
        json_str = json_str.replace('</script>', '<\\/script>')
        json_str = json_str.replace('<!--', '<\\!--')
        json_str = json_str.replace('-->', '--\\>')
        
        return json_str
        
    except (TypeError, ValueError) as e:
        logger.error(f"JSON serialization failed: {e}")
        raise Exception(f"Failed to serialize data to JSON: {e}")


def get_db_connection() -> sqlite3.Connection:
    """Get database connection with proper error handling."""
    try:
        if not os.path.exists(DATABASE_PATH):
            raise FileNotFoundError(f"Database file not found: {DATABASE_PATH}")
            
        conn = sqlite3.connect(DATABASE_PATH)
        conn.row_factory = sqlite3.Row  # Enable column access by name
        return conn
        
    except sqlite3.Error as e:
        logger.error(f"Database connection failed: {e}")
        raise Exception(f"Cannot connect to database: {e}")


def parse_json_field(field_value: str) -> List[Any]:
    """Safely parse JSON fields from database."""
    if not field_value:
        return []
    
    try:
        return json.loads(field_value)
    except (json.JSONDecodeError, TypeError) as e:
        logger.warning(f"Failed to parse JSON field: {field_value[:50]}...")
        return []


def format_paper_data(row: sqlite3.Row) -> Dict[str, Any]:
    """
    Format a database row into the required JSON structure with safe escaping.
    """
    try:
        # Parse JSON fields with validation
        authors = parse_json_field(row['authors'])
        categories = parse_json_field(row['categories']) 
        author_h_indexes = parse_json_field(row['author_h_indexes'])
        
        # Apply safe escaping to text fields
        title = safe_json_escape(row['title'])
        abstract = safe_json_escape(row['abstract'])
        summary = safe_json_escape(row['summary'])
        
        # Apply escaping to justification fields
        recommendation_justification = safe_json_escape(row['recommendation_justification'])
        novelty_justification = safe_json_escape(row['novelty_justification'])
        impact_justification = safe_json_escape(row['impact_justification'])
        rlhf_justification = safe_json_escape(row['rlhf_justification'])
        weak_supervision_justification = safe_json_escape(row['weak_supervision_justification'])
        diffusion_reasoning_justification = safe_json_escape(row['diffusion_reasoning_justification'])
        distributed_training_justification = safe_json_escape(row['distributed_training_justification'])
        datasets_justification = safe_json_escape(row['datasets_justification'])
        
        # Apply escaping to author names in arrays
        escaped_authors = [safe_json_escape(author) for author in authors]
        escaped_categories = [safe_json_escape(cat) for cat in categories]
        
        # Handle author h-indexes with escaping
        escaped_author_h_indexes = []
        for author_info in author_h_indexes:
            if isinstance(author_info, dict):
                escaped_author_info = {
                    'name': safe_json_escape(author_info.get('name', '')),
                    'h_index': author_info.get('h_index', 0),
                    'profile_url': safe_json_escape(author_info.get('profile_url', ''))
                }
                escaped_author_h_indexes.append(escaped_author_info)
        
        # Format date (extract date part from ISO datetime)
        published_date = row['published_date']
        if published_date:
            try:
                # Parse ISO format and extract date
                dt = datetime.fromisoformat(published_date.replace('Z', '+00:00'))
                published_date = dt.strftime('%Y-%m-%d')
            except (ValueError, AttributeError):
                # If parsing fails, try to extract YYYY-MM-DD pattern
                match = re.search(r'(\d{4}-\d{2}-\d{2})', published_date)
                published_date = match.group(1) if match else published_date
        
        # Build complete paper data structure
        paper_data = {
            "id": row['id'],
            "title": title,
            "authors": escaped_authors,
            "categories": escaped_categories,
            "abstract": abstract,
            "published_date": published_date,
            "arxiv_url": row['arxiv_url'],
            "pdf_url": row['pdf_url'],
            "scraper_status": row['scraper_status'],
            "intro_status": row['intro_status'],
            "embedding_status": row['embedding_status'],
            "rlhf_score": float(row['rlhf_score']) if row['rlhf_score'] is not None else 0.0,
            "weak_supervision_score": float(row['weak_supervision_score']) if row['weak_supervision_score'] is not None else 0.0,
            "diffusion_reasoning_score": float(row['diffusion_reasoning_score']) if row['diffusion_reasoning_score'] is not None else 0.0,
            "distributed_training_score": float(row['distributed_training_score']) if row['distributed_training_score'] is not None else 0.0,
            "datasets_score": float(row['datasets_score']) if row['datasets_score'] is not None else 0.0,
            "llm_validation_status": row['llm_validation_status'],
            "rlhf_relevance": row['rlhf_relevance'],
            "weak_supervision_relevance": row['weak_supervision_relevance'],
            "diffusion_reasoning_relevance": row['diffusion_reasoning_relevance'],
            "distributed_training_relevance": row['distributed_training_relevance'],
            "datasets_relevance": row['datasets_relevance'],
            "rlhf_justification": rlhf_justification,
            "weak_supervision_justification": weak_supervision_justification,
            "diffusion_reasoning_justification": diffusion_reasoning_justification,
            "distributed_training_justification": distributed_training_justification,
            "datasets_justification": datasets_justification,
            "llm_score_status": row['llm_score_status'],
            "summary": summary,
            "novelty_score": row['novelty_score'],
            "novelty_justification": novelty_justification,
            "impact_score": row['impact_score'],
            "impact_justification": impact_justification,
            "recommendation_score": row['recommendation_score'],
            "recommendation_justification": recommendation_justification,
            "h_index_status": row['h_index_status'],
            "semantic_scholar_url": row['semantic_scholar_url'],
            "total_authors": row['total_authors'] if row['total_authors'] is not None else 0,
            "authors_found": row['authors_found'] if row['authors_found'] is not None else 0,
            "highest_h_index": row['highest_h_index'] if row['highest_h_index'] is not None else 0,
            "average_h_index": float(row['average_h_index']) if row['average_h_index'] is not None else 0.0,
            "notable_authors_count": row['notable_authors_count'] if row['notable_authors_count'] is not None else 0,
            "author_h_indexes": escaped_author_h_indexes
        }
        
        return paper_data
        
    except Exception as e:
        logger.error(f"Error formatting paper {row.get('id', 'unknown')}: {e}")
        raise Exception(f"Failed to format paper data: {e}")


def get_all_dates() -> List[str]:
    """Get all unique dates that have papers in the database."""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT DISTINCT DATE(published_date) as date 
            FROM papers 
            WHERE published_date IS NOT NULL 
            ORDER BY date DESC
        """)
        
        dates = [row['date'] for row in cursor.fetchall()]
        logger.info(f"Found {len(dates)} unique dates in database")
        return dates
        
    except sqlite3.Error as e:
        logger.error(f"Database query failed: {e}")
        raise Exception(f"Failed to query dates: {e}")
    finally:
        conn.close()


def get_papers_for_date(date: str, max_papers: Optional[int] = None) -> Dict[str, Any]:
    """Get all papers for a specific date."""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        
        # Get total count first
        cursor.execute(
            "SELECT COUNT(*) as total FROM papers WHERE DATE(published_date) = ?",
            (date,)
        )
        total_papers = cursor.fetchone()['total']
        
        if total_papers == 0:
            logger.warning(f"No papers found for date {date}")
            return {
                "papers": [],
                "total_papers": 0,
                "date": date
            }
        
        # Build query with optional limit
        query = """
        SELECT id, title, authors, categories, abstract, published_date, arxiv_url, pdf_url,
               scraper_status, intro_status, embedding_status, rlhf_score, weak_supervision_score,
               diffusion_reasoning_score, distributed_training_score, datasets_score,
               llm_validation_status, rlhf_relevance, weak_supervision_relevance,
               diffusion_reasoning_relevance, distributed_training_relevance, datasets_relevance,
               rlhf_justification, weak_supervision_justification, diffusion_reasoning_justification,
               distributed_training_justification, datasets_justification, llm_score_status,
               summary, novelty_score, novelty_justification, impact_score, impact_justification,
               recommendation_score, recommendation_justification, h_index_status, semantic_scholar_url,
               total_authors, authors_found, highest_h_index, average_h_index, notable_authors_count,
               author_h_indexes
        FROM papers 
        WHERE DATE(published_date) = ?
        ORDER BY id ASC
        """
        
        if max_papers:
            query += f" LIMIT {max_papers}"
            logger.info(f"Limiting to {max_papers} papers for {date}")
        
        cursor.execute(query, (date,))
        rows = cursor.fetchall()
        
        # Format papers data
        papers = []
        for row in rows:
            paper_data = format_paper_data(row)
            papers.append(paper_data)
        
        result = {
            "papers": papers,
            "total_papers": len(papers),  # Use actual count (may be limited)
            "date": date
        }
        
        logger.info(f"Processed {len(papers)} papers for {date}")
        return result
        
    except sqlite3.Error as e:
        logger.error(f"Database query failed for {date}: {e}")
        raise Exception(f"Failed to query papers for {date}: {e}")
    finally:
        conn.close()


def format_date_for_title(date_str: str) -> str:
    """Format YYYY-MM-DD date into human readable format."""
    try:
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        return date_obj.strftime('%d %B %Y')  # "15 July 2025"
    except ValueError:
        logger.warning(f"Invalid date format: {date_str}")
        return date_str


def generate_static_page(date: str, paper_data: Dict[str, Any], template_content: str) -> str:
    """
    Generate static HTML page by injecting paper data into template.
    """
    try:
        # Format date for titles
        formatted_date = format_date_for_title(date)
        page_title = f"Papers Published on {formatted_date}"
        
        # Serialize paper data to JSON
        json_data = safe_json_dumps(paper_data)
        
        # Replace placeholders in template
        html_content = template_content
        
        # Replace title placeholders
        html_content = html_content.replace('PLACEHOLDER_TITLE', formatted_date)
        html_content = html_content.replace('PLACEHOLDER_MOBILE_TITLE', page_title)
        html_content = html_content.replace('PLACEHOLDER_DESKTOP_TITLE', page_title)
        
        # Replace data placeholder
        html_content = html_content.replace('<!--DATA_HERE-->', json_data)
        
        return html_content
        
    except Exception as e:
        logger.error(f"Failed to generate page for {date}: {e}")
        raise Exception(f"Page generation failed: {e}")


def build_static_site(target_date: Optional[str] = None, max_papers: Optional[int] = None):
    """
    Main build function - generates static HTML pages.
    """
    logger.info("Starting static site build")
    
    # Validate template exists
    if not os.path.exists(TEMPLATE_PATH):
        raise FileNotFoundError(f"Template file not found: {TEMPLATE_PATH}")
    
    # Read template content
    try:
        with open(TEMPLATE_PATH, 'r', encoding='utf-8') as f:
            template_content = f.read()
        logger.info(f"Loaded template from {TEMPLATE_PATH}")
    except Exception as e:
        raise Exception(f"Failed to read template: {e}")
    
    # Create output directory
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    logger.info(f"Output directory: {OUTPUT_DIR}")
    
    # Get dates to process
    if target_date:
        dates = [target_date]
        logger.info(f"Building single date: {target_date}")
    else:
        dates = get_all_dates()
        logger.info(f"Building all dates: {len(dates)} total")
    
    # Process each date
    built_pages = 0
    for date in dates:
        try:
            logger.info(f"Processing {date}")
            
            # Get paper data for this date
            paper_data = get_papers_for_date(date, max_papers)
            
            if paper_data['total_papers'] == 0:
                logger.warning(f"Skipping {date} - no papers found")
                continue
            
            # Generate HTML page
            html_content = generate_static_page(date, paper_data, template_content)
            
            # Write to file
            output_file = os.path.join(OUTPUT_DIR, f"{date}.html")
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            logger.info(f"Generated {output_file} with {paper_data['total_papers']} papers")
            built_pages += 1
            
        except Exception as e:
            logger.error(f"Failed to build page for {date}: {e}")
            raise Exception(f"Build failed for {date}: {e}")
    
    logger.info(f"Build completed successfully. Generated {built_pages} pages in {OUTPUT_DIR}")


def main():
    """Main entry point with command line argument parsing."""
    parser = argparse.ArgumentParser(
        description='Build static HTML pages from research paper database'
    )
    parser.add_argument(
        '--date', 
        type=str, 
        help='Build only specific date (YYYY-MM-DD format)'
    )
    parser.add_argument(
        '--max-papers', 
        type=int, 
        help='Maximum number of papers per date (for testing)'
    )
    
    args = parser.parse_args()
    
    try:
        # Validate date format if provided
        if args.date:
            try:
                datetime.strptime(args.date, '%Y-%m-%d')
            except ValueError:
                logger.error(f"Invalid date format: {args.date}. Use YYYY-MM-DD")
                return 1
        
        # Validate max_papers if provided
        if args.max_papers and args.max_papers <= 0:
            logger.error(f"max-papers must be positive integer, got: {args.max_papers}")
            return 1
        
        # Run the build
        build_static_site(
            target_date=args.date,
            max_papers=args.max_papers
        )
        
        return 0
        
    except Exception as e:
        logger.error(f"Build failed: {e}")
        return 1


if __name__ == '__main__':
    exit(main())
