import { useState } from 'react'
import { generateGrammarDrill } from '../services/api'
import { useDarkMode } from '../App'

function GrammarDrills() {
  const { darkMode } = useDarkMode()
  const [text, setText] = useState('')
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)
  const [selectedAnswers, setSelectedAnswers] = useState({})
  const [showResults, setShowResults] = useState(false)
  const [error, setError] = useState('')

  const handleGenerateDrill = async () => {
    if (!text.trim() || text.length < 10) {
      setError('Text must be at least 10 characters')
      return
    }

    setLoading(true)
    setError('')
    setShowResults(false)
    setSelectedAnswers({})
    try {
      const response = await generateGrammarDrill({ text, use_ai: true })
      setResult(response.data)
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to generate drill')
    } finally {
      setLoading(false)
    }
  }

  const handleAnswerSelect = (questionIndex, answer) => {
    setSelectedAnswers({
      ...selectedAnswers,
      [questionIndex]: answer
    })
  }

  const handleSubmit = () => {
    setShowResults(true)
  }

  const getAnswerClass = (questionIndex, optionIndex, correctAnswer) => {
    if (!showResults) return ''
    const optionLetter = String.fromCharCode(65 + optionIndex) // A, B, C, D
    const isSelected = selectedAnswers[questionIndex] === optionLetter
    const isCorrect = optionLetter === correctAnswer
    
    if (isCorrect) {
      return darkMode ? 'bg-green-700 border-green-500' : 'bg-green-100 border-green-500'
    }
    if (isSelected && !isCorrect) {
      return darkMode ? 'bg-red-700 border-red-500' : 'bg-red-100 border-red-500'
    }
    return ''
  }

  return (
    <div className={`min-h-screen ${darkMode ? 'bg-gray-900' : 'bg-gray-50'} py-8 px-4`}>
      <div className="max-w-4xl mx-auto">
        <h1 className={`text-4xl font-bold mb-8 ${darkMode ? 'text-white' : 'text-gray-900'}`}>
          🎯 Interactive Grammar Drills
        </h1>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Input Section */}
          <div className={`card ${darkMode ? 'bg-gray-800' : 'bg-white'}`}>
            <h2 className={`text-2xl font-semibold mb-4 ${darkMode ? 'text-white' : 'text-gray-900'}`}>
              Generate Drill from Your Text
            </h2>
            <textarea
              value={text}
              onChange={(e) => {
                setText(e.target.value)
                setResult(null)
                setSelectedAnswers({})
                setShowResults(false)
              }}
              placeholder="Enter text with grammar mistakes to generate personalized exercises..."
              className={`input-field w-full h-64 ${darkMode ? 'bg-gray-700 text-white' : 'bg-gray-50'}`}
            />
            <button
              onClick={handleGenerateDrill}
              disabled={loading || !text.trim()}
              className="btn-primary mt-4 w-full"
            >
              {loading ? 'Generating...' : 'Generate Drill'}
            </button>
            {error && <p className="text-red-500 mt-2">{error}</p>}
            {result && (
              <div className={`mt-4 p-3 rounded-lg ${darkMode ? 'bg-blue-900/20' : 'bg-blue-50'}`}>
                <p className={`text-sm ${darkMode ? 'text-blue-400' : 'text-blue-700'}`}>
                  {result.message}
                </p>
                <p className={`text-xs mt-1 ${darkMode ? 'text-gray-400' : 'text-gray-600'}`}>
                  Topic: {result.topic} | Difficulty: {result.difficulty}
                </p>
              </div>
            )}
          </div>

          {/* Drill Section */}
          <div className={`card ${darkMode ? 'bg-gray-800' : 'bg-white'}`}>
            <h2 className={`text-2xl font-semibold mb-4 ${darkMode ? 'text-white' : 'text-gray-900'}`}>
              Practice Exercises
            </h2>
            {result && result.exercises && result.exercises.length > 0 ? (
              <div className="space-y-6">
                {result.exercises.map((exercise, idx) => (
                  <div
                    key={idx}
                    className={`p-4 rounded-lg border ${darkMode ? 'bg-gray-700 border-gray-600' : 'bg-gray-50 border-gray-200'}`}
                  >
                    <div className="mb-3">
                      <span className={`text-sm font-medium ${darkMode ? 'text-gray-400' : 'text-gray-600'}`}>
                        Question {idx + 1}:
                      </span>
                      <p className={`mt-1 font-medium ${darkMode ? 'text-white' : 'text-gray-900'}`}>
                        {exercise.question}
                      </p>
                    </div>

                    <div className="space-y-2 mb-4">
                      {exercise.options.map((option, optIdx) => {
                        const optionLetter = String.fromCharCode(65 + optIdx)
                        const isSelected = selectedAnswers[idx] === optionLetter
                        return (
                          <label
                            key={optIdx}
                            className={`flex items-center p-3 rounded-lg border cursor-pointer transition-colors ${
                              getAnswerClass(idx, optIdx, exercise.correct)
                            } ${
                              !showResults && isSelected
                                ? darkMode ? 'bg-blue-700 border-blue-500' : 'bg-blue-100 border-blue-500'
                                : darkMode ? 'bg-gray-600 border-gray-500' : 'bg-white border-gray-300'
                            }`}
                          >
                            <input
                              type="radio"
                              name={`question-${idx}`}
                              value={optionLetter}
                              checked={isSelected}
                              onChange={() => handleAnswerSelect(idx, optionLetter)}
                              disabled={showResults}
                              className="mr-3"
                            />
                            <span className={`font-medium mr-2 ${darkMode ? 'text-white' : 'text-gray-900'}`}>
                              {optionLetter})
                            </span>
                            <span className={darkMode ? 'text-gray-200' : 'text-gray-800'}>
                              {option}
                            </span>
                          </label>
                        )
                      })}
                    </div>

                    {showResults && (
                      <div className={`p-3 rounded-lg ${darkMode ? 'bg-gray-800' : 'bg-white'}`}>
                        <p className={`text-sm font-medium mb-1 ${darkMode ? 'text-white' : 'text-gray-900'}`}>
                          {selectedAnswers[idx] === exercise.correct ? (
                            <span className="text-green-500">✓ Correct!</span>
                          ) : (
                            <span className="text-red-500">✗ Incorrect. Correct answer: {exercise.correct}</span>
                          )}
                        </p>
                        <p className={`text-xs ${darkMode ? 'text-gray-400' : 'text-gray-600'}`}>
                          {exercise.explanation}
                        </p>
                      </div>
                    )}
                  </div>
                ))}

                {!showResults && (
                  <button
                    onClick={handleSubmit}
                    disabled={Object.keys(selectedAnswers).length !== result.exercises.length}
                    className="btn-primary w-full"
                  >
                    Submit Answers
                  </button>
                )}

                {showResults && (
                  <div className={`p-4 rounded-lg text-center ${darkMode ? 'bg-green-900/20' : 'bg-green-50'}`}>
                    <p className={`text-lg font-semibold ${darkMode ? 'text-green-400' : 'text-green-700'}`}>
                      Score: {result.exercises.filter((ex, idx) => selectedAnswers[idx] === ex.correct).length} / {result.exercises.length}
                    </p>
                    <button
                      onClick={() => {
                        setResult(null)
                        setSelectedAnswers({})
                        setShowResults(false)
                        setText('')
                      }}
                      className="btn-secondary mt-4"
                    >
                      Try Another Drill
                    </button>
                  </div>
                )}
              </div>
            ) : (
              <p className={`text-center py-12 ${darkMode ? 'text-gray-400' : 'text-gray-500'}`}>
                Enter text with grammar mistakes and click "Generate Drill" to create personalized exercises
              </p>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}

export default GrammarDrills

