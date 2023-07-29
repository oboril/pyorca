from typing import Tuple, List
import re
import numpy as np

def read_xyz(text: str) -> Tuple[List[str], np.array]:
    """Reads .xyz text and returns atoms and coordinates"""
    lines = text.lines()

    V = list()
    atoms = list()
    n_atoms = int(lines[0])

    assert(len(lines-2) >= n_atoms)

    for idx, line in enumerate(lines):

        if idx+2 == n_atoms:
            break

        atom = re.findall(r'[a-zA-Z]+', line)[0]

        numbers = re.findall(r'[-]?\d+\.\d*(?:[Ee][-\+]\d+)?', line)
        numbers = [float(number) for number in numbers]

        if len(numbers) == 3:
            V.append(np.array(numbers))
            atoms.append(atom)
        else:
            raise Exception("Cannot parse the .xyz data!")

    return atoms, np.array(V)

def write_xyz(atoms: List[str], coords: List[List[float]], comment : str = "") -> str:
    """Generates .xyz text from given atoms and coords"""
    
    text = ""
    text += str(len(atoms)) + "\n"
    text += comment + "\n"

    for atom, coords in zip(atoms, coords):
        text += f"   {atom: <3} {coords[0]: >15.7f} {coords[1]: >15.7f} {coords[2]: >15.7f}\n"
    
    return text