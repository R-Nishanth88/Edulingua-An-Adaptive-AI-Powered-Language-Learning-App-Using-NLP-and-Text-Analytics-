import { Link, useNavigate } from 'react-router-dom'
import { BookOpen, LogOut, User, Moon, Sun } from 'lucide-react'
import { getBadges } from '../services/api'
import { useState, useEffect } from 'react'
import { useDarkMode } from '../App'

export default function Navbar({ user, setUser }) {
  const { darkMode, setDarkMode } = useDarkMode()
  const navigate = useNavigate()
  const [badges, setBadges] = useState([])
  const [showDropdown, setShowDropdown] = useState(false)

  useEffect(() => {
    if (user) {
      fetchBadges()
    }
  }, [user])

  const fetchBadges = async () => {
    try {
      const response = await getBadges()
      setBadges(response.data.badges || [])
    } catch (error) {
      console.error('Error fetching badges:', error)
    }
  }

  const handleLogout = () => {
    localStorage.removeItem('token')
    setUser(null)
    navigate('/')
  }

  return (
    <nav className="bg-white/95 dark:bg-gray-800/95 backdrop-blur-xl shadow-lg border-b border-gray-200/50 dark:border-gray-700/50 transition-all duration-300 sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Logo */}
          <Link to="/" className="flex items-center space-x-2 group">
            <div className="relative">
              <BookOpen className="w-8 h-8 text-primary-600 dark:text-blue-400 transform group-hover:rotate-12 transition-transform duration-300" />
              <div className="absolute inset-0 bg-blue-500/20 rounded-full blur-lg opacity-0 group-hover:opacity-100 transition-opacity"></div>
            </div>
            <span className="text-xl font-bold bg-gradient-to-r from-blue-600 via-purple-600 to-pink-600 bg-clip-text text-transparent dark:from-blue-400 dark:via-purple-400 dark:to-pink-400">
              EduLingua Pro
            </span>
          </Link>

          {/* Navigation */}
          {user ? (
            <div className="flex items-center space-x-6">
              <Link
                to="/dashboard"
                className="text-gray-700 dark:text-gray-300 hover:text-blue-600 dark:hover:text-blue-400 font-semibold transition-all duration-200 hover:scale-105 relative group"
              >
                Dashboard
                <span className="absolute bottom-0 left-0 w-0 h-0.5 bg-gradient-to-r from-blue-600 to-purple-600 group-hover:w-full transition-all duration-300"></span>
              </Link>
              <Link
                to="/chatbot"
                className="text-gray-700 dark:text-gray-300 hover:text-purple-600 dark:hover:text-purple-400 font-semibold transition-all duration-200 hover:scale-105 relative group"
              >
                Chatbot
                <span className="absolute bottom-0 left-0 w-0 h-0.5 bg-gradient-to-r from-purple-600 to-pink-600 group-hover:w-full transition-all duration-300"></span>
              </Link>
              <Link
                to="/progress"
                className="text-gray-700 dark:text-gray-300 hover:text-green-600 dark:hover:text-green-400 font-semibold transition-all duration-200 hover:scale-105 relative group"
              >
                Progress
                <span className="absolute bottom-0 left-0 w-0 h-0.5 bg-gradient-to-r from-green-600 to-emerald-600 group-hover:w-full transition-all duration-300"></span>
              </Link>
              <Link
                to="/evaluation"
                className="text-gray-700 dark:text-gray-300 hover:text-cyan-600 dark:hover:text-cyan-400 font-semibold transition-all duration-200 hover:scale-105 relative group"
              >
                Metrics
                <span className="absolute bottom-0 left-0 w-0 h-0.5 bg-gradient-to-r from-cyan-600 to-blue-600 group-hover:w-full transition-all duration-300"></span>
              </Link>
              <Link
                to="/vocabulary"
                className="text-gray-700 dark:text-gray-300 hover:text-pink-600 dark:hover:text-pink-400 font-semibold transition-all duration-200 hover:scale-105 relative group"
              >
                Vocabulary
                <span className="absolute bottom-0 left-0 w-0 h-0.5 bg-gradient-to-r from-pink-600 to-red-600 group-hover:w-full transition-all duration-300"></span>
              </Link>
              
              {/* Advanced Features Dropdown */}
              <div className="relative group">
                <button className="text-gray-700 dark:text-gray-300 hover:text-purple-600 dark:hover:text-purple-400 font-semibold transition-all duration-200 hover:scale-105 flex items-center bg-gradient-to-r from-purple-50 to-pink-50 dark:from-purple-900/20 dark:to-pink-900/20 px-4 py-2 rounded-xl border border-purple-200/50 dark:border-purple-700/30">
                  ✨ Advanced
                  <svg className="ml-1 w-4 h-4 transform group-hover:rotate-180 transition-transform duration-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                  </svg>
                </button>
                <div className="absolute left-0 mt-2 w-80 bg-white/95 dark:bg-gray-800/95 backdrop-blur-xl rounded-2xl shadow-2xl opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all duration-300 z-50 border border-gray-200/50 dark:border-gray-700/50 max-h-96 overflow-y-auto">
                  <div className="py-2">
                    <div className="px-4 py-2 text-xs font-bold text-blue-600 dark:text-blue-400 uppercase tracking-wider bg-gradient-to-r from-blue-50 to-purple-50 dark:from-blue-900/20 dark:to-purple-900/20 mx-2 rounded-lg mb-1">🤖 AI Features</div>
                    <Link to="/quality-score" className="block px-4 py-2.5 text-sm text-gray-700 dark:text-gray-300 hover:bg-gradient-to-r hover:from-blue-50 hover:to-purple-50 dark:hover:from-blue-900/20 dark:hover:to-purple-900/20 transition-all duration-200 hover:translate-x-2 rounded-lg mx-2">📊 Writing Quality Score</Link>
                    <Link to="/tone-transfer" className="block px-4 py-2.5 text-sm text-gray-700 dark:text-gray-300 hover:bg-gradient-to-r hover:from-purple-50 hover:to-pink-50 dark:hover:from-purple-900/20 dark:hover:to-pink-900/20 transition-all duration-200 hover:translate-x-2 rounded-lg mx-2">🎨 Tone Transfer</Link>
                    <Link to="/contextual-correction" className="block px-4 py-2.5 text-sm text-gray-700 dark:text-gray-300 hover:bg-gradient-to-r hover:from-cyan-50 hover:to-blue-50 dark:hover:from-cyan-900/20 dark:hover:to-blue-900/20 transition-all duration-200 hover:translate-x-2 rounded-lg mx-2">📝 Contextual Correction</Link>
                    <Link to="/summarize-review" className="block px-4 py-2.5 text-sm text-gray-700 dark:text-gray-300 hover:bg-gradient-to-r hover:from-green-50 hover:to-emerald-50 dark:hover:from-green-900/20 dark:hover:to-emerald-900/20 transition-all duration-200 hover:translate-x-2 rounded-lg mx-2">📄 Summarize & Review</Link>
                    <div className="border-t border-gray-200/50 dark:border-gray-700/50 my-2 mx-2"></div>
                    <div className="px-4 py-2 text-xs font-bold text-purple-600 dark:text-purple-400 uppercase tracking-wider bg-gradient-to-r from-purple-50 to-pink-50 dark:from-purple-900/20 dark:to-pink-900/20 mx-2 rounded-lg mb-1">📚 Learning</div>
                    <Link to="/grammar-lessons" className="block px-4 py-2.5 text-sm text-gray-700 dark:text-gray-300 hover:bg-gradient-to-r hover:from-yellow-50 hover:to-orange-50 dark:hover:from-yellow-900/20 dark:hover:to-orange-900/20 transition-all duration-200 hover:translate-x-2 rounded-lg mx-2">📖 Grammar Lessons</Link>
                    <Link to="/grammar-drills" className="block px-4 py-2.5 text-sm text-gray-700 dark:text-gray-300 hover:bg-gradient-to-r hover:from-orange-50 hover:to-red-50 dark:hover:from-orange-900/20 dark:hover:to-red-900/20 transition-all duration-200 hover:translate-x-2 rounded-lg mx-2">🎯 Grammar Drills</Link>
                    <Link to="/daily-challenges" className="block px-4 py-2.5 text-sm text-gray-700 dark:text-gray-300 hover:bg-gradient-to-r hover:from-pink-50 hover:to-rose-50 dark:hover:from-pink-900/20 dark:hover:to-rose-900/20 transition-all duration-200 hover:translate-x-2 rounded-lg mx-2">🔥 Daily Challenges</Link>
                    <div className="border-t border-gray-200/50 dark:border-gray-700/50 my-2 mx-2"></div>
                    <div className="px-4 py-2 text-xs font-bold text-green-600 dark:text-green-400 uppercase tracking-wider bg-gradient-to-r from-green-50 to-emerald-50 dark:from-green-900/20 dark:to-emerald-900/20 mx-2 rounded-lg mb-1">⚡ Advanced</div>
                    <Link to="/dialog" className="block px-4 py-2.5 text-sm text-gray-700 dark:text-gray-300 hover:bg-gradient-to-r hover:from-blue-50 hover:to-cyan-50 dark:hover:from-blue-900/20 dark:hover:to-cyan-900/20 transition-all duration-200 hover:translate-x-2 rounded-lg mx-2">💬 Dialog Practice</Link>
                    <Link to="/error-patterns" className="block px-4 py-2.5 text-sm text-gray-700 dark:text-gray-300 hover:bg-gradient-to-r hover:from-red-50 hover:to-pink-50 dark:hover:from-red-900/20 dark:hover:to-pink-900/20 transition-all duration-200 hover:translate-x-2 rounded-lg mx-2">📈 Error Patterns</Link>
                    <Link to="/difficulty" className="block px-4 py-2.5 text-sm text-gray-700 dark:text-gray-300 hover:bg-gradient-to-r hover:from-indigo-50 hover:to-purple-50 dark:hover:from-indigo-900/20 dark:hover:to-purple-900/20 transition-all duration-200 hover:translate-x-2 rounded-lg mx-2">🎚️ Adaptive Difficulty</Link>
                    <Link to="/writing-style" className="block px-4 py-2.5 text-sm text-gray-700 dark:text-gray-300 hover:bg-gradient-to-r hover:from-teal-50 hover:to-cyan-50 dark:hover:from-teal-900/20 dark:hover:to-cyan-900/20 transition-all duration-200 hover:translate-x-2 rounded-lg mx-2">✍️ Writing Style</Link>
                    <Link to="/essay-scorer" className="block px-4 py-2.5 text-sm text-gray-700 dark:text-gray-300 hover:bg-gradient-to-r hover:from-amber-50 hover:to-yellow-50 dark:hover:from-amber-900/20 dark:hover:to-yellow-900/20 transition-all duration-200 hover:translate-x-2 rounded-lg mx-2">📝 Essay Scorer</Link>
                    <Link to="/learning-path" className="block px-4 py-2.5 text-sm text-gray-700 dark:text-gray-300 hover:bg-gradient-to-r hover:from-violet-50 hover:to-purple-50 dark:hover:from-violet-900/20 dark:hover:to-purple-900/20 transition-all duration-200 hover:translate-x-2 rounded-lg mx-2">🗺️ Learning Path</Link>
                    <Link to="/plagiarism" className="block px-4 py-2.5 text-sm text-gray-700 dark:text-gray-300 hover:bg-gradient-to-r hover:from-rose-50 hover:to-red-50 dark:hover:from-rose-900/20 dark:hover:to-red-900/20 transition-all duration-200 hover:translate-x-2 rounded-lg mx-2">🔍 Plagiarism Checker</Link>
                  </div>
                </div>
              </div>
              
              {/* Dark Mode Toggle */}
              <button
                onClick={() => setDarkMode(!darkMode)}
                className="p-2.5 rounded-xl bg-gradient-to-br from-gray-100 to-gray-200 dark:from-gray-700 dark:to-gray-600 hover:from-gray-200 hover:to-gray-300 dark:hover:from-gray-600 dark:hover:to-gray-500 transition-all duration-300 transform hover:scale-110 hover:rotate-12 shadow-md hover:shadow-lg"
                aria-label="Toggle dark mode"
              >
                {darkMode ? (
                  <Sun className="w-5 h-5 text-yellow-500 animate-pulse" />
                ) : (
                  <Moon className="w-5 h-5 text-gray-700 dark:text-gray-300" />
                )}
              </button>

              {/* XP Bar */}
              <div className="flex items-center space-x-2 bg-gradient-to-r from-blue-50 to-purple-50 dark:from-blue-900/20 dark:to-purple-900/20 px-4 py-2 rounded-xl border border-blue-200/50 dark:border-blue-700/30">
                <div className="w-32 bg-gray-200 dark:bg-gray-700 rounded-full h-3 shadow-inner overflow-hidden">
                  <div
                    className="h-3 rounded-full bg-gradient-to-r from-blue-500 via-purple-500 to-pink-500 transition-all duration-500 shadow-lg relative overflow-hidden"
                    style={{ width: `${Math.min((user.xp_points / 1000) * 100, 100)}%` }}
                  >
                    <div className="absolute inset-0 bg-white/20 animate-shimmer"></div>
                  </div>
                </div>
                <span className="text-sm font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent dark:from-blue-400 dark:to-purple-400">
                  ⭐ {user.xp_points} XP
                </span>
              </div>

              {/* User Dropdown */}
              <div className="relative">
                <button
                  onClick={() => setShowDropdown(!showDropdown)}
                  className="flex items-center space-x-2 text-gray-700 dark:text-gray-300 hover:text-primary-600 dark:hover:text-primary-400 transition-colors"
                >
                  <User className="w-5 h-5" />
                  <span className="font-medium">{user.username}</span>
                </button>
                {showDropdown && (
                  <div className="absolute right-0 mt-2 w-48 bg-white dark:bg-gray-800 rounded-lg shadow-lg border border-gray-200 dark:border-gray-700 py-2 z-50">
                    <div className="px-4 py-2 border-b border-gray-200 dark:border-gray-700">
                      <p className="text-sm font-semibold text-gray-900 dark:text-gray-100">{user.username}</p>
                      <p className="text-xs text-gray-500 dark:text-gray-400">Level: {user.cefr_level}</p>
                    </div>
                    <button
                      onClick={handleLogout}
                      className="w-full text-left px-4 py-2 text-sm text-red-600 dark:text-red-400 hover:bg-red-50 dark:hover:bg-red-900/20 flex items-center transition-colors"
                    >
                      <LogOut className="w-4 h-4 mr-2" />
                      Logout
                    </button>
                  </div>
                )}
              </div>
            </div>
          ) : (
            <div className="flex items-center space-x-4">
              <button
                onClick={() => setDarkMode(!darkMode)}
                className="p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
                aria-label="Toggle dark mode"
              >
                {darkMode ? (
                  <Sun className="w-5 h-5 text-yellow-500" />
                ) : (
                  <Moon className="w-5 h-5 text-gray-700" />
                )}
              </button>
              <Link
                to="/login"
                className="text-gray-700 dark:text-gray-300 hover:text-primary-600 dark:hover:text-primary-400 font-medium transition-colors"
              >
                Login
              </Link>
              <Link
                to="/login"
                className="btn-primary"
              >
                Sign Up
              </Link>
            </div>
          )}
        </div>
      </div>
    </nav>
  )
}
