# BAMscorer

BAMscorer can be used to conduct genomic assignment tests from BAM files. 

The program takes a VCF as an input file, then runs PCA and heterozygosity calculations on the input data to generate heterozygosity calculations, eigenvalues, and SNP loading weights. The user must manually select the haplotype each reference individual belongs to based on output eigenvalues and heterozygosity using a program like Excel. These ID lists will then be input to the second script in the BAMscorer pipeline, which creates an allele database on input haplotypes, checks the same positions in input BAM files, and outputs a joint probability score that each individual belongs to one of three haplotypes: AA, BB, or AB. For genome-wide analysis AB haplotypes are not calculated.

Citation: Ferrari & Atmore et al., 2021. An accurate assignment test for extremely low-coverage whole-genome sequence data. *In prep*

For questions regarding program implementation, please contact Lane Atmore - lane@palaeome.org

Software requirements: \
PLINK \
VCFtools \
Python3 \
Eigensoft

## Downloading BAMscorer

BAMscorer can be downloaded from github. Please check the release page for the most up-to-date binaries. 
This includes: \
Linux binary \
MacOS 64-bit binary \
A compressed source code zip or tarball including: \
Test dataset \
README \
Utility scripts for visualization/data prep

**please note: BAMscorer requires glibc_2.17 or above

**N.B. early reports from linux binary use indicates there may be some glibcxx version incompatibilities between systems when running the select_snps module. I am working on a patch for this now but in the meantime have uploaded a python script that can be used in place of the select_snps module. If you are running the linux binary and are receiving a glibcxx not found error, please use select_snps.py. select_snps.py takes the same arguments as the select_snps module in the binary, which can be reviewed by using the -h function. An updated binary will be provided asap -- LMA 3.6.21 BINARY UPDATED AS OF 12:27 3.6.21, please make sure you have the latest version :)

## Running BAMscorer

There are two main modules within BAMscorer: select_snps and score_bams
The full pipeline for scoring BAMs is as follows: 
1. Run select_snps
2. Manual step (described below)
3. Run score_bams

We recommend running through this tutorial with the test data provided

A basic BAMscorer input line will look something like this: \
   **/PATH/TO/BAMscorer select_snps {args}**    or     **/PATH/TO/BAMscorer score_bams {args}**
   
If you are running on linux, you must also specify python before calling the binary, e.g., "python /PATH/TO/BAMscorer select_snps ..."
Please make sure you have all the following requirements in your python environment on linux:
pysam
pandas
numpy

Specific arguments are described below. Running BAMscorer select_snps -h or BAMscorer score_bams -h can also provide more information.


### select_snps

select_snps takes the following arguments:

Required: \
  **VCF   OUT** 
  
Optional: \
--include BED --map CHROMOSOME MAP --maf MAF --weight INT --top INT --bottom INT

To run select_snps on the test data use this command from the BAMscorer directory: \
BAMscorer select_snps test_data/LG01_testdata.vcf.gz test_data/LG01 --map test_data/chrom_map

Arguments 1 and 2 are required to run the program and merely point to the input VCF file and the output prefix. The VCF file should be bgzipped.

OPTIONAL ARGUMENTS: \
**--include** points to a BED file with specified regions to pass to VCFtools. Using --include means the script will only process sites within these regions. The BED should be tab-delimited and with headers(CHR\t START\t END). If the VCF file has not already been sliced to include only the inversion, this will allow the user to select just the inversion site for analysis. If your VCF has already been cut to the inversion site this argument can be ignored. Note: If the prefix of the .bed file is the same as the OUT prefix this file will be rewritten when the VCF is converted to PLINK format. It is also much faster to run the program on a VCF file that has already been split to just the inversion site, particularly if the genome in question is large.
 
**--map** refers to a chromosome map. If you are using a species that does not have integers for chromosome labels you need to assign integers to your chromosome/scaffold names so the data can be passed to PLINK and Eigensoft. This is a tab-delimited file with scaffold names in one column and integers in another. If your species already has integer chromosomes this argument can be ignored.

**--maf** specify a MAF filtering step for your data. Default is no MAF filtering.

**--weight** specify SNP loading weight cut-off for database creation. Default is top and bottom 5% of SNP loading loci. Argument should be an integer.

**--top/--bottom** specify pulling SNPs from the top or bottom tail of the SNP loading distribution. These arguments must be used together to specify the amount of distribution taken from each tail (0 is an accepted input value). These arguments should not be used with --weight, which pulls equally from both tails of the distribution.

select_snps first runs smartpca on SNPs in the inversion site, outputting {OUT}.pca.evec, {OUT}.pca.eval, and {OUT}.SNP.loadings files. It reads the {OUT}.SNP.loadings file back and selects the SNPs with the top and bottom 5% weights on PC1. It then uses only these sites to construct the database with the suffix {OUT}.divergent_snps.txt. Final database creation will occur in score_bams.

It then calculates heterozygosity at the inversion site using VCFtools and creates a table with values for PC1 and heterozygosity score for each individual. This table is outputted as {OUT}.pca_het.txt. 

Output files from select_snps: 

{OUT}.pca.evec (from smartPCA) \
{OUT}.pca.eval (from smartPCA) \
{OUT}.SNP.loadings (from smartPCA) \
{OUT}.divergent_snps.txt -- loci that will be used to call SNPs from BAM files \
{OUT}.pca_het.txt -- eigenvalues and heterozygosity scores for each individual from the database VCF to be used the manual step (below)


### Manual Step

The user should open the {OUT}.pca_het.txt file from select_snps in a program like Excel and sort the individuals by PC1. Inversion haplotypes (AA, BB, AB) should be manually assigned in a new column based on distribution of PC1 and heterozygosity values. Individuals homozygous for AA or BB should then be saved to new files with the following file names: {OUT}_AA_individuals.txt, {OUT}_BB_individuals.txt and placed in the same folder. All individuals in the VCF file should also be saved in the following file: {OUT}_db_individuals.txt with one individual per line.

Examples: LG01.pca_het.txt, LG01_AA_individuals.txt, and LG01_BB_individuals.txt files are included in the test_data directory

### Running score_bams

Files required before running score_bams:\
{OUT}_AA_individuals.txt \
{OUT}_BB_individuals.txt \
{OUT}_db_individuals.txt 

score_bams takes the following arguments:

Required:\
  **VCF   OUT   PATH/TO/BAMS**
  
Optional: \
--nofrq \
--wg \
--abs

To run score_bams on the test data provided use the following command from the BAMscorer directory: \
BAMscorer score_bams test_data/LG01_testdata.vcf.gz test_data/LG01 test_data/BAMs

The VCF input file and OUT prefix should be the same as for select_snps.
The **OUT** argument should be the same prefix as added to the {OUT}_AA_individuals.txt and {OUT}_BB_individuals.txt files. 
The **BAM** argument points to a folder containing the bam files. This folder should only contain BAM files required for the analysis and their indexes.

If "--nofrq" is specified, {OUT}_AA_SNPs.frq and {OUT}_BB_SNPs.frq must already be in the working directory. These files are allele frequencies output by VCFtools (normally in the first step of score_bams) and can take some time depending on the size of the VCF file. To streamline performance, if these files have been generated in a previous run there is no need to regenerate them.

If "--wg" is specified, BAMscorer will run with modifications for whole-genome analysis (see below). Instead of outputting AA, BB, and AB probabilities it will only output AA and BB probabilities.

"--abs" allows the user to specify an absolute allele frequency difference cut-off for SNPs to be included in the scoring database. If this is specified, the input should be a value between 0 and 1. For example, adding "--abs 0.3" will result in all SNPs that have an absolute allele frequency difference less than 0.3 between the major and minor alleles in each haplotype to be removed from the database used for scoring. The default value is 0. We have found that when scoring without the --wg option it is best to leave this at the default value as it can interfere with proper AB haplotype identification.
 
score_bams outputs the file **{OUT}_scores.txt**, which provides the user with a joint probability of belonging to haplotypes AA, BB, or AB. It will also report the number of loci found in the BAM that match loci in the divergent SNPs database.

Example: 

             AA    BB   AB  SNPs
      Ind1  1.0   0.0  0.0  597
      Ind2  0.0   1.0  0.0  1004
      Ind3  0.03  0.0  1.0  899

An example file LG01_scores.txt is included in the test_data directory.

score_bams first pipes through VCFtools to calculate allele frequencies for the sites that are most divergent in the type AA and type BB haplotypes using {OUT}.divergent_snps.txt. It then creates a database of the dominant and minor alleles (both ref and alt) for both haplotypes. Using these databases it iterates through the bam files in the BAM folder and creates individual databases of the alleles present at the segregating positions for both AA and BB haplotypes. It then compares the alleles present at these positions in each individual to the dominant alleles in the haplotype databases. 

Allelic state at each position is determined by the majority allele throughout all reads at the position in question. For alleles presented in equal numbers of reads, one allele is chosen at random. Each position is then scored against the divergent SNPs databases. The probability that the observed allele belongs to type AA, BB, or AB is determined by the allele frequencies of the alleles at that position in the divergent SNPs database. AB allele frequencies are calculated as the average frequencies between AA and BB at each position. Joint probabilities are then calculated for each position and the output denotes the probabilities that each individual belongs to haploytpes AA, BB, or AB.

It is sometimes the case that a BAM file will contain none of the positions desired for analysis. In this instance BAMscorer will output "Too few reads" and move on to the next file in the directory.

### If you want to use score_bams for whole-genome analysis...
If you've created your whole-genome SNP database using select_snps.py and proceeded to score_bams.py you can run the script as above. The OUT argument acts as the name for the output file and should match the prefix prefix as added to the {OUT}_AA_individuals.txt and {OUT}_BB_individuals.txt files. In the case of whole-genome analysis these may refer to different geographic locations or known phenotypes rather than "AA" or "BB" homozygote haplotypes. However, renaming these files will cause the script to fail, so please don't change the file names. 

score_bams.py can also be used as a stand-alone script if the user has a pre-existing panel of phenotypes and diagnostic SNPs. Simply create lists of individuals sorted by phenotype and use the diagnostic SNP list as the {OUT}.divergent_SNPs.txt file. Again, individuals lists for each phenotype must be coded as {OUT}_AA_individuals.txt or {OUT}_BB_individuals.txt and a full individual list will need to be saved as {OUT}_db_individuals.txt


## Also included in this repository: 
Utility_scripts: \
plot_SNPloadings.R - to visualize distribution of SNP loading weights for your data: Useful for determining best parameters for the SNP loading cut-off value \
Downsample_bootstrap_bam.sh - used for randomly downsampling BAM reads, used for bootstrapping through files to determine minimum reads required and/or filtering parameters.
WRAPbams.sh and WRAPsnps.sh - example scripts for running BAMscorer on a slurm cluster
