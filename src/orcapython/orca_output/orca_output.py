from __future__ import annotations
from dataclasses import dataclass
from typing import List

from datetime import timedelta
import re

from orcapython.orca_output.single_point.single_point import SinglePointCalculation
from orcapython.orca_output.geometry_optimization.geometry_optimization import GeometryOptimization
from orcapython.orca_output.relaxed_scan.relaxed_scan import RelaxedScan
from orcapython.orca_output.nudged_elastic_bands.nudged_elastic_bands import NudgedElasticBand

@dataclass(slots=True, init=True)
class OrcaOutput:
    """Summary of ORCA output file"""

    input_filename : str
    """File name of the input file"""

    input_text : str
    """The input text"""

    terminated_normally : bool
    """Whether the program terminated normally"""

    duration : datetime | None
    """The duration of the program execution, may not be available if ORCA terminates with an error"""

    calculations : List[SinglePointCalculation | GeometryOptimization | RelaxedScan | NudgedElasticBand]
    """Summary of all calculations from the output file"""

    def parse_file(path: str) -> OrcaOutput:
        """Parses ORCA output file"""
        with open(path, "r") as f:
            text = f.read()

        return OrcaOutput.parse(text)

    def parse(text: str) -> OrcaOutput:
        """Parses text from ORCA output file"""

        input_filename, input_text = _parse_orca_input(text)
        terminated_normally, duration = _parse_orca_termination(text)

        data = OrcaOutput(
            input_filename=input_filename,
            input_text=input_text,
            terminated_normally=terminated_normally,
            duration=duration,
            calculations=[]
        )

        return data


def _parse_orca_input(text: str) -> Tuple[str, str]:
    """Parses the input filename and input text from ORCA output file"""

    input_area = re.search(
        r"INPUT FILE\n=+\n((?:.|\s)*?) *\*\*\*\*END OF INPUT\*\*\*\*",
        text
    ).group(1)

    filename = re.search(
        r"NAME = (.*)\n",
        input_area
    ).group(1)

    lines = re.findall(
        r"\|\s*\d+\> (.*)",
        input_area
    )

    input_text = '\n'.join([line for line in lines])
    
    return filename, input_text

def _parse_orca_termination(text: str) -> Tuple[bool, datetime]:
    """Returns (terminated normally, total run time)"""

    terminated_normally = re.search(
        r"ORCA TERMINATED NORMALLY",
        text
    ) is not None

    timing = re.search(
        r"TOTAL RUN TIME: (\d+) days (\d+) hours (\d+) minutes (\d+) seconds (\d+) msec",
        text
    )

    if timing is None:
        return terminated_normally, None
    
    d,h,m,s,ms = [int(s) for s in timing.group(1,2,3,4,5)]
    duration = timedelta(days=d, hours=h, minutes=m, seconds=s, milliseconds=ms)

    return terminated_normally, timing

_calculation_headings = {
    r"" : SinglePointCalculation,
    r"" : GeometryOptimization,
    r"" : RelaxedScan,
    r"" : NudgedElasticBand
}

def _parse_calculations(text: str) -> List[SinglePointCalculation | GeometryOptimization | RelaxedScan | NudgedElasticBand]:
    """Splits the input text into calculations and calls the individual calculation parsers"""

