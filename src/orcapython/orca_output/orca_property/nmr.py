from __future__ import annotations
from dataclasses import dataclass
from typing import List

@dataclass(frozen=True, init=True)
class Nmr:
    """
    Calculated NMR data, such as shifts and coupling constants.

    Note that shifts must be adjusted as: `s(reported) = s(reference) - s(sample)`
    """

    shifts : List[NmrShift]
    """Individual isotropic shielding constants"""
    
    coupling_constants : List[List[float|None]] | None
    """Isotropic coupling constants in Hz, None if wasn't calculated for given interaction"""

    def parse(text: str) -> Nmr | None:
        """Parses NMR data from `Orca Property Calculation` text. The total number of atoms must be provided"""

        shifts = _parse_shifts(text)

        if shifts is None:
            return None

        coupling_constants = _parse_couplings(text)

        data = Nmr(
            shifts=shifts,
            coupling_constants=coupling_constants
        )

        return data

@dataclass(init=True)
class NmrShift:
    """Isotropic NMR shielding constant of single nucleus"""

    atom: str
    """Atom symbol, such as `H` or `C`"""

    atom_idx: int
    """Index of the given nucleus"""

    shift: float
    """Isotropic shielding constant"""

@dataclass(frozen=True, init=True)
class NmrCouplings:
    """Isotropic NMR coupling constants in Hz"""

    atom_idx: List[int]
    """Indeces of the nuclei"""
    
    atoms: List[str]
    """Atom symbols, such as `H` or `C`"""

    constants: List[List[float]]
    """Isotropic coupling constants in Hz"""

### HELPER FUNCTIONS

import re

def _parse_shifts(text: str) -> List[float] | None:
    """Finds and parses chemical shifts"""
    extracted = re.search(
        r"CHEMICAL SHIELDING SUMMARY \(ppm\)\n(?:.*\n){5}(?:\s+\d+\s+\w+\s+.*\n)*",
        text
    )

    if extracted is None:
        return None
    
    extracted = extracted.group(0)
    
    shifts = re.findall(
        r"\n\s*(\d+)\s+(\w+)\s+(\-?\d+\.\d+)",
        extracted
    )

    shifts = [
        NmrShift(
            atom=int(m[0]),
            atom_idx=m[1],
            shift=float(m[2])
        ) for m in shifts
    ]

    return shifts

def _parse_couplings(text: str) -> NmrCouplings | None:
    """Finds and parses coupling constants"""
    
    extracted = re.search(
        r"SUMMARY OF ISOTROPIC COUPLING CONSTANTS(?:.*\n){3}((?:\s+\d+\s+\w+\s+.*\n)*)",
        text
    )

    if extracted is None:
        return None
    
    extracted = extracted.group(1)
    
    couplings = []
    atoms = []
    atom_idx = []

    extracted = extracted.split("\n")[:-1]
    for line in extracted:
        parts = line.split()
        idx = int(parts[0])
        symbol = parts[1]
        coupl = [float(p) for p in parts[2:]]
        couplings.append(coupl)
        atoms.append(symbol)
        atom_idx.append(idx)
    
    data = NmrCouplings(
        atoms=atoms,
        atom_idx=atom_idx,
        constants=couplings
    )
    return data