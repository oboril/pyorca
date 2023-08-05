from __future__ import annotations
from dataclasses import dataclass
from typing import List

from pyorca.orca_output.geometry_optimization.geometry_optimization import GeometryOptimization
from pyorca.orca_output.orca_property.orca_property import OrcaProperty
from pyorca.orca_output.nudged_elastic_bands.settings import NebSettings

@dataclass(frozen=True, init=True)
class NudgedElasticBands(OrcaProperty):
    """Results from nudged elastic bands calculation"""

    converged: bool
    """Whether the NEB calculation converged"""

    settings : NebSettings
    """Settings for the NEB calculation"""

    reactant_optimization : GeometryOptimization | None
    """Geometry optimization of the reactant structure, if calculated"""

    product_optimization : GeometryOptimization | None
    """Geometry optimization of the product structure, if calculated"""
   
    ts_optimization : GeometryOptimization
    """Geometry optimization of the transition state structure"""
    
    image_distances : List[float]
    """RMSD (root mean squared distance) of images from reactant in Angstroem"""

    image_energies : List[float]
    """Energies of the individual images in kJ/mol"""

    def parse(text: str) -> NudgedElasticBands:
        """Parses the Nudged Elastic Bands data from ORCA output text"""

        orca_props = OrcaProperty.find_and_parse(text)

        converged = _parse_converged(text)

        settings = NebSettings.parse(text)

        image_energies, image_distances = _parse_path(text)

        reactant_optimization, product_optimization, ts_optimization = _parse_neb_data(text)

        data = NudgedElasticBands(
            **orca_props.__dict__,
            converged=converged,
            settings=settings,
            reactant_optimization=reactant_optimization,
            product_optimization=product_optimization,
            ts_optimization=ts_optimization,
            image_energies=image_energies,
            image_distances=image_distances
        )

        return data


### HELPER FUNCTIONS

import re
from pyorca.constants import hartree

def _parse_converged(text: str) -> bool:
    """Searches for the convergence message"""

    converged = re.search(
        r"THE NEB OPTIMIZATION HAS CONVERGED",
        text
    ) is not None

    return converged

def _parse_path(text: str) -> Tuple[List[float], List[float]]:
    """Finds and parses path summary. Returns energies and distances"""
    extract = re.search(
        r"PATH SUMMARY\s+\-{5,}(?:.|\s)*?Image.*\n((?:\s*\d+.*\n)*)",
        text
    ).group(1)

    images = re.findall(
        r"\d+\s+(\-?\d+\.\d+)\s+(\-?\d+\.\d+)\s+\-?\d+\.\d+\s+",
        extract
    )

    energies = [float(en)*hartree for _, en in images]
    distances = [float(dist) for dist, _ in images]

    return energies, distances

def _parse_neb_data(text: str) -> Tuple[GeometryOptimization, GeometryOptimization, GeometryOptimization]:
    """Splits the text into individual parts and passes them to other parsers"""

    reactant_opt = re.search(
        r"REACTANT OPTIMIZATION\s+\-{5,}",
        text
    )
    if reactant_opt is not None:
        reactant_opt = reactant_opt.start()

    product_opt = re.search(
        r"PRODUCT OPTIMIZATION\s+\-{5,}",
        text
    )
    if product_opt is not None:
        product_opt = product_opt.start()

    neb_opt = re.search(
        r"NEB OPTIMIZATION\s*\-{5,}",
        text
    )
    if neb_opt is not None:
        neb_opt = neb_opt.start()

    ts_opt = re.search(
        r"\*\s+TS OPTIMIZATION\s+\*\s+\*{5,}",
        text
    )
    if ts_opt is not None:
        ts_opt = ts_opt.start()

    locs = [reactant_opt, product_opt, neb_opt, ts_opt, len(text)]
    locs = [l for l in locs if l is not None]

    if reactant_opt is not None:
        end = min([l for l in locs if l > reactant_opt])
        reactant_optimization = GeometryOptimization.parse(text[reactant_opt:end])
    else:
        reactant_optimization = None

    if product_opt is not None:
        end = min([l for l in locs if l > product_opt])
        product_optimization = GeometryOptimization.parse(text[product_opt:end])
    else:
        product_optimization = None

    if ts_opt is not None:
        end = min([l for l in locs if l > ts_opt])
        ts_optimization = GeometryOptimization.parse(text[ts_opt:end])
    else:
        ts_optimization = None
    
    return reactant_optimization, product_optimization, ts_optimization
