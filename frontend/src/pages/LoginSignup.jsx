import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { loginUser, signupUser } from '../services/api'
import { LogIn, UserPlus, AlertCircle } from 'lucide-react'

export default function LoginSignup({ setUser }) {
  const [isLogin, setIsLogin] = useState(true)
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: ''
  })
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const navigate = useNavigate()

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    })
    setError('')
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    setLoading(true)

    try {
      let response
      if (isLogin) {
        response = await loginUser({
          email: formData.email,
          password: formData.password
        })
      } else {
        response = await signupUser(formData)
      }

      const { access_token, user_id, username, cefr_level, xp_points } = response.data
      localStorage.setItem('token', access_token)
      setUser({
        id: user_id,
        username,
        cefr_level,
        xp_points
      })
      navigate('/dashboard')
    } catch (err) {
      setError(err.response?.data?.detail || 'An error occurred. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 via-purple-50 to-pink-50 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900 py-12 px-4 sm:px-6 lg:px-8 relative overflow-hidden">
      {/* Animated background shapes */}
      <div className="absolute top-20 left-10 w-40 h-40 bg-blue-300/20 dark:bg-blue-500/10 rounded-full blur-3xl animate-float"></div>
      <div className="absolute bottom-20 right-10 w-60 h-60 bg-purple-300/20 dark:bg-purple-500/10 rounded-full blur-3xl animate-float" style={{ animationDelay: '2s' }}></div>
      <div className="absolute top-1/2 left-1/2 w-32 h-32 bg-pink-300/20 dark:bg-pink-500/10 rounded-full blur-2xl animate-float" style={{ animationDelay: '4s' }}></div>
      
      <div className="max-w-md w-full space-y-8 relative z-10">
        <div className="text-center">
          <div className="inline-block mb-4 animate-bounce-slow">
            <h2 className="text-5xl sm:text-6xl font-bold text-gradient mb-2">
              🧩 EduLingua Pro
            </h2>
          </div>
          <p className="text-lg text-gray-600 dark:text-gray-400 font-medium">
            {isLogin ? '✨ Welcome back!' : '🚀 Create your account'}
          </p>
        </div>

        <div className="card hover-lift">
          {/* Tabs */}
          <div className="flex gap-2 mb-6 bg-gray-100 dark:bg-gray-700 p-1 rounded-xl">
            <button
              onClick={() => {
                setIsLogin(true)
                setError('')
              }}
              className={`flex-1 py-3 px-4 text-center font-bold rounded-lg transition-all duration-300 transform ${
                isLogin
                  ? 'bg-gradient-to-r from-blue-500 to-purple-500 text-white shadow-lg scale-105'
                  : 'text-gray-600 dark:text-gray-400 hover:bg-gray-200 dark:hover:bg-gray-600'
              }`}
            >
              <LogIn className="w-5 h-5 inline mr-2" />
              Login
            </button>
            <button
              onClick={() => {
                setIsLogin(false)
                setError('')
              }}
              className={`flex-1 py-3 px-4 text-center font-bold rounded-lg transition-all duration-300 transform ${
                !isLogin
                  ? 'bg-gradient-to-r from-purple-500 to-pink-500 text-white shadow-lg scale-105'
                  : 'text-gray-600 dark:text-gray-400 hover:bg-gray-200 dark:hover:bg-gray-600'
              }`}
            >
              <UserPlus className="w-5 h-5 inline mr-2" />
              Sign Up
            </button>
          </div>

          {/* Error Message */}
          {error && (
            <div className="mb-4 p-4 bg-gradient-to-r from-red-50 to-pink-50 dark:from-red-900/20 dark:to-pink-900/20 border-2 border-red-300 dark:border-red-700 rounded-xl flex items-center text-red-700 dark:text-red-400 shadow-lg">
              <AlertCircle className="w-5 h-5 mr-2 flex-shrink-0" />
              <span className="text-sm font-medium">{error}</span>
            </div>
          )}

          {/* Form */}
          <form onSubmit={handleSubmit} className="space-y-5">
            {!isLogin && (
              <div>
                <label className="block text-sm font-bold text-gray-700 dark:text-gray-300 mb-2">
                  👤 Username
                </label>
                <input
                  type="text"
                  name="username"
                  value={formData.username}
                  onChange={handleChange}
                  required={!isLogin}
                  className="input-field"
                  placeholder="✨ Enter your username"
                />
              </div>
            )}

            <div>
              <label className="block text-sm font-bold text-gray-700 dark:text-gray-300 mb-2">
                📧 Email
              </label>
              <input
                type="email"
                name="email"
                value={formData.email}
                onChange={handleChange}
                required
                className="input-field"
                placeholder="📧 Enter your email"
              />
            </div>

            <div>
              <label className="block text-sm font-bold text-gray-700 dark:text-gray-300 mb-2">
                🔒 Password
              </label>
              <input
                type="password"
                name="password"
                value={formData.password}
                onChange={handleChange}
                required
                className="input-field"
                placeholder="🔒 Enter your password"
                minLength={6}
              />
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full btn-primary py-4 text-lg font-bold disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none"
            >
              {loading ? (
                <span className="flex items-center justify-center">
                  <div className="animate-spin rounded-full h-5 w-5 border-t-2 border-b-2 border-white mr-2"></div>
                  {isLogin ? 'Logging in...' : 'Signing up...'}
                </span>
              ) : (
                isLogin ? '🚀 Login' : '✨ Sign Up'
              )}
            </button>
          </form>
        </div>
      </div>
    </div>
  )
}
