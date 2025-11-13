import { useState, useEffect } from 'react'
import { getDailyChallenge, getChallengeCategories } from '../services/api'
import { useDarkMode } from '../App'

function DailyChallenges() {
  const { darkMode } = useDarkMode()
  const [challenge, setChallenge] = useState(null)
  const [categories, setCategories] = useState([])
  const [selectedCategory, setSelectedCategory] = useState(null)
  const [loading, setLoading] = useState(false)
  const [userResponse, setUserResponse] = useState('')
  const [wordCount, setWordCount] = useState(0)

  useEffect(() => {
    loadCategories()
    loadChallenge()
  }, [])

  const loadCategories = async () => {
    try {
      const response = await getChallengeCategories()
      setCategories(response.data.categories || [])
    } catch (err) {
      console.error('Failed to load categories:', err)
    }
  }

  const loadChallenge = async (category = null) => {
    setLoading(true)
    try {
      const response = await getDailyChallenge(category)
      setChallenge(response.data)
      setSelectedCategory(category)
    } catch (err) {
      console.error('Failed to load challenge:', err)
    } finally {
      setLoading(false)
    }
  }

  const handleResponseChange = (e) => {
    const text = e.target.value
    setUserResponse(text)
    setWordCount(text.trim().split(/\s+/).filter(word => word.length > 0).length)
  }

  return (
    <div className={`min-h-screen ${darkMode ? 'bg-gray-900' : 'bg-gray-50'} py-8 px-4`}>
      <div className="max-w-4xl mx-auto">
        <h1 className={`text-4xl font-bold mb-8 ${darkMode ? 'text-white' : 'text-gray-900'}`}>
          🎯 Daily Writing Challenges
        </h1>

        {/* Category Selection */}
        {categories.length > 0 && (
          <div className={`mb-6 card ${darkMode ? 'bg-gray-800' : 'bg-white'}`}>
            <h2 className={`text-xl font-semibold mb-4 ${darkMode ? 'text-white' : 'text-gray-900'}`}>
              Choose a Category
            </h2>
            <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-3">
              <button
                onClick={() => loadChallenge(null)}
                className={`p-3 rounded-lg border transition-colors ${
                  selectedCategory === null
                    ? darkMode ? 'bg-blue-700 border-blue-500 text-white' : 'bg-blue-100 border-blue-500 text-blue-700'
                    : darkMode ? 'bg-gray-700 border-gray-600 text-white' : 'bg-gray-50 border-gray-300 text-gray-700'
                }`}
              >
                Random
              </button>
              {categories.map((cat) => (
                <button
                  key={cat.key}
                  onClick={() => loadChallenge(cat.key)}
                  className={`p-3 rounded-lg border transition-colors ${
                    selectedCategory === cat.key
                      ? darkMode ? 'bg-blue-700 border-blue-500 text-white' : 'bg-blue-100 border-blue-500 text-blue-700'
                      : darkMode ? 'bg-gray-700 border-gray-600 text-white' : 'bg-gray-50 border-gray-300 text-gray-700'
                  }`}
                >
                  {cat.name}
                </button>
              ))}
            </div>
          </div>
        )}

        {loading ? (
          <div className="text-center py-12">
            <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-primary-600 mx-auto"></div>
          </div>
        ) : challenge ? (
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Challenge Card */}
            <div className={`card ${darkMode ? 'bg-gray-800' : 'bg-white'}`}>
              <div className="flex items-center justify-between mb-4">
                <h2 className={`text-2xl font-semibold ${darkMode ? 'text-white' : 'text-gray-900'}`}>
                  Today's Challenge
                </h2>
                <span className={`text-xs px-3 py-1 rounded-full ${
                  challenge.category === 'creative' ? 'bg-purple-500' :
                  challenge.category === 'descriptive' ? 'bg-blue-500' :
                  challenge.category === 'persuasive' ? 'bg-red-500' :
                  challenge.category === 'narrative' ? 'bg-green-500' :
                  'bg-gray-500'
                } text-white`}>
                  {challenge.category_name}
                </span>
              </div>

              <div className={`p-4 rounded-lg mb-4 ${darkMode ? 'bg-blue-900/20 border border-blue-500' : 'bg-blue-50 border border-blue-200'}`}>
                <p className={`text-lg font-medium ${darkMode ? 'text-blue-400' : 'text-blue-700'}`}>
                  {challenge.prompt}
                </p>
              </div>

              <div className="grid grid-cols-2 gap-4 mb-4">
                <div className={`p-3 rounded-lg ${darkMode ? 'bg-gray-700' : 'bg-gray-100'}`}>
                  <p className={`text-sm ${darkMode ? 'text-gray-400' : 'text-gray-600'}`}>Target Words</p>
                  <p className={`text-2xl font-bold ${darkMode ? 'text-white' : 'text-gray-900'}`}>
                    {challenge.word_count_target}
                  </p>
                </div>
                <div className={`p-3 rounded-lg ${darkMode ? 'bg-gray-700' : 'bg-gray-100'}`}>
                  <p className={`text-sm ${darkMode ? 'text-gray-400' : 'text-gray-600'}`}>Time Limit</p>
                  <p className={`text-2xl font-bold ${darkMode ? 'text-white' : 'text-gray-900'}`}>
                    {challenge.time_limit_minutes} min
                  </p>
                </div>
              </div>

              {challenge.tips && challenge.tips.length > 0 && (
                <div className={`p-4 rounded-lg ${darkMode ? 'bg-yellow-900/20 border border-yellow-500' : 'bg-yellow-50 border border-yellow-200'}`}>
                  <h4 className={`font-semibold mb-2 ${darkMode ? 'text-yellow-400' : 'text-yellow-700'}`}>
                    💡 Tips
                  </h4>
                  <ul className="space-y-1">
                    {challenge.tips.map((tip, idx) => (
                      <li key={idx} className={`text-sm ${darkMode ? 'text-gray-300' : 'text-gray-700'}`}>
                        • {tip}
                      </li>
                    ))}
                  </ul>
                </div>
              )}

              <button
                onClick={() => loadChallenge(selectedCategory)}
                className="btn-secondary mt-4 w-full"
              >
                Get New Challenge
              </button>
            </div>

            {/* Writing Area */}
            <div className={`card ${darkMode ? 'bg-gray-800' : 'bg-white'}`}>
              <h2 className={`text-2xl font-semibold mb-4 ${darkMode ? 'text-white' : 'text-gray-900'}`}>
                Your Response
              </h2>
              <textarea
                value={userResponse}
                onChange={handleResponseChange}
                placeholder="Start writing your response here..."
                className={`input-field w-full h-96 ${darkMode ? 'bg-gray-700 text-white' : 'bg-gray-50'}`}
              />
              <div className="flex justify-between items-center mt-4">
                <p className={`text-sm ${darkMode ? 'text-gray-400' : 'text-gray-600'}`}>
                  {wordCount} / {challenge.word_count_target} words
                </p>
                <div className="flex gap-2">
                  <button
                    onClick={() => {
                      // Analyze the response using the dashboard
                      window.location.href = `/dashboard?text=${encodeURIComponent(userResponse)}`
                    }}
                    className="btn-secondary"
                    disabled={!userResponse.trim()}
                  >
                    Analyze
                  </button>
                  <button
                    onClick={() => setUserResponse('')}
                    className="btn-secondary"
                  >
                    Clear
                  </button>
                </div>
              </div>
            </div>
          </div>
        ) : (
          <div className={`text-center py-12 ${darkMode ? 'text-gray-400' : 'text-gray-500'}`}>
            No challenge available. Please try again.
          </div>
        )}
      </div>
    </div>
  )
}

export default DailyChallenges

