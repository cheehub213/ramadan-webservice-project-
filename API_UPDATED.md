# API Update Summary - Bilingual Support & Explanations

## Overview
The Ramadan Decision-Making API has been significantly enhanced with:
1. **Arabic Language Support** - Accept and respond in Arabic
2. **Bilingual Responses** - English, Arabic, or both simultaneously
3. **Intelligent Explanations** - Why each verse/hadith was selected
4. **Relevance Scoring** - How relevant each result is (0-1 scale)
5. **Matched Keywords** - Which keywords triggered each result

---

## Files Modified

### 1. **app/schemas/request.py**
**Changes:**
- Changed `language` parameter to `response_language`
- Added support for "bilingual" option (returns both EN and AR)
- Now accepts: "en", "ar", or "bilingual"

**New Structure:**
```python
class SearchRequest(BaseModel):
    prompt: str                    # Accepts English or Arabic
    response_language: str = "bilingual"  # "en", "ar", or "bilingual"
    include_hadith: bool = True
    include_quran: bool = True
```

### 2. **app/schemas/quran.py**
**Changes:**
- Added `explanation_english` and `explanation_arabic` fields
- Added `relevance_score` field (0-1)
- Added `matched_keywords` field (list of matching terms)
- Created new `BilingualQuranResponse` class
- Updated `HadithResponse` with bilingual explanations

### 3. **app/services/deepseek_service.py**
**Changes:**
- Added `_detect_language()` method - detects if prompt is Arabic or English
- Updated `analyze_prompt()` - includes language detection and returns `prompt_language`
- Added `generate_explanation()` method - creates bilingual explanations for why a specific verse/hadith was chosen
- Returns both English and Arabic explanations

**New Methods:**
```python
async def generate_explanation(
    self,
    user_prompt: str,
    verse_or_hadith_text: str,
    item_type: str = "verse"
) -> Dict[str, str]:
    # Returns: {"explanation_english": "...", "explanation_arabic": "..."}
```

### 4. **app/services/matching_service.py**
**Changes:**
- Updated `match_quran_verses()` - supports "both" language option
- Added `get_matched_keywords()` - returns which keywords actually matched
- Added `calculate_relevance_score()` - calculates 0-1 relevance score
- Updated `rank_by_relevance()` - attaches relevance_score and matched_keywords to results

**New Methods:**
```python
@staticmethod
def get_matched_keywords(text: str, keywords: List[str]) -> List[str]:
    # Returns keywords that matched in the text

@staticmethod
def calculate_relevance_score(
    text: str,
    keywords: List[str],
    topic_matched: bool = False
) -> float:
    # Returns score between 0.0 and 1.0
```

### 5. **app/routes/search.py**
**Changes:**
- Updated POST `/api/v1/search/answer` endpoint with:
  - Language detection
  - Explanation generation for each result
  - Bilingual response support
  - Relevance scoring
  - Matched keywords tracking
- Updated GET `/api/v1/search/quran` with bilingual support
- Updated GET `/api/v1/search/hadith` with bilingual support

**Flow:**
1. Analyze prompt (detects language, extracts topics/keywords)
2. Search database (bilingual if requested)
3. Rank by relevance
4. Generate explanations (bilingual)
5. Return comprehensive response with all metadata

---

## New Request/Response Examples

### Request 1: English Prompt → Bilingual
```json
{
  "prompt": "I'm feeling tired during Ramadan fasting",
  "response_language": "bilingual"
}
```

### Request 2: Arabic Prompt → Arabic Response
```json
{
  "prompt": "أشعر بالإرهاق أثناء الصيام في رمضان",
  "response_language": "ar"
}
```

### Request 3: Bilingual Search
```
GET /api/v1/search/quran?keywords=patience&response_language=bilingual&limit=5
```

---

## Response Structure Enhancements

### Before
```json
{
  "results": {
    "quran_verses": [{
      "surah": "Surah Name",
      "ayah_number": 5,
      "text": "Verse text"
    }]
  }
}
```

### After
```json
{
  "prompt_language": "en",
  "response_language": "bilingual",
  "analysis": {
    "topics": ["patience", "guidance"],
    "keywords": ["struggling", "help"],
    "emotion": "distressed",
    "summary": "User seeking guidance on handling difficulties"
  },
  "results": {
    "quran_verses": [{
      "surah_number": 2,
      "surah_name": "Al-Baqarah",
      "ayah_number": 286,
      "ayah_text_english": "Allah does not burden a soul beyond that it can bear...",
      "ayah_text_arabic": "لا يكلف الله نفسا إلا وسعها...",
      "explanation_english": "This verse directly addresses your feeling of being overwhelmed...",
      "explanation_arabic": "تتناول هذه الآية مباشرة شعورك بالإرهاق...",
      "relevance_score": 0.92,
      "matched_keywords": ["burden", "bear"]
    }]
  }
}
```

---

## Testing

Run the comprehensive test suite:
```bash
python test_bilingual_api.py
```

Tests cover:
1. English prompt → Bilingual response
2. Arabic prompt → Arabic response
3. Arabic prompt → English response
4. Family conflict (Arabic) → Bilingual
5. Grief (English) → English
6. Direct Quran search (Bilingual)
7. Direct Hadith search (Bilingual)
8. Work/Financial concern → Bilingual
9. Moral dilemma (Arabic) → Bilingual
10. Social pressure → Bilingual

---

## Key Features Explained

### 1. Language Detection
- Automatically detects if prompt is English or Arabic
- Uses Unicode character range checking
- No manual language selection needed

### 2. Bilingual Responses
- `response_language: "bilingual"` returns BOTH languages
- Each verse/hadith includes English AND Arabic text
- Each includes explanations in both languages
- Ideal for bilingual users or complete understanding

### 3. Intelligent Explanations
- Uses Deepseek AI to generate context-aware explanations
- Explains WHY a specific verse/hadith matches the user's concern
- Helps users understand the connection
- Provided in both English and Arabic

### 4. Relevance Scoring
- Scores from 0.0 (not relevant) to 1.0 (highly relevant)
- Based on keyword matching and frequency
- Boosts score if topic matched
- Helps users prioritize

### 5. Matched Keywords
- Shows which specific keywords from analysis matched
- Provides transparency on matching logic
- Helps users understand why result was selected

---

## Backward Compatibility

### Deprecated Parameter
- `language: "en"` → Use `response_language: "en"` instead

### Old Requests Still Work
```json
{
  "prompt": "...",
  "language": "en"  // Will work but "response_language" is recommended
}
```

### Recommended Updates
```json
{
  "prompt": "...",
  "response_language": "bilingual"  // New parameter
}
```

---

## API Endpoint Documentation

### POST `/api/v1/search/answer`
- **Purpose**: Main intelligent search with AI analysis
- **New Features**: Bilingual support, explanations, scoring
- **Response Language Options**: "en", "ar", "bilingual"

### GET `/api/v1/search/quran`
- **Parameters**: 
  - `keywords` (required)
  - `response_language` (optional: "en", "ar", "bilingual")
  - `limit` (optional: default 5)
- **New Features**: Bilingual responses, relevance scoring

### GET `/api/v1/search/hadith`
- **Parameters**:
  - `keywords` (required)
  - `response_language` (optional: "en", "ar", "bilingual")
  - `limit` (optional: default 5)
- **New Features**: Bilingual responses, relevance scoring

---

## Performance Considerations

- **Explanation Generation**: Async (uses Deepseek API)
- **Search Speed**: <1 second for typical queries
- **Relevance Calculation**: O(n) where n = keyword count
- **Language Detection**: Immediate (no API call)

---

## Configuration

No additional configuration needed. All features work with existing `.env`:
```
DATABASE_URL=sqlite:///./ramadan.db
DEEPSEEK_API_KEY=your_api_key_here
```

---

## Future Enhancement Ideas

1. **Caching** - Cache explanations for frequently asked questions
2. **User Preferences** - Remember language preference per user
3. **More Languages** - Add support for Urdu, Malay, Indonesian
4. **Topic Refinement** - More granular topic categorization
5. **User Feedback** - Track which explanations were helpful
6. **Historical Tracking** - Save query history for analytics

---

## Documentation Files

- **BILINGUAL_FEATURES.md** - Complete feature guide with examples
- **example_responses.json** - Sample request/response pairs
- **test_bilingual_api.py** - 10 comprehensive test cases
- **API_UPDATED.md** - This file

---

## Quick Start

### Via cURL
```bash
curl -X POST "http://localhost:8001/api/v1/search/answer" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "أشعر بالضعف أثناء الصيام",
    "response_language": "bilingual"
  }'
```

### Via Python
```python
import requests

response = requests.post(
    "http://localhost:8001/api/v1/search/answer",
    json={
        "prompt": "I struggle with patience",
        "response_language": "bilingual"
    }
)
print(response.json())
```

### Via Swagger UI
1. Visit http://localhost:8001/docs
2. Click POST `/api/v1/search/answer`
3. Try it out with bilingual prompts

---

## Support

For issues or questions, check:
- `BILINGUAL_FEATURES.md` for feature documentation
- `example_responses.json` for response examples
- `test_bilingual_api.py` for test patterns
