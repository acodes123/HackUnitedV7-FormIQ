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

### Frontend → Vercel
[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new)
1. Connect your GitHub repo
2. Vercel auto-detects the `vercel.json` config
3. Set `VITE_API_URL` env var to your deployed Railway backend URL

### Backend → Railway
[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new)
1. Click the button or create a new Railway project
2. Connect your GitHub repo, set root directory to `backend/`
3. Railway auto-detects the `Dockerfile`
4. It deploys at `https://your-app.up.railway.app`
5. Copy that URL → set as `VITE_API_URL` in Vercel

Or deploy manually:
```bash
# Install Railway CLI
npm i -g @railway/cli
railway login
railway init
railway up --root-dir backend
```

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
├── frontend/          # React + Vite + Tailwind
│   ├── src/
│   │   ├── pages/     # UploadPage, ResultsPage
│   │   ├── components/ # VideoUploader, ScoreDisplay, FeedbackList
│   │   └── api.js     # Axios → backend
│   └── vercel.json
├── backend/           # Python FastAPI
│   ├── main.py        # API endpoints
│   ├── pose_analyzer.py # MediaPipe + angles
│   ├── rules.py       # Form rules + scoring
│   ├── schemas.py     # Pydantic models
│   ├── Dockerfile     # Railway-ready
│   └── requirements.txt
├── sample_video/      # Test clip
├── vercel.json        # Vercel monorepo config
└── README.md
```

## Tech Stack

**Frontend**: React, Vite, Tailwind CSS, React Router, Axios
**Backend**: Python, FastAPI, MediaPipe Pose, OpenCV, NumPy
