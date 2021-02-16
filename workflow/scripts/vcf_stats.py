import pandas as pd
import os
import numpy as np
#os.chdir('/home/pelmo/data_and_pipelines/boar_taint_variant_analysis/scripts')
from functions import read_vcf
from collections import Counter

vcf_file =  snakemake.input[0]
#vcf_file = '/home/pelmo//data_and_pipelines/boar_taint_variant_analysis/data/taint_vcf/taint_variants.vcf'

df = read_vcf(vcf_file)

df['var_id'] = df['#CHROM'] + "|" + df['POS'].astype(str)
df['var_id'] = df['var_id'].str.split('|').str[0] + "_" + df['var_id'].str.split('|').str[5]
df_clean = df.drop(columns = ['#CHROM', 'POS', 'ID', 'REF', 'ALT', 'QUAL', 'FILTER', 'INFO', 'FORMAT'])

df_clean =df_clean.set_index('var_id')
races = df_clean.columns.tolist()
for col in races:
    df[col] = df[col].apply(lambda x: x.split(':')[0] if x != './.:.' else "NONE")
    df_clean[col] = df_clean[col].apply(lambda x: x.split(':')[0] if x != './.:.' else "NONE")
pure_races = []
for race in races:
    if race  != "var_id":
        pure_races.append(race.split("|")[1])


races_unique = set(pure_races)

df_clean = df_clean.transpose()
var_dict = {}
for col in df_clean.columns:
    var_dict[col] = {}
    for race in races:
        if df_clean[col][race] not in var_dict[col]:
            var_dict[col][df_clean[col][race]] = []
        if df_clean[col][race] != "NONE":
            var_dict[col][df_clean[col][race]].append(race.split('|')[1])
        else:
            del var_dict[col][df_clean[col][race]]

var_df = pd.DataFrame.from_dict(var_dict)
var_df = var_df.transpose()

var_df = var_df[['1/1','0/1']]

df_freqs = df.merge(var_df, left_on='var_id', right_index=True)
complete_df = df_freqs




df_freqs_only = df_freqs[['var_id','#CHROM','POS','REF','ALT','1/1','0/1']]
df_freqs_only = df_freqs_only.fillna('NONE')

df_freqs_only['total_occurrences'] = 0

for col in ['1/1','0/1']:#,'2/2','3/3','5/5']:
    colname = col + "_counter"
    totcol = col + "_tot"
    counter_list = []
    totcol_list = []
    for row in df_freqs_only[col]:
        if row != "NONE":
            counter = dict(Counter(row).most_common())
            var_number = sum(counter.values())
        else:
            counter = "NONE"
            var_number = 0
        counter_list.append(counter)
        totcol_list.append(var_number)
    df_freqs_only[colname] = counter_list
    df_freqs_only[totcol] = totcol_list
    df_freqs_only['total_occurrences'] += df_freqs_only[totcol]

fillable_df = pd.DataFrame(0,index=np.arange(len(df_freqs_only)), columns = races_unique)


alleles_df_1_1 = (fillable_df + (df_freqs_only['1/1_counter'].apply(pd.Series)*2).drop(columns = [0]).fillna(0)).fillna(0)
alleles_df_0_1 = (fillable_df + (df_freqs_only['0/1_counter'].apply(pd.Series).drop(columns = [0]).fillna(0))).fillna(0)
alleles_df = alleles_df_1_1 + alleles_df_0_1

alleles_df

df_freqs_only = df_freqs_only.drop(columns = ['1/1', '0/1'])

final_df = df_freqs_only.merge(alleles_df, left_index=True, right_index=True)


final_df['total_alleles']= final_df['total_occurrences']*2
for race in alleles_df.columns.tolist():
    final_df[race] = final_df[race]/(final_df['total_alleles'])
for race in alleles_df.columns.tolist():
    final_df[race] = final_df[race].replace(0.0, 'NONE')
final_df
complete_df

final_df.to_csv(snakemake.output[0], index = False)
complete_df.to_csv(snakemake.output[1], index = False)
