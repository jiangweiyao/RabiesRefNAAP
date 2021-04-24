#!/usr/bin/env python

import sys
import os
import glob
import re
from datetime import date
import argparse
import subprocess
from pathlib import Path


def main():
    
    local_path = os.path.dirname(os.path.realpath(__file__))
    #print(local_path)
    data_path = f"{local_path}"
    scaffold_helper = f"{local_path}/scaffold_cutter.R"
    gapfixer_helper = f"{local_path}/gapfixer.R"
    now = date.today()
    home = str(Path.home())

    cli = argparse.ArgumentParser()
    cli.add_argument('-i', '--InputFolder', help="Folder containing barcoded fastq", required=True)
    cli.add_argument('-o', '--OutputFolder', help=f"Output Folder. Default is {home}/rabiesrefnaap_results/output_{now}", required=False, default=f"{home}/rabiesrefnaap_results/output_{now}")

    cli.add_argument('--TopN', help="The top N reference sequences with the most depth are analyzed. Default is 1.", type=int, required=False, default=1)
    cli.add_argument('--MinCov', help="Amplicon regions need a minimum of this average coverage number. Default is 5.", type=int, required=False, default=5)
    cli.add_argument('--threads', help="Number of threads. More is faster if your computer supports it. Default is 4.", type=int, required=False, default=4)
    cli.add_argument('--verbose', help = "Keep Intermediate Files. Default is false.", required=False, default=4)
    cli.add_argument('--model', help="Basecall Model", required=False, type=str, default='r10_min_high_g303')
    args = cli.parse_args()


    #Run fastqc and multiqc on all the fastq/fastq.gz files in the folder
    subprocess.check_output(['python', local_path+'/fastqc_multiqc.py', '-i', args.InputFolder, '-o', args.OutputFolder+'/multiqc'])
    subprocess.check_output(['cp', args.OutputFolder+'/multiqc/multiqc_report.html', args.OutputFolder+'/multiqc_report.html'])

    #Interate over all the fastq/fastq.gz files
    files = sorted([f for f in glob.glob(args.InputFolder+"/**", recursive = True) if re.search(r'(.*)\.((fastq|fq)(|\.gz))$', f)])   
    print(files)
    OutputFolder = os.path.expanduser(args.OutputFolder)

    for i in range(0, len(files)):
        filec = files[i]

        base = os.path.splitext(os.path.basename(filec))[0]
        base = os.path.splitext(base)[0]
        print(base)

        filec2 = args.OutputFolder+'/'+"filtered/"+base+"_filtered.fastq"
        #Trim and filter the reads
        subprocess.check_output(['python', local_path+'/seqtk_sizefilter_trim.py', '-i', filec, '-o', filec2])


        #Get coverage
        subprocess.check_output(['python', local_path+'/rabiescoverage.py', '-i', filec2, '-o', args.OutputFolder+'/coverage/'+base+"_coverage/"+base+"_coverage.txt", '-t', str(args.threads)])
        subprocess.check_output(['cp', args.OutputFolder+'/coverage/'+base+"_coverage/"+base+"_coverage.txt", args.OutputFolder+'/'+base+"_coverage.txt"])

        #Get assembly
        subprocess.check_output(['python', local_path+'/refnaap_cli.py', '-i', filec2, '-o', args.OutputFolder+'/assembly/'+base+"_assembly/", '-t', str(args.threads), '--TopN', str(args.TopN), '--MinCov', str(args.MinCov)])
        subprocess.check_output(['cp', args.OutputFolder+'/assembly/'+base+"_assembly/final_scaffold.fasta", args.OutputFolder+"/"+base+"_final_scaffold.fasta"])



        print("progress: {}/{}".format(i+1, len(files)))

    

    if not args.verbose:
        subprocess.check_output(['rm', '-rf', args.OutputFolder+'/coverage'])
        subprocess.check_output(['rm', '-rf', args.OutputFolder+'/assembly'])
        subprocess.check_output(['rm', '-rf', args.OutputFolder+'/filtered'])
        subprocess.check_output(['rm', '-rf', args.OutputFolder+'/multiqc'])

if __name__ == "__main__":
    sys.exit(main())
