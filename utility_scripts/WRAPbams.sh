#!/bin/bash
#SBATCH --account=xxxx
#SBATCH --time=02:00:00
#SBATCH --job-name=score_bams
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=4G

set -o errexit

module --quiet purge
module load VCFtools/XXX
module load SAMtools/XXX
module load Anaconda3/XX

export PS1=\$

source ${EBROOTANACONDA3}/etc/profile.d/conda.sh

conda deactivate &>/dev/null

conda activate <your conda environment>

VCF=$1
OUT=$2
BAM=$3
ABS=$4

/PATH/TO/BAMscorer score_bams $VCF $OUT $BAM --nofrq --abs $ABS