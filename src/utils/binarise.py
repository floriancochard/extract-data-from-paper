"""
Module for image binarisation operations using different thresholding techniques.
Each method converts a grayscale image to binary using various algorithms.
"""

import cv2
from typing import Tuple, Union
import numpy as np


class Binarise:
    """Class containing various image binarisation methods."""
    
    def otsu(self, src: np.ndarray, min_value: int = 0, max_value: int = 255) -> Tuple[float, np.ndarray]:
        """
        Apply Otsu's thresholding method with binary inversion.
        
        Args:
            src: Input grayscale image
            min_value: Minimum threshold value (default: 0)
            max_value: Maximum threshold value (default: 255)
            
        Returns:
            Tuple containing:
                - computed threshold value
                - binary image output
        
        Raises:
            ValueError: If input image is not grayscale
        """
        if len(src.shape) != 2:
            raise ValueError("Input image must be grayscale")
            
        return cv2.threshold(
            src,
            min_value,
            max_value,
            cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU
        )

    def adaptive(self, src: np.ndarray, max_value: int = 255) -> np.ndarray:
        """
        Apply adaptive thresholding using mean neighborhood value.
        
        Args:
            src: Input grayscale image
            max_value: Maximum threshold value (default: 255)
            
        Returns:
            Binary image output
            
        Raises:
            ValueError: If input image is not grayscale
        """
        if len(src.shape) != 2:
            raise ValueError("Input image must be grayscale")
            
        return cv2.adaptiveThreshold(
            src,
            max_value,
            adaptiveMethod=cv2.ADAPTIVE_THRESH_MEAN_C,
            thresholdType=cv2.THRESH_BINARY,
            blockSize=3,
            C=-0.2
        )

    def canny(self, src: np.ndarray, min_value: int = 100, max_value: int = 200) -> np.ndarray:
        """
        Apply Canny edge detection algorithm.
        
        Args:
            src: Input grayscale image
            min_value: Lower threshold for edge detection (default: 100)
            max_value: Upper threshold for edge detection (default: 200)
            
        Returns:
            Edge detection output image
            
        Raises:
            ValueError: If input image is not grayscale
        """
        if len(src.shape) != 2:
            raise ValueError("Input image must be grayscale")
            
        return cv2.Canny(
            src,
            min_value,
            max_value,
            apertureSize=3,
            L2gradient=True
        )
