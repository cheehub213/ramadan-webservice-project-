import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom'
import { useState } from 'react'
import DuaGenerator from './pages/DuaGenerator'
import ChatWithImams from './pages/ChatWithImams'
import SearchImams from './pages/SearchImams'
import History from './pages/History'
import Home from './pages/Home'

function App() {
  const [language, setLanguage] = useState<'en' | 'ar'>('en')
  const [email, setEmail] = useState('')

  const toggleLanguage = () => {
    setLanguage(language === 'en' ? 'ar' : 'en')
  }

  return (
    <Router>
      <div className={language === 'ar' ? 'rtl' : 'ltr'}>
        {/* Navigation Header */}
        <header className="bg-gradient-to-r from-islamic to-islamic-light text-white shadow-lg">
          <div className="container flex justify-between items-center py-4">
            <Link to="/" className="text-2xl font-bold">
              {language === 'en' ? '🌙 Ramadan Helper' : '🌙 مساعد رمضان'}
            </Link>

            <nav className="flex gap-6 items-center">
              <Link
                to="/dua-generator"
                className="hover:text-gray-100 transition duration-200"
              >
                {language === 'en' ? 'Dua Generator' : 'منشئ الدعاء'}
              </Link>
              <Link
                to="/chat"
                className="hover:text-gray-100 transition duration-200"
              >
                {language === 'en' ? 'Chat' : 'الدردشة'}
              </Link>
              <Link
                to="/search-imams"
                className="hover:text-gray-100 transition duration-200"
              >
                {language === 'en' ? 'Find Imams' : 'البحث عن الأئمة'}
              </Link>
              <Link
                to="/history"
                className="hover:text-gray-100 transition duration-200"
              >
                {language === 'en' ? 'History' : 'السجل'}
              </Link>

              <button
                onClick={toggleLanguage}
                className="bg-white text-islamic px-3 py-1 rounded font-semibold hover:bg-gray-100"
              >
                {language === 'en' ? 'العربية' : 'English'}
              </button>
            </nav>
          </div>
        </header>

        {/* Main Content */}
        <main className="min-h-screen">
          <Routes>
            <Route path="/" element={<Home language={language} email={email} setEmail={setEmail} />} />
            <Route path="/dua-generator" element={<DuaGenerator language={language} email={email} />} />
            <Route path="/chat" element={<ChatWithImams language={language} email={email} />} />
            <Route path="/search-imams" element={<SearchImams language={language} />} />
            <Route path="/history" element={<History language={language} email={email} />} />
          </Routes>
        </main>

        {/* Footer */}
        <footer className="bg-gray-800 text-white text-center py-6 mt-12">
          <p>
            {language === 'en'
              ? '© 2024 Ramadan Helper. May Allah accept from us. Ameen.'
              : '© 2024 مساعد رمضان. يا ألله اقبل منا. آمين.'}
          </p>
        </footer>
      </div>
    </Router>
  )
}

export default App
