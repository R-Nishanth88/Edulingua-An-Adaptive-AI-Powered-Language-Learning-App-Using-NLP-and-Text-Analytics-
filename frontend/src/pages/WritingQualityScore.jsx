import { useState } from 'react'
import { writingQualityScore } from '../services/api'
import { useDarkMode } from '../App'

function WritingQualityScore() {
  const { darkMode } = useDarkMode()
  const [text, setText] = useState('')
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)
  const [error, setError] = useState('')

  const handleAnalyze = async () => {
    if (!text.trim() || text.length < 10) {
      setError('Text must be at least 10 characters')
      return
    }

    setLoading(true)
    setError('')
    try {
      const response = await writingQualityScore({ text, use_ai: true })
      setResult(response.data)
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to analyze writing quality')
    } finally {
      setLoading(false)
    }
  }

  const getScoreColor = (score) => {
    if (score >= 90) return 'text-green-500'
    if (score >= 80) return 'text-blue-500'
    if (score >= 70) return 'text-yellow-500'
    if (score >= 60) return 'text-orange-500'
    return 'text-red-500'
  }

  const getGradeColor = (grade) => {
    if (grade.startsWith('A')) return 'bg-green-500'
    if (grade.startsWith('B')) return 'bg-blue-500'
    if (grade.startsWith('C')) return 'bg-yellow-500'
    if (grade.startsWith('D')) return 'bg-orange-500'
    return 'bg-red-500'
  }

  return (
    <div className={`min-h-screen ${darkMode ? 'bg-gray-900' : 'bg-gray-50'} py-8 px-4`}>
      <div className="max-w-6xl mx-auto">
        <h1 className={`text-4xl font-bold mb-8 ${darkMode ? 'text-white' : 'text-gray-900'}`}>
          📊 Writing Quality Score
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
              placeholder="Type or paste your text here for quality analysis..."
              className={`input-field w-full h-64 ${darkMode ? 'bg-gray-700 text-white' : 'bg-gray-50'}`}
            />
            <button
              onClick={handleAnalyze}
              disabled={loading || !text.trim()}
              className="btn-primary mt-4 w-full"
            >
              {loading ? 'Analyzing...' : 'Analyze Writing Quality'}
            </button>
            {error && <p className="text-red-500 mt-2">{error}</p>}
          </div>

          {/* Results Section */}
          <div className={`card ${darkMode ? 'bg-gray-800' : 'bg-white'}`}>
            <h2 className={`text-2xl font-semibold mb-4 ${darkMode ? 'text-white' : 'text-gray-900'}`}>
              Quality Analysis
            </h2>
            {result ? (
              <div className="space-y-6">
                {/* Overall Score */}
                <div className="text-center">
                  <div className={`inline-block px-6 py-3 rounded-full ${getGradeColor(result.grade)} text-white text-2xl font-bold mb-2`}>
                    {result.grade}
                  </div>
                  <div className={`text-5xl font-bold ${getScoreColor(result.overall_score)}`}>
                    {result.overall_score}/100
                  </div>
                  <p className={`text-sm mt-2 ${darkMode ? 'text-gray-400' : 'text-gray-600'}`}>
                    Overall Writing Quality Score
                  </p>
                </div>

                {/* Component Scores */}
                <div className="space-y-4">
                  <h3 className={`font-semibold ${darkMode ? 'text-white' : 'text-gray-900'}`}>
                    Component Breakdown:
                  </h3>
                  {Object.entries(result.components || {}).map(([key, component]) => (
                    <div key={key} className={`p-4 rounded-lg ${darkMode ? 'bg-gray-700' : 'bg-gray-100'}`}>
                      <div className="flex justify-between items-center mb-2">
                        <span className={`font-medium capitalize ${darkMode ? 'text-white' : 'text-gray-900'}`}>
                          {key.replace(/_/g, ' ')}
                        </span>
                        <span className={`font-bold ${getScoreColor(component.score)}`}>
                          {component.score}/100
                        </span>
                      </div>
                      <div className="w-full bg-gray-300 rounded-full h-2">
                        <div
                          className={`h-2 rounded-full ${getScoreColor(component.score).replace('text-', 'bg-')}`}
                          style={{ width: `${component.score}%` }}
                        />
                      </div>
                      <p className={`text-xs mt-1 ${darkMode ? 'text-gray-400' : 'text-gray-600'}`}>
                        Weight: {(component.weight * 100).toFixed(0)}%
                      </p>
                    </div>
                  ))}
                </div>

                {/* Feedback */}
                <div className={`p-4 rounded-lg ${darkMode ? 'bg-blue-900/20 border border-blue-500' : 'bg-blue-50 border border-blue-200'}`}>
                  <h4 className={`font-semibold mb-2 ${darkMode ? 'text-blue-400' : 'text-blue-700'}`}>
                    💡 Feedback
                  </h4>
                  <p className={`text-sm ${darkMode ? 'text-gray-300' : 'text-gray-700'}`}>
                    {result.feedback}
                  </p>
                  {result.ai_feedback && (
                    <div className="mt-3 pt-3 border-t border-blue-300">
                      <p className={`text-sm font-medium ${darkMode ? 'text-blue-300' : 'text-blue-600'}`}>
                        AI Suggestions:
                      </p>
                      <p className={`text-sm mt-1 ${darkMode ? 'text-gray-300' : 'text-gray-700'}`}>
                        {result.ai_feedback}
                      </p>
                    </div>
                  )}
                </div>

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
                      {result.components?.grammar_correctness?.errors_found || 0}
                    </p>
                    <p className={`text-xs ${darkMode ? 'text-gray-400' : 'text-gray-600'}`}>Errors</p>
                  </div>
                </div>
              </div>
            ) : (
              <p className={`text-center py-12 ${darkMode ? 'text-gray-400' : 'text-gray-500'}`}>
                Enter text and click "Analyze Writing Quality" to see results
              </p>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}

export default WritingQualityScore

