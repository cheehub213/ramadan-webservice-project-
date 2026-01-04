# 💬 Live Chat & 🤲 Personalized Dua Generator

## Overview

Two new powerful features have been added to the Ramadan WebService:

### 1. **Live Chat with Imams** 💬
Users can start real-time conversations with imams to discuss their problems. Imams can mark themselves as available/online and respond to user messages.

### 2. **Personalized Dua Generator** 🤲
When users describe their problems, the system generates:
- A relevant **Quranic verse (Aya)** with explanation
- A relevant **Hadith** with guidance
- A **Personalized Dua (supplication)** tailored to their specific situation

---

## 1️⃣ LIVE CHAT SYSTEM

### Architecture

**3 Database Tables:**
- `chats` - Stores chat conversations between users and imams
- `chat_messages` - Individual messages within conversations
- `imam_availability` - Tracks imam online/offline status

### Starting a Chat

**Endpoint:** `POST /api/v1/chat/conversations`

**Request:**
```json
{
  "imam_id": 1,
  "user_email": "user@example.com",
  "user_name": "Ahmed",
  "title": "Marriage Advice",
  "description": "I'm having difficulty communicating with my spouse about financial matters"
}
```

**Response (HTTP 200):**
```json
{
  "id": 1,
  "imam_id": 1,
  "user_email": "user@example.com",
  "user_name": "Ahmed",
  "title": "Marriage Advice",
  "description": "I'm having difficulty...",
  "is_active": true,
  "imam_is_available": false,
  "created_at": "2026-01-01T12:00:00",
  "updated_at": "2026-01-01T12:00:00",
  "last_message_at": null
}
```

### Sending Messages

**Endpoint:** `POST /api/v1/chat/conversations/{chat_id}/messages`

**Request (User message):**
```json
{
  "message": "I don't know how to discuss finances with my wife without causing arguments",
  "sender_type": "user",
  "sender_id": "user@example.com",
  "sender_name": "Ahmed"
}
```

**Request (Imam response):**
```json
{
  "message": "Based on Islamic teachings, here are some recommendations...",
  "sender_type": "imam",
  "sender_id": "1",
  "sender_name": "Dr. Mohammad Ahmed Hassan"
}
```

**Response:**
```json
{
  "id": 1,
  "chat_id": 1,
  "sender_type": "user",
  "sender_id": "user@example.com",
  "sender_name": "Ahmed",
  "message": "I don't know how to discuss...",
  "is_read": false,
  "created_at": "2026-01-01T12:00:00"
}
```

### Getting Chat History

**Endpoint:** `GET /api/v1/chat/conversations/{chat_id}`

Returns full conversation with all messages and unread count.

**Response:**
```json
{
  "id": 1,
  "imam_id": 1,
  "user_email": "user@example.com",
  "user_name": "Ahmed",
  "title": "Marriage Advice",
  "description": "...",
  "is_active": true,
  "imam_is_available": true,
  "messages": [
    {
      "id": 1,
      "chat_id": 1,
      "sender_type": "user",
      "sender_id": "user@example.com",
      "sender_name": "Ahmed",
      "message": "...",
      "is_read": true,
      "created_at": "2026-01-01T12:00:00"
    },
    {
      "id": 2,
      "chat_id": 1,
      "sender_type": "imam",
      "sender_id": "1",
      "sender_name": "Dr. Mohammad Ahmed Hassan",
      "message": "Based on Islamic teachings...",
      "is_read": true,
      "created_at": "2026-01-01T12:05:00"
    }
  ],
  "unread_count": 0,
  "created_at": "2026-01-01T12:00:00",
  "updated_at": "2026-01-01T12:05:00"
}
```

### User Chat List

**Endpoint:** `GET /api/v1/chat/conversations/user/{user_email}`

**Query Parameters:**
- `active_only` (boolean, default: true) - Show only active chats

**Response:**
```json
[
  {
    "id": 1,
    "imam_id": 1,
    "user_email": "user@example.com",
    "user_name": "Ahmed",
    "title": "Marriage Advice",
    "is_active": true,
    "imam_is_available": true,
    "last_message_at": "2026-01-01T12:05:00",
    "unread_count": 0
  },
  {
    "id": 2,
    "imam_id": 2,
    "user_email": "user@example.com",
    "user_name": "Ahmed",
    "title": "Youth Guidance",
    "is_active": true,
    "imam_is_available": false,
    "last_message_at": "2026-01-01T13:30:00",
    "unread_count": 2
  }
]
```

### Imam Chat List

**Endpoint:** `GET /api/v1/chat/conversations/imam/{imam_id}`

Shows all chats for a specific imam with unread user messages count.

### Imam Availability Status

**Endpoint:** `PUT /api/v1/chat/imam/{imam_id}/availability`

**Request:**
```json
{
  "is_online": true,
  "is_available_for_chat": true
}
```

**Response:**
```json
{
  "id": 1,
  "imam_id": 1,
  "is_online": true,
  "is_available_for_chat": true,
  "last_seen_at": "2026-01-01T12:00:00",
  "last_status_change_at": "2026-01-01T12:00:00"
}
```

### Mark Messages as Read

**Endpoint:** `PUT /api/v1/chat/messages/read`

**Request:**
```json
{
  "message_ids": [1, 2, 3]
}
```

**Response:**
```json
{
  "status": "success",
  "marked_as_read": 3
}
```

### Mark Entire Chat as Read

**Endpoint:** `PUT /api/v1/chat/conversations/{chat_id}/read`

**Response:**
```json
{
  "status": "success",
  "marked_as_read": 5
}
```

### Close Chat

**Endpoint:** `PUT /api/v1/chat/conversations/{chat_id}/close`

Marks conversation as inactive (archived).

---

## 2️⃣ PERSONALIZED DUA GENERATOR

### How It Works

Users describe their problem → System uses AI to generate:
1. **Quranic Verse (Aya)** - Relevant Surah and verse with explanation
2. **Hadith** - Prophet's teachings related to the problem
3. **Personalized Dua** - Supplication asking Allah for help

All responses are generated using the Deepseek AI API and tailored to the specific problem.

### Generating a Dua

**Endpoint:** `POST /api/v1/dua/generate`

**Request:**
```json
{
  "problem_description": "I'm struggling with anger and impatience. I lose my temper easily and say things I regret. I want to improve my character and be more patient like Prophet was.",
  "problem_category": "Spiritual",
  "user_email": "user@example.com",
  "user_name": "Ahmed",
  "language": "English"
}
```

**Response (HTTP 200):**
```json
{
  "id": 1,
  "user_email": "user@example.com",
  "user_name": "Ahmed",
  "problem_description": "I'm struggling with anger...",
  "problem_category": "Spiritual",
  "generated_aya": "Allah says in Surah Al-'Imran (3:134): 'Those who spend [in the cause of Allah] during ease and hardship and who restrain anger and who pardon the people - and Allah loves the doers of good.'(Surah Al-'Imran, Verse 134)\n\nExplanation: This verse teaches that controlling anger is a characteristic of those who are righteous. It shows that patience and forgiveness are highly valued in Islam.",
  "generated_hadith": "The Prophet Muhammad said: 'The strong person is not the one who can overpower others, but the one who controls himself when angry.' (Hadith: Sahih Bukhari 5763)\n\nExplanation: This hadith directly addresses anger management and shows the Prophet's emphasis on self-control as a sign of true strength.",
  "generated_dua": "Ya Allah (O Allah), I turn to You seeking help in controlling my anger and developing patience. Grant me a heart full of tranquility, a tongue that speaks wisdom, and hands that do good. Help me follow the example of Your Prophet in patience and forgiveness. When anger rises, help me remember Your mercy and teach me to respond with gentleness. O Allah, transform my character and make me among those who are patient and forgiving. Ameen.\n\nHow to use: Recite this dua whenever you feel anger rising, preferably after wudu (ablution). Also recite it in the morning and evening.",
  "created_at": "2026-01-01T12:00:00"
}
```

### Problem Categories

**Available categories:**
- Family - Family relationships, marriage, children, parents
- Health - Physical and mental health concerns
- Work & Career - Job, career, business, wealth
- Finance - Financial difficulties and decisions
- Spiritual - Spiritual growth, faith, guidance
- Education - Studies, learning, academic challenges
- Relationships - Friendships, social connections
- Personal Growth - Self-improvement, character development

**Endpoint:** `GET /api/v1/dua/categories`

```json
[
  {
    "id": 1,
    "name": "Family",
    "description": "Family relationships, marriage, children, parents",
    "icon": "👨‍👩‍👧‍👦",
    "example_problems": "Marital issues, communication problems, parenting challenges"
  },
  {
    "id": 2,
    "name": "Health",
    "description": "Physical and mental health concerns",
    "icon": "🏥",
    "example_problems": "Illness, anxiety, stress, recovery"
  }
  // ... more categories
]
```

### Dua Examples

**Example 1: Financial Difficulty**

```json
POST /api/v1/dua/generate
{
  "problem_description": "I've been unemployed for 6 months and my savings are running out. I feel hopeless and worried about my family's future. I need Allah's help to find a job.",
  "problem_category": "Finance",
  "user_email": "business@example.com",
  "language": "English"
}
```

**Generated Response includes:**
- Surah Al-Waqi'ah (56:73) about Allah's provision
- Hadith about relying on Allah
- Dua asking for sustenance and successful job search

**Example 2: Health Issue**

```json
POST /api/v1/dua/generate
{
  "problem_description": "My mother has been diagnosed with cancer. I'm very worried about her health and recovery. Please help us find strength during this difficult time.",
  "problem_category": "Health",
  "user_email": "user@example.com"
}
```

**Generated Response includes:**
- Surah Al-Balad (90:10) about patience during hardship
- Hadith about visiting the sick
- Dua for healing and patience

**Example 3: Family Conflict**

```json
POST /api/v1/dua/generate
{
  "problem_description": "My teenage son doesn't listen to me anymore. We argue about everything - studies, friends, religion. I don't know how to reach him.",
  "problem_category": "Family",
  "user_email": "parent@example.com"
}
```

**Generated Response includes:**
- Surah Luqman guidance about parenting
- Hadith about respecting parents
- Personalized dua for improved parent-child relationship

### User History

**Endpoint:** `GET /api/v1/dua/history/{user_email}`

**Query Parameters:**
- `limit` (integer, default: 10, max: 100) - Number of records to return

**Response:**
```json
[
  {
    "id": 1,
    "problem_description": "I'm struggling with anger...",
    "problem_category": "Spiritual",
    "generated_dua": "Ya Allah...",
    "is_helpful": "yes",
    "created_at": "2026-01-01T12:00:00"
  },
  {
    "id": 2,
    "problem_description": "Financial difficulty...",
    "problem_category": "Finance",
    "generated_dua": "Ya Allah, grant me sustenance...",
    "is_helpful": null,
    "created_at": "2025-12-31T15:00:00"
  }
]
```

### Submit Feedback

**Endpoint:** `POST /api/v1/dua/feedback`

**Request:**
```json
{
  "dua_request_id": 1,
  "is_helpful": "yes",
  "feedback": "The dua really helped me feel more peaceful. I've been reciting it daily."
}
```

**Response:**
```json
{
  "status": "success",
  "message": "Feedback recorded"
}
```

### View Specific Dua

**Endpoint:** `GET /api/v1/dua/{dua_request_id}`

Retrieves a previously generated dua with all its details.

### Statistics

**Endpoint:** `GET /api/v1/dua/stats/helpful`

Shows how helpful the generated duas have been overall.

**Response:**
```json
{
  "total_requests": 150,
  "helpful": 128,
  "not_helpful": 12,
  "helpful_percentage": 85.33
}
```

---

## 📱 User Workflow

### Chat User Journey:
1. User selects an imam from the directory
2. **POST** `/api/v1/chat/conversations` - Starts chat
3. **POST** `/api/v1/chat/conversations/{chat_id}/messages` - Sends first message
4. Imam receives notification (check via **GET** `/api/v1/chat/conversations/imam/{imam_id}`)
5. **PUT** `/api/v1/chat/imam/{imam_id}/availability` - Imam marks as available
6. Imam **POST**s response messages
7. User sees new messages (check for `unread_count`)
8. **PUT** `/api/v1/chat/messages/read` - Mark messages as read
9. Chat continues until resolved
10. **PUT** `/api/v1/chat/conversations/{chat_id}/close` - Close chat when done

### Dua Generator User Journey:
1. User describes their problem
2. **POST** `/api/v1/dua/generate` - Get personalized guidance
3. Receive Aya, Hadith, and Dua
4. **POST** `/api/v1/dua/feedback` - Provide feedback if helpful
5. **GET** `/api/v1/dua/history/{user_email}` - View past duas

---

## Database Schema

### Chat Tables

```sql
CREATE TABLE chats (
  id INTEGER PRIMARY KEY,
  imam_id INTEGER NOT NULL,
  user_email VARCHAR(255) NOT NULL,
  user_name VARCHAR(255),
  title VARCHAR(255),
  description TEXT,
  is_active BOOLEAN DEFAULT TRUE,
  imam_is_available BOOLEAN DEFAULT FALSE,
  created_at DATETIME,
  updated_at DATETIME,
  last_message_at DATETIME
);

CREATE TABLE chat_messages (
  id INTEGER PRIMARY KEY,
  chat_id INTEGER NOT NULL FOREIGN KEY,
  sender_type VARCHAR(20) NOT NULL,  -- "user" or "imam"
  sender_id VARCHAR(255) NOT NULL,
  sender_name VARCHAR(255),
  message TEXT NOT NULL,
  is_read BOOLEAN DEFAULT FALSE,
  read_at DATETIME,
  created_at DATETIME,
  updated_at DATETIME
);

CREATE TABLE imam_availability (
  id INTEGER PRIMARY KEY,
  imam_id INTEGER NOT NULL UNIQUE,
  is_online BOOLEAN DEFAULT FALSE,
  is_available_for_chat BOOLEAN DEFAULT FALSE,
  last_seen_at DATETIME,
  last_status_change_at DATETIME,
  auto_offline_after_minutes INTEGER DEFAULT 15
);
```

### Dua Tables

```sql
CREATE TABLE dua_requests (
  id INTEGER PRIMARY KEY,
  user_email VARCHAR(255),
  user_name VARCHAR(255),
  problem_description TEXT NOT NULL,
  problem_category VARCHAR(100),
  language VARCHAR(50) DEFAULT "English",
  generated_aya TEXT,
  generated_hadith TEXT,
  generated_dua TEXT,
  deepseek_prompt TEXT,
  deepseek_response TEXT,
  is_helpful VARCHAR(10),  -- "yes", "no", or null
  user_feedback TEXT,
  created_at DATETIME,
  updated_at DATETIME
);

CREATE TABLE dua_categories (
  id INTEGER PRIMARY KEY,
  name VARCHAR(100) NOT NULL UNIQUE,
  description TEXT,
  icon VARCHAR(50),
  example_problems TEXT
);
```

---

## API Summary

### Chat Endpoints (8 total)
1. `POST /api/v1/chat/conversations` - Start chat
2. `GET /api/v1/chat/conversations/{chat_id}` - Get chat details
3. `GET /api/v1/chat/conversations/user/{user_email}` - User's chats
4. `GET /api/v1/chat/conversations/imam/{imam_id}` - Imam's chats
5. `POST /api/v1/chat/conversations/{chat_id}/messages` - Send message
6. `GET /api/v1/chat/conversations/{chat_id}/messages` - Get messages
7. `PUT /api/v1/chat/messages/read` - Mark messages read
8. `PUT /api/v1/chat/conversations/{chat_id}/read` - Mark chat read
9. `PUT /api/v1/chat/imam/{imam_id}/availability` - Update imam status
10. `GET /api/v1/chat/imam/{imam_id}/availability` - Get imam status
11. `PUT /api/v1/chat/conversations/{chat_id}/close` - Close chat

### Dua Generator Endpoints (7 total)
1. `POST /api/v1/dua/generate` - Generate personalized dua
2. `GET /api/v1/dua/history/{user_email}` - Get user history
3. `POST /api/v1/dua/feedback` - Submit feedback
4. `GET /api/v1/dua/categories` - Get problem categories
5. `GET /api/v1/dua/{dua_request_id}` - Get specific dua
6. `GET /api/v1/dua/stats/helpful` - Get helpfulness stats

---

## 🎯 Key Features

### Chat System:
✅ Real-time messaging with imams
✅ Message read/unread tracking
✅ Imam availability status
✅ Chat history and archiving
✅ Multiple concurrent chats per user
✅ Unread message count

### Dua Generator:
✅ Personalized Quranic verses
✅ Relevant Hadiths with explanations
✅ Custom duas based on problems
✅ AI-powered using Deepseek API
✅ User feedback & ratings
✅ History tracking
✅ 8 problem categories
✅ Multi-language support

---

**Ready to test? Check the API documentation at `/docs`!** 🚀
