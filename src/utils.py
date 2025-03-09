import numpy as np

def calculate_angle(p1, p2, p3):
    '''Calculate the angle between three points in degrees'''
    v1 = np.array(p1) - np.array(p2)
    v2 = np.array(p3) - np.array(p2)
    cos_angle = np.dot(v1, v2)/(np.linalg.norm(v1)*np.linalg.norm(v2))
    angle = np.degrees(np.arccos(np.clip(cos_angle, -1.0, 1.0)))
    return angle

def calculate_vector_angle(v1_start, v1_end, v2_start, v2_end):
    """Calculate the angle (in degrees) between two vectors."""
    v1 = np.array(v1_end) - np.array(v1_start)
    v2 = np.array(v2_end) - np.array(v2_start)
    dot_product = np.dot(v1, v2)
    norm_v1 = np.linalg.norm(v1)
    norm_v2 = np.linalg.norm(v2)
    if norm_v1 == 0 or norm_v2 == 0:
        return 0  # Handle degenerate case
    cos_theta = dot_product / (norm_v1 * norm_v2)
    cos_theta = np.clip(cos_theta, -1.0, 1.0)
    return np.degrees(np.arccos(cos_theta))