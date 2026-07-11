import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import VideoUploader from '../components/VideoUploader'
import { analyzeVideo } from '../api'

export default function UploadPage() {
  const navigate = useNavigate()
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const handleFile = async (file) => {
    setLoading(true)
    setError(null)
    try {
      const result = await analyzeVideo(file)
      navigate('/results', { state: { ...result, videoUrl: URL.createObjectURL(file) } })
    } catch (err) {
      setError(err.response?.data?.detail || err.message || 'Analysis failed. Try again.')
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen flex flex-col items-center justify-center px-4 py-12">
      <div className="text-center mb-10">
        <h1 className="text-5xl font-bold mb-2">
          Form<span className="text-green-400">IQ</span>
        </h1>
        <p className="text-slate-400 text-lg">AI Basketball Shot Analyzer</p>
        <p className="text-slate-600 text-sm mt-1">Upload your shot video for instant form feedback</p>
      </div>

      <VideoUploader onFileSelected={handleFile} loading={loading} />

      {error && (
        <div className="mt-6 px-6 py-3 bg-red-900/40 border border-red-700 rounded-xl text-red-300 text-sm">
          {error}
        </div>
      )}
    </div>
  )
}
