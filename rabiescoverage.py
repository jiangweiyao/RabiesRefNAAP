import subprocess
import sys 
import os 
import argparse

def main():

    local_path = os.path.dirname(os.path.realpath(__file__))

    cli = argparse.ArgumentParser()
    cli.add_argument('-i', '--Input', help="Input file", required=True)
    cli.add_argument('-o', '--Output', help="Output file", required=False, default="coverage.txt")
    cli.add_argument('-t', '--threads', help="Number of threads", type=int, required=False, default=1)
    args = cli.parse_args()


    minimap_cmd = subprocess.Popen(['minimap2', '-ax', 'map-ont', '-t', str(args.threads), local_path+'/Americas2.fasta', args.Input], stdout=subprocess.PIPE)
    subprocess.call(['samtools', 'sort', '-o', 'output.bam'], stdin=minimap_cmd.stdout)

    subprocess.call(['samtools', 'index', 'output.bam'])

    samtools_reads_cmd = subprocess.Popen(['samtools', 'view', '-c', 'output.bam'], stdout=subprocess.PIPE)
    reads = (str(samtools_reads_cmd.communicate()[0].rstrip(), 'utf-8'))
    print(reads)

    samtools_mapped_cmd = subprocess.Popen(['samtools', 'view', '-c', '-F 260', 'output.bam'], stdout=subprocess.PIPE)
    mapped = (str(samtools_mapped_cmd.communicate()[0].rstrip(), 'utf-8')) 
    print(mapped)

    Ndepth_cmd = subprocess.Popen(['samtools', 'depth', '-b', local_path+'/AmericasN.bed', 'output.bam'], stdout=subprocess.PIPE)
    Ncov_cmd = subprocess.Popen(['awk', '{ total += $3; count++ } END { print total/1350 }'], stdin=Ndepth_cmd.stdout, stdout=subprocess.PIPE)
    ncov = (str(Ncov_cmd.communicate()[0].rstrip(), 'utf-8'))
    print(ncov)

    Gdepth_cmd = subprocess.Popen(['samtools', 'depth', '-b', local_path+'/AmericasG.bed', 'output.bam'], stdout=subprocess.PIPE)
    Gcov_cmd = subprocess.Popen(['awk', '{ total += $3; count++ } END { print total/1575 }'], stdin=Gdepth_cmd.stdout, stdout=subprocess.PIPE)
    gcov = (str(Gcov_cmd.communicate()[0].rstrip(), 'utf-8'))
    print(gcov)

    Avelenght1_cmd = subprocess.Popen(['samtools', 'view', '-F 260', 'output.bam'], stdout=subprocess.PIPE)
    Avelenght2_cmd = subprocess.Popen(['awk', '{ sum_length += length($10) } END { print sum_length/NR }'], stdin=Avelenght1_cmd.stdout, stdout=subprocess.PIPE)
    avelength = (str(Avelenght2_cmd.communicate()[0].rstrip(), 'utf-8'))
    print(avelength)



#        # Get average length of mapped reads
#        samtools_mappeds_cmd = f"samtools view -F 260 -b {metric_dir}/{base}.sorted.bam > {metric_dir}/{base}.mapped.bam"
#        samtools_avelen_cmd = f"samtools view {metric_dir}/{base}.mapped.bam " + '| awk \'{ sum_length += length($10) } END { print sum_length/NR }\''
#        os.system(samtools_mappeds_cmd)
#        readlength = os.popen(samtools_avelen_cmd).read()




if __name__ == "__main__":
    sys.exit(main())

