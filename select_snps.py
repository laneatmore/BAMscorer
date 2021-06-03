#!/usr/bin/env python

#Written by Lane M Atmore Feb 2021

import subprocess
import sys
import os
from os import path
import pandas as pd
import csv
import numpy as np
import argparse

#make sure pandas doesn't truncate our datasets
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)


parser = argparse.ArgumentParser()
parser.add_argument('VCF', type = str, help = 'Tell the caller which VCF you want to use')
parser.add_argument('OUT', type = str, help = 'Designate a prefix for all output files')
parser.add_argument('--include', type = str, help = 'Include designated regions from the BED file')
parser.add_argument('--map', type = str, help = 'Designate integers for non-integer chroms or scaffolds with a chromosome map (see VCFtools). Required for plink if you have non-integer chromosomes.')
parser.add_argument('--maf', type = str, help = 'Assign MAF filtering cut-off value')
parser.add_argument('--weight', type = str, nargs = '?', help = 'Assign SNP loading cut-off value', default = '5')
parser.add_argument('--top', type = str, help = 'Select only the top tail of the SNP loading distribution. Must be used with --bottom')
parser.add_argument('--bottom', type = str, help = 'Select only the bottom tail of the SNP loading distribution. Must be used with --top')
args, unknown = parser.parse_known_args()
pass_args = sys.argv[1:]
		
pass_args_str = ' '.join([str(elem) for elem in pass_args])
print("running BAMscorer with: " + pass_args_str, flush = True)

VCF = str(sys.argv[1])
OUT = str(sys.argv[2])
weight = int(args.weight)

if args.top:
	top_weight = int(args.top)
if args.bottom:
	bottom_weight = int(args.bottom)
		
if (len(sys.argv) < 2):
	sys.exit("Too few arguments specified", flush = True)
else:
	pass
			
		#First prep the files with plink and VCFtools
def tabix():
	if os.path.exists(VCF + '.tbi'):
		pass
	else:
		os.system('tabix -p vcf ' + VCF)
	
def cut_vcf():
	print('Prepping VCF')
	#If all arguments are specified
	if(args.include and args.map):
		#and if inclusion sites are required
		os.system('vcftools --gzvcf ' + VCF + ' \
			--bed ' + args.include + ' \
			--plink \
			--chrom-map ' + args.map + ' \
			--out ' + OUT)
				
		os.system('plink --file ' + OUT + ' \
			--keep-allele-order \
			--allow-extra-chr --set-missing-var-ids @:# \
			--make-bed \
			--double-id \
			--out ' + OUT)
		print('VCF converted to PLINK with ' + args.include + ', ' + args.map, flush = True)
	
	#If you don't need a chromosome map but need to cut the VCF
	elif(len(sys.argv) >= 5 and args.include):
	#If you have regions to include
		
		os.system('vcftools --gzvcf ' + VCF + ' \
			--bed ' + args.include + ' \
			--plink \
			--out ' + OUT)
			
		os.system('plink --file ' + OUT + ' \
			--keep-allele-order \
			--allow-extra-chr --set-missing-var-ids @:# \
			--make-bed \
			--double-id \
			--out ' + OUT)
		print('VCF converted to PLINK with ' + args.include, flush = True)
				
	#if VCF pre-split but still need chrom_map
	elif(len(sys.argv) >= 5 and args.map):
		
		os.system('vcftools --gzvcf ' + VCF + ' \
			--chrom-map ' + args.map + ' \
			--plink \
			--out ' + OUT)
		
		os.system('plink --file ' + OUT + ' \
			--keep-allele-order \
			--allow-extra-chr --set-missing-var-ids @:# \
			--make-bed \
			--double-id \
			--out ' + OUT)
		print('VCF converted to PLINK with ' + args.map, flush = True)
				
	#if VCF already split into inversion site and no need for chrom_map
	elif(len(sys.argv) >= 3 and not args.map and not args.include):
		os.system('plink --vcf ' + VCF + ' --keep-allele-order \
			--allow-extra-chr --set-missing-var-ids @:# \
			--make-bed \
			--double-id \
			--out ' + OUT)
		print('VCF converted to PLINK', flush = True)
	
	else:
		sys.exit("have you specified the right arguments?")
		
def cut_vcf_maf():
	print('Prepping VCF')
	#If all arguments are specified
	if(args.include and args.map):
		#and if inclusion sites are required
		os.system('vcftools --gzvcf ' + VCF + ' \
			--bed ' + args.include + ' \
			--plink \
			--chrom-map ' + args.map + ' \
			--out ' + OUT)
				
		os.system('plink --file ' + OUT + ' \
			--keep-allele-order \
			--allow-extra-chr --set-missing-var-ids @:# \
			--make-bed \
			--double-id \
			--maf ' + args.maf + ' \
			--out ' + OUT)
		print('VCF converted to PLINK with ' + args.include + ', ' + args.map, flush = True)
	
	#If you don't need a chromosome map but need to cut the VCF
	elif(len(sys.argv) >= 5 and args.include):
	#If you have regions to include
		
		os.system('vcftools --gzvcf ' + VCF + ' \
			--bed ' + args.include + ' \
			--plink \
			--out ' + OUT)
			
		os.system('plink --file ' + OUT + ' \
			--keep-allele-order \
			--allow-extra-chr --set-missing-var-ids @:# \
			--make-bed \
			--double-id \
			--maf ' + args.maf + ' \
			--out ' + OUT)
		print('VCF converted to PLINK with ' + args.include, flush = True)
				
	#if VCF pre-split but still need chrom_map
	elif(len(sys.argv) >= 5 and args.map):
		
		os.system('vcftools --gzvcf ' + VCF + ' \
			--chrom-map ' + args.map + ' \
			--plink \
			--out ' + OUT)
		
		os.system('plink --file ' + OUT + ' \
			--keep-allele-order \
			--allow-extra-chr --set-missing-var-ids @:# \
			--make-bed \
			--double-id \
			--maf ' + args.maf + ' \
			--out ' + OUT)
		print('VCF converted to PLINK with ' + args.map, flush = True)
				
	#if VCF already split into inversion site and no need for chrom_map
	elif(len(sys.argv) >= 3 and not args.map and not args.include):
		os.system('plink --vcf ' + VCF + ' --keep-allele-order \
			--allow-extra-chr --set-missing-var-ids @:# \
			--make-bed \
			--double-id \
			--maf ' + args.maf + ' \
			--out ' + OUT)
		print('VCF converted to PLINK')
	
	else:
		sys.exit("have you specified the right arguments?")
		#run VCFtools to calculate heterozygosity based on the most divergent SNPs
		
def fix_fam(OUT):
	fam = pd.read_csv(OUT + '.fam', sep = ' ', header = None)
	fam[5] = fam[5].replace([-9],1)
	fam.to_csv(OUT + '.fam', sep = ' ', header = None, index = None)

def check_files(OUT):
	filepath1=OUT + '.params.txt'

	if os.path.exists(filepath1):
		os.remove(filepath1)
	else:
		pass

def check_files2(OUT):
	filepath2=OUT + '.par'
	if os.path.exists(filepath2):
		os.remove(filepath2)	
	else:
		pass
		
#make new .params and .par files for eigensoft
#run convertf and smartpca
def convertf_run(OUT):
	with open(OUT + '.params.txt', 'w') as f:
		print('genotypename: ' + OUT + '.bed', file=f)
		print('snpname: ' + OUT + '.bim', file=f)
		print('indivname: ' + OUT + '.fam', file=f)
		print('outputformat: PACKEDANCESTRYMAP', file=f)
		print('genooutfilename: ' + OUT + '.geno', file=f)
		print('snpoutfilename: ' + OUT + '.snp', file=f)
		print('indoutfilename: ' + OUT + '.ind', file=f)

	convertf = subprocess.Popen('convertf -p ' + OUT + '.params.txt', shell = True)
	convertf.communicate()

def smartpca_run(OUT):
	with open(OUT + '.par', 'w') as f: 
		print('genotypename: ' + OUT + '.geno', file=f)
		print('snpname: ' + OUT + '.snp', file=f)
		print('indivname: ' + OUT + '.ind', file=f)
		print('evecoutname: ' + OUT + '.pca.evec', file=f)
		print('evaloutname: ' + OUT + '.pca.eval', file=f)
		print('altnormstyle: NO', file=f)
		print('lsqproject: YES', file=f)
		print('snpweightoutname: ' + OUT + '.SNP.loadings', file=f)
		print('numoutevec: 2', file=f)
		print('numoutlieriter: 0', file=f)
		print('numoutlierevec: 10', file=f)
		print('outliersigmathresh: 2', file=f)
		print('qtmode: 0', file=f)

	smartpca = subprocess.Popen('smartpca -p ' + OUT + '.par > ' + OUT + '.log', shell = True)
	smartpca.communicate()

#make a txt file with PC1 values for each individual to use for assigning
#haplotype groups

def update_evec(OUT):
	evec = open(OUT + '.pca.evec', 'r')
	updated_evec = open(OUT + '.pca.txt', 'w')

	for line in evec:
		if line.strip():
			cols = line.split()
			updated_evec.write(cols[0] + '\t' + cols[1] + '\t' + cols[2] + '\n')

	evec.close()
	updated_evec.close()
	
#Now we want to grab the loci that have the highest SNP loadings
#We will only take those loci that are in the top/bottom 5% of SNP loadings
def divergent_snps_symm(OUT, weight):
	snp_loadings = pd.read_csv(OUT + '.SNP.loadings', 
		delim_whitespace = True, 
		names = ['position', 'chr', 'pos', 'pc1', 'pc2'])
		
	top = snp_loadings[snp_loadings.pc1 > np.percentile(snp_loadings.pc1,(100-weight))]
	bottom = snp_loadings[snp_loadings.pc1 < np.percentile(snp_loadings.pc1,weight)]
	divergent_snps = pd.concat([top, bottom])
	divergent_snps['CHR'] = divergent_snps['position'].str.split(':').map(lambda x: x[0])
	divergent_snps[['CHR','pos']].to_csv(OUT + '.divergent_SNPs.txt', 
		sep = '\t', header = None, index = None)
	print('Divergent SNPs database created', flush = True)

def divergent_snps_custom(OUT, top_weight, bottom_weight):
	snp_loadings = pd.read_csv(OUT + '.SNP.loadings', 
		delim_whitespace = True, 
		names = ['position', 'chr', 'pos', 'pc1', 'pc2'])
		
	top = snp_loadings[snp_loadings.pc1 > np.percentile(snp_loadings.pc1,(100-top_weight))]
	bottom = snp_loadings[snp_loadings.pc1 < np.percentile(snp_loadings.pc1,bottom_weight)]
	divergent_snps = pd.concat([top, bottom])
	divergent_snps['CHR'] = divergent_snps['position'].str.split(':').map(lambda x: x[0])
	divergent_snps[['CHR','pos']].to_csv(OUT + '.divergent_SNPs.txt', 
		sep = '\t', header = None, index = None)
	print('Divergent SNPs database created', flush = True)

def het_calc(VCF, OUT):
	os.system('vcftools --gzvcf ' + VCF + ' \
		--positions ' + OUT + '.divergent_SNPs.txt --het \
		--out ' + OUT) 

#now update the evec.txt file to include the heterozygosity scores
def pca_het(OUT):
	pc1_txt = pd.read_csv(OUT + '.pca.txt', sep = '\t', names = ['Ind', 'PC1', 'PC2'])
	pc1_txt = pc1_txt.drop(pc1_txt.index[0])
	het = pd.read_csv(OUT + '.het', sep = '\t')
	pc1_txt['het'] = het['F'].values
	pc1_txt['ind'] = pc1_txt['Ind'].str.split(':').map(lambda x: x[1])
	pc1_txt = pc1_txt[['ind', 'PC1', 'het']]
	pc1_txt.to_csv(OUT + '.pca_het.txt', sep = '\t', index = None)
	print("Outputting pca/het values to " + OUT + '.pca_het.txt', flush = True)

def clean_up(OUT):
	print('Removing temporary files', flush = True)
	os.remove(OUT + '.par')
	os.remove(OUT + '.pca.txt')
	os.remove(OUT + '.ind')
	if os.path.exists(OUT + '.map'):
		os.remove(OUT + '.map')
	os.remove(OUT + '.bim')
	os.remove(OUT + '.bed')
	os.remove(OUT + '.fam')
	if os.path.exists(OUT + '.ped'):
		os.remove(OUT + '.ped')
	os.remove(OUT + '.het')
	os.remove(OUT + '.nosex')
	os.remove(OUT + '.params.txt')
	os.remove(OUT + '.snp')
	os.remove(OUT + '.geno')
	
def main():
	tabix()
	if not args.maf:
		cut_vcf()
	if args.maf:
		cut_vcf_maf()
	fix_fam(OUT)
	check_files(OUT)
	check_files2(OUT)
	convertf_run(OUT)
	smartpca_run(OUT)
	update_evec(OUT)
	if args.top and args.bottom:
		divergent_snps_custom(OUT, top_weight, bottom_weight)
	else:
		divergent_snps_symm(OUT, weight)
	het_calc(VCF, OUT)
	pca_het(OUT)
	clean_up(OUT)
	
if __name__ == '__main__':
	main()

	
##########################################
#MANUAL STEP: select homozygous individuals
##########################################
	
# Sort individuals according to PC 1 (e.g. in Excel) and use PC1 and F 
# values to select type AA and type BB individuals 

# Copy individuals into two separate lists -- 
# {INVERSION}_AA_individuals.txt
# {INVERSION}_BB_individuals.txt
