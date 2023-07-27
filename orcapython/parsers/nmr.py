from __future__ import annotations
from typing import Optional, List, Dict

import re

class NMR:
    """
    This class contains isotropic shielding constants (in ppm) and coupling constants (in Hz)

    Attributes
    ----------
    shifts : List[Tuple[int,string,float]]
        List of shifts, contains (atom index, element, shift)
    
    couplings : Optional[List[List[float]]]
        A 2D array containing pairwise coupling constants in Hz

    couplings_atoms : Optional[List[Tuple[int,string]]]
       List of atom indeces and symbols, in the same order as coupling constants
    """

    def __init__(self) -> NMR:
        """Dummy init function. Use NMR.parse() to parse actual data"""

    def parse(text: str, reference_shifts : Dict[str,float] = {}) -> Optional[NMR]:
        """
        Parses the NMR data from text from .out file

        Parameters
        ----------
        reference_shifts : Dict[str, float]
            Reference shifts for the individual atoms. If not provided, 0.0 is used
        
        """

        # Shifts
        extract = re.compile(r"CHEMICAL SHIELDING SUMMARY \(ppm\)\n(?:.*\n){5}(?:\s+\d+\s+\w+\s+.*\n)*")
        query = re.compile(r"\n\s*(\d+)\s+(\w+)\s+(\-?\d+\.\d+)")

        extracted = extract.findall(text)
        if len(extracted) == 0:
            return None
        elif len(extracted) > 1:
            print("WARNING: Found multiple entries for NMR data!")
        
        result = NMR()

        result.shifts = [
            (
                int(m[0]),
                m[1],
                (0. if m[1] not in reference_shifts else reference_shifts[m[1]]) - float(m[2])
            )
            for m in query.findall(extracted[-1])]
        
        # Coupling constants

        extract = re.compile(r"SUMMARY OF ISOTROPIC COUPLING CONSTANTS(?:.*\n){3}((?:\s+\d+\s+\w+\s+.*\n)*)")
        extracted = extract.findall(text)
        
        if len(extracted) == 0:
            result.couplings = None
            result.couplings_atoms = None
        else:
            result.couplings = []
            result.couplings_atoms = []

            extracted = extracted[-1].split("\n")[:-1]
            for line in extracted:
                parts = line.split()
                idx = int(parts[0])
                symbol = parts[1]
                coupl = [float(p) for p in parts[2:]]

                result.couplings.append(coupl)
                result.couplings_atoms.append((idx, symbol))

        return result

    def __str__(self) -> str:
        res = "NMR shifts:"
        res += "\n-----------"
        for i, a, s in self.shifts:
            sh = f"{s:0.2f} ppm"
            res += f"\n   {a+str(i): <5}{sh: >10}"
        
        if self.couplings is not None:
            res += "\n\nNMR coupling constants [Hz]"
            res += "\n---------------------------"
            res += "\n"+" "*5+"".join([f"{a+str(i): >10}" for i,a in self.couplings_atoms])
            for coupl, (i,a) in zip(self.couplings, self.couplings_atoms):
                res += f"\n{a+str(i): >5}"+"".join([f"{c: >10.2f}" for c in coupl])

        return res