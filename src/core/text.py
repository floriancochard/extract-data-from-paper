"""
Text processing module for correcting raw OCR output.
"""

import re
from collections import Counter
from dataclasses import dataclass
from typing import Tuple, List, Optional
import numpy as np
from spellchecker import SpellChecker
import utils

@dataclass
class VariableRules:
    """Rules for variable inference based on digit patterns."""
    pressure = {'digits': ('0', '9'), 'length_range': (90, 110)}
    wind = {'digits': ('0', '1', '2', '3'), 'length_range': (50, 70)}
    diurnal = {'digits': ('+', '-'), 'length_range': None}
    temperature = {'digits': ('7', '8'), 'length_range': (60, 80)}
    humidity = {'digits': ('6', '7', '8', '9'), 'length_range': (40, 60)}
    grass_temp = {'digits': ('6', '7', '8'), 'length_range': (30, 50)}

class Text:
    """Processing functions to correct raw text output."""

    def __init__(self, src: str):
        self.src = src
        self.logger = utils.Log().create_logger(self.__class__.__name__)
        self.rules = VariableRules()

    def estimate_digit_occurence(self) -> Tuple[str, int]:
        """
        Analyze digit patterns in the text.
        
        Returns:
            Tuple[str, int]: Most common first character and total digit count
        """
        # Find first characters after whitespace
        first_chars = re.findall(r'(?<=\s)([\d\+\-].*?)', self.src)
        first_char = Counter(first_chars).most_common(1)[0][0] if first_chars else ''
        
        # Count total digits
        digit_count = len(re.sub(r'[^\d]', '', self.src))
        
        return first_char, digit_count

    def infer_variable(self, most_common_digit: str, digit_length: int) -> str:
        """
        Infer variable type based on digit patterns.
        
        Args:
            most_common_digit: Most frequent first digit
            digit_length: Total number of digits
            
        Returns:
            str: Inferred variable type
        """
        def check_rule(digits: tuple, length_range: Optional[tuple]) -> bool:
            digit_match = most_common_digit in digits
            if length_range is None:
                return digit_match
            return digit_match and length_range[0] < digit_length < length_range[1]

        # Check each variable rule
        if check_rule(**self.rules.pressure):
            self.logger.info('pressure found')
            return 'pressure'
        elif check_rule(**self.rules.wind):
            self.logger.info('wind found')
            return 'wind'
        elif check_rule(**self.rules.diurnal):
            self.logger.info('diurnal inequalities')
            return 'diurnal inequalities'
        elif check_rule(**self.rules.temperature):
            self.logger.info('temperature found')
            return 'temperature'
        elif check_rule(**self.rules.humidity):
            self.logger.info('relative humidity')
            return 'relative humidity'
        elif check_rule(**self.rules.grass_temp):
            self.logger.info('grass temperature')
            return 'grass temperature'
        
        self.logger.info("not found")
        return 'default'

    def legend_levenshtein_correct(self, pathfile: str) -> List[str]:
        """
        Correct text using Levenshtein distance and a custom dictionary.
        
        Args:
            pathfile: Path to dictionary file
            
        Returns:
            List[str]: Corrected text segments
        """
        dst = []
        words = " ".join(self.src).split()
        
        # Initialize spellchecker with custom settings
        spell = SpellChecker(language=None, distance=2, case_sensitive=True)
        spell.word_frequency.load_text_file(pathfile)
        
        # Find misspelled words
        misspelled = spell.unknown(words)
        word_array = np.array([w for w in misspelled if w not in spell])
        corrections = np.array([spell.correction(w) for w in word_array])
        candidates = np.array([spell.candidates(w) for w in word_array])
        
        # Filter for alpha-only corrections
        alpha_mask = np.array([c.isalpha() for c in corrections])
        word_array = word_array[alpha_mask]
        corrections = corrections[alpha_mask]
        candidates = candidates[alpha_mask]
        
        # Apply corrections
        for segment in self.src:
            segment = segment.upper()
            for word, correction, candidate in zip(word_array, corrections, candidates):
                segment = segment.replace(word.upper(), correction.upper())
            dst.append(segment)
            
        return dst

    def text_processing(self) -> str:
        """
        Process text through multiple correction steps.
        
        Returns:
            str: Processed text
        """
        # Initial text normalization
        self.src = utils.Replace(self.src).to_unicode()
        self.src = utils.Replace(self.src).to_essential_digit()

        # Remove unwanted characters
        alpha, self.src = utils.Delete(self.src).delete_unwanted_char()
        self.logger.info(f"Alpha characters: {alpha}")
        
        # Infer variable type
        mcd, mcl = self.estimate_digit_occurence()
        variable = self.infer_variable(mcd, mcl)

        # Text transformations
        self.src = utils.Replace(self.src).digit_to_sign(variable)
        self.src = utils.Replace(self.src).edit_sign()
        self.src = utils.Replace(self.src).char_to_digit()
        self.src = utils.Replace(self.src).sign_to_nan()
        
        # Clean up
        self.src = utils.Delete(self.src).remove_double()
        self.src = utils.Delete(self.src).remove_empty()
        
        # Final formatting
        self.src = utils.Split(self.src).split_digit_from_digit(variable)
        self.src = utils.Insert(self.src).add_point(variable)
        self.src = utils.Replace(self.src).edit_digit()

        return f"{alpha} {self.src}"
