export default function ResultCard({ icon, title, value, color = "text-primary-600", gradient, hoverGradient }) {
  return (
    <div className={`card hover-lift group ${gradient ? 'overflow-hidden' : ''}`}>
      {gradient && (
        <div className={`absolute inset-0 bg-gradient-to-br ${gradient} ${hoverGradient || ''} opacity-10 group-hover:opacity-20 transition-opacity duration-300`}></div>
      )}
      <div className="flex items-center relative z-10">
        <div className={`${gradient ? `p-4 rounded-2xl bg-gradient-to-br ${gradient} text-white shadow-lg transform group-hover:scale-110 group-hover:rotate-6 transition-all duration-300` : color} mr-4`}>
          {icon}
        </div>
        <div>
          <p className="text-sm font-semibold text-gray-600 dark:text-gray-400 uppercase tracking-wide">{title}</p>
          <p className={`text-3xl font-bold ${gradient ? 'bg-gradient-to-r ' + gradient + ' bg-clip-text text-transparent' : 'text-gray-900 dark:text-white'}`}>
            {value}
          </p>
        </div>
      </div>
    </div>
  )
}
