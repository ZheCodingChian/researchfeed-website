# Topic Filter - Detailed Specification

## Overview

The Topic Filter is a sophisticated filtering system that allows users to selectively view topics within research paper cards based on their interest in specific machine learning areas. This filter operates on five core topics and provides dynamic content rendering within paper modules, while keeping all papers visible unless no topics are selected.

## Core Concepts

### 1. Filter Topics

The system operates on exactly **5 topics** in a **fixed order**:

1. **RLHF** (Reinforcement Learning from Human Feedback)
2. **Weak Supervision**
3. **Diffusion Reasoning**
4. **Distributed Training**
5. **Datasets**

**Key Properties:**
- Order is preserved across all components
- Each topic has consistent naming across mobile/desktop interfaces
- Topics map to specific paper data fields

### 2. Filter States

The filter maintains two parallel state objects:

```javascript
// Current active filters (what's actually applied)
let currentTopicFilters = {
    rlhf: true,
    weakSupervision: true,
    diffusionReasoning: true,
    distributedTraining: true,
    datasets: true
};

// Pending changes (what user has selected but not applied)
let pendingTopicFilters = {
    rlhf: true,
    weakSupervision: true,
    diffusionReasoning: true,
    distributedTraining: true,
    datasets: true
};
```

**Default State:** All topics enabled (`true`)

### 3. Module Toggle States

Each paper module maintains toggle states using CSS classes (like justification show/hide):

```html
<!-- Default state: hidden topics are not shown -->
<div class="similarity-module" data-paper-id="paper_123">
    <!-- Module content with topic visibility -->
</div>

<!-- Toggle state: hidden topics are shown -->
<div class="similarity-module show-hidden-topics" data-paper-id="paper_123">
    <!-- All topics visible regardless of filter -->
</div>

<!-- Topic relevance module -->
<div class="topic-relevance-module" data-paper-id="paper_123">
    <!-- Similar toggle state management -->
</div>

<div class="topic-relevance-module show-hidden-topics" data-paper-id="paper_123">
    <!-- All topics visible regardless of filter -->
</div>
```

**Default State:** No `show-hidden-topics` class (hidden topics remain hidden)
**Toggle State:** `show-hidden-topics` class added (all topics become visible)

## User Interface Components

### 1. Filter Dropdown Interface

**Mobile Version:**
```html
<button id="mobile-topic-btn">
    <span class="font-bold">Topic:</span> 
    <span class="font-normal">[Dynamic Text]</span> 
    <span class="text-lg">▼</span>
</button>

<div id="mobile-topic-dropdown" class="hidden">
    <!-- 5 checkboxes for each topic -->
    <input type="checkbox" id="mobile-topic-rlhf" checked>
    <label for="mobile-topic-rlhf">RLHF</label>
    <!-- ... 4 more checkboxes -->
    
    <button onclick="applyTopicFilter()">Apply Filter</button>
</div>
```

**Desktop Version:**
- Identical structure with `desktop-topic-*` IDs
- Synchronized with mobile version

### 2. Dynamic Button Text Logic

The dropdown button text updates based on selection count:

| Checked Count | Display Text |
|---------------|-------------|
| 5 (all)       | "All Selected" |
| 0 (none)      | "None Selected" |
| 1             | "1 Selected" |
| 2-4           | "{count} Selected" |

**Example:**
```javascript
// 3 topics selected
"Topic: 3 Selected ▼"

// All topics selected  
"Topic: All Selected ▼"

// No topics selected
"Topic: None Selected ▼"
```

### 3. Paper Card Modifications

Each paper card contains two modules that are affected by the topic filter:

#### A. Similarity Scores Module

**Before Filtering (All Topics Shown):**
```html
<div class="similarity-module">
    <h3>Similarity Scores</h3>
    
    <!-- Always shown if selected OR toggle is active -->
    <div class="rlhf-row">RLHF: 0.847</div>
    <div class="weak-supervision-row">Weak Supervision: 0.623</div>
    <div class="diffusion-reasoning-row">Diffusion Reasoning: 0.234</div>
    <div class="distributed-training-row">Distributed Training: 0.156</div>
    <div class="datasets-row">Datasets: 0.789</div>
    
    <!-- Show if any topics are hidden -->
    <button onclick="toggleTopicsVisibility(paperID, 'similarity')">
        Show Other Topics
    </button>
    
    <!-- Always present -->
    <button onclick="toggleSimilarityScores(this)">
        Show Normalized Scores ⇄
    </button>
</div>
```

**After Filtering (Only RLHF + Datasets Selected):**
```html
<div class="similarity-module" data-paper-id="paper_123">
    <h3>Similarity Scores</h3>
    
    <!-- Visible topics -->
    <div class="rlhf-row">RLHF: 0.847</div>
    <div class="datasets-row">Datasets: 0.789</div>
    
    <!-- Hidden topics (only shown if module has show-hidden-topics class) -->
    <div class="weak-supervision-row topic-hidden" style="display: none;">...</div>
    <div class="diffusion-reasoning-row topic-hidden" style="display: none;">...</div>
    <div class="distributed-training-row topic-hidden" style="display: none;">...</div>
    
    <!-- Toggle button appears when some topics are hidden -->
    <button onclick="toggleTopicsVisibility(this)">
        Show Other Topics
    </button>
    
    <!-- Normalized scores button -->
    <button onclick="toggleSimilarityScores(this)">
        Show Normalized Scores ⇄
    </button>
</div>
```

**After Toggle (show-hidden-topics class added):**
```html
<div class="similarity-module show-hidden-topics" data-paper-id="paper_123">
    <!-- Now ALL topics are visible regardless of filter -->
    <div class="rlhf-row">RLHF: 0.847</div>
    <div class="weak-supervision-row">Weak Supervision: 0.623</div>  <!-- Now visible -->
    <div class="diffusion-reasoning-row">Diffusion Reasoning: 0.234</div>  <!-- Now visible -->
    <div class="distributed-training-row">Distributed Training: 0.156</div>  <!-- Now visible -->
    <div class="datasets-row">Datasets: 0.789</div>
    
    <!-- Toggle button text changes -->
    <button onclick="toggleTopicsVisibility(this)">
        Hide Other Topics
    </button>
</div>
```

#### B. Topic Relevance Module

Similar structure but shows relevance scores and justifications:

**Components:**
- Topic relevance indicators (High/Medium/Low/None)
- Topic-specific justification text
- Toggle button for hidden topics

## Filtering Logic

### 1. Paper-Level Filtering

The Topic Filter operates **ONLY** on topic visibility within papers, **NOT** on paper inclusion/exclusion:

```javascript
function passesTopicFilter(paper) {
    // Topic filter NEVER excludes papers
    // The only exception: if NO topics are selected, show NO papers
    const selectedTopics = Object.values(currentTopicFilters);
    const hasAnyTopicSelected = selectedTopics.some(Boolean);
    
    // If no topics selected, hide all papers (special case)
    if (!hasAnyTopicSelected) return false;
    
    // Otherwise, ALL papers pass the filter
    // Topic filtering only affects what's SHOWN WITHIN each paper
    return true;
}
```

**Key Principles:**
- **No content checks**: Papers are never excluded based on whether they have "meaningful" topic content
- **Simple rule**: If no topics selected → 0 papers shown. Otherwise → all papers shown
- **Topic visibility**: Filtering only controls which topics are visible within each paper's modules

### 2. Topic-Level Rendering

Within each displayed paper, topics are rendered conditionally based on filter + toggle state:

```javascript
function shouldShowTopic(topicKey, moduleElement) {
    // Always show if topic is selected in filter
    if (currentTopicFilters[topicKey]) return true;
    
    // Show if module has toggle override (show-hidden-topics class)
    if (moduleElement.classList.contains('show-hidden-topics')) return true;
    
    // Otherwise hide
    return false;
}

// Rendering logic in template
${shouldShowTopic('rlhf', moduleElement) ? `
    <div class="rlhf-row">
        <!-- RLHF content -->
    </div>
` : ''}
```

## State Management

### 1. URL Persistence

Filter states are persisted in URL parameters:

```
?topic_rlhf=true&topic_weak=false&topic_diffusion=true&topic_distributed=false&topic_datasets=true
```

**Parameter Mapping:**
- `topic_rlhf` → `currentTopicFilters.rlhf`
- `topic_weak` → `currentTopicFilters.weakSupervision`
- `topic_diffusion` → `currentTopicFilters.diffusionReasoning`
- `topic_distributed` → `currentTopicFilters.distributedTraining`
- `topic_datasets` → `currentTopicFilters.datasets`

### 2. Checkbox Synchronization

Mobile and desktop checkboxes are kept in sync:

```javascript
// When mobile checkbox changes
document.getElementById('mobile-topic-rlhf').addEventListener('change', () => {
    // Sync to desktop
    document.getElementById('desktop-topic-rlhf').checked = 
        document.getElementById('mobile-topic-rlhf').checked;
    
    // Update pending state
    updatePendingTopicFilters();
    updateTopicButtonText();
});
```

### 3. Module Toggle State Management

Module toggle states use CSS classes (like justification toggles):

```javascript
function toggleTopicsVisibility(buttonElement) {
    // Find the parent module
    const module = buttonElement.closest('.similarity-module, .topic-relevance-module');
    
    // Toggle the CSS class
    if (module.classList.contains('show-hidden-topics')) {
        module.classList.remove('show-hidden-topics');
        buttonElement.textContent = 'Show Other Topics';
    } else {
        module.classList.add('show-hidden-topics');
        buttonElement.textContent = 'Hide Other Topics';
    }
    
    // Re-render topic visibility in this module
    updateTopicVisibilityInModule(module);
}
```

## User Interaction Flows

### 1. Basic Filtering Flow

1. **User opens dropdown** → `toggleMobileTopicDropdown()` / `toggleDesktopTopicDropdown()`
2. **User changes checkboxes** → Event listeners update `pendingTopicFilters` and button text
3. **User clicks "Apply Filter"** → `applyTopicFilter()` is called:
   - Copy `pendingTopicFilters` to `currentTopicFilters`
   - Remove all `show-hidden-topics` classes from modules (reset toggle states)
   - Update URL parameters
   - Close dropdowns
   - Run `applyFiltersAndSort()` to re-filter papers (almost always shows all papers)
   - Call `displayCurrentPage()` to re-render with new topic visibility

### 2. Topic Toggle Flow

1. **User sees paper with hidden topics** → "Show Other Topics" button is visible
2. **User clicks toggle button** → `toggleTopicsVisibility(buttonElement)` is called:
   - Add/remove `show-hidden-topics` class on the specific module
   - Update button text to "Hide Other Topics" / "Show Other Topics"
   - Update topic visibility in that module only (no full re-render needed)

### 3. Page Navigation Flow

1. **User navigates to different page** → `displayCurrentPage()` is called
2. **New papers are rendered** → All new papers start without `show-hidden-topics` classes
3. **Previous toggle states are lost** → Each page starts fresh (like justification toggles)

## Data Requirements

### 1. Paper Data Structure

Each paper must contain the following fields for the topic filter to work:

```javascript
{
    "id": "2401.12345",
    "title": "Paper Title",
    
    // Similarity scores (required)
    "rlhf_score": 0.847,
    "weak_supervision_score": 0.623,
    "diffusion_reasoning_score": 0.234,
    "distributed_training_score": 0.156,
    "datasets_score": 0.789,
    
    // Topic relevance indicators (required)
    "rlhf_relevance": "High",           // High/Medium/Low/None
    "weak_supervision_relevance": "Medium",
    "diffusion_reasoning_relevance": "Low",
    "distributed_training_relevance": "None", 
    "datasets_relevance": "High",
    
    // Justification text (required)
    "rlhf_justification": "This paper presents a novel approach to RLHF...",
    "weak_supervision_justification": "The method shows connections to weak supervision through...",
    "diffusion_reasoning_justification": "Limited relevance to diffusion reasoning...",
    "distributed_training_justification": "No significant distributed training components.",
    "datasets_justification": "Introduces a new benchmark dataset for evaluation..."
}
```

### 2. Topic Content Detection

**REMOVED SECTION**: The Topic Filter does **NOT** check for meaningful content. All papers are shown regardless of their topic data quality. The filter only controls topic visibility within paper modules.

## Normalized Score Recalculation

### 1. Dynamic Score Normalization

When topics are filtered, similarity scores need to be recalculated to maintain proper proportional representation:

```javascript
function recalculateNormalizedScores(moduleElement) {
    const paperId = moduleElement.dataset.paperId;
    const paper = findPaperById(paperId);
    const showHidden = moduleElement.classList.contains('show-hidden-topics');
    
    // Determine which topics are visible
    const visibleTopics = [];
    if (currentTopicFilters.rlhf || showHidden) visibleTopics.push('rlhf');
    if (currentTopicFilters.weakSupervision || showHidden) visibleTopics.push('weak_supervision');
    if (currentTopicFilters.diffusionReasoning || showHidden) visibleTopics.push('diffusion_reasoning');
    if (currentTopicFilters.distributedTraining || showHidden) visibleTopics.push('distributed_training');
    if (currentTopicFilters.datasets || showHidden) visibleTopics.push('datasets');
    
    // Get scores for visible topics only
    const visibleScores = visibleTopics.map(topic => paper[`${topic}_score`]);
    const maxVisible = Math.max(...visibleScores);
    
    // Recalculate progress bar widths
    visibleTopics.forEach(topic => {
        const score = paper[`${topic}_score`];
        const normalizedWidth = (score / maxVisible) * 100;
        
        updateProgressBar(paperId, topic, normalizedWidth);
    });
}
```

### 2. Progress Bar Updates

Progress bars in the similarity module dynamically adjust based on visible topics:

- **All topics visible**: Bars show relative proportions across all 5 topics
- **Filtered topics**: Bars recalculate to show proportions among visible topics only
- **Toggle states**: Bars update when topics are shown/hidden via toggle buttons

## CSS Classes and Styling

### 1. Filter-Specific Classes

```css
/* Module toggle states (like justification toggles) */
.similarity-module.show-hidden-topics .topic-hidden {
    display: block !important;
}

.topic-relevance-module.show-hidden-topics .topic-hidden {
    display: block !important;
}

/* Hidden topic indicators */
.topic-hidden {
    /* Topics hidden by filter but can be shown by toggle */
}

/* Button states */
.bg-neutral-500 {
    /* Default dropdown button */
}

.bg-neutral-600 {
    /* Active/open dropdown button */
    /* Toggle button for "Show Other Topics" */
}
```

### 2. Visibility States

Topics use inline `style="display: none;"` for hidden topics, with CSS override via module classes:

```html
<!-- Filtered out topic -->
<div class="topic-row topic-hidden" style="display: none;">
    <!-- Hidden by default, shown if module has show-hidden-topics class -->
</div>

<!-- Visible topic -->
<div class="topic-row">
    <!-- Always visible -->
</div>

<!-- Module with toggle active -->
<div class="similarity-module show-hidden-topics">
    <!-- Now ALL topic-hidden elements become visible via CSS override -->
    <div class="topic-row topic-hidden" style="display: none;">
        <!-- This is now visible due to CSS: .show-hidden-topics .topic-hidden { display: block !important; } -->
    </div>
</div>
```

## Performance Considerations

### 1. Rendering Strategy

- **CSS Hidden Approach**: Uses `display: none` instead of DOM removal
- **Pros**: Faster toggling, preserves state, simpler re-rendering
- **Cons**: Larger DOM size, hidden content still parsed

### 2. Re-rendering Optimization

```javascript
function updateTopicVisibilityInModule(moduleElement) {
    // Update topic visibility without full paper re-render
    // Only toggle display states based on current filter + module toggle class
    
    const showHidden = moduleElement.classList.contains('show-hidden-topics');
    
    // Update each topic's visibility
    const topicElements = moduleElement.querySelectorAll('[data-topic]');
    topicElements.forEach(element => {
        const topic = element.dataset.topic;
        const shouldShow = currentTopicFilters[topic] || showHidden;
        
        if (shouldShow) {
            element.style.display = '';
            element.classList.remove('topic-hidden');
        } else {
            element.style.display = 'none';
            element.classList.add('topic-hidden');
        }
    });
    
    // Update toggle button text
    const toggleButton = moduleElement.querySelector('[onclick*="toggleTopicsVisibility"]');
    if (toggleButton) {
        toggleButton.textContent = showHidden ? 'Hide Other Topics' : 'Show Other Topics';
    }
}
```

### 3. State Management Efficiency

- Toggle states stored in CSS classes (like justification toggles)
- Filter states debounced during checkbox changes
- URL updates batched with filter application
- No JavaScript state objects for toggle management

## Integration Points

### 1. Existing Filter System

The topic filter integrates with the existing filter pipeline:

```javascript
function applyFiltersAndSort() {
    // Apply all filters in sequence
    filteredSortedPapers = allPapers
        .filter(paper => passesHIndexFilter(paper))
        .filter(paper => passesScoringFilter(paper))
        .filter(paper => passesRecommendationFilter(paper))
        .filter(paper => passesNoveltyFilter(paper))
        .filter(paper => passesImpactFilter(paper))
        .filter(paper => passesTopicFilter(paper));  // ← New filter (usually passes all papers)
    
    sortPapers(currentSort);
    // ... pagination and display
}
```

**Note**: The topic filter almost always returns `true` for all papers, except when no topics are selected.

### 2. Dropdown Management

// Shares dropdown infrastructure with other filters:

```javascript
// Dropdown positioning and behavior
function setDropdownDirection(button, dropdown) {
    // Shared with H-Index, Scoring, Recommendation, Novelty, Impact
}

// Disabled state management
function updateAdvancedFiltersDisabledState() {
    // Includes topic filter in disabled state logic
}
```

### 3. URL Parameter Management

Extends existing URL parameter system:

```javascript
// Existing parameters: sort, hindex_*, scoring_*, recommendation_*, novelty_*, impact_*
// New parameters: topic_rlhf, topic_weak, topic_diffusion, topic_distributed, topic_datasets
```

## Error Handling

### 1. Missing Data Handling

```javascript
function safeGetScore(paper, topicKey) {
    const score = paper[`${topicKey}_score`];
    return (score !== undefined && score !== null) ? score : 0.0;
}

function safeGetRelevance(paper, topicKey) {
    const relevance = paper[`${topicKey}_relevance`];
    return relevance || "None";
}

function safeGetJustification(paper, topicKey) {
    const justification = paper[`${topicKey}_justification`];
    return justification || "No justification available.";
}
```

### 2. State Consistency

```javascript
function ensureConsistentState() {
    // Validate filter states
    Object.keys(currentTopicFilters).forEach(key => {
        if (typeof currentTopicFilters[key] !== 'boolean') {
            currentTopicFilters[key] = true; // Default to enabled
        }
    });
    
    // Clean up orphaned toggle states (CSS classes are self-managing)
    // No manual cleanup needed for CSS-based toggle states
}
```

## Testing Scenarios

### 1. Basic Functionality Tests

1. **All topics selected**: All papers visible, all topics shown in cards
2. **No topics selected**: No papers visible
3. **Single topic selected**: Only papers with that topic visible, only that topic shown
4. **Multiple topics selected**: Papers with any selected topic visible, only selected topics shown

### 2. Toggle Interaction Tests

1. **Show other topics**: Hidden topics become visible for specific paper
2. **Hide other topics**: Previously shown topics become hidden again
3. **Multiple papers**: Toggle states independent between papers
4. **Page navigation**: Toggle states reset for new papers

### 3. State Persistence Tests

1. **URL updates**: Filter states reflected in URL parameters
2. **Page reload**: Filter states restored from URL
3. **Browser navigation**: Back/forward buttons work correctly
4. **Bookmark sharing**: URLs with filter states work for other users

### 4. Integration Tests

1. **Multiple filters**: Topic filter works with H-Index, Scoring, Recommendation, Novelty, Impact
2. **Sorting**: Sorted order maintained when topic filter applied
3. **Pagination**: Page navigation works with filtered results (almost always all papers)
4. **Mobile/desktop sync**: Checkbox changes synchronized across interfaces

## Future Enhancements

### 1. Advanced Features

- **Custom topic selection**: Allow users to define their own topics
- **Topic weighting**: Assign importance weights to different topics
- **Relevance scoring**: Show quantitative relevance scores instead of High/Medium/Low
- **Topic clustering**: Group related topics together

### 2. Performance Improvements

- **Virtual scrolling**: Handle large numbers of papers more efficiently
- **Lazy loading**: Load topic data on demand
- **State compression**: More efficient URL parameter encoding
- **Caching**: Cache filtered results for faster navigation

### 3. User Experience

- **Topic previews**: Show topic content before applying filter
- **Quick filters**: One-click presets for common topic combinations
- **Topic explanations**: Help text explaining what each topic covers
- **Visual indicators**: Better visual feedback for filtered content

## Implementation Checklist

### Phase 1: Core Infrastructure
- [ ] HTML filter dropdown structure (mobile + desktop)
- [ ] JavaScript state management variables (`currentTopicFilters`, `pendingTopicFilters`)
- [ ] Basic filter application logic (`passesTopicFilter()` - simple rule)
- [ ] URL parameter persistence (`topic_*` parameters)
- [ ] Checkbox synchronization

### Phase 2: Content Rendering
- [ ] Conditional topic rendering in similarity module
- [ ] Conditional topic rendering in topic relevance module  
- [ ] Dynamic justification text filtering
- [ ] Progress bar recalculation for visible topics

### Phase 3: Toggle Functionality
- [ ] CSS class-based toggle state management (like justification toggles)
- [ ] "Show/Hide Other Topics" buttons
- [ ] Module-level topic visibility updates
- [ ] Toggle state consistency across page navigation

### Phase 4: Integration & Polish
- [ ] Integration with existing filter pipeline (mostly pass-through)
- [ ] Error handling and edge cases
- [ ] Performance optimization (CSS-based approach)
- [ ] User interface polish
- [ ] Comprehensive testing

This specification provides the complete blueprint for implementing the topic-based relevance filter system with all the detailed behaviors, edge cases, and integration requirements.
