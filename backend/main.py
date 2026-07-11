import os
import uuid
import cv2
import base64
import numpy as np
from fastapi import FastAPI, UploadFile, File, APIRouter
from fastapi.middleware.cors import CORSMiddleware

from pose_analyzer import PoseAnalyzer
from rules import evaluate_elbow, evaluate_knee, evaluate_release, calculate_score
from schemas import AnalyzeResponse

app = FastAPI(title="FormIQ – Basketball Shot Analyzer")
router = APIRouter(prefix="/api")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

analyzer = PoseAnalyzer()

TEMP_DIR = "temp_videos"
os.makedirs(TEMP_DIR, exist_ok=True)


def encode_frame(frame: np.ndarray) -> str:
    """Convert OpenCV frame (BGR) to base64 JPEG string for frontend display."""
    _, buffer = cv2.imencode(".jpg", frame, [cv2.IMWRITE_JPEG_QUALITY, 80])
    return base64.b64encode(buffer).decode("utf-8")


def find_key_frames(video_path: str):
    """
    Extract 3 key frames from the video:
    1. Start of motion (first frame with pose detected)
    2. Maximum jump height (frame where hip y is smallest)
    3. Release point (frame where wrist y is smallest relative to shoulder)
    """
    cap = cv2.VideoCapture(video_path)
    frames = []
    annotated_raw = []

    frame_idx = 0
    max_jump_frame = None
    min_hip_y = float("inf")
    release_frame = None
    min_wrist_y = float("inf")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        landmarks = analyzer.process_frame(frame)
        if landmarks is None:
            frame_idx += 1
            continue

        wrist_y, shoulder_y = analyzer.get_wrist_shoulder_y(landmarks)

        # Track frame for annotated output (first, max jump, release)
        if len(frames) == 0:
            frames.append((frame_idx, frame.copy(), landmarks))
            annotated_raw.append((frame_idx, frame.copy(), landmarks))

        # Track maximum jump height by hip y (smaller y = higher)
        for side in ["right", "left"]:
            hip = landmarks.get(f"{side}_hip")
            if hip is not None and hip[1] < min_hip_y:
                min_hip_y = hip[1]
                max_jump_frame = (frame_idx, frame.copy(), landmarks)

        # Track release point by wrist y (smaller y = higher = release point)
        if wrist_y is not None and wrist_y < min_wrist_y:
            min_wrist_y = wrist_y
            release_frame = (frame_idx, frame.copy(), landmarks)

        frame_idx += 1

    cap.release()

    # Collect key frames
    key_frames = []
    seen_indices = set()

    for f in [frames[0] if frames else None, max_jump_frame, release_frame]:
        if f is not None and f[0] not in seen_indices:
            key_frames.append(f)
            seen_indices.add(f[0])

    return key_frames


@router.post("/analyze", response_model=AnalyzeResponse)
async def analyze_video(file: UploadFile = File(...)):
    """
    Upload a basketball shooting video (mp4).
    Returns score, feedback, angles, and annotated frames with skeleton overlay.
    """
    # Save uploaded video
    ext = os.path.splitext(file.filename)[1] or ".mp4"
    temp_path = os.path.join(TEMP_DIR, f"{uuid.uuid4()}{ext}")
    with open(temp_path, "wb") as f:
        f.write(await file.read())

    try:
        # Find key frames
        key_frames = find_key_frames(temp_path)
        if not key_frames:
            return AnalyzeResponse(
                score=0,
                feedback=["No pose detected — ensure full body is visible"],
                angles={},
                annotated_frames=[],
            )

        # Use the shooting arm side (right-handed by default, detect from landmarks)
        side = "right"

        # Collect angles from key frames
        all_angles = {"elbow": [], "knee": []}
        for _, frame, landmarks in key_frames:
            angles = analyzer.compute_angles(landmarks, side)
            if "elbow" in angles:
                all_angles["elbow"].append(angles["elbow"])
            if "knee" in angles:
                all_angles["knee"].append(angles["knee"])

        # Average angles across key frames
        avg_elbow = np.mean(all_angles["elbow"]) if all_angles["elbow"] else None
        avg_knee = np.mean(all_angles["knee"]) if all_angles["knee"] else None

        # Get release timing from the frame with highest wrist position
        release_frame = None
        min_wrist = float("inf")
        min_shoulder = None
        for _, frame, landmarks in key_frames:
            wrist_y, shoulder_y = analyzer.get_wrist_shoulder_y(landmarks, side)
            if wrist_y is not None and wrist_y < min_wrist:
                min_wrist = wrist_y
                min_shoulder = shoulder_y
                release_frame = landmarks

        wrist_y_rel = min_wrist if min_wrist != float("inf") else None

        # Evaluate rules
        elbow_score, elbow_fb = evaluate_elbow(avg_elbow)
        knee_score, knee_fb = evaluate_knee(avg_knee)
        release_score, release_fb = evaluate_release(wrist_y_rel, min_shoulder)

        total = calculate_score([elbow_score, knee_score, release_score])

        feedback = [elbow_fb, knee_fb, release_fb]

        # Annotate frames with skeleton
        annotated_b64 = []
        for _, frame, landmarks in key_frames:
            skeleton_frame = analyzer.draw_skeleton(frame, landmarks)
            # Add angle text overlay
            angles = analyzer.compute_angles(landmarks, side)
            y_offset = 30
            for name, val in angles.items():
                cv2.putText(
                    skeleton_frame, f"{name}: {val}°", (10, y_offset),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2
                )
                y_offset += 30
            annotated_b64.append(encode_frame(skeleton_frame))

        return AnalyzeResponse(
            score=total,
            feedback=feedback,
            angles={
                "elbow": avg_elbow if avg_elbow is not None else 0,
                "knee": avg_knee if avg_knee is not None else 0,
            },
            annotated_frames=annotated_b64,
        )

    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)


@router.get("/health")
async def health():
    return {"status": "ok"}

app.include_router(router)
