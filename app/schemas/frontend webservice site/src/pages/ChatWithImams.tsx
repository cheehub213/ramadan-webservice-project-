import { useState, useEffect } from 'react'
import { chatService, imamService } from '../services/api'

interface ChatWithImamsProps {
  language: 'en' | 'ar'
  email: string
}

interface Imam {
  id: string
  name: string
  email: string
  expertise: string
  is_available: boolean
}

interface Message {
  id: string
  conversation_id: string
  message: string
  sender_type: 'user' | 'imam'
  created_at: string
  is_read: boolean
}

interface Conversation {
  id: string
  user_email: string
  imam_id: string
  topic: string
  created_at: string
  updated_at: string
  messages: Message[]
}

export default function ChatWithImams({ language, email }: ChatWithImamsProps) {
  const [imams, setImams] = useState<Imam[]>([])
  const [conversations, setConversations] = useState<Conversation[]>([])
  const [selectedImam, setSelectedImam] = useState<string | null>(null)
  const [selectedConversation, setSelectedConversation] = useState<Conversation | null>(null)
  const [newMessage, setNewMessage] = useState('')
  const [topic, setTopic] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  useEffect(() => {
    fetchImams()
    if (email) {
      fetchConversations()
    }
  }, [email])

  const fetchImams = async () => {
    try {
      const data = await imamService.getImams()
      setImams(Array.isArray(data) ? data : data.imams || [])
    } catch (err) {
      setError('Failed to load imams')
      console.error(err)
    }
  }

  const fetchConversations = async () => {
    try {
      const data = await chatService.getUserConversations(email)
      setConversations(Array.isArray(data) ? data : data.conversations || [])
    } catch (err) {
      setError('Failed to load conversations')
      console.error(err)
    }
  }

  const handleStartConversation = async () => {
    if (!selectedImam || !topic) {
      setError(language === 'en' ? 'Please select an imam and enter a topic' : 'يرجى اختيار إمام وإدخال موضوع')
      return
    }

    setLoading(true)
    try {
      const response = await chatService.createConversation(email, selectedImam, topic)
      setSelectedConversation(response)
      setTopic('')
      await fetchConversations()
    } catch (err) {
      setError('Failed to start conversation')
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  const handleSendMessage = async () => {
    if (!selectedConversation || !newMessage.trim()) return

    setLoading(true)
    try {
      const response = await chatService.sendMessage(
        selectedConversation.id,
        newMessage,
        'user'
      )
      setNewMessage('')
      // Refresh conversation
      const updated = await chatService.getConversation(selectedConversation.id)
      setSelectedConversation(updated)
    } catch (err) {
      setError('Failed to send message')
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="container mx-auto py-12">
      <h1 className="text-4xl font-bold text-islamic mb-8 text-center">
        {language === 'en' ? 'Chat with Islamic Scholars' : 'الحوار مع العلماء الإسلاميين'}
      </h1>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Imams List and Chat History */}
        <div className="lg:col-span-1 space-y-6">
          {/* Available Imams */}
          <div className="card">
            <h2 className="text-xl font-bold text-islamic mb-4">
              {language === 'en' ? 'Available Imams' : 'الأئمة المتاحون'}
            </h2>

            {imams.length === 0 ? (
              <p className="text-gray-600">
                {language === 'en' ? 'No imams available' : 'لا توجد أئمة متاحة'}
              </p>
            ) : (
              <div className="space-y-3">
                {imams.map((imam) => (
                  <div
                    key={imam.id}
                    onClick={() => setSelectedImam(imam.id)}
                    className={`p-3 rounded-lg cursor-pointer transition ${
                      selectedImam === imam.id
                        ? 'bg-islamic text-white'
                        : 'bg-gray-100 hover:bg-gray-200'
                    }`}
                  >
                    <div className="font-semibold">{imam.name}</div>
                    <div className="text-sm">
                      {imam.is_available ? (
                        <span className="text-green-600">● {language === 'en' ? 'Available' : 'متاح'}</span>
                      ) : (
                        <span className="text-red-600">● {language === 'en' ? 'Offline' : 'غير متصل'}</span>
                      )}
                    </div>
                    <div className="text-xs opacity-75 mt-1">{imam.expertise}</div>
                  </div>
                ))}
              </div>
            )}
          </div>

          {/* Previous Conversations */}
          <div className="card">
            <h2 className="text-xl font-bold text-islamic mb-4">
              {language === 'en' ? 'Your Conversations' : 'محادثاتك'}
            </h2>

            {conversations.length === 0 ? (
              <p className="text-gray-600">
                {language === 'en' ? 'No conversations yet' : 'لا توجد محادثات حتى الآن'}
              </p>
            ) : (
              <div className="space-y-2">
                {conversations.map((conv) => (
                  <button
                    key={conv.id}
                    onClick={() => setSelectedConversation(conv)}
                    className={`w-full text-left p-3 rounded-lg transition ${
                      selectedConversation?.id === conv.id
                        ? 'bg-islamic text-white'
                        : 'bg-gray-100 hover:bg-gray-200'
                    }`}
                  >
                    <div className="font-semibold truncate">{conv.topic}</div>
                    <div className="text-xs opacity-75">
                      {new Date(conv.created_at).toLocaleDateString()}
                    </div>
                  </button>
                ))}
              </div>
            )}
          </div>
        </div>

        {/* Chat Area */}
        <div className="lg:col-span-2 card flex flex-col h-[600px]">
          {selectedConversation ? (
            <>
              {/* Messages */}
              <div className="flex-1 overflow-y-auto mb-6 space-y-4 p-4 bg-gray-50 rounded">
                {selectedConversation.messages?.length === 0 ? (
                  <p className="text-center text-gray-600 py-8">
                    {language === 'en' ? 'No messages yet. Start the conversation!' : 'لا توجد رسائل حتى الآن. ابدأ المحادثة!'}
                  </p>
                ) : (
                  selectedConversation.messages?.map((msg) => (
                    <div
                      key={msg.id}
                      className={`flex ${msg.sender_type === 'user' ? 'justify-end' : 'justify-start'}`}
                    >
                      <div
                        className={`max-w-xs lg:max-w-md px-4 py-2 rounded-lg ${
                          msg.sender_type === 'user'
                            ? 'bg-islamic text-white'
                            : 'bg-gray-300 text-gray-800'
                        }`}
                      >
                        <p>{msg.message}</p>
                        <p className="text-xs opacity-75 mt-1">
                          {new Date(msg.created_at).toLocaleTimeString()}
                        </p>
                      </div>
                    </div>
                  ))
                )}
              </div>

              {/* Message Input */}
              <div className="flex gap-2">
                <input
                  type="text"
                  value={newMessage}
                  onChange={(e) => setNewMessage(e.target.value)}
                  onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
                  placeholder={language === 'en' ? 'Type your message...' : 'اكتب رسالتك...'}
                  className="flex-1 px-4 py-2 border-2 border-gray-300 rounded-lg focus:outline-none focus:border-islamic"
                />
                <button
                  onClick={handleSendMessage}
                  disabled={loading}
                  className="btn-primary disabled:opacity-50"
                >
                  {language === 'en' ? 'Send' : 'أرسل'}
                </button>
              </div>
            </>
          ) : (
            <div className="flex flex-col gap-6">
              <h2 className="text-2xl font-bold text-islamic">
                {language === 'en' ? 'Start New Conversation' : 'ابدأ محادثة جديدة'}
              </h2>

              {error && (
                <div className="p-4 bg-red-100 border-2 border-red-500 text-red-700 rounded-lg">
                  {error}
                </div>
              )}

              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-2">
                  {language === 'en' ? 'Select Imam' : 'اختر إمام'}
                </label>
                <select
                  value={selectedImam || ''}
                  onChange={(e) => setSelectedImam(e.target.value)}
                  className="w-full px-4 py-2 border-2 border-gray-300 rounded-lg focus:outline-none focus:border-islamic"
                >
                  <option value="">{language === 'en' ? 'Choose an imam...' : 'اختر إماماً...'}</option>
                  {imams.map((imam) => (
                    <option key={imam.id} value={imam.id}>
                      {imam.name}
                    </option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-2">
                  {language === 'en' ? 'Topic' : 'الموضوع'}
                </label>
                <input
                  type="text"
                  value={topic}
                  onChange={(e) => setTopic(e.target.value)}
                  placeholder={language === 'en' ? 'What would you like to discuss?' : 'ما الذي تود مناقشته؟'}
                  className="w-full px-4 py-2 border-2 border-gray-300 rounded-lg focus:outline-none focus:border-islamic"
                />
              </div>

              <button
                onClick={handleStartConversation}
                disabled={loading}
                className="btn-primary disabled:opacity-50"
              >
                {loading
                  ? language === 'en' ? 'Starting...' : 'جاري البدء...'
                  : language === 'en' ? 'Start Conversation' : 'ابدأ المحادثة'}
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
