import pandas as pd
import os
#import matplotlib.pyplot as plt
#import seaborn as sns
#from matplotlib import rcParams
import json
import ast

'''
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

'''

#os.chdir('/home/pelmo/data_and_pipelines/boar_taint_variant_analysis/scripts')

from functions import vep,read_vcf

vep_input_file = snakemake.input[0]
vcf_stats_df = pd.read_csv(snakemake.input[1])

#vep_input_file = '/home/pelmo/data_and_pipelines/boar_taint_variant_analysis/data/vep/vep_input.tsv'
#vcf_stats_df = pd.read_csv('/home/pelmo/data_and_pipelines/boar_taint_variant_analysis/data/stats/taint_variants_stats.csv')
vcf_stats_df
with open(vep_input_file, 'r') as f:
    vep_input = f.readlines()
vep_df = vep(vep_input)
vep_df
vcf_stats_df[['most_severe_consequence', 'intergenic_consequences', 'colocated_variants', 'transcript_consequences']] = vep_df[[ 'most_severe_consequence', 'intergenic_consequences', 'colocated_variants', 'transcript_consequences']]
#vcf_stats_df[vcf_stats_df['most_severe_consequence'] == 'missense_variant']['transcript_consequences']
#vcf_stats_df
#data = vcf_stats_df.groupby(by='#CHROM')

#ast.literal_eval(vcf_stats_df['1/1_counter'][1])

#groups = dict(list(data))



#vcf_stats_df[vcf_stats_df['most_severe_consequence'] == 'missense_variant']

#sns.set_theme(style="whitegrid")
#sns.set(rc={'figure.figsize':(11.7,8.27)})
#sns.displot(x='0/1_tot', data=CYP11A1_vep, palette='muted')


#vep_df['transcript_consequences'].tolist()



#import seaborn as sns
#df = sns.load_dataset("penguins")
#sns.pairplot(vep_df, hue="seq_region_name")




#a = pd.read_csv('/home/pelmo/tesi/boar_taint_variant_analysis/data/stats/vcf_as_csv.csv')

#a.columns.tolist()

#meishan_cols = ['#CHROM','MS20U10|meishan', 'MS20U11|meishan', 'MS21M07|meishan', 'MS21M14|meishan']

#a[meishan_cols]


vcf_stats_df.to_csv(snakemake.output[0], index = False)
