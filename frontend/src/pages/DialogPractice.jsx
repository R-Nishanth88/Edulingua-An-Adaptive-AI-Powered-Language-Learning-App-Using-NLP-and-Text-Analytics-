import { useState } from 'react'
import { MessageSquare, Send, Sparkles, CheckCircle, XCircle } from 'lucide-react'
import { generateDialog, generateDialogResponse, evaluateDialog } from '../services/api'

export default function DialogPractice() {
  const [topic, setTopic] = useState('introductions')
  const [level, setLevel] = useState('B1')
  const [dialog, setDialog] = useState(null)
  const [userInput, setUserInput] = useState('')
  const [conversation, setConversation] = useState([])
  const [evaluation, setEvaluation] = useState(null)
  const [loading, setLoading] = useState(false)

  const handleGenerateDialog = async () => {
    setLoading(true)
    try {
      const response = await generateDialog({ topic, level, num_exchanges: 5 })
      setDialog(response.data)
      setConversation(response.data.exchanges || [])
      setEvaluation(null)
    } catch (error) {
      console.error('Error generating dialog:', error)
      alert('Failed to generate dialog. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  const handleSendMessage = async () => {
    if (!userInput.trim()) return

    const userMessage = {
      speaker: 'You',
      text: userInput,
      type: 'user_input'
    }
    const updatedConversation = [...conversation, userMessage]
    setConversation(updatedConversation)
    setUserInput('')

    try {
      const response = await generateDialogResponse({
        user_input: userInput,
        context: conversation,
        topic
      })
      
      const aiMessage = {
        speaker: 'AI Tutor',
        text: response.data.response || "I understand. Can you tell me more?",
        type: response.data.type || 'response'
      }
      setConversation([...updatedConversation, aiMessage])
    } catch (error) {
      console.error('Error generating response:', error)
      const errorMessage = {
        speaker: 'AI Tutor',
        text: "I'm sorry, I didn't understand that. Could you rephrase?",
        type: 'error'
      }
      setConversation([...updatedConversation, errorMessage])
    }
  }

  const handleEvaluate = async (userResponse, expectedResponse) => {
    try {
      const response = await evaluateDialog({
        user_response: userResponse,
        expected_response: expectedResponse,
        context: conversation
      })
      setEvaluation(response.data)
    } catch (error) {
      console.error('Error evaluating:', error)
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 dark:from-gray-900 dark:to-gray-800 p-6">
      <div className="max-w-6xl mx-auto">
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-900 dark:text-white mb-2">
            <MessageSquare className="inline-block mr-3" />
            Dialog Practice
          </h1>
          <p className="text-gray-600 dark:text-gray-300">
            Practice conversational English with AI-generated scenarios
          </p>
        </div>

        {/* Dialog Generator */}
        <div className="card mb-6">
          <h2 className="text-2xl font-semibold mb-4 text-gray-800 dark:text-gray-200">
            Generate Conversation
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
            <div>
              <label className="block text-sm font-medium mb-2 text-gray-700 dark:text-gray-300">
                Topic
              </label>
              <select
                value={topic}
                onChange={(e) => setTopic(e.target.value)}
                className="input-field dark:bg-gray-700 dark:text-white"
              >
                <option value="introductions">Introductions</option>
                <option value="ordering_food">Ordering Food</option>
                <option value="job_interview">Job Interview</option>
                <option value="shopping">Shopping</option>
                <option value="travel">Travel</option>
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium mb-2 text-gray-700 dark:text-gray-300">
                Level
              </label>
              <select
                value={level}
                onChange={(e) => setLevel(e.target.value)}
                className="input-field dark:bg-gray-700 dark:text-white"
              >
                <option value="A1">A1 - Beginner</option>
                <option value="A2">A2 - Elementary</option>
                <option value="B1">B1 - Intermediate</option>
                <option value="B2">B2 - Upper Intermediate</option>
                <option value="C1">C1 - Advanced</option>
              </select>
            </div>
            <div className="flex items-end">
              <button
                onClick={handleGenerateDialog}
                disabled={loading}
                className="btn-primary w-full flex items-center justify-center"
              >
                {loading ? (
                  <span className="animate-spin">⏳</span>
                ) : (
                  <>
                    <Sparkles className="mr-2" size={20} />
                    Generate Dialog
                  </>
                )}
              </button>
            </div>
          </div>
        </div>

        {/* Dialog Display */}
        {dialog && (
          <div className="card mb-6">
            <h3 className="text-xl font-semibold mb-4 text-gray-800 dark:text-gray-200">
              Scenario: {dialog.scenario}
            </h3>
            <div className="space-y-4">
              {conversation.map((exchange, idx) => (
                <div
                  key={idx}
                  className={`p-4 rounded-lg ${
                    exchange.speaker === 'You'
                      ? 'bg-blue-100 dark:bg-blue-900/30 ml-8'
                      : 'bg-gray-100 dark:bg-gray-700 mr-8'
                  }`}
                >
                  <div className="flex items-start">
                    <div className="flex-1">
                      <p className="font-semibold text-gray-800 dark:text-gray-200">
                        {exchange.speaker}:
                      </p>
                      <p className="text-gray-700 dark:text-gray-300 mt-1">
                        {exchange.text}
                      </p>
                    </div>
                    {exchange.type === 'user_input' && dialog.exchanges[idx] && (
                      <button
                        onClick={() => handleEvaluate(exchange.text, dialog.exchanges[idx]?.text)}
                        className="btn-secondary text-sm ml-2"
                      >
                        Evaluate
                      </button>
                    )}
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* User Input */}
        {dialog && (
          <div className="card">
            <div className="flex gap-2">
              <input
                type="text"
                value={userInput}
                onChange={(e) => setUserInput(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
                placeholder="Type your response..."
                className="input-field flex-1 dark:bg-gray-700 dark:text-white"
              />
              <button
                onClick={handleSendMessage}
                className="btn-primary flex items-center"
              >
                <Send size={20} />
              </button>
            </div>
          </div>
        )}

        {/* Evaluation Result */}
        {evaluation && (
          <div className="card mt-6 bg-green-50 dark:bg-green-900/20 border-l-4 border-green-500">
            <h3 className="text-xl font-semibold mb-4 text-green-800 dark:text-green-300">
              Evaluation Result
            </h3>
            <div className="space-y-2">
              <div className="flex items-center justify-between">
                <span className="text-gray-700 dark:text-gray-300">Overall Score:</span>
                <span className="font-bold text-green-700 dark:text-green-400">
                  {evaluation.score}%
                </span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-gray-700 dark:text-gray-300">Similarity:</span>
                <span className="font-semibold">{evaluation.similarity_score}%</span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-gray-700 dark:text-gray-300">Grammar:</span>
                <span className="font-semibold">{evaluation.grammar_score}%</span>
              </div>
              {evaluation.feedback && evaluation.feedback.length > 0 && (
                <div className="mt-4">
                  <p className="font-semibold mb-2">Feedback:</p>
                  <ul className="list-disc list-inside space-y-1">
                    {evaluation.feedback.map((fb, idx) => (
                      <li key={idx} className="text-gray-700 dark:text-gray-300">{fb}</li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

