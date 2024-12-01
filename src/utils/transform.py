"""
Module for image transformation operations.
Provides utilities for rotating and estimating skew angles in images.
"""

import cv2
import numpy as np
from typing import Tuple, Union


class Transform:
    """Class containing image transformation utilities."""

    def estimate_angle(self, src: np.ndarray) -> float:
        """
        Estimate skew angle of the document.

        Args:
            src: Input binary image

        Returns:
            Estimated rotation angle in degrees

        Raises:
            TypeError: If src is not a numpy array
        """
        if not isinstance(src, np.ndarray):
            raise TypeError("Input must be a numpy array")

        non_zero_pixels = cv2.findNonZero(src)
        _, _, angle = cv2.minAreaRect(non_zero_pixels)
        
        return angle + 90 if angle <= -45 else angle

    def rotate(self, src: np.ndarray, angle: float) -> np.ndarray:
        """
        Rotate a document by specified angle.

        Args:
            src: Input image
            angle: Rotation angle in degrees

        Returns:
            Rotated image

        Raises:
            TypeError: If src is not a numpy array
            ValueError: If angle is not a valid float
        """
        if not isinstance(src, np.ndarray):
            raise TypeError("Input must be a numpy array")
        if not isinstance(angle, (int, float)):
            raise ValueError("Angle must be a number")

        # Get image dimensions
        height, width = src.shape[:2]
        center = (width/2, height/2)

        # Calculate rotation matrix
        rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1.0)

        # Calculate new bounds
        abs_cos = abs(rotation_matrix[0, 0])
        abs_sin = abs(rotation_matrix[0, 1])
        bound_w = int(height * abs_sin + width * abs_cos)
        bound_h = int(height * abs_cos + width * abs_sin)

        # Adjust rotation matrix for new bounds
        rotation_matrix[0, 2] += bound_w/2 - center[0]
        rotation_matrix[1, 2] += bound_h/2 - center[1]

        # Apply rotation
        dst = cv2.warpAffine(
            src,
            rotation_matrix,
            (bound_w, bound_h),
            flags=cv2.INTER_CUBIC,
            borderMode=cv2.BORDER_REPLICATE
        )

        return dst
