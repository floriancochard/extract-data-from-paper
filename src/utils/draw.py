"""
Module for drawing operations on images.
Provides utilities to draw lines, contours, and text on images using OpenCV.
"""

import cv2
import numpy as np
from typing import Optional, Tuple, Union
from . import log


class Draw:
    """Class containing drawing utilities for image manipulation."""

    def __init__(self, src: np.ndarray):
        """
        Initialize Draw class with source image.

        Args:
            src: Input image to draw on

        Raises:
            TypeError: If src is not a numpy array
        """
        if not isinstance(src, np.ndarray):
            raise TypeError("Input must be a numpy array")
        self.src = src
        self.logger = log.Log().create_logger('default')

    def draw_lines(self, lines: Optional[np.ndarray], 
                  color: Tuple[int, int, int] = (0, 0, 255),
                  thickness: int = 3) -> np.ndarray:
        """
        Draw lines on the image.

        Args:
            lines: Array of line coordinates [x1, y1, x2, y2]
            color: RGB color tuple (default: red)
            thickness: Line thickness (default: 3)

        Returns:
            Image with drawn lines

        Raises:
            ValueError: If lines array is malformed
        """
        if lines is not None:
            try:
                for line in lines:
                    x1, y1, x2, y2 = line[0]
                    cv2.line(self.src, (x1, y1), (x2, y2), color, thickness, cv2.LINE_AA)
            except (IndexError, ValueError) as e:
                self.logger.error(f'Invalid line format: {e}')
        else:
            self.logger.warning('No lines to draw.')

        return self.src

    def draw_contours(self, start_x: int, start_y: int, end_x: int, end_y: int,
                     color: Tuple[int, int, int] = (0, 255, 0),
                     thickness: int = 3) -> np.ndarray:
        """
        Draw rectangular contours on the image.

        Args:
            start_x: Starting x coordinate
            start_y: Starting y coordinate
            end_x: Ending x coordinate
            end_y: Ending y coordinate
            color: RGB color tuple (default: green)
            thickness: Rectangle thickness (default: 3)

        Returns:
            Image with drawn contours

        Raises:
            ValueError: If coordinates are invalid
        """
        if any(coord < 0 for coord in [start_x, start_y, end_x, end_y]):
            raise ValueError("Coordinates must be non-negative")

        cv2.rectangle(
            self.src,
            pt1=(start_x, start_y),
            pt2=(end_x, end_y),
            color=color,
            thickness=thickness
        )
        return self.src

    def draw_text(self, text: str, x: int, y: int,
                 color: Tuple[int, int, int] = (0, 0, 255),
                 scale: float = 1.0,
                 thickness: int = 3) -> np.ndarray:
        """
        Draw text on the image.

        Args:
            text: String to draw
            x: X coordinate
            y: Y coordinate
            color: RGB color tuple (default: red)
            scale: Text scale factor (default: 1.0)
            thickness: Text thickness (default: 3)

        Returns:
            Image with drawn text

        Raises:
            ValueError: If coordinates are invalid
        """
        if not text:
            self.logger.warning('Empty text string provided.')
            return self.src

        if x < 0 or y < 0:
            raise ValueError("Coordinates must be non-negative")

        cv2.putText(
            self.src,
            text,
            (x, y),
            cv2.FONT_HERSHEY_COMPLEX,
            scale,
            color,
            thickness
        )
        return self.src
