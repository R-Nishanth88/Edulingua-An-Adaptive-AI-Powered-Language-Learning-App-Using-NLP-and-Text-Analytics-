import { useState, useEffect } from 'react'
import { Map, Target, BookOpen, Clock, CheckCircle } from 'lucide-react'
import { getLearningPath } from '../services/api'

export default function LearningPath() {
  const [path, setPath] = useState(null)
  const [loading, setLoading] = useState(true)
  const [days, setDays] = useState(30)

  useEffect(() => {
    loadPath()
  }, [days])

  const loadPath = async () => {
    setLoading(true)
    try {
      const response = await getLearningPath(days)
      setPath(response.data)
    } catch (error) {
      console.error('Error loading learning path:', error)
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

  if (!path) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <p className="text-gray-600 dark:text-gray-400">No learning path available</p>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-teal-50 to-cyan-100 dark:from-gray-900 dark:to-gray-800 p-6">
      <div className="max-w-6xl mx-auto">
        <div className="flex justify-between items-center mb-8">
          <div>
            <h1 className="text-4xl font-bold text-gray-900 dark:text-white mb-2">
              <Map className="inline-block mr-3" />
              Learning Path
            </h1>
            <p className="text-gray-600 dark:text-gray-300">
              Personalized recommendations based on your performance
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

        {/* Current Level */}
        <div className="card mb-6 bg-gradient-to-r from-blue-500 to-purple-600 text-white">
          <div className="text-center">
            <p className="text-sm opacity-90 mb-2">Your Current Level</p>
            <p className="text-5xl font-bold">{path.current_level}</p>
          </div>
        </div>

        {/* Next Lessons */}
        {path.learning_path.next_lessons && path.learning_path.next_lessons.length > 0 && (
          <div className="card mb-6">
            <h2 className="text-2xl font-semibold mb-4 text-gray-800 dark:text-gray-200">
              Recommended Lessons
            </h2>
            <div className="space-y-4">
              {path.learning_path.next_lessons.map((lesson, idx) => (
                <div
                  key={idx}
                  className="p-6 bg-gray-50 dark:bg-gray-700 rounded-lg border-l-4 border-blue-500"
                >
                  <div className="flex items-start justify-between mb-4">
                    <div className="flex-1">
                      <div className="flex items-center mb-2">
                        <BookOpen className="text-blue-500 mr-2" size={24} />
                        <h3 className="text-xl font-semibold text-gray-800 dark:text-gray-200">
                          {lesson.title}
                        </h3>
                      </div>
                      <p className="text-gray-600 dark:text-gray-400 mb-2">{lesson.topic}</p>
                      <div className="flex items-center gap-4 text-sm text-gray-500 dark:text-gray-500">
                        <span className="flex items-center">
                          <Clock size={16} className="mr-1" />
                          {lesson.estimated_duration}
                        </span>
                        <span className="flex items-center">
                          <Target size={16} className="mr-1" />
                          {lesson.level}
                        </span>
                      </div>
                    </div>
                    <span
                      className={`px-3 py-1 rounded-full text-sm font-semibold ${
                        lesson.priority === 'high'
                          ? 'bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-400'
                          : 'bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-400'
                      }`}
                    >
                      {lesson.priority} priority
                    </span>
                  </div>
                  {lesson.objectives && lesson.objectives.length > 0 && (
                    <div className="mb-4">
                      <p className="font-semibold text-gray-700 dark:text-gray-300 mb-2">
                        Learning Objectives:
                      </p>
                      <ul className="list-disc list-inside space-y-1 text-gray-600 dark:text-gray-400">
                        {lesson.objectives.map((obj, oIdx) => (
                          <li key={oIdx}>{obj}</li>
                        ))}
                      </ul>
                    </div>
                  )}
                  {lesson.exercises && lesson.exercises.length > 0 && (
                    <div>
                      <p className="font-semibold text-gray-700 dark:text-gray-300 mb-2">
                        Practice Exercises:
                      </p>
                      <ul className="list-disc list-inside space-y-1 text-gray-600 dark:text-gray-400">
                        {lesson.exercises.map((exercise, eIdx) => (
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

        {/* Milestones */}
        {path.learning_path.milestones && path.learning_path.milestones.length > 0 && (
          <div className="card mb-6">
            <h2 className="text-2xl font-semibold mb-4 text-gray-800 dark:text-gray-200">
              Learning Milestones
            </h2>
            <div className="space-y-4">
              {path.learning_path.milestones.map((milestone, idx) => (
                <div
                  key={idx}
                  className="p-4 bg-gray-50 dark:bg-gray-700 rounded-lg"
                >
                  <div className="flex items-center justify-between mb-2">
                    <h3 className="font-semibold text-gray-800 dark:text-gray-200">
                      {milestone.milestone}
                    </h3>
                    {milestone.progress !== undefined && (
                      <span className="text-sm font-semibold text-gray-600 dark:text-gray-400">
                        {milestone.progress.toFixed(1)}%
                      </span>
                    )}
                  </div>
                  {milestone.progress !== undefined && (
                    <div className="w-full bg-gray-200 dark:bg-gray-600 rounded-full h-2 mb-2">
                      <div
                        className="bg-blue-600 h-2 rounded-full"
                        style={{ width: `${milestone.progress}%` }}
                      ></div>
                    </div>
                  )}
                  {milestone.estimated_time && (
                    <p className="text-sm text-gray-600 dark:text-gray-400">
                      Estimated: {milestone.estimated_time}
                    </p>
                  )}
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Performance Insights */}
        {path.performance_insights && (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {path.performance_insights.strengths && path.performance_insights.strengths.length > 0 && (
              <div className="card bg-green-50 dark:bg-green-900/20 border-l-4 border-green-500">
                <h3 className="text-xl font-semibold mb-4 text-green-800 dark:text-green-300">
                  Your Strengths
                </h3>
                <ul className="space-y-2">
                  {path.performance_insights.strengths.map((strength, idx) => (
                    <li key={idx} className="flex items-center text-gray-700 dark:text-gray-300">
                      <CheckCircle className="text-green-500 mr-2" size={20} />
                      {strength}
                    </li>
                  ))}
                </ul>
              </div>
            )}
            {path.performance_insights.weaknesses && path.performance_insights.weaknesses.length > 0 && (
              <div className="card bg-yellow-50 dark:bg-yellow-900/20 border-l-4 border-yellow-500">
                <h3 className="text-xl font-semibold mb-4 text-yellow-800 dark:text-yellow-300">
                  Areas to Focus On
                </h3>
                <ul className="space-y-2">
                  {path.performance_insights.weaknesses.map((weakness, idx) => (
                    <li key={idx} className="text-gray-700 dark:text-gray-300">
                      • {weakness.category} ({weakness.error_count} errors)
                    </li>
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

