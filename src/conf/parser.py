"""
Command line argument parser for the application.
"""

import os
from pathlib import Path
from typing import Optional
import argparse
from dataclasses import dataclass
import core

@dataclass
class CommandLineArgs:
    """Container for command line arguments."""
    remove_output: bool = False
    version: bool = False
    input_path: Optional[Path] = None
    output_path: Optional[Path] = None
    verbose: bool = False

def get_parser() -> argparse.ArgumentParser:
    """
    Create and configure the argument parser.
    
    Returns:
        argparse.ArgumentParser: Configured parser
    """
    parser = argparse.ArgumentParser(
        description="Extract and process data from historical weather records"
    )
    
    # File operations
    parser.add_argument(
        '-ro', '--remove-output',
        action='store_true',
        help="Remove all files from output directory",
        default=False
    )
    
    # Paths
    parser.add_argument(
        '-i', '--input',
        type=Path,
        help="Path to input directory",
        default=None
    )
    
    parser.add_argument(
        '-o', '--output',
        type=Path,
        help="Path to output directory",
        default=None
    )
    
    # Utility options
    parser.add_argument(
        '-v', '--version',
        action='store_true',
        help="Display version of the project",
        default=False
    )
    
    parser.add_argument(
        '--verbose',
        action='store_true',
        help="Enable verbose output",
        default=False
    )
    
    return parser

class Parser:
    """Command line argument parser and handler."""

    def __init__(self):
        self.parser = get_parser()
        self.args = self._parse_args()

    def _parse_args(self) -> CommandLineArgs:
        """
        Parse command line arguments into a structured format.
        
        Returns:
            CommandLineArgs: Parsed arguments
        """
        parsed = self.parser.parse_args()
        return CommandLineArgs(
            remove_output=parsed.remove_output,
            version=parsed.version,
            input_path=parsed.input,
            output_path=parsed.output,
            verbose=parsed.verbose
        )

    def _get_output_directory(self) -> Path:
        """
        Get the output directory path, using default if not specified.
        
        Returns:
            Path: The resolved output directory path
        """
        return self.args.output_path or Path('data/output')

    def _remove_directory_contents(self, directory: Path) -> None:
        """
        Remove all contents of a directory while preserving the directory itself.
        
        Args:
            directory: Path to the directory to clear
            
        Raises:
            OSError: If there's an error during file removal
        """
        for item in directory.glob('*'):
            if item.is_file():
                item.unlink()
            elif item.is_dir():
                import shutil
                shutil.rmtree(item)

    def clear_output(self) -> int:
        """
        Remove all files from the output directory.
        
        Returns:
            int: Exit code (0 for success)
        """
        if not self.args.remove_output:
            return 0

        output_dir = self._get_output_directory()
        
        if not output_dir.exists():
            print(f"Output directory {output_dir} does not exist")
            return 0

        try:
            self._remove_directory_contents(output_dir)
            print(f"Cleared contents of {output_dir}")
            return 0
        except OSError as e:
            print(f"Error clearing output directory: {e}")
            return 1

    def version(self) -> str:
        """
        Get the current version of the project.
        
        Returns:
            str: Version string
        """
        return '0.1.alpha'

    def process(self) -> int:
        """
        Process the command line arguments and execute corresponding actions.
        
        Returns:
            int: Exit code (0 for success)
        """
        if self.args.version:
            print(f"Version: {self.version()}")
            return 0
            
        if self.args.remove_output:
            return self.clear_output()
            
        if self.args.verbose:
            print("Verbose mode enabled")
            
        # Add additional processing logic here
        return 0

    @property
    def input_path(self) -> Optional[Path]:
        """Get the input directory path."""
        return self.args.input_path

    @property
    def output_path(self) -> Optional[Path]:
        """Get the output directory path."""
        return self.args.output_path

    @property
    def is_verbose(self) -> bool:
        """Check if verbose mode is enabled."""
        return self.args.verbose
