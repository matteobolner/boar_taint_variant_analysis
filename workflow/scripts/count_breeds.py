import pandas as pd

df = pd.read_csv('/home/pelmo/data_and_pipelines/sscrofa_variant_remapping/data/vcf_files/headers/breeds_separated.txt', sep = "|", header=None)
df.columns=['id','breed']
df
new_df = pd.DataFrame(df['breed'].value_counts())
new_df =new_df.reset_index()
new_df.to_csv('/home/pelmo/data_and_pipelines/breeds.csv')
