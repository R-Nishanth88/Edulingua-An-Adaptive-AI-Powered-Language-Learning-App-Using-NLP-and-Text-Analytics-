import { useState } from 'react'
import { contextualCorrection, coherenceAnalysis } from '../services/api'
import { useDarkMode } from '../App'

function ContextualCorrection() {
  const { darkMode } = useDarkMode()
  const [text, setText] = useState('')
  const [loading, setLoading] = useState(false)
  const [correctionResult, setCorrectionResult] = useState(null)
  const [coherenceResult, setCoherenceResult] = useState(null)
  const [error, setError] = useState('')

  const handleCorrection = async () => {
    if (!text.trim() || text.length < 10) {
      setError('Text must be at least 10 characters')
      return
    }

    setLoading(true)
    setError('')
    try {
      const [correction, coherence] = await Promise.all([
        contextualCorrection({ text, use_ai: true }),
        coherenceAnalysis({ text, use_ai: true })
      ])
      setCorrectionResult(correction.data)
      setCoherenceResult(coherence.data)
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to correct text')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className={`min-h-screen ${darkMode ? 'bg-gray-900' : 'bg-gray-50'} py-8 px-4`}>
      <div className="max-w-6xl mx-auto">
        <h1 className={`text-4xl font-bold mb-8 ${darkMode ? 'text-white' : 'text-gray-900'}`}>
          📝 Context-Aware Grammar Correction
        </h1>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Input Section */}
          <div className={`card ${darkMode ? 'bg-gray-800' : 'bg-white'}`}>
            <h2 className={`text-2xl font-semibold mb-4 ${darkMode ? 'text-white' : 'text-gray-900'}`}>
              Enter Paragraph
            </h2>
            <textarea
              value={text}
              onChange={(e) => {
                setText(e.target.value)
                setCorrectionResult(null)
                setCoherenceResult(null)
              }}
              placeholder="Enter a paragraph (multiple sentences) for context-aware correction..."
              className={`input-field w-full h-64 ${darkMode ? 'bg-gray-700 text-white' : 'bg-gray-50'}`}
            />
            <button
              onClick={handleCorrection}
              disabled={loading || !text.trim()}
              className="btn-primary mt-4 w-full"
            >
              {loading ? 'Correcting...' : 'Correct with Context'}
            </button>
            {error && <p className="text-red-500 mt-2">{error}</p>}
          </div>

          {/* Results Section */}
          <div className={`card ${darkMode ? 'bg-gray-800' : 'bg-white'}`}>
            <h2 className={`text-2xl font-semibold mb-4 ${darkMode ? 'text-white' : 'text-gray-900'}`}>
              Corrected Text
            </h2>
            {correctionResult ? (
              <div className="space-y-6">
                {/* Corrected Text */}
                <div className={`p-4 rounded-lg ${darkMode ? 'bg-green-900/20 border border-green-500' : 'bg-green-50 border border-green-200'}`}>
                  <p className={`text-sm font-medium mb-2 ${darkMode ? 'text-green-400' : 'text-green-700'}`}>
                    ✓ Corrected Paragraph
                  </p>
                  <p className={`text-base ${darkMode ? 'text-gray-200' : 'text-gray-800'}`}>
                    {correctionResult.corrected}
                  </p>
                </div>

                {/* Changes Summary */}
                {correctionResult.changes && correctionResult.changes.length > 0 && (
                  <div className={`p-4 rounded-lg ${darkMode ? 'bg-gray-700' : 'bg-gray-100'}`}>
                    <h4 className={`font-semibold mb-2 ${darkMode ? 'text-white' : 'text-gray-900'}`}>
                      Changes Made ({correctionResult.corrections_applied || 0})
                    </h4>
                    <div className="space-y-2">
                      {correctionResult.changes.slice(0, 5).map((change, idx) => (
                        <div key={idx} className={`text-sm ${darkMode ? 'text-gray-300' : 'text-gray-700'}`}>
                          <span className="font-medium">Sentence {change.sentence_index + 1}:</span> {change.message}
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {/* Coherence Analysis */}
                {coherenceResult && (
                  <div className={`p-4 rounded-lg ${darkMode ? 'bg-blue-900/20 border border-blue-500' : 'bg-blue-50 border border-blue-200'}`}>
                    <h4 className={`font-semibold mb-2 ${darkMode ? 'text-blue-400' : 'text-blue-700'}`}>
                      Coherence Analysis
                    </h4>
                    <div className="space-y-2">
                      <div className="flex justify-between">
                        <span className={`text-sm ${darkMode ? 'text-gray-300' : 'text-gray-700'}`}>
                          Coherence Score:
                        </span>
                        <span className={`font-bold ${coherenceResult.coherence_score >= 0.7 ? 'text-green-500' : 'text-yellow-500'}`}>
                          {(coherenceResult.coherence_score * 100).toFixed(0)}%
                        </span>
                      </div>
                      {coherenceResult.suggestions && coherenceResult.suggestions.length > 0 && (
                        <div className="mt-2">
                          <p className={`text-xs font-medium mb-1 ${darkMode ? 'text-blue-300' : 'text-blue-600'}`}>
                            Suggestions:
                          </p>
                          <ul className="text-xs space-y-1">
                            {coherenceResult.suggestions.map((suggestion, idx) => (
                              <li key={idx} className={darkMode ? 'text-gray-300' : 'text-gray-700'}>
                                • {suggestion}
                              </li>
                            ))}
                          </ul>
                        </div>
                      )}
                    </div>
                  </div>
                )}

                {/* Stats */}
                <div className="grid grid-cols-3 gap-4 text-center">
                  <div>
                    <p className={`text-2xl font-bold ${darkMode ? 'text-white' : 'text-gray-900'}`}>
                      {correctionResult.sentence_count || 0}
                    </p>
                    <p className={`text-xs ${darkMode ? 'text-gray-400' : 'text-gray-600'}`}>Sentences</p>
                  </div>
                  <div>
                    <p className={`text-2xl font-bold ${darkMode ? 'text-white' : 'text-gray-900'}`}>
                      {correctionResult.corrections_applied || 0}
                    </p>
                    <p className={`text-xs ${darkMode ? 'text-gray-400' : 'text-gray-600'}`}>Corrections</p>
                  </div>
                  <div>
                    <p className={`text-2xl font-bold ${darkMode ? 'text-white' : 'text-gray-900'}`}>
                      {correctionResult.context_preserved ? '✓' : '✗'}
                    </p>
                    <p className={`text-xs ${darkMode ? 'text-gray-400' : 'text-gray-600'}`}>Context</p>
                  </div>
                </div>
              </div>
            ) : (
              <p className={`text-center py-12 ${darkMode ? 'text-gray-400' : 'text-gray-500'}`}>
                Enter a paragraph and click "Correct with Context" to see results
              </p>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}

export default ContextualCorrection

