import { useState, useEffect } from 'react'
import { toneTransfer, getAvailableTones, detectTone } from '../services/api'
import { useDarkMode } from '../App'

function ToneTransfer() {
  const { darkMode } = useDarkMode()
  const [text, setText] = useState('')
  const [selectedTone, setSelectedTone] = useState('formal')
  const [availableTones, setAvailableTones] = useState([])
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)
  const [detectedTone, setDetectedTone] = useState(null)
  const [error, setError] = useState('')

  useEffect(() => {
    loadTones()
  }, [])

  const loadTones = async () => {
    try {
      const response = await getAvailableTones()
      setAvailableTones(response.data.tones || [])
    } catch (err) {
      console.error('Failed to load tones:', err)
    }
  }

  const handleDetectTone = async () => {
    if (!text.trim()) return
    try {
      const response = await detectTone({ text, use_ai: true })
      setDetectedTone(response.data)
    } catch (err) {
      console.error('Failed to detect tone:', err)
    }
  }

  const handleTransfer = async () => {
    if (!text.trim() || text.length < 5) {
      setError('Text must be at least 5 characters')
      return
    }

    setLoading(true)
    setError('')
    try {
      const response = await toneTransfer({
        text,
        target_tone: selectedTone,
        use_ai: true
      })
      setResult(response.data)
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to transfer tone')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className={`min-h-screen ${darkMode ? 'bg-gray-900' : 'bg-gray-50'} py-8 px-4`}>
      <div className="max-w-6xl mx-auto">
        <h1 className={`text-4xl font-bold mb-8 ${darkMode ? 'text-white' : 'text-gray-900'}`}>
          🎨 Tone & Style Transfer
        </h1>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Input Section */}
          <div className={`card ${darkMode ? 'bg-gray-800' : 'bg-white'}`}>
            <h2 className={`text-2xl font-semibold mb-4 ${darkMode ? 'text-white' : 'text-gray-900'}`}>
              Original Text
            </h2>
            <textarea
              value={text}
              onChange={(e) => {
                setText(e.target.value)
                setDetectedTone(null)
                setResult(null)
              }}
              placeholder="Enter text to transfer to a different tone..."
              className={`input-field w-full h-48 ${darkMode ? 'bg-gray-700 text-white' : 'bg-gray-50'}`}
            />
            
            {text && (
              <button
                onClick={handleDetectTone}
                className="btn-secondary mt-2 w-full"
              >
                Detect Current Tone
              </button>
            )}

            {detectedTone && (
              <div className={`mt-4 p-3 rounded-lg ${darkMode ? 'bg-blue-900/20' : 'bg-blue-50'}`}>
                <p className={`text-sm ${darkMode ? 'text-blue-400' : 'text-blue-700'}`}>
                  <strong>Detected Tone:</strong> {detectedTone.detected_tone} 
                  (confidence: {(detectedTone.confidence * 100).toFixed(0)}%)
                </p>
              </div>
            )}

            <div className="mt-4">
              <label className={`block mb-2 font-medium ${darkMode ? 'text-white' : 'text-gray-900'}`}>
                Target Tone:
              </label>
              <select
                value={selectedTone}
                onChange={(e) => setSelectedTone(e.target.value)}
                className={`input-field w-full ${darkMode ? 'bg-gray-700 text-white' : 'bg-gray-50'}`}
              >
                {availableTones.map((tone) => (
                  <option key={tone.name} value={tone.name}>
                    {tone.name.charAt(0).toUpperCase() + tone.name.slice(1)} - {tone.description}
                  </option>
                ))}
              </select>
            </div>

            <button
              onClick={handleTransfer}
              disabled={loading || !text.trim()}
              className="btn-primary mt-4 w-full"
            >
              {loading ? 'Transferring...' : 'Transfer Tone'}
            </button>
            {error && <p className="text-red-500 mt-2">{error}</p>}
          </div>

          {/* Output Section */}
          <div className={`card ${darkMode ? 'bg-gray-800' : 'bg-white'}`}>
            <h2 className={`text-2xl font-semibold mb-4 ${darkMode ? 'text-white' : 'text-gray-900'}`}>
              Rephrased Text
            </h2>
            {result ? (
              <div className="space-y-4">
                {result.success ? (
                  <>
                    <div className={`p-4 rounded-lg ${darkMode ? 'bg-green-900/20 border border-green-500' : 'bg-green-50 border border-green-200'}`}>
                      <p className={`text-sm font-medium mb-2 ${darkMode ? 'text-green-400' : 'text-green-700'}`}>
                        ✓ Successfully transferred to {result.target_tone} tone
                      </p>
                      <p className={`text-base ${darkMode ? 'text-gray-200' : 'text-gray-800'}`}>
                        {result.rephrased}
                      </p>
                    </div>

                    {result.tone_info && (
                      <div className={`p-4 rounded-lg ${darkMode ? 'bg-gray-700' : 'bg-gray-100'}`}>
                        <h4 className={`font-semibold mb-2 ${darkMode ? 'text-white' : 'text-gray-900'}`}>
                          {result.tone_info.description}
                        </h4>
                        <ul className={`text-sm space-y-1 ${darkMode ? 'text-gray-300' : 'text-gray-700'}`}>
                          {result.tone_info.characteristics?.map((char, idx) => (
                            <li key={idx}>• {char}</li>
                          ))}
                        </ul>
                      </div>
                    )}
                  </>
                ) : (
                  <div className={`p-4 rounded-lg ${darkMode ? 'bg-red-900/20' : 'bg-red-50'}`}>
                    <p className={`text-sm ${darkMode ? 'text-red-400' : 'text-red-700'}`}>
                      {result.error || 'Tone transfer failed'}
                    </p>
                  </div>
                )}
              </div>
            ) : (
              <p className={`text-center py-12 ${darkMode ? 'text-gray-400' : 'text-gray-500'}`}>
                Enter text and select a target tone to see the rephrased version
              </p>
            )}
          </div>
        </div>

        {/* Tone Examples */}
        {availableTones.length > 0 && (
          <div className={`mt-8 card ${darkMode ? 'bg-gray-800' : 'bg-white'}`}>
            <h2 className={`text-2xl font-semibold mb-4 ${darkMode ? 'text-white' : 'text-gray-900'}`}>
              Available Tones
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {availableTones.map((tone) => (
                <div
                  key={tone.name}
                  className={`p-4 rounded-lg border ${darkMode ? 'bg-gray-700 border-gray-600' : 'bg-gray-50 border-gray-200'}`}
                >
                  <h3 className={`font-semibold mb-2 ${darkMode ? 'text-white' : 'text-gray-900'}`}>
                    {tone.name.charAt(0).toUpperCase() + tone.name.slice(1)}
                  </h3>
                  <p className={`text-sm mb-2 ${darkMode ? 'text-gray-400' : 'text-gray-600'}`}>
                    {tone.description}
                  </p>
                  {tone.example && (
                    <p className={`text-xs italic ${darkMode ? 'text-gray-500' : 'text-gray-500'}`}>
                      "{tone.example}"
                    </p>
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

export default ToneTransfer

