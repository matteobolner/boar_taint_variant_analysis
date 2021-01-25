import csv
import matplotlib.pyplot as plt
import pandas as pd
import requests
import seaborn as sns
import sys
import os
import json
import pickle

a = pd.read_csv('/home/pelmo/data_and_pipelines/ena_databases/data/db_automated/9822_data/9822_database.csv')
project_ids = a['study_accession'].unique().tolist()

project_ids
headers={ "Content-Type" : "application/json"}
json_list = []
project_ids
df = pd.DataFrame(project_ids, columns = ['study_accession'])
df['xrefs'] = ''
df
for id in project_ids:
    r = requests.get('https://www.ebi.ac.uk/ena/xref/rest/json/search?accession=' + id, headers=headers)
    if r.ok:
        decoded = r.json()
        x = pd.DataFrame.from_records(decoded)
        #df['xref']=decoded

xref_df = pd.DataFrame.from_records(json_list)

xref_df
