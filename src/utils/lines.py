"""
Module for line detection operations in images.
Provides utilities to detect horizontal and vertical lines using morphological and Hough transforms.
"""

import numpy as np
import cv2
from typing import Optional, Tuple


class Lines:
    """Class containing line detection utilities."""

    def find_lines(self, src: np.ndarray) -> np.ndarray:
        """
        Find lines in a document using morphological operations.

        Args:
            src: Input binary image

        Returns:
            Binary image containing detected lines

        Raises:
            TypeError: If src is not a numpy array
        """
        if not isinstance(src, np.ndarray):
            raise TypeError("Input must be a numpy array")

        hlines = src.copy()
        vlines = src.copy()

        # Horizontal lines detection
        h_kernel1 = cv2.getStructuringElement(cv2.MORPH_RECT, (20, 1))
        h_kernel2 = cv2.getStructuringElement(cv2.MORPH_RECT, (20, 4))
        h_kernel3 = cv2.getStructuringElement(cv2.MORPH_RECT, (50, 1))

        hlines = cv2.erode(hlines, h_kernel1, iterations=2)
        hlines = cv2.dilate(hlines, h_kernel2, iterations=2)
        hlines = cv2.dilate(hlines, h_kernel3, iterations=4)
        hlines = cv2.erode(hlines, h_kernel3, iterations=4)

        # Vertical lines detection
        v_kernel1 = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 20))
        v_kernel2 = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 40))
        v_kernel3 = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 50))

        vlines = cv2.erode(vlines, v_kernel1, iterations=2)
        vlines = cv2.dilate(vlines, v_kernel2, iterations=2)
        vlines = cv2.dilate(vlines, v_kernel3, iterations=4)
        vlines = cv2.erode(vlines, v_kernel3, iterations=4)

        return hlines + vlines

    def houghlinesS(self, src: np.ndarray) -> Optional[np.ndarray]:
        """
        Find lines using standard Hough transform.

        Args:
            src: Input binary image

        Returns:
            Array of detected lines or None if no lines found

        Raises:
            TypeError: If src is not a numpy array
        """
        if not isinstance(src, np.ndarray):
            raise TypeError("Input must be a numpy array")

        params = {
            'rho': 1.0,
            'theta': np.pi / 180,
            'threshold': 350,
            'minLineLength': 20,
            'maxLineGap': 200
        }

        return cv2.HoughLines(src, **params)

    def houghlinesP(self, src: np.ndarray) -> Optional[np.ndarray]:
        """
        Find lines using probabilistic Hough transform.

        Args:
            src: Input binary image

        Returns:
            Array of detected line segments or None if no lines found

        Raises:
            TypeError: If src is not a numpy array
        """
        if not isinstance(src, np.ndarray):
            raise TypeError("Input must be a numpy array")

        params = {
            'rho': 1.0,
            'theta': np.pi / 180,
            'threshold': 150,
            'minLineLength': 250,
            'maxLineGap': 4
        }

        return cv2.HoughLinesP(src, **params)
