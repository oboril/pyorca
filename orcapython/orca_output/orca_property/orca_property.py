from dataclasses import dataclass
from typing import List, Optional

from orcapython.orca_output.orca_property.normal_modes import NormalModes
from orcapython.orca_output.orca_property.thermochemistry import Thermochemistry
from orcapython.orca_output.orca_property.nmr import Nmr

@dataclass(slots=True, init=True)
class OrcaProperty:
    """
    Results of `Orca Property Calculation`

    Attributes
    ----------

    atoms : List[str]
        Atom symbols like `H` or `C`, the order is identical for entire calculation

    dipole_moment : float
        Dipole moment in Debye
    
    rotational_constants : List[float]
        Rotational constants in cm^-1

    normal_modes : NormalModes | None
        Normal modes and IR intensities, if calculated

    thermochemistry : List[Thermochemistry]
        Thermodynamical energies at individiual temperatures

    nmr : Nmr | None
        NMR shifts and coupling constants, if calculated

    """
    atoms : List[str]
    dipole_moment : float
    rotational_constants : List[float]
    normal_modes : NormalModes | None
    thermochemistry : List[Thermochemistry]
    nmr : Nmr | None

