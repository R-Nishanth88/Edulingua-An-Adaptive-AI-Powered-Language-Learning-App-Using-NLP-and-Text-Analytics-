export default function GrammarHighlight({ text, errors }) {
  if (!errors || errors.length === 0) {
    return <p className="text-gray-700">{text}</p>
  }

  // Sort errors by start position
  const sortedErrors = [...errors].sort((a, b) => a.start - b.start)
  
  let highlightedText = []
  let lastIndex = 0

  sortedErrors.forEach((error, idx) => {
    // Add text before error
    if (error.start > lastIndex) {
      highlightedText.push(
        <span key={`text-${idx}`}>{text.substring(lastIndex, error.start)}</span>
      )
    }

    // Add highlighted error
    highlightedText.push(
      <span
        key={`error-${idx}`}
        className="bg-red-100 text-red-800 underline cursor-help"
        title={`${error.message || error.type}: ${error.explanation || ''}`}
      >
        {text.substring(error.start, Math.min(error.end, text.length))}
      </span>
    )

    lastIndex = Math.min(error.end, text.length)
  })

  // Add remaining text
  if (lastIndex < text.length) {
    highlightedText.push(
      <span key="text-end">{text.substring(lastIndex)}</span>
    )
  }

  return (
    <div className="text-gray-700">
      <p className="mb-2">{highlightedText}</p>
      <div className="mt-3 space-y-1">
        {sortedErrors.slice(0, 5).map((error, idx) => (
          <div key={idx} className="text-sm text-red-700 bg-red-50 p-2 rounded">
            <span className="font-semibold">{error.type}:</span> {error.message || error.explanation}
          </div>
        ))}
      </div>
    </div>
  )
}
