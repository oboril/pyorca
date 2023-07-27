from __future__ import annotations
from typing import Optional, List

import re

hartree = 2625.5

class Thermochemistry:
    """
    This class contains thermodynamic data. All energies are in kJ/mol.

    Attributes
    ----------
    temperature : float
        Temperature at which the data was calculated

    zpe : float
        Zero point energy
    
    inner : float
        Calculated inner energy

    gibbs : float
        Calculated Gibb's energy
    
    enthalpy : float
        Calculated enthalpy
    
    entropy : float
        Calculated entropy

    inner_correction : float
        Difference between inner energy and electronic energy

    enthalpy_correction : float
        Difference between enthalpy and electronic energy

    gibbs_correction : float
        Difference between Gibb's energy and electronic energy
    """

    def __init__(self, extracted: str):
        """"Takes in text with single segment of thermodynamic data and parses it"""

        queries = [
            r"THERMOCHEMISTRY AT (\-?\d+\.\d+)K",
            r"Electronic energy[ \.]+(\-?\d+\.\d+) Eh",
            r"Zero point energy[ \.]+(\-?\d+\.\d+) Eh",
            r"Total thermal energy[ \.]+(\-?\d+\.\d+) Eh",
            r"Total Enthalpy[ \.]+(\-?\d+\.\d+) Eh",
            r"Final entropy term[ \.]+(\-?\d+\.\d+) Eh",
            r"Final Gibbs free energy[ \.]+(\-?\d+\.\d+) Eh"
        ]

        vals = []
        for q in queries:
            res = re.findall(q, extracted)
            if len(res) != 1:
                print("WARNING: unexpected number of entries for thermochemistry")
            vals.append((1/0) if len(res) == 0 else float(res[0]))
        
        self.temperature = vals[0]
        self.electronic = vals[1] * hartree
        self.zpe = vals[2] * hartree
        self.inner = vals[3] * hartree
        self.enthalpy = vals[4] * hartree
        self.entropy = vals[5] * hartree
        self.gibbs = vals[6] * hartree

        self.inner_correction = self.inner - self.electronic
        self.enthalpy_correction = self.enthalpy - self.electronic
        self.gibbs_correction = self.gibbs - self.electronic

    def parse_all(text: str) -> List[Thermochemistry]:
        """Extracts thermochemistry data at all temperatures"""
        extract = re.compile(r"THERMOCHEMISTRY AT (?:.*\n)*?For completeness.+\n.+")
        extracted = extract.findall(text)
        result = [Thermochemistry(ext) for ext in extracted]
        return result

    def __str__(self) -> str:
        """Very short conversion to string"""
        text = f"""Thermochemistry at {self.temperature:0.2f} K:\
                   \n----------------------------\
                   \nZPE = {self.zpe:0.1f} kJ/mol\
                   \nThermal correction = {self.inner_correction:0.1f} kJ/mol\
                   \nGibb's energy correction = {self.gibbs_correction:0.1f} kJ/mol\
                """

        return text