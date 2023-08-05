from __future__ import annotations
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

    def parse(text: str) -> ElectronicSpectrum | None:
        """Finds and parses electronic transition data"""
        data = _parse_electronic(text)
        
        if data is None:
            return None

        energies, wavelenghts, intensities = data

        return ElectronicSpectrum(energies, wavelenghts, intensities)



### HELPER FUNCTIONS

import re

def _parse_electronic(text: str) -> Tuple[List[float], List[float], List[float]] | None:
    """Returns list of intensities and wavelenghts of electronic transitions"""
    extract = re.search(
        r"ABSORPTION SPECTRUM VIA TRANSITION ELECTRIC DIPOLE MOMENTS(?:.*\n){5}(?:\s*\d+\s+\-?\d+.*\n)*",
        text
    )
    if extract is None:
        return None
    extract = extract.group(0)

    transitions = re.findall(
        r"\n\s*\d+\s+(\-?\d+\.\d+)\s+(\-?\d+\.\d+)\s+(\-?\d+\.\d+)",
        extract
    )

    energies = [float(m[0]) for m in transitions]
    wavelenghts = [float(m[1]) for m in transitions]
    intensities = [float(m[2]) for m in transitions]
    return energies, wavelenghts, intensities