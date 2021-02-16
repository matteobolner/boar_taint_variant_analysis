import pandas as pd
import os
#os.chdir('/home/pelmo/data_and_pipelines/boar_taint_variant_analysis/scripts')

from functions import read_vcf

vcf_file = read_vcf(snakemake.input[0])
#vcf_file = read_vcf('/home/pelmo/data_and_pipelines/boar_taint_variant_analysis/data/taint_vcf/taint_variants.vcf')
vcf_file['POS']= vcf_file['#CHROM'].str.split("|").str[5]
vcf_file['#CHROM'] = vcf_file['#CHROM'].str.split("|").str[2]
vcf_file.to_csv(snakemake.output[0], index = False, header=None, sep = "\t")
