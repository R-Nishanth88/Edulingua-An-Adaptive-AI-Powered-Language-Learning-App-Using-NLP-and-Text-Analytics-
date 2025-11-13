import { useState } from 'react'
import { Shield, AlertTriangle, CheckCircle } from 'lucide-react'
import { checkPlagiarism } from '../services/api'

export default function PlagiarismChecker() {
  const [text, setText] = useState('')
  const [referenceTexts, setReferenceTexts] = useState([''])
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)

  const handleAddReference = () => {
    setReferenceTexts([...referenceTexts, ''])
  }

  const handleRemoveReference = (index) => {
    setReferenceTexts(referenceTexts.filter((_, i) => i !== index))
  }

  const handleReferenceChange = (index, value) => {
    const newRefs = [...referenceTexts]
    newRefs[index] = value
    setReferenceTexts(newRefs)
  }

  const handleCheck = async () => {
    if (!text.trim()) return
    setLoading(true)
    try {
      const refs = referenceTexts.filter(ref => ref.trim())
      const response = await checkPlagiarism({
        text,
        reference_texts: refs.length > 0 ? refs : null
      })
      setResult(response.data)
    } catch (error) {
      console.error('Error checking plagiarism:', error)
      alert('Failed to check plagiarism. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  const getRiskColor = (risk) => {
    switch (risk) {
      case 'high':
        return 'text-red-600 dark:text-red-400'
      case 'medium':
        return 'text-yellow-600 dark:text-yellow-400'
      default:
        return 'text-green-600 dark:text-green-400'
    }
  }

  const getRiskBg = (risk) => {
    switch (risk) {
      case 'high':
        return 'bg-red-50 dark:bg-red-900/20 border-red-500'
      case 'medium':
        return 'bg-yellow-50 dark:bg-yellow-900/20 border-yellow-500'
      default:
        return 'bg-green-50 dark:bg-green-900/20 border-green-500'
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-orange-50 to-amber-100 dark:from-gray-900 dark:to-gray-800 p-6">
      <div className="max-w-6xl mx-auto">
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-900 dark:text-white mb-2">
            <Shield className="inline-block mr-3" />
            Plagiarism & Repetition Checker
          </h1>
          <p className="text-gray-600 dark:text-gray-300">
            Ensure originality in your written exercises
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
            placeholder="Paste or type your text here to check for plagiarism and repetition..."
            className="input-field dark:bg-gray-700 dark:text-white h-48"
          />
        </div>

        {/* Reference Texts */}
        <div className="card mb-6">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-2xl font-semibold text-gray-800 dark:text-gray-200">
              Reference Texts (Optional)
            </h2>
            <button
              onClick={handleAddReference}
              className="btn-secondary text-sm"
            >
              + Add Reference
            </button>
          </div>
          <div className="space-y-4">
            {referenceTexts.map((ref, idx) => (
              <div key={idx} className="flex gap-2">
                <textarea
                  value={ref}
                  onChange={(e) => handleReferenceChange(idx, e.target.value)}
                  placeholder={`Reference text ${idx + 1}...`}
                  className="input-field dark:bg-gray-700 dark:text-white flex-1 h-24"
                />
                {referenceTexts.length > 1 && (
                  <button
                    onClick={() => handleRemoveReference(idx)}
                    className="btn-secondary"
                  >
                    Remove
                  </button>
                )}
              </div>
            ))}
          </div>
        </div>

        <button
          onClick={handleCheck}
          disabled={loading || !text.trim()}
          className="btn-primary w-full mb-6"
        >
          {loading ? 'Checking...' : 'Check for Plagiarism & Repetition'}
        </button>

        {/* Results */}
        {result && (
          <>
            {/* Overall Score */}
            <div className={`card mb-6 ${getRiskBg(result.plagiarism_risk)} border-l-4`}>
              <div className="text-center">
                <div className="flex items-center justify-center mb-4">
                  {result.plagiarism_risk === 'low' ? (
                    <CheckCircle className="text-green-500" size={48} />
                  ) : (
                    <AlertTriangle className="text-yellow-500" size={48} />
                  )}
                </div>
                <p className="text-sm text-gray-600 dark:text-gray-400 mb-2">
                  Originality Score
                </p>
                <p className="text-6xl font-bold text-gray-800 dark:text-gray-200">
                  {result.originality_score}
                </p>
                <p className="text-2xl mt-2">
                  Risk Level:{' '}
                  <span className={getRiskColor(result.plagiarism_risk)}>
                    {result.plagiarism_risk.toUpperCase()}
                  </span>
                </p>
              </div>
            </div>

            {/* Repetition Score */}
            <div className="card mb-6">
              <h2 className="text-2xl font-semibold mb-4 text-gray-800 dark:text-gray-200">
                Repetition Analysis
              </h2>
              <div className="grid grid-cols-2 gap-4 mb-4">
                <div>
                  <p className="text-sm text-gray-600 dark:text-gray-400">Repetition Score</p>
                  <p className="text-3xl font-bold text-gray-800 dark:text-gray-200">
                    {(result.repetition_score * 100).toFixed(1)}%
                  </p>
                </div>
                <div>
                  <p className="text-sm text-gray-600 dark:text-gray-400">Repetitive Phrases</p>
                  <p className="text-3xl font-bold text-gray-800 dark:text-gray-200">
                    {result.repetitive_phrases?.length || 0}
                  </p>
                </div>
              </div>
              {result.repetitive_phrases && result.repetitive_phrases.length > 0 && (
                <div>
                  <p className="font-semibold mb-2 text-gray-800 dark:text-gray-200">
                    Repeated Phrases:
                  </p>
                  <div className="space-y-2">
                    {result.repetitive_phrases.map((phrase, idx) => (
                      <div
                        key={idx}
                        className="p-3 bg-gray-50 dark:bg-gray-700 rounded-lg"
                      >
                        <p className="text-gray-800 dark:text-gray-200 font-medium">
                          "{phrase.phrase}"
                        </p>
                        <p className="text-sm text-gray-600 dark:text-gray-400">
                          Appears {phrase.count} time(s)
                        </p>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>

            {/* Matches */}
            {result.matches && result.matches.length > 0 && (
              <div className="card mb-6 bg-red-50 dark:bg-red-900/20 border-l-4 border-red-500">
                <h2 className="text-2xl font-semibold mb-4 text-red-800 dark:text-red-300">
                  Potential Matches
                </h2>
                <div className="space-y-4">
                  {result.matches.map((match, idx) => (
                    <div
                      key={idx}
                      className="p-4 bg-white dark:bg-gray-800 rounded-lg"
                    >
                      <div className="flex items-center justify-between mb-2">
                        <span className="font-semibold text-gray-800 dark:text-gray-200">
                          Reference {match.reference_index + 1}
                        </span>
                        <span
                          className={`px-3 py-1 rounded-full text-sm font-semibold ${
                            match.risk_level === 'high'
                              ? 'bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-400'
                              : 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-400'
                          }`}
                        >
                          {match.similarity}% similar
                        </span>
                      </div>
                      <p className="text-sm text-gray-600 dark:text-gray-400 italic">
                        {match.excerpt}
                      </p>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Recommendations */}
            {result.recommendations && result.recommendations.length > 0 && (
              <div className="card bg-blue-50 dark:bg-blue-900/20 border-l-4 border-blue-500">
                <h3 className="text-xl font-semibold mb-4 text-blue-800 dark:text-blue-300">
                  Recommendations
                </h3>
                <ul className="space-y-2">
                  {result.recommendations.map((rec, idx) => (
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

