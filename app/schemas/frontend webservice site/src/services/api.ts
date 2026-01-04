import axios, { AxiosInstance } from 'axios'

const API_BASE_URL = 'http://127.0.0.1:8001'

const api: AxiosInstance = axios.create({
  baseURL: `${API_BASE_URL}/api/v1`,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Dua Endpoints
export const duaService = {
  // Generate personalized dua in both English and Arabic
  generateDua: async (email: string, category: string, context: string) => {
    const response = await api.post('/dua/generate', {
      email,
      category,
      context,
    })
    return response.data
  },

  // Get dua history for user
  getDuaHistory: async (email: string) => {
    const response = await api.get(`/dua/history/${email}`)
    return response.data
  },

  // Get all dua categories
  getCategories: async () => {
    const response = await api.get('/dua/categories')
    return response.data
  },

  // Get single dua by ID
  getDuaById: async (id: string) => {
    const response = await api.get(`/dua/${id}`)
    return response.data
  },

  // Submit feedback on dua
  submitFeedback: async (duaId: string, email: string, helpful: boolean, notes: string = '') => {
    const response = await api.post('/dua/feedback', {
      dua_id: duaId,
      email,
      is_helpful: helpful,
      notes,
    })
    return response.data
  },

  // Get helpful duas statistics
  getHelpfulStats: async () => {
    const response = await api.get('/dua/stats/helpful')
    return response.data
  },
}

// Chat Endpoints
export const chatService = {
  // Create new conversation
  createConversation: async (email: string, imamId: string, topic: string) => {
    const response = await api.post('/chat/conversations', {
      user_email: email,
      imam_id: imamId,
      topic,
    })
    return response.data
  },

  // Get user conversations
  getUserConversations: async (email: string) => {
    const response = await api.get(`/chat/conversations/user/${email}`)
    return response.data
  },

  // Get specific conversation
  getConversation: async (conversationId: string) => {
    const response = await api.get(`/chat/conversations/${conversationId}`)
    return response.data
  },

  // Send message
  sendMessage: async (conversationId: string, message: string, senderType: 'user' | 'imam') => {
    const response = await api.post(`/chat/conversations/${conversationId}/messages`, {
      message,
      sender_type: senderType,
    })
    return response.data
  },

  // Get messages for conversation
  getMessages: async (conversationId: string) => {
    const response = await api.get(`/chat/conversations/${conversationId}/messages`)
    return response.data
  },

  // Mark messages as read
  markMessagesAsRead: async (messageIds: string[]) => {
    const response = await api.put('/chat/messages/read', {
      message_ids: messageIds,
    })
    return response.data
  },

  // Set imam availability
  setImamAvailability: async (imamId: string, isAvailable: boolean) => {
    const response = await api.put(`/chat/imam/${imamId}/availability`, {
      is_available: isAvailable,
    })
    return response.data
  },

  // Get imam availability
  getImamAvailability: async (imamId: string) => {
    const response = await api.get(`/chat/imam/${imamId}/availability`)
    return response.data
  },
}

// Search Endpoints (for Quran and Hadith)
export const searchService = {
  // Search Quran
  searchQuran: async (query: string, language: 'en' | 'ar' = 'en') => {
    const response = await api.get('/search/quran', {
      params: { query, language },
    })
    return response.data
  },

  // Search Hadith
  searchHadith: async (query: string, language: 'en' | 'ar' = 'en') => {
    const response = await api.get('/search/hadith', {
      params: { query, language },
    })
    return response.data
  },
}

// Imam Endpoints
export const imamService = {
  // Get all imams
  getImams: async () => {
    const response = await api.get('/imam/list')
    return response.data
  },

  // Get imam by ID
  getImamById: async (imamId: string) => {
    const response = await api.get(`/imam/${imamId}`)
    return response.data
  },

  // Register new imam
  registerImam: async (name: string, email: string, expertise: string) => {
    const response = await api.post('/imam/register', {
      name,
      email,
      expertise,
    })
    return response.data
  },
}

export default api
