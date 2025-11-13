import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import { useState, useEffect, createContext, useContext } from 'react'
import Navbar from './components/Navbar'
import Home from './pages/Home'
import LoginSignup from './pages/LoginSignup'
import Dashboard from './pages/Dashboard'
import Chatbot from './pages/Chatbot'
import Progress from './pages/Progress'
import VocabularyTrainer from './pages/VocabularyTrainer'
import DialogPractice from './pages/DialogPractice'
import ErrorPatterns from './pages/ErrorPatterns'
import AdaptiveDifficulty from './pages/AdaptiveDifficulty'
import WritingStyle from './pages/WritingStyle'
import EssayScorer from './pages/EssayScorer'
import LearningPath from './pages/LearningPath'
import PlagiarismChecker from './pages/PlagiarismChecker'
import WritingQualityScore from './pages/WritingQualityScore'
import ToneTransfer from './pages/ToneTransfer'
import ContextualCorrection from './pages/ContextualCorrection'
import SummarizeReview from './pages/SummarizeReview'
import GrammarLessons from './pages/GrammarLessons'
import GrammarDrills from './pages/GrammarDrills'
import DailyChallenges from './pages/DailyChallenges'
import EvaluationMetrics from './pages/EvaluationMetrics'

const DarkModeContext = createContext()

export const useDarkMode = () => useContext(DarkModeContext)

function App() {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)
  const [darkMode, setDarkMode] = useState(() => {
    const saved = localStorage.getItem('darkMode')
    return saved ? JSON.parse(saved) : false
  })

  useEffect(() => {
    localStorage.setItem('darkMode', JSON.stringify(darkMode))
    // Smooth transition for dark mode
    const html = document.documentElement
    if (darkMode) {
      html.style.transition = 'background-color 0.3s ease, color 0.3s ease'
      html.classList.add('dark')
    } else {
      html.style.transition = 'background-color 0.3s ease, color 0.3s ease'
      html.classList.remove('dark')
    }
  }, [darkMode])

  useEffect(() => {
    const token = localStorage.getItem('token')
    if (token) {
      // Verify token and get user info
      import('./services/api').then(({ getCurrentUser }) => {
        getCurrentUser()
          .then((res) => {
            setUser(res.data)
          })
          .catch(() => {
            localStorage.removeItem('token')
            setUser(null)
          })
          .finally(() => setLoading(false))
      })
    } else {
      setLoading(false)
    }
  }, [])

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-primary-600"></div>
      </div>
    )
  }

  return (
    <DarkModeContext.Provider value={{ darkMode, setDarkMode }}>
      <Router>
        <div className="min-h-screen bg-gray-50 dark:bg-gray-900 transition-colors duration-200">
          <Navbar user={user} setUser={setUser} />
        <Routes>
          <Route path="/" element={<Home />} />
          <Route 
            path="/login" 
            element={user ? <Navigate to="/dashboard" /> : <LoginSignup setUser={setUser} />} 
          />
          <Route 
            path="/dashboard" 
            element={user ? <Dashboard user={user} /> : <Navigate to="/login" />} 
          />
          <Route 
            path="/chatbot" 
            element={user ? <Chatbot /> : <Navigate to="/login" />} 
          />
          <Route 
            path="/progress" 
            element={user ? <Progress user={user} /> : <Navigate to="/login" />} 
          />
              <Route 
                path="/vocabulary" 
                element={user ? <VocabularyTrainer /> : <Navigate to="/login" />} 
              />
              <Route 
                path="/dialog" 
                element={user ? <DialogPractice /> : <Navigate to="/login" />} 
              />
              <Route 
                path="/error-patterns" 
                element={user ? <ErrorPatterns /> : <Navigate to="/login" />} 
              />
              <Route 
                path="/difficulty" 
                element={user ? <AdaptiveDifficulty /> : <Navigate to="/login" />} 
              />
              <Route 
                path="/writing-style" 
                element={user ? <WritingStyle /> : <Navigate to="/login" />} 
              />
              <Route 
                path="/essay-scorer" 
                element={user ? <EssayScorer /> : <Navigate to="/login" />} 
              />
              <Route 
                path="/learning-path" 
                element={user ? <LearningPath /> : <Navigate to="/login" />} 
              />
              <Route 
                path="/plagiarism" 
                element={user ? <PlagiarismChecker /> : <Navigate to="/login" />} 
              />
              <Route 
                path="/quality-score" 
                element={user ? <WritingQualityScore /> : <Navigate to="/login" />} 
              />
              <Route 
                path="/tone-transfer" 
                element={user ? <ToneTransfer /> : <Navigate to="/login" />} 
              />
              <Route 
                path="/contextual-correction" 
                element={user ? <ContextualCorrection /> : <Navigate to="/login" />} 
              />
              <Route 
                path="/summarize-review" 
                element={user ? <SummarizeReview /> : <Navigate to="/login" />} 
              />
              <Route 
                path="/grammar-lessons" 
                element={user ? <GrammarLessons /> : <Navigate to="/login" />} 
              />
              <Route 
                path="/grammar-drills" 
                element={user ? <GrammarDrills /> : <Navigate to="/login" />} 
              />
              <Route 
                path="/daily-challenges" 
                element={user ? <DailyChallenges /> : <Navigate to="/login" />} 
              />
              <Route 
                path="/evaluation" 
                element={user ? <EvaluationMetrics /> : <Navigate to="/login" />} 
              />
            </Routes>
        </div>
      </Router>
    </DarkModeContext.Provider>
  )
}

export default App
