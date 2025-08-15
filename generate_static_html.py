#!/usr/bin/env python3
"""
Static HTML Generator for Research Papers

This script generates a complete HTML file with processed papers data embedded,
eliminating the need for client-side data fetching or a web server.
"""

import json
import html
import re
from typing import Dict, Any, List


class StaticHtmlGenerator:
    """Generates static HTML with embedded papers data."""
    
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
        
        # Convert basic inline and block math
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
    
    def load_template(self, template_file: str) -> str:
        """Load the HTML template file."""
        try:
            with open(template_file, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            print(f"Error: Template file {template_file} not found.")
            return None
        except Exception as e:
            print(f"Error reading template file: {e}")
            return None
    
    def load_papers_data(self, input_file: str) -> Dict[str, Any]:
        """Load and process papers data."""
        try:
            with open(input_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            if 'papers' not in data:
                print("Error: No 'papers' field found in JSON.")
                return None
            
            print(f"Processing {len(data['papers'])} papers...")
            
            # Process all papers (including minimal entries)
            processed_papers = []
            for i, paper in enumerate(data['papers']):
                processed_paper = self.process_paper(paper)
                processed_papers.append(processed_paper)
                
                if (i + 1) % 50 == 0:
                    print(f"Processed {i + 1} papers...")
            
            # Create processed data structure
            processed_data = {
                'date': data.get('date'),
                'total_papers': len(processed_papers),
                'original_total': data.get('total_papers'),
                'papers': processed_papers,
                'processed_at': '2025-08-15T00:00:00Z'
            }
            
            return processed_data
            
        except Exception as e:
            print(f"Error loading papers data: {e}")
            return None
    
    def inject_data_into_template(self, template: str, papers_data: Dict[str, Any]) -> str:
        """Inject processed papers data into the HTML template."""
        
        # Convert papers data to JavaScript format
        papers_json = json.dumps(papers_data, ensure_ascii=False, separators=(',', ':'))
        
        # Replace the papersData initialization
        # Find: let papersData = null;
        # Replace with: let papersData = {our_data};
        papersdata_pattern = r'let papersData\s*=\s*null\s*;'
        replacement = f'let papersData = {papers_json};'
        
        updated_template = re.sub(papersdata_pattern, replacement, template)
        
        if updated_template == template:
            print("Warning: Could not find papersData declaration in template")
            # Fallback: try to find any papersData = null pattern
            fallback_pattern = r'papersData\s*=\s*null\s*;'
            updated_template = re.sub(fallback_pattern, f'papersData = {papers_json};', template)
        
        # Replace the loadPapersData() call in DOMContentLoaded with direct setup
        # Find the DOMContentLoaded listener and replace loadPapersData() call
        dom_ready_pattern = r'(document\.addEventListener\([\'"]DOMContentLoaded[\'"],\s*function\(\)\s*\{[^}]*?)loadPapersData\(\);([^}]*\}\);)'
        
        new_dom_ready = r'\1// Data is already embedded - no need to load\n            setupEmbeddedData();\2'
        
        updated_template = re.sub(dom_ready_pattern, new_dom_ready, updated_template, flags=re.DOTALL)
        
        # Add the setupEmbeddedData function
        setup_function = '''
        // Setup page with embedded data
        function setupEmbeddedData() {
            console.log(`Loaded ${papersData.papers.length} papers from ${papersData.date}`);
            
            // Update page info
            updatePageInfo();
            
            // Render papers
            renderPapers();
            
            console.log('Static page setup complete!');
        }'''
        
        # Insert the setup function before the closing </script> tag
        script_end = '</script>'
        script_end_pos = updated_template.rfind(script_end)
        if script_end_pos != -1:
            updated_template = (updated_template[:script_end_pos] + 
                             setup_function + '\n        ' + 
                             updated_template[script_end_pos:])
        
        return updated_template
    
    def generate_static_html(self, input_file: str, template_file: str, output_file: str) -> None:
        """Generate static HTML with embedded papers data."""
        
        print(f"Loading template from {template_file}...")
        template = self.load_template(template_file)
        if not template:
            return
        
        print(f"Loading papers data from {input_file}...")
        papers_data = self.load_papers_data(input_file)
        if not papers_data:
            return
        
        print("Injecting data into template...")
        final_html = self.inject_data_into_template(template, papers_data)
        
        print(f"Saving static HTML to {output_file}...")
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(final_html)
            
            print(f"✅ Successfully generated static HTML!")
            print(f"   Papers processed: {len(papers_data['papers'])}")
            print(f"   Output file: {output_file}")
            print(f"   You can now open {output_file} directly in your browser!")
            
        except Exception as e:
            print(f"Error saving HTML file: {e}")


def main():
    """Main function to generate static HTML."""
    generator = StaticHtmlGenerator()
    
    input_file = 'papers_2025-07-22.json'
    template_file = 'page.html'
    output_file = 'papers_dashboard.html'
    
    generator.generate_static_html(input_file, template_file, output_file)


if __name__ == "__main__":
    main()
