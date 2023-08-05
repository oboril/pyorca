from __future__ import annotations
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

    imaginary : int
    """Count of imaginary vibrational modes - normal modes with negative energies"""

    def parse(text: str) -> NormalModes | None:
        """Finds and parses vibrational data, or None if vibrational data is not present"""

        normal_modes = _parse_normal_modes(text)
        if normal_modes is None:
            return None
        
        imaginary = sum([1 for x in normal_modes if x < 0.])

        ir_frequencies, ir_extinction = _parse_ir_spectrum(text)

        data = NormalModes(
            normal_modes=normal_modes,
            imaginary=imaginary,
            ir_frequencies=ir_frequencies,
            ir_extinction=ir_extinction
        )

        return data

### HELPER FUNCTIONS

import re

def _parse_normal_modes(text: str) -> None | List[float]:
    """Tries to find and extract all harmonic frequencies"""

    extracted = re.search(
        r"VIBRATIONAL FREQUENCIES(?:.*\n){5}((?:.*cm\*\*-1.*\n)+)",
        text
    )

    if extracted is None:
        return None
    
    extracted = extracted.group(1)

    freqs = re.findall(
        r"\d+\:\s+(\-?\d+\.\d+) cm",
        extracted
    )

    freqs = [float(f) for f in freqs]

    return freqs


def _parse_ir_spectrum(text: str) -> Tuple[None, None] | Tuple[List[float], List[float]]:
    """Tries to find and extract information about IR spectrum"""

    extracted = re.search(
        r"IR SPECTRUM(?:.*\n){6}((?:\s*\d+\:.+\n)+)",
        text
    )

    if extracted is None:
        return None, None
    
    extracted = extracted.group(1)

    spectrum = re.findall(
        r"\d+\:\s+(\-?\d+\.\d+)\s+(\-?\d+\.\d+)",
        extracted
    )

    spectrum = [[float(wavenum), float(eps)] for wavenum, eps in spectrum]

    return (list(x) for x in zip(*spectrum))
