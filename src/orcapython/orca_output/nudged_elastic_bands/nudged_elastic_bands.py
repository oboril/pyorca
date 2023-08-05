from __future__ import annotations
from dataclasses import dataclass
from typing import List

@dataclass(slots=True, init=True)
class NudgedElasticBand:
    """
    Results from nudged elastic bands calculation

    Attributes
    ----------

    settings : NebSettings
        NEB settings

    reactant_optimization : GeometryOptimization | None
        Geometry optimization of the reactant structure, if calculated

    product_optimization : GeometryOptimization | None
        Geometry optimization of the product structure, if calculated
   
    ts_optimization : GeometryOptimization
        Geometry optimization of the transition state structure
    
    image_distances : List[float]
        Distances of the individual images in Angstroem
    
    image_energies : List[float]
        Energies of the individual images in kJ/mol
    """