"""
Module for text splitting operations.
Provides utilities to split and process text based on digits and patterns.
"""

import re
import string
from collections import Counter
from itertools import chain
from typing import Optional, Literal


class Split:
    """Class containing text splitting utilities."""

    def __init__(self, src: str):
        """
        Initialize Split class with source text.

        Args:
            src: Input text to be processed

        Raises:
            TypeError: If src is not a string
        """
        if not isinstance(src, str):
            raise TypeError("Input must be a string")
        self.src = src

    def split_digit_from_legend(self) -> Literal["digit", "legend"]:
        """
        Determine if text contains primarily digits or legend text.

        Returns:
            "digit" if text contains sufficient digits, "legend" otherwise
        """
        DIGIT_LOW = 20
        digit_count = 0
        alpha_count = 0

        char_counts = Counter(chain(self.src))
        for char, count in char_counts.items():
            if char in string.digits:
                digit_count += count
            if char in string.ascii_letters:
                alpha_count += count

        return "digit" if digit_count > DIGIT_LOW else "legend"

    def split_digit_from_digit(self, variable: str) -> str:
        """
        Split digit sequences based on variable type patterns.

        Args:
            variable: Type of data being processed ('pressure', 'temperature', 
                     or 'relative humidity')

        Returns:
            Processed text with split digit sequences

        Raises:
            ValueError: If variable type is not supported
        """
        if variable not in ['pressure', 'temperature', 'relative humidity']:
            raise ValueError("Unsupported variable type")

        patterns = {
            'pressure': [
                (r'(?<=\b\d{3}[^A-Za-z0-9\s]\d{1})(?=[^A-Za-z0-9\s]\b)(.)', ' '),
                (r'(?<=\b([^A-Za-z\.\s]{4}))(?=([^A-Za-z\.\s]{4})\\b)', ' '),
                (r'(?<=\d{3}[^A-Za-z0-9\s]\d{1})(?=\d{3}[^A-Za-z0-9\s]\d{1})', ' '),
                (r'(?<=\d{3}[^A-Za-z0-9 ]\d{1})(?=\d{3}[^A-Za-z0-9\s]\d{1})', ' '),
                (r'(?<=\d{3}[^A-Za-z0-9\s]\d{1})(?=[^A-Za-z0-9\s])(.)', ' '),
                (r'(?<=\d{3}[^A-Za-z0-9\s]\d{2})(?=[^A-Za-z0-9\s])(.)', ' '),
                (r'(?<=(\d{3}[^A-Za-z0-9\s]\d{2}))(?=(\d{3}[^A-Za-z0-9\s]\d{2}))', ' '),
                (r'(?<=\d{4})(?=(\d{3}[^A-Za-z0-9 ]\d{1}))', ' '),
                (r'\b(?<=09\d{2})(?=[^A-Za-z0-9\+\-\s]\d{3}\W\d)\b(.)', ' ')
            ],
            'temperature': [
                (r'(?<=\\b(\d{3}))(?=(\d{2,4})\\b)', ' '),
                (r'(?<=\\b(\d{3}))(?=\d{2}[^A-Za-z0-9 ]+\d?)', ' '),
                (r'(?<=\\b\d{2})(?=\d[^0-9 ])', ' '),
                (r'(?<=\\b\d{3})(?=\d[^A-Za-z0-9 ]\d)', ' ')
            ],
            'relative humidity': [
                (r'(?<=\b100)(?=(\d{2,})\b)', ' '),
                (r'(?<=\b(\d{2}))(?=(\d{2,3})\b)', ' '),
                (r'(?<=\b\d{2})(?=\d[^0-9\s])', ' '),
                (r'(?<=\d{2})(?:(\d{2}))', ' \g<1>')
            ]
        }

        for pattern, replacement in patterns[variable]:
            self.src = re.sub(pattern, replacement, self.src)

        return self.src
