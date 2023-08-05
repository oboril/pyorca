"""This module contains scripts for working with molecule coordinates"""

from orcapython.xyz.xyz_io import read_xyz, write_xyz
from orcapython.xyz.align import aligned_rmsd, align_xyz_files
from orcapython.xyz.smiles_to_xyz import smiles_to_xyz, smiles_file_to_xyz