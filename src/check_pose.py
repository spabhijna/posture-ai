import json

import numpy as np

from utils import calculate_angle, calculate_vector_angle


class PoseChecker:
    def __init__(self, congfig_path):
        with open(congfig_path, "r") as f:
            config = json.load(f)
            self.rules = config["rules"]

    def _check_threshold(self, value, threshold):
        """Check if a value satisfies the threshold."""
        if "min" in threshold and "max" in threshold:
            return threshold["min"] <= value <= threshold["max"]
        elif "min" in threshold:
            return value >= threshold["min"]
        elif "max" in threshold:
            return value <= threshold["max"]
        else:
            raise ValueError("Invalid threshold specification")

    def check_pose(self, keypoints):
        """
        Check if the pose is correct based on the rules
        """
        issues = []
        for rule in self.rules:
            if rule["type"] == "angle":
                a, b, c = rule["keypoints"]
                if c == "Vertical":
                    c = [
                        keypoints[b][0],
                        keypoints[b][1] - 100,
                    ]  # Virtual vertical point
                else:
                    c = keypoints[c]
                a, b = keypoints[a], keypoints[b]
                angle = calculate_angle(a, b, c)
                if not self._check_threshold(angle, rule["threshold"]):
                    issues.append(f"{rule['name']} incorrect ({angle:.1f} degrees)")

            elif rule["type"] == "distance":
                a, b = keypoints[a], keypoints[b]
                distance = np.linalg.norm(np.array(a) - np.array(b))
                if not self._check_threshold(distance, rule["threshold"]):
                    issues.append(f"{rule['name']} incorrect ({distance:.1f} units)")

            elif rule == "distance_ratio":
                pair1, pair2 = rule["pairs"]
                dist1 = np.linalg.norm(
                    np.array(keypoints[pair1[0]]) - np.array(keypoints[pair1[1]])
                )
                dist2 = np.linalg.norm(
                    np.array(keypoints[pair2[0]]) - np.array(keypoints[pair2[1]])
                )
                ratio = dist1 / dist2 if dist2 != 0 else float("inf")
                if not self._check_threshold(ratio, rule["threshold"]):
                    issues.append(f"{rule['name']} incorrect (ratio {ratio:.2f})")

            elif rule == "angle_between_vectors":
                vec1, vec2 = rule["vectors"]
                angle = calculate_vector_angle(
                    keypoints[vec1[0]],
                    keypoints[vec1[1]],
                    keypoints[vec2[0]],
                    keypoints[vec2[1]],
                )
                if not self._check_threshold(angle, rule["threshold"]):
                    issues.append(f"{rule['name']} incorrect ({angle:.1f} degrees)")

            return "Correct" if not issues else "Incorrect: " + ", ".join(issues)
