from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import json
import re
from datetime import datetime
import logging

app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)  # Enable CORS for frontend communication

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DATABASE_PATH = 'cache.db'

def get_db_connection():
    """Get database connection with proper error handling"""
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        conn.row_factory = sqlite3.Row  # Enable column access by name
        return conn
    except sqlite3.Error as e:
        logger.error(f"Database connection error: {e}")
        return None

def parse_json_field(field_value):
    """Safely parse JSON fields from database"""
    if not field_value:
        return []
    try:
        return json.loads(field_value)
    except (json.JSONDecodeError, TypeError):
        logger.warning(f"Failed to parse JSON field: {field_value}")
        return []

def format_paper_data(row):
    """Format a database row into the required JSON structure"""
    try:
        # Parse JSON fields
        authors = parse_json_field(row['authors'])
        categories = parse_json_field(row['categories'])
        author_h_indexes = parse_json_field(row['author_h_indexes'])
        
        # Get text fields (Flask's jsonify will handle proper JSON escaping)
        title = row['title']
        abstract = row['abstract']
        summary = row['summary']
        
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
        
        # Build flat JSON structure
        paper_data = {
            "id": row['id'],
            "title": title,
            "authors": authors,
            "categories": categories,
            "abstract": abstract,
            "published_date": published_date,
            "arxiv_url": row['arxiv_url'],
            "pdf_url": row['pdf_url'],
            "scraper_status": row['scraper_status'],
            "intro_status": row['intro_status'],
            "embedding_status": row['embedding_status'],
            "rlhf_score": row['rlhf_score'],
            "weak_supervision_score": row['weak_supervision_score'],
            "diffusion_reasoning_score": row['diffusion_reasoning_score'],
            "distributed_training_score": row['distributed_training_score'],
            "datasets_score": row['datasets_score'],
            "llm_validation_status": row['llm_validation_status'],
            "rlhf_relevance": row['rlhf_relevance'],
            "weak_supervision_relevance": row['weak_supervision_relevance'],
            "diffusion_reasoning_relevance": row['diffusion_reasoning_relevance'],
            "distributed_training_relevance": row['distributed_training_relevance'],
            "datasets_relevance": row['datasets_relevance'],
            "rlhf_justification": row['rlhf_justification'],
            "weak_supervision_justification": row['weak_supervision_justification'],
            "diffusion_reasoning_justification": row['diffusion_reasoning_justification'],
            "distributed_training_justification": row['distributed_training_justification'],
            "datasets_justification": row['datasets_justification'],
            "llm_score_status": row['llm_score_status'],
            "summary": summary,
            "novelty_score": row['novelty_score'],
            "novelty_justification": row['novelty_justification'],
            "impact_score": row['impact_score'],
            "impact_justification": row['impact_justification'],
            "recommendation_score": row['recommendation_score'],
            "recommendation_justification": row['recommendation_justification'],
            "h_index_status": row['h_index_status'],
            "semantic_scholar_url": row['semantic_scholar_url'],
            "total_authors": row['total_authors'],
            "authors_found": row['authors_found'],
            "highest_h_index": row['highest_h_index'],
            "average_h_index": row['average_h_index'],
            "notable_authors_count": row['notable_authors_count'],
            "author_h_indexes": author_h_indexes
        }
        
        return paper_data
        
    except Exception as e:
        logger.error(f"Error formatting paper data: {e}")
        return None

@app.route('/')
def index():
    """Serve the main page"""
    return app.send_static_file('2025-07-15.html')

@app.route('/2025-07-15.html')
def serve_page():
    """Serve the 2025-07-15 page"""
    return app.send_static_file('2025-07-15.html')

@app.route('/favicon.png')
def favicon():
    """Serve the favicon"""
    return app.send_static_file('favicon.png')

@app.route('/favicon.ico')
def favicon_ico():
    """Serve the favicon as ICO (fallback)"""
    return app.send_static_file('favicon.png')

@app.route('/apple-touch-icon.png')
def apple_touch_icon():
    """Serve the Apple touch icon"""
    return app.send_static_file('apple-touch-icon.png')

@app.route('/apple-touch-icon-precomposed.png')
def apple_touch_icon_precomposed():
    """Serve the Apple touch icon precomposed"""
    return app.send_static_file('apple-touch-icon-precomposed.png')

@app.route('/api/papers/count')
def get_papers_count():
    """Get total count of papers for a specific date"""
    date = request.args.get('date')
    
    if not date:
        return jsonify({"error": "Date parameter is required (YYYY-MM-DD format)"}), 400
    
    # Validate date format
    try:
        datetime.strptime(date, '%Y-%m-%d')
    except ValueError:
        return jsonify({"error": "Invalid date format. Use YYYY-MM-DD"}), 400
    
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
    
    try:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT COUNT(*) as total FROM papers WHERE DATE(published_date) = ?",
            (date,)
        )
        result = cursor.fetchone()
        total_papers = result['total']
        
        return jsonify({"total_papers": total_papers})
        
    except sqlite3.Error as e:
        logger.error(f"Database query error: {e}")
        return jsonify({"error": "Database query failed"}), 500
    finally:
        conn.close()

@app.route('/api/papers')
def get_papers():
    """Get paginated papers for a specific date"""
    date = request.args.get('date')
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 10, type=int)
    
    if not date:
        return jsonify({"error": "Date parameter is required (YYYY-MM-DD format)"}), 400
    
    # Validate date format
    try:
        datetime.strptime(date, '%Y-%m-%d')
    except ValueError:
        return jsonify({"error": "Invalid date format. Use YYYY-MM-DD"}), 400
    
    # Validate pagination parameters
    if page < 1:
        return jsonify({"error": "Page must be >= 1"}), 400
    if limit < 1 or limit > 100:
        return jsonify({"error": "Limit must be between 1 and 100"}), 400
    
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
    
    try:
        cursor = conn.cursor()
        
        # Get total count for pagination info
        cursor.execute(
            "SELECT COUNT(*) as total FROM papers WHERE DATE(published_date) = ?",
            (date,)
        )
        total_papers = cursor.fetchone()['total']
        
        if total_papers == 0:
            return jsonify({
                "papers": [],
                "page": page,
                "limit": limit,
                "total_papers": 0,
                "total_pages": 0,
                "has_next": False,
                "has_prev": False
            })
        
        # Calculate pagination
        total_pages = (total_papers + limit - 1) // limit  # Ceiling division
        offset = (page - 1) * limit
        
        # Check if page is out of bounds
        if page > total_pages:
            return jsonify({"error": f"Page {page} is out of bounds. Total pages: {total_pages}"}), 400
        
        # Get papers for the requested page (ordered by arXiv ID)
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
        ORDER BY id
        LIMIT ? OFFSET ?
        """
        
        cursor.execute(query, (date, limit, offset))
        rows = cursor.fetchall()
        
        # Format papers data
        papers = []
        for row in rows:
            paper_data = format_paper_data(row)
            if paper_data:
                papers.append(paper_data)
        
        response = {
            "papers": papers,
            "page": page,
            "limit": limit,
            "total_papers": total_papers,
            "total_pages": total_pages,
            "has_next": page < total_pages,
            "has_prev": page > 1
        }
        
        return jsonify(response)
        
    except sqlite3.Error as e:
        logger.error(f"Database query error: {e}")
        return jsonify({"error": "Database query failed"}), 500
    finally:
        conn.close()

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    logger.info("Starting Research Feed API server...")
    app.run(debug=True, host='127.0.0.1', port=5000)
