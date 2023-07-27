from __future__ import annotations
from typing import Optional, List

import orcapython.parsers.basic_parsers as bp
from orcapython.parsers.thermochemistry import Thermochemistry

class OutputData:
    """
    Stores all data that is extracted from .out file

    Attributes
    ----------
    terminated_normally : bool
        Whether the ORCA program terminated normally

    single_point_energies : List[float]
        All values of "FINAL SINGLE POINT ENERGY" in the output file

    final_energy : Optional[float]
        The final value of "FINAL SINGLE POINT ENERGY"

    vib_freqs : List[float]
        The frequencies of the normal modes

    negative_freqs : bool
        Whether the normal modes include imaginary nodes (modes with negative frequencies)

    thermochemistry : List[Thermochemistry]
        Contains list of thermodynamical data at individual temperatures
    """

    def __init__(self, text: str):
        """Takes in text from .out file and parses all data"""
        self.terminated_normally = bp.exit_status(text)
        self.single_point_energies = bp.single_point_energies(text)
        self.final_energy = None if len(self.single_point_energies) == 0 else self.single_point_energies[-1]
        self.vib_freqs = bp.freqs(text)
        self.negative_freqs = any([f < 0 for f in self.vib_freqs])
        self.thermochemistry = Thermochemistry.parse_all(text)

    def parse_file(path: str) -> OutputData:
        """Parses .out file"""
        with open(path, "r") as f:
            text = f.read()
            parsed = OutputData(text)
        return parsed