import pandas as pd
import os
#import matplotlib.pyplot as plt
#import seaborn as sns
#from matplotlib import rcParams
import json
import numpy as np
'''
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

'''

#os.chdir('/home/pelmo/data_and_pipelines/boar_taint_variant_analysis/scripts')

#from functions import vep,read_vcf
vep_df = pd.read_csv(snakemake.input[0], sep = "\t", comment = '%')
#vep_df = pd.read_csv('/home/pelmo/data_and_pipelines/boar_taint_variant_analysis/data/vep/vep_output_comment_fixed.tsv', sep = "\t", comment = '%')

vcf_stats_df = pd.read_csv(snakemake.input[1])

#vcf_stats_df = pd.read_csv('/home/pelmo/data_and_pipelines/boar_taint_variant_analysis/data/stats/taint_variants_stats.csv')
vcf_stats_df['ensembl_ids'] = vcf_stats_df['#CHROM'].str.split('|').str[1]

ensembl_ids = vcf_stats_df['#CHROM'].str.split('|').str[1].unique().tolist()
vep_df = vep_df[vep_df['Gene'].isin(ensembl_ids)]
vcf_stats_df['position']= vcf_stats_df['var_id'].str.split('_').str[1]
vep_df['position'] = vep_df['Location'].str.split(':').str[1].str.split('-').str[0]

merged_df = vcf_stats_df.merge(vep_df, left_on='position', right_on='position')

columns = ['IMPACT', 'STRAND', 'SYMBOL', 'SYMBOL_SOURCE', 'HGNC_ID', 'BIOTYPE', 'APPRIS', 'ENSP', 'SWISSPROT', 'TREMBL', 'UNIPARC', 'SIFT', 'DISTANCE']
extra_df = pd.DataFrame(index=np.arange(len(merged_df)),columns=columns)

merged_df['Extra'].str.split(';').tolist()
counter = -1
for row in merged_df['Extra'].str.split(';').tolist():
    counter +=1
    for name in row:
        extra_df[name.split('=')[0]][counter] = name.split('=')[1]
final_df = merged_df.merge(extra_df, left_index=True, right_index=True)
final_df = final_df.drop(columns = ['Extra'])
#with open(vep_input_file, 'r') as f:
#    vep_input = f.readlines()
#vep_df = vep(vep_input)
#vep_df
#vcf_stats_df[['most_severe_consequence', 'intergenic_consequences', 'colocated_variants', 'transcript_consequences']] = vep_df[[ 'most_severe_consequence', 'intergenic_consequences', 'colocated_variants', 'transcript_consequences']]

final_df.to_csv(snakemake.output[0], index = False)
