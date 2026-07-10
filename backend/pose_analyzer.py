import cv2
import mediapipe as mp
import numpy as np
from typing import Optional


mp_pose = mp.solutions.pose


def angle_between(a: np.ndarray, b: np.ndarray, c: np.ndarray) -> float:
    """
    Calculate angle at point b between vectors ba and bc.
    Uses law of cosines: angle = arccos((ba·bc) / (|ba| * |bc|))

    For example, elbow angle = angle_between(shoulder, elbow, wrist)
    gives the angle at the elbow joint.
    """
    ba = a - b
    bc = c - b
    dot = np.dot(ba, bc)
    norm = np.linalg.norm(ba) * np.linalg.norm(bc)
    if norm == 0:
        return 0.0
    cos_angle = np.clip(dot / norm, -1.0, 1.0)
    return np.degrees(np.arccos(cos_angle))


class PoseAnalyzer:
    def __init__(self):
        self.pose = mp_pose.Pose(
            static_image_mode=False,
            model_complexity=1,
            enable_segmentation=False,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5,
        )

    def process_frame(self, frame: np.ndarray) -> Optional[dict]:
        """Run MediaPipe on a single frame, return landmark dict or None."""
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.pose.process(rgb)
        if not results.pose_landmarks:
            return None

        h, w, _ = frame.shape
        lm = results.pose_landmarks.landmark
        landmarks = {}
        idx_map = {
            "left_shoulder": 11, "right_shoulder": 12,
            "left_elbow": 13, "right_elbow": 14,
            "left_wrist": 15, "right_wrist": 16,
            "left_hip": 23, "right_hip": 24,
            "left_knee": 25, "right_knee": 26,
            "left_ankle": 27, "right_ankle": 28,
        }
        for name, idx in idx_map.items():
            landmarks[name] = np.array([lm[idx].x * w, lm[idx].y * h, lm[idx].z * w])

        return landmarks

    def draw_skeleton(self, frame: np.ndarray, landmarks: dict) -> np.ndarray:
        """Draw pose skeleton lines and joints on the frame."""
        connections = [
            ("left_shoulder", "left_elbow"), ("right_shoulder", "right_elbow"),
            ("left_elbow", "left_wrist"), ("right_elbow", "right_wrist"),
            ("left_shoulder", "right_shoulder"),
            ("left_hip", "right_hip"),
            ("left_shoulder", "left_hip"), ("right_shoulder", "right_hip"),
            ("left_hip", "left_knee"), ("right_hip", "right_knee"),
            ("left_knee", "left_ankle"), ("right_knee", "right_ankle"),
        ]
        overlay = frame.copy()
        for a, b in connections:
            if a in landmarks and b in landmarks:
                pt1 = tuple(landmarks[a][:2].astype(int))
                pt2 = tuple(landmarks[b][:2].astype(int))
                cv2.line(overlay, pt1, pt2, (0, 255, 0), 2)
                cv2.circle(overlay, pt1, 4, (0, 0, 255), -1)
                cv2.circle(overlay, pt2, 4, (0, 0, 255), -1)
        return overlay

    def compute_angles(self, landmarks: dict, side: str = "right") -> dict:
        """Compute elbow and knee angles for the given side."""
        prefix = side
        shoulder = landmarks.get(f"{prefix}_shoulder")
        elbow = landmarks.get(f"{prefix}_elbow")
        wrist = landmarks.get(f"{prefix}_wrist")
        hip = landmarks.get(f"{prefix}_hip")
        knee = landmarks.get(f"{prefix}_knee")
        ankle = landmarks.get(f"{prefix}_ankle")

        angles = {}
        if shoulder is not None and elbow is not None and wrist is not None:
            angles["elbow"] = round(angle_between(shoulder, elbow, wrist), 1)
        if hip is not None and knee is not None and ankle is not None:
            angles["knee"] = round(angle_between(hip, knee, ankle), 1)
        return angles

    def get_wrist_shoulder_y(self, landmarks: dict, side: str = "right") -> tuple:
        """Return (wrist_y, shoulder_y) for release timing check."""
        prefix = side
        wrist = landmarks.get(f"{prefix}_wrist")
        shoulder = landmarks.get(f"{prefix}_shoulder")
        if wrist is None or shoulder is None:
            return None, None
        return wrist[1], shoulder[1]
