# Research Feed Website - Build System Documentation

## Overview

This project implements a **dual-rendering approach** for generating HTML pages with complex paper data containing LaTeX notations, quotes, and special characters. The solution is based on the methodology described in `build.md` and solves the critical problem of safely embedding JSON data with complex content into HTML/JavaScript.

## The Problem

When embedding research paper data into HTML/JavaScript, we face several challenges:
- **Quote Escaping**: Papers contain various types of quotation marks that break JSON
- **LaTeX Escaping**: Mathematical notations with backslashes and special symbols
- **Unicode Handling**: International characters, mathematical symbols, accents
- **Security**: Preventing XSS attacks while maintaining functionality

## The Solution: Dual-Rendering Approach

### Core Concept

Instead of trying to manually escape all edge cases, we use a **two-pronged approach**:

1. **Template-Side Rendering (Server-Side)**: Static HTML structure with HTML-escaped content
2. **JavaScript-Side Data (Client-Side)**: JSON data for dynamic functionality using safe JSON serialization

### The Critical Line

```javascript
// THE CRITICAL ESCAPING SOLUTION
window.paperData = {{ papers_json_data }};
```

Where `papers_json_data` is generated using:

```python
@staticmethod  
def tojson_safe(data):
    """
    Equivalent to Jinja2's |tojson|safe filter
    Handles:
    - Quote escaping: " becomes \"
    - LaTeX escaping: backslashes, special characters  
    - Unicode escaping: mathematical symbols, accents
    - JSON compliance: ensures valid JSON structure
    """
    return json.dumps(data, ensure_ascii=False, separators=(',', ':'))
```

## File Structure

```
research-feed-website/
├── build_page.py              # Build script with dual-rendering logic
├── page_template.html         # Template with placeholders
├── page_generated.html        # Generated output
├── papers_2025-07-22.json     # Source data
└── build_system_docs.md       # This documentation
```

## Usage

### Basic Build Process

```bash
python build_page.py
```

### What Happens

1. **Load Data**: Reads JSON paper data from `papers_2025-07-22.json`
2. **Prepare Template Data**: 
   - `papers_list`: Full objects for template rendering
   - `papers_json`: JSON-serializable data for JavaScript
   - `papers_json_escaped`: Safely escaped JSON string
3. **Render Template**: Substitutes placeholders with data
4. **Generate Output**: Creates `page_generated.html`

## Examples of Escaping in Action

### Input (Paper Title)
```
Understanding "Deep Learning" & LaTeX: $\alpha + \beta = \gamma$
```

### Server-Side (HTML Template)
```html
<h5 class="paper-title">
    Understanding "Deep Learning" &amp; LaTeX: $\alpha + \beta = \gamma$
</h5>
```

### Client-Side (JSON Data)
```javascript
window.paperData = [{
    "title": "Understanding \"Deep Learning\" & LaTeX: $\\alpha + \\beta = \\gamma$"
}];
```

## Benefits

✅ **No Manual Escaping Required**: Built-in JSON serialization handles edge cases  
✅ **LaTeX-Safe**: Mathematical notations properly escaped  
✅ **Quote-Safe**: All quotation marks handled correctly  
✅ **Unicode-Safe**: International characters work correctly  
✅ **Performance**: Single JSON serialization, cached client-side  
✅ **Maintainable**: Clear separation between static and dynamic content  
✅ **Secure**: Prevents XSS while maintaining functionality  

## Customization

### Adding New Fields

1. Update `prepare_template_data()` in `build_page.py`:
```python
paper_dict = {
    'new_field': paper.get('new_field', 'default_value'),
    # ... existing fields
}
```

2. Use in JavaScript:
```javascript
function createPaperCard(paper) {
    return `<div>${paper.new_field}</div>`;
}
```

### Template Variables

Add new template variables in `build_page()`:
```python
template_vars = {
    'custom_variable': 'custom_value',
    # ... existing variables
}
```

Use in template:
```html
<span>{{ custom_variable }}</span>
```

## Advanced Features

### Template Engine

The simple template engine supports:
- Variable substitution: `{{ variable_name }}`
- Conditional escaping: Variables ending in `_json_data` aren't HTML-escaped
- HTML escaping: Regular variables are automatically escaped

### JSON Serialization Options

```python
# Current settings
json.dumps(data, ensure_ascii=False, separators=(',', ':'))

# Options:
# ensure_ascii=False: Allows Unicode characters
# separators=(',', ':'): Compact JSON (no extra spaces)
# indent=None: Compact output
```

## Troubleshooting

### JSON Not Loading
- Check browser console for JavaScript errors
- Verify `window.paperData` is defined
- Ensure JSON is valid (use JSON validator)

### Template Variables Not Substituting
- Check placeholder format: `{{ variable_name }}`
- Ensure variable exists in `template_vars`
- Verify template file exists and is readable

### Escaping Issues
- Ensure using `tojson_safe()` for JSON data
- Check if new content needs special handling
- Verify proper separation of template vs. JSON variables

## Performance Considerations

- **Large Datasets**: Consider pagination for 1000+ papers
- **JSON Size**: Monitor total JSON payload size
- **Caching**: Generated HTML can be cached/served statically
- **Loading**: Papers render progressively via JavaScript

## Security Notes

- HTML template variables are automatically escaped
- JSON data uses safe serialization
- No user input is directly embedded
- External links use `rel="noopener noreferrer"`

This dual-rendering approach provides a robust, maintainable solution for complex research paper data while ensuring security and performance.
