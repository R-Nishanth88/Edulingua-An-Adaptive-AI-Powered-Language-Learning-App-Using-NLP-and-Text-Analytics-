import { useState, useEffect } from 'react'
import { getRecommendations } from '../services/api'
import { BookOpen, CheckCircle, XCircle } from 'lucide-react'

export default function VocabularyTrainer() {
  const [vocabulary, setVocabulary] = useState([])
  const [currentWord, setCurrentWord] = useState(null)
  const [score, setScore] = useState(0)
  const [showAnswer, setShowAnswer] = useState(false)

  useEffect(() => {
    loadVocabulary()
  }, [])

  const loadVocabulary = async () => {
    try {
      const response = await getRecommendations()
      // Simulate vocabulary words (in production, fetch from API)
      const words = [
        { word: 'ubiquitous', meaning: 'present everywhere', example: 'Smartphones are ubiquitous in modern society.' },
        { word: 'ephemeral', meaning: 'lasting for a very short time', example: 'The beauty of cherry blossoms is ephemeral.' },
        { word: 'serendipity', meaning: 'the occurrence of pleasant things by chance', example: 'Finding that book was pure serendipity.' },
        { word: 'eloquent', meaning: 'fluent and persuasive in speaking', example: 'She gave an eloquent speech at the conference.' },
        { word: 'resilient', meaning: 'able to recover quickly from difficulties', example: 'Children are remarkably resilient.' }
      ]
      setVocabulary(words)
      if (words.length > 0) {
        setCurrentWord(words[0])
      }
    } catch (error) {
      console.error('Error loading vocabulary:', error)
    }
  }

  const handleNext = () => {
    const currentIndex = vocabulary.findIndex(w => w.word === currentWord?.word)
    const nextIndex = (currentIndex + 1) % vocabulary.length
    setCurrentWord(vocabulary[nextIndex])
    setShowAnswer(false)
  }

  const handleMarkLearned = () => {
    setScore(score + 1)
    handleNext()
  }

  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Vocabulary Trainer</h1>
        <p className="text-gray-600">
          Expand your vocabulary with daily words and practice exercises
        </p>
      </div>

      <div className="card mb-6">
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center">
            <BookOpen className="w-6 h-6 text-primary-600 mr-2" />
            <h2 className="text-xl font-semibold">Daily Vocabulary</h2>
          </div>
          <div className="text-sm text-gray-600">
            Score: <span className="font-bold text-primary-600">{score}</span>
          </div>
        </div>

        {currentWord ? (
          <div className="space-y-4">
            <div className="bg-primary-50 rounded-lg p-6 text-center">
              <h3 className="text-3xl font-bold text-primary-700 mb-4">{currentWord.word}</h3>
              {showAnswer && (
                <div className="mt-4 space-y-2">
                  <p className="text-lg text-gray-700">
                    <span className="font-semibold">Meaning:</span> {currentWord.meaning}
                  </p>
                  <p className="text-sm text-gray-600 italic">
                    Example: "{currentWord.example}"
                  </p>
                </div>
              )}
            </div>

            <div className="flex gap-3">
              {!showAnswer ? (
                <button
                  onClick={() => setShowAnswer(true)}
                  className="btn-primary flex-1"
                >
                  Show Answer
                </button>
              ) : (
                <>
                  <button
                    onClick={handleNext}
                    className="btn-secondary flex-1"
                  >
                    <XCircle className="w-5 h-5 inline mr-2" />
                    Need More Practice
                  </button>
                  <button
                    onClick={handleMarkLearned}
                    className="btn-primary flex-1"
                  >
                    <CheckCircle className="w-5 h-5 inline mr-2" />
                    Mark as Learned
                  </button>
                </>
              )}
            </div>
          </div>
        ) : (
          <p className="text-gray-500 text-center py-8">Loading vocabulary...</p>
        )}
      </div>

      <div className="card">
        <h3 className="text-lg font-semibold mb-4">Vocabulary List</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {vocabulary.map((word, idx) => (
            <div
              key={idx}
              className={`border rounded-lg p-4 ${
                currentWord?.word === word.word
                  ? 'border-primary-500 bg-primary-50'
                  : 'border-gray-200'
              }`}
            >
              <p className="font-semibold text-gray-900">{word.word}</p>
              <p className="text-sm text-gray-600 mt-1">{word.meaning}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}
