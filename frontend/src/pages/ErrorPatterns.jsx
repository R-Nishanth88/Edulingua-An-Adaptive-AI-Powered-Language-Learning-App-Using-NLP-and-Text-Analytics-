import { useState, useEffect } from 'react'
import { TrendingUp, AlertCircle, Target, BookOpen } from 'lucide-react'
import { getErrorPatterns } from '../services/api'
import { LineChart, Line, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'

export default function ErrorPatterns() {
  const [patterns, setPatterns] = useState(null)
  const [loading, setLoading] = useState(true)
  const [days, setDays] = useState(30)

  useEffect(() => {
    loadPatterns()
  }, [days])

  const loadPatterns = async () => {
    setLoading(true)
    try {
      const response = await getErrorPatterns(days)
      setPatterns(response.data)
    } catch (error) {
      console.error('Error loading patterns:', error)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-primary-600"></div>
      </div>
    )
  }

  if (!patterns) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <p className="text-gray-600 dark:text-gray-400">No error patterns found</p>
      </div>
    )
  }

  const chartData = Object.entries(patterns.most_common_errors || {})
    .map(([type, count]) => ({ type, count }))
    .slice(0, 10)

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 to-pink-100 dark:from-gray-900 dark:to-gray-800 p-6">
      <div className="max-w-6xl mx-auto">
        <div className="flex justify-between items-center mb-8">
          <div>
            <h1 className="text-4xl font-bold text-gray-900 dark:text-white mb-2">
              <TrendingUp className="inline-block mr-3" />
              Error Pattern Analytics
            </h1>
            <p className="text-gray-600 dark:text-gray-300">
              Track your common mistakes and get personalized improvement paths
            </p>
          </div>
          <select
            value={days}
            onChange={(e) => setDays(Number(e.target.value))}
            className="input-field dark:bg-gray-700 dark:text-white w-40"
          >
            <option value={7}>Last 7 days</option>
            <option value={30}>Last 30 days</option>
            <option value={90}>Last 90 days</option>
          </select>
        </div>

        {/* Summary Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
          <div className="card bg-red-50 dark:bg-red-900/20 border-l-4 border-red-500">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600 dark:text-gray-400">Total Errors</p>
                <p className="text-3xl font-bold text-red-700 dark:text-red-400">
                  {patterns.total_errors || 0}
                </p>
              </div>
              <AlertCircle className="text-red-500" size={40} />
            </div>
          </div>
          <div className="card bg-yellow-50 dark:bg-yellow-900/20 border-l-4 border-yellow-500">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600 dark:text-gray-400">Unique Error Types</p>
                <p className="text-3xl font-bold text-yellow-700 dark:text-yellow-400">
                  {patterns.unique_error_types || 0}
                </p>
              </div>
              <Target className="text-yellow-500" size={40} />
            </div>
          </div>
          <div className="card bg-blue-50 dark:bg-blue-900/20 border-l-4 border-blue-500">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600 dark:text-gray-400">Analysis Period</p>
                <p className="text-3xl font-bold text-blue-700 dark:text-blue-400">
                  {patterns.analysis_period_days}d
                </p>
              </div>
              <BookOpen className="text-blue-500" size={40} />
            </div>
          </div>
        </div>

        {/* Error Frequency Chart */}
        <div className="card mb-6">
          <h2 className="text-2xl font-semibold mb-4 text-gray-800 dark:text-gray-200">
            Most Common Errors
          </h2>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={chartData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="type" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Bar dataKey="count" fill="#3b82f6" />
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Error Patterns */}
        {patterns.error_patterns && patterns.error_patterns.length > 0 && (
          <div className="card mb-6">
            <h2 className="text-2xl font-semibold mb-4 text-gray-800 dark:text-gray-200">
              Identified Patterns
            </h2>
            <div className="space-y-4">
              {patterns.error_patterns.map((pattern, idx) => (
                <div
                  key={idx}
                  className="p-4 bg-gray-50 dark:bg-gray-700 rounded-lg border-l-4 border-orange-500"
                >
                  <div className="flex items-start justify-between">
                    <div>
                      <p className="font-semibold text-gray-800 dark:text-gray-200">
                        {pattern.pattern.replace('_', ' ').toUpperCase()}
                      </p>
                      <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">
                        {pattern.description}
                      </p>
                      <p className="text-sm text-gray-500 dark:text-gray-500 mt-2">
                        Error Type: {pattern.error_type} | Frequency: {pattern.frequency || pattern.cluster_size}
                      </p>
                    </div>
                    <span
                      className={`px-3 py-1 rounded-full text-sm font-semibold ${
                        pattern.severity === 'high'
                          ? 'bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-400'
                          : 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-400'
                      }`}
                    >
                      {pattern.severity || 'medium'}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Recommendations */}
        {patterns.recommendations && patterns.recommendations.length > 0 && (
          <div className="card">
            <h2 className="text-2xl font-semibold mb-4 text-gray-800 dark:text-gray-200">
              Personalized Recommendations
            </h2>
            <div className="space-y-4">
              {patterns.recommendations.map((rec, idx) => (
                <div
                  key={idx}
                  className="p-4 bg-green-50 dark:bg-green-900/20 rounded-lg border-l-4 border-green-500"
                >
                  <div className="flex items-start justify-between mb-2">
                    <h3 className="font-semibold text-gray-800 dark:text-gray-200">
                      {rec.error_type.replace('_', ' ').toUpperCase()}
                    </h3>
                    <span
                      className={`px-3 py-1 rounded-full text-sm font-semibold ${
                        rec.priority === 'high'
                          ? 'bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-400'
                          : 'bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-400'
                      }`}
                    >
                      {rec.priority} priority
                    </span>
                  </div>
                  <p className="text-gray-700 dark:text-gray-300 mb-3">{rec.action}</p>
                  {rec.practice_exercises && rec.practice_exercises.length > 0 && (
                    <div>
                      <p className="text-sm font-semibold text-gray-600 dark:text-gray-400 mb-1">
                        Practice Exercises:
                      </p>
                      <ul className="list-disc list-inside text-sm text-gray-600 dark:text-gray-400">
                        {rec.practice_exercises.map((exercise, eIdx) => (
                          <li key={eIdx}>{exercise}</li>
                        ))}
                      </ul>
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

