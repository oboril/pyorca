from __future__ import annotations
from dataclasses import dataclass
from typing import List

from datetime import datetime

from orcapython.orca_output.single_point.single_point import SinglePointCalculation
from orcapython.orca_output.geometry_optimization.geometry_optimization import GeometryOptimization
from orcapython.orca_output.relaxed_scan.relaxed_scan import RelaxedScan
from orcapython.orca_output.nudged_elastic_bands.nudged_elastic_bands import NudgedElasticBand

@dataclass(slots=True, init=True)
class OrcaOutput:
    """Summary of ORCA output file"""

    input_filename : str
    """File name of the input file"""

    input : str
    """The input text"""

    terminated_normally : bool
    """Whether the program terminated normally"""

    duration : datetime | None
    """The duration of the program execution, may not be available if ORCA terminates with an error"""

    calculations : List[SinglePoint | GeometryOptimization | RelaxedScan | NudgedElasticBand]
    """Summary of all calculations from the output file"""