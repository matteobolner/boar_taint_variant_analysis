import pandas as pd
import os
#import matplotlib.pyplot as plt
#import seaborn as sns
#from matplotlib import rcParams

#os.chdir('/home/pelmo/boar_taint_variant_analysis/scripts')

from functions import vep,read_vcf

vep_input_file = snakemake.input[0]
vcf_stats_df = pd.read_csv(snakemake.input[1])

with open(vep_input_file, 'r') as f:
    vep_input = f.readlines()
vep_df = vep(vep_input)

vcf_stats_df[['most_severe_consequence', 'intergenic_consequences', 'colocated_variants', 'transcript_consequences']] = vep_df[[ 'most_severe_consequence', 'intergenic_consequences', 'colocated_variants', 'transcript_consequences']]
#vcf_stats_df[vcf_stats_df['most_severe_consequence'] == 'missense_variant']['transcript_consequences']

data = vcf_stats_df.groupby(by='#CHROM')

'''sns.set_theme(style="whitegrid")
sns.set(rc={'figure.figsize':(11.7,8.27)})
sns.displot(x='most_severe_consequence', data=vep_df, hue='gene_name', palette='muted')


vep_df['transcript_consequences'].tolist()




import seaborn as sns
df = sns.load_dataset("penguins")
sns.pairplot(vep_df, hue="seq_region_name")
'''


vcf_stats_df.to_csv(snakemake.output[0], index = False)
