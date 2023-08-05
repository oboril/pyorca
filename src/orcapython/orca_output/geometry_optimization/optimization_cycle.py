from __future__ import annotations
from dataclasses import dataclass
from typing import List

@dataclass(slots=True, init=True)
class OptimizationCycle:
    """Information about individual geometry optimization cycle."""

    coordinates : List[List[float]]
    """Cartesian coordinates in Angstroem, `coordinates[atom_idx][axis]`"""