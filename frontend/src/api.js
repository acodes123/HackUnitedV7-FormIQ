import axios from 'axios'

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const api = axios.create({
  baseURL: API_BASE,
})

export async function analyzeVideo(file) {
  const form = new FormData()
  form.append('file', file)

  const path = API_BASE.includes('localhost') ? '/analyze' : '/api/analyze'

  const { data } = await api.post(path, form, {
    headers: { 'Content-Type': 'multipart/form-data' },
    timeout: 120000,
  })
  return data
}
