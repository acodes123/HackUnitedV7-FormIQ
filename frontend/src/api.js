import axios from 'axios'

const isLocal = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
const API_BASE = import.meta.env.VITE_API_URL || (isLocal ? 'http://localhost:8000' : '')

const api = axios.create({
  baseURL: API_BASE,
})

export async function analyzeVideo(file) {
  const form = new FormData()
  form.append('file', file)

  const path = API_BASE ? '/analyze' : '/api/analyze'

  const { data } = await api.post(path, form, {
    headers: { 'Content-Type': 'multipart/form-data' },
    timeout: 120000,
  })
  return data
}
