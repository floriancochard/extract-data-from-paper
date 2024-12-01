"""Metadata extraction utilities."""

import re
import pathlib
from typing import Union, Optional
from PIL import Image

class Metadata:
    def __init__(self, src: Union[str, pathlib.Path]):
        self.src = pathlib.Path(src)
        if not self.src.exists():
            raise FileNotFoundError(f"Source file {src} not found")
            
    def get_year(self) -> str:
        """Extract year from filename."""
        match = re.search(r"y(\d{4})", str(self.src))
        if not match:
            raise ValueError(f"Could not extract year from {self.src}")
        return match.group(1)

    def get_page(self):
        #assert(isinstance(self.src, (pathlib.Path)))
        page = re.search(r"p(\d{1,3})", str(self.src)).group(1)
        return page

    def get_block(self):
        #assert(isinstance(self.src, (pathlib.Path)))
        block = re.search(r"b(\d{1,2})", str(self.src)).group(1)
        return block
    
    def get_line(self):
        #assert(isinstance(self.src, (pathlib.Path)))
        print("Source:", self.src)
        row = re.search(r"r(\d{1,3})", str(self.src)).group(1)
        return row

    def get_image_height(self):
        from PIL import Image
        img = Image.open(self.src)
        height = img.height
        return height