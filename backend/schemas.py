from pydantic import BaseModel
from typing import List


class AnalyzeResponse(BaseModel):
    score: int
    feedback: List[str]
    angles: dict
    annotated_frames: List[str]
