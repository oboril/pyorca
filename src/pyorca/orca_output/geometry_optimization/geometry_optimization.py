from __future__ import annotations
from dataclasses import dataclass
from typing import List

from pyorca.orca_output.geometry_optimization.optimization_cycle import OptimizationCycle
from pyorca.orca_output.orca_property.orca_property import OrcaProperty
from pyorca.orca_output.single_point.single_point import SinglePointCalculation

@dataclass(frozen=True, init=True)
class GeometryOptimization(OrcaProperty):
    """Information about geometry optimization cycles and final evaluation."""

    cycles : List[OptimizationCycle]
    """Individual Optimization cycles"""

    final_single_point: SinglePointCalculation
    """Final evaluation at the stationary point"""

    converged : bool
    """Whether the optimization reached stationary point"""

    final_energy : float
    """Final energy in kJ/mol"""

    final_coordinates : List[List[float]]
    """Final cartesian coordinates in Angstroem, `coordinates[atom_idx][axis]`"""

    def __iter__(self):
        """Returns iterator that iterates though the Geometry Optimization Cycles"""
        return iter(self.cycles)

    def parse(text: str) -> GeometryOptimization:
        """Parses part of ORCA output text containing information about geometry optimization"""

        orca_props = OrcaProperty.find_and_parse(text)

        converged = _optimization_converged(text)

        final_single_point = _parse_final_evaluation(text)

        final_energy = _find_final_energy(text)

        atoms, final_coordinates = _find_final_coordinates(text)
        # assert(all([a1 == a2 for a1,a2 in zip(orca_props.atoms, atoms)]))

        cycles = _parse_optimization_cycles(text)

        data = GeometryOptimization(
            **orca_props.__dict__,
            cycles=cycles,
            final_coordinates=final_coordinates,
            converged=converged,
            final_energy=final_energy,
            final_single_point=final_single_point
        )

        return data

### HELPER FUNCTIONS

import re
from pyorca.constants import hartree
from pyorca.orca_output.coordinates import COORDINATES_REGEX, parse_coordinates

def _optimization_converged(text: str) -> bool:
    """Tries to find the `Optimization Converged` message"""

    converged = re.search(
        r"THE OPTIMIZATION HAS CONVERGED",
        text
    ) is not None

    return converged

def _find_final_energy(text: str) -> float:
    """Finds the last Single Point Energy value"""
    energies = re.findall(
        r"FINAL SINGLE POINT ENERGY\s+(\-?\d+\.\d+)",
        text
    )
    
    return float(energies[-1])*hartree

def _find_final_coordinates(text: str) -> Tuple[List[str], List[List[float]]]:
    """Finds the last entry of cartesian coordinates"""
    coords = re.findall(
        COORDINATES_REGEX,
        text
    )
    
    last_coords = coords[-1]

    atoms, coords = parse_coordinates(last_coords)

    return atoms, coords

def _parse_optimization_cycles(text: str) -> List[OptimizationCycle]:
    """Splits the input and passes the individual cycles to OptimizationCycle.parse"""

    cycle_starts = re.finditer(
        r"GEOMETRY OPTIMIZATION CYCLE\s+\d+",
        text
    )

    converged = re.search(
        r"THE OPTIMIZATION HAS CONVERGED",
        text
    )

    if converged is None:
        end = len(text)
    else:
        end = converged.endpos

    segments = [cs.start() for cs in cycle_starts] + [end]

    cycles = []
    for start, end in zip(segments[:-1], segments[1:]):
        cycle = OptimizationCycle.parse(text[start:end])
        cycles.append(cycle)

    return cycles

def _parse_final_evaluation(text: str) -> SinglePointCalculation:
    """Finds the Final Energy Evaluation at the Stationary Point and passes it to the parser"""

    start = re.search(
        r"\*\*\*\s*FINAL ENERGY EVALUATION AT THE STATIONARY POINT\s*\*\*\*",
        text
    )
    if start is None:
        return None
    start = start.start()

    return SinglePointCalculation.parse(text[start:])


