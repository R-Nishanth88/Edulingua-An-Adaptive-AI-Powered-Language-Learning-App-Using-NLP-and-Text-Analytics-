export default function WordCloud({ errors }) {
  if (!errors || errors.length === 0) {
    return <p className="text-gray-500 text-center py-8">No error data available</p>
  }

  // Sort by frequency and take top 20
  const topErrors = errors
    .sort((a, b) => (b.frequency || 0) - (a.frequency || 0))
    .slice(0, 20)

  // Calculate size based on frequency
  const maxFreq = Math.max(...topErrors.map(e => e.frequency || 1))
  const minFreq = Math.min(...topErrors.map(e => e.frequency || 1))

  return (
    <div className="flex flex-wrap gap-3 justify-center p-6">
      {topErrors.map((error, idx) => {
        const frequency = error.frequency || 1
        const size = 12 + ((frequency - minFreq) / (maxFreq - minFreq || 1)) * 20
        const opacity = 0.6 + ((frequency - minFreq) / (maxFreq - minFreq || 1)) * 0.4

        return (
          <span
            key={idx}
            className="inline-block px-3 py-2 bg-red-100 text-red-800 rounded-lg font-semibold hover:bg-red-200 transition-colors cursor-pointer"
            style={{
              fontSize: `${size}px`,
              opacity: opacity
            }}
            title={`${error.type}: ${frequency} occurrences`}
          >
            {error.type}
          </span>
        )
      })}
    </div>
  )
}
