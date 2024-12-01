"""
Extract Data from Paper
Base Initialization class.

Copyright (c) 2020
Licensed under GNU AFFERO GENERAL PUBLIC LICENSE
Written by Florian Cochard
"""

from pathlib import Path
from dataclasses import dataclass
from typing import List
from core import Params

@dataclass
class DirectoryPaths:
    """Container for directory paths used in the application."""
    selection: Path
    preprocess: Path
    block: Path
    line: Path
    log: Path
    tessinput: Path
    tessinput_line: Path

@dataclass
class FilePaths:
    """Container for file paths used in the application."""
    selection: Path
    preprocess: Path
    block: Path
    line: Path
    log: Path
    tessinput: Path
    tessinput_line: Path

class IO:
    """Create and manage files and directories for the program."""

    def __init__(self):
        params = Params()
        self.years = params.YEARS
        self.pages = params.PAGES
        
        # Format year and page numbers consistently
        self.years_formatted = [f"{year:04d}" for year in self.years]
        self.pages_formatted = [f"{page:03d}" for page in self.pages]
        
        # Set up base paths
        self.cwd = Path.cwd()
        self.data_dir = Path('data')
        self.input_dir = self.data_dir / 'input'
        self.output_dir = self.data_dir / 'output'
        
        # Initialize directory and file structures
        self._setup_paths()
        self._create_directories()
        self._create_files()
        self._setup_input_files()
        self.PATH_SELECTION = self.dirs.selection
        self.PATH_SELECTION_FILE = self.files.selection
        self.PATH_PREPROCESS = self.dirs.preprocess
        self.PATH_PREPROCESS_FILE = self.files.preprocess
        self.PATH_BLOCK = self.dirs.block
        self.PATH_BLOCK_FILE = self.files.block
        self.PATH_LINE = self.dirs.line
        self.PATH_LINE_FILE = self.files.line
        # The PATH_INPUT_FILES is now properly set by _setup_input_files()

    def _setup_paths(self):
        """Initialize all directory and file paths."""
        self.path_input = self.cwd / self.input_dir
        self.path_output = self.cwd / self.output_dir

        # Setup directory paths
        self.dirs = DirectoryPaths(
            selection=self.path_output / 'selection',
            preprocess=self.path_output / 'preprocess',
            block=self.path_output / 'block',
            line=self.path_output / 'line',
            log=self.path_output / 'log',
            tessinput=self.path_output / 'tessinput',
            tessinput_line=self.path_output / 'tessinput/line'
        )

        # Setup file paths
        self.files = FilePaths(
            selection=self.dirs.selection / 'selection.txt',
            preprocess=self.dirs.preprocess / 'preprocess.txt',
            block=self.dirs.block / 'block.txt',
            line=self.dirs.line / 'line.txt',
            log=self.dirs.log / 'log.txt',
            tessinput=self.dirs.tessinput / 'tessinput.txt',
            tessinput_line=self.dirs.tessinput_line / 'line.txt'
        )

    def _create_directories(self):
        """Create all required directories."""
        for directory in vars(self.dirs).values():
            directory.mkdir(parents=True, exist_ok=True)

    def _create_files(self):
        """Create all required files."""
        for file_path in vars(self.files).values():
            file_path.touch(exist_ok=True)

    def _setup_input_files(self):
        """Setup input file paths based on years and pages."""
        self.input_files = [
            f"input_y{year}-p{page}.png"
            for year in self.years_formatted
            for page in self.pages_formatted
        ]

        self.input_file_paths = []
        for year in self.years_formatted:
            year_dir = self.path_input / year
            if year_dir.exists():
                for input_file in self.input_files:
                    file_path = year_dir / input_file
                    if file_path.exists():
                        self.input_file_paths.append(file_path)

        self.PATH_INPUT_FILES = self.input_file_paths if self.input_file_paths else []

        if not self.PATH_INPUT_FILES:
            raise ValueError("No input files found. Please check that your input directory contains the expected files.")

    @property
    def all_directories(self) -> List[Path]:
        """Return a list of all directory paths."""
        return list(vars(self.dirs).values())

    @property
    def all_files(self) -> List[Path]:
        """Return a list of all file paths."""
        return list(vars(self.files).values())
