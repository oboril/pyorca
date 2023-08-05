from dataclasses import dataclass
from typing import List

@dataclass(frozen=True, init=True)
class Nmr:
    """
    Calculated NMR data, such as shifts and coupling constants.

    Note that shifts must be adjusted as: `s(reported) = s(reference) - s(sample)`
    """

    shifts : List[float|None]
    """Individual isotropic shielding constants, None if wasn't calculated for given atom."""
    
    coupling_constants : List[List[float|None]] | None
    """Isotropic coupling constants in Hz, None if wasn't calculated for given interaction"""