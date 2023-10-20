"""This file contains methods for generating 3D conformers using RD Kit"""

from typing import Literal, Tuple, List
from dataclasses import dataclass

from rdkit.Chem import AllChem
from rdkit import Chem

from pyorca.constants import kcal_mol

@dataclass(frozen=True,init=True)
class ConformerResult:
    atoms: List[str]
    """List of atom symbols"""

    coordinates: List[List[float]]
    """Coordinates of individual atoms, `coordinates[atom_idx][axis]`"""

    energy: float
    """Force field energy of the conformer, kJ/mol"""

    converged: bool
    """Whether the force field optimization converged"""

def conformer_from_smiles(
    smiles: str,
    n_confs: int = 10,
    force_field : Literal['UFF', 'MMFF94'] = 'UFF',
    ff_iters : int = 1000
) -> ConformerResult:
    """
    Generates single 3D conformer from SMILES.

    RDKit is used to create `n_confs` random conformers,
    the conformers are optimized using selected MM force field,
    and the geometry of the conformer with lowest energy is returned.

    This is not rigorous conformer search!
    """
    assert(force_field in ['UFF', 'MMFF94'])

    # Generate molecule from SMILES
    molecule = AllChem.MolFromSmiles(smiles)
    molecule = Chem.AddHs(molecule)

    # Generate 3D structure
    AllChem.EmbedMolecule(molecule)

    if force_field == 'UFF':
        AllChem.UFFOptimizeMolecule(molecule)
    elif force_field == 'MMFF94':
        AllChem.MMFFOptimizeMolecule(molecule)

    # Create conformers, cids = conformer IDs
    cids = AllChem.EmbedMultipleConfs(molecule, numConfs=n_confs)

    # optimize all conformers, res = list of (not converged, energy)
    if force_field == 'UFF':
        res = AllChem.UFFOptimizeMoleculeConfs(molecule, maxIters=ff_iters)
    elif force_field == 'MMFF94':
        res = AllChem.MMFFOptimizeMoleculeConfs(molecule, maxIters=ff_iters)

    # zip the results together, (not converged, energy, id)
    data = list(zip(*zip(*res),cids))

    # sort by energy
    data = sorted(data, key=lambda d: d[1])

    # take the conformer with lowest energy
    not_converged, energy, cid = data[0]

    # get coordinates
    atoms = []
    coordinates = []
    for i, atom in enumerate(molecule.GetAtoms()):
        positions = molecule.GetConformer(cid).GetAtomPosition(i)
        atoms.append(atom.GetSymbol())
        coordinates.append([positions.x, positions.y, positions.z])

    data = ConformerResult(
        atoms=atoms,
        coordinates=coordinates,
        energy=energy*kcal_mol,
        converged=(not_converged==0)
    )

    return data