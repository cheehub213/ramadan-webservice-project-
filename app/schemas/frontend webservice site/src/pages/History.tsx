import { useState, useEffect } from 'react'
import { duaService } from '../services/api'

interface HistoryProps {
  language: 'en' | 'ar'
  email: string
}

interface HistoryDua {
  id: string
  category: string
  context: string
  generated_dua_en: string
  generated_dua_ar: string
  is_helpful: boolean | null
  feedback_notes: string
  created_at: string
}

export default function History({ language, email }: HistoryProps) {
  const [history, setHistory] = useState<HistoryDua[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [filterByHelpful, setFilterByHelpful] = useState<'all' | 'helpful' | 'not-helpful'>('all')

  useEffect(() => {
    if (email) {
      fetchHistory()
    }
  }, [email])

  const fetchHistory = async () => {
    try {
      setLoading(true)
      const data = await duaService.getDuaHistory(email)
      setHistory(Array.isArray(data) ? data : data.history || [])
    } catch (err) {
      setError(language === 'en' ? 'Failed to load history' : 'فشل تحميل السجل')
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  const filteredHistory = history.filter((item) => {
    if (filterByHelpful === 'all') return true
    if (filterByHelpful === 'helpful') return item.is_helpful === true
    if (filterByHelpful === 'not-helpful') return item.is_helpful === false
    return true
  })

  return (
    <div className="container mx-auto py-12">
      <h1 className="text-4xl font-bold text-islamic mb-8 text-center">
        {language === 'en' ? 'Your Dua History' : 'سجل أدعيتك'}
      </h1>

      {/* Filter Buttons */}
      <div className="flex gap-4 mb-8 justify-center flex-wrap">
        <button
          onClick={() => setFilterByHelpful('all')}
          className={`px-6 py-2 rounded-lg font-semibold transition ${
            filterByHelpful === 'all'
              ? 'bg-islamic text-white'
              : 'bg-gray-200 text-gray-800 hover:bg-gray-300'
          }`}
        >
          {language === 'en' ? 'All' : 'الكل'}
        </button>
        <button
          onClick={() => setFilterByHelpful('helpful')}
          className={`px-6 py-2 rounded-lg font-semibold transition ${
            filterByHelpful === 'helpful'
              ? 'bg-green-600 text-white'
              : 'bg-gray-200 text-gray-800 hover:bg-gray-300'
          }`}
        >
          {language === 'en' ? '👍 Helpful' : '👍 مفيد'}
        </button>
        <button
          onClick={() => setFilterByHelpful('not-helpful')}
          className={`px-6 py-2 rounded-lg font-semibold transition ${
            filterByHelpful === 'not-helpful'
              ? 'bg-red-600 text-white'
              : 'bg-gray-200 text-gray-800 hover:bg-gray-300'
          }`}
        >
          {language === 'en' ? '👎 Not Helpful' : '👎 غير مفيد'}
        </button>
      </div>

      {error && (
        <div className="mb-8 p-4 bg-red-100 border-2 border-red-500 text-red-700 rounded-lg">
          {error}
        </div>
      )}

      {loading ? (
        <div className="text-center py-12">
          <p className="text-gray-600">
            {language === 'en' ? 'Loading your history...' : 'جاري تحميل سجلك...'}
          </p>
        </div>
      ) : filteredHistory.length === 0 ? (
        <div className="text-center py-12 card">
          <p className="text-gray-600 text-lg">
            {language === 'en'
              ? 'No duas found in your history'
              : 'لم يتم العثور على أدعية في سجلك'}
          </p>
          <p className="text-gray-500 mt-2">
            {language === 'en'
              ? 'Start by generating a new dua'
              : 'ابدأ بإنشاء دعاء جديد'}
          </p>
        </div>
      ) : (
        <div className="space-y-6">
          {filteredHistory.map((item, index) => (
            <div key={item.id} className="card">
              {/* Header with Category and Date */}
              <div className="flex justify-between items-start mb-4">
                <div>
                  <h3 className="text-2xl font-bold text-islamic">{item.category}</h3>
                  <p className="text-sm text-gray-600">
                    {new Date(item.created_at).toLocaleDateString(
                      language === 'en' ? 'en-US' : 'ar-SA'
                    )}
                  </p>
                </div>
                {item.is_helpful !== null && (
                  <div
                    className={`px-4 py-2 rounded-lg font-semibold ${
                      item.is_helpful
                        ? 'bg-green-100 text-green-800'
                        : 'bg-red-100 text-red-800'
                    }`}
                  >
                    {item.is_helpful
                      ? language === 'en' ? '👍 Helpful' : '👍 مفيد'
                      : language === 'en' ? '👎 Not Helpful' : '👎 غير مفيد'}
                  </div>
                )}
              </div>

              {/* Context */}
              <div className="mb-6 p-4 bg-gray-50 rounded-lg">
                <h4 className="font-semibold text-gray-700 mb-2">
                  {language === 'en' ? 'Your Context' : 'سياقك'}
                </h4>
                <p className="text-gray-600">{item.context}</p>
              </div>

              {/* English Dua */}
              <div className="mb-6 p-4 bg-blue-50 rounded-lg border-l-4 border-blue-400">
                <h4 className="font-semibold text-blue-900 mb-2">
                  {language === 'en' ? '🇬🇧 English Dua' : '🇬🇧 الدعاء بالإنجليزية'}
                </h4>
                <p className="text-gray-800 italic leading-relaxed">
                  {item.generated_dua_en}
                </p>
              </div>

              {/* Arabic Dua */}
              <div className="mb-6 p-4 bg-green-50 rounded-lg border-l-4 border-green-400 text-right" dir="rtl">
                <h4 className="font-semibold text-green-900 mb-2">
                  {language === 'en' ? '🇸🇦 Arabic Dua' : '🇸🇦 الدعاء بالعربية'}
                </h4>
                <p className="text-gray-800 leading-relaxed">
                  {item.generated_dua_ar}
                </p>
              </div>

              {/* Feedback Notes */}
              {item.feedback_notes && (
                <div className="p-4 bg-yellow-50 rounded-lg border-l-4 border-yellow-400">
                  <h4 className="font-semibold text-yellow-900 mb-2">
                    {language === 'en' ? 'Your Notes' : 'ملاحظاتك'}
                  </h4>
                  <p className="text-gray-800">{item.feedback_notes}</p>
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
