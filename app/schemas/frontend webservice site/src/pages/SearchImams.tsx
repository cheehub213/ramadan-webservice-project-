import { useState, useEffect } from 'react'
import { imamService } from '../services/api'

interface SearchImamsProps {
  language: 'en' | 'ar'
}

interface Imam {
  id: string
  name: string
  email: string
  expertise: string
  is_available: boolean
}

export default function SearchImams({ language }: SearchImamsProps) {
  const [imams, setImams] = useState<Imam[]>([])
  const [searchTerm, setSearchTerm] = useState('')
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    fetchImams()
  }, [])

  const fetchImams = async () => {
    try {
      setLoading(true)
      const data = await imamService.getImams()
      setImams(Array.isArray(data) ? data : data.imams || [])
    } catch (err) {
      setError(language === 'en' ? 'Failed to load imams' : 'فشل تحميل الأئمة')
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  const filteredImams = imams.filter(
    (imam) =>
      imam.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      imam.expertise.toLowerCase().includes(searchTerm.toLowerCase())
  )

  return (
    <div className="container mx-auto py-12">
      <h1 className="text-4xl font-bold text-islamic mb-8 text-center">
        {language === 'en' ? 'Find Islamic Scholars' : 'البحث عن العلماء الإسلاميين'}
      </h1>

      {/* Search Bar */}
      <div className="mb-8">
        <input
          type="text"
          placeholder={
            language === 'en'
              ? 'Search by name or expertise...'
              : 'ابحث حسب الاسم أو التخصص...'
          }
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          className="w-full px-6 py-3 border-2 border-gray-300 rounded-lg text-lg focus:outline-none focus:border-islamic"
        />
      </div>

      {error && (
        <div className="mb-8 p-4 bg-red-100 border-2 border-red-500 text-red-700 rounded-lg">
          {error}
        </div>
      )}

      {loading ? (
        <div className="text-center py-12">
          <p className="text-gray-600">
            {language === 'en' ? 'Loading scholars...' : 'جاري تحميل العلماء...'}
          </p>
        </div>
      ) : filteredImams.length === 0 ? (
        <div className="text-center py-12">
          <p className="text-gray-600">
            {language === 'en'
              ? 'No scholars found matching your search'
              : 'لم يتم العثور على علماء يطابقون بحثك'}
          </p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredImams.map((imam) => (
            <div key={imam.id} className="card">
              <div className="flex items-start justify-between mb-4">
                <div>
                  <h3 className="text-xl font-bold text-islamic">{imam.name}</h3>
                  <p className="text-sm text-gray-600">{imam.email}</p>
                </div>
                <div
                  className={`px-3 py-1 rounded-full text-sm font-semibold ${
                    imam.is_available
                      ? 'bg-green-100 text-green-800'
                      : 'bg-gray-100 text-gray-800'
                  }`}
                >
                  {imam.is_available
                    ? language === 'en' ? '🟢 Available' : '🟢 متاح'
                    : language === 'en' ? '⚫ Offline' : '⚫ غير متصل'}
                </div>
              </div>

              <div className="mb-6">
                <h4 className="font-semibold text-gray-700 mb-2">
                  {language === 'en' ? 'Expertise' : 'التخصص'}
                </h4>
                <p className="text-gray-600">{imam.expertise}</p>
              </div>

              <button className="w-full btn-primary">
                {language === 'en' ? 'Chat Now' : 'ابدأ الحوار'}
              </button>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
