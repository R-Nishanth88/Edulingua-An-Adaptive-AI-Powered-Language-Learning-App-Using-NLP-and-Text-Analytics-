import { useState, useEffect } from 'react'
import { 
  getEvaluationDashboard, 
  getLearningEffectiveness, 
  getSystemPerformance,
  getFeatureUsage,
  getQualityMetrics,
  getProgressTrends
} from '../services/api'
import { useDarkMode } from '../App'
import { 
  TrendingUp, TrendingDown, Activity, Award, Target, 
  BarChart3, PieChart, Zap, Users, CheckCircle, AlertCircle 
} from 'lucide-react'
import { LineChart, Line, BarChart, Bar, PieChart as RechartsPieChart, Pie, Cell, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'

// Helper functions outside component
const getTrendIcon = (trend) => {
  if (trend === 'improving') return <TrendingUp className="w-5 h-5 text-green-500" />
  if (trend === 'declining') return <TrendingDown className="w-5 h-5 text-red-500" />
  return <Activity className="w-5 h-5 text-yellow-500" />
}

const getTrendColor = (trend) => {
  if (trend === 'improving') return 'text-green-600 dark:text-green-400'
  if (trend === 'declining') return 'text-red-600 dark:text-red-400'
  return 'text-yellow-600 dark:text-yellow-400'
}

function EvaluationMetrics() {
  const { darkMode } = useDarkMode()
  const [loading, setLoading] = useState(true)
  const [dashboardData, setDashboardData] = useState(null)
  const [selectedPeriod, setSelectedPeriod] = useState(30)
  const [activeTab, setActiveTab] = useState('overview')
  const [error, setError] = useState('')

  useEffect(() => {
    loadDashboardData()
  }, [selectedPeriod])

  const loadDashboardData = async () => {
    setLoading(true)
    setError('')
    try {
      const response = await getEvaluationDashboard(selectedPeriod)
      setDashboardData(response.data)
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to load evaluation metrics')
      console.error('Error loading metrics:', err)
    } finally {
      setLoading(false)
    }
  }

  const COLORS = ['#3b82f6', '#8b5cf6', '#ec4899', '#10b981', '#f59e0b', '#ef4444']

  if (loading) {
    return (
      <div className={`min-h-screen ${darkMode ? 'bg-gray-900' : 'bg-gray-50'} flex items-center justify-center`}>
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className={`text-lg ${darkMode ? 'text-gray-400' : 'text-gray-600'}`}>Loading evaluation metrics...</p>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className={`min-h-screen ${darkMode ? 'bg-gray-900' : 'bg-gray-50'} flex items-center justify-center`}>
        <div className={`card ${darkMode ? 'bg-gray-800' : 'bg-white'} max-w-md`}>
          <div className="text-center">
            <AlertCircle className="w-12 h-12 text-red-500 mx-auto mb-4" />
            <p className={`text-lg font-semibold mb-2 ${darkMode ? 'text-white' : 'text-gray-900'}`}>Error</p>
            <p className={`text-sm ${darkMode ? 'text-gray-400' : 'text-gray-600'}`}>{error}</p>
          </div>
        </div>
      </div>
    )
  }

  if (!dashboardData) {
    return (
      <div className={`min-h-screen ${darkMode ? 'bg-gray-900' : 'bg-gray-50'} flex items-center justify-center`}>
        <p className={`text-lg ${darkMode ? 'text-gray-400' : 'text-gray-600'}`}>No data available</p>
      </div>
    )
  }

  const { learning_effectiveness, quality_metrics, system_performance, feature_usage, progress_trends, summary } = dashboardData

  // Prepare chart data
  const featureUsageData = feature_usage?.feature_usage_counts ? 
    Object.entries(feature_usage.feature_usage_counts)
      .filter(([_, count]) => count > 0)
      .map(([name, value]) => ({
        name: name.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase()),
        value
      })) : []

  return (
    <div className={`min-h-screen ${darkMode ? 'bg-gray-900' : 'bg-gray-50'} py-8 px-4`}>
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <div className="flex items-center justify-between mb-4">
            <h1 className={`text-4xl sm:text-5xl font-bold text-gradient`}>
              📊 Evaluation Metrics
            </h1>
            <select
              value={selectedPeriod}
              onChange={(e) => setSelectedPeriod(Number(e.target.value))}
              className={`input-field w-40 ${darkMode ? 'bg-gray-700 text-white' : 'bg-white'}`}
            >
              <option value={7}>Last 7 days</option>
              <option value={30}>Last 30 days</option>
              <option value={90}>Last 90 days</option>
              <option value={365}>Last year</option>
            </select>
          </div>
          {summary && (
            <div className={`card-gradient p-6 ${darkMode ? 'bg-gradient-to-br from-blue-900/20 to-purple-900/20' : 'bg-gradient-to-br from-blue-50 to-purple-50'}`}>
              <div className="flex items-center justify-between">
                <div>
                  <p className={`text-sm font-semibold mb-1 ${darkMode ? 'text-gray-400' : 'text-gray-600'}`}>
                    Overall Score
                  </p>
                  <p className={`text-4xl font-bold ${summary.overall_score >= 70 ? 'text-green-600' : summary.overall_score >= 50 ? 'text-yellow-600' : 'text-red-600'}`}>
                    {summary.overall_score}/100
                  </p>
                </div>
                <div className={`badge ${summary.status === 'excellent' ? 'badge-success' : 'badge-warning'} text-lg px-6 py-3`}>
                  {summary.status === 'excellent' ? '⭐ Excellent' : '✓ Good'}
                </div>
              </div>
            </div>
          )}
        </div>

        {/* Tabs */}
        <div className="flex flex-wrap gap-2 mb-6 border-b-2 border-gray-200/50 dark:border-gray-700/50 pb-2">
          {['overview', 'learning', 'quality', 'system', 'features'].map((tab) => (
            <button
              key={tab}
              onClick={() => setActiveTab(tab)}
              className={`px-5 py-2.5 font-bold rounded-xl transition-all duration-300 transform hover:scale-105 capitalize ${
                activeTab === tab
                  ? 'bg-gradient-to-r from-blue-500 to-purple-500 text-white shadow-lg scale-105'
                  : 'text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700'
              }`}
            >
              {tab}
            </button>
          ))}
        </div>

        {/* Overview Tab */}
        {activeTab === 'overview' && (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {/* Learning Effectiveness */}
            <MetricCard
              title="Learning Effectiveness"
              value={`${learning_effectiveness?.error_reduction_rate || 0}%`}
              subtitle="Error Reduction Rate"
              icon={<Target className="w-8 h-8" />}
              gradient="from-green-400 to-emerald-500"
              trend={progress_trends?.trend}
            />

            {/* Quality Score */}
            <MetricCard
              title="Quality Score"
              value={`${quality_metrics?.quality_score || 0}/100`}
              subtitle="Correction Success Rate"
              icon={<Award className="w-8 h-8" />}
              gradient="from-blue-400 to-cyan-500"
            />

            {/* Engagement Rate */}
            <MetricCard
              title="Engagement"
              value={`${system_performance?.engagement_rate || 0}%`}
              subtitle="Active Users"
              icon={<Users className="w-8 h-8" />}
              gradient="from-purple-400 to-pink-500"
            />

            {/* System Health */}
            <MetricCard
              title="System Health"
              value={system_performance?.system_health || 'unknown'}
              subtitle="Status"
              icon={<Zap className="w-8 h-8" />}
              gradient="from-yellow-400 to-orange-500"
            />
          </div>
        )}

        {/* Learning Tab */}
        {activeTab === 'learning' && (
          <div className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              <MetricCard
                title="Error Reduction"
                value={`${learning_effectiveness?.error_reduction_rate || 0}%`}
                subtitle="Grammar errors reduced"
                icon={<TrendingDown className="w-8 h-8" />}
                gradient="from-green-400 to-emerald-500"
              />
              <MetricCard
                title="Proficiency Improvement"
                value={`+${learning_effectiveness?.proficiency_improvement || 0}`}
                subtitle="CEFR levels improved"
                icon={<TrendingUp className="w-8 h-8" />}
                gradient="from-blue-400 to-cyan-500"
              />
              <MetricCard
                title="Engagement Score"
                value={`${learning_effectiveness?.engagement_score || 0}/100`}
                subtitle="User activity level"
                icon={<Activity className="w-8 h-8" />}
                gradient="from-purple-400 to-pink-500"
              />
            </div>

            {progress_trends && Object.keys(progress_trends).length > 0 && (
              <div className={`card ${darkMode ? 'bg-gray-800' : 'bg-white'}`}>
                <h3 className={`text-2xl font-bold mb-6 ${darkMode ? 'text-white' : 'text-gray-900'}`}>
                  Progress Trends
                </h3>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  <TrendCard
                    title="Grammar"
                    trend={progress_trends.grammar_trend}
                    improvement={progress_trends.improvement_rate}
                  />
                  <TrendCard
                    title="Vocabulary"
                    trend={progress_trends.vocabulary_trend}
                  />
                  <TrendCard
                    title="Overall"
                    trend={progress_trends.trend}
                  />
                </div>
              </div>
            )}
          </div>
        )}

        {/* Quality Tab */}
        {activeTab === 'quality' && (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <MetricCard
              title="Correction Success Rate"
              value={`${quality_metrics?.correction_success_rate || 0}%`}
              subtitle="Successful corrections"
              icon={<CheckCircle className="w-8 h-8" />}
              gradient="from-green-400 to-emerald-500"
              fullWidth
            />
            <MetricCard
              title="Average Errors per Text"
              value={quality_metrics?.average_errors_per_text || 0}
              subtitle="Errors detected"
              icon={<AlertCircle className="w-8 h-8" />}
              gradient="from-yellow-400 to-orange-500"
              fullWidth
            />
            <MetricCard
              title="User Satisfaction"
              value={`${quality_metrics?.user_satisfaction || 0}/5`}
              subtitle="Average rating"
              icon={<Award className="w-8 h-8" />}
              gradient="from-blue-400 to-purple-500"
              fullWidth
            />
            <MetricCard
              title="Total Corrections"
              value={quality_metrics?.total_corrections || 0}
              subtitle="Corrections performed"
              icon={<BarChart3 className="w-8 h-8" />}
              gradient="from-pink-400 to-red-500"
              fullWidth
            />
          </div>
        )}

        {/* System Tab */}
        {activeTab === 'system' && (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            <MetricCard
              title="Total Users"
              value={system_performance?.total_users || 0}
              subtitle="Registered users"
              icon={<Users className="w-8 h-8" />}
              gradient="from-blue-400 to-cyan-500"
            />
            <MetricCard
              title="Active Users"
              value={system_performance?.active_users || 0}
              subtitle="Users with activity"
              icon={<Activity className="w-8 h-8" />}
              gradient="from-green-400 to-emerald-500"
            />
            <MetricCard
              title="Engagement Rate"
              value={`${system_performance?.engagement_rate || 0}%`}
              subtitle="Active / Total"
              icon={<PieChart className="w-8 h-8" />}
              gradient="from-purple-400 to-pink-500"
            />
            <MetricCard
              title="Avg Sessions/User"
              value={system_performance?.average_sessions_per_user || 0}
              subtitle="Average sessions"
              icon={<BarChart3 className="w-8 h-8" />}
              gradient="from-yellow-400 to-orange-500"
            />
            <MetricCard
              title="Total Feedback"
              value={system_performance?.total_feedback_logs || 0}
              subtitle="Feedback entries"
              icon={<CheckCircle className="w-8 h-8" />}
              gradient="from-cyan-400 to-blue-500"
            />
            <MetricCard
              title="System Health"
              value={system_performance?.system_health || 'unknown'}
              subtitle="Status"
              icon={<Zap className="w-8 h-8" />}
              gradient="from-green-400 to-teal-500"
            />
          </div>
        )}

        {/* Features Tab */}
        {activeTab === 'features' && (
          <div className="space-y-6">
            <div className={`card ${darkMode ? 'bg-gray-800' : 'bg-white'}`}>
              <h3 className={`text-2xl font-bold mb-6 ${darkMode ? 'text-white' : 'text-gray-900'}`}>
                Feature Usage Distribution
              </h3>
              {featureUsageData.length > 0 ? (
                <ResponsiveContainer width="100%" height={400}>
                  <RechartsPieChart>
                    <Pie
                      data={featureUsageData}
                      cx="50%"
                      cy="50%"
                      labelLine={false}
                      label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(0)}%`}
                      outerRadius={120}
                      fill="#8884d8"
                      dataKey="value"
                    >
                      {featureUsageData.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                      ))}
                    </Pie>
                    <Tooltip />
                    <Legend />
                  </RechartsPieChart>
                </ResponsiveContainer>
              ) : (
                <p className={`text-center py-12 ${darkMode ? 'text-gray-400' : 'text-gray-600'}`}>
                  No feature usage data available
                </p>
              )}
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {feature_usage?.feature_usage_counts && Object.entries(feature_usage.feature_usage_counts).map(([feature, count], idx) => (
                <div
                  key={feature}
                  className={`card ${darkMode ? 'bg-gray-800' : 'bg-white'} hover-lift`}
                >
                  <div className="flex items-center justify-between">
                    <div>
                      <p className={`text-sm font-semibold mb-1 ${darkMode ? 'text-gray-400' : 'text-gray-600'}`}>
                        {feature.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase())}
                      </p>
                      <p className={`text-2xl font-bold ${darkMode ? 'text-white' : 'text-gray-900'}`}>
                        {count}
                      </p>
                    </div>
                    <div className={`p-3 rounded-xl bg-gradient-to-br ${['from-blue-500 to-cyan-500', 'from-purple-500 to-pink-500', 'from-green-500 to-emerald-500', 'from-yellow-500 to-orange-500', 'from-pink-500 to-red-500', 'from-cyan-500 to-blue-500'][idx % 6]} text-white`}>
                      <BarChart3 className="w-6 h-6" />
                    </div>
                  </div>
                  {feature_usage.feature_usage_percentages && (
                    <div className="mt-3">
                      <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                        <div
                          className="h-2 rounded-full bg-gradient-to-r from-blue-500 to-purple-500"
                          style={{ width: `${feature_usage.feature_usage_percentages[feature] || 0}%` }}
                        />
                      </div>
                      <p className={`text-xs mt-1 ${darkMode ? 'text-gray-400' : 'text-gray-600'}`}>
                        {feature_usage.feature_usage_percentages[feature] || 0}% of total usage
                      </p>
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

function MetricCard({ title, value, subtitle, icon, gradient, trend, fullWidth = false }) {
  const { darkMode } = useDarkMode()
  return (
    <div className={`card hover-lift ${fullWidth ? '' : ''} group`}>
      <div className="flex items-center justify-between">
        <div className="flex-1">
          <p className={`text-sm font-semibold mb-1 ${darkMode ? 'text-gray-400' : 'text-gray-600'}`}>
            {title}
          </p>
          <p className={`text-3xl font-bold mb-1 ${darkMode ? 'text-white' : 'text-gray-900'}`}>
            {value}
          </p>
          <p className={`text-xs ${darkMode ? 'text-gray-500' : 'text-gray-500'}`}>
            {subtitle}
          </p>
          {trend && (
            <div className="flex items-center gap-1 mt-2">
              {getTrendIcon(trend)}
              <span className={`text-xs font-medium ${getTrendColor(trend)}`}>
                {trend === 'improving' ? 'Improving' : trend === 'declining' ? 'Declining' : 'Stable'}
              </span>
            </div>
          )}
        </div>
        <div className={`p-4 rounded-2xl bg-gradient-to-br ${gradient} text-white shadow-lg transform group-hover:scale-110 group-hover:rotate-6 transition-all duration-300`}>
          {icon}
        </div>
      </div>
    </div>
  )
}

function TrendCard({ title, trend, improvement }) {
  const { darkMode } = useDarkMode()
  return (
    <div className={`p-4 rounded-xl border-2 ${
      trend === 'improving' 
        ? 'border-green-500 bg-green-50 dark:bg-green-900/20' 
        : trend === 'declining'
        ? 'border-red-500 bg-red-50 dark:bg-red-900/20'
        : 'border-yellow-500 bg-yellow-50 dark:bg-yellow-900/20'
    }`}>
      <div className="flex items-center justify-between mb-2">
        <h4 className={`font-bold ${darkMode ? 'text-white' : 'text-gray-900'}`}>{title}</h4>
        {getTrendIcon(trend)}
      </div>
      <p className={`text-sm ${darkMode ? 'text-gray-400' : 'text-gray-600'}`}>
        Trend: <span className={`font-semibold ${getTrendColor(trend)}`}>{trend}</span>
      </p>
      {improvement !== undefined && (
        <p className={`text-xs mt-1 ${darkMode ? 'text-gray-500' : 'text-gray-500'}`}>
          Improvement: {improvement}%
        </p>
      )}
    </div>
  )
}

export default EvaluationMetrics

