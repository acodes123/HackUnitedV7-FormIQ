export default function ScoreDisplay({ score }) {
  const getColor = () => {
    if (score >= 80) return 'text-green-400'
    if (score >= 50) return 'text-yellow-400'
    return 'text-red-400'
  }

  const getLabel = () => {
    if (score >= 80) return 'Great shot!'
    if (score >= 50) return 'Needs work'
    return 'Keep practicing'
  }

  return (
    <div className="flex flex-col items-center">
      <div className="relative w-40 h-40">
        <svg className="w-full h-full -rotate-90" viewBox="0 0 100 100">
          <circle cx="50" cy="50" r="42" fill="none" stroke="#1e293b" strokeWidth="8" />
          <circle
            cx="50" cy="50" r="42" fill="none"
            stroke="currentColor" strokeWidth="8"
            strokeLinecap="round"
            strokeDasharray={`${(score / 100) * 264} 264`}
            className={getColor()}
          />
        </svg>
        <div className="absolute inset-0 flex items-center justify-center">
          <span className={`text-5xl font-bold ${getColor()}`}>{score}</span>
        </div>
      </div>
      <span className="text-2xl font-semibold mt-2 text-slate-300">{getLabel()}</span>
      <span className="text-sm text-slate-500">out of 100</span>
    </div>
  )
}
