import { useState, useRef, useEffect } from 'react'
import { chatWithBot } from '../services/api'
import { Send, Bot, User } from 'lucide-react'

export default function Chatbot() {
  const [messages, setMessages] = useState([
    {
      role: 'bot',
      content: "Hello! I'm your AI English tutor. I can help you with grammar, vocabulary, writing tips, and answer your questions. What would you like to learn today?",
      suggestions: ["Grammar Help", "Vocabulary Tips", "Writing Advice", "Practice Quiz"]
    }
  ])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const messagesEndRef = useRef(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const handleSend = async (e) => {
    e.preventDefault()
    if (!input.trim() || loading) return

    const userMessage = input.trim()
    setInput('')
    setMessages(prev => [...prev, { role: 'user', content: userMessage }])
    setLoading(true)

    try {
      const response = await chatWithBot(userMessage)
      setMessages(prev => [...prev, {
        role: 'bot',
        content: response.data.response,
        suggestions: response.data.suggestions || []
      }])
    } catch (error) {
      console.error('Chat error:', error)
      setMessages(prev => [...prev, {
        role: 'bot',
        content: 'Sorry, I encountered an error. Please try again.'
      }])
    } finally {
      setLoading(false)
    }
  }

  const handleSuggestion = (suggestion) => {
    setInput(suggestion)
  }

  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 dark:text-gray-100 mb-2">AI Tutor Chatbot</h1>
        <p className="text-gray-600 dark:text-gray-400">
          Ask me anything about English grammar, vocabulary, or writing! I can also correct your sentences.
        </p>
      </div>

      <div className="card h-[600px] flex flex-col dark:bg-gray-800 dark:border-gray-700">
        {/* Messages */}
        <div className="flex-1 overflow-y-auto p-4 space-y-4">
          {messages.map((msg, idx) => (
            <div
              key={idx}
              className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'} animate-fade-in`}
            >
              <div
                className={`max-w-[80%] rounded-lg p-4 ${
                  msg.role === 'user'
                    ? 'bg-primary-600 text-white dark:bg-primary-700'
                    : 'bg-gray-100 dark:bg-gray-700 text-gray-900 dark:text-gray-100'
                }`}
              >
                <div className="flex items-start mb-2">
                  {msg.role === 'bot' ? (
                    <Bot className="w-5 h-5 mr-2 mt-0.5 flex-shrink-0" />
                  ) : (
                    <User className="w-5 h-5 mr-2 mt-0.5 flex-shrink-0" />
                  )}
                  <p className="whitespace-pre-wrap text-sm leading-relaxed">{msg.content}</p>
                </div>
                {msg.suggestions && msg.suggestions.length > 0 && (
                  <div className="mt-3 flex flex-wrap gap-2">
                    {msg.suggestions.map((suggestion, sIdx) => (
                      <button
                        key={sIdx}
                        onClick={() => handleSuggestion(suggestion)}
                        className={`text-xs px-3 py-1.5 rounded-full transition-all hover:scale-105 ${
                          msg.role === 'user'
                            ? 'bg-white/20 hover:bg-white/30 text-white'
                            : 'bg-primary-100 dark:bg-primary-900/30 hover:bg-primary-200 dark:hover:bg-primary-900/50 text-primary-700 dark:text-primary-300'
                        }`}
                      >
                        {suggestion}
                      </button>
                    ))}
                  </div>
                )}
              </div>
            </div>
          ))}
          {loading && (
            <div className="flex justify-start">
              <div className="bg-gray-100 dark:bg-gray-700 rounded-lg p-4">
                <div className="flex items-center space-x-2">
                  <Bot className="w-5 h-5 text-gray-400" />
                  <div className="flex space-x-1">
                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                  </div>
                </div>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        {/* Input */}
        <form onSubmit={handleSend} className="border-t border-gray-200 dark:border-gray-700 p-4">
          <div className="flex gap-2">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Ask me anything about English..."
              className="flex-1 input-field dark:bg-gray-700 dark:text-white dark:border-gray-600"
              disabled={loading}
            />
            <button
              type="submit"
              disabled={loading || !input.trim()}
              className="btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <Send className="w-5 h-5" />
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}
