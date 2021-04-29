# Rabies Reference Based Nanopore Amplicon Analysis Pipeline (RabiesRefNAAP)

This pipeline processes the raw, basecalled Nanopore reads generated from the Rabies Nanopore Sequencing protocol developed in the CDC. It does the following steps:
1. It QCs the fastq files using fastqc and multiqc to generate a quality report.
2. It trims the left and right ends of the reads by 25 basepairs, and filters out reads shorter than 50bp.
3. It finds the coverage of the reads over the G and N regions of the Rabies reference files.
4. It generates the sequence of Rabies coveraged by the reads using reference based assembly, gap fixing, and Medaka

This workflow depends on Bioconda to install the environmental dependencies.
And then run the attached script using the environment.

## Summary - Installation 
1. Clone Repository 
2. Install Conda if not already in environment
3. Create conda environment

## Summary - How to run after installation.
1. Activate conda environment - `conda activate rabiesrefnaap`
2. Run the GUI - `~/RabiesRefNAAP/RabiesRefNAAP.py`
3. Sample fastq data is in test folder
4. Shut down your environment to protect it from modifications - `conda deactivate`


## Clone this code using GIT

### Install git for Debian systems using the following command (if necessary)
```
sudo apt update
sudo apt install git
```

##Installation directions 
These instructions install the code into your home path. Modify the instructions if you want to install elsewhere as appropriate. 

### Clone the code from repository
```
cd ~
git clone https://github.com/jiangweiyao/RabiesRefNAAP.git
```

### Install Miniconda (if no Conda is install on system). 
You can run the prepackaged script install_miniconda.sh to install into your home directory (recommended) by using the following command
```
. ~/RabiesRefNAAP/install_miniconda.sh
```

Detailed instruction on the the Miniconda website if anything goes wrong:
https://conda.io/projects/conda/en/latest/user-guide/install/linux.html

### Clone the environment. Need to do once.

We use conda to create an environment (that we can activate and deactivate) to install our dependent software and resolve their dependencies. This environment is called "rabiesrefnaap". 

```
conda env create -f ~/RabiesRefNAAP/environment.yml
```

Conda will automatically figure out and install all dependencies for you. It might take some time for Conda to resolve the dependencies and install everything for you. 

## Run the code.

Activating your environment makes the software you installed in that environment available for use. You will see "(RefNAAP)" in front bash after activation.
```
conda activate rabiesrefnaap
```

There are two versions of code. The GUI version and the CLI version.

Run the GUI version (change path if it is installed else where.)
```
~/RabiesRefNAAP/RabiesRefNAAP.py
```

Run the CLI version using the included test files (change path if it is installed else where.)
```
~/RabiesRefNAAP/RabiesRefNAAP_CLI.py -i ~/RabiesRefNAAP/fastq/
```


When you are finished running the workflow, exit out of your environment by running `conda deactivate`. Deactivating your environment exits out of your current environment and protects it from being modified by other programs. You can build as many environments as you want and enter and exit out of them. Each environment is separate from each other to prevent version or dependency clashes. The author recommands using Conda/Bioconda to manage your dependencies.

## Author
- Jiangwei Yao
- Crystal Gigante

## License 
Apache License 2.0
