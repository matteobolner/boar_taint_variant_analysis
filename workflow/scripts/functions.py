
###OLD SCRIPT WITH REST FUNCTIONS FOR READING THE VCF AS A PD DATAFRAME AND
###USING THE VEP REST API 

import pandas as pd
import io
import requests, sys
import json


server = "https://rest.ensembl.org"

def read_vcf(path):
    info = []
    with open(path, 'r') as f:
        for l in f:
            if l.startswith('##'):
                info.append(l)
            elif l.startswith('#CHROM'):
                header=(l)
                break
    df = pd.read_csv(path, sep = "\t", comment = '#', header = None)
    header = header.rstrip(' \n').split('\t')
    df.columns = header
    return(df)

def vep(var_list):
    chunks = [var_list[x:x+200] for x in range(0, len(var_list), 200)]
    vep_output = []
    vep_df = pd.DataFrame([], columns = ['assembly_name', 'input', 'id', 'seq_region_name', 'strand', 'start', 'end', 'allele_string', 'most_severe_consequence', 'intergenic_consequences'])
    vep_df
    for chunk in chunks:
        var_list = json.dumps(chunk)
        ext = "/vep/sus_scrofa/region"
        headers={ "Content-Type" : "application/json", "Accept" : "application/json"}
        r = requests.post(server+ext, headers=headers, data='{ "variants" : ' + var_list + ' }')
        if not r.ok:
          r.raise_for_status()
          sys.exit()
        decoded = r.json()
        temp_df = pd.DataFrame.from_dict(decoded)
        vep_df = pd.concat([vep_df, temp_df ], ignore_index=True)
    vep_df['input'] = vep_df['input'].str.replace('\t', ' ')
    return(vep_df)
