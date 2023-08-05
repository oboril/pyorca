from __future__ import annotations
from dataclasses import dataclass
from typing import List

from pyorca.orca_output.single_point.population_analysis import PopulationAnalysis

@dataclass(frozen=True, init=True)
class OptimizationCycle:
    """Information about individual geometry optimization cycle."""

    energy : float
    """Single point electronic energy in this cycle in kJ/mol"""

    coordinates : List[List[float]]
    """Cartesian coordinates in Angstroem, `coordinates[atom_idx][axis]`"""

    population_analysis : PopulationAnalysis
    """Bond orders and atomic charges"""

    def parse(text: str) -> OptimizationCycle:
        """Parses information from text extracted from output file"""

        energy = _parse_energy(text)

        coordinates = _parse_coords(text)

        population_analysis = PopulationAnalysis.parse(text)

        data = OptimizationCycle(
            energy=energy,
            coordinates=coordinates,
            population_analysis=population_analysis
        )

        return data

### HELPER FUNCTIONS

import re
from pyorca.constants import hartree
from pyorca.orca_output.coordinates import COORDINATES_REGEX, parse_coordinates

def _parse_energy(text: str) -> float:
    """Finds and parses single point energy"""

    energy = re.search(
        r"FINAL SINGLE POINT ENERGY\s+(\-?\d+\.\d+)",
        text
    )

    if energy is None:
        return None
    
    return float(energy.group(1)) * hartree


def _parse_coords(text: str) -> List[List[float]]:
    """Returns the coordinates from the text"""

    coordinates = re.search(COORDINATES_REGEX, text)

    if coordinates is None:
        return None

    _, coordinates = parse_coordinates(coordinates.group(0))

    return coordinates