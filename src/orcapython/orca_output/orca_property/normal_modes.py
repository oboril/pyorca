from dataclasses import dataclass
from typing import List, Tuple

@dataclass(frozen=True, init=True)
class NormalModes:
    """Contains data from harmonic vibrational modes"""
    
    normal_modes : List[float]
    """Frequencies of normal modes in cm^-1"""

    ir_frequencies : List[float]
    """Frequencies of vibrational modes"""
    
    ir_extinction : List[float]
    """Extinction coefficients of vibrational modes"""