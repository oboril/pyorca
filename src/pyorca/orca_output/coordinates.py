from typing import List, Tuple

import re

COORDINATES_REGEX = r"CARTESIAN COORDINATES \(ANGSTROEM\)\n\-+\n(?:\s+\w+(?:\s+\-?\d+\.\d+){3}\s)+"

def parse_coordinates(text: str) -> Tuple[List[str], List[List[float]]]:
    """Takes in block of text with Cartesian coordinates and returns atoms and their coordinates"""

    matches = re.finditer(
        r"(\w+)\s+(\-?\d+\.\d+)\s+(\-?\d+\.\d+)\s+(\-?\d+\.\d+)",
        text
    )

    atoms = []
    coords = []

    for m in matches:
        atoms.append(m.group(1))
        c = [float(x) for x in m.group(2,3,4)]
        coords.append(c)

    return atoms, coords
