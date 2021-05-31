#!/bin/bash
#SBATCH --account=xxxx
#SBATCH --time=02:00:00
#SBATCH --job-name=select_snps
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=4G

set -o errexit

module --quiet purge
module load VCFtools/XXX
module load PLINK/XXX
module load EIGENSOFT/XXX
module load tabix/XXX
module load Anaconda3/XXX
module load BCFtools/XXX

export PS1=\$

source ${EBROOTANACONDA3}/etc/profile.d/conda.sh

conda deactivate &>/dev/null

conda activate <your conda environment>

VCF=$1
OUT=$2
BED= $3
CHROM_MAP=$3
MAF=$4
WEIGHT=$5

#If you have a VCF that is already cut to the inversion site you only need args 1 and 2
#Use the --include flag to point the script to a BED file with the inversion start and end points
#Use the --map flag to point to a chromosome map to recode non-integer chromosomes to integers for PLINK and Eigensoft

/PATH/TO/BAMscorer select_snps $1 $2 --include $3 --map $4 --maf $5 --weight $5