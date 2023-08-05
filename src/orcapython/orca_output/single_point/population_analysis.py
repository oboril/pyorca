from dataclasses import dataclass
from typing import List, Tuple

@dataclass(slots=True, init=True)
class PopulationAnalysis:
    """Electronic population analysis information"""

    charge_mulliken : List[float]
    """Mulliken gross atomic charge"""

    bond_orders : List[Tuple[int, int, float]]
    """Reported Mayer bond orders (idx of 1st atom, idx of 2nd atom, bond order)"""