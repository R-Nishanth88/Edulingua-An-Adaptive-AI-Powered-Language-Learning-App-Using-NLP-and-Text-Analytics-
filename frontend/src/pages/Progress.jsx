import { useState, useEffect } from 'react'
import { getProgress } from '../services/api'
import Charts from '../components/Charts'
import WordCloud from '../components/WordCloud'
import BadgeDisplay from '../components/BadgeDisplay'
import { TrendingUp, Award, BarChart3 } from 'lucide-react'

export default function Progress({ user }) {
  const [progressData, setProgressData] = useState(null)
  const [loading, setLoading] = useState(true)
  const [activeTab, setActiveTab] = useState('overview')

  useEffect(() => {
    fetchProgress()
  }, [])

  const fetchProgress = async () => {
    try {
      const response = await getProgress(30)
      setProgressData(response.data)
    } catch (error) {
      console.error('Error fetching progress:', error)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="flex items-center justify-center h-64">
          <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-primary-600"></div>
        </div>
      </div>
    )
  }

  if (!progressData) {
    return (
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <p className="text-gray-500">No progress data available yet. Start analyzing text to see your progress!</p>
      </div>
    )
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Progress Dashboard</h1>
        <p className="text-gray-600">
          Track your learning journey and see how you're improving
        </p>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
        <div className="card">
          <div className="flex items-center">
            <TrendingUp className="w-8 h-8 text-green-600 mr-3" />
            <div>
              <p className="text-sm text-gray-600">Current Level</p>
              <p className="text-2xl font-bold text-gray-900">{progressData.user?.current_cefr_level || 'A1'}</p>
            </div>
          </div>
        </div>
        <div className="card">
          <div className="flex items-center">
            <BarChart3 className="w-8 h-8 text-blue-600 mr-3" />
            <div>
              <p className="text-sm text-gray-600">Total Practices</p>
              <p className="text-2xl font-bold text-gray-900">{progressData.user?.total_practices || 0}</p>
            </div>
          </div>
        </div>
        <div className="card">
          <div className="flex items-center">
            <Award className="w-8 h-8 text-yellow-600 mr-3" />
            <div>
              <p className="text-sm text-gray-600">XP Points</p>
              <p className="text-2xl font-bold text-gray-900">{progressData.user?.xp_points || 0}</p>
            </div>
          </div>
        </div>
        <div className="card">
          <div className="flex items-center">
            <TrendingUp className="w-8 h-8 text-purple-600 mr-3" />
            <div>
              <p className="text-sm text-gray-600">Improvement Rate</p>
              <p className="text-2xl font-bold text-gray-900">
                {progressData.statistics?.improvement_rate?.toFixed(1) || 0}%
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Tabs */}
      <div className="mb-6 border-b border-gray-200">
        <div className="flex space-x-4">
          <button
            onClick={() => setActiveTab('overview')}
            className={`px-4 py-2 font-semibold transition-colors ${
              activeTab === 'overview'
                ? 'text-primary-600 border-b-2 border-primary-600'
                : 'text-gray-500 hover:text-gray-700'
            }`}
          >
            Overview
          </button>
          <button
            onClick={() => setActiveTab('grammar')}
            className={`px-4 py-2 font-semibold transition-colors ${
              activeTab === 'grammar'
                ? 'text-primary-600 border-b-2 border-primary-600'
                : 'text-gray-500 hover:text-gray-700'
            }`}
          >
            Grammar Trends
          </button>
          <button
            onClick={() => setActiveTab('vocabulary')}
            className={`px-4 py-2 font-semibold transition-colors ${
              activeTab === 'vocabulary'
                ? 'text-primary-600 border-b-2 border-primary-600'
                : 'text-gray-500 hover:text-gray-700'
            }`}
          >
            Vocabulary Growth
          </button>
          <button
            onClick={() => setActiveTab('achievements')}
            className={`px-4 py-2 font-semibold transition-colors ${
              activeTab === 'achievements'
                ? 'text-primary-600 border-b-2 border-primary-600'
                : 'text-gray-500 hover:text-gray-700'
            }`}
          >
            Achievements
          </button>
        </div>
      </div>

      {/* Tab Content */}
      <div>
        {activeTab === 'overview' && (
          <div className="space-y-6">
            <Charts progressData={progressData} />
            {progressData.error_analysis && (
              <div className="card">
                <h3 className="text-xl font-semibold mb-4">Common Errors</h3>
                <WordCloud errors={progressData.error_analysis.common_errors} />
              </div>
            )}
          </div>
        )}
        {activeTab === 'grammar' && (
          <div className="card">
            <h3 className="text-xl font-semibold mb-4">Grammar Error Trends</h3>
            <Charts progressData={progressData} chartType="grammar" />
          </div>
        )}
        {activeTab === 'vocabulary' && (
          <div className="card">
            <h3 className="text-xl font-semibold mb-4">Vocabulary Growth</h3>
            <Charts progressData={progressData} chartType="vocabulary" />
          </div>
        )}
        {activeTab === 'achievements' && (
          <div className="card">
            <h3 className="text-xl font-semibold mb-4">Your Achievements</h3>
            <BadgeDisplay user={user} />
          </div>
        )}
      </div>
    </div>
  )
}
