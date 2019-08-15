###for common_view function

import pandas as pd

def read_data(getFileLocation):
    # for finding delimiter to make general csv compatible, but has to create extra render object; overhead

    reader = pd.read_csv(getFileLocation, sep=None, iterator=True, engine='python')
    inferred_sep = reader._engine.data.dialect.delimiter

    # actual data frame created
    df = pd.read_csv(getFileLocation, sep=inferred_sep)
    return df

# make dataframe to read csv file and convert to list;
# no use, now list has been converted inside grid view function
# ;#

def make_df_list(getFileLocation):
    df = pd.read_csv(getFileLocation)

    df_list = [df.columns.values.tolist()] + df.values.tolist()

    return df_list

