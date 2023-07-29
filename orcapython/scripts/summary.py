"""Script for parsing and summarizing .out files"""

import argparse
from orcapython import OutputData
import os

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Script for quick parsing of .out files from ORCA")
    parser.add_argument("path", type=str, help="The .out ORCA file, or directory containing .out files")

    args = parser.parse_args()

    if not os.path.exists(args.path):
        print("Cannot find the output file/directory")
        exit(1)
    
    if os.path.isdir(args.path):
        for path in os.listdir(args.path):
            if path.endswith(".out"):
                print(f"{'   ' + path + '   ':#^50}\n")
                data = OutputData.parse_file(os.path.join(args.path,path))
                print(data.summary())
                print("#"*50)
                print("\n"*2)
    else:
        data = OutputData.parse_file(path)
        print(data.summary())
    
    exit(0)