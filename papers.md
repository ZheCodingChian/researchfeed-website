## Paper Class Attribute Values

### Core Metadata (String/List/DateTime fields)
- `id`: String (arXiv ID like "2501.12345")
- `title`: String (paper title)
- `authors`: List[str] (list of author names)
- `categories`: List[str] (arXiv categories like ["cs.AI", "cs.CV"])
- `abstract`: String (paper abstract)
- `published_date`: datetime object

### URL Fields (Optional Strings)
- `arxiv_url`: Optional[str] (arXiv abstract page URL)
- `pdf_url`: Optional[str] (direct PDF download URL)  
- `latex_url`: Optional[str] (LaTeX source files URL)

### Status Fields (Exact Possible Values)

#### 1. `scraper_status`
- `"initial"` (default)
- `"successfully_scraped"`
- `"scraping_failed"`

#### 2. `intro_status`
- `"not_extracted"` (default)
- `"intro_successful"`
- `"no_latex_source"`
- `"no_intro_found"`
- `"extraction_failed"`

#### 3. `embedding_status`
- `"not_embedded"` (default)
- `"completed"`
- `"failed"`

#### 4. `llm_validation_status`
- `"not_validated"` (default)
- `"completed"`
- `"failed"`

#### 5. `llm_score_status`
- `"not_scored"` (default)
- `"completed"`
- `"failed"`
- `"not_relevant_enough"`

#### 6. `h_index_status`
- `"not_fetched"` (default)
- `"completed"`
- `"failed"`

### LLM Validation Relevance Fields (5 topics)
Each of these fields can have these exact values:
- `rlhf_relevance`
- `weak_supervision_relevance`
- `diffusion_reasoning_relevance`
- `distributed_training_relevance`
- `datasets_relevance`

**Possible values:**
- `"not_validated"` (default)
- `"Highly Relevant"`
- `"Moderately Relevant"`
- `"Tangentially Relevant"`
- `"Not Relevant"`

### LLM Scoring Fields

#### `novelty_score`
- `None` (default)
- `"High"`
- `"Moderate"`
- `"Low"`
- `"None"`

#### `impact_score`
- `None` (default)
- `"High"`
- `"Moderate"`
- `"Low"`
- `"Negligible"`

#### `recommendation_score`
- `None` (default)
- `"Must Read"`
- `"Should Read"`
- `"Can Skip"`
- `"Ignore"`

### Similarity Score Fields (Float values)
- `rlhf_score`: Optional[float] (0.0 to 1.0)
- `weak_supervision_score`: Optional[float] (0.0 to 1.0)
- `diffusion_reasoning_score`: Optional[float] (0.0 to 1.0)
- `distributed_training_score`: Optional[float] (0.0 to 1.0)
- `datasets_score`: Optional[float] (0.0 to 1.0)

### H-Index Related Fields
- `h_index_fetch_method`: Optional[str] (`"full_id"`, `"base_id"`, `"title_search"`)
- `total_authors`: Optional[int]
- `authors_found`: Optional[int]
- `highest_h_index`: Optional[int]
- `average_h_index`: Optional[float]
- `notable_authors_count`: Optional[int]

### Text Fields (Optional Strings)
- `introduction_text`: Optional[str]
- `intro_extraction_method`: Optional[str]
- `tex_file_name`: Optional[str]
- `summary`: Optional[str] (LLM-generated)
- `novelty_justification`: Optional[str]
- `impact_justification`: Optional[str]
- `recommendation_justification`: Optional[str]
- `semantic_scholar_url`: Optional[str]
- `highest_similarity_topic`: Optional[str]

### Justification Fields (Default: "no_justification")
- `rlhf_justification`: str
- `weak_supervision_justification`: str
- `diffusion_reasoning_justification`: str
- `distributed_training_justification`: str
- `datasets_justification`: str

### Complex Object: AuthorHIndex
The `author_h_indexes` field contains a list of `AuthorHIndex` objects with the following structure:

```python
@dataclass
class AuthorHIndex:
    name: str                    # Author's full name
    profile_url: Optional[str]   # Semantic Scholar profile URL (if found)
    h_index: Optional[int]       # Author's H-index value (if available)
```

**Example AuthorHIndex objects:**
```json
[
    {
        "name": "John Smith",
        "profile_url": "https://www.semanticscholar.org/author/123456789",
        "h_index": 42
    },
    {
        "name": "Jane Doe", 
        "profile_url": null,
        "h_index": null
    }
]
```

### Other Fields
- `errors`: List[str] (list of error messages)
- `author_h_indexes`: List[AuthorHIndex] (complex objects - see above)
- `created_at`: datetime (ISO format string when serialized)
- `updated_at`: datetime (ISO format string when serialized)
- `last_generated`: Optional[str] (YYYY-MM-DD format)

This comprehensive breakdown shows the exact possible values for each field, especially the status fields that track processing through the 9-stage pipeline.