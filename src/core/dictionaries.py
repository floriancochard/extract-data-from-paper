import numpy as np
from collections import chain
from typing import List, Dict

# Constants
TEMP_MIN = -10
TEMP_MAX = 1000
PRESSURE_MIN = 0
PRESSURE_MAX_LOW = 10
PRESSURE_MAX_HIGH = 100

def generate_temperature_ranges() -> Dict[str, Dict[str, str]]:
    """Generate temperature-related dictionaries."""
    # Diurnal inequalities (250-350 in 0.01 steps)
    diurnal_ineq = list(map('{:.2f}'.format, np.arange(250, 350, 0.01)))
    
    # Monthly means (-5 to +5 in 0.01 steps)
    monthly_mean = (
        list(map('{:.2f}'.format, np.arange(-5.0, 0, 0.01))) +
        list(map('+{:.2f}'.format, np.arange(0, 5.0, 0.01)))
    )
    
    # Absolute extremes (+10 to +99 in 0.1 steps)
    extremes = list(map('+{:.1f}'.format, np.arange(10, 99, 0.1)))
    
    return {
        'diurnal_ineq': {k: {'value': v} for k, v in zip(diurnal_ineq, diurnal_ineq)},
        'monthly_mean': {k: {'value': v} for k, v in zip(monthly_mean, monthly_mean)},
        'extremes': {k: {'value': v} for k, v in zip(extremes, extremes)}
    }

def generate_pressure_ranges() -> List[str]:
    """Generate pressure-related values with proper formatting."""
    pressure_low = [f'00{round(x, 2)}' for x in np.arange(PRESSURE_MIN, PRESSURE_MAX_LOW, 0.01)]
    pressure_high = [f'0{round(x, 2)}' for x in np.arange(PRESSURE_MAX_LOW, PRESSURE_MAX_HIGH, 0.01)]
    return pressure_low + pressure_high

def generate_numeric_ranges() -> List[float]:
    """Generate basic numeric ranges."""
    return (
        list(map(lambda x: round(x, 2), np.arange(TEMP_MIN, TEMP_MAX, 0.01))) +  # floats
        list(map(int, np.arange(TEMP_MIN, TEMP_MAX, 1)))  # integers
    )

# Meteorological categories
CATEGORIES = {
    'months': ['Jan', 'Feb', 'Mar', 'April', 'May', 'June', 'July', 'Aug', 'Sept', 'Oct', 'Nov', 'Dec'],
    'variables': [
        'pressure', 'absolute pressure', 'pressure at station level and at sea level.',
        'absolute temperature', 'temperature', 'temperature in the ground', 'night grass temperature',
        'humidity', 'humidity : annual means', 'relative humidity',
        'rainfall', 'duration of bright sunshine', 'wind',
        'cloud', 'solar', 'potential gradient',
        'magnetism', 'water', 'pollution'
    ]
}

# Create dictionaries
month_dict = {k: {'value': v} for k, v in zip(CATEGORIES['months'], CATEGORIES['months'])}
variable_dict = {
    k.upper(): {'value': k.upper()} 
    for k in CATEGORIES['variables']
}

def generate_word_list() -> None:
    """Generate and save the complete word list to a file."""
    # Combine all numeric and text values
    all_values = (
        generate_numeric_ranges() +
        generate_pressure_ranges() +
        [word for word in combined_upper.split()] +
        [word for word in combined_lower.split()]
    )
    
    # Write unique values to file
    with open('values.user-words', 'w') as f:
        for item in sorted(set(all_values)):
            f.write(f"{item}\n")

# ... rest of the existing category lists (months, variables, statistics, etc.) ...
