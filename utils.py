import pandas as pd

def format_metadata_col(df, col, new_col):
    df[new_col] = df[col].str.lower()
    df[new_col] = df[new_col].str.replace('-', '_')
    df[new_col] = df[new_col].str.replace(' ', '_')
    return df

def process_encode_metadata(fname):
    df = pd.read_csv(fname, sep='\t')
    cols = ['Experiment accession', 'Biosample term name', 'File accession', 'Output type',
       'Biological replicate(s)', 'Technical replicate(s)']
    df = df[cols]
    df = format_metadata_col(df, 'Biosample term name', 'biosamp')
    df = format_metadata_col(df, 'Output type', 'output')

    # get biorep number for each experiment
    keep_cols = ['Experiment accession', 'biosamp']
    output_type_keep = df['output'].unique().tolist()[0]
    temp = df.loc[df['output'] == output_type_keep][keep_cols].copy(deep=True)
    temp['biorep'] = temp[keep_cols].groupby('biosamp').cumcount()+1
    temp.drop('biosamp', axis=1, inplace=True)

    # merge in biorep
    df = df.merge(temp, how='left', on='Experiment accession')

    return df