import pandas as pd
import os
from functions import read_vcf

vcf_file = read_vcf(snakemake.input[0])
vcf_file['#CHROM'] = vcf_file['#CHROM'].str.split("|").str[2]
vcf_file.to_csv(snakemake.output[0], index = False, header=None, sep = "\t")
