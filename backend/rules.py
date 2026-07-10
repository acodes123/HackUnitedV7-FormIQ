def evaluate_elbow(angle: float) -> tuple:
    """
    Evaluate elbow angle at release.
    Ideal range: 85°–100° (proper shooting pocket).
    Too wide: > 120° means elbow flared out.
    Too tucked: < 70° means elbow too close to body.
    """
    if angle is None:
        return (15, "Could not detect elbow angle")
    if 85 <= angle <= 100:
        return (40, "Good elbow angle at release")
    elif 75 <= angle < 85 or 100 < angle <= 120:
        return (25, "Elbow angle slightly off — aim for 85°–100°")
    elif angle > 120:
        return (10, "Elbow too wide — keep it closer to your body")
    else:
        return (10, "Elbow too tucked — extend more on release")


def evaluate_knee(angle: float) -> tuple:
    """
    Evaluate knee bend before jump.
    Ideal range: 130°–145° (good athletic stance).
    Too straight: > 160° means not bending enough.
    """
    if angle is None:
        return (10, "Could not detect knee angle")
    if 130 <= angle <= 145:
        return (30, "Good knee bend — nice athletic stance")
    elif 145 < angle <= 160:
        return (20, "Bend knees more for better power")
    elif angle > 160:
        return (10, "Knees too straight — bend them more before jumping")
    else:
        return (20, "Bending too deep — try a more natural stance")


def evaluate_release(wrist_y: float, shoulder_y: float) -> tuple:
    """
    Evaluate release timing based on wrist height vs shoulder height.
    In image coordinates, y increases downward, so lower y = higher position.
    A good release has the wrist above the shoulder at the shot's peak.
    """
    if wrist_y is None or shoulder_y is None:
        return (15, "Could not detect release point")
    # Lower y value = higher in the frame
    if wrist_y < shoulder_y - 10:
        return (30, "Good release — wrist above shoulder at peak")
    elif abs(wrist_y - shoulder_y) <= 10:
        return (20, "Release at shoulder level — try releasing higher")
    else:
        return (10, "Release too low — wrist should be above shoulder")


def calculate_score(feedback_scores: list) -> int:
    """Calculate total score from individual rule scores."""
    return sum(feedback_scores)
