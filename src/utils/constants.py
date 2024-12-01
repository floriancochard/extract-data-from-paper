"""Constants used across utility modules."""

# Image processing
MAX_PIXEL_VALUE = 255
MIN_PIXEL_VALUE = 0

# Morphological operations
KERNEL_SIZE_SMALL = (3,3)
KERNEL_SIZE_MEDIUM = (5,5)
KERNEL_SIZE_LARGE = (7,7)

# Text processing
VALID_CHARACTERS = r'[A-Za-z0-9\.\-\'\,\°\-\s\!]'
DIGIT_THRESHOLD = 20
RATIO_THRESHOLD = 0.3 