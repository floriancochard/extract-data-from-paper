"""
Module for text cleaning and character deletion operations.
Provides utilities to clean and format text data using regular expressions.
"""

import re
from typing import Tuple


class Delete:
    """Class containing text cleaning and formatting methods."""

    def __init__(self, src: str):
        """
        Initialize Delete class with source text.

        Args:
            src: Input text to be processed
        """
        if not isinstance(src, str):
            raise TypeError("Input must be a string")
        self.src = src

    def delete_unwanted_char(self) -> Tuple[str, str]:
        """
        Remove unwanted characters and split text into character and digit components.

        Returns:
            Tuple containing:
                - extracted character component
                - cleaned digit component

        Example:
            "19 Temperature 23.5" -> ("Temperature", "23.5")
        """
        catch = (
            r'([1-9]|[1-3][1-9]+|[lL]eve[lL]|Station|N[oO0]+n|'
            r'Mean|Year|Pressure|Temperature|Relative|Humidity|Wind|Speed|'
            r'Jan|Fe[b8]|Mar|April|May|June|Jul|July|Aug|Sept|[oO0]ct|N[oO0]v|Dec)'
        )
        pattern = r'(?:\n?|^)' + catch + r'(?:\.|\,|\n|\s)+(.*)'

        match = re.search(pattern, self.src, re.DOTALL)
        if match:
            char = match.group(1)
            digit = match.group(2)
        else:
            char = '[D]'
            digit = self.src

        # Clean up digit component
        digit = re.sub(r'(\n){2}', ' ', digit)
        digit = re.sub(
            r'(?:\d\s{5,})([1-9]|[1-3][0-9])(?=\s+\d+)',
            r'\1',
            digit
        )

        return char, digit

    def remove_double(self) -> str:
        """
        Remove double spaces and redundant newlines.

        Returns:
            Cleaned text with single spaces
        """
        self.src = re.sub(r'(\s){2,}', r'\1', self.src)
        self.src = re.sub(r'(?<=[^\s])(\n)+(.*?)', ' ', self.src)
        return self.src

    def remove_empty(self) -> str:
        """
        Remove empty spaces around specific patterns.

        Returns:
            Cleaned text with removed empty spaces
        """
        self.src = re.sub(
            r'(\s[+-]|\s\d{2,3})(\s)([^A-Za-z])',
            r'\1\3',
            self.src
        )
        return self.src
