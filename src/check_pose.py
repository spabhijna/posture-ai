import numpy as np
from utils import calculate_angle

class PoseChecker:
    def __init__(self):
        """Initialize posture rules."""
        self.rules = {
            "back_angle": {"threshold": 20, "keypoints": [5, 11]},
            "knee_angle": {"threshold": (90, 120), "keypoints": [11, 13, 15]},
            "head_angle": {"threshold": 15, "keypoints": [0, 5]},
            "elbow_angle": {"threshold": (70, 110), "keypoints": [5, 7, 9]},
            "feet_spacing": {"threshold": (0.6, 1.2), "keypoints": [15, 16, 5, 6]},
            "hip_twist": {"threshold": 10, "keypoints": [11, 12, 5, 6]}
        }

    def check_pose(self, keypoints):
        """Check if the worker's pose is correct."""
        if len(keypoints) < 17:
            return "Unknown (Incomplete Keypoints)"

        issues = []

        # Back Alignment
        vertical_ref = [keypoints[11][0], keypoints[11][1] - 100]
        back_angle = calculate_angle(keypoints[5], keypoints[11], vertical_ref)
        if back_angle >= self.rules["back_angle"]["threshold"]:
            issues.append(f"Back too bent ({back_angle:.1f} degrees)")

        # Knee Bend
        knee_angle = calculate_angle(keypoints[11], keypoints[13], keypoints[15])
        knee_min, knee_max = self.rules["knee_angle"]["threshold"]
        if not (knee_min <= knee_angle <= knee_max):
            issues.append(f"Knee angle off ({knee_angle:.1f}degrees)")

        # Head Position
        torso_ref = [keypoints[5][0], keypoints[5][1] - 50]
        head_angle = calculate_angle(keypoints[0], keypoints[5], torso_ref)
        if head_angle >= self.rules["head_angle"]["threshold"]:
            issues.append(f"Head tilted ({head_angle:.1f}degrees)")

        # Arm Position
        elbow_angle = calculate_angle(keypoints[5], keypoints[7], keypoints[9])
        elbow_min, elbow_max = self.rules["elbow_angle"]["threshold"]
        if not (elbow_min <= elbow_angle <= elbow_max):
            issues.append(f"Arms not aligned ({elbow_angle:.1f}degrees)")

        # Feet Spacing
        feet_distance = np.linalg.norm(np.array(keypoints[15]) - np.array(keypoints[16]))
        shoulder_width = np.linalg.norm(np.array(keypoints[5]) - np.array(keypoints[6]))
        feet_min, feet_max = self.rules["feet_spacing"]["threshold"]
        if not (feet_min * shoulder_width <= feet_distance <= feet_max * shoulder_width):
            issues.append(f"Feet spacing off ({feet_distance:.1f} cm)")

        # Hip Twist
        hip_line = np.array(keypoints[12]) - np.array(keypoints[11])
        shoulder_line = np.array(keypoints[6]) - np.array(keypoints[5])
        twist_angle = np.degrees(np.arccos(np.clip(np.dot(hip_line, shoulder_line) / 
                                                   (np.linalg.norm(hip_line) * np.linalg.norm(shoulder_line)), -1.0, 1.0)))
        if twist_angle >= self.rules["hip_twist"]["threshold"]:
            issues.append(f"Torso twisted ({twist_angle:.1f}degrees)")

        return "Correct" if not issues else "Incorrect: " + ", ".join(issues)