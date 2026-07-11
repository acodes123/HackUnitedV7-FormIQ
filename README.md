# FormIQ – AI Basketball Shot Analyzer 🏀

Analyze your basketball shooting form from video using AI pose estimation.
Upload your shot and get instant feedback on elbow angle, knee bend, and release timing.

## Quick Start (Local Dev)

### Backend
```bash
cd backend
python -m venv venv
venv\Scripts\activate      # Windows
# source venv/bin/activate  # Mac/Linux
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:5173

## Deploy

### Backend → Render (Free, no credit card)

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy)

1. Click the button above, or go to [render.com](https://render.com) and sign up with GitHub (no credit card)
2. Click **New +** → **Web Service** → connect your GitHub repo
3. Set **Root Directory** to `backend/`
4. Render auto-detects the Dockerfile — click **Deploy**
5. You get a URL like `https://formiq-backend.onrender.com`
6. Copy that URL

### Frontend → Vercel

1. Go to [vercel.com](https://vercel.com) and import your GitHub repo
2. Vercel auto-detects the config — just deploy
3. Go to project **Settings → Environment Variables**
4. Add `VITE_API_URL = https://formiq-backend.onrender.com` (your Render URL)
5. Redeploy

That's it. Your frontend on Vercel talks to the backend on Render.

## How It Works

1. **Upload** an mp4 of your basketball shot
2. **Pose Detection**: MediaPipe Pose extracts body landmarks per frame
3. **Angle Math**: Law of cosines on shoulder→elbow→wrist and hip→knee→ankle
4. **Scoring** (out of 100):

| Rule | Points | Ideal |
|------|--------|-------|
| Elbow at release | 40 | 85°–100° |
| Knee bend | 30 | 130°–145° |
| Release timing | 30 | Wrist above shoulder |

5. **Results**: Score circle, skeleton overlay on key frames, feedback bullets

## Project Structure

```
├── frontend/            # React + Vite + Tailwind
│   ├── src/
│   │   ├── pages/      # UploadPage, ResultsPage
│   │   ├── components/ # VideoUploader, ScoreDisplay, FeedbackList
│   │   └── api.js      # Axios → backend
├── backend/             # Python FastAPI
│   ├── main.py         # API endpoints
│   ├── pose_analyzer.py # MediaPipe + angles
│   ├── rules.py        # Form rules + scoring
│   ├── schemas.py      # Pydantic models
│   ├── Dockerfile      # Render-ready
│   └── requirements.txt
├── sample_video/       # Test clip
├── render.yaml         # Render deploy config
├── vercel.json         # Vercel config
└── README.md
```

## Tech Stack

**Frontend**: React, Vite, Tailwind CSS, React Router, Axios
**Backend**: Python, FastAPI, MediaPipe Pose, OpenCV, NumPy
**Deploy**: Vercel (frontend) + Render (backend, free tier)
