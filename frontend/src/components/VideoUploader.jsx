import { useState, useRef } from 'react'

export default function VideoUploader({ onFileSelected, loading }) {
  const [dragOver, setDragOver] = useState(false)
  const [preview, setPreview] = useState(null)
  const inputRef = useRef(null)

  const handleFile = (file) => {
    if (!file || !file.type.startsWith('video/')) return
    setPreview(URL.createObjectURL(file))
    onFileSelected(file)
  }

  const handleDrop = (e) => {
    e.preventDefault()
    setDragOver(false)
    handleFile(e.dataTransfer.files[0])
  }

  const handleChange = (e) => {
    handleFile(e.target.files[0])
  }

  return (
    <div className="flex flex-col items-center gap-6 w-full max-w-xl mx-auto">
      <div
        onDragOver={(e) => { e.preventDefault(); setDragOver(true) }}
        onDragLeave={() => setDragOver(false)}
        onDrop={handleDrop}
        onClick={() => inputRef.current?.click()}
        className={`w-full cursor-pointer rounded-2xl border-2 border-dashed p-12 text-center transition-all ${
          dragOver
            ? 'border-green-400 bg-green-400/10'
            : 'border-slate-600 bg-slate-800/50 hover:border-slate-500'
        }`}
      >
        <input
          ref={inputRef}
          type="file"
          accept="video/mp4,video/webm"
          onChange={handleChange}
          className="hidden"
        />
        <div className="text-5xl mb-4">🏀</div>
        <p className="text-lg font-medium text-slate-300">
          Drop your basketball shot video here
        </p>
        <p className="text-sm text-slate-500 mt-2">or click to browse (mp4)</p>
      </div>

      {preview && (
        <div className="w-full rounded-xl overflow-hidden border border-slate-700">
          <video src={preview} controls className="w-full max-h-64 bg-black" />
        </div>
      )}

      {loading && (
        <div className="flex items-center gap-3 text-slate-400">
          <svg className="animate-spin h-5 w-5" viewBox="0 0 24 24">
            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
          </svg>
          Analyzing your shot...
        </div>
      )}
    </div>
  )
}
