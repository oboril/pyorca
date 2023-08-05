from dataclasses import dataclass

from orcapython.orca_output.orca_property.orca_property import OrcaProperty
from orcapython.orca_output.single_point.population_analysis import PopulationAnalysis
from orcapython.orca_output.single_point.electronic_spectrum import ElectronicSpectrum

@dataclass(slots=True, init=True)
class SinglePointCalculation(OrcaProperty):
    """
    Results of single point calculation

    Attributes
    ----------

    population_analysis : PopulationAnalysis
        Atomic charges and bond orders

    electronic_spectrum : ElectronicSpectrum | None
        UV-VIS transition energies and intensities, if calculated

    """

    population_analysis : PopulationAnalysis
    electronic_spectrum : ElectronicSpectrum | None