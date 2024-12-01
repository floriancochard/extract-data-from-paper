"""
Extract Data from Paper
Base Parameters class.

Copyright (c) 2020
Licensed under GNU AFFERO GENERAL PUBLIC LICENSE
Written by Florian Cochard
"""

from dataclasses import dataclass
from typing import List, Literal

@dataclass(frozen=True)
class TesseractConfig:
    """Tesseract OCR configuration parameters."""
    # OEM (OCR Engine Mode) options
    OEM_BLOCK: int = 0  # Legacy engine only
    OEM_LINE: int = 0   # Legacy engine only
    OEM_LINE_ALT: int = 1  # Neural nets LSTM engine only
    
    # PSM (Page Segmentation Mode) options
    PSM_BLOCK: int = 6  # Assume uniform block of text
    PSM_LINE: int = 6   # Assume uniform block of text
    PSM_LINE_ALT: int = 6  # Assume uniform block of text

@dataclass(frozen=True)
class ProcessingConfig:
    """Image processing configuration parameters."""
    # Minimum number of lines required to trigger analysis
    MIN_LINES_TO_ANALYZE: int = 75

@dataclass(frozen=True)
class TestConfig:
    """Test configuration parameters."""
    # Sample years and pages for testing
    YEARS: List[int] = (1922,)
    PAGES: List[int] = (28, 40)

class Params:
    """Base Parameters Class for OCR and image processing configuration."""

    # OCR method type
    METHOD: Literal["LINE", "BLOCK"] = "LINE"

    def __init__(self):
        self._tesseract = TesseractConfig()
        self._processing = ProcessingConfig()
        self._test = TestConfig()

    @property
    def OEM_BLOCK_TO_STRING(self) -> int:
        """Legacy OEM method for block processing."""
        return self._tesseract.OEM_BLOCK

    @property
    def PSM_BLOCK_TO_STRING(self) -> int:
        """PSM method for block processing."""
        return self._tesseract.PSM_BLOCK

    @property
    def OEM_LINE_TO_STRING(self) -> int:
        """Legacy OEM method for line processing."""
        return self._tesseract.OEM_LINE

    @property
    def PSM_LINE_TO_STRING(self) -> int:
        """PSM method for line processing."""
        return self._tesseract.PSM_LINE

    @property
    def OEM_LINE_TO_STRING_ALT(self) -> int:
        """Alternative OEM method for line processing."""
        return self._tesseract.OEM_LINE_ALT

    @property
    def PSM_LINE_TO_STRING_ALT(self) -> int:
        """Alternative PSM method for line processing."""
        return self._tesseract.PSM_LINE_ALT

    @property
    def TRIGGER_ANALYZE(self) -> int:
        """Minimum number of lines required to trigger analysis."""
        return self._processing.MIN_LINES_TO_ANALYZE

    @property
    def YEARS(self) -> List[int]:
        """Years to process during testing."""
        return list(self._test.YEARS)

    @property
    def PAGES(self) -> List[int]:
        """Pages to process during testing."""
        return list(self._test.PAGES)