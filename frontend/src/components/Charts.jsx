import { LineChart, Line, AreaChart, Area, BarChart, Bar, RadarChart, Radar, PolarGrid, PolarAngleAxis, PolarRadiusAxis, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'

export default function Charts({ progressData, chartType = 'overview' }) {
  if (!progressData || !progressData.trends) {
    return <p className="text-gray-500 text-center py-8">No data available for charts</p>
  }

  const grammarData = progressData.trends.grammar_errors || []
  const readabilityData = progressData.trends.readability || []
  const sentimentData = progressData.trends.sentiment || []

  if (chartType === 'grammar') {
    return (
      <div className="space-y-6">
        <div className="card">
          <h4 className="text-lg font-semibold mb-4">Grammar Errors Over Time</h4>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={grammarData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="date" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Line type="monotone" dataKey="errors" stroke="#ef4444" strokeWidth={2} />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>
    )
  }

  if (chartType === 'vocabulary') {
    return (
      <div className="card">
        <h4 className="text-lg font-semibold mb-4">Vocabulary Growth</h4>
        <ResponsiveContainer width="100%" height={300}>
          <AreaChart data={readabilityData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="date" />
            <YAxis />
            <Tooltip />
            <Legend />
            <Area type="monotone" dataKey="readability" stroke="#3b82f6" fill="#3b82f6" fillOpacity={0.6} />
          </AreaChart>
        </ResponsiveContainer>
      </div>
    )
  }

  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <div className="card">
        <h4 className="text-lg font-semibold mb-4">Grammar Errors Trend</h4>
        <ResponsiveContainer width="100%" height={250}>
          <LineChart data={grammarData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="date" />
            <YAxis />
            <Tooltip />
            <Line type="monotone" dataKey="errors" stroke="#ef4444" strokeWidth={2} />
          </LineChart>
        </ResponsiveContainer>
      </div>

      <div className="card">
        <h4 className="text-lg font-semibold mb-4">Readability Progress</h4>
        <ResponsiveContainer width="100%" height={250}>
          <AreaChart data={readabilityData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="date" />
            <YAxis />
            <Tooltip />
            <Area type="monotone" dataKey="readability" stroke="#3b82f6" fill="#3b82f6" fillOpacity={0.6} />
          </AreaChart>
        </ResponsiveContainer>
      </div>

      <div className="card">
        <h4 className="text-lg font-semibold mb-4">Sentiment Analysis</h4>
        <ResponsiveContainer width="100%" height={250}>
          <LineChart data={sentimentData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="date" />
            <YAxis />
            <Tooltip />
            <Line type="monotone" dataKey="sentiment" stroke="#8b5cf6" strokeWidth={2} />
          </LineChart>
        </ResponsiveContainer>
      </div>

      <div className="card">
        <h4 className="text-lg font-semibold mb-4">CEFR Level Progress</h4>
        <ResponsiveContainer width="100%" height={250}>
          <BarChart data={grammarData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="date" />
            <YAxis />
            <Tooltip />
            <Bar dataKey="errors" fill="#f59e0b" />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  )
}
