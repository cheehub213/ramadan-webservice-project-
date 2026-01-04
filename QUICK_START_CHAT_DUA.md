# 🚀 Quick Start Guide - Chat & Dua Features

## Installation

No additional installation needed! The features are integrated into the existing system.

## Starting the Server

```bash
cd "c:\Users\cheeh\Desktop\webservice ramadan"
python -m uvicorn app.main:app --host 127.0.0.1 --port 8001
```

The server will be available at: `http://127.0.0.1:8001`

## 📚 API Documentation

Once server is running, visit:
- **Interactive Docs:** `http://127.0.0.1:8001/docs` (Swagger UI)
- **Alternative Docs:** `http://127.0.0.1:8001/redoc` (ReDoc)

## 💬 Live Chat - Quick Examples

### 1. Start a Chat with Imam

```bash
curl -X POST http://127.0.0.1:8001/api/v1/chat/conversations \
  -H "Content-Type: application/json" \
  -d '{
    "imam_id": 1,
    "user_email": "user@example.com",
    "user_name": "Ahmed",
    "title": "Marriage Advice",
    "description": "I need help with marriage communication"
  }'
```

Response will include `chat_id` - save this!

### 2. Send a Message

```bash
curl -X POST http://127.0.0.1:8001/api/v1/chat/conversations/1/messages \
  -H "Content-Type: application/json" \
  -d '{
    "message": "How can I improve communication with my spouse?",
    "sender_type": "user",
    "sender_id": "user@example.com",
    "sender_name": "Ahmed"
  }'
```

### 3. Check Messages

```bash
curl http://127.0.0.1:8001/api/v1/chat/conversations/1
```

### 4. Imam Goes Online

```bash
curl -X PUT http://127.0.0.1:8001/api/v1/chat/imam/1/availability \
  -H "Content-Type: application/json" \
  -d '{
    "is_online": true,
    "is_available_for_chat": true
  }'
```

### 5. Imam Sends Response

```bash
curl -X POST http://127.0.0.1:8001/api/v1/chat/conversations/1/messages \
  -H "Content-Type: application/json" \
  -d '{
    "message": "In Islam, open communication is essential...",
    "sender_type": "imam",
    "sender_id": "1",
    "sender_name": "Dr. Mohammad Ahmed Hassan"
  }'
```

### 6. View User's Chats

```bash
curl http://127.0.0.1:8001/api/v1/chat/conversations/user/user@example.com
```

### 7. View Imam's Chats

```bash
curl http://127.0.0.1:8001/api/v1/chat/conversations/imam/1
```

---

## 🤲 Dua Generator - Quick Examples

### 1. Get Problem Categories

```bash
curl http://127.0.0.1:8001/api/v1/dua/categories
```

### 2. Generate a Personalized Dua

```bash
curl -X POST http://127.0.0.1:8001/api/v1/dua/generate \
  -H "Content-Type: application/json" \
  -d '{
    "problem_description": "I am struggling with anger. I lose my temper easily and regret my words. I want to be more patient like the Prophet.",
    "problem_category": "Spiritual",
    "user_email": "user@example.com",
    "user_name": "Ahmed",
    "language": "English"
  }'
```

You will receive:
- **Aya** (Quranic verse) with explanation
- **Hadith** (Prophet's teaching) with guidance  
- **Dua** (Personalized supplication)

### 3. Get User's Dua History

```bash
curl http://127.0.0.1:8001/api/v1/dua/history/user@example.com
```

### 4. Submit Feedback on a Dua

```bash
curl -X POST http://127.0.0.1:8001/api/v1/dua/feedback \
  -H "Content-Type: application/json" \
  -d '{
    "dua_request_id": 1,
    "is_helpful": "yes",
    "feedback": "This dua helped me feel peaceful. I recite it daily."
  }'
```

### 5. Get Helpfulness Statistics

```bash
curl http://127.0.0.1:8001/api/v1/dua/stats/helpful
```

---

## 🧪 Run Full Test Suite

```bash
cd "c:\Users\cheeh\Desktop\webservice ramadan"
python test_chat_dua.py
```

This will test:
- Chat creation and messaging
- Imam availability
- Dua generation
- User history
- Statistics

---

## 📋 Chat Flow Diagram

```
User               System              Imam
 |                  |                   |
 +---> Start Chat --+                   |
 |                  |                   |
 |                  |<-- Notified ---+
 |                  |                |
 |                  |<-- Goes Online-+
 |                  |                |
 +---> Send Msg ----+                |
 |                  |---> Receive ---+
 |                  |                |
 |                  |<-- Send Reply--+
 |                  |                |
 +---> Read Msg ----+                |
 |                  |                |
 +---> Close Chat --+                |
```

---

## 🤲 Dua Generator Flow Diagram

```
User Input (Problem Description)
           |
           v
  Build AI Prompt
           |
           v
 Call Deepseek API
           |
           v
 Parse Response (Aya, Hadith, Dua)
           |
           v
 Store in Database
           |
           v
 Return to User
           |
           v
 User Provides Feedback
           |
           v
 Track Statistics
```

---

## 🔑 Key Endpoints Reference

### Chat
- `POST /api/v1/chat/conversations` - Start
- `POST /api/v1/chat/conversations/{id}/messages` - Send message
- `GET /api/v1/chat/conversations/{id}` - View chat
- `GET /api/v1/chat/conversations/user/{email}` - User's chats
- `GET /api/v1/chat/conversations/imam/{id}` - Imam's chats
- `PUT /api/v1/chat/imam/{id}/availability` - Imam status
- `PUT /api/v1/chat/messages/read` - Mark read

### Dua
- `POST /api/v1/dua/generate` - Generate
- `GET /api/v1/dua/history/{email}` - History
- `POST /api/v1/dua/feedback` - Feedback
- `GET /api/v1/dua/categories` - Categories
- `GET /api/v1/dua/stats/helpful` - Stats

---

## 📊 Example Response - Dua Generation

```json
{
  "id": 1,
  "user_email": "user@example.com",
  "user_name": "Ahmed",
  "problem_description": "I struggle with anger...",
  "problem_category": "Spiritual",
  "generated_aya": "Allah says in Surah Al-'Imran (3:134): 'Those who spend [in the cause of Allah] during ease and hardship and who restrain anger and who pardon the people - and Allah loves the doers of good.'\n\nExplanation: This verse teaches that controlling anger is a characteristic of the righteous.",
  "generated_hadith": "The Prophet Muhammad said: 'The strong person is not the one who can overpower others, but the one who controls himself when angry.'\n\nExplanation: This hadith directly addresses anger management and shows the Prophet's emphasis on self-control.",
  "generated_dua": "Ya Allah, I turn to You seeking help in controlling my anger and developing patience. Grant me a heart full of tranquility...",
  "created_at": "2026-01-01T12:00:00"
}
```

---

## 🧑‍💼 User Stories

### User Story 1: Get Islamic Guidance
1. User visits app and describes their marriage problem
2. System generates Quranic verse about marriage
3. System provides relevant hadith
4. System creates personalized dua for their situation
5. User rates how helpful it was
6. System tracks feedback for improvement

### User Story 2: Chat with Real Imam
1. User starts a chat with Imam #1
2. User describes their family issue
3. System notifies imam (in real-time dashboard)
4. Imam marks themselves as available
5. Imam responds with Islamic guidance
6. User reads imam's response
7. Both continue conversation until resolved
8. User closes chat (archived for later reference)

---

## 🎯 Problem Categories Available

When generating duas, choose from:
- **Family** - Marriage, children, parents
- **Health** - Illness, anxiety, stress
- **Work & Career** - Job search, business
- **Finance** - Debt, poverty, hardship
- **Spiritual** - Faith, guidance, growth
- **Education** - Studies, exams, learning
- **Relationships** - Friendships, social
- **Personal Growth** - Habits, character

---

## 🔍 Troubleshooting

### Chat not working?
- Make sure `imam_id` exists
- Check email format is valid
- Verify chat_id exists before messaging

### Dua not generating?
- Check problem description is detailed (min 20 chars)
- Ensure problem category is valid
- Verify Deepseek API is working

### Server not starting?
```bash
# Kill existing processes
taskkill /F /IM python.exe

# Then try again
python -m uvicorn app.main:app --host 127.0.0.1 --port 8001
```

---

## 📚 Documentation Files

- **CHAT_DUA_FEATURES.md** - Complete API documentation (400+ lines)
- **CHAT_DUA_IMPLEMENTATION.md** - Implementation details
- **test_chat_dua.py** - Test suite with examples
- This file - Quick start guide

---

## 💡 Tips & Tricks

1. **Get all imam chats**: Use `GET /api/v1/chat/conversations/imam/{id}` to monitor unread messages
2. **Track dua helpfulness**: Check stats with `GET /api/v1/dua/stats/helpful`
3. **Store chat IDs**: Save chat IDs when creating to avoid lookups
4. **Use categories wisely**: Specific categories give better dua results
5. **Provide detailed problems**: More detail = better personalization

---

## 🚀 Next Features Ideas

- WebSocket for real-time chat updates
- Push notifications for new messages
- Dua scheduling and reminders
- User authentication (JWT)
- Dua translations to other languages
- Image/file upload in chat
- Imam ratings based on feedback

---

**Ready to test?** Start your server and visit `/docs` for interactive testing! 🎉
