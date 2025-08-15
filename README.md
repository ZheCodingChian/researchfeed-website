# Research Feed API Server

This Flask API server provides endpoints to access the research papers database for the Research Feed website.

## Setup Instructions

### 1. Prerequisites
- Python 3.8 or higher
- SQLite database file `cache.db` in the project root

### 2. Installation

1. **Clone/Navigate to the project directory:**
   ```powershell
   cd "C:\DevTools\GitHub\research feed website"
   ```

2. **Create and activate a virtual environment:**
   ```powershell
   python -m venv .venv
   .venv\Scripts\Activate.ps1
   ```

3. **Install dependencies:**
   ```powershell
   pip install -r requirements.txt
   ```

### 3. Running the Server

Start the Flask development server:
```powershell
python app.py
```

The server will run on `http://127.0.0.1:5000` by default.

## API Endpoints

### 1. Get Papers Count by Date

**Endpoint:** `GET /api/papers/count`

**Parameters:**
- `date` (required): Publication date in YYYY-MM-DD format

**Example Request:**
```
GET http://127.0.0.1:5000/api/papers/count?date=2025-07-09
```

**Example Response:**
```json
{
  "total_papers": 150
}
```

### 2. Get Paginated Papers by Date

**Endpoint:** `GET /api/papers`

**Parameters:**
- `date` (required): Publication date in YYYY-MM-DD format
- `page` (optional, default=1): Page number (starts from 1)
- `limit` (optional, default=10): Number of papers per page (max 100)

**Example Request:**
```
GET http://127.0.0.1:5000/api/papers?date=2025-07-09&page=1&limit=10
```

**Example Response:**
```json
{
  "papers": [
    {
      "id": "2507.06459",
      "title": "EA: An Event Autoencoder for High-Speed Vision Sensing",
      "authors": ["Riadul Islam", "Joey Mulé", "Dhandeep Challagundla"],
      "categories": ["cs.CV"],
      "abstract": "This paper presents a novel approach to...",
      "published_date": "2025-07-09",
      "arxiv_url": "https://arxiv.org/abs/2507.06459",
      "pdf_url": "https://arxiv.org/pdf/2507.06459.pdf",
      "scraper_status": "completed",
      "intro_status": "extracted",
      "embedding_status": "embedded",
      "rlhf_score": 0.85,
      "weak_supervision_score": 0.72,
      "diffusion_reasoning_score": 0.91,
      "distributed_training_score": 0.45,
      "datasets_score": 0.33,
      "llm_validation_status": "validated",
      "rlhf_relevance": "relevant",
      "weak_supervision_relevance": "not_relevant",
      "diffusion_reasoning_relevance": "highly_relevant",
      "distributed_training_relevance": "not_relevant",
      "datasets_relevance": "somewhat_relevant",
      "rlhf_justification": "The paper discusses RLHF techniques...",
      "weak_supervision_justification": "No mention of weak supervision...",
      "diffusion_reasoning_justification": "Core focus on diffusion models...",
      "distributed_training_justification": "Not applicable to this work...",
      "datasets_justification": "Limited dataset discussion...",
      "llm_score_status": "scored",
      "summary": "This work introduces a novel event autoencoder...",
      "novelty_score": "8",
      "novelty_justification": "Novel approach to event-based vision...",
      "impact_score": "7",
      "impact_justification": "Significant potential impact on computer vision...",
      "recommendation_score": "6",
      "recommendation_justification": "Worth reading for researchers in the field...",
      "h_index_status": "fetched",
      "semantic_scholar_url": "https://semanticscholar.org/paper/...",
      "total_authors": 5,
      "authors_found": 4,
      "highest_h_index": 45,
      "average_h_index": 28.5,
      "notable_authors_count": 2,
      "author_h_indexes": [
        {
          "name": "Riadul Islam",
          "h_index": 45,
          "profile_url": "https://semanticscholar.org/author/..."
        },
        {
          "name": "Joey Mulé",
          "h_index": 32,
          "profile_url": "https://semanticscholar.org/author/..."
        }
      ]
    }
  ],
  "page": 1,
  "limit": 10,
  "total_papers": 150,
  "total_pages": 15,
  "has_next": true,
  "has_prev": false
}
```

## Response Format

### Papers Array Structure

Each paper object contains the following fields (all at root level):

**Core Information:**
- `id`: arXiv paper ID
- `title`: Paper title (with LaTeX notation preserved)
- `authors`: Array of author names
- `categories`: Array of arXiv categories
- `abstract`: Paper abstract (with LaTeX notation preserved)
- `published_date`: Publication date (YYYY-MM-DD format)
- `arxiv_url`: Link to arXiv abstract page
- `pdf_url`: Direct PDF download link

**Processing Status:**
- `scraper_status`: Status of paper scraping
- `intro_status`: Status of introduction extraction
- `embedding_status`: Status of embedding generation

**Topic Relevance Scores:**
- `rlhf_score`: RLHF relevance score (0.0-1.0)
- `weak_supervision_score`: Weak supervision relevance score (0.0-1.0)
- `diffusion_reasoning_score`: Diffusion reasoning relevance score (0.0-1.0)
- `distributed_training_score`: Distributed training relevance score (0.0-1.0)
- `datasets_score`: Datasets relevance score (0.0-1.0)

**LLM Validation:**
- `llm_validation_status`: Overall validation status
- `rlhf_relevance`: RLHF relevance assessment
- `weak_supervision_relevance`: Weak supervision relevance assessment
- `diffusion_reasoning_relevance`: Diffusion reasoning relevance assessment
- `distributed_training_relevance`: Distributed training relevance assessment
- `datasets_relevance`: Datasets relevance assessment

**Justifications:**
- `rlhf_justification`: Explanation for RLHF relevance
- `weak_supervision_justification`: Explanation for weak supervision relevance
- `diffusion_reasoning_justification`: Explanation for diffusion reasoning relevance
- `distributed_training_justification`: Explanation for distributed training relevance
- `datasets_justification`: Explanation for datasets relevance

**LLM Evaluation:**
- `llm_score_status`: Status of LLM scoring
- `summary`: AI-generated paper summary
- `novelty_score`: Novelty rating
- `novelty_justification`: Explanation of novelty score
- `impact_score`: Impact rating
- `impact_justification`: Explanation of impact score
- `recommendation_score`: Recommendation rating
- `recommendation_justification`: Explanation of recommendation

**Author Analytics:**
- `h_index_status`: Status of h-index fetching
- `semantic_scholar_url`: Semantic Scholar paper URL
- `total_authors`: Total number of authors
- `authors_found`: Number of authors found in Semantic Scholar
- `highest_h_index`: Highest h-index among authors
- `average_h_index`: Average h-index of found authors
- `notable_authors_count`: Number of notable authors
- `author_h_indexes`: Array of author objects with h-index data

### Pagination Metadata

- `page`: Current page number
- `limit`: Number of papers per page
- `total_papers`: Total number of papers for the date
- `total_pages`: Total number of pages
- `has_next`: Whether there is a next page
- `has_prev`: Whether there is a previous page

## Error Responses

All endpoints return appropriate HTTP status codes:

- `200`: Success
- `400`: Bad Request (invalid parameters)
- `404`: Not Found (invalid endpoint)
- `500`: Internal Server Error (database issues)

**Error Response Format:**
```json
{
  "error": "Description of the error"
}
```

## Notes

- Papers are ordered by arXiv ID for consistent pagination
- **LaTeX notation is fully preserved** in titles, abstracts, and summaries for frontend rendering with KaTeX
- JSON special characters are automatically escaped by Flask's jsonify() function
- The server runs in debug mode for development (disable for production)
- Date filtering uses the publication date from the database
- Text content maintains original formatting including mathematical expressions like `$\alpha + \beta$`, `\textbf{bold text}`, etc.
