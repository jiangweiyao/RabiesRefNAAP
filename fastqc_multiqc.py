import sys
import glob
import os
import subprocess
import argparse
import re

def main():
    
    local_path = os.path.dirname(os.path.realpath(__file__))

    cli = argparse.ArgumentParser()
    cli.add_argument('-i', '--InputFolder', help="Input folder file", required=True)
    cli.add_argument('-o', '--OutputFolder', help="Output folder", required=False, default=".")
    args = cli.parse_args()
    #subprocess.run(["wc", args.Input])

    files = sorted([f for f in glob.glob(args.InputFolder+"/**", recursive = True) if re.search(r'(.*)\.((fastq|fq)(|\.gz))$', f)])   
    #InputFolder = os.path.expanduser(args.InputFolder)
    #files = sorted(glob.glob(InputFolder+"/*.fastq"))
    print(files)

    OutputFolder = os.path.expanduser(args.OutputFolder)
    os.makedirs(OutputFolder, exist_ok=True)


    for i in range(0, len(files)):
        filec = files[i]

        base = os.path.splitext(os.path.basename(filec))[0]
        base = os.path.splitext(base)[0]
        #print(base)
        #subprocess.call(["seqtk", "seq", "-L", str(args.Size), args.Input], stdout=f)
        subprocess.call(["fastqc", filec, "-o", OutputFolder])


    subprocess.call(["multiqc", OutputFolder, "-o", OutputFolder])

if __name__ == "__main__":
    sys.exit(main())
