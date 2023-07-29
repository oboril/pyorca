"""
This script facilitates running ORCA while keeping neat directory structure

What happens:
1. runtime/ folder is created if it doesn't exist
2. the input file is copied into the runtime/folder
3. the calculation is ran and output is placed into the original folder
"""

import argparse
from orcapython import OutputData
import os
import shutil
from datetime import datetime

from orcapython.filehandling import paths_from_inppath, run_orca
from orcapython import OutputData

from typing import Tuple

description = """\
This script facilitates running ORCA while keeping neat directory structure

Run as orca_run input_file_name.inp

What happens:
1. runtime/ folder is created if it doesn't exist
2. the input file is copied into the runtime/folder
3. the calculation is ran and output is placed into the original folder
"""

if __name__ == "__main__":
    starttime = datetime.now()

    # Parse input arguments
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("path", type=str, help="Path to the .inp file")
    parser.add_argument("--summary", nargs="?", default=False, const=True, help="Print summary of the calculation when it finishes")

    args = parser.parse_args()

    # Process the paths
    name, basedir, runtimedir = paths_from_inppath(args.path)
    outpath = os.path.join(basedir, name+".out")
    input_dest = os.path.join(runtimedir, name+".inp")

    # Copy input file into runtime
    shutil.copy(args.path, input_dest)

    # Run orca
    print("Starting ORCA calculation!")
    print("The start time is", starttime)
    success = run_orca(input_dest, outpath)
    if not success:
        print("ORCA calculation failed!")
        print("Elapsed", datetime.now() - starttime)
        exit(1)
    
    print("ORCA terminated normally")
    print("Elapsed", datetime.now() - starttime)

    # print summary if required
    if args.summary:
        data = OutputData.parse_file(outpath)
        print("\nSUMMARY:")
        print(data.summary())
    
    exit(0)