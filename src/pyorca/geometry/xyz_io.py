from typing import Tuple, List
import re
import numpy as np

def read_xyz(text: str) -> Tuple[List[str], np.array, str]:
    """Reads .xyz text and returns atoms, coordinates and comment line"""
    lines = text.splitlines()

    V = list()
    atoms = list()
    n_atoms = int(lines[0])

    assert(len(lines)-2 >= n_atoms)

    comment = lines[1]

    for idx, line in enumerate(lines[2:]):

        if idx == n_atoms:
            break

        atom = re.findall(r'[a-zA-Z]+', line)[0]

        numbers = re.findall(r'[-]?\d+\.\d*(?:[Ee][-\+]\d+)?', line)
        numbers = [float(number) for number in numbers]

        if len(numbers) == 3:
            V.append(np.array(numbers))
            atoms.append(atom)
        else:
            raise Exception("Cannot parse the .xyz data!")

    return atoms, np.array(V), comment

def write_xyz(atoms: List[str], coords: List[List[float]], comment : str = "") -> str:
    """Generates .xyz text from given atoms and coords"""
    
    text = ""
    text += str(len(atoms)) + "\n"
    text += comment + "\n"

    text += generate_xyz_block(atoms, coords)
    text += "\n" # some programs struggle to parse files without empty line at the end
    
    return text

def generate_xyz_block(atoms: List[str], coords: List[List[float]]) -> str:
    """Generates xyz block from given atoms and coords. This can be used to generate ORCA input files."""
    text = ""
    for atom, coords in zip(atoms, coords):
        text += f"   {atom: <3} {coords[0]: >15.7f} {coords[1]: >15.7f} {coords[2]: >15.7f}\n"
    text = text[:-1]
    return text