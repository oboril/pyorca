from __future__ import annotations
from dataclasses import dataclass
from typing import List, Tuple

@dataclass(frozen=True, init=True)
class BondOrder:
    """Bond order between two atoms"""

    atom1: int
    """Index of the first atom"""

    atom2: int
    """Index of the second atom"""

    order: float
    """Bond order"""

@dataclass(frozen=True, init=True)
class PopulationAnalysis:
    """Electronic population analysis information"""

    charges_mulliken : List[float]
    """Mulliken atomic charges"""

    charges_loewdin : List[float]
    """Loewdin atomic charges"""

    bond_orders : List[BondOrder]
    """Reported Mayer bond orders"""

    def parse(text: str) -> PopulationAnalysis:
        """Finds and parses population analysis data"""

        charges_mulliken = _parse_charge_mulliken(text)

        charges_loewdin = _parse_charge_loewdin(text)

        bond_orders = _parse_mayer_bond_order(text)

        data = PopulationAnalysis(
            charges_mulliken=charges_mulliken,
            charges_loewdin=charges_loewdin,
            bond_orders=bond_orders
        )

        return data

### HELPER FUNCTIONS

import re

def _parse_charge_mulliken(text: str) -> List[float]:
    """Finds and parses Mulliken charges"""
    extract = re.search(
        r"MULLIKEN ATOMIC CHARGES(?:.*\n)*?Sum of atomic charges",
        text
    )
    if extract is None:
        return None
    extract = extract.group(0)

    charges = re.findall(
        r"\d+\s+\w+\s*\:\s+(\-?\d+\.\d+)",
        extract
    )

    return [float(ch) for ch in charges]


def _parse_charge_loewdin(text: str) -> List[float]:
    """Finds and parses Loewdin charges"""
    extract = re.search(
        r"LOEWDIN ATOMIC CHARGES\n\-+(?:\s*\d+\s*\w+\s*\:.*\n)*",
        text
    )
    if extract is None:
        return None
    extract = extract.group(0)

    charges = re.findall(
        r"\d+\s+\w+\s*\:\s+(\-?\d+\.\d+)",
        extract
    )

    return [float(ch) for ch in charges]

def _parse_mayer_bond_order(text: str) -> List[BondOrder]:
    """Finds and parses Mayer bond orders"""
    extract = re.search(
        r"Mayer bond orders.+\n((?:B.+\n)*)",
        text
    )
    if extract is None:
        return None
    extract = extract.group(1)

    bonds = re.findall(
        r"B\(\s*(\d+)\-\w+\s*\,\s*(\d+)\-\w+\s*\)\s*\:\s+(\-?\d+\.\d+)",
        extract
    )

    bonds = [
        BondOrder(int(idx1), int(idx2), float(order))
        for idx1, idx2, order in bonds
    ]

    return bonds