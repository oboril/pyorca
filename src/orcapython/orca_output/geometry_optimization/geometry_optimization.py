from __future__ import annotations
from dataclasses import dataclass
from typing import List

from orcapython.orca_output.geometry_optimization.optimization_cycle import OptimizationCycle
from orcapython.orca_output.orca_property.orca_property import OrcaProperty

@dataclass(frozen=True, init=True)
class GeometryOptimization(OrcaProperty):
    """Information about geometry optimization cycles and final evaluation."""

    cycles : List[OptimizationCycle]
    """Individual Optimization cycles"""

    final_coordinates : List[List[float]]
    """Final cartesian coordinates in Angstroem, `coordinates[atom_idx][axis]`"""

    converged : bool
    """Whether the optimization reached stationary point"""

    final_energy : float
    """Final energy in kJ/mol"""

    def parse(text: str) -> GeometryOptimization:
        """Parses part of ORCA output text containing information about geometry optimization"""

        orca_props = OrcaProperty.find_and_parse(text)
        print(orca_props)

        data = GeometryOptimization(
            **orca_props.__dict__,
            cycles=None,
            final_coordinates=None,
            converged=None,
            final_energy=None,
        )

        return data