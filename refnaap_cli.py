import sys
import os
import subprocess
import argparse

def main():
    
    local_path = os.path.dirname(os.path.realpath(__file__))
    #print(local_path)
    data_path = f"{local_path}"
    scaffold_helper = f"{local_path}/scaffold_cutter.R"
    gapfixer_helper = f"{local_path}/gapfixer.R"

    cli = argparse.ArgumentParser()
    cli.add_argument('-i', '--Input', help="Input file", required=True)
    cli.add_argument('-o', '--Output', help="Output", required=False, default="contigs.fasta")
    cli.add_argument('-r', '--RefFile', help="Reference File ", required=False, default=f'{local_path}/Americas2.fasta')
    cli.add_argument('--TopN', help="The top N reference sequences with the most depth are analyzed.", type=int, required=False, default=1)
    cli.add_argument('--MinCov', help="Amplicon regions need a minimum of this average coverage number", type=int, required=False, default=5)
    cli.add_argument('-t', '--threads', help="Number of threads. More is faster if your computer supports it", type=int, required=False, default=4)
    cli.add_argument('--model', help="Basecall Model", required=False, type=str, default='r10_min_high_g303')
    cli.add_argument('--verbose', help = "Keep Intermediate Files", required=False, default=False)
    args = cli.parse_args()


    OutputFolder = os.path.expanduser(os.path.dirname(args.Output))
    #print(OutputFolder)
    if not OutputFolder:
        print("no path specified")
        OutputFolder = "."

    os.makedirs(OutputFolder, exist_ok=True)

    minimap_cmd = subprocess.Popen(['minimap2', '-ax', 'map-ont', '-t', str(args.threads), local_path+'/Americas2.fasta', args.Input], stdout=subprocess.PIPE)
    subprocess.call(['samtools', 'sort', '-o', OutputFolder+'/cacheoutput.bam'], stdin=minimap_cmd.stdout)
    subprocess.call(['samtools', 'index', OutputFolder+'/cacheoutput.bam'])

    f = open(OutputFolder+"/sample.coverage", "w")
    subprocess.call(["samtools", "depth", OutputFolder+'/cacheoutput.bam'], stdout=f)
    f.close()

    subprocess.call(["Rscript", scaffold_helper, str(args.TopN), str(args.MinCov), str(args.RefFile), OutputFolder+"/sample.coverage", OutputFolder+"/scaffold.fasta", OutputFolder+"/cov.txt"])
    subprocess.call(["medaka_consensus", "-i", str(args.Input), "-d", OutputFolder+"/scaffold.fasta", "-o", OutputFolder+"/medaka1", "-m", str(args.model), "-t", str(args.threads)])

    subprocess.call(["Rscript", gapfixer_helper, OutputFolder+"/scaffold.fasta", OutputFolder+"/medaka1/consensus.fasta", OutputFolder+"/gapfixed.fasta"])



if __name__ == "__main__":
    sys.exit(main())
