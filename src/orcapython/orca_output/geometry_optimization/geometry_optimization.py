from __future__ import annotations
from dataclasses import dataclass
from typing import List

from orcapython.orca_output.geometry_optimization.optimization_cycle import OptimizationCycle
from orcapython.orca_output.orca_property.orca_property import OrcaProperty

@dataclass(slots=True, init=True)
class GeometryOptimization(OrcaProperty):
    """
    Information about geometry optimization cycles and final evaluation.

    Attributes
    ----------

    cycles : List[OptimizationCycle]
        Individual Optimization cycles
    
    final_coordinates : List[List[float]]
        Final cartesian coordinates in Angstroem, `coordinates[atom_idx][axis]`

    converged : bool
        Whether the optimization reached stationary point
    
    final_energy : float
        Final energy in kJ/mol
    
    """

    cycles : List[OptimizationCycle]
    final_coordinates : List[List[float]]
    converged : bool
    final_energy : float