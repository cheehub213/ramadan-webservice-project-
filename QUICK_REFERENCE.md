# 🌍 Bilingual API - Quick Reference Card

## What's New? 🎉

✅ **Arabic Support** - Accept prompts in English OR Arabic  
✅ **Bilingual Responses** - Get results in EN, AR, or BOTH  
✅ **Smart Explanations** - Know WHY each verse/hadith was chosen  
✅ **Relevance Scoring** - See how relevant each result is (0-1)  
✅ **Matched Keywords** - Track which words triggered each result  

---

## 3 Ways to Use the API

### 1️⃣ **Intelligent Search** (Recommended)
**Endpoint:** `POST /api/v1/search/answer`

```json
{
  "prompt": "I'm struggling with patience",
  "response_language": "bilingual"
}
```

**You Get:**
- AI analysis of your concern
- Relevant Quran verses with explanations
- Relevant Hadiths with explanations
- Emotion detected, topics extracted, relevance scores

### 2️⃣ **Direct Quran Search**
**Endpoint:** `GET /api/v1/search/quran?keywords=patience&response_language=bilingual`

**You Get:**
- Matching verses only
- Bilingual text
- Relevance scores
- Matched keywords

### 3️⃣ **Direct Hadith Search**
**Endpoint:** `GET /api/v1/search/hadith?keywords=trust&response_language=bilingual`

**You Get:**
- Matching Hadiths only
- Bilingual text
- Relevance scores
- Source information

---

## Language Options

| Value | What You Get |
|-------|-------------|
| `"en"` | English text + English explanations |
| `"ar"` | Arabic text + Arabic explanations |
| `"bilingual"` | BOTH English AND Arabic for everything |

---

## Example Requests

### English Prompt → Bilingual
```bash
curl -X POST "http://localhost:8001/api/v1/search/answer" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "I feel weak during fasting",
    "response_language": "bilingual"
  }'
```

### Arabic Prompt → Arabic
```bash
curl -X POST "http://localhost:8001/api/v1/search/answer" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "أشعر بالضعف أثناء الصيام",
    "response_language": "ar"
  }'
```

### Search Quran (Bilingual)
```bash
curl "http://localhost:8001/api/v1/search/quran?keywords=patience,strength&response_language=bilingual&limit=5"
```

---

## Response Overview

```json
{
  "status": "success",
  "user_prompt": "Original prompt",
  "prompt_language": "en or ar",
  "response_language": "selected language",
  
  "analysis": {
    "topics": ["patience", "faith"],
    "keywords": ["struggling", "help"],
    "emotion": "distressed",
    "summary": "User seeks guidance on..."
  },
  
  "results": {
    "quran_verses": [
      {
        "surah_number": 2,
        "surah_name": "Al-Baqarah",
        "ayah_number": 286,
        
        // Available if response_language includes "en"
        "ayah_text_english": "Allah does not burden...",
        "explanation_english": "Why this verse helps your situation",
        
        // Available if response_language includes "ar"
        "ayah_text_arabic": "لا يكلف الله نفسا...",
        "explanation_arabic": "شرح لماذا تساعد هذه الآية",
        
        // Always included
        "relevance_score": 0.92,        // 0-1 scale
        "matched_keywords": ["burden"]  // Which words matched
      }
    ],
    "hadiths": [ /* Similar structure */ ]
  }
}
```

---

## What Each Field Means

| Field | Meaning |
|-------|---------|
| `prompt_language` | Language AI detected in your prompt |
| `response_language` | Language(s) you requested in response |
| `topics` | Main themes extracted from your concern |
| `keywords` | Specific words used to search database |
| `emotion` | Emotional state detected by AI |
| `relevance_score` | How relevant (0=not relevant, 1=highly relevant) |
| `matched_keywords` | Which keywords from analysis matched this result |
| `explanation_*` | Why this specific verse/hadith was selected |

---

## Test Different Scenarios

### Health & Physical Challenges
```
Prompt: "I'm exhausted during fasting"
Response Language: "bilingual"
```

### Emotional & Spiritual Struggles
```
Prompt: "I feel disconnected from my faith"
Response Language: "bilingual"
```

### Family Issues
```
Prompt: "My family is in conflict"
Response Language: "bilingual"
```

### Financial Concerns
```
Prompt: "I lost my job and worried about family"
Response Language: "bilingual"
```

### Moral Dilemmas
```
Prompt: "Someone asked me to compromise my integrity"
Response Language: "bilingual"
```

### Using Arabic Prompts
```
Prompt: "أنا أعاني من الشكوك في إيماني"
Response Language: "bilingual"
```

---

## Testing

Run all tests:
```bash
python test_bilingual_api.py
```

Tests 10 different scenarios including:
- English → Bilingual
- Arabic → Arabic
- Arabic → English
- Mixed languages
- Direct searches
- Various life situations

---

## Via Swagger UI (Easiest! 🎯)

1. Open: http://localhost:8001/docs
2. Find: **POST /api/v1/search/answer**
3. Click: **"Try it out"**
4. Paste request from above
5. Click: **"Execute"**
6. See full bilingual response! ✨

---

## Response Language Comparison

### English Only (`response_language: "en"`)
```json
{
  "ayah_text_english": "...",
  "explanation_english": "...",
  "matched_keywords": [...]
}
```
**Best for:** English-only users, smaller responses

### Arabic Only (`response_language: "ar"`)
```json
{
  "ayah_text_arabic": "...",
  "explanation_arabic": "...",
  "matched_keywords": [...]
}
```
**Best for:** Arabic-only users

### Bilingual (`response_language: "bilingual"`)
```json
{
  "ayah_text_english": "...",
  "ayah_text_arabic": "...",
  "explanation_english": "...",
  "explanation_arabic": "...",
  "matched_keywords": [...]
}
```
**Best for:** Complete understanding, bilingual users, learning

---

## Key Points ✨

1. **Auto-Detect**: No need to tell API if prompt is English/Arabic - it figures it out!
2. **Bilingual Default**: Default response language is "bilingual" for maximum helpfulness
3. **Explanations**: Every result explains WHY it was selected - not just what it is
4. **Scoring**: Higher relevance score = more relevant to your situation
5. **Transparency**: See which keywords matched = understand the matching logic

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| No results found | Try different keywords, check spelling |
| Want English only | Set `response_language: "en"` |
| Want Arabic only | Set `response_language: "ar"` |
| Want to understand why | Use `response_language: "bilingual"` for explanations |
| API is slow | Explanations take longer - wait a few seconds |

---

## Files to Review

📄 **BILINGUAL_FEATURES.md** - Full feature documentation  
📄 **API_UPDATED.md** - Technical update details  
📄 **example_responses.json** - Sample request/response pairs  
📄 **test_bilingual_api.py** - 10 working test cases  
📄 **QUICK_REFERENCE.md** - This file  

---

## Next Steps

1. ✅ Read this quick reference
2. ✅ Open Swagger UI: http://localhost:8001/docs
3. ✅ Try the `/answer` endpoint with a bilingual prompt
4. ✅ Run `python test_bilingual_api.py` to see all examples
5. ✅ Explore different `response_language` options

---

## Support & Questions

For detailed information:
- **Features**: See BILINGUAL_FEATURES.md
- **Examples**: See example_responses.json
- **Tests**: See test_bilingual_api.py
- **Technical Details**: See API_UPDATED.md

---

**Happy exploring! 🌟**

The API now speaks your language and explains its wisdom! 
