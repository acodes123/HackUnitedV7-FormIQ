const GOOD = '✓'
const WARN = '!'
const BAD = '✗'

function getIcon(text) {
  const lower = text.toLowerCase()
  if (lower.startsWith('good')) return { icon: GOOD, color: 'text-green-400' }
  if (lower.startsWith('could not')) return { icon: WARN, color: 'text-yellow-400' }
  return { icon: BAD, color: 'text-red-400' }
}

export default function FeedbackList({ feedback }) {
  return (
    <div className="space-y-3">
      <h3 className="text-lg font-semibold text-slate-300 mb-4">Feedback</h3>
      {feedback.map((item, i) => {
        const { icon, color } = getIcon(item)
        return (
          <div
            key={i}
            className="flex items-start gap-3 bg-slate-800/50 rounded-lg px-4 py-3 border border-slate-700/50"
          >
            <span className={`text-lg font-bold mt-0.5 ${color}`}>{icon}</span>
            <span className="text-sm text-slate-300">{item}</span>
          </div>
        )
      })}
    </div>
  )
}
