#!/usr/bin/env python

import os
import sys
import subprocess
import argparse 


def main():

    cli = argparse.ArgumentParser()
    cli.add_argument('-i', '--Input', help="Input fastq file", required=True)
    cli.add_argument('-o', '--Output', help="Output file name", required=False, default="SizeFilteredAndTrimmed.fastq")
    cli.add_argument('-s', '--Size', help="Filter out reads shorter than size", required=False, default=50)
    cli.add_argument('-l', '--Left', help = "Trim this many bases from the left size", required=False, default=25)
    cli.add_argument('-r', '--Right', help = "Trim this many bases from the right size", required=False, default=25)
    args = cli.parse_args()
    #subprocess.run(["wc", args.Input])

    OutputFolder = os.path.expanduser(os.path.dirname(args.Output))
    #print(OutputFolder)
    if not OutputFolder:
        print("no path specified")
        OutputFolder = "."

    os.makedirs(OutputFolder, exist_ok=True)

    f = open(OutputFolder+"/filteredintaaaaaa.fq", "w")
    subprocess.call(["seqtk", "seq", "-L", str(args.Size), args.Input], stdout=f)
    f.close()

    f = open(args.Output, "w")
    subprocess.call(["seqtk", "trimfq", "-b", str(args.Left), "-e", str(args.Right), OutputFolder+"/filteredintaaaaaa.fq"], stdout=f)
    f.close()

    os.remove(OutputFolder+"/filteredintaaaaaa.fq")
 
if __name__ == "__main__":
    sys.exit(main())
