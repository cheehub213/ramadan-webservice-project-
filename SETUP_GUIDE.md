# Ramadan Helper - Complete Setup Guide

## Project Structure
```
webservice ramadan/
├── app/
│   └── schemas/
│       └── frontend webservice site/
│           └── app.html (Updated Frontend)
└── backend/
    ├── main.py (FastAPI App)
    ├── config.py (Configuration)
    ├── database.py (Database Setup)
    ├── models.py (SQLAlchemy Models)
    ├── schemas.py (Pydantic Schemas)
    ├── routes.py (API Endpoints)
    ├── youtube_service.py (YouTube Integration)
    ├── frontend_api_client.js (Frontend API calls)
    ├── requirements.txt
    ├── .env (Environment variables)
    └── README.md
```

## Step-by-Step Setup

### Phase 1: Backend Setup

#### 1.1 Install PostgreSQL

**Windows:**
- Download from [postgresql.org](https://www.postgresql.org/download/windows/)
- Run installer, note down username and password
- Default port: 5432

**Or use Docker:**
```bash
docker run --name ramadan_postgres -e POSTGRES_PASSWORD=password -e POSTGRES_DB=ramadan_db -p 5432:5432 -d postgres
```

#### 1.2 Install Python Dependencies
```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

#### 1.3 Get YouTube API Key
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create new project "Ramadan Helper"
3. Enable "YouTube Data API v3"
4. Create API key (Credentials → API key)
5. Copy the key

#### 1.4 Configure Environment
Create `.env` file in backend/:
```
DATABASE_URL=postgresql://postgres:your_password@localhost:5432/ramadan_db
YOUTUBE_API_KEY=your_youtube_api_key_here
DEBUG=True
```

#### 1.5 Run Backend
```bash
# From backend directory
python main.py

# Server runs at http://localhost:8000
# API Docs at http://localhost:8000/docs
```

### Phase 2: Populate Videos

#### 2.1 Search YouTube for Videos
Use the API playground at `http://localhost:8000/docs`

**Example:** Search for "Ramadan Islamic lecture"
```bash
curl -X POST "http://localhost:8000/api/search/youtube" \
  -H "Content-Type: application/json" \
  -d '{"query":"Ramadan Islamic lecture", "max_results": 10}'
```

#### 2.2 Copy Video IDs from Results
Save the video IDs (e.g., "dQw4w9WgXcQ")

#### 2.3 Import Videos to Database
```bash
curl -X POST "http://localhost:8000/api/videos/import?keywords=ramadan&keywords=islam&keywords=lecture" \
  -H "Content-Type: application/json" \
  -d '{"youtube_ids": ["dQw4w9WgXcQ", "jNQXAC9IVRw"]}'
```

### Phase 3: Update Frontend

#### 3.1 Replace Video Search Function
In `app.html`, replace the `findIslamicVideo()` function with `findIslamicVideoAPI()` from `frontend_api_client.js`

#### 3.2 Link to Backend
In `app.html`, add script before closing `</body>` tag:
```html
<script src="/path/to/frontend_api_client.js"></script>
```

Update `findIslamicVideo()` onclick handlers to `findIslamicVideoAPI()`

### Phase 4: Test the System

#### 4.1 Test Backend
```bash
# Health check
curl http://localhost:8000/health

# Get all videos
curl http://localhost:8000/api/videos

# Search videos
curl -X POST "http://localhost:8000/api/search" \
  -H "Content-Type: application/json" \
  -d '{"query": "anxiety", "user_email": "test@example.com"}'
```

#### 4.2 Test Frontend
1. Open `app.html` in browser
2. Navigate to "📺 Islamic Videos"
3. Enter search query
4. Should see results from database

## API Endpoints Reference

### Search
- `POST /api/search` - Search videos by query

### Videos
- `GET /api/videos` - Get all videos
- `GET /api/videos/{id}` - Get specific video
- `POST /api/videos/import` - Import from YouTube
- `POST /api/search/youtube` - Search YouTube

### Users
- `POST /api/users` - Create user
- `GET /api/users/{email}` - Get user

### Saved Videos
- `POST /api/users/{user_id}/saved-videos/{video_id}` - Save video
- `GET /api/users/{user_id}/saved-videos` - Get saved videos
- `DELETE /api/users/{user_id}/saved-videos/{video_id}` - Unsave video

## Troubleshooting

### Database Connection Error
```
ERROR: could not connect to server
```
**Solution:** Check PostgreSQL is running
```bash
# Windows
pg_isready -h localhost

# Or restart service
net start postgresql-x64-##
```

### YouTube API Error
```
401 Unauthorized
```
**Solution:** Check YOUTUBE_API_KEY in .env is correct

### CORS Error in Browser
```
Access to XMLHttpRequest blocked by CORS
```
**Solution:** Backend is running? Check http://localhost:8000/health

### No Videos Found
**Solution:** You need to import videos first using the `/api/videos/import` endpoint

## Next Steps

1. Populate database with more Islamic videos
2. Deploy backend to cloud (Heroku, AWS, DigitalOcean)
3. Update frontend API_BASE_URL to point to deployed backend
4. Add video ratings and reviews
5. Add user authentication
6. Add more search filters and categories

## Support

For issues:
1. Check backend logs: `python main.py` console output
2. Check API docs: `http://localhost:8000/docs`
3. Check browser console for frontend errors
4. Verify database connection: `psql -U postgres -d ramadan_db`
