from dataclasses import dataclass
from typing import List, Tuple

@dataclass(frozen=True, init=True)
class ElectronicSpectrum:
    """Calculated energies and intensities for electronic transitions"""

    energies : List[float]
    """Excited state energies in cm^-1"""

    wavelengths : List[float]
    """Transition wavelengths from ground state in nm"""

    intensities : List[float]
    """The `fosc` values for transitions from ground states"""