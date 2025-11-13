import { useState } from 'react'
import { PenTool, CheckCircle, AlertCircle } from 'lucide-react'
import { analyzeWritingStyle } from '../services/api'
import { RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Radar, ResponsiveContainer } from 'recharts'

export default function WritingStyle() {
  const [text, setText] = useState('')
  const [analysis, setAnalysis] = useState(null)
  const [loading, setLoading] = useState(false)

  const handleAnalyze = async () => {
    if (!text.trim()) return
    setLoading(true)
    try {
      const response = await analyzeWritingStyle({ text })
      setAnalysis(response.data)
    } catch (error) {
      console.error('Error analyzing style:', error)
      alert('Failed to analyze writing style. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  const radarData = analysis
    ? [
        {
          aspect: 'Clarity',
          score: analysis.scores.clarity,
          fullMark: 100
        },
        {
          aspect: 'Conciseness',
          score: analysis.scores.conciseness,
          fullMark: 100
        },
        {
          aspect: 'Coherence',
          score: analysis.scores.coherence,
          fullMark: 100
        },
        {
          aspect: 'Formality',
          score: analysis.scores.formality,
          fullMark: 100
        },
        {
          aspect: 'Structure',
          score: analysis.scores.structure,
          fullMark: 100
        }
      ]
    : []

  return (
    <div className="min-h-screen bg-gradient-to-br from-pink-50 to-rose-100 dark:from-gray-900 dark:to-gray-800 p-6">
      <div className="max-w-6xl mx-auto">
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-900 dark:text-white mb-2">
            <PenTool className="inline-block mr-3" />
            Writing Style Analyzer
          </h1>
          <p className="text-gray-600 dark:text-gray-300">
            Get comprehensive feedback on clarity, conciseness, coherence, formality, and structure
          </p>
        </div>

        {/* Input */}
        <div className="card mb-6">
          <h2 className="text-2xl font-semibold mb-4 text-gray-800 dark:text-gray-200">
            Enter Your Text
          </h2>
          <textarea
            value={text}
            onChange={(e) => setText(e.target.value)}
            placeholder="Paste or type your text here for style analysis..."
            className="input-field dark:bg-gray-700 dark:text-white h-48"
          />
          <button
            onClick={handleAnalyze}
            disabled={loading || !text.trim()}
            className="btn-primary mt-4"
          >
            {loading ? 'Analyzing...' : 'Analyze Writing Style'}
          </button>
        </div>

        {/* Results */}
        {analysis && (
          <>
            {/* Overall Score */}
            <div className="card mb-6 bg-gradient-to-r from-blue-500 to-purple-600 text-white">
              <div className="text-center">
                <p className="text-sm opacity-90 mb-2">Overall Writing Style Score</p>
                <p className="text-6xl font-bold">{analysis.overall_score}</p>
                <p className="text-2xl mt-2">out of 100</p>
              </div>
            </div>

            {/* Radar Chart */}
            <div className="card mb-6">
              <h2 className="text-2xl font-semibold mb-4 text-gray-800 dark:text-gray-200">
                Style Breakdown
              </h2>
              <ResponsiveContainer width="100%" height={400}>
                <RadarChart data={radarData}>
                  <PolarGrid />
                  <PolarAngleAxis dataKey="aspect" />
                  <PolarRadiusAxis angle={90} domain={[0, 100]} />
                  <Radar
                    name="Score"
                    dataKey="score"
                    stroke="#3b82f6"
                    fill="#3b82f6"
                    fillOpacity={0.6}
                  />
                </RadarChart>
              </ResponsiveContainer>
            </div>

            {/* Detailed Scores */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4 mb-6">
              {Object.entries(analysis.scores).map(([aspect, score]) => (
                <div
                  key={aspect}
                  className="card text-center bg-gray-50 dark:bg-gray-700"
                >
                  <p className="text-sm text-gray-600 dark:text-gray-400 mb-2 capitalize">
                    {aspect}
                  </p>
                  <p className="text-3xl font-bold text-gray-800 dark:text-gray-200">
                    {score}
                  </p>
                  <div className="mt-2">
                    <div className="w-full bg-gray-200 dark:bg-gray-600 rounded-full h-2">
                      <div
                        className="bg-blue-600 h-2 rounded-full"
                        style={{ width: `${score}%` }}
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
                {Object.entries(analysis.feedback).map(([aspect, feedback]) => (
                  <div
                    key={aspect}
                    className="p-4 bg-gray-50 dark:bg-gray-700 rounded-lg"
                  >
                    <div className="flex items-start">
                      {parseFloat(analysis.scores[aspect]) >= 70 ? (
                        <CheckCircle className="text-green-500 mr-3 mt-1" size={20} />
                      ) : (
                        <AlertCircle className="text-yellow-500 mr-3 mt-1" size={20} />
                      )}
                      <div>
                        <p className="font-semibold text-gray-800 dark:text-gray-200 capitalize mb-1">
                          {aspect}
                        </p>
                        <p className="text-gray-700 dark:text-gray-300">{feedback}</p>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Strengths & Improvements */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
              {analysis.strengths && analysis.strengths.length > 0 && (
                <div className="card bg-green-50 dark:bg-green-900/20 border-l-4 border-green-500">
                  <h3 className="text-xl font-semibold mb-4 text-green-800 dark:text-green-300">
                    Strengths
                  </h3>
                  <ul className="space-y-2">
                    {analysis.strengths.map((strength, idx) => (
                      <li key={idx} className="flex items-center text-gray-700 dark:text-gray-300">
                        <CheckCircle className="text-green-500 mr-2" size={20} />
                        {strength}
                      </li>
                    ))}
                  </ul>
                </div>
              )}
              {analysis.improvements && analysis.improvements.length > 0 && (
                <div className="card bg-yellow-50 dark:bg-yellow-900/20 border-l-4 border-yellow-500">
                  <h3 className="text-xl font-semibold mb-4 text-yellow-800 dark:text-yellow-300">
                    Areas for Improvement
                  </h3>
                  <ul className="space-y-2">
                    {analysis.improvements.map((improvement, idx) => (
                      <li key={idx} className="flex items-center text-gray-700 dark:text-gray-300">
                        <AlertCircle className="text-yellow-500 mr-2" size={20} />
                        {improvement}
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </div>

            {/* Recommendations */}
            {analysis.recommendations && analysis.recommendations.length > 0 && (
              <div className="card bg-blue-50 dark:bg-blue-900/20 border-l-4 border-blue-500">
                <h3 className="text-xl font-semibold mb-4 text-blue-800 dark:text-blue-300">
                  Recommendations
                </h3>
                <ul className="space-y-2">
                  {analysis.recommendations.map((rec, idx) => (
                    <li key={idx} className="text-gray-700 dark:text-gray-300">
                      • {rec}
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </>
        )}
      </div>
    </div>
  )
}

