from __future__ import annotations
from dataclasses import dataclass
from typing import List

from orcapython.orca_output.geometry_optimization.geometry_optimization import GeometryOptimization

@dataclass(slots=True, init=True)
class RelaxedScan:
    """
    Results from relaxed surface scan calculation

    Attributes
    ----------
    
    steps : List[GeometryOptimization]
        Results from individual constrained optimizations

    """

    steps : List[GeometryOptimization]