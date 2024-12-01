"""
Module for morphological operations on images.
Provides utilities for basic morphological transformations using OpenCV.
"""

import cv2
import numpy as np
from typing import Tuple


class Morph:
    """Class containing morphological transformation utilities."""

    def to_close(self, src: np.ndarray, hsize: int, vsize: int, iterations: int) -> np.ndarray:
        """
        Apply closing morphological operation.

        Args:
            src: Input image
            hsize: Horizontal size of the kernel
            vsize: Vertical size of the kernel
            iterations: Number of times to apply the operation

        Returns:
            Processed image after closing operation

        Raises:
            TypeError: If src is not a numpy array
            ValueError: If kernel sizes or iterations are negative
        """
        if not isinstance(src, np.ndarray):
            raise TypeError("Input must be a numpy array")
        if any(val <= 0 for val in [hsize, vsize, iterations]):
            raise ValueError("Kernel sizes and iterations must be positive")

        kernel = cv2.getStructuringElement(cv2.MORPH_CLOSE, (hsize, vsize))
        return cv2.morphologyEx(src, kernel, iterations=iterations)

    def to_open(self, src: np.ndarray, hsize: int, vsize: int, iterations: int) -> np.ndarray:
        """
        Apply opening morphological operation.

        Args:
            src: Input image
            hsize: Horizontal size of the kernel
            vsize: Vertical size of the kernel
            iterations: Number of times to apply the operation

        Returns:
            Processed image after opening operation

        Raises:
            TypeError: If src is not a numpy array
            ValueError: If kernel sizes or iterations are negative
        """
        if not isinstance(src, np.ndarray):
            raise TypeError("Input must be a numpy array")
        if any(val <= 0 for val in [hsize, vsize, iterations]):
            raise ValueError("Kernel sizes and iterations must be positive")

        kernel = cv2.getStructuringElement(cv2.MORPH_OPEN, (hsize, vsize))
        return cv2.morphologyEx(src, kernel, iterations=iterations)

    def to_dilate(self, src: np.ndarray, hsize: int, vsize: int, iterations: int) -> np.ndarray:
        """
        Apply dilation with rectangular kernel.

        Args:
            src: Input image
            hsize: Horizontal size of the kernel
            vsize: Vertical size of the kernel
            iterations: Number of times to apply the operation

        Returns:
            Processed image after dilation

        Raises:
            TypeError: If src is not a numpy array
            ValueError: If kernel sizes or iterations are negative
        """
        if not isinstance(src, np.ndarray):
            raise TypeError("Input must be a numpy array")
        if any(val <= 0 for val in [hsize, vsize, iterations]):
            raise ValueError("Kernel sizes and iterations must be positive")

        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (hsize, vsize))
        return cv2.dilate(src, kernel, (-1, -1), iterations=iterations)

    def to_erode(self, src: np.ndarray, hsize: int, vsize: int, iterations: int) -> np.ndarray:
        """
        Apply erosion with rectangular kernel.

        Args:
            src: Input image
            hsize: Horizontal size of the kernel
            vsize: Vertical size of the kernel
            iterations: Number of times to apply the operation

        Returns:
            Processed image after erosion

        Raises:
            TypeError: If src is not a numpy array
            ValueError: If kernel sizes or iterations are negative
        """
        if not isinstance(src, np.ndarray):
            raise TypeError("Input must be a numpy array")
        if any(val <= 0 for val in [hsize, vsize, iterations]):
            raise ValueError("Kernel sizes and iterations must be positive")

        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (hsize, vsize))
        return cv2.erode(src, kernel, (-1, -1), iterations=iterations)
