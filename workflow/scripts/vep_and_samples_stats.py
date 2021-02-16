import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import sys
import os
import json
import numpy as np
df = pd.read_csv(snakemake.input[0])

def plot_coding(df):
    #df = pd.read_csv('/home/pelmo/data_and_pipelines/boar_taint_variant_analysis/test_final_df_vep.csv')
    consequences = df['Consequence'].value_counts(normalize =True).reset_index().rename(columns={'index': 'Consequence', 'Consequence': 'Percentage'})
    others = consequences[consequences['Percentage']<0.005]['Percentage'].sum()
    consequences = consequences[consequences['Percentage']>=0.005]
    consequences=consequences.append({'Consequence': 'Others','Percentage':others}, ignore_index=True)
    sns.set(rc={'figure.figsize':(15,10)})

    conseq_plot = sns.barplot(x=consequences['Consequence'],y=consequences['Percentage'],palette='muted')
    ax=conseq_plot
    for p in ax.patches:
                 ax.annotate("%.2f" % p.get_height(), (p.get_x() + p.get_width() / 2., p.get_height()),
                     ha='center', va='center', fontsize=11, color='gray', xytext=(0, 20),
                     textcoords='offset points')

    conseq_plot.set_xticklabels(conseq_plot.get_xticklabels(), rotation=0)
    fig = conseq_plot.get_figure()

    fig.savefig(snakemake.output[0], bbox_inches = "tight",dpi = 100)
    fig.clf()
    return()

plot_coding(df)

def plot_nc(df):
    coding_conseqs = ['synonymous_variant','missense_variant', 'inframe_insertion','stop_gained,frameshift_variant','missense_variant,splice_region_variant']
    coding_df = df[df['Consequence'].isin(coding_conseqs)]
    coding_consequences = coding_df['Consequence'].value_counts().reset_index().rename(columns={'index': 'Consequence', 'Consequence': 'Count'})
    sns.set(rc={'figure.figsize':(30,20)})

    cd_conseq_plot = sns.barplot(x=coding_consequences['Consequence'],y=coding_consequences['Count'],palette='muted')

    ax=cd_conseq_plot
    for p in ax.patches:
                 ax.annotate("%.0f" % p.get_height(), (p.get_x() + p.get_width() / 2., p.get_height()),
                     ha='center', va='center', fontsize=11, color='gray', xytext=(0, 20),
                     textcoords='offset points')

    def change_width(ax, new_value) :
        for patch in ax.patches :
            current_width = patch.get_width()
            diff = current_width - new_value

            # we change the bar width
            patch.set_width(new_value)

            # we recenter the bar
            patch.set_x(patch.get_x() + diff * .5)
    change_width(ax, .90)
    cd_conseq_plot.set_xticklabels(cd_conseq_plot.get_xticklabels(), rotation=0)
    fig_2 = cd_conseq_plot.get_figure()

    fig_2.savefig(snakemake.output[1], bbox_inches = "tight",dpi = 100)
    fig_2.clf()
plot_nc(df)

def heatmap(final_df):
    sift_df = final_df[final_df['Consequence']=='missense_variant']
    races = ['angler_sattleschwein', 'berkshire', 'british_saddleback', 'bunte_bentheimer', 'calabrese', 'casertana', 'chato_murciano', 'cinta_senese', 'duroc', 'gloucester_old_spot', 'hampshire',  'landrace', 'large_black', 'large_white', 'leicoma', 'linderodsvin', 'mangalica', 'mangalica_blonde', 'mangalica_red', 'mangalica_swallow_belly','middle_white', 'negro_iberico', 'neijiang', 'nera_siciliana', 'pietrain',
    'retinto', 'tamworth','jinhua','wujin', 'meishan', 'penzhou', 'yanan','bearded_pig','visayan_warty_pig','wild_boar', 'common_warthog', 'sus_verrucosus']
    sift_df[['var_id','POS', 'REF','ALT', 'Consequence','SIFT']]

    sift_df_for_heatmap = sift_df[races].replace('NONE','NaN')
    sift_df_for_heatmap = sift_df_for_heatmap.astype(float)
    sift_df_for_heatmap['var_id']=sift_df['var_id']
    sift_df_for_heatmap.set_index('var_id', inplace=True)

    f, heatmap = plt.subplots(figsize=(25, 22))
    #sns.set(font_scale=0.5)
    #sns.set(rc={'figure.figsize':(30,22)})
    heatmap = sns.heatmap(sift_df_for_heatmap, linewidths=3,annot=True, fmt=".2f", cmap ='Reds', cbar=False,xticklabels=True)
    heatmap.set(title="Alternative allele frequency of each variant by breed", xlabel="Breeds",ylabel="Gene and variant position",)
    hmap = heatmap.get_figure()
    #sns.set(rc={'figure.figsize':(30,22)})
    hmap.savefig(snakemake.output[2], bbox_inches = "tight", dpi = 200)
    hmap.clf()
    return()
heatmap(df)
