"""
OCR module for text recognition from processed images.
"""

import cv2
import pytesseract
from dataclasses import dataclass
from typing import Optional
import utils
from core import Params

@dataclass
class OCRConfig:
    """Container for OCR configuration parameters."""
    oem: int
    psm: int
    dpi: int = 300
    lang: str = 'eng'
    write_images: bool = True

    def to_string(self) -> str:
        """Convert config to tesseract command string."""
        return (f'-l {self.lang} --oem {self.oem} --psm {self.psm} '
                f'--dpi {self.dpi} -c tessedit_write_images={str(self.write_images).lower()}')

class OCR:
    """Text recognition from processed images to raw string."""

    def __init__(self, src: str):
        self.src = src
        self._setup_metadata()
        self._setup_configs()
        self.logger = utils.Log().create_logger(self.__class__.__name__)

    def _setup_metadata(self):
        """Initialize metadata from source file."""
        metadata = utils.Metadata(self.src)
        self.year = metadata.get_year()
        self.page = metadata.get_page()
        self.nth_block = metadata.get_block()
        self.nth_line = metadata.get_line()
        self.height = metadata.get_image_height()

    def _setup_configs(self):
        """Initialize OCR configurations."""
        params = Params()
        self.configs = {
            'block': OCRConfig(params.OEM_BLOCK_TO_STRING, params.PSM_BLOCK_TO_STRING),
            'line': OCRConfig(params.OEM_LINE_TO_STRING, params.PSM_LINE_TO_STRING),
            'line_alt': OCRConfig(params.OEM_LINE_TO_STRING_ALT, params.PSM_LINE_TO_STRING_ALT)
        }

    def _preprocess_image(self, img) -> tuple:
        """Preprocess image for OCR."""
        self.logger.debug("\t > grayscale")
        gray = utils.Color().to_gray(img)

        self.logger.debug("\t > binarize")
        _, thresh = cv2.threshold(
            gray, 127, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        
        return gray, thresh

    def _perform_ocr(self, image, config: OCRConfig) -> str:
        """Perform OCR with given configuration."""
        self.logger.debug("\t > text recognition (wait)")
        return pytesseract.image_to_string(image, config=config.to_string())

    def block_to_string(self) -> Optional[str]:
        """Extract text from a block image.
        
        Returns:
            str: Extracted text or None if processing fails
        """
        self.logger.info(
            f"\033[1m Starting - Block segmentation and recognition "
            f"of year {self.year} page {self.page}. \033[0m"
        )

        img = cv2.imread(str(self.src))
        if img is None:
            self.logger.error(f"Failed to load image: {self.src}")
            return None

        self.logger.info(f'\N{wrench} Analyzing block {self.nth_block}')
        
        _, thresh = self._preprocess_image(img)
        output = self._perform_ocr(thresh, self.configs['block'])

        self.logger.debug("\t > text extracted:")
        print(output, '\n')

        return output

    def line_to_string(self) -> Optional[str]:
        """Extract text from a line image.
        
        Returns:
            str: Extracted text or None if processing fails
        """
        H_LIM_RECOGNITION = 60

        self.logger.info(
            f"\033[1m Starting - Line segmentation and recognition "
            f"of year {self.year} page {self.page}. \033[0m"
        )

        img = cv2.imread(str(self.src))
        if img is None:
            self.logger.error(f"Failed to load image: {self.src}")
            return None

        self.logger.info(
            f'\N{wrench} Analyzing line {self.nth_line} from block {self.nth_block}'
        )

        _, thresh = self._preprocess_image(img)
        
        if self.height <= H_LIM_RECOGNITION:
            output = self._perform_ocr(thresh, self.configs['line'])
        else:
            output = self._perform_ocr(thresh, self.configs['line_alt'])
            output = "[NEW]".join(output.split('\n'))
            self.logger.info(
                f"> ℹ info: h > HLIM: p{self.page} b{self.nth_block} "
                f"r{self.nth_line} processed in LTSM mode\n"
            )

        self.logger.debug("\t > text extracted:")
        print(output, '\n')

        return output
