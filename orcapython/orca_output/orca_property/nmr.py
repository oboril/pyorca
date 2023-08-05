from dataclasses import dataclass
from typing import List

@dataclass(slots=True, init=True)
class Nmr:
    """
    Calculated NMR data, such as shifts and coupling constants.

    Note that shifts must be adjusted as: `s(reported) = s(reference) - s(sample)`

    Attributes
    ----------

    shifts : List[NmrShift]
        Individual isotropic shielding constants
    
    coupling_constants : NmrCouplingConstants | None
        Isotropic coupling constants in Hz

    """

    shifts : List[NmrShift]
    
    coupling_constants : NmrCouplingConstants | None


@dataclass(slots=True, init=True)
class NmrShift:
    """
    Isotropic NMR shielding data
    
    Attributes
    ----------

    atom : str
        Atom symbol, such as `H` or `C`

    atom_idx : int
        Atom index as in input coordinates, 0-indexed

    shift : float
        Shift due to isotropic shielding in ppm. Must be subtracted from reference shift.

    """
    atom : str
    atom_idx : int
    shift : float

@dataclass(slots=True, init=True)
class NmrCouplingConstants:
    """
    Isotropic coupling constants in Hz. All three list have identical indexing.

    Attributes
    ----------

    atoms : List[str]
        Atom symbols, such as `H` or `C`
    
    atoms_idx : List[int]
        Atom indeces as in input coordinates, 0-indexed

    constants : List[List[float]]
        Isotropic coupling constants in Hz
    """

    atoms : List[str]
    atoms_idx : List[int]
    constants : List[List[float]]