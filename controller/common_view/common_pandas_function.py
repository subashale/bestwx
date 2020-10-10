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

# dataframe of missing rows
#df = file location
def missing_df(dfLoc, missingAre):
    print(missingAre)
    df = pd.read_csv(dfLoc, na_values=missingAre.split(","))
    # if len(missingAre) == 0:
    #     return df[df.isnull().any(axis=1)]
    # else:
    #     pd.read_csv(df, na_values=missingAre.split(","))

    return df[df.isnull().any(axis=1)]

def not_missing_df(dfLoc, missingAre):

    #if there is space before after ',' then remove

    df = pd.read_csv(dfLoc, na_values=missingAre.split(","))
    dfObj = df
    return dfObj.drop(missing_df(dfLoc, missingAre).index)

# dataframe of  count of missing data
def count_missing_df():
    pass