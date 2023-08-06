"""Basic functions for calculating distances and angles"""

from typing import List

import numpy as np

def distance(coords1 : List[float], coords2 : List[float]) -> float:
    """Returns euclidean distance between the two points"""
    c1 = np.array(coords1)
    c2 = np.array(coords2)
    return np.sqrt(np.sum((c1-c2)**2))

def angle_degree(coords1: List[float], coords2: List[float], coords3: List[float]) -> float:
    """Returns the angle in degrees defined by the three points"""
    c1 = np.array(coords1)
    c2 = np.array(coords2)
    c3 = np.array(coords3)

    return _angle_between_vecs(c1-c2, c3-c2)

def dihedral_degree(coords1: List[float], coords2: List[float], coords3: List[float], coords4: List[float]) -> float:
    """Returns the dihedral angle in degrees defined by the four points"""

    c1 = np.array(coords1)
    c2 = np.array(coords2)
    c3 = np.array(coords3)
    c4 = np.array(coords4)

    return _angle_between_vecs(c1-c2, c4-c3)

def _angle_between_vecs(v1: np.array, v2: np.array) -> float:
    """Angle in degrees between the two vectors"""
    v1 /= np.sqrt(np.sum(v1**2))
    v2 /= np.sqrt(np.sum(v2**2))

    return np.arccos(np.clip(np.dot(v1, v2), -1.0, 1.0)) / np.pi * 180