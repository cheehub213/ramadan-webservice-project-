# 🔌 BACKEND API INTEGRATION GUIDE

## Overview

The app is ready to connect to real DeepSeek API and backend database. This guide shows what needs to be connected.

---

## 1️⃣ ASK AI / PROMPT ANALYZER

### Current Implementation (Local):
```javascript
// In app.html - analyzePrompt() function
// Uses: Local database with 6 Ayahs + 5 Hadiths
// Matching: Keyword-based algorithm
// Response time: ~2 seconds (simulated)
```

### For Production - Replace With Real API:

#### Step 1: Call DeepSeek API
```javascript
async function analyzePromptWithDeepSeek(userPrompt) {
    const response = await fetch('https://api.deepseek.com/v1/chat/completions', {
        method: 'POST',
        headers: {
            'Authorization': 'Bearer YOUR_DEEPSEEK_API_KEY',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            model: 'deepseek-chat',
            messages: [
                {
                    role: 'system',
                    content: `You are an Islamic scholar. User asked: "${userPrompt}". 
                    Provide an Islamic perspective in 2-3 sentences.`
                },
                {
                    role: 'user',
                    content: userPrompt
                }
            ],
            temperature: 0.7,
            max_tokens: 500
        })
    });

    const data = await response.json();
    const aiExplanation = data.choices[0].message.content;
    return aiExplanation;
}
```

#### Step 2: Fetch Matching Ayah from Database
```javascript
async function getRelevantAyah(userPrompt) {
    const response = await fetch('http://127.0.0.1:8001/api/v1/islamic/ayahs', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            query: userPrompt,
            limit: 1
        })
    });
    
    const data = await response.json();
    return data.ayahs[0]; // Returns: { text, arabic, reference, translation, explanation }
}
```

#### Step 3: Fetch Matching Hadith from Database
```javascript
async function getRelevantHadith(userPrompt) {
    const response = await fetch('http://127.0.0.1:8001/api/v1/islamic/hadiths', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            query: userPrompt,
            limit: 1
        })
    });
    
    const data = await response.json();
    return data.hadiths[0]; // Returns: { text, arabic, narrator, explanation }
}
```

#### Full Function for Production:
```javascript
async function analyzePrompt() {
    const prompt = document.getElementById('promptInput').value.trim();

    if (!prompt) {
        alert('Please enter your question');
        return;
    }

    document.getElementById('loadingIndicator').classList.remove('hidden');
    document.getElementById('resultsSection').classList.add('hidden');

    try {
        // Call all APIs in parallel
        const [aiExplanation, ayah, hadith] = await Promise.all([
            analyzePromptWithDeepSeek(prompt),
            getRelevantAyah(prompt),
            getRelevantHadith(prompt)
        ]);

        // Display results
        document.getElementById('aiExplanation').textContent = aiExplanation;
        document.getElementById('ayahText').textContent = ayah.arabic;
        document.getElementById('ayahReference').textContent = `📍 ${ayah.reference}`;
        document.getElementById('ayahTranslation').textContent = ayah.translation;
        document.getElementById('ayahExplanation').textContent = ayah.explanation;
        
        document.getElementById('hadithText').textContent = hadith.text;
        document.getElementById('hadithNarrator').textContent = `📚 Narrated by: ${hadith.narrator}`;
        document.getElementById('hadithExplanation').textContent = hadith.explanation;

        // Store in history
        const response = {
            id: Date.now(),
            prompt,
            aiExplanation,
            ayah,
            hadith,
            date: new Date().toLocaleDateString()
        };

        await fetch('http://127.0.0.1:8001/api/v1/ai/responses', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                email: userEmail,
                ...response
            })
        });

        document.getElementById('loadingIndicator').classList.add('hidden');
        document.getElementById('resultsSection').classList.remove('hidden');

    } catch (error) {
        alert('Error: ' + error.message);
        document.getElementById('loadingIndicator').classList.add('hidden');
    }
}
```

---

## 2️⃣ CHAT WITH IMAMS

### Current Implementation (Local):
```javascript
// In app.html - sendMessage() function
// Messages: Stored in browser localStorage
// Responses: Simulated with 1-second delay
// Per-imam: Separate conversation threads
```

### For Production - Connect to Real API:

#### Step 1: Send Message to Backend
```javascript
async function sendMessage() {
    const input = document.getElementById('messageInput');
    const message = input.value.trim();

    if (!message || !currentChat) {
        alert('Please select an imam and type a message');
        return;
    }

    // Show message immediately
    const time = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    currentChat.messages.push({
        sender: 'user',
        text: message,
        time: time
    });
    loadChatMessages();
    input.value = '';

    try {
        // Send to backend
        const response = await fetch('http://127.0.0.1:8001/api/v1/chat/conversations/' + 
            currentChat.id + '/messages', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                email: userEmail,
                imam_id: selectedImamId,
                message: message
            })
        });

        const data = await response.json();
        const imamTime = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
        
        // Add imam response
        currentChat.messages.push({
            sender: 'imam',
            text: data.response,
            time: imamTime
        });

        // Save locally
        chats[`chat_${selectedImamId}`] = currentChat;
        localStorage.setItem('chats', JSON.stringify(chats));
        loadChatMessages();

    } catch (error) {
        alert('Error sending message: ' + error.message);
    }
}
```

#### Step 2: Load Existing Conversations
```javascript
async function loadChatHistory() {
    try {
        const response = await fetch(`http://127.0.0.1:8001/api/v1/chat/conversations/user/${userEmail}`);
        const data = await response.json();
        
        // Map to local structure
        data.conversations.forEach(conv => {
            const key = `chat_${conv.imam_id}`;
            chats[key] = {
                id: conv.id,
                imam: conv.imam_name,
                messages: conv.messages,
                imam_id: conv.imam_id
            };
        });

        localStorage.setItem('chats', JSON.stringify(chats));
    } catch (error) {
        console.error('Error loading chat history:', error);
    }
}
```

#### Backend Endpoints Needed:
```
POST   /api/v1/chat/conversations/:id/messages
       Send a message to an imam

GET    /api/v1/chat/conversations/user/:email
       Get all conversations for a user

GET    /api/v1/chat/conversations/:id
       Get a specific conversation

GET    /api/v1/chat/conversations/:id/messages
       Get messages in a conversation
```

---

## 3️⃣ SAVE AI RESPONSES TO DATABASE

### Current Implementation:
```javascript
// Saved to localStorage only
```

### For Production:
```javascript
async function saveResponse() {
    if (currentAIResponse) {
        try {
            await fetch('http://127.0.0.1:8001/api/v1/ai/responses', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    email: userEmail,
                    prompt: currentAIResponse.prompt,
                    explanation: currentAIResponse.aiExplanation,
                    ayah_id: currentAIResponse.ayah.id,
                    hadith_id: currentAIResponse.hadith.id,
                    date: new Date().toISOString()
                })
            });

            alert('✅ Response saved!');
            
        } catch (error) {
            alert('Error saving: ' + error.message);
        }
    }
}
```

---

## 4️⃣ GET ISLAMIC DATABASE CONTENT

### Ayahs Endpoint:
```
POST /api/v1/islamic/ayahs
{
    "query": "anxiety",
    "limit": 1
}

Response:
{
    "ayahs": [
        {
            "id": "2:153",
            "text": "Ayah in Arabic",
            "arabic": "آية بالعربية",
            "reference": "Quran 2:153",
            "translation": "English translation",
            "explanation": "Explanation of the verse",
            "keywords": ["patience", "hardship"]
        }
    ]
}
```

### Hadiths Endpoint:
```
POST /api/v1/islamic/hadiths
{
    "query": "family",
    "limit": 1
}

Response:
{
    "hadiths": [
        {
            "id": "1",
            "text": "Hadith in English",
            "arabic": "الحديث بالعربية",
            "narrator": "Sahih Bukhari",
            "explanation": "What this hadith means",
            "keywords": ["family", "kindness"]
        }
    ]
}
```

---

## 5️⃣ HISTORY PAGE - LOAD DATA FROM DATABASE

### Current Implementation:
```javascript
// Uses local localStorage only
```

### For Production:
```javascript
async function loadAIHistory() {
    try {
        const response = await fetch(`http://127.0.0.1:8001/api/v1/ai/responses/user/${userEmail}`);
        const data = await response.json();
        aiResponses = data.responses;
        
        // Display in history page
        displayHistoryResults(data.responses);
        
    } catch (error) {
        console.error('Error loading history:', error);
        // Fall back to localStorage
        displayHistoryResults(aiResponses);
    }
}

function displayHistoryResults(responses) {
    const historyDiv = document.getElementById('aiHistory');
    historyDiv.innerHTML = responses.map(r => `
        <div class="bg-white rounded-lg shadow p-6 mb-4">
            <h3 class="font-bold text-lg mb-2">Question: ${r.prompt}</h3>
            <p class="text-gray-600 mb-4">${r.date}</p>
            <p class="text-gray-800 mb-4">${r.explanation}</p>
            <p class="text-sm">📖 Ayah: ${r.ayah.reference}</p>
            <p class="text-sm">📚 Hadith: ${r.hadith.narrator}</p>
        </div>
    `).join('');
}
```

---

## 🔐 REQUIRED ENVIRONMENT VARIABLES

```javascript
// In your backend .env file:

DEEPSEEK_API_KEY=your_key_here
DEEPSEEK_API_URL=https://api.deepseek.com/v1
FRONTEND_URL=http://localhost:5173
DATABASE_URL=your_database_connection
```

---

## 📊 COMPLETE FLOW DIAGRAM

```
User Opens app.html
    ↓
User Enters Email
    ↓
User Selects Feature:
    ├─ Ask AI → Analyzes → Calls DeepSeek → Gets Ayah/Hadith → Displays
    ├─ Chat → Selects Imam → Types Message → Sends to Backend → Gets Response
    ├─ Dua Generator → Works as is (already complete)
    └─ History → Loads from Backend + localStorage
    ↓
All Data Saved → localStorage (backup) + Backend Database (primary)
```

---

## 🚀 MIGRATION STEPS

### Phase 1: Keep Local (Current)
- Uses local database
- Uses localStorage
- Works completely offline
- Good for testing

### Phase 2: Add Backend (Optional)
- Keep local database as fallback
- Call backend APIs when available
- Sync data between devices
- Enable user accounts

### Phase 3: Full Production
- Remove local database
- Use backend only
- WebSocket for real-time chat
- Server-side authentication

---

## ✅ TESTING CHECKLIST

Before going to production:

- [ ] DeepSeek API key obtained
- [ ] Backend endpoints working
- [ ] Database has at least 10 Ayahs
- [ ] Database has at least 10 Hadiths
- [ ] Chat endpoint tested
- [ ] Message persistence works
- [ ] History loads correctly
- [ ] Error handling works
- [ ] Mobile responsive
- [ ] Performance acceptable

---

## 🎯 CODE LOCATIONS TO MODIFY

1. **Ask AI**: Lines ~574-620 in app.html
   - Replace: `findRelevantContent()` with API calls

2. **Chat**: Lines ~650-750 in app.html
   - Replace: Local responses with API calls

3. **Save Response**: Lines ~625 in app.html
   - Add: Backend save call

4. **Load History**: In history page section
   - Add: Load from backend

---

## 📞 SUPPORT

For API integration help:
- Check backend documentation
- Test endpoints with Postman first
- Use browser DevTools Console to debug
- Check Network tab for API calls

---

## 🌟 BENEFITS OF BACKEND

✅ Persist data across devices  
✅ Real-time imam responses (WebSocket)  
✅ User accounts  
✅ Better DeepSeek analysis  
✅ Statistics and analytics  
✅ Multi-language support  
✅ Spam detection  
✅ User safety features  

---

Made with ❤️ for Ramadan. May Allah accept. Ameen. 🌙
