import numpy as np


def create_projection_matrix(width, height):
    """Create orthographic projection matrix"""
    return np.array([
        [2.0 / width, 0, 0, -1],
        [0, 2.0 / height, 0, -1],
        [0, 0, -1, 0],
        [0, 0, 0, 1]
    ], dtype=np.float32)


def create_view_matrix():
    """Create identity view matrix"""
    return np.eye(4, dtype=np.float32)
