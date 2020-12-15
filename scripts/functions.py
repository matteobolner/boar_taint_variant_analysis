import pandas as pd
import io

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
