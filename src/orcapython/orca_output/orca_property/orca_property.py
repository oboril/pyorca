from __future__ import annotations
from dataclasses import dataclass
from typing import List, Optional

from orcapython.orca_output.orca_property.normal_modes import NormalModes
from orcapython.orca_output.orca_property.thermochemistry import Thermochemistry
from orcapython.orca_output.orca_property.nmr import Nmr

@dataclass(frozen=True, init=True)
class OrcaProperty:
    """Results of `Orca Property Calculation`"""

    atoms : List[str]
    """Atom symbols like `H` or `C`, the order is identical for entire calculation"""

    initial_coordinates : List[List[float]]
    """Cartesian coordinates of the initial structure in Angstroem, `coordinates[atom_idx][axis]`"""

    dipole_moment : float
    """Dipole moment in Debye"""
    
    rotational_constants : List[float]
    """Rotational constants in cm^-1"""

    normal_modes : NormalModes | None
    """Normal modes and IR intensities, if calculated"""

    thermochemistry : List[Thermochemistry]
    """Thermodynamical energies at individiual temperatures"""

    nmr : Nmr | None
    """NMR shifts and coupling constants, if calculated"""

    def find_and_parse(text: str) -> OrcaProperty:
        """Finds and parses part of the ORCA output text containing information from Orca Property Calculation"""

        atoms, initial_coordinates = _parse_init_coords(text)

        text = _extract_orca_prop_calc(text)

        dipole_moment = _parse_dipole_moment(text)

        rotational_constants = _parse_rotational_constants(text)

        normal_modes = NormalModes.parse(text)

        data = OrcaProperty(
            atoms=atoms,
            initial_coordinates=initial_coordinates,
            dipole_moment=dipole_moment,
            rotational_constants=rotational_constants,
            normal_modes=normal_modes,
            thermochemistry=[],
            nmr=None
        )

        return data

### HELPER FUNCTIONS

import re

from orcapython.orca_output.coordinates import COORDINATES_REGEX, parse_coordinates

def _parse_init_coords(text: str):
    """Returns the first coordinates from the text"""

    initial_coordinates = re.search(COORDINATES_REGEX, text)
    if initial_coordinates is not None:
        atoms, initial_coordinates = parse_coordinates(initial_coordinates.group(0))
    else:
        atoms = None
        initial_coordinates = None

    return atoms, initial_coordinates

def _extract_orca_prop_calc(text: str) -> str:
    """Crops the string so that Orca Property Calculation is at the start"""

    start = re.search(
        r"\*+\s+\*\s*ORCA property calculations\s*\*\s+\*+",
        text
    ).start()

    return text[start:]

def _parse_dipole_moment(text: str) -> float:
    """Finds and parses dipole moment in Debye"""

    found = re.search(
        r"DIPOLE MOMENT(?:.|\s)*?Magnitude \(Debye\)\s+\:\s+(\-?\d+\.\d+)",
        text
    )

    if found is None:
        return None
    
    return float(found.group(1))

def _parse_rotational_constants(text: str) -> List[float]:
    """Finds and parses rotational constants in cm^-1"""

    found = re.search(
        r"Rotational spectrum(?:.|\s)*?Rotational constants in cm\-1:\s+(\-?\d+\.\d+)\s+(\-?\d+\.\d+)\s+(\-?\d+\.\d+)",
        text
    )

    if found is None:
        return None
    
    constants = [float(s) for s in found.group(1,2,3)]
    return constants