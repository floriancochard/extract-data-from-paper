"""
Module for text replacement and character correction operations.
Provides utilities to clean and standardize text data using regular expressions.
"""

import re
from typing import Optional


class Replace:
    """Class containing text replacement and correction utilities."""

    def __init__(self, src: str):
        """
        Initialize Replace class with source text.

        Args:
            src: Input text to be processed

        Raises:
            TypeError: If src is not a string
        """
        if not isinstance(src, str):
            raise TypeError("Input must be a string")
        self.src = src

    def to_unicode(self) -> str:
        """
        Convert special characters to standard unicode.

        Returns:
            String with standardized unicode characters
        """
        self.src = re.sub(r"\—", "-", self.src)
        return self.src

    def to_essential_digit(self) -> str:
        """
        Correct common OCR errors for digits 0 and 1.

        Returns:
            String with corrected digit characters
        """
        self.src = re.sub(r'[oO©]', '0', self.src)
        self.src = re.sub(r'[I\!]', '1', self.src)
        return self.src

    def digit_to_sign(self, variable: str) -> str:
        """
        Convert leading digits to plus/minus signs.

        Args:
            variable: Type of data being processed

        Returns:
            String with converted signs
        """
        self.src = re.sub(r'(?=\b4\d{3})(.)', '+', self.src)
        self.src = re.sub(
            r'(?=\b4\d{3,5}\b|\b4\d{1}[^A-Za-z ]\d{2}\b|\b4[\-\+]+\d+|(?<=[+])4(?=[-]\d{1,}))(.)',
            '+',
            self.src
        )

        if variable == "diurnal inequalities":
            self.src = re.sub(r'(?=\b4\d{2})(.)', '+', self.src)

        return self.src

    def edit_sign(self) -> str:
        """
        Correct successive sign errors.

        Returns:
            String with corrected signs
        """
        self.src = re.sub(r'((?!(\-\-))[\-\—\~]{2,}|[\—\~]|(\-\()(?=0))', '-', self.src)
        self.src = re.sub(
            r'([\+]+[\+\-]+|\-\+|\-[{}]\-|(?!(\-|\-\-|\{\}))([\-\{\}]+)|[\{\}]+)(?=.*)',
            '+',
            self.src
        )
        return self.src

    def char_to_digit(self) -> str:
        """
        Convert common OCR character errors to correct digits.

        Returns:
            String with corrected digits
        """
        replacements = {
            r'[oO©D]': '0',
            r'[xXtTiIlLrK\!]': '1',
            r'[zZ£]': '2',
            r'[¢]': '4',
            r'[sS]': '5',
            r'[C€]': '6',
            r'[yY%]': '7',
            r'[&bB]': '8',
            r'[§qQgGhH$]': '9'
        }

        for pattern, replacement in replacements.items():
            self.src = re.sub(pattern, replacement, self.src)
        
        self.src = re.sub(r'(?<=\-)(\()(?=\-)', '0', self.src)
        return self.src

    def sign_to_nan(self) -> str:
        """
        Convert isolated minus signs to NaN.

        Returns:
            String with NaN replacements
        """
        self.src = re.sub(r'(?=(?<=\s)|(?<=^))([-_.]+)(?=\s|$)', 'NaN', self.src)
        return self.src

    def edit_digit(self) -> str:
        """
        Apply various digit corrections and formatting rules.

        Returns:
            String with corrected digits and formatting
        """
        corrections = [
            (r'(?<=[+-])(?=\d[0-4]\W\d{2})(.)', ''),
            (r'(?=\b(4)\d{1}.\d{1}\b)(.)', '7'),
            (r'^([\W\d{1}]\s)', ''),
            (r'(\b0)(?=9\d{1}.\d{1}\b)', '[0]'),
            (r'((?<=\d{1})[-](?=\s|$))', '[N]'),
            (r'([^A-Za-z0-9 ])(?=\d{3}.\d{1})', ''),
            (r'([0])(?=[0]\d{2}[^A-Za-z0-9 ]\d{1})', ''),
            (r'(?:^(([^A-Za-z0-9 ]\d{1})|([A-Za-z]\s\d{1})|(\d{2})(?=\d{3}\.\d{1}\s)))',
             '[\g<1>] '),
            (r'(\d{2,3})([^A-Za-z0-9.\s])(?=\s|$)', '\g<1>.[X]')
        ]

        for pattern, replacement in corrections:
            self.src = re.sub(pattern, replacement, self.src)
        return self.src
