from __future__ import annotations
from dataclasses import dataclass
from typing import List

from pyorca.orca_output.geometry_optimization.geometry_optimization import GeometryOptimization

@dataclass(frozen=True, init=True)
class RelaxedScan:
    """Results from relaxed surface scan calculation"""

    steps : List[GeometryOptimization]
    """Results from individual constrained optimizations"""

    def parse(text: str) -> RelaxedScan:
        """Parses the relaxed surface scan data from the text from ORCA output file"""

        steps = _parse_relaxed_scan(text)

        return RelaxedScan(steps)


### HELPER FUNCTIONS

import re

def _parse_relaxed_scan(text: str) -> List[GeometryOptimization]:
    """Splits the text into individual steps and passes them to GeometryOptimization.parse()"""

    starts = re.finditer(
        r"RELAXED SURFACE SCAN STEP\s+\d+",
        text
    )

    segments = [s.start() for s in starts] + [len(text)]

    optimizations = []
    for start, end in zip(segments[:-1], segments[1:]):
        opt = GeometryOptimization.parse(text[start:end])
        optimizations.append(opt)
    
    return optimizations