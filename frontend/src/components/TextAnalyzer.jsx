import { FileText, Sparkles, BookOpen } from 'lucide-react'

export default function TextAnalyzer({
  text,
  setText,
  onAnalyze,
  onSummarize,
  onGenerateQuiz,
  loading
}) {
  return (
    <div className="space-y-4">
      <div className="relative">
        <textarea
          value={text}
          onChange={(e) => setText(e.target.value)}
          placeholder="✨ Enter or paste your English text here for analysis..."
          className="w-full h-64 input-field resize-none font-medium"
          disabled={loading}
        />
        {text && (
          <div className="absolute bottom-3 right-3 flex gap-2">
            <span className="badge badge-primary text-xs">
              {text.length} chars
            </span>
            <span className="badge badge-success text-xs">
              {text.split(/\s+/).filter(Boolean).length} words
            </span>
          </div>
        )}
      </div>
      <div className="flex flex-wrap gap-3">
        <button
          onClick={onAnalyze}
          disabled={loading || !text.trim()}
          className="btn-primary flex items-center justify-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none"
        >
          <FileText className="w-5 h-5" />
          {loading ? (
            <>
              <span className="animate-spin">⚙️</span> Analyzing...
            </>
          ) : (
            '🚀 Analyze'
          )}
        </button>
        <button
          onClick={onSummarize}
          disabled={loading || !text.trim()}
          className="btn-secondary flex items-center justify-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none"
        >
          <Sparkles className="w-5 h-5" />
          ✨ Summarize
        </button>
        <button
          onClick={onGenerateQuiz}
          disabled={loading || !text.trim()}
          className="btn-secondary flex items-center justify-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none"
        >
          <BookOpen className="w-5 h-5" />
          📚 Generate Quiz
        </button>
      </div>
    </div>
  )
}
