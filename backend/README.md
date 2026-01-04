# Ramadan Helper - Backend Setup

## Prerequisites
- Python 3.8+
- PostgreSQL (recommended) or MySQL
- YouTube Data API Key

## Installation

### 1. Set Up Environment
```bash
cd backend
python -m venv venv

# On Windows
venv\Scripts\activate

# On Mac/Linux
source venv/bin/activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables
Create a `.env` file in the backend directory:
```
DATABASE_URL=postgresql://username:password@localhost:5432/ramadan_db
YOUTUBE_API_KEY=your_youtube_api_key_here
DEBUG=True
```

### 4. Get YouTube API Key
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project
3. Enable "YouTube Data API v3"
4. Create an API key
5. Add the key to your `.env` file

### 5. Set Up Database

**PostgreSQL (Recommended)**
```bash
# Install PostgreSQL
# Create database
createdb ramadan_db

# The app will automatically create tables on startup
```

**MySQL**
```bash
# Update DATABASE_URL in .env
DATABASE_URL=mysql+pymysql://username:password@localhost:3306/ramadan_db

# Install mysql-connector
pip install mysql-connector-python
```

### 6. Run the Server
```bash
python main.py

# Or use uvicorn directly
uvicorn main:app --reload
```

The API will be available at: `http://localhost:8000`
API Documentation: `http://localhost:8000/docs`

## API Endpoints

### Search Videos
```
POST /api/search
{
    "query": "anxiety ramadan",
    "user_email": "user@example.com"
}
```

### Get All Videos
```
GET /api/videos
```

### Import Videos from YouTube
```
POST /api/videos/import?keywords=ramadan&keywords=islam
{
    "youtube_ids": ["dQw4w9WgXcQ", "jNQXAC9IVRw"]
}
```

### Search YouTube (Get video IDs to import)
```
POST /api/search/youtube
{
    "query": "Ramadan Islamic lecture",
    "max_results": 10
}
```

### User Management
```
POST /api/users
{
    "email": "user@example.com",
    "name": "John Doe"
}

GET /api/users/user@example.com
```

### Save/Get Saved Videos
```
POST /api/users/{user_id}/saved-videos/{video_id}
GET /api/users/{user_id}/saved-videos
DELETE /api/users/{user_id}/saved-videos/{video_id}
```

## Database Schema

### Tables
- **users**: Store user information
- **videos**: YouTube videos with metadata
- **keywords**: Tags for categorizing videos
- **searches**: User search history
- **search_results**: Ranked search results
- **saved_videos**: Videos saved by users
- **video_keywords**: Many-to-many relationship between videos and keywords

## Workflow

1. **Admin/Setup**: Import Islamic videos from YouTube using their video IDs
2. **User Search**: User submits a search query
3. **Matching**: Backend searches videos by keyword relevance
4. **Results**: Return ranked results to frontend
5. **Save**: User can save videos for later viewing
