"""
Module for analyzing and validating image processing results.
Provides utilities to determine if images should be processed further.
"""

import os
import re
from typing import Optional, Tuple, Union
from . import log


class Should:
    """Class containing analysis and validation utilities."""

    def __init__(self):
        """Initialize Should class with logger."""
        self.logger = log.Log().create_logger('default')

    def analyze(self, src: str, trigger_analyze: int, year: str, 
                page: str, lines: Optional[list]) -> Optional[str]:
        """
        Determine if an image should be analyzed based on line count.

        Important note: TRIGGER value is empirical. The decision is based on the number 
        of lines identified in a page. If the number is below TRIGGER_ANALYZE value, 
        the document is discarded. Otherwise the document is added to the list.

        With 1922 document, lines are correctly recognized with HoughlinesP
        It is to relate with the Canny binarization method apparently. But
        for "bad" scanning version from 1873 to 1921, lines are not correctly
        detected. As a result the trigger needs to adapt to the quality
        of the scan and / or the quality of the binarization method. Indeed,
        it would be a bad idea to apply the samed binarization method to
        different kind of files).

        Therefore a trigger of 75 seems to be a good balance for the following
        
        HoughlinesP parameters:
            threshold = 150 # number of intersections to detect a line
            minLineLength = 250 #minimum number of points that can form a line
            maxLineGap = 4 # maximum gap between two points to be considered
                in the same line

        Args:
            src: Source image path
            trigger_analyze: Minimum number of lines required
            year: Document year
            page: Page number
            lines: Detected lines from HoughlinesP

        Returns:
            Source path if analysis should proceed, None otherwise
        """
        if lines is None:
            self.logger.info("No lines detected by HoughlinesP")
            return None

        len_lines = len(lines)
        if len_lines >= trigger_analyze:
            self.logger.info(
                f"✅ Page {page} from document {year} contains {len_lines} lines | 🔧 set to analyze."
            )
            return src

        self.logger.warning(
            f"❌ Discard: page {page} contains {len_lines} lines (below {trigger_analyze} limit) | "
            f"Document {year} discarded\n➡ Consider lowering the trigger limit if needed."
        )
        return None

    def recognize_again(self, src: str) -> Tuple[bool, Optional[int], Optional[int]]:
        """
        Determine if text needs another OCR pass based on content analysis.

        Args:
            src: OCR text result

        Returns:
            Tuple containing:
                - Boolean indicating if another pass is needed
                - OEM value if needed, None otherwise
                - PSM value if needed, None otherwise
        """
        patterns = {
            'digit': r'(?:.\n?|^)+([1-9]|[1-3][1-9]+)(?:\n|\s{2,})+(.*)',
            'string': r'(?:.\n?|^)+((?:Level|Station|Non|Mean|Year|'
                     r'Pressure|Temperature|Relative|Humidity|Wind|Speed|'
                     r'Jan|Feb|Mar|April|May|June|Jul|Aug|Sept|Oct|Nov|Dec)'
                     r'(?:\.|\,|\-|\n|\s{1})+(.*)'
        }

        special_chars = {
            'format': r'\°\s|\s[\.\-\']\s',
            'invalid': r'[^A-Za-z0-9\.\-\'\,\°\-\s\!]'
        }

        # Check digit patterns
        digit_match = re.search(patterns['digit'], src, re.DOTALL)
        if digit_match:
            values = digit_match.group(2)
            has_newlines = bool(re.search(r'(\n+)', values, re.DOTALL))
            has_special = bool(re.search(
                f"({special_chars['format']}|{special_chars['invalid']})", 
                values, re.DOTALL
            ))

            if has_newlines and has_special:
                return True, 1, 11
            elif has_newlines:
                return True, 0, 11
            elif has_special:
                return True, 1, 11

        # Check string patterns
        string_match = re.search(patterns['string'], src, re.DOTALL)
        if string_match:
            values = string_match.group(2)
            has_newlines = bool(re.search(r'(\n+)', values, re.DOTALL))
            
            if not has_newlines:
                return True, 1, 11
            return True, 0, 7

        # Check for special characters without other patterns
        if re.search(
            f"({special_chars['format']}|(\n)+|{special_chars['invalid']})",
            src, re.DOTALL
        ):
            return True, 1, 11

        return False, None, None
