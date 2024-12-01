#!/usr/bin/env python3
"""
Main entry point for the image processing and OCR pipeline.
Handles command line arguments and orchestrates the processing workflow.
"""

from pathlib import Path
from typing import List
import core
import conf
import csv
import pandas as pd

class Pipeline:
    """Class to manage the image processing pipeline."""

    def __init__(self):
        """Initialize pipeline with core parameters and IO."""
        self.params = core.Params()
        self.io = core.IO()
        
        # Make sure input files exist
        if not hasattr(self.io, 'PATH_INPUT_FILES'):
            raise AttributeError("IO class must have PATH_INPUT_FILES attribute. Please check core.IO implementation.")

    def run_selection(self) -> None:
        """Run image selection phase."""
        selection = [
            core.Image(src, self.io.PATH_SELECTION).selection(self.params.TRIGGER_ANALYZE) 
            for src in self.io.PATH_INPUT_FILES
        ]
        self.io.PATH_SELECTION_FILE.write_text("\n".join([str(sel) for sel in selection]))

    def run_preprocessing(self) -> None:
        """Run image preprocessing phase."""
        source = self.io.PATH_SELECTION_FILE.read_text().split("\n")
        preprocess = [
            core.Image(Path(src), self.io.PATH_PREPROCESS).clean() 
            for src in source
        ]
        self.io.PATH_PREPROCESS_FILE.write_text("\n".join([str(pre) for pre in preprocess]))

    def run_block_segmentation(self) -> None:
        """Run block segmentation phase."""
        source = self.io.PATH_PREPROCESS_FILE.read_text().split("\n")
        blocks = [
            core.Image(Path(src), self.io.PATH_BLOCK).block_segmentation() 
            for src in source
        ]
        self.io.PATH_BLOCK_FILE.write_text("\n".join([block for sublist in blocks for block in sublist]))

    def run_line_segmentation(self) -> List[dict]:
        """Run line segmentation and OCR phase."""
        source = self.io.PATH_BLOCK_FILE.read_text().split("\n")
        results = []

        if self.params.METHOD == "BLOCK":
            for src in source:
                path = Path(src)
                try:
                    # More flexible parsing of the filename
                    parts = path.stem.split('-')
                    if len(parts) >= 3:
                        year, page, block_num = parts[-3:]  # Take last 3 parts if available
                    else:
                        # Handle cases with fewer parts - adjust this based on your actual filename format
                        year = parts[0]
                        page = parts[1]
                        block_num = "1"  # default value
                except ValueError as e:
                    logger.error(f"Error parsing filename {path.stem}: {e}")
                    continue
                text = core.OCR(path).block_to_string()
                results.append({
                    'text': text,
                    'year': year,
                    'page': page,
                    'block': block_num
                })
            return results

        if self.params.METHOD == "LINE":
            lines = []
            for src in source:
                path = Path(src)
                try:
                    # More flexible parsing of the filename 
                    parts = path.stem.split('-')
                    if len(parts) >= 3:
                        year, page, block_num = parts[-3:]  # Take last 3 parts if available
                    else:
                        # Handle cases with fewer parts - adjust this based on your actual filename format
                        year = parts[0]
                        page = parts[1]
                        block_num = "1"  # default value
                except ValueError as e:
                    logger.error(f"Error parsing filename {path.stem}: {e}")
                    continue
                block_lines = core.Image(path, self.io.PATH_LINE).line_segmentation()
                
                for line_path in block_lines:
                    # Convert string to Path object
                    line_path = Path(line_path)
                    line_num = line_path.stem.split('-')[-1]  # Now this will work
                    text = core.OCR(line_path).line_to_string()
                    results.append({
                        'text': text,
                        'year': year,
                        'page': page,
                        'block': block_num,
                        'line': line_num
                    })
            return results

        raise ValueError(f"Unsupported method: {self.params.METHOD}")


def main():
    """Main entry point for the application."""
    parser = conf.parser.get_parser()
    args = vars(parser.parse_args())

    if args['version']:
        conf.Parser().version()
        return

    if args['remove_output']:
        conf.Parser().clear_output()
        return

    # Initialize and run pipeline
    pipeline = Pipeline()
    pipeline.run_selection()
    pipeline.run_preprocessing()
    pipeline.run_block_segmentation()
    results = pipeline.run_line_segmentation()
    
    # Use pandas for better CSV handling
    df = pd.DataFrame(results)
    df = df.sort_values(['year', 'page', 'block', 'line'] if 'line' in df.columns else ['year', 'page', 'block'])
    df.to_csv('output.csv', index=False, encoding='utf-8')


if __name__ == "__main__":
    main()