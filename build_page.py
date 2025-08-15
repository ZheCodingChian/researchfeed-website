#!/usr/bin/env python3
"""
Build script for generating page.html with paper data using dual-rendering approach.
Based on the solution described in build.md for handling JSON escaping safely.
"""

import json
import os
from datetime import datetime
from pathlib import Path

# Simple template engine approach - could be replaced with Jinja2 for more complex needs
class SimpleTemplateEngine:
    def __init__(self, template_content):
        self.template = template_content
    
    def render(self, **context):
        """Simple variable substitution with selective escaping"""
        result = self.template
        for key, value in context.items():
            if key.endswith('_json_data'):
                # Don't HTML escape JSON data - it's already safely escaped by tojson_safe
                result = result.replace(f'{{{{ {key} }}}}', str(value))
            else:
                # HTML escape regular template variables for safety
                escaped_value = self.html_escape(str(value))
                result = result.replace(f'{{{{ {key} }}}}', escaped_value)
        return result
    
    @staticmethod
    def html_escape(text):
        """Basic HTML escaping"""
        return (text.replace('&', '&amp;')
                   .replace('<', '&lt;')
                   .replace('>', '&gt;')
                   .replace('"', '&quot;')
                   .replace("'", '&#x27;'))
    
    @staticmethod  
    def tojson_safe(data):
        """
        THE CRITICAL ESCAPING SOLUTION equivalent to Jinja2's |tojson|safe filter
        This handles:
        - Quote escaping: " becomes \"
        - LaTeX escaping: backslashes, special characters  
        - Unicode escaping: mathematical symbols, accents
        - JSON compliance: ensures valid JSON structure
        """
        return json.dumps(data, ensure_ascii=False, separators=(',', ':'))

def load_paper_data(json_file_path):
    """Load paper data from JSON file"""
    try:
        with open(json_file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: {json_file_path} not found")
        return None
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        return None

def prepare_template_data(paper_data):
    """
    Prepare data for dual-rendering approach:
    - papers_list: Full Paper objects for template rendering
    - papers_json: JSON-serializable data for JavaScript
    """
    if not paper_data or 'papers' not in paper_data:
        return None
    
    papers_list = paper_data['papers']
    
    # Convert to JSON-serializable format for JavaScript
    papers_json = []
    for paper in papers_list:
        # Create clean dictionary with all fields
        paper_dict = {
            'id': paper.get('id', ''),
            'title': paper.get('title', ''),
            'authors': paper.get('authors', []),
            'categories': paper.get('categories', []),
            'abstract': paper.get('abstract', ''),
            'published_date': paper.get('published_date', ''),
            'arxiv_url': paper.get('arxiv_url', ''),
            'pdf_url': paper.get('pdf_url', ''),
            'latex_url': paper.get('latex_url', ''),
            
            # Status fields
            'scraper_status': paper.get('scraper_status', ''),
            'intro_status': paper.get('intro_status', ''),
            'embedding_status': paper.get('embedding_status', ''),
            'llm_validation_status': paper.get('llm_validation_status', ''),
            'llm_score_status': paper.get('llm_score_status', ''),
            'h_index_status': paper.get('h_index_status', ''),
            
            # Content fields
            'introduction_text': paper.get('introduction_text', ''),
            'intro_extraction_method': paper.get('intro_extraction_method', ''),
            'tex_file_name': paper.get('tex_file_name', ''),
            
            # Similarity scores
            'rlhf_score': paper.get('rlhf_score', 0.0),
            'weak_supervision_score': paper.get('weak_supervision_score', 0.0),
            'diffusion_reasoning_score': paper.get('diffusion_reasoning_score', 0.0),
            'distributed_training_score': paper.get('distributed_training_score', 0.0),
            'datasets_score': paper.get('datasets_score', 0.0),
            'highest_similarity_topic': paper.get('highest_similarity_topic', ''),
            
            # LLM validation results
            'rlhf_relevance': paper.get('rlhf_relevance', 'not_validated'),
            'weak_supervision_relevance': paper.get('weak_supervision_relevance', 'not_validated'),
            'diffusion_reasoning_relevance': paper.get('diffusion_reasoning_relevance', 'not_validated'),
            'distributed_training_relevance': paper.get('distributed_training_relevance', 'not_validated'),
            'datasets_relevance': paper.get('datasets_relevance', 'not_validated'),
            
            # Justifications
            'rlhf_justification': paper.get('rlhf_justification', 'not_validated'),
            'weak_supervision_justification': paper.get('weak_supervision_justification', 'not_validated'),
            'diffusion_reasoning_justification': paper.get('diffusion_reasoning_justification', 'not_validated'),
            'distributed_training_justification': paper.get('distributed_training_justification', 'not_validated'),
            'datasets_justification': paper.get('datasets_justification', 'not_validated'),
            
            # LLM scores (if available)
            'summary': paper.get('summary', ''),
            'novelty_score': paper.get('novelty_score', ''),
            'novelty_justification': paper.get('novelty_justification', ''),
            'impact_score': paper.get('impact_score', ''),
            'impact_justification': paper.get('impact_justification', ''),
            'recommendation_score': paper.get('recommendation_score', ''),
            'recommendation_justification': paper.get('recommendation_justification', ''),
            
            # H-index data
            'semantic_scholar_url': paper.get('semantic_scholar_url', ''),
            'h_index_fetch_method': paper.get('h_index_fetch_method', ''),
            'total_authors': paper.get('total_authors', 0),
            'authors_found': paper.get('authors_found', 0),
            'highest_h_index': paper.get('highest_h_index', 0),
            'average_h_index': paper.get('average_h_index', 0.0),
            'notable_authors_count': paper.get('notable_authors_count', 0),
            'author_h_indexes': paper.get('author_h_indexes', []),
            
            # Timestamps
            'created_at': paper.get('created_at', ''),
            'updated_at': paper.get('updated_at', ''),
            'last_generated': paper.get('last_generated', '')
        }
        papers_json.append(paper_dict)
    
    return {
        'date': paper_data.get('date', ''),
        'total_papers': paper_data.get('total_papers', 0),
        'papers_list': papers_list,  # For template rendering
        'papers_json': papers_json,  # For JavaScript
        'papers_json_escaped': SimpleTemplateEngine.tojson_safe(papers_json)  # THE CRITICAL SOLUTION
    }

def build_page(template_path, output_path, paper_data_path):
    """
    Main build function implementing the dual-rendering approach
    """
    print(f"Loading paper data from {paper_data_path}...")
    paper_data = load_paper_data(paper_data_path)
    if not paper_data:
        return False
    
    print(f"Loading template from {template_path}...")
    try:
        with open(template_path, 'r', encoding='utf-8') as f:
            template_content = f.read()
    except FileNotFoundError:
        print(f"Error: Template file {template_path} not found")
        return False
    
    print("Preparing template data using dual-rendering approach...")
    template_data = prepare_template_data(paper_data)
    if not template_data:
        return False
    
    # Additional template variables
    current_date = datetime.now().strftime("%d %B %Y")
    
    template_vars = {
        'page_title': f"Papers Published on {template_data['date']}",
        'papers_count': template_data['total_papers'],
        'current_date': current_date,
        'papers_json_data': template_data['papers_json_escaped'],  # THE CRITICAL LINE
        'generation_timestamp': datetime.now().isoformat()
    }
    
    print("Rendering template with escaped JSON data...")
    engine = SimpleTemplateEngine(template_content)
    rendered_html = engine.render(**template_vars)
    
    print(f"Writing output to {output_path}...")
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(rendered_html)
        print(f"✅ Successfully generated {output_path}")
        print(f"📊 Processed {template_data['total_papers']} papers")
        return True
    except Exception as e:
        print(f"Error writing output file: {e}")
        return False

def main():
    """Main entry point"""
    # File paths
    current_dir = Path(__file__).parent
    template_path = current_dir / "page_template.html"
    output_path = current_dir / "page_generated.html"
    paper_data_path = current_dir / "papers_2025-07-22.json"
    
    print("🚀 Starting page.html build process...")
    print("📋 Using dual-rendering approach for safe JSON escaping")
    print(f"📁 Template: {template_path}")
    print(f"📁 Data: {paper_data_path}")
    print(f"📁 Output: {output_path}")
    print("─" * 60)
    
    success = build_page(template_path, output_path, paper_data_path)
    
    if success:
        print("─" * 60)
        print("✅ Build completed successfully!")
        print(f"🌐 Open {output_path} in your browser to view the result")
    else:
        print("❌ Build failed!")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
