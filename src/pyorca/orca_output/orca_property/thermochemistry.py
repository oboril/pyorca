from __future__ import annotations
from dataclasses import dataclass

import re

from pyorca.constants import hartree

@dataclass(frozen=True, init=True)
class Thermochemistry:
    """
    Results of thermochemistry calculations at single temperature.
    
    All energies are in kJ/mol, entropy is in J/mol/K.
    """
    
    temperature : float
    """Temperature in Kelvin"""

    single_point_energy : float
    """Electronic single point energy"""

    zpe : float
    """Zero point energy - vibrational correction to electronic energy"""
    
    inner_energy : float
    """Inner energy `U`"""
    
    enthalpy : float
    """Enthalpy `H`"""
    
    entropy : float
    """Entropy `S`"""
    
    gibbs_energy : float
    """Gibb's energy `G`"""

    def parse(text: str) -> Thermochemistry:
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
            res = re.findall(q, text)
            if len(res) != 1:
                print("WARNING: unexpected number of entries for thermochemistry")
            vals.append(float(res[0]))
        
        data = Thermochemistry(
            temperature = vals[0],
            single_point_energy = vals[1] * hartree,
            zpe = vals[2] * hartree,
            inner_energy = vals[3] * hartree,
            enthalpy = vals[4] * hartree,
            entropy = vals[5] * hartree,
            gibbs_energy = vals[6] * hartree,
        )

        return data
