"""Helper functions to deal with files and folders"""

from typing import Tuple
from dataclasses import dataclass

import os
import shutil
import subprocess

@dataclass(frozen=True, init=True)
class OrcaCommandResult:
    status_code : int
    """Status code that ORCA returned"""

    status_message : str
    """Status message from ORCA"""

    output_file : str
    """Path to the ORCA output file"""

    runtime_dir : str
    """Path to the runtime directory, where all ORCA intermediate files are saved"""

    basename : str
    """Name of the calculation, without .inp extension"""

def run_orca(input_path) -> OrcaCommandResult:
    """
    Runs ORCA calculation with the specified input file.
    
    The input file is copied into `runtime/` directory, where will be also all intermediate results from ORCA.

    The final output file is saved in the same directory as input file, but with `.out` extension.
    """

    name, inpname, dir_path, runtime_path = _paths_from_inppath(input_path)

    inp_file = os.path.join(runtime_path, inpname)
    out_file = os.path.join(dir_path, name+'.out')
    shutil.copy(input_path, inp_file)
    status, message = _run_orca(inp_file, out_file)

    result = OrcaCommandResult(
        status_code=status,
        status_message=message,
        output_file=out_file,
        runtime_dir=runtime_path,
        basename=name
    )

    return result

def find_orca() -> str:
    """Returns the full path to ORCA executable"""
    orca_path = shutil.which('orca')
    return orca_path

def _paths_from_inppath(inppath: str, create_runtime=True) -> Tuple[str, str, str]:
    """
    Takes in path to .inp file, and returns all relevant paths:
    (base filename, input filename, base directory, runtime directory)

    If create_runtime is True, the runtime directory is created if it doesn't exist.
    """

    if not os.path.exists(inppath):
        raise Exception("Cannot find the input file")

    dir_path = os.path.dirname(inppath)
    runtime_path = os.path.join(dir_path, "runtime")
    inpname = os.path.basename(inppath)
    name = os.path.splitext(inpname)[0]

    if create_runtime and not os.path.exists(runtime_path):
        os.mkdir(runtime_path)
    
    return (name, inpname, dir_path, runtime_path)

def _run_orca(input, output) -> Tuple[int, str]:
    """Runs ORCA, returns status code and message"""

    orca_path = find_orca()
    command = f'"{orca_path}" "{input}" > "{output}"'
    status = subprocess.getstatusoutput(command)
    return status[0], status[1]

