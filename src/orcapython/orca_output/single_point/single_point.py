from __future__ import annotations
from dataclasses import dataclass

from orcapython.orca_output.orca_property.orca_property import OrcaProperty
from orcapython.orca_output.single_point.population_analysis import PopulationAnalysis
from orcapython.orca_output.single_point.electronic_spectrum import ElectronicSpectrum

@dataclass(frozen=True, init=True)
class SinglePointCalculation(OrcaProperty):
    """Results of single point calculation"""

    population_analysis : PopulationAnalysis
    """Atomic charges and bond orders"""

    electronic_spectrum : ElectronicSpectrum | None
    """UV-VIS transition energies and intensities, if calculated"""

    def parse(text: str) -> SinglePointCalculation:
        """Parses part of ORCA output text containing information about geometry optimization"""

        orca_props = OrcaProperty.find_and_parse(text)
        print(orca_props)

        population_analysis = PopulationAnalysis.parse(text)

        data = SinglePointCalculation(
            **orca_props.__dict__,
            population_analysis=population_analysis,
            electronic_spectrum=None
        )

        return data