from __future__ import annotations
from dataclasses import dataclass
from typing import List

@dataclass(frozen=True, init=True)
class NebSettings:
    """Contains information about NEB settings"""

    n_images: int
    """Number of images"""

    n_opt_images: int
    """Number of optimized images"""

    optimize_endpoints: bool
    """Optimize end points before NEB calculation"""

    def parse(text: str) -> NebSettings:
        """Finds and parses NEB settings summary"""

        settings = _parse_settings(text)
        if settings is None:
            return None
        
        n_images, n_opt_images, optimize_endpoints = settings
    
        return NebSettings(n_images, n_opt_images, optimize_endpoints)



### HELPER FUNCTIONS

import re

def _parse_settings(text: str) -> None | Tuple[int, int, bool]:
    extract = re.search(
        r"Nudged Elastic Band Calculation(?:.|\s)*?Constrained atoms.*\n",
        text
    )

    if extract is None:
        return None
    
    extract = extract.group(0)

    n_images = re.search(
        r"Number of images.+?(\d+)",
        text
    )
    n_images = int(n_images.group(1))

    n_opt_images = re.search(
        r"Number of optimized images.+?(\d+)",
        text
    )
    n_opt_images = int(n_opt_images.group(1))

    optimize_endpoints = re.search(
        r"Optimization of end points before NEB\s+\.+\s+(YES|NO)",
        text
    )

    optimize_endpoints = optimize_endpoints.group(1) == "YES"

    return n_images, n_opt_images, optimize_endpoints

