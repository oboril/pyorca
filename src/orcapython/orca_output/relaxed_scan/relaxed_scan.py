from __future__ import annotations
from dataclasses import dataclass
from typing import List

from orcapython.orca_output.geometry_optimization.geometry_optimization import GeometryOptimization

@dataclass(frozen=True, init=True)
class RelaxedScan:
    """Results from relaxed surface scan calculation"""

    steps : List[GeometryOptimization]
    """Results from individual constrained optimizations"""