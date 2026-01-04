import { useNavigate } from 'react-router-dom'

interface HomeProps {
  language: 'en' | 'ar'
  email: string
  setEmail: (email: string) => void
}

export default function Home({ language, email, setEmail }: HomeProps) {
  const navigate = useNavigate()

  const handleGetStarted = () => {
    if (email) {
      navigate('/dua-generator')
    }
  }

  return (
    <div className="container mx-auto py-12">
      {/* Hero Section */}
      <div className="text-center mb-12">
        <h1 className="text-5xl font-bold text-islamic mb-4">
          {language === 'en'
            ? 'Welcome to Ramadan Helper'
            : 'مرحبا بك في مساعد رمضان'}
        </h1>
        <p className="text-xl text-gray-600 mb-8">
          {language === 'en'
            ? 'Your personal Islamic companion for duas, guidance, and spiritual connection'
            : 'رفيقك الإسلامي الشخصي للأدعية والإرشاد والتواصل الروحي'}
        </p>

        {/* Email Input */}
        <div className="flex gap-2 justify-center mb-8">
          <input
            type="email"
            placeholder={language === 'en' ? 'Enter your email' : 'أدخل بريدك الإلكتروني'}
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            className="px-4 py-3 border-2 border-gray-300 rounded-lg w-64 focus:outline-none focus:border-islamic"
          />
          <button
            onClick={handleGetStarted}
            disabled={!email}
            className="btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {language === 'en' ? 'Get Started' : 'ابدأ الآن'}
          </button>
        </div>
      </div>

      {/* Features Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12">
        {/* Dua Generator Card */}
        <div className="card cursor-pointer hover:scale-105 transform transition"
          onClick={() => email && navigate('/dua-generator')}
        >
          <div className="text-4xl mb-4">📿</div>
          <h2 className="text-2xl font-bold text-islamic mb-3">
            {language === 'en' ? 'Dua Generator' : 'منشئ الدعاء'}
          </h2>
          <p className="text-gray-600">
            {language === 'en'
              ? 'Get personalized duas for your specific needs and concerns in English and Arabic'
              : 'احصل على أدعية مخصصة لاحتياجاتك الخاصة باللغة الإنجليزية والعربية'}
          </p>
        </div>

        {/* Chat Card */}
        <div className="card cursor-pointer hover:scale-105 transform transition"
          onClick={() => email && navigate('/chat')}
        >
          <div className="text-4xl mb-4">💬</div>
          <h2 className="text-2xl font-bold text-islamic mb-3">
            {language === 'en' ? 'Chat with Imams' : 'الحوار مع الأئمة'}
          </h2>
          <p className="text-gray-600">
            {language === 'en'
              ? 'Ask questions and receive guidance from learned Islamic scholars'
              : 'اطرح أسئلتك واحصل على إرشادات من العلماء الإسلاميين المتعلمين'}
          </p>
        </div>

        {/* Find Imams Card */}
        <div className="card cursor-pointer hover:scale-105 transform transition"
          onClick={() => email && navigate('/search-imams')}
        >
          <div className="text-4xl mb-4">🕌</div>
          <h2 className="text-2xl font-bold text-islamic mb-3">
            {language === 'en' ? 'Find Imams' : 'البحث عن الأئمة'}
          </h2>
          <p className="text-gray-600">
            {language === 'en'
              ? 'Connect with experienced Islamic scholars in your area'
              : 'تواصل مع العلماء الإسلاميين ذوي الخبرة في منطقتك'}
          </p>
        </div>
      </div>

      {/* About Section */}
      <div className="bg-islamic bg-opacity-10 rounded-lg p-8 mb-12">
        <h2 className="text-3xl font-bold text-islamic mb-4">
          {language === 'en' ? 'About Ramadan Helper' : 'حول مساعد رمضان'}
        </h2>
        <p className="text-gray-700 mb-4">
          {language === 'en'
            ? 'Ramadan Helper is designed to support your spiritual journey during the blessed month of Ramadan and throughout the year. We combine the wisdom of Islamic scholarship with modern technology to provide personalized guidance.'
            : 'تم تصميم مساعد رمضان لدعم رحلتك الروحية خلال الشهر الكريم وطوال السنة. نحن نجمع بين حكمة العلماء الإسلاميين والتكنولوجيا الحديثة لتقديم إرشادات شخصية.'}
        </p>
        <p className="text-gray-700">
          {language === 'en'
            ? 'Whether you need spiritual guidance, personalized duas, or want to connect with Islamic scholars, we are here to help you make the most of your Ramadan experience.'
            : 'سواء كنت تحتاج إلى إرشادات روحية أو أدعية شخصية أو تريد التواصل مع العلماء الإسلاميين، فنحن هنا لمساعدتك على تحقيق أقصى استفادة من تجربة رمضان الخاصة بك.'}
        </p>
      </div>
    </div>
  )
}
