import { useState, useEffect } from 'react'
import { getBadges } from '../services/api'
import { Award, Trophy } from 'lucide-react'

export default function BadgeDisplay({ user }) {
  const [badges, setBadges] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchBadges()
  }, [])

  const fetchBadges = async () => {
    try {
      const response = await getBadges()
      setBadges(response.data.available_badges || [])
    } catch (error) {
      console.error('Error fetching badges:', error)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return <p className="text-gray-500 text-center py-8">Loading badges...</p>
  }

  const earnedBadges = badges.filter(b => b.earned)
  const availableBadges = badges.filter(b => !b.earned)

  return (
    <div className="space-y-6">
      <div>
        <h4 className="text-lg font-semibold mb-4 flex items-center">
          <Trophy className="w-5 h-5 mr-2 text-yellow-600" />
          Earned Badges ({earnedBadges.length})
        </h4>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {earnedBadges.map((badge, idx) => (
            <div
              key={idx}
              className="card border-2 border-yellow-400 bg-yellow-50 hover:shadow-lg transition-shadow"
            >
              <div className="flex items-center">
                <Award className="w-8 h-8 text-yellow-600 mr-3" />
                <div>
                  <p className="font-semibold text-gray-900">{badge.name}</p>
                  <p className="text-sm text-gray-600">{badge.description}</p>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      <div>
        <h4 className="text-lg font-semibold mb-4">Available Badges</h4>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {availableBadges.map((badge, idx) => (
            <div
              key={idx}
              className="card border border-gray-200 bg-gray-50 opacity-75"
            >
              <div className="flex items-center">
                <Award className="w-8 h-8 text-gray-400 mr-3" />
                <div>
                  <p className="font-semibold text-gray-600">{badge.name}</p>
                  <p className="text-sm text-gray-500">{badge.description}</p>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}
