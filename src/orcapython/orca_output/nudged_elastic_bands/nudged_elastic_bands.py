from __future__ import annotations
from dataclasses import dataclass
from typing import List

from orcapython.orca_output.geometry_optimization.geometry_optimization import GeometryOptimization

@dataclass(frozen=True, init=True)
class NudgedElasticBand:
    """Results from nudged elastic bands calculation"""

    settings : None
    """Settings for the NEB calculation"""

    reactant_optimization : GeometryOptimization | None
    """Geometry optimization of the reactant structure, if calculated"""

    product_optimization : GeometryOptimization | None
    """Geometry optimization of the product structure, if calculated"""
   
    ts_optimization : GeometryOptimization
    """Geometry optimization of the transition state structure"""
    
    image_distances : List[float]
    """Distances of the individual images from reactant in Angstroem"""
    
    image_energies : List[float]
    """Energies of the individual images in kJ/mol"""