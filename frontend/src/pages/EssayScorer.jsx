import { useState } from 'react'
import { FileText, Award, TrendingUp } from 'lucide-react'
import { scoreEssay } from '../services/api'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'

export default function EssayScorer() {
  const [text, setText] = useState('')
  const [topic, setTopic] = useState('')
  const [score, setScore] = useState(null)
  const [loading, setLoading] = useState(false)

  const handleScore = async () => {
    if (!text.trim()) return
    setLoading(true)
    try {
      const response = await scoreEssay({ text, topic: topic || null })
      setScore(response.data)
    } catch (error) {
      console.error('Error scoring essay:', error)
      alert('Failed to score essay. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  const chartData = score
    ? [
        { component: 'Grammar', score: score.component_scores.grammar },
        { component: 'Vocabulary', score: score.component_scores.vocabulary },
        { component: 'Coherence', score: score.component_scores.coherence },
        { component: 'Structure', score: score.component_scores.structure },
        { component: 'Argument', score: score.component_scores.argument_strength },
        { component: 'Style', score: score.component_scores.style }
      ]
    : []

  const getGradeColor = (grade) => {
    switch (grade) {
      case 'A':
        return 'text-green-600 dark:text-green-400'
      case 'B':
        return 'text-blue-600 dark:text-blue-400'
      case 'C':
        return 'text-yellow-600 dark:text-yellow-400'
      case 'D':
        return 'text-orange-600 dark:text-orange-400'
      default:
        return 'text-red-600 dark:text-red-400'
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-50 to-purple-100 dark:from-gray-900 dark:to-gray-800 p-6">
      <div className="max-w-6xl mx-auto">
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-900 dark:text-white mb-2">
            <FileText className="inline-block mr-3" />
            Automatic Essay Scorer
          </h1>
          <p className="text-gray-600 dark:text-gray-300">
            Get comprehensive essay grading with detailed feedback
          </p>
        </div>

        {/* Input */}
        <div className="card mb-6">
          <h2 className="text-2xl font-semibold mb-4 text-gray-800 dark:text-gray-200">
            Enter Your Essay
          </h2>
          <input
            type="text"
            value={topic}
            onChange={(e) => setTopic(e.target.value)}
            placeholder="Essay topic (optional)"
            className="input-field dark:bg-gray-700 dark:text-white mb-4"
          />
          <textarea
            value={text}
            onChange={(e) => setText(e.target.value)}
            placeholder="Paste or type your essay here..."
            className="input-field dark:bg-gray-700 dark:text-white h-64"
          />
          <button
            onClick={handleScore}
            disabled={loading || !text.trim()}
            className="btn-primary mt-4"
          >
            {loading ? 'Scoring...' : 'Score Essay'}
          </button>
        </div>

        {/* Results */}
        {score && (
          <>
            {/* Overall Score */}
            <div className="card mb-6 bg-gradient-to-r from-indigo-500 to-purple-600 text-white">
              <div className="text-center">
                <div className="flex items-center justify-center mb-4">
                  <Award size={48} />
                </div>
                <p className="text-sm opacity-90 mb-2">Overall Essay Score</p>
                <p className="text-6xl font-bold">{score.overall_score}</p>
                <p className="text-2xl mt-2">
                  Grade:{' '}
                  <span className={getGradeColor(score.grade)}>{score.grade}</span>
                </p>
              </div>
            </div>

            {/* Component Scores Chart */}
            <div className="card mb-6">
              <h2 className="text-2xl font-semibold mb-4 text-gray-800 dark:text-gray-200">
                Component Scores
              </h2>
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={chartData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="component" />
                  <YAxis domain={[0, 100]} />
                  <Tooltip />
                  <Legend />
                  <Bar dataKey="score" fill="#6366f1" />
                </BarChart>
              </ResponsiveContainer>
            </div>

            {/* Detailed Scores */}
            <div className="grid grid-cols-2 md:grid-cols-3 gap-4 mb-6">
              {Object.entries(score.component_scores).map(([component, componentScore]) => (
                <div key={component} className="card text-center bg-gray-50 dark:bg-gray-700">
                  <p className="text-sm text-gray-600 dark:text-gray-400 mb-2 capitalize">
                    {component.replace('_', ' ')}
                  </p>
                  <p className="text-3xl font-bold text-gray-800 dark:text-gray-200">
                    {componentScore}
                  </p>
                  <div className="mt-2">
                    <div className="w-full bg-gray-200 dark:bg-gray-600 rounded-full h-2">
                      <div
                        className="bg-indigo-600 h-2 rounded-full"
                        style={{ width: `${componentScore}%` }}
                      ></div>
                    </div>
                  </div>
                </div>
              ))}
            </div>

            {/* Feedback */}
            <div className="card mb-6">
              <h2 className="text-2xl font-semibold mb-4 text-gray-800 dark:text-gray-200">
                Detailed Feedback
              </h2>
              <div className="space-y-4">
                {Object.entries(score.feedback).map(([component, feedback]) => (
                  <div
                    key={component}
                    className="p-4 bg-gray-50 dark:bg-gray-700 rounded-lg"
                  >
                    <p className="font-semibold text-gray-800 dark:text-gray-200 capitalize mb-1">
                      {component.replace('_', ' ')}
                    </p>
                    <p className="text-gray-700 dark:text-gray-300">{feedback}</p>
                  </div>
                ))}
              </div>
            </div>

            {/* Strengths & Improvements */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
              {score.strengths && score.strengths.length > 0 && (
                <div className="card bg-green-50 dark:bg-green-900/20 border-l-4 border-green-500">
                  <h3 className="text-xl font-semibold mb-4 text-green-800 dark:text-green-300">
                    Strengths
                  </h3>
                  <ul className="space-y-2">
                    {score.strengths.map((strength, idx) => (
                      <li key={idx} className="text-gray-700 dark:text-gray-300">
                        ✓ {strength}
                      </li>
                    ))}
                  </ul>
                </div>
              )}
              {score.improvements && score.improvements.length > 0 && (
                <div className="card bg-yellow-50 dark:bg-yellow-900/20 border-l-4 border-yellow-500">
                  <h3 className="text-xl font-semibold mb-4 text-yellow-800 dark:text-yellow-300">
                    Areas for Improvement
                  </h3>
                  <ul className="space-y-2">
                    {score.improvements.map((improvement, idx) => (
                      <li key={idx} className="text-gray-700 dark:text-gray-300">
                        • {improvement}
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </div>

            {/* Detailed Analysis */}
            {score.detailed_analysis && (
              <div className="card bg-blue-50 dark:bg-blue-900/20 border-l-4 border-blue-500">
                <h3 className="text-xl font-semibold mb-4 text-blue-800 dark:text-blue-300">
                  Detailed Analysis
                </h3>
                <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
                  <div>
                    <p className="text-sm text-gray-600 dark:text-gray-400">Word Count</p>
                    <p className="text-2xl font-bold text-gray-800 dark:text-gray-200">
                      {score.detailed_analysis.word_count}
                    </p>
                  </div>
                  <div>
                    <p className="text-sm text-gray-600 dark:text-gray-400">Sentences</p>
                    <p className="text-2xl font-bold text-gray-800 dark:text-gray-200">
                      {score.detailed_analysis.sentence_count}
                    </p>
                  </div>
                  <div>
                    <p className="text-sm text-gray-600 dark:text-gray-400">Grammar Errors</p>
                    <p className="text-2xl font-bold text-gray-800 dark:text-gray-200">
                      {score.detailed_analysis.grammar_errors}
                    </p>
                  </div>
                  <div>
                    <p className="text-sm text-gray-600 dark:text-gray-400">Readability</p>
                    <p className="text-2xl font-bold text-gray-800 dark:text-gray-200">
                      {score.detailed_analysis.readability.toFixed(1)}
                    </p>
                  </div>
                  <div>
                    <p className="text-sm text-gray-600 dark:text-gray-400">Lexical Diversity</p>
                    <p className="text-2xl font-bold text-gray-800 dark:text-gray-200">
                      {(score.detailed_analysis.lexical_diversity * 100).toFixed(1)}%
                    </p>
                  </div>
                </div>
              </div>
            )}
          </>
        )}
      </div>
    </div>
  )
}

