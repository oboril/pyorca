from dataclasses import dataclass
from typing import List, Optional

from orcapython.orca_output.orca_property.vibrational_spectrum import VibrationalSpectrum
from orcapython.orca_output.orca_property.thermochemistry import Thermochemistry
from orcapython.orca_output.orca_property.nmr import Nmr

@dataclass(slots=True, init=True)
class OrcaProperty:
    """
    Results of `Orca Property Calculation`

    Attributes
    ----------

    dipole_moment : float
        Dipole moment in Debye
    
    rotational_constants : List[float]
        Rotational constants in cm^-1

    vibrational_spectrum : VibrationalSpectrum | None
        Normal modes and IR intensities, if calculated

    thermochemistry : List[Thermochemistry]
        Thermodynamical energies at individiual temperatures

    nmr : Nmr | None
        NMR shifts and coupling constants, if calculated

    """
    dipole_moment : float
    rotational_constants : List[float]
    vibrational_spectrum : VibrationalSpectrum | None
    thermochemistry : List[Thermochemistry]
    nmr : Nmr | None

