"""
Module for text insertion and formatting operations.
Provides utilities to add decimal points and format numerical values.
"""

import re
from typing import Optional


class Insert:
    """Class containing text insertion and formatting methods."""

    def __init__(self, src: str):
        """
        Initialize Insert class with source text.

        Args:
            src: Input text to be processed

        Raises:
            TypeError: If src is not a string
        """
        if not isinstance(src, str):
            raise TypeError("Input must be a string")
        self.src = src

    def add_point(self, variable: str) -> str:
        """
        Add decimal points to numerical values based on variable type.

        Args:
            variable: Type of variable ('pressure', 'temperature', 'diurnal inequalities')

        Returns:
            Formatted text with added decimal points

        Raises:
            ValueError: If variable type is not supported
        """
        valid_variables = {'pressure', 'temperature', 'diurnal inequalities'}
        if variable not in valid_variables:
            raise ValueError(f"Variable must be one of: {valid_variables}")

        # Extract leading characters (station level, date, etc.)
        pattern = r'(^(\W|[A-Za-z]+\d\W|\d{1,2}\s|\W+\d{1,2}\s)+)'
        leading_chars = re.match(pattern, self.src)
        char = leading_chars.group(0) if leading_chars else ''
        
        # Remove leading characters for processing
        self.src = re.sub(pattern, '', self.src)

        # Common processing patterns
        self.src = self._process_common_patterns()

        # Variable-specific processing
        processors = {
            'pressure': self._process_pressure,
            'temperature': self._process_temperature,
            'diurnal inequalities': self._process_diurnal
        }
        
        self.src = processors[variable]()
        
        # Restore leading characters
        return char + self.src

    def _process_common_patterns(self) -> str:
        """Apply common formatting patterns to all variables."""
        # Convert various separators to decimal points
        text = re.sub(r'(?<=\d)[^A-Za-bd-z0-9 ]+(?=\d|\s|$)', ".", self.src)
        # Convert minus signs between digits to decimal points
        return re.sub(r'(?<=\d)([^\w\d\s]+)(?=\d)', '.', text)

    def _process_pressure(self) -> str:
        """Process pressure-specific patterns."""
        text = self.src
        patterns = [
            (r'(?<=\b[09]\d{2})(?=\d{1}(\s|$))', '.'),
            (r'(?<=\b\d{3})(?=\d{2}\b(\s|$))', '.'),
            (r'(?<=\b\d{4})(?=\d{2}\b(\s|$))', '.'),
            (r'(?<=\b[09]\d{2})(?=\d{1}(?:\s|$))', '.')
        ]
        for pattern, replacement in patterns:
            text = re.sub(pattern, replacement, text)
        return text

    def _process_temperature(self) -> str:
        """Process temperature-specific patterns."""
        return re.sub(r'(?<=\b[6-9]\d)(?=\d{1,2}(\s|$))', '.', self.src)

    def _process_diurnal(self) -> str:
        """Process diurnal inequalities patterns."""
        text = re.sub(r'(?<=\s\d{4})(?=\d{2}\s)', '.', self.src)
        return re.sub(r'(?<=[+-][0-9])(?=\d{2}(\s|$))', '.', text)
