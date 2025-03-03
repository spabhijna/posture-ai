import numpy as np

def calculate_angle(p1,p2,p3):
    '''Calculate the angle between three points'''
    v1 = np.array(p1) - np.array(p2)
    v2 = np.array(p3) - np.array(p2)
    cos_angle = np.dot(v1,v2)/(np.linalg.norm(v1)*np.linalg.norm(v2))
    angle = np.arccos(cos_angle)
    return angle