import { useState, useEffect } from 'react'
import { duaService } from '../services/api'

interface DuaGeneratorProps {
  language: 'en' | 'ar'
  email: string
}

interface Dua {
  id: string
  category: string
  context: string
  dua_text_en: string
  dua_text_ar: string
  how_to_use_en: string
  how_to_use_ar: string
  created_at: string
}

export default function DuaGenerator({ language, email }: DuaGeneratorProps) {
  const [categories, setCategories] = useState<string[]>([])
  const [selectedCategory, setSelectedCategory] = useState('')
  const [context, setContext] = useState('')
  const [loading, setLoading] = useState(false)
  const [generatedDua, setGeneratedDua] = useState<Dua | null>(null)
  const [error, setError] = useState('')

  useEffect(() => {
    fetchCategories()
  }, [])

  const fetchCategories = async () => {
    try {
      const data = await duaService.getCategories()
      setCategories(data.categories || [])
      if (data.categories && data.categories.length > 0) {
        setSelectedCategory(data.categories[0])
      }
    } catch (err) {
      setError('Failed to load categories')
      console.error(err)
    }
  }

  const handleGenerateDua = async () => {
    if (!email || !selectedCategory || !context) {
      setError(language === 'en' ? 'Please fill in all fields' : 'يرجى ملء جميع الحقول')
      return
    }

    setLoading(true)
    setError('')

    try {
      const response = await duaService.generateDua(email, selectedCategory, context)
      setGeneratedDua(response)
    } catch (err) {
      setError(language === 'en' ? 'Failed to generate dua' : 'فشل في إنشاء الدعاء')
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="container mx-auto py-12">
      <h1 className="text-4xl font-bold text-islamic mb-8 text-center">
        {language === 'en' ? 'Personalized Dua Generator' : 'منشئ الدعاء الشخصي'}
      </h1>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Input Form */}
        <div className="card">
          <h2 className="text-2xl font-bold text-islamic mb-6">
            {language === 'en' ? 'Tell us your need' : 'أخبرنا عن احتياجك'}
          </h2>

          {/* Category Selection */}
          <div className="mb-6">
            <label className="block text-sm font-semibold text-gray-700 mb-2">
              {language === 'en' ? 'Select Category' : 'اختر الفئة'}
            </label>
            <select
              value={selectedCategory}
              onChange={(e) => setSelectedCategory(e.target.value)}
              className="w-full px-4 py-2 border-2 border-gray-300 rounded-lg focus:outline-none focus:border-islamic"
            >
              {categories.map((cat) => (
                <option key={cat} value={cat}>
                  {cat}
                </option>
              ))}
            </select>
          </div>

          {/* Context Input */}
          <div className="mb-6">
            <label className="block text-sm font-semibold text-gray-700 mb-2">
              {language === 'en' ? 'Your Situation / Context' : 'وضعك / السياق'}
            </label>
            <textarea
              value={context}
              onChange={(e) => setContext(e.target.value)}
              placeholder={
                language === 'en'
                  ? 'Describe your situation in detail...'
                  : 'وصف وضعك بالتفصيل...'
              }
              rows={6}
              className="w-full px-4 py-2 border-2 border-gray-300 rounded-lg focus:outline-none focus:border-islamic resize-none"
            />
          </div>

          {/* Error Message */}
          {error && (
            <div className="mb-6 p-4 bg-red-100 border-2 border-red-500 text-red-700 rounded-lg">
              {error}
            </div>
          )}

          {/* Generate Button */}
          <button
            onClick={handleGenerateDua}
            disabled={loading}
            className={`w-full btn-primary disabled:opacity-50 disabled:cursor-not-allowed`}
          >
            {loading
              ? language === 'en'
                ? 'Generating...'
                : 'جاري التوليد...'
              : language === 'en'
              ? 'Generate My Dua'
              : 'توليد دعائي'}
          </button>
        </div>

        {/* Generated Dua Display */}
        {generatedDua && (
          <div className="card bg-gradient-to-br from-islamic-light to-white">
            <h2 className="text-2xl font-bold text-islamic mb-6">
              {language === 'en' ? 'Your Personalized Dua' : 'دعاؤك الشخصي'}
            </h2>

            {/* English Dua */}
            <div className="mb-8 p-4 bg-white rounded-lg border-l-4 border-islamic">
              <h3 className="font-semibold text-islamic mb-2">
                {language === 'en' ? '🇬🇧 English Dua' : '🇬🇧 الدعاء بالإنجليزية'}
              </h3>
              <p className="text-gray-800 text-lg mb-4 italic">
                {generatedDua.dua_text_en}
              </p>
              <p className="text-sm text-gray-600">
                <strong>{language === 'en' ? 'How to use: ' : 'كيفية الاستخدام: '}</strong>
                {generatedDua.how_to_use_en}
              </p>
            </div>

            {/* Arabic Dua */}
            <div className="mb-8 p-4 bg-white rounded-lg border-l-4 border-islamic text-right" dir="rtl">
              <h3 className="font-semibold text-islamic mb-2">
                {language === 'en' ? '🇸🇦 Arabic Dua' : '🇸🇦 الدعاء بالعربية'}
              </h3>
              <p className="text-gray-800 text-lg mb-4 leading-relaxed">
                {generatedDua.dua_text_ar}
              </p>
              <p className="text-sm text-gray-600">
                <strong>{language === 'en' ? 'كيفية الاستخدام: ' : 'طريقة الاستخدام: '}</strong>
                {generatedDua.how_to_use_ar}
              </p>
            </div>

            {/* Feedback Buttons */}
            <div className="flex gap-4">
              <button className="flex-1 btn-primary text-sm">
                {language === 'en' ? '👍 Helpful' : '👍 مفيد'}
              </button>
              <button className="flex-1 btn-secondary text-sm">
                {language === 'en' ? '👎 Not Helpful' : '👎 غير مفيد'}
              </button>
            </div>
          </div>
        )}
      </div>

      {/* Info Section */}
      <div className="mt-12 bg-blue-50 rounded-lg p-8">
        <h3 className="text-2xl font-bold text-islamic mb-4">
          {language === 'en' ? 'About This Dua' : 'حول هذا الدعاء'}
        </h3>
        <p className="text-gray-700">
          {language === 'en'
            ? 'This dua has been personalized using AI to address your specific situation while maintaining Islamic authenticity. Both English and Arabic versions are provided for your convenience. Make sincere dua with a focused heart and trust in Allah\'s wisdom.'
            : 'تم تخصيص هذا الدعاء باستخدام الذكاء الاصطناعي لمعالجة وضعك الخاص مع الحفاظ على الأصالة الإسلامية. تم توفير النسختين الإنجليزية والعربية لراحتك. ادع بإخلاص مع قلب مركز وثق بحكمة الله.'}
        </p>
      </div>
    </div>
  )
}
