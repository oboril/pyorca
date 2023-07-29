"""Helper functions to deal with files and folders"""

import os
import shutil
import subprocess

from typing import Tuple

def find_orca() -> str:
    """Returns the full path to ORCA executable"""
    orca_path = shutil.which('orca')
    return orca_path

def paths_from_inppath(inppath: str, create_runtime=True) -> Tuple[str, str, str]:
    """
    Takes in path to .inp file, and returns all relevant paths:
    (base filename, base directory, runtime directory)

    if create_runtime is True, the runtime directory is created if it doesn't exist
    """

    if not os.path.exists(inppath):
        raise Exception("Cannot find the input file")

    dir_path = os.path.dirname(inppath)
    runtime_path = os.path.join(dir_path, "runtime")
    inpname = os.path.basename(inppath)
    name = os.path.splitext(inpname)[0]

    if create_runtime and not os.path.exists(runtime_path):
        os.mkdir(runtime_path)
    
    return (name, dir_path, runtime_path)

def run_orca(input, output) -> bool:
    """Runs ORCA, returns whether orca terminated with status code 0"""
    orca_path = find_orca()
    command = f'"{orca_path}" "{input}" > "{output}"'
    status = subprocess.getstatusoutput(command)
    if status[0] != 0:
        print(f"Error {status[0]} while running ORCA!")
        print(status[1])
        return False
    return True