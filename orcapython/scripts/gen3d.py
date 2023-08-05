"""Uses OpenBabel conformer search to generate .xyz file from SMILES"""

description = """\
This script uses OpenBabel to generate 3D conformer from SMILES

Example use:
orca_gen3d input_file.smi
orca_gen3d input_file.smi output_file.xyz
orca_gen3d CC(O)OCC ethylacetate.xyz
"""

import argparse
import os

from orcapython.xyz import smiles_to_xyz, smiles_file_to_xyz

description = """\
This script aligns molecules in .xyz files and prints the RMSD.

Usage: orca_align reference.xyz sample1.xyz sample2.xyz [more samples ...]
"""

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("input", type=str, help="Either path to .smi input file or SMILES directly")
    parser.add_argument("output", type=str, nargs="?", help="Path where the .xyz output file should be saved")

    args = parser.parse_args()

    # Try to generate output name if not specified
    if args.output is None:
        if args.input.endswith(".smi"):
            args.output = args.input[:-4] + ".xyz"
        else:
            print("The output file has to be specified with SMILES input!")
            exit(1)

    if args.input.endswith(".smi"):
        # The input is a SMILES file
        if not os.path.exists(args.input):
            print("Could not find the input file!")
            exit(1)
        
        smiles_file_to_xyz(args.input, args.output)
    else:
        # The input are SMILES directly
        smiles_to_xyz(args.input, args.output)
    
    print("SMILES converted to .xyz!")
    
    exit(0)