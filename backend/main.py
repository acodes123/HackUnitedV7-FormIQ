import os
import sys
import traceback
from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="FormIQ – Basketball Shot Analyzer")
router = APIRouter(prefix="/api")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@router.get("/health")
async def health():
    return {"status": "ok", "message": "minimal health check works"}


@router.post("/analyze")
async def analyze_video(file: bytes = None):
    try:
        import cv2
        import numpy as np
        import mediapipe as mp
        from pose_analyzer import PoseAnalyzer
        from rules import evaluate_elbow, evaluate_knee, evaluate_release
        from schemas import AnalyzeResponse

        return {"status": "imports_ok"}
    except Exception as e:
        return {"status": "import_failed", "error": str(e), "traceback": traceback.format_exc()}


app.include_router(router)
