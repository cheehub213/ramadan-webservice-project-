// =====================================================
// API SERVICE MODULE FOR RAMADAN HELPER FRONTEND
// =====================================================
// File: /js/api-service.js
// Purpose: Centralized API client for all backend calls
// =====================================================

const API_BASE = 'http://localhost:8000/api';

/**
 * Comprehensive API Service for Ramadan Helper
 * All backend endpoint calls go through this module
 */
const apiService = {

  // ====================== USER ENDPOINTS ======================
  
  /**
   * Login or register a user
   * @param {string} email - User email
   * @param {string} name - User name (optional)
   * @param {string} userType - "user" or "imam"
   * @returns {Promise} User object with id, email, name, user_type
   */
  loginUser: async function(email, name = '', userType = 'user') {
    const response = await fetch(`${API_BASE}/users/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, name, user_type: userType })
    });
    if (!response.ok) throw new Error('Login failed');
    return response.json();
  },

  /**
   * Get user profile
   * @param {string} email - User email
   * @returns {Promise} User object
   */
  getUser: async function(email) {
    const response = await fetch(`${API_BASE}/users/${email}`);
    if (!response.ok) throw new Error('User not found');
    return response.json();
  },

  // ====================== DUA ENDPOINTS ======================

  /**
   * Get all dua categories
   * @returns {Promise} Object with categories array
   */
  getDuaCategories: async function() {
    const response = await fetch(`${API_BASE}/dua/categories`);
    if (!response.ok) throw new Error('Failed to get categories');
    return response.json();
  },

  /**
   * Generate personalized dua
   * @param {string} email - User email
   * @param {string} category - Dua category
   * @param {string} context - User's situation description
   * @returns {Promise} Dua object with bilingual texts
   */
  generateDua: async function(email, category, context) {
    const response = await fetch(`${API_BASE}/dua/generate`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, category, context })
    });
    if (!response.ok) throw new Error('Failed to generate dua');
    return response.json();
  },

  /**
   * Get user's dua history
   * @param {string} email - User email
   * @returns {Promise} Array of dua history objects
   */
  getDuaHistory: async function(email) {
    const response = await fetch(`${API_BASE}/dua/history/${email}`);
    if (!response.ok) throw new Error('Failed to get dua history');
    return response.json();
  },

  /**
   * Submit feedback on a dua
   * @param {number} duaId - Dua ID
   * @param {boolean} helpful - Was it helpful?
   * @param {string} notes - Optional feedback notes
   * @returns {Promise} Response object
   */
  submitDuaFeedback: async function(duaId, helpful, notes = '') {
    const response = await fetch(`${API_BASE}/dua/feedback`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ dua_id: duaId, helpful, notes })
    });
    if (!response.ok) throw new Error('Failed to submit feedback');
    return response.json();
  },

  // ====================== IMAM ENDPOINTS ======================

  /**
   * Get all available imams
   * @returns {Promise} Array of imam objects
   */
  getImams: async function() {
    const response = await fetch(`${API_BASE}/imams`);
    if (!response.ok) throw new Error('Failed to get imams');
    return response.json();
  },

  /**
   * Get specific imam details
   * @param {number} imamId - Imam ID
   * @returns {Promise} Imam object
   */
  getImam: async function(imamId) {
    const response = await fetch(`${API_BASE}/imams/${imamId}`);
    if (!response.ok) throw new Error('Imam not found');
    return response.json();
  },

  // ====================== CHAT ENDPOINTS ======================

  /**
   * Create new conversation with imam
   * @param {string} userEmail - User email
   * @param {number} imamId - Imam ID
   * @param {string} topic - Conversation topic
   * @returns {Promise} Conversation object
   */
  createConversation: async function(userEmail, imamId, topic) {
    const response = await fetch(`${API_BASE}/chat/conversations`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ user_email: userEmail, imam_id: imamId, topic })
    });
    if (!response.ok) throw new Error('Failed to create conversation');
    return response.json();
  },

  /**
   * Get all conversations for user
   * @param {string} userEmail - User email
   * @returns {Promise} Array of conversation objects
   */
  getUserConversations: async function(userEmail) {
    const response = await fetch(`${API_BASE}/chat/conversations/${userEmail}`);
    if (!response.ok) throw new Error('Failed to get conversations');
    return response.json();
  },

  /**
   * Send message in conversation
   * @param {number} conversationId - Conversation ID
   * @param {string} senderEmail - Sender email
   * @param {string} senderType - "user" or "imam"
   * @param {string} messageText - Message content
   * @returns {Promise} Message object
   */
  sendMessage: async function(conversationId, senderEmail, senderType, messageText) {
    const response = await fetch(`${API_BASE}/chat/messages`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        conversation_id: conversationId,
        sender_email: senderEmail,
        sender_type: senderType,
        message_text: messageText
      })
    });
    if (!response.ok) throw new Error('Failed to send message');
    return response.json();
  },

  /**
   * Get all messages in conversation
   * @param {number} conversationId - Conversation ID
   * @returns {Promise} Array of message objects
   */
  getConversationMessages: async function(conversationId) {
    const response = await fetch(`${API_BASE}/chat/messages/${conversationId}`);
    if (!response.ok) throw new Error('Failed to get messages');
    return response.json();
  },

  // ====================== ANALYZER ENDPOINTS ======================

  /**
   * Analyze Islamic question (Ask AI)
   * @param {string} email - User email
   * @param {string} question - Islamic question
   * @returns {Promise} Analysis object with ayah, hadith, explanation
   */
  analyzeQuestion: async function(email, question) {
    const response = await fetch(`${API_BASE}/analyzer/analyze`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, question })
    });
    if (!response.ok) throw new Error('Failed to analyze question');
    return response.json();
  },

  /**
   * Get all Quranic verses
   * @returns {Promise} Object with ayahs array
   */
  getAyahs: async function() {
    const response = await fetch(`${API_BASE}/analyzer/ayahs`);
    if (!response.ok) throw new Error('Failed to get ayahs');
    return response.json();
  },

  /**
   * Get all Hadith sayings
   * @returns {Promise} Object with hadiths array
   */
  getHadiths: async function() {
    const response = await fetch(`${API_BASE}/analyzer/hadiths`);
    if (!response.ok) throw new Error('Failed to get hadiths');
    return response.json();
  },

  // ====================== VIDEO ENDPOINTS ======================

  /**
   * Get all videos
   * @returns {Promise} Array of video objects
   */
  getVideos: async function() {
    const response = await fetch(`${API_BASE}/videos`);
    if (!response.ok) throw new Error('Failed to get videos');
    return response.json();
  },

  /**
   * Get specific video
   * @param {number} videoId - Video ID
   * @returns {Promise} Video object
   */
  getVideo: async function(videoId) {
    const response = await fetch(`${API_BASE}/videos/${videoId}`);
    if (!response.ok) throw new Error('Video not found');
    return response.json();
  },

  /**
   * Search videos by query
   * @param {string} query - Search query
   * @returns {Promise} Array of matching video objects
   */
  searchVideos: async function(query) {
    const response = await fetch(
      `${API_BASE}/videos/search?query=${encodeURIComponent(query)}`
    );
    if (!response.ok) throw new Error('Failed to search videos');
    return response.json();
  },

  /**
   * Add new video to database
   * @param {object} videoData - Video object
   * @returns {Promise} Response with video ID
   */
  addVideo: async function(videoData) {
    const response = await fetch(`${API_BASE}/videos/add`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(videoData)
    });
    if (!response.ok) throw new Error('Failed to add video');
    return response.json();
  },

  // ====================== HISTORY ENDPOINTS ======================

  /**
   * Get user activity history
   * @param {string} userEmail - User email
   * @returns {Promise} Array of history objects
   */
  getUserHistory: async function(userEmail) {
    const response = await fetch(`${API_BASE}/history/${userEmail}`);
    if (!response.ok) throw new Error('Failed to get history');
    return response.json();
  },

  /**
   * Log user action
   * @param {string} userEmail - User email
   * @param {string} actionType - Type of action
   * @param {object} actionData - Action details
   * @returns {Promise} Response object
   */
  logAction: async function(userEmail, actionType, actionData) {
    const response = await fetch(`${API_BASE}/history/log`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        user_email: userEmail,
        action_type: actionType,
        action_data: actionData
      })
    });
    if (!response.ok) throw new Error('Failed to log action');
    return response.json();
  }
};

// =====================================================================
// USAGE EXAMPLES
// =====================================================================

/*
// Example 1: Login User
const user = await apiService.loginUser('user@example.com', 'John');

// Example 2: Generate Dua
const dua = await apiService.generateDua(
  'user@example.com',
  'Fear & Anxiety',
  'I am anxious about my future'
);
displayDua(dua);

// Example 3: Get Imams and Create Chat
const imams = await apiService.getImams();
const conversation = await apiService.createConversation(
  'user@example.com',
  imams[0].id,
  'Islamic Guidance'
);

// Example 4: Send Message
await apiService.sendMessage(
  conversation.id,
  'user@example.com',
  'user',
  'Assalamu Alaikum, I need help with...'
);

// Example 5: Ask AI
const analysis = await apiService.analyzeQuestion(
  'user@example.com',
  'How do I deal with anxiety in Islam?'
);
displayAyah(analysis.ayah);
displayHadith(analysis.hadith);
displayExplanation(analysis.explanation);

// Example 6: Search Videos
const videos = await apiService.searchVideos('prayer');

// Example 7: Log User Action
await apiService.logAction(
  'user@example.com',
  'dua_generated',
  { category: 'Fear & Anxiety' }
);
*/
