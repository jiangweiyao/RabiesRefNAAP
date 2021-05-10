#!/usr/bin/env python

import sys
import os
import glob
import re
from datetime import date
from gooey import Gooey, GooeyParser
import subprocess
from pathlib import Path

@Gooey(program_name='Fastq Merger', 
        default_size=(720, 900))

def main():
    
    local_path = os.path.dirname(os.path.realpath(__file__))
    #print(local_path)
    data_path = f"{local_path}"
    scaffold_helper = f"{local_path}/scaffold_cutter.R"
    gapfixer_helper = f"{local_path}/gapfixer.R"
    now = date.today()
    home = str(Path.home())

    cli = GooeyParser(description="Fastq File Merger")
    required_args = cli.add_argument_group("Input Output Location", gooey_options={'columns': 1, 'show_border': True})
    required_args.add_argument('--InputFolder', help="Folder containing subfolders of fastq files", required=True, widget='DirChooser')
    required_args.add_argument('--OutputFolder', help="Output Folder", required=False, default=f"{home}/rabiesrefnaap_results/fastq_{now}", widget='DirChooser')

    args = cli.parse_args()

    OutputFolder = os.path.expanduser(args.OutputFolder)
    os.makedirs(OutputFolder, exist_ok=True)

    folders = next(os.walk(args.InputFolder))[1]
    print(folders)
    for i in folders:
        read_files = glob.glob(args.InputFolder+"/"+i+"/*.fastq")
        print(read_files)
        with open(f"{args.OutputFolder}/{i}.fastq", "wb") as outfile:
            for f in read_files:
                with open(f, "rb") as infile:
                    for line in infile:
                        outfile.write(line)

if __name__ == "__main__":
    sys.exit(main())
