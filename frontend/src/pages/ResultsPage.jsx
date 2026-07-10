import { useLocation, useNavigate } from 'react-router-dom'
import ScoreDisplay from '../components/ScoreDisplay'
import FeedbackList from '../components/FeedbackList'

export default function ResultsPage() {
  const location = useLocation()
  const navigate = useNavigate()
  const data = location.state

  if (!data) {
    navigate('/')
    return null
  }

  const { score, feedback, angles, annotated_frames, videoUrl } = data
  const hasFrames = annotated_frames && annotated_frames.length > 0

  return (
    <div className="min-h-screen px-4 py-8 max-w-5xl mx-auto">
      <button
        onClick={() => navigate('/')}
        className="text-sm text-slate-500 hover:text-slate-300 transition-colors mb-6 flex items-center gap-1"
      >
        ← Back
      </button>

      <h1 className="text-3xl font-bold mb-8 text-center">
        Your Shot Analysis
      </h1>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Left column: video + skeleton */}
        <div className="space-y-6">
          {hasFrames && (
            <div className="rounded-xl overflow-hidden border border-slate-700 bg-black">
              <div className="flex flex-col gap-1">
                {annotated_frames.map((b64, i) => (
                  <img
                    key={i}
                    src={`data:image/jpeg;base64,${b64}`}
                    alt={`Frame ${i + 1}`}
                    className="w-full"
                  />
                ))}
              </div>
              <div className="px-4 py-2 text-xs text-slate-500 bg-slate-900">
                Skeleton overlay on key frames (start, peak jump, release)
              </div>
            </div>
          )}

          {videoUrl && (
            <div className="rounded-xl overflow-hidden border border-slate-700">
              <video src={videoUrl} controls className="w-full bg-black max-h-72" />
              <div className="px-4 py-2 text-xs text-slate-500 bg-slate-900">
                Original upload
              </div>
            </div>
          )}
        </div>

        {/* Right column: score + feedback */}
        <div className="space-y-8">
          <ScoreDisplay score={score} />

          {angles.elbow > 0 && (
            <div className="bg-slate-800/50 rounded-xl p-5 border border-slate-700/50">
              <h3 className="text-sm font-semibold text-slate-400 mb-3">Measured Angles</h3>
              <div className="grid grid-cols-2 gap-4">
                <div className="bg-slate-900/50 rounded-lg p-3 text-center">
                  <div className="text-2xl font-bold text-green-400">{angles.elbow}°</div>
                  <div className="text-xs text-slate-500 mt-1">Elbow Angle</div>
                </div>
                <div className="bg-slate-900/50 rounded-lg p-3 text-center">
                  <div className="text-2xl font-bold text-yellow-400">{angles.knee}°</div>
                  <div className="text-xs text-slate-500 mt-1">Knee Angle</div>
                </div>
              </div>
            </div>
          )}

          <FeedbackList feedback={feedback} />

          <button
            onClick={() => navigate('/')}
            className="w-full py-3 bg-green-600 hover:bg-green-500 rounded-xl font-semibold transition-colors"
          >
            Analyze another shot
          </button>
        </div>
      </div>
    </div>
  )
}
