# FormIQ – AI Basketball Shot Analyzer 🏀

Analyze your basketball shooting form from video using AI pose estimation. Upload a video of your shot and get instant feedback on elbow angle, knee bend, and release timing.

## Project Structure

```
formiq/
├── backend/              # Python FastAPI server
│   ├── main.py           # API endpoints
│   ├── pose_analyzer.py  # MediaPipe pose detection + angle computation
│   ├── rules.py          # Basketball form rules + scoring
│   ├── schemas.py        # Pydantic response models
│   └── requirements.txt
├── frontend/             # React + Vite + Tailwind
│   ├── src/
│   │   ├── pages/        # UploadPage, ResultsPage
│   │   ├── components/   # VideoUploader, ScoreDisplay, FeedbackList
│   │   └── api.js        # Axios client
│   └── ...
├── sample_video/         # Test clips
└── README.md
```

## Setup

### Backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate    # Windows
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

Open http://localhost:5173 in your browser.

## How It Works

1. Upload an mp4 video of a basketball shot
2. Backend extracts key frames (start, max jump height, release point)
3. MediaPipe Pose detects body landmarks (shoulders, elbows, wrists, hips, knees, ankles)
4. Angle calculation using law of cosines:
   - **Elbow angle**: angle between shoulder → elbow → wrist
   - **Knee angle**: angle between hip → knee → ankle
5. Rule-based scoring:
   - Elbow at release: ideal 85°–100° (40 pts)
   - Knee bend: ideal 130°–145° (30 pts)
   - Release timing: wrist above shoulder at peak (30 pts)
6. Returns score (0–100), feedback bullets, and annotated frames

## Scoring

| Rule | Max Points | Ideal Range |
|------|-----------|-------------|
| Elbow angle | 40 | 85°–100° |
| Knee bend | 30 | 130°–145° |
| Release timing | 30 | Wrist above shoulder |

## Deployment

**Frontend** (Vercel):
```bash
cd frontend
npm run build
# Connect dist/ folder to Vercel or use Vercel CLI
```

Set `VITE_API_URL` environment variable to your deployed backend URL.

**Backend**: Deploy to Railway, Render, or Fly.io. The FastAPI app listens on port 8000 by default.

## Tech Stack

- **Frontend**: React, Vite, Tailwind CSS, React Router, Axios
- **Backend**: Python, FastAPI, MediaPipe, OpenCV, NumPy
