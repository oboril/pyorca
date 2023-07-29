import argparse
import os

from orcapython.xyz import align_xyz_files

description = """\
This script aligns molecules in .xyz files and prints the RMSD.

Usage: orca_align reference.xyz sample1.xyz sample2.xyz [more samples ...]
"""

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("reference", type=str, help="The reference .xyz file")
    parser.add_argument("samples", type=str, nargs="+", help="The sample .xyz files to be compared to reference")

    args = parser.parse_args()
    
    for sample in args.samples:
        rmsd = align_xyz_files(args.reference, sample)
        print(f"{sample: <20} RMSD = {rmsd:0.4f}")
    
    exit(0)