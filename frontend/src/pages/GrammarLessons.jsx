import { useState, useEffect } from 'react'
import { getGrammarLessons, getGrammarTopics } from '../services/api'
import { useDarkMode } from '../App'

function GrammarLessons() {
  const { darkMode } = useDarkMode()
  const [text, setText] = useState('')
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)
  const [topics, setTopics] = useState([])
  const [error, setError] = useState('')

  useEffect(() => {
    loadTopics()
  }, [])

  const loadTopics = async () => {
    try {
      const response = await getGrammarTopics()
      setTopics(response.data.topics || [])
    } catch (err) {
      console.error('Failed to load topics:', err)
    }
  }

  const handleGetLessons = async () => {
    if (!text.trim() || text.length < 10) {
      setError('Text must be at least 10 characters')
      return
    }

    setLoading(true)
    setError('')
    try {
      const response = await getGrammarLessons({ text, use_ai: true })
      setResult(response.data)
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to get grammar lessons')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className={`min-h-screen ${darkMode ? 'bg-gray-900' : 'bg-gray-50'} py-8 px-4`}>
      <div className="max-w-6xl mx-auto">
        <h1 className={`text-4xl font-bold mb-8 ${darkMode ? 'text-white' : 'text-gray-900'}`}>
          📚 Grammar Topic Linking
        </h1>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Input Section */}
          <div className={`card ${darkMode ? 'bg-gray-800' : 'bg-white'}`}>
            <h2 className={`text-2xl font-semibold mb-4 ${darkMode ? 'text-white' : 'text-gray-900'}`}>
              Check Your Text
            </h2>
            <textarea
              value={text}
              onChange={(e) => {
                setText(e.target.value)
                setResult(null)
              }}
              placeholder="Enter text to get personalized grammar lessons based on your mistakes..."
              className={`input-field w-full h-64 ${darkMode ? 'bg-gray-700 text-white' : 'bg-gray-50'}`}
            />
            <button
              onClick={handleGetLessons}
              disabled={loading || !text.trim()}
              className="btn-primary mt-4 w-full"
            >
              {loading ? 'Analyzing...' : 'Get Grammar Lessons'}
            </button>
            {error && <p className="text-red-500 mt-2">{error}</p>}
          </div>

          {/* Results Section */}
          <div className={`card ${darkMode ? 'bg-gray-800' : 'bg-white'}`}>
            <h2 className={`text-2xl font-semibold mb-4 ${darkMode ? 'text-white' : 'text-gray-900'}`}>
              Recommended Lessons
            </h2>
            {result ? (
              <div className="space-y-4">
                <div className={`p-4 rounded-lg ${darkMode ? 'bg-blue-900/20 border border-blue-500' : 'bg-blue-50 border border-blue-200'}`}>
                  <p className={`text-sm ${darkMode ? 'text-blue-400' : 'text-blue-700'}`}>
                    {result.message}
                  </p>
                  <p className={`text-xs mt-1 ${darkMode ? 'text-gray-400' : 'text-gray-600'}`}>
                    Found {result.total_errors} error(s) across {result.unique_error_types} error type(s)
                  </p>
                </div>

                {result.lessons && result.lessons.length > 0 ? (
                  <div className="space-y-4">
                    {result.lessons.map((lesson, idx) => (
                      <div
                        key={idx}
                        className={`p-4 rounded-lg border ${
                          lesson.relevance === 'high' 
                            ? darkMode ? 'bg-red-900/20 border-red-500' : 'bg-red-50 border-red-200'
                            : darkMode ? 'bg-gray-700 border-gray-600' : 'bg-gray-100 border-gray-200'
                        }`}
                      >
                        <div className="flex items-start justify-between mb-2">
                          <h3 className={`font-semibold ${darkMode ? 'text-white' : 'text-gray-900'}`}>
                            {lesson.topic}
                          </h3>
                          <span className={`text-xs px-2 py-1 rounded ${
                            lesson.relevance === 'high' ? 'bg-red-500 text-white' : 'bg-gray-500 text-white'
                          }`}>
                            {lesson.error_count} error(s)
                          </span>
                        </div>
                        <p className={`text-sm mb-3 ${darkMode ? 'text-gray-300' : 'text-gray-700'}`}>
                          {lesson.description}
                        </p>

                        {lesson.ai_explanation && (
                          <div className={`p-3 rounded mb-3 ${darkMode ? 'bg-gray-800' : 'bg-white'}`}>
                            <p className={`text-sm ${darkMode ? 'text-gray-300' : 'text-gray-700'}`}>
                              {lesson.ai_explanation}
                            </p>
                          </div>
                        )}

                        <div className="mb-3">
                          <h4 className={`font-medium text-sm mb-2 ${darkMode ? 'text-white' : 'text-gray-900'}`}>
                            Rules:
                          </h4>
                          <ul className="space-y-1">
                            {lesson.rules?.map((rule, ruleIdx) => (
                              <li key={ruleIdx} className={`text-xs ${darkMode ? 'text-gray-400' : 'text-gray-600'}`}>
                                • {rule}
                              </li>
                            ))}
                          </ul>
                        </div>

                        <div>
                          <h4 className={`font-medium text-sm mb-2 ${darkMode ? 'text-white' : 'text-gray-900'}`}>
                            Examples:
                          </h4>
                          <ul className="space-y-1">
                            {lesson.examples?.map((example, exIdx) => (
                              <li key={exIdx} className={`text-xs italic ${darkMode ? 'text-gray-400' : 'text-gray-600'}`}>
                                "{example}"
                              </li>
                            ))}
                          </ul>
                        </div>
                      </div>
                    ))}
                  </div>
                ) : (
                  <div className={`p-4 rounded-lg text-center ${darkMode ? 'bg-green-900/20' : 'bg-green-50'}`}>
                    <p className={`text-sm ${darkMode ? 'text-green-400' : 'text-green-700'}`}>
                      ✓ No errors found! Great job!
                    </p>
                  </div>
                )}
              </div>
            ) : (
              <p className={`text-center py-12 ${darkMode ? 'text-gray-400' : 'text-gray-500'}`}>
                Enter text and click "Get Grammar Lessons" to see personalized lessons
              </p>
            )}
          </div>
        </div>

        {/* Available Topics */}
        {topics.length > 0 && (
          <div className={`mt-8 card ${darkMode ? 'bg-gray-800' : 'bg-white'}`}>
            <h2 className={`text-2xl font-semibold mb-4 ${darkMode ? 'text-white' : 'text-gray-900'}`}>
              Available Grammar Topics
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {topics.map((topic) => (
                <div
                  key={topic.key}
                  className={`p-4 rounded-lg border ${darkMode ? 'bg-gray-700 border-gray-600' : 'bg-gray-50 border-gray-200'}`}
                >
                  <h3 className={`font-semibold mb-2 ${darkMode ? 'text-white' : 'text-gray-900'}`}>
                    {topic.name}
                  </h3>
                  <p className={`text-sm ${darkMode ? 'text-gray-400' : 'text-gray-600'}`}>
                    {topic.description}
                  </p>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

export default GrammarLessons

