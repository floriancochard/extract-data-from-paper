"""
Module for image noise and artifact removal operations.
Provides utilities to clean and enhance image quality using OpenCV.
"""

import cv2
import numpy as np
from typing import Tuple


class Remove:
    """Class containing image cleaning and enhancement utilities."""

    def noise(self, src: np.ndarray) -> np.ndarray:
        """
        Remove noise through Gaussian blur operation.

        Args:
            src: Input image

        Returns:
            Denoised image after Gaussian blur

        Raises:
            TypeError: If src is not a numpy array
        """
        if not isinstance(src, np.ndarray):
            raise TypeError("Input must be a numpy array")
            
        return cv2.GaussianBlur(src, ksize=(5, 5), sigmaX=0)

    def artifacts(self, src: np.ndarray, height: int) -> Tuple[np.ndarray, np.ndarray]:
        """
        Remove artifacts in lines before OCR processing.
        
        Removes remaining spots of digits and other noise using morphological operations.

        Args:
            src: Input BGR image
            height: Height of the image row in pixels

        Returns:
            Tuple containing:
                - Binary mask of cleaned regions
                - Cleaned image with artifacts removed

        Raises:
            TypeError: If src is not a numpy array
            ValueError: If height is negative
        """
        if not isinstance(src, np.ndarray):
            raise TypeError("Input must be a numpy array")
        if height <= 0:
            raise ValueError("Height must be positive")

        # Constants
        H_LIM_SEGMENTATION = 75

        # Convert to grayscale and threshold
        gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
        thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
        mask = np.zeros(src.shape, dtype=np.uint8)

        # Apply morphological operations based on height
        if height < H_LIM_SEGMENTATION:
            kclose = cv2.getStructuringElement(cv2.MORPH_CROSS, (120, 1))
            thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kclose, iterations=1)
        else:
            kclose = cv2.getStructuringElement(cv2.MORPH_CROSS, (120, 1))
            kopen = cv2.getStructuringElement(cv2.MORPH_CROSS, (1, 4))
            thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kclose, iterations=1)
            thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kopen, iterations=1)

        # Find and sort contours
        cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if len(cnts) == 2 else cnts[1]
        cnts = sorted(cnts, key=cv2.contourArea, reverse=True)

        # Draw contours on mask
        if cnts:
            cv2.drawContours(mask, [cnts[0]], -1, (255, 255, 255), -1)

        # Apply mask and set background to white
        mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
        result = cv2.bitwise_and(src, src, mask=mask)
        result[mask == 0] = (255, 255, 255)

        return mask, result
