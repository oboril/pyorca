from typing import Optional, List, Tuple

import re

def exit_status(text: str) -> bool:
    """Returns true if ORCA terminated normally"""
    query = re.compile(r"\*\*\*\*ORCA TERMINATED NORMALLY\*\*\*\*")
    matches = query.findall(text)
    return len(matches) > 0

def single_point_energies(text: str) -> List[float]:
    """Returns list of all `FINAL SINGLE POINT ENERGY` values"""
    query = re.compile(r"FINAL SINGLE POINT ENERGY\s+(\-?\d+\.\d+)")
    matches = query.findall(text)
    energies = [float(m) for m in matches]
    return energies

def freqs(text: str) -> List[float]:
    """Returns list of harmonic frequencies"""
    extract = re.compile(r"VIBRATIONAL FREQUENCIES\n(?:.*\n){4}((?:\s*\d+\:.*cm\*\*\-1.*\n)*)")
    query = re.compile(r"(\-?\d+\.\d+) cm\*\*\-1")
    extracted = extract.findall(text)
    if len(extracted) == 0:
        return []
    elif len(extracted) > 1:
        print("WARNING: The output file contains multiple records with vibrational frequencies")

    freqs = [float(m) for m in query.findall(extracted[-1])]
    return freqs

def electronic(text: str) -> List[Tuple[float,float]]:
    """Returns list of intensities and wavelenghts of electronic transitions"""
    extract = re.compile(r"ABSORPTION SPECTRUM VIA TRANSITION ELECTRIC DIPOLE MOMENTS(?:.*\n){5}(?:\s*\d+\s+\-?\d+.*\n)*")
    query = re.compile(r"\n\s*\d+\s+\-?\d+\.\d+\s+(\-?\d+\.\d+)\s+(\-?\d+\.\d+)")
    extracted = extract.findall(text)
    if len(extracted) == 0:
        return []
    elif len(extracted) > 1:
        print("WARNING: The output file contains multiple records with electronic transitions")

    trans = [(float(m[1]), float(m[0])) for m in query.findall(extracted[-1])]
    return trans