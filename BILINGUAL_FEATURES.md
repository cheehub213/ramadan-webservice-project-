# Bilingual Ramadan API - Features Guide

## New Features Overview

### 1. **Arabic Language Support** 🌍
- API now accepts prompts in **English AND Arabic**
- Automatically detects prompt language
- Supports responses in English, Arabic, or **both languages simultaneously (bilingual)**

### 2. **Explanation Generation** 📚
- Each Quran verse and Hadith now includes explanations
- Explanations explain **WHY** that specific verse/hadith was selected
- Explanations provided in both English and Arabic
- Helps users understand the connection between their problem and the guidance

### 3. **Relevance Scoring** 📊
- Each result includes a relevance score (0.0 - 1.0)
- Shows how relevant the verse/hadith is to the user's specific concern
- Helps users prioritize which guidance to focus on

### 4. **Matched Keywords Tracking** 🔍
- Shows which keywords from the analysis matched in each verse/hadith
- Provides transparency on why a result was selected
- Helps users understand the matching logic

---

## API Endpoint Updates

### POST `/api/v1/search/answer`

**Main Intelligence Endpoint**

#### Request Schema
```json
{
  "prompt": "Your problem or question (English or Arabic)",
  "response_language": "en|ar|bilingual",
  "include_hadith": true,
  "include_quran": true
}
```

#### Response Schema
```json
{
  "status": "success",
  "user_prompt": "Original prompt",
  "prompt_language": "en or ar",
  "response_language": "selected language",
  "analysis": {
    "topics": ["topic1", "topic2"],
    "keywords": ["keyword1", "keyword2"],
    "emotion": "emotional state",
    "summary": "Brief analysis summary"
  },
  "results": {
    "quran_verses": [
      {
        "surah_number": 1,
        "surah_name": "Surah Name",
        "ayah_number": 5,
        "ayah_text_english": "English verse text",
        "ayah_text_arabic": "النص العربي للآية",
        "explanation_english": "Why this verse addresses your concern",
        "explanation_arabic": "شرح لماذا تعالج هذه الآية مخاوفك",
        "relevance_score": 0.85,
        "matched_keywords": ["keyword1", "keyword2"]
      }
    ],
    "hadiths": [
      {
        "hadith_number": "1234",
        "narrator": "Prophet's Companion",
        "source": "Sahih Bukhari",
        "hadith_text_english": "English hadith text",
        "hadith_text_arabic": "نص الحديث العربي",
        "explanation_english": "Why this hadith is relevant",
        "explanation_arabic": "شرح لماذا يكون هذا الحديث ذا صلة",
        "relevance_score": 0.82,
        "matched_keywords": ["keyword1"]
      }
    ]
  }
}
```

### GET `/api/v1/search/quran`

**Direct Quran Search with Bilingual Support**

#### Parameters
```
keywords: "keyword1,keyword2"        (comma-separated)
response_language: "en|ar|bilingual" (default: "en")
limit: 5                             (maximum results)
```

#### Response
Returns verses with relevance scores, matched keywords, and bilingual text

### GET `/api/v1/search/hadith`

**Direct Hadith Search with Bilingual Support**

#### Parameters
```
keywords: "keyword1,keyword2"        (comma-separated)
response_language: "en|ar|bilingual" (default: "bilingual")
limit: 5                             (maximum results)
```

#### Response
Returns hadiths with relevance scores, matched keywords, and bilingual text

---

## Test Cases

### Test 1: English Prompt → Bilingual Response
```json
{
  "prompt": "I'm feeling very tired and weak during fasting in Ramadan",
  "response_language": "bilingual"
}
```

### Test 2: Arabic Prompt → Arabic Response
```json
{
  "prompt": "أشعر بالضعف والإرهاق أثناء الصيام في رمضان",
  "response_language": "ar"
}
```

### Test 3: Arabic Prompt → English Response
```json
{
  "prompt": "أنا أعاني من الشكوك في إيماني",
  "response_language": "en"
}
```

### Test 4: Bilingual Search
```
GET /api/v1/search/quran?keywords=patience,strength&response_language=bilingual&limit=3
```

---

## How Explanations Work

When you submit a prompt, the system:

1. **Analyzes** your prompt with Deepseek AI (detects language, extracts emotion, topics)
2. **Searches** the database for relevant verses and hadiths
3. **Ranks** results by relevance score
4. **Explains** why each result was selected using Deepseek AI
5. **Returns** complete guidance with explanations in your preferred language(s)

### Example Flow

**User Input:**
```
"I lost my job during Ramadan and I'm worried about providing for my family"
```

**Analysis Output:**
- Topics: `["financial hardship", "family responsibility", "trust in God"]`
- Keywords: `["job", "family", "worried", "provide"]`
- Emotion: `"anxious"`

**Matching & Explanation:**
For each verse/hadith found:
- Explains connection to financial hardship theme
- Explains how it addresses family concerns
- Provides guidance on trust and resilience
- Includes relevance score (e.g., 0.87)

---

## Response Language Options

### `response_language: "en"`
- Returns only English text
- Smaller response size
- Best for English-only users

### `response_language: "ar"`
- Returns only Arabic text
- Best for Arabic-only users
- Includes Arabic-specific explanations

### `response_language: "bilingual"` (Recommended)
- Returns both English AND Arabic text
- Complete bilingual explanations
- Shows cultural and linguistic nuances
- Best for complete understanding

---

## Integration Examples

### Using Python
```python
import requests

payload = {
    "prompt": "I'm struggling with patience during Ramadan",
    "response_language": "bilingual"
}

response = requests.post(
    "http://localhost:8001/api/v1/search/answer",
    json=payload
)

data = response.json()
for verse in data['results']['quran_verses']:
    print(f"Surah {verse['surah_number']}: {verse['surah_name']}")
    print(f"English: {verse['ayah_text_english']}")
    print(f"Arabic: {verse['ayah_text_arabic']}")
    print(f"Why selected: {verse['explanation_english']}")
    print(f"Relevance: {verse['relevance_score']}")
    print()
```

### Using cURL
```bash
curl -X POST "http://localhost:8001/api/v1/search/answer" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "أشعر بالضعف أثناء الصيام",
    "response_language": "bilingual"
  }'
```

### Using Swagger UI
1. Open http://localhost:8001/docs
2. Find POST `/api/v1/search/answer`
3. Click "Try it out"
4. Paste your request
5. See full bilingual response with explanations

---

## Database Structure

### Quran Models
- **QuranEnglish**: English translations with topics
- **QuranArabic**: Original Arabic text with topics
- Both indexed for fast searching

### Hadith Model
- **Hadith**: Bilingual hadiths with narrator and source information

---

## Configuration

In `.env`:
```
DATABASE_URL=sqlite:///./ramadan.db
DEEPSEEK_API_KEY=your_api_key_here
DEEPSEEK_API_BASE_URL=https://api.deepseek.com/v1
```

---

## Performance Notes

- **Explanation Generation**: Uses Deepseek API (async)
- **Search Speed**: Sub-second for direct searches
- **Relevance Calculation**: Fast local scoring
- **Language Detection**: Immediate (no API call)

---

## Future Enhancements

- [ ] User preference saving
- [ ] Topic categorization refinement
- [ ] Caching of explanations
- [ ] Additional language support (Urdu, Malay, etc.)
- [ ] User feedback on explanation quality
- [ ] Historical tracking of user queries
