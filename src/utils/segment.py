"""
Module for image segmentation operations.
Provides utilities to segment images into blocks and lines using morphological operations.
"""

import cv2
import numpy as np
from typing import Optional


class Segment:
    """Class containing image segmentation utilities."""

    def segment_block(self, src: np.ndarray) -> np.ndarray:
        """
        Segment blocks in an image using morphological operations.

        Args:
            src: Input binary image

        Returns:
            Segmented image containing blocks

        Raises:
            TypeError: If src is not a numpy array
        """
        if not isinstance(src, np.ndarray):
            raise TypeError("Input must be a numpy array")

        # Define structuring elements
        kernels = {
            'h_open': cv2.getStructuringElement(cv2.MORPH_RECT, (5, 1)),
            'h_close': cv2.getStructuringElement(cv2.MORPH_RECT, (500, 1)),
            'v_open': cv2.getStructuringElement(cv2.MORPH_RECT, (1, 1)),
            'v_close': cv2.getStructuringElement(cv2.MORPH_RECT, (1, 40))
        }

        # Apply morphological operations
        segment = src.copy()
        segment = cv2.morphologyEx(segment, cv2.MORPH_OPEN, kernels['h_open'], iterations=1)
        segment = cv2.morphologyEx(segment, cv2.MORPH_CLOSE, kernels['h_close'], iterations=4)
        segment = cv2.morphologyEx(segment, cv2.MORPH_OPEN, kernels['v_open'], iterations=1)
        segment = cv2.morphologyEx(segment, cv2.MORPH_CLOSE, kernels['v_close'], iterations=2)

        return segment

    def segment_line(self, src: np.ndarray) -> np.ndarray:
        """
        Segment lines in a block image using morphological operations.

        Args:
            src: Input binary image

        Returns:
            Segmented image containing lines

        Raises:
            TypeError: If src is not a numpy array
        """
        if not isinstance(src, np.ndarray):
            raise TypeError("Input must be a numpy array")

        # Define structuring elements
        kernels = {
            'close': cv2.getStructuringElement(cv2.MORPH_CROSS, (150, 1)),
            'open': cv2.getStructuringElement(cv2.MORPH_CROSS, (150, 5)),
            'erode': cv2.getStructuringElement(cv2.MORPH_CROSS, (1, 1))
        }

        # Apply morphological operations
        segment = src.copy()
        segment = cv2.morphologyEx(segment, cv2.MORPH_CLOSE, kernels['close'], iterations=2)
        segment = cv2.morphologyEx(segment, cv2.MORPH_OPEN, kernels['open'], iterations=2)
        segment = cv2.erode(segment, kernels['erode'], iterations=1)

        return segment
