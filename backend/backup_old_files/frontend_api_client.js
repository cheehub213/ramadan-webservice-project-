// API Configuration
const API_BASE_URL = "http://localhost:8000/api";

// ============= API HELPER FUNCTIONS =============
async function apiCall(endpoint, options = {}) {
    const url = `${API_BASE_URL}${endpoint}`;
    const defaultOptions = {
        headers: {
            'Content-Type': 'application/json',
        },
    };
    
    try {
        const response = await fetch(url, { ...defaultOptions, ...options });
        if (!response.ok) {
            throw new Error(`API Error: ${response.status}`);
        }
        return await response.json();
    } catch (error) {
        console.error('API Call Error:', error);
        throw error;
    }
}

// ============= USER MANAGEMENT =============
async function ensureUserExists(email, name = "User") {
    try {
        // Try to get user
        const user = await apiCall(`/users/${email}`);
        return user;
    } catch (error) {
        // Create new user if doesn't exist
        const newUser = await apiCall(`/users`, {
            method: 'POST',
            body: JSON.stringify({ email, name })
        });
        return newUser;
    }
}

// ============= ISLAMIC VIDEOS SEARCH =============
async function findIslamicVideoAPI() {
    const prompt = document.getElementById('videoSearchPrompt').value.trim();

    if (!prompt) {
        alert('Please describe your problem or concern');
        return;
    }

    document.getElementById('videoLoadingIndicator').classList.remove('hidden');
    document.getElementById('videoResultsSection').classList.add('hidden');

    try {
        // Get current user
        const userEmail = localStorage.getItem('userEmail') || 'guest@ramadan.local';
        
        // Search videos via API
        const searchResults = await apiCall('/search', {
            method: 'POST',
            body: JSON.stringify({
                query: prompt,
                user_email: userEmail
            })
        });

        if (searchResults.results.length === 0) {
            alert('No videos found matching your query. Try different keywords.');
            document.getElementById('videoLoadingIndicator').classList.add('hidden');
            return;
        }

        // Display main video (top result)
        const mainVideo = searchResults.results[0].video;
        displayMainVideo(mainVideo);

        // Display similar videos
        displaySimilarVideos(searchResults.results.slice(1, 4));

        // Display all videos
        await displayAllVideosAPI();

        document.getElementById('videoLoadingIndicator').classList.add('hidden');
        document.getElementById('videoResultsSection').classList.remove('hidden');
        window.scrollTo(0, document.getElementById('videoResultsSection').offsetTop);

    } catch (error) {
        alert('Error searching videos: ' + error.message);
        document.getElementById('videoLoadingIndicator').classList.add('hidden');
    }
}

function displayMainVideo(video) {
    document.getElementById('displayVideoThumbnail').textContent = '🎥';
    document.getElementById('displayVideoTitle').textContent = video.title;
    document.getElementById('displayVideoChannel').textContent = `📺 Channel: ${video.channel}`;
    document.getElementById('displayVideoDuration').textContent = `⏱️ Duration: ${video.duration}`;
    const keywordsTags = video.keywords.map(k => k.name).join(', ');
    document.getElementById('displayVideoKeywords').textContent = `Topics: ${keywordsTags || 'Islamic content'}`;
    document.getElementById('displayVideoDescription').textContent = video.description.substring(0, 200) + '...';
    document.getElementById('displayVideoFullDescription').textContent = video.description;
    document.getElementById('displayYoutubeLink').href = `https://www.youtube.com/watch?v=${video.youtube_id}`;
}

function displaySimilarVideos(videos) {
    const similarContainer = document.getElementById('similarVideosContainer');
    similarContainer.innerHTML = '';
    
    videos.forEach(result => {
        const video = result.video;
        const videoCard = document.createElement('div');
        videoCard.className = 'bg-white rounded-lg shadow p-4 cursor-pointer hover:shadow-lg transition';
        videoCard.innerHTML = `
            <div class="text-4xl mb-3">🎥</div>
            <h3 class="font-bold text-gray-900 mb-2 text-sm">${video.title}</h3>
            <p class="text-xs text-gray-600 mb-3">${video.channel}</p>
            <a href="https://www.youtube.com/watch?v=${video.youtube_id}" target="_blank" class="text-emerald-700 font-semibold hover:text-emerald-600 text-sm">Watch Video →</a>
        `;
        similarContainer.appendChild(videoCard);
    });
}

async function displayAllVideosAPI() {
    try {
        const videos = await apiCall('/videos');
        const container = document.getElementById('allVideosContainer');
        container.innerHTML = '';
        
        videos.slice(0, 12).forEach(video => {
            const videoCard = document.createElement('div');
            videoCard.className = 'bg-white rounded-lg shadow p-6 hover:shadow-xl transition';
            const keywords = video.keywords.map(k => k.name).join(', ');
            videoCard.innerHTML = `
                <div class="text-6xl mb-4 text-center">🎥</div>
                <h3 class="font-bold text-gray-900 mb-2 h-16 overflow-hidden text-sm">${video.title}</h3>
                <p class="text-xs text-gray-600 mb-1">📺 ${video.channel}</p>
                <p class="text-xs text-gray-600 mb-4">⏱️ ${video.duration}</p>
                <p class="text-xs text-gray-700 mb-2 h-12 overflow-hidden">Topics: ${keywords || 'Islamic content'}</p>
                <a href="https://www.youtube.com/watch?v=${video.youtube_id}" target="_blank" class="block px-4 py-2 bg-red-600 text-white text-center font-semibold rounded-lg hover:bg-red-700 transition text-xs">
                    ▶️ Watch on YouTube
                </a>
            `;
            container.appendChild(videoCard);
        });
    } catch (error) {
        console.error('Error loading videos:', error);
    }
}

function findAnotherVideoAPI() {
    document.getElementById('videoSearchPrompt').value = '';
    document.getElementById('videoResultsSection').classList.add('hidden');
    document.getElementById('videoSearchPrompt').focus();
}

// ============= INITIALIZE =============
window.addEventListener('DOMContentLoaded', async function() {
    // Ensure user exists and load videos
    const userEmail = localStorage.getItem('userEmail') || 'guest@ramadan.local';
    try {
        await ensureUserExists(userEmail, 'Ramadan Helper User');
        await displayAllVideosAPI();
    } catch (error) {
        console.error('Initialization error:', error);
    }
});

// Export functions for HTML onclick handlers
window.findIslamicVideoAPI = findIslamicVideoAPI;
window.findAnotherVideoAPI = findAnotherVideoAPI;
window.ensureUserExists = ensureUserExists;
