"""
Module for color space conversion operations.
Provides utilities to transform images between different color spaces.
"""

import cv2
import numpy as np
from typing import Union


class Color:
    """Class containing color space conversion methods."""

    def to_gray(self, src: np.ndarray) -> np.ndarray:
        """
        Convert an RGB/BGR image to grayscale.

        Args:
            src: Input image in BGR format (OpenCV default)

        Returns:
            Grayscale version of the input image

        Raises:
            ValueError: If input image is not in BGR format (3 channels)
        """
        if len(src.shape) != 3 or src.shape[2] != 3:
            raise ValueError("Input image must be in BGR format (3 channels)")

        return cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)

    def to_rgb(self, src: np.ndarray) -> np.ndarray:
        """
        Convert a BGR image to RGB format.

        Args:
            src: Input image in BGR format (OpenCV default)

        Returns:
            RGB version of the input image

        Raises:
            ValueError: If input image is not in BGR format (3 channels)
        """
        if len(src.shape) != 3 or src.shape[2] != 3:
            raise ValueError("Input image must be in BGR format (3 channels)")

        return cv2.cvtColor(src, cv2.COLOR_BGR2RGB)
