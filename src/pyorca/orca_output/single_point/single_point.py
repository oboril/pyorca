from __future__ import annotations
from dataclasses import dataclass

import re

from pyorca.constants import hartree
from pyorca.orca_output.orca_property.orca_property import OrcaProperty
from pyorca.orca_output.single_point.population_analysis import PopulationAnalysis
from pyorca.orca_output.single_point.electronic_spectrum import ElectronicSpectrum

@dataclass(frozen=True, init=True)
class SinglePointCalculation(OrcaProperty):
    """Results of single point calculation"""

    population_analysis : PopulationAnalysis
    """Atomic charges and bond orders"""

    electronic_spectrum : ElectronicSpectrum | None
    """UV-VIS transition energies and intensities, if calculated"""

    energy : float
    """Final single point energy"""

    def parse(text: str) -> SinglePointCalculation:
        """Parses part of ORCA output text containing information about geometry optimization"""

        orca_props = OrcaProperty.find_and_parse(text)

        population_analysis = PopulationAnalysis.parse(text)
        electronic_spectrum = ElectronicSpectrum.parse(text)

        energy = _parse_energy(text)

        data = SinglePointCalculation(
            **orca_props.__dict__,
            population_analysis=population_analysis,
            electronic_spectrum=electronic_spectrum,
            energy=energy
        )

        return data
    

def _parse_energy(text: str) -> float:
    """Finds and parses all thermochemical data in `Orca Property Calculation` section"""

    energy = re.search(
        r"FINAL SINGLE POINT ENERGY\s+(\-?\d+\.\d+)",
        text
    )

    if energy is None:
        return None
    
    return float(energy.group(1)) * hartree