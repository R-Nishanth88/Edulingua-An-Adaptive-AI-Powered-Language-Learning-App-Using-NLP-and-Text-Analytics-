import { useState, useEffect } from 'react'
import { Gauge, TrendingUp, BookOpen, Target } from 'lucide-react'
import { getPerformanceLevel, calculateDifficulty, adjustDifficulty } from '../services/api'

export default function AdaptiveDifficulty() {
  const [performance, setPerformance] = useState(null)
  const [text, setText] = useState('')
  const [difficultyResult, setDifficultyResult] = useState(null)
  const [adjustmentResult, setAdjustmentResult] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadPerformance()
  }, [])

  const loadPerformance = async () => {
    setLoading(true)
    try {
      const response = await getPerformanceLevel(30)
      setPerformance(response.data)
    } catch (error) {
      console.error('Error loading performance:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleCalculateDifficulty = async () => {
    if (!text.trim()) return
    try {
      const response = await calculateDifficulty({ text })
      setDifficultyResult(response.data)
    } catch (error) {
      console.error('Error calculating difficulty:', error)
    }
  }

  const handleAdjustDifficulty = async () => {
    if (!text.trim() || !performance) return
    try {
      const response = await adjustDifficulty({
        text,
        target_level: performance.current_level,
        current_difficulty: difficultyResult?.difficulty_score || 0.5,
        auto_rephrase: true  // Automatically rephrase
      })
      setAdjustmentResult(response.data)
      // If rephrased text is available, update the text field
      if (response.data.rephrased_text) {
        setText(response.data.rephrased_text)
      }
    } catch (error) {
      console.error('Error adjusting difficulty:', error)
    }
  }

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-primary-600"></div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-green-50 to-emerald-100 dark:from-gray-900 dark:to-gray-800 p-6">
      <div className="max-w-6xl mx-auto">
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-900 dark:text-white mb-2">
            <Gauge className="inline-block mr-3" />
            Adaptive Difficulty
          </h1>
          <p className="text-gray-600 dark:text-gray-300">
            Get personalized difficulty recommendations based on your performance
          </p>
        </div>

        {/* Performance Level */}
        {performance && (
          <div className="card mb-6">
            <h2 className="text-2xl font-semibold mb-4 text-gray-800 dark:text-gray-200">
              Your Current Performance Level
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="bg-blue-50 dark:bg-blue-900/20 p-4 rounded-lg">
                <div className="flex items-center justify-between mb-2">
                  <span className="text-gray-600 dark:text-gray-400">Current Level</span>
                  <BookOpen className="text-blue-500" size={24} />
                </div>
                <p className="text-3xl font-bold text-blue-700 dark:text-blue-400">
                  {performance.current_level}
                </p>
              </div>
              <div className="bg-purple-50 dark:bg-purple-900/20 p-4 rounded-lg">
                <div className="flex items-center justify-between mb-2">
                  <span className="text-gray-600 dark:text-gray-400">Error Rate</span>
                  <TrendingUp className="text-purple-500" size={24} />
                </div>
                <p className="text-3xl font-bold text-purple-700 dark:text-purple-400">
                  {(performance.performance_metrics.avg_error_rate * 100).toFixed(1)}%
                </p>
              </div>
            </div>
            {performance.recommended_difficulty && (
              <div className="mt-4 p-4 bg-gray-50 dark:bg-gray-700 rounded-lg">
                <h3 className="font-semibold mb-2 text-gray-800 dark:text-gray-200">
                  Recommended Difficulty Parameters
                </h3>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
                  <div>
                    <span className="text-gray-600 dark:text-gray-400">Sentence Length:</span>
                    <p className="font-semibold">
                      {performance.recommended_difficulty.min_sentence_length} -{' '}
                      {performance.recommended_difficulty.max_sentence_length} words
                    </p>
                  </div>
                  <div>
                    <span className="text-gray-600 dark:text-gray-400">Flesch Score:</span>
                    <p className="font-semibold">≥ {performance.recommended_difficulty.min_flesch}</p>
                  </div>
                  <div>
                    <span className="text-gray-600 dark:text-gray-400">Max Word Length:</span>
                    <p className="font-semibold">{performance.recommended_difficulty.max_word_length}</p>
                  </div>
                  <div>
                    <span className="text-gray-600 dark:text-gray-400">Vocabulary:</span>
                    <p className="font-semibold">
                      {performance.recommended_difficulty.vocabulary_complexity}
                    </p>
                  </div>
                </div>
              </div>
            )}
          </div>
        )}

        {/* Difficulty Calculator */}
        <div className="card mb-6">
          <h2 className="text-2xl font-semibold mb-4 text-gray-800 dark:text-gray-200">
            Calculate Text Difficulty
          </h2>
          <textarea
            value={text}
            onChange={(e) => setText(e.target.value)}
            placeholder="Enter text to analyze difficulty..."
            className="input-field dark:bg-gray-700 dark:text-white h-32"
          />
          <div className="flex gap-2 mt-4">
            <button onClick={handleCalculateDifficulty} className="btn-primary">
              Calculate Difficulty
            </button>
            {performance && (
              <button onClick={handleAdjustDifficulty} className="btn-secondary">
                Adjust to My Level
              </button>
            )}
          </div>
        </div>

        {/* Difficulty Result */}
        {difficultyResult && (
          <div className="card mb-6 bg-indigo-50 dark:bg-indigo-900/20 border-l-4 border-indigo-500">
            <h3 className="text-xl font-semibold mb-4 text-indigo-800 dark:text-indigo-300">
              Difficulty Analysis
            </h3>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <span className="text-gray-600 dark:text-gray-400">Difficulty Score:</span>
                <p className="text-2xl font-bold text-indigo-700 dark:text-indigo-400">
                  {(difficultyResult.difficulty_score * 100).toFixed(1)}%
                </p>
              </div>
              <div>
                <span className="text-gray-600 dark:text-gray-400">Level:</span>
                <p className="text-2xl font-bold text-indigo-700 dark:text-indigo-400">
                  {difficultyResult.difficulty_level}
                </p>
              </div>
            </div>
          </div>
        )}

        {/* Adjustment Result */}
        {adjustmentResult && (
          <div className="card bg-green-50 dark:bg-green-900/20 border-l-4 border-green-500">
            <h3 className="text-xl font-semibold mb-4 text-green-800 dark:text-green-300">
              Difficulty Adjustment Suggestions
            </h3>
            <div className="space-y-2 mb-4">
              <div className="flex justify-between">
                <span className="text-gray-700 dark:text-gray-300">Original Difficulty:</span>
                <span className="font-semibold">
                  {(adjustmentResult.original_difficulty * 100).toFixed(1)}%
                </span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-700 dark:text-gray-300">Target Level:</span>
                <span className="font-semibold">{adjustmentResult.target_level}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-700 dark:text-gray-300">Target Difficulty:</span>
                <span className="font-semibold">
                  {(adjustmentResult.target_difficulty * 100).toFixed(1)}%
                </span>
              </div>
            </div>
            {adjustmentResult.rephrased_text && (
              <div className="mt-4 p-4 bg-blue-50 dark:bg-blue-900/20 rounded-lg border border-blue-200 dark:border-blue-800">
                <h4 className="font-semibold mb-2 text-blue-800 dark:text-blue-300">
                  ✨ Rephrased Text (Adjusted to Your Level):
                </h4>
                <p className="text-gray-800 dark:text-gray-200 mb-2">
                  {adjustmentResult.rephrased_text}
                </p>
                {adjustmentResult.rephrased_difficulty && (
                  <p className="text-sm text-gray-600 dark:text-gray-400">
                    New Difficulty: {(adjustmentResult.rephrased_difficulty * 100).toFixed(1)}%
                  </p>
                )}
              </div>
            )}
            {adjustmentResult.adjustments_needed && adjustmentResult.adjustments_needed.length > 0 && (
              <div className="mt-4">
                <p className="font-semibold mb-2 text-gray-800 dark:text-gray-200">
                  Adjustments Needed:
                </p>
                <ul className="list-disc list-inside space-y-1 text-gray-700 dark:text-gray-300">
                  {adjustmentResult.adjustments_needed.map((adj, idx) => (
                    <li key={idx}>{adj}</li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  )
}

