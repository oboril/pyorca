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

        data = OrcaProperty(
            atoms=None,
            dipole_moment=None,
            rotational_constants=None,
            normal_modes=None,
            thermochemistry=[],
            nmr=None
        )

        return data

