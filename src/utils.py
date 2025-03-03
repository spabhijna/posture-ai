import numpy as np

def calculate_angle(p1, p2, p3):
    '''Calculate the angle between three points in degrees'''
    v1 = np.array(p1) - np.array(p2)
    v2 = np.array(p3) - np.array(p2)
    cos_angle = np.dot(v1, v2)/(np.linalg.norm(v1)*np.linalg.norm(v2))
    angle = np.degrees(np.arccos(np.clip(cos_angle, -1.0, 1.0)))
    return angle
