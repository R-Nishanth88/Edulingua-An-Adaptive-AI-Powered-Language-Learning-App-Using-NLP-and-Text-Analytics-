import { useState } from 'react'
import { analyzeText, summarizeText, generateQuestions, getRecommendations, updateXP } from '../services/api'
import TextAnalyzer from '../components/TextAnalyzer'
import ResultCard from '../components/ResultCard'
import GrammarHighlight from '../components/GrammarHighlight'
import { FileText, BookOpen, Lightbulb, TrendingUp, Award } from 'lucide-react'

export default function Dashboard({ user }) {
  const [text, setText] = useState('')
  const [results, setResults] = useState(null)
  const [summary, setSummary] = useState(null)
  const [questions, setQuestions] = useState([])
  const [recommendations, setRecommendations] = useState([])
  const [loading, setLoading] = useState(false)
  const [activeTab, setActiveTab] = useState('analysis')

  const handleAnalyze = async () => {
    if (!text.trim() || text.length < 10) {
      alert('Please enter at least 10 characters of text.')
      return
    }

    setLoading(true)
    try {
      const analysisResponse = await analyzeText({ text })
      setResults(analysisResponse.data)
      setActiveTab('analysis')

      // Award XP for analysis
      await updateXP({
        points: 10,
        reason: 'Text analysis completed'
      })

      // Fetch recommendations
      const recResponse = await getRecommendations()
      setRecommendations(recResponse.data.recommendations || [])
    } catch (error) {
      console.error('Analysis error:', error)
      alert('Error analyzing text. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  const handleSummarize = async () => {
    if (!text.trim()) {
      alert('Please enter some text first.')
      return
    }

    setLoading(true)
    try {
      const response = await summarizeText({ text })
      setSummary(response.data)
      setActiveTab('summary')
    } catch (error) {
      console.error('Summarization error:', error)
      alert('Error generating summary. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  const handleGenerateQuiz = async () => {
    if (!text.trim()) {
      alert('Please enter some text first.')
      return
    }

    setLoading(true)
    try {
      const response = await generateQuestions({ text })
      setQuestions(response.data.questions || [])
      setActiveTab('quiz')
    } catch (error) {
      console.error('Question generation error:', error)
      alert('Error generating questions. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="mb-8">
        <div className="flex items-center gap-3 mb-4">
          <h1 className="text-4xl sm:text-5xl font-bold text-gradient">📊 Dashboard</h1>
          <div className="hidden sm:block animate-bounce-slow">🎉</div>
        </div>
        <p className="text-lg text-gray-600 dark:text-gray-400">
          Welcome back, <span className="font-bold text-blue-600 dark:text-blue-400">{user?.username}</span>! Analyze your English writing and improve your skills.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
        <ResultCard
          icon={<Award className="w-8 h-8" />}
          title="CEFR Level"
          value={user?.cefr_level || 'A1'}
          gradient="from-yellow-400 via-orange-500 to-red-500"
          hoverGradient="hover:from-yellow-500 hover:via-orange-600 hover:to-red-600"
        />
        <ResultCard
          icon={<TrendingUp className="w-8 h-8" />}
          title="XP Points"
          value={user?.xp_points || 0}
          gradient="from-green-400 via-emerald-500 to-teal-500"
          hoverGradient="hover:from-green-500 hover:via-emerald-600 hover:to-teal-600"
        />
        <ResultCard
          icon={<BookOpen className="w-8 h-8" />}
          title="Status"
          value="Active"
          gradient="from-blue-400 via-cyan-500 to-blue-500"
          hoverGradient="hover:from-blue-500 hover:via-cyan-600 hover:to-blue-600"
        />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Input Panel */}
        <div className="card hover-lift glow-effect">
          <h2 className="text-2xl font-bold mb-6 flex items-center text-gradient">
            <div className="p-2 rounded-xl bg-gradient-to-br from-blue-500 to-purple-500 text-white mr-3 shadow-lg">
              <FileText className="w-6 h-6" />
            </div>
            Text Input
          </h2>
          <TextAnalyzer
            text={text}
            setText={setText}
            onAnalyze={handleAnalyze}
            onSummarize={handleSummarize}
            onGenerateQuiz={handleGenerateQuiz}
            loading={loading}
          />
        </div>

        {/* Results Panel */}
        <div className="card hover-lift">
          <div className="flex flex-wrap gap-2 border-b-2 border-gray-200/50 dark:border-gray-700/50 mb-6 pb-2">
            <button
              onClick={() => setActiveTab('analysis')}
              className={`px-5 py-2.5 font-bold rounded-xl transition-all duration-300 transform hover:scale-105 ${
                activeTab === 'analysis'
                  ? 'bg-gradient-to-r from-blue-500 to-purple-500 text-white shadow-lg scale-105'
                  : 'text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700'
              }`}
            >
              📊 Analysis
            </button>
            <button
              onClick={() => setActiveTab('summary')}
              className={`px-5 py-2.5 font-bold rounded-xl transition-all duration-300 transform hover:scale-105 ${
                activeTab === 'summary'
                  ? 'bg-gradient-to-r from-purple-500 to-pink-500 text-white shadow-lg scale-105'
                  : 'text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700'
              }`}
            >
              📄 Summary
            </button>
            <button
              onClick={() => setActiveTab('quiz')}
              className={`px-5 py-2.5 font-bold rounded-xl transition-all duration-300 transform hover:scale-105 ${
                activeTab === 'quiz'
                  ? 'bg-gradient-to-r from-green-500 to-emerald-500 text-white shadow-lg scale-105'
                  : 'text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700'
              }`}
            >
              🎯 Quiz
            </button>
            <button
              onClick={() => setActiveTab('recommendations')}
              className={`px-5 py-2.5 font-bold rounded-xl transition-all duration-300 transform hover:scale-105 ${
                activeTab === 'recommendations'
                  ? 'bg-gradient-to-r from-yellow-500 to-orange-500 text-white shadow-lg scale-105'
                  : 'text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700'
              }`}
            >
              💡 Recommendations
            </button>
          </div>

          <div className="mt-4">
            {activeTab === 'analysis' && results && (
              <AnalysisResults results={results} originalText={text} />
            )}
            {activeTab === 'summary' && summary && (
              <SummaryResults summary={summary} />
            )}
            {activeTab === 'quiz' && questions.length > 0 && (
              <QuizResults questions={questions} />
            )}
            {activeTab === 'recommendations' && (
              <RecommendationsList recommendations={recommendations} />
            )}
            {!results && !summary && questions.length === 0 && activeTab === 'analysis' && (
              <p className="text-gray-500 dark:text-gray-400 text-center py-8">
                Enter text and click "Analyze" to see results
              </p>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}

function AnalysisResults({ results, originalText }) {
  return (
    <div className="space-y-4">
      {/* Corrected Sentence */}
      {results.grammar?.corrected_text && results.grammar.corrected_text !== originalText && (
        <div className="bg-green-50 dark:bg-green-900/20 border-l-4 border-green-500 pl-4 py-3 rounded-r-lg">
          <h3 className="font-semibold text-green-700 dark:text-green-400 mb-2">✓ Corrected Sentence</h3>
          <p className="text-sm text-gray-800 dark:text-gray-200 font-medium mb-1">Original:</p>
          <p className="text-sm text-gray-600 dark:text-gray-400 mb-3 italic">{originalText}</p>
          <p className="text-sm text-gray-800 dark:text-gray-200 font-medium mb-1">Corrected:</p>
          <p className="text-sm text-green-700 dark:text-green-300 font-semibold">{results.grammar.corrected_text}</p>
        </div>
      )}

      {/* Rephrasing Suggestions */}
      {results.rephrasing?.suggestions && results.rephrasing.suggestions.length > 0 && (
        <div className="bg-blue-50 dark:bg-blue-900/20 border-l-4 border-blue-500 pl-4 py-3 rounded-r-lg">
          <h3 className="font-semibold text-blue-700 dark:text-blue-400 mb-2">💡 Rephrasing Suggestions</h3>
          <div className="space-y-3">
            {results.rephrasing.suggestions.map((suggestion, idx) => (
              <div key={idx} className="text-sm">
                <p className="text-gray-600 dark:text-gray-400 mb-1 italic">{suggestion.explanation}</p>
                <p className="text-gray-800 dark:text-gray-200 font-medium mb-1">Original:</p>
                <p className="text-gray-600 dark:text-gray-400 mb-2">{suggestion.original}</p>
                <p className="text-gray-800 dark:text-gray-200 font-medium mb-1">Suggestion:</p>
                <p className="text-blue-700 dark:text-blue-300 font-semibold">{suggestion.suggestion}</p>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Grammar Errors */}
      <div className="border-l-4 border-red-500 dark:border-red-400 pl-4">
        <h3 className="font-semibold text-red-700 dark:text-red-400 mb-2">Grammar Errors ({results.grammar?.error_count || 0})</h3>
        {results.grammar?.errors?.length > 0 ? (
          <div className="space-y-2">
            <GrammarHighlight text={originalText} errors={results.grammar.errors} />
            <div className="mt-3 space-y-2">
              {results.grammar.errors.slice(0, 5).map((error, idx) => (
                <div key={idx} className="bg-red-50 dark:bg-red-900/20 p-3 rounded-lg text-sm">
                  <p className="font-semibold text-red-700 dark:text-red-400 mb-1">{error.type}: {error.message}</p>
                  {error.suggested_correction && (
                    <p className="text-gray-700 dark:text-gray-300">
                      <span className="text-red-600 dark:text-red-400">Error: </span>
                      <span className="line-through">{error.text}</span>
                      {' → '}
                      <span className="text-green-600 dark:text-green-400 font-semibold">{error.suggested_correction}</span>
                    </p>
                  )}
                  {error.explanation && (
                    <p className="text-gray-600 dark:text-gray-400 mt-1 italic">{error.explanation}</p>
                  )}
                </div>
              ))}
            </div>
          </div>
        ) : (
          <p className="text-green-600 dark:text-green-400 text-sm">✓ No grammar errors detected!</p>
        )}
      </div>

      {/* Readability */}
      <div className="border-l-4 border-blue-500 dark:border-blue-400 pl-4">
        <h3 className="font-semibold text-blue-700 dark:text-blue-400 mb-2">Readability</h3>
        <p className="text-sm">
          <span className="font-semibold">CEFR Level:</span> {results.readability?.cefr_level}
        </p>
        <p className="text-sm">
          <span className="font-semibold">Flesch Reading Ease:</span> {results.readability?.flesch_reading_ease}
        </p>
        <p className="text-sm text-gray-600 dark:text-gray-400">{results.readability?.interpretation}</p>
      </div>

      {/* Vocabulary */}
      <div className="border-l-4 border-green-500 dark:border-green-400 pl-4">
        <h3 className="font-semibold text-green-700 dark:text-green-400 mb-2">Vocabulary</h3>
        <p className="text-sm">
          <span className="font-semibold">Lexical Diversity (TTR):</span> {results.vocabulary?.lexical_diversity?.ttr}
        </p>
        <p className="text-sm">
          <span className="font-semibold">Unique Words:</span> {results.vocabulary?.lexical_diversity?.unique_words}
        </p>
      </div>

      {/* Tone & Style */}
      <div className="border-l-4 border-purple-500 dark:border-purple-400 pl-4">
        <h3 className="font-semibold text-purple-700 dark:text-purple-400 mb-2">Tone & Style</h3>
        <p className="text-sm">
          <span className="font-semibold">Tone:</span> {results.tone_style?.tone}
        </p>
        <p className="text-sm">
          <span className="font-semibold">Formality:</span> {results.tone_style?.formality}
        </p>
        <p className="text-sm">
          <span className="font-semibold">Sentiment:</span> {results.tone_style?.sentiment?.label}
        </p>
      </div>

      {/* Proficiency */}
      <div className="border-l-4 border-yellow-500 dark:border-yellow-400 pl-4">
        <h3 className="font-semibold text-yellow-700 dark:text-yellow-400 mb-2">Proficiency Prediction</h3>
        <p className="text-sm">
          <span className="font-semibold">Predicted Level:</span> {results.proficiency?.cefr_level}
        </p>
        <p className="text-sm">
          <span className="font-semibold">Confidence:</span> {(results.proficiency?.confidence * 100).toFixed(1)}%
        </p>
      </div>
    </div>
  )
}

function SummaryResults({ summary }) {
  return (
    <div>
      <h3 className="font-semibold mb-3">Summary</h3>
      <p className="text-gray-700 mb-4">{summary.summary}</p>
      <div className="text-sm text-gray-600">
        <p>Original: {summary.original_length} words</p>
        <p>Summary: {summary.summary_length} words</p>
        <p>Compression: {(summary.compression_ratio * 100).toFixed(1)}%</p>
      </div>
    </div>
  )
}

function QuizResults({ questions }) {
  return (
    <div>
      <h3 className="font-semibold mb-3">Comprehension Questions</h3>
      <div className="space-y-4">
        {questions.map((q, idx) => (
          <div key={idx} className="border border-gray-200 rounded-lg p-4">
            <p className="font-semibold mb-2">{idx + 1}. {q.question}</p>
            {q.hint && (
              <p className="text-sm text-gray-600 italic">Hint: {q.hint}</p>
            )}
          </div>
        ))}
      </div>
    </div>
  )
}

function RecommendationsList({ recommendations }) {
  if (recommendations.length === 0) {
    return (
      <div className="text-center py-8">
        <Lightbulb className="w-12 h-12 text-gray-400 mx-auto mb-2" />
        <p className="text-gray-500">No recommendations available yet. Analyze some text first!</p>
      </div>
    )
  }

  return (
    <div>
      <h3 className="font-semibold mb-3">Learning Recommendations</h3>
      <div className="space-y-3">
        {recommendations.map((rec, idx) => (
          <a
            key={idx}
            href={rec.link}
            target="_blank"
            rel="noopener noreferrer"
            className="block border border-gray-200 rounded-lg p-4 hover:bg-gray-50 transition-colors"
          >
            <p className="font-semibold text-primary-600">{rec.content_title}</p>
            <p className="text-sm text-gray-600 mt-1">{rec.description}</p>
            <span className="inline-block mt-2 text-xs bg-primary-100 text-primary-700 px-2 py-1 rounded">
              {rec.difficulty}
            </span>
          </a>
        ))}
      </div>
    </div>
  )
}
