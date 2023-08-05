from dataclasses import dataclass
from typing import List, Tuple

@dataclass(slots=True, init=True)
class VibrationalSpectrum:
    """
    Contains data from harmonic vibrational modes.

    Attributes
    ----------

    normal_modes : List[float]
        frequencies of normal modes in cm^-1

    ir_frequencies : List[float]
        frequencies of vibrational modes
    
    ir_extinction : List[float]
        extinction coefficients of vibrational modes
    
    """
    
    normal_modes: List[float]
    ir_frequencies: List[float]
    ir_extinction: List[float]