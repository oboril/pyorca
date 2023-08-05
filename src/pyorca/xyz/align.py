"""This module contains procedures for aligning molecules and calculating RMSD"""

import numpy as np

from typing import List

from orcapython.xyz import read_xyz

def align_xyz_files(path1 : str, path2 : str) -> float:
    """Aligns molecules from .xyz files and returns the RMSD"""

    with open(path1, "r") as f:
        _, coords1 = read_xyz(f.read())
    
    with open(path2, "r") as f:
        _, coords2 = read_xyz(f.read())

    return aligned_rmsd(coords1, coords2)

def aligned_rmsd(coords1 : List[List[float]] | np.array, coords2 : List[List[float]] | np.array) -> float:
    """Aligns the structures and returns the RMSD. Assumes the ordering of atoms is identical in both."""
    
    # Convert the coordinates to numpy array
    coords1 = np.array(coords1)
    coords2 = np.array(coords2)

    # Move to the center of mass
    coords1 -= np.mean(coords1, axis=0)
    coords2 -= np.mean(coords2, axis=0)

    # Generate rotation matrix by Kabsch algorithm
    R = kabsch(coords1, coords2)

    # Rotate
    coords2 = np.dot(coords2, R)

    # Calculate RMSD
    rmsd_aligned = np.sqrt(np.sum((coords1 - coords2)**2) / coords1.shape[0])

    return rmsd_aligned


def kabsch(coord_var: np.array, coord_ref: np.array) -> np.array:
    """Calculates rotation matrix to align two molecules, http://en.wikipedia.org/wiki/Kabsch_algorithm"""

    # covariance matrix
    covar = np.dot(coord_var.T, coord_ref)

    # SVD
    v, s, wt = np.linalg.svd(covar)

    # proper/improper rotation, JCC 2004, 25, 1894.
    d = (np.linalg.det(v) * np.linalg.det(wt)) < 0.0

    if d: # antialigns of the last singular vector
        s[-1] = -s[-1]
        v[:, -1] = -v[:, -1]

    # Create Rotation matrix R
    R = np.dot(v, wt)

    return R