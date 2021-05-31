#!/bin/bash

# Job name:
#SBATCH --job-name=Create_subset
#
# Project:
#SBATCH --account=nn9244k
#
# Wall clock limit:
#SBATCH --time=24:00:00
#
# Processor and memory usage:
#SBATCH --mem-per-cpu=15G
#
#SBATCH--ntasks-per-node=1

##Resampling script by Bastiaan Star. Date in the far ancient past. 

##Script to randomly downsample and resample bamfiles 

##USAGE: sbatch <scriptname> <bamfilename> 

module purge
module load SAMtools/1.9-foss-2018b


#Create temp directory for read selection
mkdir -p temp_$1

#Parse the header of the BAM file for later use
samtools view -H $1 > temp_$1/header_$1

#Get list of readnames from the BAM file
samtools view $1 |awk '{print $1}' > temp_$1/list_read_names_$1

#Get total number of reads BAM file
read_n=$(wc -l temp_$1/list_read_names_$1 |cut -d " " -f 1)

echo "Total read number is $read_n"

##CHECK if BAM file allows resampling. Note if you have only a few reads more than the resampling number,
##you are not really resampling anymore....
if [ 100000 -gt $read_n ]; then echo "WARNING, SOURCE BAM has too few reads to resample 100000" ; else echo "BAM file contains a sufficient number of reads for downsampling" ; fi

#Create directory for the downsampled BAM file
mkdir -p downsampled_$1

#Subsample in this set, Change to what you need
for y in 00500 01000 01500 02000 02500 03000 03500 04000 04500 05000 05500 06000 06500 07000 07500 08000 08500 09000 09500 10000 20000 30000 40000 50000 60000 70000 80000 90000 99999;
do
echo "Resample $y random reads..."

#Possible iterative subsampling: you may want to resample for bootstrapping purposes. We use shuf for randomisation here.

for x in {01..20};
do
echo "downsample .. $y and iteration .. $x"
shuf -n $y temp_$1/list_read_names_$1 -o temp_$1/shuf_$x
samtools view $1 | fgrep -w -f temp_$1/shuf_$x > temp_$1/$1_$x.sam 2> /dev/null
cat temp_$1/header_$1 temp_$1/$1_$x.sam > temp_$1/temp.$1_$x.sam 2> /dev/null
samtools view -Shub temp_$1/temp.$1_$x.sam > temp_$1/$1_$x.bam 2> /dev/null

samtools sort temp_$1/$1_$x.bam -o downsampled_$1/$1_${y}_${x}.bam 2> /dev/null
samtools index downsampled_$1/$1_${y}_${x}.bam 2> /dev/null


done

done

rm -r temp_$1