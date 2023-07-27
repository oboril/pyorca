from __future__ import annotations
from typing import Optional, List

import orcapython.parsers.basic_parsers as bp
from orcapython.parsers.thermochemistry import Thermochemistry
from orcapython.parsers.nmr import NMR

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
    
    electronic_trans : List[Tuple[float,float]]
        Contains list of electronic transitions (intensity, wavelength)
    
    nmr : NMR
        Contains NMR data - shifts and coupling constants
    """

    def __init__(self, text: str):
        """Takes in text from .out file and parses all data"""
        self.terminated_normally = bp.exit_status(text)
        self.single_point_energies = bp.single_point_energies(text)
        self.final_energy = None if len(self.single_point_energies) == 0 else self.single_point_energies[-1]
        self.vib_freqs = bp.freqs(text)
        self.negative_freqs = any([f < 0 for f in self.vib_freqs])
        self.thermochemistry = Thermochemistry.parse_all(text)
        self.electronic_trans = bp.electronic(text)
        self.nmr = NMR.parse(text)

    def parse_file(path: str) -> OutputData:
        """Parses .out file"""
        with open(path, "r") as f:
            text = f.read()
            parsed = OutputData(text)
        return parsed

    def format_el_transitions(self, n_max : int = 10, min_lambda : float = 0) -> str:
        """Formats the most intense electronic transitions for printing"""
        text = ""
        text += "Electronic transitions\n"
        text += "----------------------\n"
        text += f" I [A.U.]  wavelength\n"

        trans = [t for t in self.electronic_trans if t[1] > min_lambda]

        for i,w in sorted(trans)[::-1][:10]:
            text += f"{i: >8.4f}   {w:>6.1f} nm\n"

        return text[:-1]

    def summary(self) -> str:
        """Generates summary of all parsed data"""
        text = ""

        if self.terminated_normally:
            text += "ORCA terminated normally\n"
        else:
            text += "ORCA did NOT terminate normally!\n"
        
        if self.final_energy is not None:
            text += f"Final energy: {self.final_energy:0.1f} kJ/mol ({len(self.single_point_energies)} S.P. energies logged)\n"
        
        if len(self.vib_freqs) > 0:
            if not self.negative_freqs:
                text += f"Vibrational frequencies available (n={len(self.vib_freqs)}), all are positive\n"
            else:
                text += f"Vibrational frequencies available (n={len(self.vib_freqs)})\n"
                text += f"WARNING: there are negative frequencies (n={sum(1 if f < 0 else 0 for f in self.vib_freqs)})\n"
        
        for th in self.thermochemistry:
            text += "\n"+str(th)+"\n"

        if len(self.electronic_trans) > 0:
            text += "\n"+self.format_el_transitions()+"\n"
        
        if self.nmr is not None:
            text += "\n"+str(self.nmr)+"\n"
        
        return text