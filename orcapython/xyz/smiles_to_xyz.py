"""This uses OpenBabel to convert smiles file to .xyz structure"""

import os
import subprocess

def smiles_file_to_xyz(input: str, output: str):
    """
    Uses OpenBabel to get 3D geometry of the molecule specified by SMILES

    The `input` and `output` arguments specify path to the input and output files
    
    Reference: https://open-babel.readthedocs.io/en/latest/3DStructureGen/SingleConformer.html
    """

    command = 'obabel -i smi "%INP%" -o xyz -O "%OUT%" -h --gen3d --best --weighted'\
        .replace("%INP%", input)\
        .replace("%OUT%", output)

    status = subprocess.getstatusoutput(command)
    if status[0] != 0:
        raise Exception(f"OpenBabel exited with code {status[0]}!\n"+status[1])

def smiles_to_xyz(input: str, output: str):
    """
    Uses OpenBabel to get 3D geometry of the molecule specified by SMILES

    `input` is the input smiles string

    `output` is path to the .xyz file
    
    Reference: https://open-babel.readthedocs.io/en/latest/3DStructureGen/SingleConformer.html
    """

    command = 'obabel -:"%INP%" -o xyz -O "%OUT%" -h --gen3d --conformer --ff UFF --systematic --score energy'\
        .replace("%INP%", input)\
        .replace("%OUT%", output)

    status = subprocess.getstatusoutput(command)
    if status[0] != 0:
        raise Exception(f"OpenBabel exited with code {status[0]}!\n"+status[1])