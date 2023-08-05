from dataclasses import dataclass
from typing import List, Tuple

@dataclass(slots=True, init=True)
class PopulationAnalysis:
    """
    Some population analysis information.

    Attributes
    ----------
    
    charge_mulliken : List[float]
        Mulliken gross atomic charge
    
    bond_orders : List[Tuple[int, int, float]]
        Reported Mayer bond orders (idx of 1st atom, idx of 2nd atom, bond order)
    
    """

    charge_mulliken : List[float]
    bond_orders : List[Tuple[int, int, float]]