import { useState } from 'react'
import { summarizeAndReview } from '../services/api'
import { useDarkMode } from '../App'

function SummarizeReview() {
  const { darkMode } = useDarkMode()
  const [text, setText] = useState('')
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)
  const [error, setError] = useState('')

  const handleAnalyze = async () => {
    if (!text.trim() || text.length < 50) {
      setError('Text must be at least 50 characters')
      return
    }

    setLoading(true)
    setError('')
    try {
      const response = await summarizeAndReview({ text, use_ai: true })
      setResult(response.data)
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to summarize and review')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className={`min-h-screen ${darkMode ? 'bg-gray-900' : 'bg-gray-50'} py-8 px-4`}>
      <div className="max-w-6xl mx-auto">
        <h1 className={`text-4xl font-bold mb-8 ${darkMode ? 'text-white' : 'text-gray-900'}`}>
          📄 Text Summarizer & Reviewer
        </h1>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Input Section */}
          <div className={`card ${darkMode ? 'bg-gray-800' : 'bg-white'}`}>
            <h2 className={`text-2xl font-semibold mb-4 ${darkMode ? 'text-white' : 'text-gray-900'}`}>
              Enter Your Text
            </h2>
            <textarea
              value={text}
              onChange={(e) => setText(e.target.value)}
              placeholder="Paste your essay or long text here (minimum 50 characters)..."
              className={`input-field w-full h-96 ${darkMode ? 'bg-gray-700 text-white' : 'bg-gray-50'}`}
            />
            <button
              onClick={handleAnalyze}
              disabled={loading || !text.trim()}
              className="btn-primary mt-4 w-full"
            >
              {loading ? 'Analyzing...' : 'Summarize & Review'}
            </button>
            {error && <p className="text-red-500 mt-2">{error}</p>}
            {text && (
              <p className={`text-sm mt-2 ${darkMode ? 'text-gray-400' : 'text-gray-600'}`}>
                {text.length} characters, {text.split(/\s+/).length} words
              </p>
            )}
          </div>

          {/* Results Section */}
          <div className={`card ${darkMode ? 'bg-gray-800' : 'bg-white'}`}>
            <h2 className={`text-2xl font-semibold mb-4 ${darkMode ? 'text-white' : 'text-gray-900'}`}>
              Summary & Review
            </h2>
            {result ? (
              <div className="space-y-6">
                {/* Summary */}
                <div className={`p-4 rounded-lg ${darkMode ? 'bg-blue-900/20 border border-blue-500' : 'bg-blue-50 border border-blue-200'}`}>
                  <h3 className={`font-semibold mb-2 ${darkMode ? 'text-blue-400' : 'text-blue-700'}`}>
                    📝 Summary
                  </h3>
                  <p className={`text-base ${darkMode ? 'text-gray-200' : 'text-gray-800'}`}>
                    {result.summary}
                  </p>
                </div>

                {/* Key Points */}
                {result.key_points && result.key_points.length > 0 && (
                  <div className={`p-4 rounded-lg ${darkMode ? 'bg-gray-700' : 'bg-gray-100'}`}>
                    <h3 className={`font-semibold mb-2 ${darkMode ? 'text-white' : 'text-gray-900'}`}>
                      🔑 Key Points
                    </h3>
                    <ul className="space-y-2">
                      {result.key_points.map((point, idx) => (
                        <li key={idx} className={`text-sm ${darkMode ? 'text-gray-300' : 'text-gray-700'}`}>
                          • {point}
                        </li>
                      ))}
                    </ul>
                  </div>
                )}

                {/* Improvement Suggestions */}
                {result.improvements && result.improvements.length > 0 && (
                  <div className={`p-4 rounded-lg ${darkMode ? 'bg-yellow-900/20 border border-yellow-500' : 'bg-yellow-50 border border-yellow-200'}`}>
                    <h3 className={`font-semibold mb-2 ${darkMode ? 'text-yellow-400' : 'text-yellow-700'}`}>
                      💡 Improvement Suggestions
                    </h3>
                    <div className="space-y-3">
                      {result.improvements.map((improvement, idx) => (
                        <div key={idx} className={`p-3 rounded ${darkMode ? 'bg-gray-700' : 'bg-white'}`}>
                          <div className="flex items-start justify-between mb-1">
                            <span className={`font-medium text-sm ${darkMode ? 'text-white' : 'text-gray-900'}`}>
                              {improvement.category}
                            </span>
                            <span className={`text-xs px-2 py-1 rounded ${
                              improvement.priority === 'high' ? 'bg-red-500 text-white' :
                              improvement.priority === 'medium' ? 'bg-yellow-500 text-white' :
                              'bg-blue-500 text-white'
                            }`}>
                              {improvement.priority}
                            </span>
                          </div>
                          <p className={`text-sm mt-1 ${darkMode ? 'text-gray-300' : 'text-gray-700'}`}>
                            {improvement.suggestion}
                          </p>
                          {improvement.current_score && (
                            <p className={`text-xs mt-1 ${darkMode ? 'text-gray-400' : 'text-gray-600'}`}>
                              Current score: {improvement.current_score}/100
                            </p>
                          )}
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {/* Stats */}
                <div className="grid grid-cols-3 gap-4 text-center">
                  <div>
                    <p className={`text-2xl font-bold ${darkMode ? 'text-white' : 'text-gray-900'}`}>
                      {result.word_count}
                    </p>
                    <p className={`text-xs ${darkMode ? 'text-gray-400' : 'text-gray-600'}`}>Words</p>
                  </div>
                  <div>
                    <p className={`text-2xl font-bold ${darkMode ? 'text-white' : 'text-gray-900'}`}>
                      {result.sentence_count}
                    </p>
                    <p className={`text-xs ${darkMode ? 'text-gray-400' : 'text-gray-600'}`}>Sentences</p>
                  </div>
                  <div>
                    <p className={`text-2xl font-bold ${darkMode ? 'text-white' : 'text-gray-900'}`}>
                      {result.grammar_errors || 0}
                    </p>
                    <p className={`text-xs ${darkMode ? 'text-gray-400' : 'text-gray-600'}`}>Errors</p>
                  </div>
                </div>

                {result.quality_score && (
                  <div className={`p-4 rounded-lg text-center ${darkMode ? 'bg-green-900/20' : 'bg-green-50'}`}>
                    <p className={`text-sm ${darkMode ? 'text-gray-400' : 'text-gray-600'}`}>Quality Score</p>
                    <p className={`text-3xl font-bold ${darkMode ? 'text-green-400' : 'text-green-600'}`}>
                      {result.quality_score}/100
                    </p>
                  </div>
                )}
              </div>
            ) : (
              <p className={`text-center py-12 ${darkMode ? 'text-gray-400' : 'text-gray-500'}`}>
                Enter text and click "Summarize & Review" to see results
              </p>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}

export default SummarizeReview

