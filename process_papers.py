#!/usr/bin/env python3
"""
Research Papers Data Processor

This script processes the raw papers JSON file to:
1. Escape HTML characters in text fields
2. Convert LaTeX mathematical notation to MathJax format
3. Clean and validate data for frontend consumption
"""

import json
import html
import re
from typing import Dict, Any, List


class PapersProcessor:
    """Processes research papers data for web display."""
    
    def __init__(self):
        self.latex_patterns = {
            # Common mathematical symbols - using raw strings to avoid escape issues
            r'\$\\leq\$': r'\\(\leq\\)',
            r'\$\\geq\$': r'\\(\geq\\)',
            r'\$\\le\$': r'\\(\le\\)',
            r'\$\\ge\$': r'\\(\ge\\)',
            r'\$\\neq\$': r'\\(\\neq\\)',
            r'\$\\approx\$': r'\\(\\approx\\)',
            r'\$\\sim\$': r'\\(\\sim\\)',
            r'\$\\pm\$': r'\\(\\pm\\)',
            r'\$\\mp\$': r'\\(\\mp\\)',
            r'\$\\times\$': r'\\(\\times\\)',
            r'\$\\div\$': r'\\(\\div\\)',
            r'\$\\infty\$': r'\\(\\infty\\)',
            r'\$\\alpha\$': r'\\(\\alpha\\)',
            r'\$\\beta\$': r'\\(\\beta\\)',
            r'\$\\gamma\$': r'\\(\\gamma\\)',
            r'\$\\delta\$': r'\\(\\delta\\)',
            r'\$\\epsilon\$': r'\\(\\epsilon\\)',
            r'\$\\theta\$': r'\\(\\theta\\)',
            r'\$\\lambda\$': r'\\(\\lambda\\)',
            r'\$\\mu\$': r'\\(\\mu\\)',
            r'\$\\pi\$': r'\\(\\pi\\)',
            r'\$\\sigma\$': r'\\(\\sigma\\)',
            r'\$\\tau\$': r'\\(\\tau\\)',
            r'\$\\phi\$': r'\\(\\phi\\)',
            r'\$\\omega\$': r'\\(\\omega\\)',
        }
    
    def escape_html_text(self, text: str) -> str:
        """Escape HTML characters in text while preserving LaTeX."""
        if not isinstance(text, str):
            return text
        
        # First, temporarily replace LaTeX expressions to protect them
        protected_expressions = {}
        latex_inline_pattern = r'\$[^$]+\$'
        latex_block_pattern = r'\$\$[^$]+\$\$'
        
        # Protect block LaTeX first ($$...$$)
        for i, match in enumerate(re.finditer(latex_block_pattern, text)):
            placeholder = f"__LATEX_BLOCK_{i}__"
            protected_expressions[placeholder] = match.group()
            text = text.replace(match.group(), placeholder)
        
        # Protect inline LaTeX ($...$)
        for i, match in enumerate(re.finditer(latex_inline_pattern, text)):
            placeholder = f"__LATEX_INLINE_{i}__"
            protected_expressions[placeholder] = match.group()
            text = text.replace(match.group(), placeholder)
        
        # Escape HTML characters
        text = html.escape(text)
        
        # Restore protected LaTeX expressions
        for placeholder, latex_expr in protected_expressions.items():
            text = text.replace(placeholder, latex_expr)
        
        return text
    
    def convert_latex_to_mathjax(self, text: str) -> str:
        """Convert LaTeX mathematical notation to MathJax format."""
        if not isinstance(text, str):
            return text
        
        # Skip the specific pattern replacements for now to avoid regex issues
        # Just convert basic inline and block math
        
        # Convert generic inline math expressions $...$ to \(...\)
        # First protect display math $$...$$ 
        protected_displays = []
        display_pattern = r'\$\$([^$]+)\$\$'
        for match in re.finditer(display_pattern, text):
            placeholder = f"__DISPLAY_MATH_{len(protected_displays)}__"
            protected_displays.append((placeholder, f'\\[{match.group(1)}\\]'))
            text = text.replace(match.group(0), placeholder)
        
        # Now convert inline math $...$ to \(...\)
        text = re.sub(r'\$([^$]+)\$', r'\\(\1\\)', text)
        
        # Restore display math
        for placeholder, replacement in protected_displays:
            text = text.replace(placeholder, replacement)
        
        return text
    
    def process_text_field(self, text: str) -> str:
        """Process a text field with HTML escaping and LaTeX conversion."""
        if not isinstance(text, str):
            return text
        
        # First escape HTML
        text = self.escape_html_text(text)
        
        # Then convert LaTeX to MathJax
        text = self.convert_latex_to_mathjax(text)
        
        return text
    
    def process_paper(self, paper: Dict[str, Any]) -> Dict[str, Any]:
        """Process a single paper object."""
        if not isinstance(paper, dict):
            return paper
        
        # Fields that need text processing
        text_fields = [
            'title', 'abstract', 'introduction_text', 'summary',
            'novelty_justification', 'impact_justification', 
            'recommendation_justification', 'rlhf_justification',
            'weak_supervision_justification', 'diffusion_reasoning_justification',
            'distributed_training_justification', 'datasets_justification'
        ]
        
        processed_paper = paper.copy()
        
        # Process text fields
        for field in text_fields:
            if field in processed_paper and processed_paper[field]:
                processed_paper[field] = self.process_text_field(processed_paper[field])
        
        # Process author names (list of strings)
        if 'authors' in processed_paper and isinstance(processed_paper['authors'], list):
            processed_paper['authors'] = [
                self.process_text_field(author) if isinstance(author, str) else author
                for author in processed_paper['authors']
            ]
        
        # Process categories (list of strings)
        if 'categories' in processed_paper and isinstance(processed_paper['categories'], list):
            processed_paper['categories'] = [
                self.process_text_field(category) if isinstance(category, str) else category
                for category in processed_paper['categories']
            ]
        
        return processed_paper
    
    def process_papers_file(self, input_file: str, output_file: str) -> None:
        """Process the papers JSON file."""
        print(f"Loading papers from {input_file}...")
        
        try:
            with open(input_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except FileNotFoundError:
            print(f"Error: File {input_file} not found.")
            return
        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON in {input_file}: {e}")
            return
        
        if 'papers' not in data:
            print("Error: No 'papers' field found in JSON.")
            return
        
        print(f"Processing {len(data['papers'])} papers...")
        
        # Process each paper
        processed_papers = []
        for i, paper in enumerate(data['papers']):
            if isinstance(paper, dict) and len(paper) > 1:  # Skip minimal entries
                processed_paper = self.process_paper(paper)
                processed_papers.append(processed_paper)
                
                if (i + 1) % 10 == 0:
                    print(f"Processed {i + 1} papers...")
        
        # Create output data
        output_data = {
            'date': data.get('date'),
            'total_papers': len(processed_papers),
            'original_total': data.get('total_papers'),
            'papers': processed_papers,
            'processed_at': '2025-08-15T00:00:00Z'
        }
        
        print(f"Saving {len(processed_papers)} processed papers to {output_file}...")
        
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(output_data, f, indent=2, ensure_ascii=False)
            
            print(f"✅ Successfully processed papers!")
            print(f"   Input: {data.get('total_papers', 0)} papers")
            print(f"   Output: {len(processed_papers)} complete papers")
            print(f"   Saved to: {output_file}")
            
        except Exception as e:
            print(f"Error saving file: {e}")


def main():
    """Main function to run the papers processor."""
    processor = PapersProcessor()
    
    input_file = 'papers_2025-07-22.json'
    output_file = 'processed_papers.json'
    
    processor.process_papers_file(input_file, output_file)


if __name__ == "__main__":
    main()
